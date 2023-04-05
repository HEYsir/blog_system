#!/bin/bash

set -x -e
LOGNAME="blog_system"
PRJDIR=$(cd "$(dirname "$0")";pwd)
LOGDIR="/var/log/uwsgi"

orgLog=$LOGDIR/$LOGNAME.log

DATE=`date -d "yesterday" +"%Y-%m-%d"`
dstLog=$LOGDIR/$LOGNAME-${DATE}.log
mv $orgLog $dstLog

echo l > $PRJDIR/uwsgi.fifo
# touchfile="/home/logs/.touchforlogrotat"
# touch $touchfile
