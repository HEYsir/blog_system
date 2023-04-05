#!/bin/bash

set -x -e

PRJDIR=$(cd "$(dirname "$0")";pwd)
LOGDIR="/var/log"

LOGNAME="blog_system"
DATE=`date -d "yesterday" +"%Y-%m-%d"`

# uwsgi日志处理
uwsgiLogDir=$LOGDIR/uwsgi
orgLog=$uwsgiLogDir/$LOGNAME.log
dstLog=$uwsgiLogDir/$LOGNAME-${DATE}.log
mv $orgLog $dstLog
echo l > $PRJDIR/uwsgi.fifo
# touchfile="/home/logs/.touchforlogrotat"
# touch $touchfile
# 删除30天前的*.log文件
find $uwsgiLogDir -mtime +30 -type f -name \*.log -exec rm -f {} \; 

# nginx日志处理
LOGNAME="blog_system"
ngxLogDir=$LOGDIR/nginx
# access log
orgLog=$ngxLogDir/$LOGNAME.access.log
dstLog=$ngxLogDir/$LOGNAME.access-${DATE}.log
mv $orgLog $dstLog
# error log
orgLog=$ngxLogDir/$LOGNAME.error.log
dstLog=$ngxLogDir/$LOGNAME.error-${DATE}.log
mv $orgLog $dstLog

kill -USR1 `cat ${ngxLogDir}/nginx.pid`
find $ngxLogDir -mtime +30 -type f -name \*.log -exec rm -f {}