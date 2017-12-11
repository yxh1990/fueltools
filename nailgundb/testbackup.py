#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys,os,time
import pexpect
from lib import utils

db_user = 'nailgun'
db_pwd = 'vbTwv6mC'
db_port = '5432'
db_name = 'nailgun'
backup_path = '/root/'
cmd_path = '/usr/bin/'
log_path = backup_path + 'log'

# 创建日志函数
def writeLogs(filename,contents):
  f = file(filename,'aw')
  f.write(contents)
  f.close()

today = backup_path + time.strftime('%Y-%m-%d')
fname = today + os.sep + time.strftime('%Y-%m-%d') + '_' + db_name + '.backup'

# 创建备份目录
# if not os.path.exists(today):
#    Msg = '-'*30 + time.strftime('%Y-%m-%d,%H:%M:%S') + '-'*30 + '\n'
#    if(os.mkdir(today)) == None:
#        Msg += '** 成功创建备份目录： ' + today + '\n\n'
#        writeLogs(log_path,Msg)
#    else:
#        Msg += '!! 创建备份目录： ' + today + '失败，请检查目录是否可写！\n\n'
#        writeLogs(log_path,Msg)
#        sys.exit()

# 备份nailgun数据库
cmd_dump = "%spg_dump -i -h localhost -p %s -U %s -F c -b -v -f %s %s" % \
               (cmd_path,db_port,db_user,fname,db_name)
print(cmd_dump)
cmd ="sh test.sh"
process = pexpect.spawn("/bin/bash", ["-c", cmd])
#index = process.expect(["(?i)password", pexpect.EOF, pexpect.TIMEOUT])

# # 执行备份命令
# if process.expect(["(?i)password"]) == 0:
# 	dbpassword = utils.getdbpassword()
# 	#print(dir(process))
# 	res=process.send(dbpassword)
# 	print(res)
# 	writeLogs(log_path,'数据备份为： ' + fname + '\n')
# else:
# 	writeLogs(log_path,'数据备份失败！\n')

