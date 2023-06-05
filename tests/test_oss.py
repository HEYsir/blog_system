import json

from django.conf import settings
from django.test import TestCase


class OssUploadTests(TestCase):
    def setUp(self) -> None:
        settings.DEBUG = False
        self.url = settings.OSS_URL

    def test_upload_ok(self):
        with open("/home/noinf/图片/上传测试.png", "rb") as file:
            rsp = self.client.post(self.url, {"name": "aaa.jpg", "file": file})
            print(rsp.content.decode("utf-8"))
            self.assertEqual(200, rsp.status_code)
            retJson = rsp.json()
            self.assertEqual(200, retJson.get("code"))
