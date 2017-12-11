1.agent 放到 /opt/nailgun/bin/agent目录 
  要修改成777执行权限
  此文件用途用于收集agent节点的具体信息

  调试agent > ruby agent 直接像python 文件一样在命令行调试执行
  单独使用ruby agent 只能一次发送一次http请求,有时候会超时,所以才会使用
  定时任务不断的重复发送请求.

2.nailgun-agent 放到 /etc/cron.d 目录下,放到此目录下后会自动生效执行,无需另外操作.
  此文件启动定时任务反复执行agent里面的代码.
  flock -w 5 -o /var/lock/agent.lock -c "/opt/nailgun/bin/agent 2>&1 | tee -a /var/log/nailgun-agent.log  | /usr/bin/logger -t nailgun-agent"

  调试日志
    tail -f 200 /var/log/nailgun-agent.log


3.config.yaml  /etc/nailgun-agent/config.yaml
  agent里面需要用到的配置信息数据存放到此文件中.

4.ruby执行环境准备
 1./usr/bin/ruby ruby文件需要777权限
    把rubyenv中的bin下的ruby文件 复制到 /usr/bin目录下
   /usr/bin/gem gem文件需要777权限
    把rubyenv中bin下的gem文件 复制到/usr/bin目录下

 2./usr/lib/ruby
   把rubyenv中的lib目录下的ruby目录 复制到 /usr/lib目录下

 3./usr/lib64/ruby
   把rubyenv中的lib64目录下的ruby目录 复制到 /usr/lib64目录下

 4./usr/lib64
   把rubyenv中libso中的两个so文件 复制到  /usr/lib64目录下

5.创建lock文件
  /var/lock/agent.lock

6.创建日志文件
  /var/log/nailgun-agent.log 
  修改日志的权限为777

7.创建文件/etc/nailgun_systemtype
  内容为 bootstrap

8.agent根据/etc/nailgun_uid这个文件是否存在,如果不存在就用post否则用put.



