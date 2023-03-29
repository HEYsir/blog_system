#! /bin/bash

set -e
echo $1
echo $2
newSrcPath=$1
orgSrcPath=$2
cp -rf ${newSrcPath}/* ${orgSrcPath}

source ${orgSrcPath}/pyenv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# uwsgi --reload uwsgi.ini  # 在虚拟环境内，shell无法找到uwsgi命令
echo c > ${orgSrcPath}/uwsgi.fifo   # 依赖uwsgi.ini里的配置，当前会在项目根目录下生成