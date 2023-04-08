"""
Django settings for blog_system project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# read secrue config file
with open(os.path.join(BASE_DIR, "configure/config"), "rt") as f:
    config = json.load(f)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config["DEBUG"]

ALLOWED_HOSTS = config["ALLOWED_HOSTS"]


# Application definition

INSTALLED_APPS = [
    "noinf",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blog_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "theme/templates"),
        ],  # 模板文件的路径设置
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "noinf.views.global_setting",  # 将全局变量加入到上下文处理器中
            ],
        },
    },
]

WSGI_APPLICATION = "blog_system.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
db_config = config["db_config"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_config["NAME"],
        "USER": db_config["USER"],
        "PASSWORD": db_config["PASSWORD"],
        "HOST": db_config["HOST"],
        "PORT": db_config["PORT"],
        "TEST": {
            "NAME": db_config["NAME"],
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"  # admin后台页面默认英文

TIME_ZONE = "Asia/Shanghai"  # 设置为中国的时区

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 设置为False，要不然数据库时间和当前时间不一致


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
# 静态文件路径设置，当然这里和官方推荐有点区别，这里这个工程只有一个应用所以没有区别是否公用
# 这里任然保留，不屏蔽上面的APP路径下的static
STATICFILES_DIRS = (os.path.join(BASE_DIR, "theme/static"),)
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, "collect_static").replace("\\", "/")

# 自定义用户Model
AUTH_USER_MODEL = "noinf.User"

# upload files (file, Images)
MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# webhooks相关配置
WebHooks = config["WebHooks"]
WH_RootUrl = WebHooks["rootUrl"]
WH_Secret = WebHooks["secret"]
# 博客文章发布
PUBLISH_SEC = WH_Secret
PUBLISH_URL = os.path.join(WH_RootUrl, WebHooks["publish"]["url"])
CONTENT_PATH = WebHooks["publish"]["contentPath"]
# 服务部署
WH_Deploys = WebHooks["deploy"]
DEPLOY_URL = os.path.join(WH_RootUrl, WH_Deploys["url"], "<str:srvtype>/")
DEPLOY_SYS = {}
for subSys in WH_Deploys["subSys"]:
    DEPLOY_SYS[subSys["type"]] = subSys

# 日志配置
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "default": {
            "format": "%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s %(levelname)s- %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "default"},
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "when": "D",
            "interval": 1,
            "formatter": "default",
        },
        "request": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/request.log"),
            "formatter": "default",
        },
        "root": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/root.log"),
            "formatter": "default",
        },
        "db_backends": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/db_backends.log"),
            "formatter": "default",
        },
    },
    "loggers": {
        # 应用中自定义日志记录器
        "mylogger": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": True,
        },
        # "django": {
        #     "level": "DEBUG",
        #     "handlers": ["console", "file"],
        #     "propagate": False,
        # },
        # "django.request": {
        #     "level": "DEBUG",
        #     "handlers": ["request"],
        #     "propagate": False,
        # },
        # "django.db.backends": {
        #     "level": "DEBUG",
        #     "handlers": ["db_backends"],
        #     "propagate": False,
        # },
    },
    # "root": {
    #     "level": "DEBUG",
    #     "handlers": ["root"],
    # },
}
