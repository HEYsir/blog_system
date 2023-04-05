#! /bin/bash

set -e

CURDIR=$(cd "$(dirname "$0")";pwd)
echo $CURDIR

nginxconf=$CURDIR/nginx.conf
echo $nginxconf

echo "
# Stop dance for OpenResty
# =========================
#
# ExecStop sends SIGSTOP (graceful stop) to OpenResty's nginx process.
# If, after 5s (--retry QUIT/5) nginx is still running, systemd takes control
# and sends SIGTERM (fast shutdown) to the main process.
# After another 5s (TimeoutStopSec=5), and if nginx is alive, systemd sends
# SIGKILL to all the remaining processes in the process group (KillMode=mixed).
#
# nginx signals reference doc:
# http://nginx.org/en/docs/control.html
#
[Unit]
Description=The OpenResty Application Platform
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/var/log/nginx/nginx.pid
ExecStartPre=/usr/local/openresty/nginx/sbin/nginx -t -q -c $nginxconf -g 'daemon on; master_process on;' 
ExecStart=/usr/local/openresty/nginx/sbin/nginx -c $nginxconf -g 'daemon on; master_process on;' 
ExecReload=/usr/local/openresty/nginx/sbin/nginx -c $nginxconf -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /var/log/nginx/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
" > /usr/lib/systemd/system/openresty.service
