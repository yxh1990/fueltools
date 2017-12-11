#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

import os
from lib import utils
from lib import dbutils
import sys

#1.判断必须是否传递备份文件名称
if len(sys.argv) < 2:
	print("you must set recoveryfilename!")
	sys.exit()

#2.判断需要恢复文件名是否已经存在
filename = sys.argv[1]
if not os.path.exists(filename):
	print("%s file does not exist,Please set the correct file path!" %(filename,))
	sys.exit()

print("危险操作,建议执行恢复数据前先执行数据备份脚本,如果您确定要执行本次操作请在下面输入yes,按下回车键即可开始执行恢复!")
confirmsg = raw_input("确定执行输入(yes):")
if confirmsg != "yes":
	print("你取消了本次恢复数据操作!")
	pass
else:
	if not os.path.exists(os.path.join("/usr/bin","pg_restore")):
		cp_restorecmd = "cp -r packages/pg_restore /usr/bin"
		utils.execute_cmd(cp_restorecmd, "安装pg_restore模块失败")
		chmodcmd = "chmod 777 /usr/bin/pg_restore"
		utils.execute_cmd(chmodcmd, "给pg_restore添加执行权限失败")
	dbpassword =  utils.getdbpassword()
	#print("开始删除数据库的表")
	#dbutils.dropdb()
	#print("删除数据库所有表完毕")
	utils.setPasswordFile()
	restore_cmd = "pg_restore -U nailgun -c -n public -d nailgun -h 127.0.0.1 < %s" %(filename,)
	print(restore_cmd)
	utils.execute_cmd(restore_cmd,"恢复数据失败")
	print("成功恢复%s所有的数据,刷新浏览器后生效."%(filename,))
