#! /bin/bash
set -x -e
PRJDIR=$(cd "$(dirname "$0")";pwd)
# nginx/openresty系统服务/usr/lib/systemd/system/openresty.service修改
# 指定配置文件
bash $PRJDIR/configure/server_openresty.sh

# 日志切片
# 这个实际是生成的临时配置，服务重启后丢失
# crontab -l > tmpcron 
# echo "0 0  * * * root  bash $PRJDIR/init.sh" >> tmpcron
# crontab tmpcron
# rm -f tmpcron
echo "* * * * * root ash $PRJDIR/logrotat.sh" >> /etc/crontab