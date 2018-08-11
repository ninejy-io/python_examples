redis-cli -h 127.0.0.1 -p 6379 MONITOR | head -n 10000 > ./tmp/monitor_log.txt
