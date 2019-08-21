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

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^noinf/', include('noinf.urls')),
]
"""

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('articles/<int:id>/', views.detail, name='detail'),
    url(r'^uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r"^uploads/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, }),
]
