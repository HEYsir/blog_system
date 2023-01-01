# blog_system
使用python语言及django框架从零实现一个博客系统,用于替换现有的wordpress.

# 部署说明
针对Pillow库的安装，
在centos下，需要事先系统级依赖：
sudo yum install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
sudo yum install python3-devel
sudo yum install zlib-devel
sudo yum install libjpeg-turbo-devel
ubuntu是否需要解决依赖，不记得了。

## 安装mysqlclient
apt install python3-dev libmysqlclient-dev
pip install wheel
pip install mysqlclient