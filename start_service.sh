#!/bin/bash

# 清空log
> uwsgi.log

# 停止 Apache2 服务
# /etc/init.d/apache2 stop

# 执行 uwsgi 命令
uwsgi --ini uwsgi.ini &

# 执行 daphne 命令
daphne website.asgi:application -b 0.0.0.0 -p 6002 &

# 启动 Redis 服务器
redis-server &

# 重启 Nginx
service nginx restart