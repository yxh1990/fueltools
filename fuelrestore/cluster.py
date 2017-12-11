#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

import subprocess
import sys
import os


#1.判断必须是否传递集群名称
if len(sys.argv) < 2:
	print("you must set clustername!")
	sys.exit()

cluster_name = sys.argv[1]

def execute_cmd(cmd, customer_errmsg):
	res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	res.wait()
	readmsg = res.stdout.read().strip()
	errormsg = res.stderr.read()

	if errormsg:
		print(errormsg)
		print(customer_errmsg)
		sys.exit()
	else:
		return readmsg


if os.path.exists('/usr/lib/python2.6/site-packages/sqlalchemy'):
	print("当前节点上已经安装sqlalchemy,自动跳过安装步骤....")
else:
	sqlalchemycmd = "cp -r packages/sqlalchemy /usr/lib/python2.6/site-packages"
	execute_cmd(sqlalchemycmd, "安装sqlalchemy模块失败")

	pg2cmd = "cp -r packages/psycopg2 /usr/lib/python2.6/site-packages"
	execute_cmd(pg2cmd, "安装数据库驱动模块失败")


import json
import yaml
from sqlalchemy import create_engine

fr = open('/etc/fuel/astute.yaml', 'r')
data = yaml.load(fr)
dbpassword=data["postgres"]["nailgun_password"]
fr.close()
engine = create_engine("postgresql://nailgun:{0}@127.0.0.1:5432/nailgun".format(dbpassword),client_encoding="utf-8")

selectcmd="select id from clusters WHERE  name ='"+cluster_name+"'"
result=engine.execute(selectcmd)
#print(dir(result))
#print(result.first().id)
res = result.first()
if res:
	updatecmd = "update clusters set status='operational' where id ="+str(res.id)
	engine.execute(updatecmd)
	#updatecmd2 = "update clusters set replaced_deployment_info='sucess' where id =" + str(res.id)
	#engine.execute(updatecmd2)
	deltetaskcmd = "delete from tasks where cluster_id="+str(res.id)
	engine.execute(deltetaskcmd)
else:
	print("the database has no cluster")
	sys.exit()
engine.dispose()
print("the database is rollback.....")

