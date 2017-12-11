#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

import sys
import os
from lib import utils

#1.判断必须是否传递备份文件名称
if len(sys.argv) < 2:
	print("you must set backupfilename!")
	sys.exit()

#2.判断设置的备份文件名是否已经存在
filename = sys.argv[1]
if os.path.exists(filename):
	print("%s already exists,please set another filename!" %(filename,))
	sys.exit()

if not os.path.exists(os.path.join("/usr/bin","pg_dump")):
	pg_dumpcmd = "cp -r packages/pg_dump /usr/bin"
	utils.execute_cmd(pg_dumpcmd, "安装pg_dump模块失败")
	chmodcmd = "chmod 777 /usr/bin/pg_dump"
	utils.execute_cmd(chmodcmd, "给pg_dump添加执行权限失败")

dbpassword =  utils.getdbpassword()

print("start backup database ......")
#pg_dump -F t -c -f/root/test.tar 'host=127.0.0.1 hostaddr=127.0.0.1 port=5432 user=nailgun password=vbTwv6mC dbname=nailgun'
#dbbackupcmd = 'pg_dump -b "host=127.0.0.1 hostaddr=127.0.0.1 port=5432 user=nailgun password=%s dbname=nailgun" > /root/mydb.bak' %(dbpassword,)
utils.setPasswordFile()
dbbackupcmd ="pg_dump -F t -c -f%s -U nailgun -d nailgun -h 127.0.0.1 " %(filename,)
print(dbbackupcmd)
utils.execute_cmd(dbbackupcmd,"备份数据库出现异常")
print("数据库备份%s成功!" %(filename,))










