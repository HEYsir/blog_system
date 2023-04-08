import base64
import hashlib
import hmac
import json
import os
import re
import subprocess
import time
import urllib
import zipfile

import frontmatter
import git
import markdown
import requests
from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from noinf.models import Ad, Article, NavCategory, Category, MySiteInfo, Topic, Tag, User

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


exclude = [
    "username",
    "email",
    "is_staff",
    "last_login",
    "password",
    "last_name",
    "date_joined",
    "is_active",
    "is_superuser",
]


# 全局的settings文件的配置
def global_setting(request):
    top_nav = NavCategory.objects.exclude(name="未分类")
    userInfo = User.objects.all()[0]  # 在没有创建用户的情况下会导致访问失败

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
        page = int(request.GET.get("page", 1))
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
        beian_police_no = re.sub(r"\D", "", beian_police)
        beian_miit = beian[0].beian_miit

    last_article_list = Article.objects.filter(status="p").order_by("-date_publish")
    topNavRq = request.GET.get("topNav")
    try:
        topNavIdx = int(topNavRq)
        last_article_list = last_article_list.filter(category__pid__id=topNavIdx)
    except Exception:
        print("?topNav=", topNavRq)

    popular_article_list = Article.objects.filter(status="p").order_by("-click_count")
    topic_list = Topic.objects.all()

    article_list = getPage(request, last_article_list, 10)

    # 广告数据
    ad_list = Ad.objects.all().order_by("-index")[:4]

    return render(request, "index.html", locals())


def detail(request, id):  # 查看文章详情
    try:
        # 获取文章信息
        article = Article.objects.get(pk=id)
        # 浏览量 +1
        article.click_count += 1
        article.save(update_fields=["click_count"])
    except Article.DoesNotExist:
        return render(request, "", {"reason": "没有找到对应的文章"})

    return render(request, "article-pop.html", locals())


def topic_article(request, topic_id):
    try:
        # 获取文章信息
        topic = Topic.objects.get(id=topic_id)
        topic_article = topic.article_set.all()
        article_list = getPage(request, topic_article, 10)
    except Exception:
        return render(request, "404.html", {"reason": "没有找到对应的文章"})

    return render(request, "index.html", locals())


def git_update(path):
    g = git.Git(path)
    g.pull()


def md2html(fileContent):
    exts = [
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.tables",
        "markdown.extensions.toc",
    ]
    md = markdown.Markdown(extensions=exts)
    html = md.convert(fileContent)
    return html


@require_POST  # 限制只能是POST方法请求
def hookPublish(request):
    if "application/json" != request.META.get("CONTENT_TYPE"):
        return HttpResponse(status=404)
    if "git-oschina-hook" != request.META.get("HTTP_USER_AGENT"):
        return HttpResponse(status=404)

    timestamp = request.META.get("HTTP_X_GITEE_TIMESTAMP")
    reqToken = request.META.get("HTTP_X_GITEE_TOKEN")
    reqEvent = request.META.get("HTTP_X_GITEE_EVENT")
    if not (timestamp and reqToken and reqEvent):
        return HttpResponse(status=404)
    if "Push Hook" != reqEvent:
        return HttpResponse(status=404)
    timestamp = int(timestamp)
    if not settings.DEBUG:
        if abs(timestamp / 1000 - time.time()) / 3600 > 1:
            return HttpResponse(status=404)

    secret = settings.PUBLISH_SEC
    secret_enc = bytes(secret, "utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    # string_to_sign_enc = bytes(string_to_sign, 'utf-8')
    string_to_sign_enc = string_to_sign.encode("utf-8")
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
    json_result = json.loads(postBody)

    path = settings.CONTENT_PATH
    git_update(path)
    files = set()
    commits = json_result["commits"]
    publishUser = User.objects.get(username="HEYsir")
    for commit in commits:
        newFiles = commit.get("added") or []
        mdfFiles = commit.get("modified") or []
        files.update(newFiles, mdfFiles)
    for file in list(files):
        # 获取文件并更新到数据库
        (filename, format) = file.split(".")
        with open(path + file, mode="r", encoding="utf-8") as fd:
            metadata = {}
            content = fd.read()
            if format in ["md", "MD", "Md", "mD"]:
                metadata, mdContent = frontmatter.parse(content)
                content = md2html(mdContent)
                # content = mdContent
            print(metadata)
            title = metadata.get("title") or filename
            summery = metadata.get("summery") if metadata.get("summery") else ""
            formdata = {
                "title": title,
                "desc": summery,
                "content": content,
                "user": publishUser,
            }
            # 配置文章分类
            category = metadata.get("category")
            if category:
                nav = metadata.get("nav")
                navObj = NavCategory.objects.filter(name=nav).first() if nav else None
                if navObj is None:
                    categoryObj, isCreated = Category.objects.get_or_create(name=category)
                else:
                    categoryObj, isCreated = Category.objects.get_or_create(name=category, pid=navObj)
                formdata["category"] = categoryObj
            # 配置文章主题
            topic = metadata.get("topic")
            topicDesc = metadata.get("toptopicDescic")
            if topic:
                topicObj, _ = Topic.objects.get_or_create(title=topic, desc=topicDesc)
                formdata["topic"] = topicObj
            articleObj, _ = Article.objects.update_or_create(defaults=formdata, title=title)
            # 配置文章标签
            tags = metadata.get("tag")
            for tag in tags:
                tagObj, _ = Tag.objects.get_or_create(name=tag)
                articleObj.tag.add(tagObj)
            articleObj.save()

    return HttpResponse(status=200)


def __unzip(zipPath, dstPath):
    file = zipfile.ZipFile(zipPath)
    print("开始解压...")
    file.extractall(dstPath)
    file.close()


@require_POST  # 限制只能是POST方法请求
def deployDeal(request, srvtype):
    subSys = settings.DEPLOY_SYS.get(srvtype)
    if not subSys:
        return HttpResponse(f"部署服务{srvtype}暂不支持", status=404)

    if "application/json" != request.META.get("CONTENT_TYPE"):
        return HttpResponse("请求格式不支持", status=404)
    if "GitHub-Hookshot" not in request.META.get("HTTP_USER_AGENT"):
        return HttpResponse("无效AGENT", status=404)
    if "405847292" != request.META.get("HTTP_X_GITHUB_HOOK_ID"):
        return HttpResponse("无效HOOK_ID", status=404)
    if "118770247" != request.META.get("HTTP_X_GITHUB_HOOK_INSTALLATION_TARGET_ID"):
        return HttpResponse("无效Target-ID", status=404)
    if "repository" != request.META.get("HTTP_X_GITHUB_HOOK_INSTALLATION_TARGET_TYPE"):
        return HttpResponse("无效arget-Type", status=404)
    reqSign = request.META.get("HTTP_X_HUB_SIGNATURE_256")
    reqEvent = request.META.get("HTTP_X_GITHUB_EVENT")
    if not (reqSign and reqEvent):
        return HttpResponse("无有效webhook头信息", status=404)
    if reqEvent not in ["ping", "push", "release"]:
        return HttpResponse("webhook的事件类型不支持", status=404)

    postBody = request.body
    secret_enc = settings.PUBLISH_SEC.encode("utf-8")
    hmac_code = hmac.new(secret_enc, postBody, digestmod=hashlib.sha256).hexdigest()
    sign = "sha256=" + hmac_code
    if settings.DEBUG:
        print(sign)
        print(reqSign)
    else:
        if hmac.compare_digest(sign, reqSign):
            return HttpResponse("验签失败", status=404)

    # 获取报文
    json_result = json.loads(postBody)
    # 判断仓库
    repoName = json_result["repository"]["name"]
    if "blog_system" != repoName:
        return HttpResponse("仓库名称不匹配:{repoName}", status=404)
    # 判断是否release，当前通过事件类型判断
    if "release" == reqEvent:
        if "published" != json_result["action"]:
            return HttpResponse("非release的published行为不响应")
        html_url = json_result["release"]["html_url"]
        version = html_url.split("/")[-1]
        downloadUrl = f"https://codeload.github.com/HEYsir/blog_system/zip/refs/tags/{version}"
    else:
        downloadUrl = "https://codeload.github.com/HEYsir/blog_system/zip/refs/heads/master"

    # 下载
    main_path = subSys["contentPath"]  # 文件保存路径，如果不存在就会被重建
    if not os.path.exists(main_path):  # 如果路径不存在
        os.makedirs(main_path, exist_ok=True)
    downloadPath = os.path.join(main_path, "master.zip")
    rsp = requests.get(downloadUrl, stream=True)

    with open(downloadPath, "wb") as zipFile:
        for chunk in rsp.iter_content(chunk_size=512):
            zipFile.write(chunk)
    __unzip(downloadPath, main_path)

    # 部署并触发服务重启
    verNum = re.split("v|V", version)[1]
    original = os.path.join(main_path, f"blog_system-{verNum}")
    target = settings.BASE_DIR
    subprocess.run(["/bin/bash", "deploy.sh", f"{original}", f"{target}"])

    return HttpResponse(status=200)
