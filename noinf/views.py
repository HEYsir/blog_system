from django.shortcuts import render
from .models import *
from django.apps import apps

import re

# def getmodelfield(appname, modelname, exclude):
#     """
#     获取model的verbose_name和name的字段
#     """
#     filed = User._meta.fields
#     print(filed)
#     fielddic = {}
#
#     params = [f for f in filed if f.name not in exclude]
#
#     for i in params:
#         fielddic[i.name] = i.verbose_name
#
#     print(fielddic)
#     return fielddic


exclude = ['username','email','is_staff','last_login','password','last_name','date_joined','is_active','is_superuser']

# 全局的settings文件的配置
def global_setting(request):
    top_nav = NavCategory.objects.all()
    userInfo = User.objects.all()[0] #在没有创建用户的情况下会导致访问失败
    # user_fileds = User._meta.get_fields()
    user_fileds = User._meta._get_fields(reverse=False, include_parents=False)
    # print(user_fileds)

    # 由于User继承子抽象类AbstractUser,AbstractUser中的所有成员都直接成为被继承的本地成员，而不是父模型成员
    # 所以只能这种方式过滤，https://docs.djangoproject.com/en/2.1/ref/models/meta/#retrieving-all-field-instances-of-a-model
    # include_parents
    params = [f for f in user_fileds if f.name not in exclude]
    fielddic = {}
    for i in params:
        fielddic[i.name] = i.verbose_name

    # print(fielddic)

    return locals()


# Create your views here.
def index(request):
    beian_police = ""
    beian_miit = ""
    beian = MySiteInfo.objects.all()
    if beian:
        # 由于返回的是列表，这里不增加列表索引会出错
        beian_police = beian[0].beian_police
        beian_police_no = re.sub("\D", "", beian_police)
        beian_miit = beian[0].beian_miit

    return render(request, 'index.html', locals())
