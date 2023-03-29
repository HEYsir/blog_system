#! /bin/sh

set -e
echo $1
echo $2
newSrcPath=$1
orgSrcPath=$2
cp -rf ${newSrcPath}/* ${orgSrcPath}
uwsgi --reload uwsgi.ini