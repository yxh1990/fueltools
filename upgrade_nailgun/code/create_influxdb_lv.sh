set influxdb_space [exec vgs | grep dbvg | cut -d "." -f 2 | cut -d " " -f 2]
set influxdb_space [expr {$influxdb_space - 1}]
spawn lvcreate -L${influxdb_space}GB -n influxdb_lv dbvg
expect "signature detected on" { send "y\r" }