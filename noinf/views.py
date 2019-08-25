from django.shortcuts import render
from .models import *
from django.apps import apps
from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger, Paginator

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
    top_nav = NavCategory.objects.exclude(name='未分类')
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


# 定义一个分页函数
def getPage(request, article_all, per_page_num):
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(article_all, per_page_num)

    try:
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        # 如果请求的页数不是整数、页面不存在、页数超范围, 返回第一页。
        article_list = paginator.page(1)

    return article_list


# Create your views here.
def index(request):
    beian_police = ""
    beian_miit = ""
    beian_police_no = ""
    beian = MySiteInfo.objects.all()
    if beian:
        # 由于返回的是列表，这里不增加列表索引会出错
        beian_police = beian[0].beian_police
        beian_police_no = re.sub("\D", "", beian_police)
        beian_miit = beian[0].beian_miit

    last_article_list = Article.objects.all().order_by("-date_publish")
    popular_article_list = Article.objects.all().order_by("-click_count")



    article_list = getPage(request, last_article_list, 10)


    # 广告数据
    ad_list = Ad.objects.all().order_by('-index')[:4]

    return render(request, 'index.html', locals())

def detail(request, id):  # 查看文章详情
    pass
