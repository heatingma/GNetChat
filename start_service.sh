#!/bin/bash

# 清空log
> uwsgi.log

# 停止 Apache2 服务
/etc/init.d/apache2 stop

# 执行 uwsgi 命令
uwsgi --ini uwsgi.ini &

# 执行 daphne 命令
supervisord -c /etc/supervisord.conf &
supervisorctl start daphne &

# redis设置
sudo sysctl vm.overcommit_memory=1 &

# 启动 Redis 服务器
redis-server 

# 重启 Nginx
service nginx restart