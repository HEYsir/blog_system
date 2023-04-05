#! /bin/bash
set -x -e
PRJDIR=$(cd "$(dirname "$0")";pwd)

# 日志切片
# 这个实际是生成的临时配置，服务重启后丢失
# crontab -l > tmpcron 
# echo "0 0  * * * root  bash $PRJDIR/init.sh" >> tmpcron
# crontab tmpcron
# rm -f tmpcron
echo "* * * * * root ash $PRJDIR/logrotat.sh" >> /etc/crontab