import datetime as dt
import json
import os
import uuid

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from oss.upload import OssOperate


@login_required
@csrf_exempt
@require_POST  # 限制只能是POST方法请求
def upload_image(request: HttpRequest, dir_name):
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 1, "message": "上传出错"}
    imagefile = request.FILES.get("imgFile", None)
    if imagefile:
        result = image_upload(imagefile, dir_name)

    return HttpResponse(json.dumps(result), content_type="application/json")


def generation_upload_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + "/%d/%d/" % (today.year, today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name


def image_upload(files, dir_name):
    bsuccess = False
    print(dir_name)
    # 允许上传文件类型
    allow_suffix = [
        "jpg",
        "png",
        "jpeg",
        "gif",
        "bmp",
    ]
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}

    relative_path_file = generation_upload_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)

    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    with open(path_file, "wb") as fd:
        fd.write(files.file.read())
        bsuccess = True

    if bsuccess:
        file_url = settings.MEDIA_URL + relative_path_file + file_name
        return {"error": 0, "url": file_url}

    return {"error": 1, "message": "图片存储失败"}


@csrf_exempt
@require_POST  # 限制只能是POST方法请求
def oss_upload(request: HttpRequest):
    file = request.FILES.get("file")
    if file is None:
        return JsonResponse({"code": 400, "msg": "no files for upload"})
    filename = file.name

    oss = OssOperate()
    oss.upload(file, filename)
