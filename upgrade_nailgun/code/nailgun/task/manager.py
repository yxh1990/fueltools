# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import traceback
import web
import os
from nailgun.objects.serializers.network_configuration \
    import NeutronNetworkConfigurationSerializer
from nailgun.objects.serializers.network_configuration \
    import NovaNetworkConfigurationSerializer

from nailgun.consts import CLUSTER_STATUSES
from nailgun.consts import NODE_STATUSES
from nailgun.consts import TASK_NAMES
from nailgun.consts import TASK_STATUSES
from nailgun.db import db
from nailgun.db.sqlalchemy.models import Cluster
from nailgun.db.sqlalchemy.models import Task
from nailgun.db.sqlalchemy.models import ClusterdeployMsg
from nailgun.db.sqlalchemy.models import Role
from nailgun.errors import errors
from nailgun.logger import logger
from nailgun import objects
from nailgun.openstack.common import jsonutils
import nailgun.rpc as rpc
from nailgun.task import task as tasks
from nailgun.task.task import TaskHelper
from nailgun.task import ebsStartall as ebs
from nailgun.task import onestStartall as onest
from nailgun.orchestrator import deployment_serializers
from nailgun.orchestrator import plugins_serializers
from nailgun.orchestrator import provisioning_serializers
from nailgun.settings import settings
from itertools import groupby
from operator import itemgetter


class TaskManager(object):

    def __init__(self, cluster_id=None):
        if cluster_id:
            self.cluster = db().query(Cluster).get(cluster_id)

    def _call_silently(self, task, instance, *args, **kwargs):
        # create action_log for task
        al = TaskHelper.create_action_log(task)

        method = getattr(instance, kwargs.pop('method_name', 'execute'))
        if task.status == TASK_STATUSES.error:
            TaskHelper.update_action_log(task, al)
            return
        try:
            to_return = method(task, *args, **kwargs)

            # update action_log instance for task
            # for asynchronous task it will be not final update
            # as they also are updated in rpc receiver
            TaskHelper.update_action_log(task, al)

            return to_return
        except Exception as exc:
            err = str(exc)
            if any([
                not hasattr(exc, "log_traceback"),
                hasattr(exc, "log_traceback") and exc.log_traceback
            ]):
                logger.error(traceback.format_exc())

            # update task entity with given data
            data = {'status': 'error',
                    'progress': 100,
                    'message': err}
            objects.Task.update(task, data)

            TaskHelper.update_action_log(task, al)

    def check_running_task(self, task_name):
        current_tasks = db().query(Task).filter_by(
            name=task_name
        )
        for task in current_tasks:
            if task.status == "running":
                raise errors.DumpRunning()
            elif task.status in ("ready", "error"):
                db().delete(task)
                db().commit()

    def serialize_network_cfg(self, cluster):
        serializer = {'nova_network': NovaNetworkConfigurationSerializer,
                      'neutron': NeutronNetworkConfigurationSerializer}
        return serializer[cluster.net_provider].serialize_for_cluster(cluster)


class ApplyChangesTaskManager(TaskManager):
    def _lock_required_tasks(self):
        names = (
            TASK_NAMES.deploy,
            TASK_NAMES.stop_deployment,
            TASK_NAMES.reset_environment
        )
        return objects.TaskCollection.lock_cluster_tasks(
            cluster_id=self.cluster.id, names=names
        )

    def _remove_obsolete_tasks(self):
        locked_tasks = self._lock_required_tasks()
        current_tasks = objects.TaskCollection.filter_by(
            locked_tasks,
            name=TASK_NAMES.deploy
        )
        for task in current_tasks:
            if task.status == TASK_STATUSES.running:
                db().commit()
                raise errors.DeploymentAlreadyStarted()
            elif task.status in (TASK_STATUSES.ready, TASK_STATUSES.error):
                db().delete(task)
        db().flush()

        obsolete_tasks = objects.TaskCollection.filter_by_list(
            locked_tasks,
            'name',
            (TASK_NAMES.stop_deployment, TASK_NAMES.reset_environment)
        )
        for task in obsolete_tasks:
            db().delete(task)
        db().flush()

    def get_task_deploy_msg(self):
        deploy_task = db().query(ClusterdeployMsg).filter_by(
            cluster_id=self.cluster.id
        ).first()
        if deploy_task:
           return deploy_task.cluster_deploymsg
        else:
           return "there is no old cluster_deploymsg"


    def execute(self):
        #开始执行部署变更
        logger.info(
            u"Trying to start deployment at cluster '{0}'".format(
                self.cluster.name or self.cluster.id
            )
        )
        #显示网络信息(openstack部署前执行网络验证)
        network_info = self.serialize_network_cfg(self.cluster)
        logger.info(
            u"Network info:\n{0}".format(
                jsonutils.dumps(network_info, indent=4)
            )
        )

        self._remove_obsolete_tasks() #obsolete 过时的

        supertask = Task(name=TASK_NAMES.deploy, cluster=self.cluster)
        db().add(supertask)

        nodes_to_delete = TaskHelper.nodes_to_delete(self.cluster)
        nodes_to_deploy = TaskHelper.nodes_to_deploy(self.cluster)
        nodes_to_provision = TaskHelper.nodes_to_provision(self.cluster)

        task_messages = []
        #如果是openstack环境,就执行原来流程判断看集群中是否有节点的变化
        if self.cluster.cluster_type==1:
           if not any([nodes_to_provision, nodes_to_deploy, nodes_to_delete]):
              db().rollback()
              raise errors.WrongNodeStatus("No changes to deploy")

        # we should have task committed for processing in other threads
        db().commit()
        TaskHelper.create_action_log(supertask)

        # Run validation if user didn't redefine
        # provisioning and deployment information

        if (not objects.Cluster.get_provisioning_info(self.cluster) and
                not objects.Cluster.get_deployment_info(self.cluster)):
            try:
                if self.cluster.cluster_type==1:
                   self.check_before_deployment(supertask)
            except errors.CheckBeforeDeploymentError:
                db().commit()
                return supertask

        task_deletion, task_provision, task_deployment = None, None, None

        if nodes_to_delete:
            objects.TaskCollection.lock_cluster_tasks(self.cluster.id)
            # For more accurate progress calculation
            task_weight = 0.4
            task_deletion = supertask.create_subtask(TASK_NAMES.node_deletion,
                                                     weight=task_weight)
            logger.debug("Launching deletion task: %s", task_deletion.uuid)

            self._call_silently(task_deletion, tasks.DeletionTask)
            # we should have task committed for processing in other threads
            db().commit()

        if nodes_to_provision:
            objects.TaskCollection.lock_cluster_tasks(self.cluster.id)
            # updating nodes
            nodes_to_provision = objects.NodeCollection.lock_nodes(
                nodes_to_provision
            )
            objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_provision)
            logger.debug("There are nodes to provision: %s",
                         " ".join([n.fqdn for n in nodes_to_provision]))

            # For more accurate progress calulation
            task_weight = 0.4
            task_provision = supertask.create_subtask(TASK_NAMES.provision,
                                                      weight=task_weight)

            # we should have task committed for processing in other threads
            db().commit()
            provision_message = self._call_silently(
                task_provision,
                tasks.ProvisionTask,
                nodes_to_provision,
                method_name='message'
            )

            task_provision = objects.Task.get_by_uid(
                task_provision.id,
                fail_if_not_found=True,
                lock_for_update=True
            )
            # if failed to generate task message for orchestrator
            # then task is already set to error
            if task_provision.status == TASK_STATUSES.error:
                return supertask

            task_provision.cache = provision_message
            db().commit()
            task_messages.append(provision_message)
        else:
            pass

        #nodes_to_deploy=self.cluster.nodes
        if nodes_to_deploy:
            objects.TaskCollection.lock_cluster_tasks(self.cluster.id)
            # locking nodes before updating
            objects.NodeCollection.lock_nodes(nodes_to_deploy)
            # updating nodes
            objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_deploy)
            logger.debug("There are nodes to deploy: %s",
                         " ".join([n.fqdn for n in nodes_to_deploy]))
            task_deployment = supertask.create_subtask(TASK_NAMES.deployment)

            # we should have task committed for processing in other threads
            db().commit()
            deployment_message = self._call_silently(
                task_deployment,
                tasks.DeploymentTask,
                nodes_to_deploy,
                method_name='message'
            )
            
            # clusterdeploymsg = ClusterdeployMsg(cluster_id=self.cluster.id,cluster_deploymsg='deployment_message')
            # db().add(clusterdeploymsg)
            # clusterdeploymsg只要保存状态为new的部署信息,如果第一次部署失败有错误节点
            # 第二次点击部署变更的时候会只会发送消息给错误节点,这样的信息覆盖掉第一次
            # 完整的部署信息会导致集群启动和停止的失败(因为只发送给错误节点).
            logger.info(u'执行部署变更操作,开始操作cluster_deploy_msg表')
            data={}
            data['cluster_id']=self.cluster.id
            data['cluster_deploymsg']=jsonutils.dumps(deployment_message)
            clusterdeploymsg=db().query(ClusterdeployMsg).filter_by(cluster_id=self.cluster.id).first()
           
            if clusterdeploymsg:
                if self.cluster.status == CLUSTER_STATUSES.new:
                   objects.ClusterdeployMsgObject.update(clusterdeploymsg,{'cluster_deploymsg':data['cluster_deploymsg']})
            else:
                objects.ClusterdeployMsgCollection.create(data)
            

            task_deployment = objects.Task.get_by_uid(
                task_deployment.id,
                fail_if_not_found=True,
                lock_for_update=True
            )
            # if failed to generate task message for orchestrator
            # then task is already set to error
            if task_deployment.status == TASK_STATUSES.error:
                return supertask

            task_deployment.cache = deployment_message
            db().commit()
            task_messages.append(deployment_message)
        else:
            pass
        if len(nodes_to_delete)<=0 and len(nodes_to_deploy)<=0: 
            #这里不能单纯用nodes_to_deploy是否为空来判断是启动或者停止
            #因为nodes_to_delete不为空而nodes_to_deploy为空的话依然会
            #执行下面的代码,此种情况程序会出现异常
            
            oprolename = web.cookies().get("oprolename")
            opaction   = web.cookies().get("opaction")
            nodes_to_startorstop=TaskHelper.nodes_to_startorstop(self.cluster)
            if oprolename !="all":
               logger.info(u'这里执行的是单角色启动或者停止部署')
               task_deployment = supertask.create_subtask(TASK_NAMES.deployment)

               # we should have task committed for processing in other threads
               # openstack定制化环境点击部署变更和启动,停止按钮没有执行
               # 此程序,而是直接通过调用/opt/start.py执行
               # 目前只有cloudmaster和ebs环境会执行此处代码
               db().commit()
               
               deployment_message = self._call_silently(
                 task_deployment,
                 tasks.DeploymentTask,
                 nodes_to_startorstop,
                 method_name='message'
               )
               deploymsg=deployment_message
               deploymsg['respond_to']="start_stop_resp"
               deploymsg['args']['task_uuid']=task_deployment.uuid
               #deployment_info[]是列表,这个列表中含有的元素都是字典
               #角色下面的label参数就只是在此处添加和修改的.
               deployment_info_old_list=deploymsg['args']['deployment_info']
               deployment_info_list=[]
               nodeuids=[];
               for key,item in groupby(deployment_info_old_list,itemgetter('uid')):
                   nodeuids.append(key)

               deployment_info_list=deployment_info_old_list[0:len(nodeuids)]
               #此处删除和启动停止无关的角色信息
               deploymsg['args']['deployment_info']=[]
               for i in range(len(deployment_info_list)):
                   deployment_info=deployment_info_list[i]
                   deployment_info["role"]=oprolename
                   deployment_info["uid"]=nodeuids[i]
                   deploymsg['args']['deployment_info'].append(deployment_info)


               for deployment_info in deployment_info_list:  #此处是一个列表
                   deployment_info_keys=deployment_info.keys()  
                   changelable_keys=[]
                   operationalrole=""
                   for key in deployment_info_keys:
                       if key.lower() == oprolename.lower():
                          operationalrole=key
                       else:
                          changelable_keys.append(key)
                
                   deployment_info[operationalrole]['action']=opaction
                   deployment_info[operationalrole]['label']='0'
                   for key in changelable_keys:
                       if type(deployment_info[key])==dict and deployment_info[key].get('label')!=None:
                          deployment_info[key]['label']='1'  

               logger.info(deployment_info[operationalrole]['action'])
               logger.info(oprolename)    

               task_deployment = objects.Task.get_by_uid(
                   task_deployment.id,
                   fail_if_not_found=True,
                   lock_for_update=True
               )
               # if failed to generate task message for orchestrator
               # then task is already set to error
               if task_deployment.status == TASK_STATUSES.error:
                  return supertask

               task_deployment.cache = deploymsg
               db().commit()
               task_messages.append(deploymsg)

            else:
               logger.info(u'这里执行的是一键启动和停止操作')
               serialized_cluster = deployment_serializers.serialize(
                 self.cluster, nodes_to_startorstop)
               pre_deployment = plugins_serializers.pre_deployment_serialize(
                 self.cluster, nodes_to_startorstop)
               post_deployment = plugins_serializers.post_deployment_serialize(
                 self.cluster, nodes_to_startorstop)
               deployment_message=self.make_astute_message(
                 'deploy',
                 'deploy_resp',
                 {
                  'deployment_info': serialized_cluster,
                  'pre_deployment': pre_deployment,
                  'post_deployment': post_deployment
                 }
               )
               if self.cluster.cluster_type == 3:
                  ebs_start=ebs.StartAllRole()
                  if opaction == "stop":
                     task_messages=ebs_start.make_deploy_msgs(self.cluster,supertask,deployment_message,1)
                  else:
                     task_messages=ebs_start.make_deploy_msgs(self.cluster,supertask,deployment_message,2)
               else:
                 pass


        if nodes_to_provision:
            nodes_to_provision = objects.NodeCollection.lock_nodes(
                nodes_to_provision
            )
            for node in nodes_to_provision:
                node.status = NODE_STATUSES.provisioning
            db().commit()

        objects.Cluster.get_by_uid(
            self.cluster.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        self.cluster.status = CLUSTER_STATUSES.deployment
        db().add(self.cluster)
        db().commit()

        if task_messages:
              rpc.cast('naily', task_messages)
            
        logger.debug(
            u"Deployment: task to deploy cluster '{0}' is {1}".format(
                self.cluster.name or self.cluster.id,
                supertask.uuid
            )
        )
        return supertask

    def make_astute_message(self,method, respond_to, args):
       message = {
         'api_version': settings.VERSION['api'],
         'method': method,
         'respond_to': respond_to,
         'args': args
       }
       return message

    def check_before_deployment(self, supertask):
        # checking admin intersection with untagged
        network_info = self.serialize_network_cfg(self.cluster)
        network_info["networks"] = [
            n for n in network_info["networks"] if n["name"] != "fuelweb_admin"
        ]

        check_networks = supertask.create_subtask(TASK_NAMES.check_networks)

        self._call_silently(
            check_networks,
            tasks.CheckNetworksTask,
            data=network_info,
            check_admin_untagged=True
        )

        if check_networks.status == TASK_STATUSES.error:
            logger.warning(
                "Checking networks failed: %s", check_networks.message
            )
            raise errors.CheckBeforeDeploymentError(check_networks.message)
        TaskHelper.set_ready_if_not_finished(check_networks)
        db().delete(check_networks)
        db().refresh(supertask)
        db().flush()

        # checking prerequisites
        check_before = supertask.create_subtask(
            TASK_NAMES.check_before_deployment
        )
        logger.debug("Checking prerequisites task: %s", check_before.uuid)

        self._call_silently(
            check_before,
            tasks.CheckBeforeDeploymentTask
        )

        # if failed to check prerequisites
        # then task is already set to error
        if check_before.status == TASK_STATUSES.error:
            logger.warning(
                "Checking prerequisites failed: %s", check_before.message
            )
            raise errors.CheckBeforeDeploymentError(check_before.message)
        logger.debug(
            "Checking prerequisites is successful, starting deployment..."
        )
        TaskHelper.set_ready_if_not_finished(check_before)
        db().delete(check_before)
        db().refresh(supertask)
        db().flush()


class ProvisioningTaskManager(TaskManager):

    def execute(self, nodes_to_provision):
        """Run provisioning task on specified nodes
        """
        # locking nodes
        nodes_ids = [node.id for node in nodes_to_provision]
        nodes = objects.NodeCollection.filter_by_list(
            None,
            'id',
            nodes_ids,
            order_by='id'
        )
        objects.NodeCollection.lock_for_update(nodes).all()

        objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_provision)
        logger.debug('Nodes to provision: {0}'.format(
            ' '.join([n.fqdn for n in nodes_to_provision])))

        task_provision = Task(name='provision', cluster=self.cluster)
        db().add(task_provision)
        db().commit()

        provision_message = self._call_silently(
            task_provision,
            tasks.ProvisionTask,
            nodes_to_provision,
            method_name='message'
        )

        task_provision = objects.Task.get_by_uid(
            task_provision.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        task_provision.cache = provision_message
        objects.NodeCollection.lock_for_update(nodes).all()

        for node in nodes_to_provision:
            node.pending_addition = False
            node.status = NODE_STATUSES.provisioning
            node.progress = 0

        db().commit()

        rpc.cast('naily', provision_message)

        return task_provision


class DeploymentTaskManager(TaskManager):

    def execute(self, nodes_to_deployment):
        # locking nodes for update
        objects.NodeCollection.lock_nodes(nodes_to_deployment)
        objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_deployment)

        logger.debug('Nodes to deploy: {0}'.format(
            ' '.join([n.fqdn for n in nodes_to_deployment])))
        task_deployment = Task(name='deployment', cluster=self.cluster)
        db().add(task_deployment)

        deployment_message = self._call_silently(
            task_deployment,
            tasks.DeploymentTask,
            nodes_to_deployment,
            method_name='message')

        db().refresh(task_deployment)

        # locking task
        task_deployment = objects.Task.get_by_uid(
            task_deployment.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        # locking nodes
        objects.NodeCollection.lock_nodes(nodes_to_deployment)

        task_deployment.cache = deployment_message

        for node in nodes_to_deployment:
            node.status = 'deploying'
            node.progress = 0

        db().commit()

        rpc.cast('naily', deployment_message)

        return task_deployment


class StopDeploymentTaskManager(TaskManager):

    def execute(self):
        # locking tasks for processing
        names = (
            TASK_NAMES.stop_deployment,
            TASK_NAMES.deployment,
            TASK_NAMES.provision
        )
        objects.TaskCollection.lock_cluster_tasks(
            self.cluster.id,
            names=names
        )

        stop_running = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id,
            name=TASK_NAMES.stop_deployment,
        )
        stop_running = objects.TaskCollection.order_by(
            stop_running, 'id'
        ).first()

        if stop_running:
            if stop_running.status == TASK_STATUSES.running:
                raise errors.StopAlreadyRunning(
                    "Stopping deployment task "
                    "is already launched"
                )
            else:
                db().delete(stop_running)
                db().flush()

        deployment_task = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id,
            name=TASK_NAMES.deployment,
        )
        deployment_task = objects.TaskCollection.order_by(
            deployment_task, 'id'
        ).first()

        provisioning_task = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id,
            name=TASK_NAMES.provision,
        )
        provisioning_task = objects.TaskCollection.order_by(
            provisioning_task, 'id'
        ).first()

        if not deployment_task and not provisioning_task:
            db().rollback()
            raise errors.DeploymentNotRunning(
                u"Nothing to stop - deployment is "
                u"not running on environment '{0}'".format(
                    self.cluster.id
                )
            )

        task = Task(
            name="stop_deployment",
            cluster=self.cluster
        )
        db().add(task)
        db().commit()
        self._call_silently(
            task,
            tasks.StopDeploymentTask,
            deploy_task=deployment_task,
            provision_task=provisioning_task
        )
        return task


class ResetEnvironmentTaskManager(TaskManager):

    def execute(self):
        deploy_running = db().query(Task).filter_by(
            cluster=self.cluster,
            name='deploy',
            status='running'
        ).first()
        if deploy_running:
            raise errors.DeploymentAlreadyStarted(
                u"Can't reset environment '{0}' when "
                u"deployment is running".format(
                    self.cluster.id
                )
            )

        obsolete_tasks = db().query(Task).filter_by(
            cluster_id=self.cluster.id,
        ).filter(
            Task.name.in_([
                'deploy',
                'deployment',
                'stop_deployment'
            ])
        )
        for task in obsolete_tasks:
            db().delete(task)
        db().commit()

        task = Task(
            name="reset_environment",
            cluster=self.cluster
        )
        db().add(task)
        db.commit()
        self.deleteoptfile()
        self._call_silently(
            task,
            tasks.ResetEnvironmentTask
        )
        return task

    def deleteoptfile(self):
        jsondir="/opt/%s" %(self.cluster.id)
        openstackinifile = "/opt/openstack_init_%s" %(self.cluster.id)
        role_ip_mapfile = "/opt/role_ip_map_%s.json" %(self.cluster.id)
        if os.path.exists(jsondir):
           os.popen('rm -rf %s' %(jsondir))
           logger.info("success delete dir %s" %(jsondir))
        if os.path.exists(openstackinifile):
           os.popen("rm -rf %s" %(openstackinifile))
           logger.info("success delete file %s" %(openstackinifile))
        if os.path.exists(role_ip_mapfile):
           os.popen("rm -rf %s" %(role_ip_mapfile))
           logger.info("success delete file %s" %(role_ip_mapfile))

class UpdateEnvironmentTaskManager(TaskManager):

    def execute(self):
        if not self.cluster.pending_release_id:
            raise errors.InvalidReleaseId(
                u"Can't update environment '{0}' when "
                u"new release Id is invalid".format(self.cluster.name))

        running_tasks = db().query(Task).filter_by(
            cluster_id=self.cluster.id,
            status='running'
        ).filter(
            Task.name.in_([
                'deploy',
                'deployment',
                'reset_environment',
                'stop_deployment'
            ])
        )
        if running_tasks.first():
            raise errors.TaskAlreadyRunning(
                u"Can't update environment '{0}' when "
                u"other task is running".format(
                    self.cluster.id
                )
            )

        nodes_to_change = TaskHelper.nodes_to_upgrade(self.cluster)
        objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_change)
        logger.debug('Nodes to update: {0}'.format(
            ' '.join([n.fqdn for n in nodes_to_change])))
        task_update = Task(name='update', cluster=self.cluster)
        db().add(task_update)
        self.cluster.status = 'update'
        db().flush()

        deployment_message = self._call_silently(
            task_update,
            tasks.UpdateTask,
            nodes_to_change,
            method_name='message')

        db().refresh(task_update)

        for node in nodes_to_change:
            node.status = 'deploying'
            node.progress = 0

        db().commit()
        rpc.cast('naily', deployment_message)

        return task_update


class CheckNetworksTaskManager(TaskManager):

    def execute(self, data, check_admin_untagged=False):
        locked_tasks = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id,
            name=TASK_NAMES.check_networks
        )
        locked_tasks = objects.TaskCollection.order_by(locked_tasks, 'id')
        check_networks = objects.TaskCollection.lock_for_update(
            locked_tasks
        ).first()
        if check_networks:
            TaskHelper.set_ready_if_not_finished(check_networks)
            db().delete(check_networks)
            db().flush()

        task = Task(
            name=TASK_NAMES.check_networks,
            cluster=self.cluster
        )
        db().add(task)
        db().commit()
        self._call_silently(
            task,
            tasks.CheckNetworksTask,
            data,
            check_admin_untagged
        )

        task = objects.Task.get_by_uid(
            task.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        if task.status == TASK_STATUSES.running:
            # update task status with given data
            data = {'status': TASK_STATUSES.ready, 'progress': 100}
            objects.Task.update(task, data)
        db().commit()
        return task


class VerifyNetworksTaskManager(TaskManager):
    #这两种状态不能进行验证网络
    _blocking_statuses = (
        CLUSTER_STATUSES.deployment,
        CLUSTER_STATUSES.update,
    )

    def remove_previous_task(self):
        locked_tasks = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id
        )
        locked_tasks = objects.TaskCollection.filter_by_list(
            locked_tasks,
            'name',
            (TASK_NAMES.check_networks, TASK_NAMES.verify_networks),
            order_by='id'
        )
        locked_tasks = objects.TaskCollection.lock_for_update(
            locked_tasks
        ).all()

        check_networks = objects.TaskCollection.filter_by(
            locked_tasks,
            name=TASK_NAMES.check_networks
        )
        check_networks = list(check_networks)

        if check_networks:
            db().delete(check_networks[0])
            db().flush()

        verification_tasks = objects.TaskCollection.filter_by(
            locked_tasks,
            name=TASK_NAMES.verify_networks
        )
        verification_tasks = list(verification_tasks)

        if verification_tasks:
            ver_task = verification_tasks[0]
            if ver_task.status == TASK_STATUSES.running:
                raise errors.CantRemoveOldVerificationTask()
            for subtask in ver_task.subtasks:
                db().delete(subtask)
            db().delete(ver_task)
            db().flush()

    def execute(self, nets, vlan_ids):
        self.remove_previous_task()

        task = Task(
            name=TASK_NAMES.check_networks,
            cluster=self.cluster
        )

        if len(self.cluster.nodes) < 2:
            task.status = TASK_STATUSES.error
            task.progress = 100
            task.message = ('At least two nodes are required to be '
                            'in the environment for network verification.')
            db().add(task)
            db().commit()
            return task

        if len(self.cluster.node_groups) > 1:
            task.status = TASK_STATUSES.error
            task.progress = 100
            task.message = ('Network verfiication is disabled for '
                            'environments containing more than one node '
                            'group.')
            db().add(task)
            db().commit()
            return task

        if self.cluster.status in self._blocking_statuses:
            task.status = TASK_STATUSES.error
            task.progress = 100
            task.message = (
                "Environment is not ready to run network verification "
                "because it is in '{0}' state.".format(self.cluster.status)
            )
            db().add(task)
            db().commit()
            return task

        db().add(task)
        db().commit()

        self._call_silently(
            task,
            tasks.CheckNetworksTask,
            data=nets,
            check_admin_untagged=True
        )
        db().refresh(task)
        #1.先进行CheckNetworksTask,然后按照返回结果再进行调用
        #    CheckNetworksTask调用的是nailgun.network.checker.py
        #    这里面的检测代码是在nailgun中
        #2.如果CheckNetworksTask没有返回错误,便在此task基础上
        #  创建一个verify_task,然后给此verify_task创建两个子task
        #  CheckDhcpTask和MulticastVerificationTask
        #  
        if task.status != TASK_STATUSES.error:
            # this one is connected with UI issues - we need to
            # separate if error happened inside nailgun or somewhere
            # in the orchestrator, and UI does it by task name.
            task.name = TASK_NAMES.verify_networks
            verify_task = tasks.VerifyNetworksTask(task, vlan_ids)

            if tasks.CheckDhcpTask.enabled(self.cluster):
                dhcp_subtask = objects.task.Task.create_subtask(
                    task, name=TASK_NAMES.check_dhcp)
                verify_task.add_subtask(tasks.CheckDhcpTask(
                    dhcp_subtask, vlan_ids))

            if tasks.MulticastVerificationTask.enabled(self.cluster):
                multicast = objects.task.Task.create_subtask(
                    task, name=TASK_NAMES.multicast_verification)
                verify_task.add_subtask(
                    tasks.MulticastVerificationTask(multicast))

            db().commit()
            self._call_silently(task, verify_task)

        return task


class ClusterDeletionManager(TaskManager):

    def execute(self):
        # locking required tasks
        locked_tasks = objects.TaskCollection.lock_cluster_tasks(
            self.cluster.id
        )
        # locking cluster
        objects.Cluster.get_by_uid(
            self.cluster.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        # locking nodes
        nodes = objects.NodeCollection.filter_by(
            None,
            cluster_id=self.cluster.id
        )
        nodes = objects.NodeCollection.order_by(nodes, 'id')
        objects.NodeCollection.lock_for_update(nodes).all()

        current_cluster_tasks = objects.TaskCollection.filter_by_list(
            locked_tasks,
            'name',
            (TASK_NAMES.cluster_deletion,)
        )

        deploy_running = objects.TaskCollection.filter_by(
            None,
            cluster_id=self.cluster.id,
            name=TASK_NAMES.deploy,
            status=TASK_STATUSES.running
        )
        deploy_running = objects.TaskCollection.order_by(
            deploy_running,
            'id'
        ).first()
        if deploy_running:
            logger.error(
                u"Deleting cluster '{0}' "
                "while deployment is still running".format(
                    self.cluster.name
                )
            )

        logger.debug("Removing cluster tasks")
        for task in current_cluster_tasks:
            if task.status == TASK_STATUSES.running:
                db().rollback()
                raise errors.DeletionAlreadyStarted()
            elif task.status in (TASK_STATUSES.ready, TASK_STATUSES.error):
                for subtask in task.subtasks:
                    db().delete(subtask)
                db().delete(task)
        db().flush()

        logger.debug("Labeling cluster nodes to delete")
        for node in self.cluster.nodes:
            node.pending_deletion = True
            db().add(node)
        db().flush()

        self.cluster.status = CLUSTER_STATUSES.remove
        db().add(self.cluster)

        logger.debug("Creating cluster deletion task")
        task = Task(name="cluster_deletion", cluster=self.cluster)
        db().add(task)
        db().commit()
        self._call_silently(
            task,
            tasks.ClusterDeletionTask
        )
        return task


class DumpTaskManager(TaskManager):

    def execute(self):
        logger.info("Trying to start dump_environment task")
        self.check_running_task('dump')

        task = Task(name="dump")
        db().add(task)
        db().commit()
        self._call_silently(
            task,
            tasks.DumpTask,
        )
        return task


class GenerateCapacityLogTaskManager(TaskManager):

    def execute(self):
        logger.info("Trying to start capacity_log task")
        self.check_running_task('capacity_log')

        task = Task(name='capacity_log')
        db().add(task)
        db().commit()
        self._call_silently(
            task,
            tasks.GenerateCapacityLogTask)
        return task



class InstallosTaskManager(TaskManager):

    def execute(self, nodes_to_provision):
        """Run provisioning task on specified nodes
        """
        # locking nodes
        nodes_ids = [node.id for node in nodes_to_provision]
        nodes = objects.NodeCollection.filter_by_list(
            None,
            'id',
            nodes_ids,
            order_by='id'
        )
        objects.NodeCollection.lock_for_update(nodes).all()

        objects.NodeCollection.update_slave_nodes_fqdn(nodes_to_provision)
        logger.debug('Nodes to provision: {0}'.format(
            ' '.join([n.fqdn for n in nodes_to_provision])))

        task_provision = Task(name='provision')
        task_provision.node_ids=nodes_ids 
        #node_ids参数在安装成功时候无用,但在安装失败的时候需要用到
        db().add(task_provision)
        db().commit()

        provision_message = self._call_silently(
            task_provision,
            tasks.InstallosTask,
            nodes_to_provision,
            method_name='message'
        )

        task_provision = objects.Task.get_by_uid(
            task_provision.id,
            fail_if_not_found=True,
            lock_for_update=True
        )
        task_provision.cache = provision_message
        objects.NodeCollection.lock_for_update(nodes).all()

        for node in nodes_to_provision:
            node.pending_addition = False
            node.status = NODE_STATUSES.provisioning
            node.progress = 0

        db().commit()

        rpc.cast('naily', provision_message)
        logger.info(u'消息发送完毕')
        return task_provision

