# blog_system
使用python语言及django框架从零实现一个博客系统,用于替换现有的wordpress.

## 系统环境
1. 安装git
apt install git
## 部署说明
1. 安装虚拟环境

    ```bash
    apt install python3-venv
    # 进入项目路径
    python3 -m venv pyenv
    source pyenv/bin/activat 
    ```
2. 安装依赖库

   ```shell
   apt install python3-dev libmysqlclient-dev
   pip install wheel
   pip install -r requirement.txt
   ```

   针对Pillow库的安装，在**centos**下，需要事先系统级依赖：

   ```
   yum install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
   yum install python3-devel
   yum install zlib-devel
   yum install libjpeg-turbo-devel
   ```

3. 配置文件

   复制配置模板文件，并填充必要的配置

   ```bash
   cp configure/config_template configure/config
   ```

   执行如下脚本生成密码串，并写入到配置文件的`SECRET_KEY`字段

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. 数据库迁移
python manage.py makemigrations
python manage.py migrae
5. 起服务
确定基础运行无异常
python manage.py runserver
起uwsgi
uwsgi --ini uwsgi.ini

6. nginx代理配置
   ```conf
   location / {
      include uwsgi_params;
      #uwsgi_pass  unix:///run/uwsgi/blogsrv.sock;
      uwsgi_pass 127.0.0.1:8000;
   }
   ```
   IPC方式存在异常

7. 配置日志

   非root用户执行命令`echo "your password" | sudo -S bash init.sh`
   
   root用户执行`bash init.sh`

8. 阿萨德

# FQA

## mysqlclient或uWSGI安装报错

如果在安装uWSGI和mysqlcient时出现如下错误，只要卸载重新安装就行了，问题就是前一步依赖的wheel库还没安装成功

```bash
ERROR: Command errored out with exit status 1:                                                                               
 ......
  error: invalid command 'bdist_wheel'                                                                                       
  \----------------------------------------                                                                                   
  ERROR: Failed building wheel for mysqlclient
```

正确的过程应当是先单独完成wheel库的安装