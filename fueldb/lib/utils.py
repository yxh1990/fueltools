#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author yanxianghui

import sys
import yaml
import subprocess
import os

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

def getdbpassword():
	fr = open('/etc/fuel/astute.yaml', 'r')
	data = yaml.load(fr)
	dbpassword = data["postgres"]["nailgun_password"]
	fr.close()
	return dbpassword

def setPasswordFile():
	filepathname="/root/.pgpass"
	if not os.path.exists(filepathname):
		f = open(filepathname,'w+')
		f.write("*:5432:nailgun:nailgun:%s" %(getdbpassword(),))
		f.close()
		chmodcmd = "chmod 0600 /root/.pgpass"
		execute_cmd(chmodcmd,"设置密码文件的权限失败")


