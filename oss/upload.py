import os
import oss2 as aliyunoss

from django.conf import settings

OSS = settings.OSS_CFG


class OssOperate:
    def __init__(self):
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。
        # 强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = aliyunoss.Auth(OSS["keyId"], OSS["keySecret"])
        # yourEndpoint填写Bucket所在地域对应的Endpoint。
        # 以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        self.bucket = aliyunoss.Bucket(auth, OSS["endpoint"], OSS["bucket"])

    def upload_local_file(self, filepath, filename):
        # 必须以二进制的方式打开文件。
        # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
        with open(filepath, "rb") as fileobj:
            # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
            fileobj.seek(0, os.SEEK_SET)
            # Tell方法用于返回当前位置。
            # current = fileobj.tell()
            result = self.upload(fileobj, filename)
        return result

    def upload(self, data, filename):
        # 如果需要在上传文件时设置文件存储类型（x-oss-storage-class）和访问权限（x-oss-object-acl），请在put_object中设置相关Header。
        # headers = dict()
        # headers["x-oss-storage-class"] = "Standard"
        # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE

        # 填写Object完整路径和字符串。Object完整路径中不能包含Bucket名称。
        # result = bucket.put_object('exampleobject.txt', 'Hello OSS', headers=headers)
        result = self.bucket.put_object(filename, data)
        return result
