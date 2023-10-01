#!/bin/bash

# 停止 uwsgi 进程
uwsgi --stop uwsgi.pid

# 停止 daphne 进程
pkill -f "daphne website.asgi:application"

# 停止 Redis 服务器
redis-cli shutdown

# 停止 Nginx 服务器
service nginx stop

# 启动 Apache2 服务器
/etc/init.d/apache2 start