"""blog_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
# noinf的【urls.py】设置,使输入IP就能访问首页
from noinf import views
from django.conf import settings
from django.views.static import serve

from noinf.upload import upload_image
##支持生产部署时的静态文件解析
from django.views import static

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^noinf/', include('noinf.urls')),
]
"""
urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('topic/<int:topic_id>/', views.topic_article, name='topic_article'),
    path('articles/<int:id>/', views.detail, name='detail'),
    url(r'^uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r"^uploads/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, }),
    ##支持生产部署时的静态文件解析
    url(r'^static/(?P<path>.*)$', static.serve,
          {'document_root': settings.STATIC_ROOT}, name='static'),
    path(settings.PUBLISH_URL.lstrip('/'), views.hookPublish),
    path(settings.DEPLOY_URL.lstrip('/'), views.deployDeal),
]
