from django.shortcuts import render
from noinf.models import *
from django.apps import apps
from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
import re
from django.views.decorators.http import require_POST
from django.conf import settings

import time
import hmac
import hashlib
import base64
import urllib
import json

import git
import frontmatter
import markdown

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

    last_article_list = Article.objects.filter(status='p').order_by("-date_publish")
    topNavRq = request.GET.get('topNav')
    try:
        topNavIdx = int(topNavRq)
        last_article_list = last_article_list.filter(category__pid__id=topNavIdx)
    except:
        print("?topNav=", topNavRq)

    popular_article_list = Article.objects.filter(status='p').order_by("-click_count")
    topic_list = Topic.objects.all()


    article_list = getPage(request, last_article_list, 10)


    # 广告数据
    ad_list = Ad.objects.all().order_by('-index')[:4]

    return render(request, 'index.html', locals())


def detail(request, id):  # 查看文章详情
    try:
        # 获取文章信息
        article = Article.objects.get(pk=id)
        # 浏览量 +1
        article.click_count += 1
        article.save(update_fields=['click_count'])
    except Article.DoesNotExist:
        return render(request, '', {'reason': '没有找到对应的文章'})

    return render(request, 'article-pop.html', locals())


def topic_article(request, topic_id):
    try:
        # 获取文章信息
        topic = Topic.objects.get(id = topic_id)
        topic_article = topic.article_set.all()
        article_list = getPage(request, topic_article, 10)
    except:
        return render(request, '404.html', {'reason': '没有找到对应的文章'})

    return render(request, 'index.html', locals())


def git_update(path):
    g = git.Git(path)
    g.pull()


def md2html(fileContent):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']	
    md =  markdown.Markdown(extensions = exts)
    html = md.convert(fileContent)
    return html


@require_POST # 限制只能是POST方法请求
def hookPublish(request):
    if 'application/json' != request.META.get('CONTENT_TYPE'):
        return HttpResponse(status=404)
    if 'git-oschina-hook' != request.META.get('HTTP_USER_AGENT'):
        return HttpResponse(status=404)

    timestamp = request.META.get('HTTP_X_GITEE_TIMESTAMP')
    reqToken = request.META.get('HTTP_X_GITEE_TOKEN')
    reqEvent = request.META.get('HTTP_X_GITEE_EVENT')
    if not (timestamp and reqToken and reqEvent):
        return HttpResponse(status=404)
    if 'Push Hook' != reqEvent:
        return HttpResponse(status=404)
    timestamp = int(timestamp)
    if not settings.DEBUG:
        if abs(timestamp/1000 - time.time())/3600 > 1:
            return HttpResponse(status=404)
    
    secret = settings.PUBLISH_SEC
    secret_enc = bytes(secret, 'utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    # string_to_sign_enc = bytes(string_to_sign, 'utf-8')
    string_to_sign_enc = string_to_sign.encode('utf-8')
    print(type(string_to_sign_enc))
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    if settings.DEBUG:
        print(timestamp)
        print(sign)
        print(reqToken)
    else:
        if sign != reqToken:
            return HttpResponse(status=404)

    # 获取报文
    postBody = request.body
    print(postBody)
    json_result = json.loads(postBody)
    print(json_result)

    path = settings.CONTENT_PATH
    git_update(path)
    files = []
    commits = json_result['commits']
    publishUser = User.objects.get(username='HEYsir')
    for commit in commits:
        tFiles = commit['added']
        for file in tFiles:
            # 获取文件并更新到数据库
            (filename, format) = file.split('.') 
            with open(path+file, mode='r', encoding="utf-8") as fd:
                metadata = {}
                content = fd.read()
                if format in ['md', 'MD', 'Md', 'mD']:
                    metadata, mdContent = frontmatter.parse(content)
                    content = md2html(mdContent)
                    # content = mdContent
                print(metadata)
                title = metadata.get('title')
                summery = metadata.get('summery') if metadata.get('summery') else ''
                formdata = {
                    'title':title if title else filename, 
                    'desc':summery, 
                    'content':content, 
                    'user':publishUser,
                }
                # 配置文章分类
                category = metadata.get('category')  
                if category:
                    nav = metadata.get('nav')
                    navObj = NavCategory.objects.filter(name=nav).first() if nav else None
                    if navObj is None:
                        categoryObj, isCreated = Category.objects.get_or_create(name=category)
                    else:
                        categoryObj, isCreated = Category.objects.get_or_create(name=category, pid=navObj)
                    formdata['category'] = categoryObj
                # 配置文章主题
                topic = metadata.get('topic')
                topicDesc = metadata.get('toptopicDescic')
                if topic:
                    topicObj, isCreated = Topic.objects.get_or_create(title=topic, desc=topicDesc)
                    formdata['topic'] = topicObj
                newArticleObj = Article.objects.create(**formdata)
                # 配置文章标签
                tags = metadata.get('tag')
                for tag in tags:
                    tagObj, isCreated = Tag.objects.get_or_create(name=tag)
                    newArticleObj.tag.add(tagObj)
        # tFiles = commit['remove']
        # for file in tFiles:
        #     # 获取文件并更新到数据库
        #     with open(path+file, mode='r') as fd:
        #         text = fd.read()
        #         (title, format) = file.split('.') 
        #         Article.objects.filter(title=title, desc='', content=text, user=publishUser).update
        tFiles = commit['modified']
        for file in tFiles:
            # 获取文件并更新到数据库
            with open(path+file, mode='r') as fd:
                text = fd.read()
                (title, format) = file.split('.') 
                Article.objects.filter(title=title).update(content=text)
    return HttpResponse(status=200)
