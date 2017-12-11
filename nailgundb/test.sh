#!/bin/expect
set timeout 300
spawn pg_dump -h 127.0.0.1 -U nailgun nailgun > /root/ddd
expect "Password: "
send "vbTwv6mC\r"

