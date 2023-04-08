import json

from django.conf import settings
from django.test import TestCase


# Create your tests here.
class BlogPublishTests(TestCase):
    def setUp(self) -> None:
        settings.DEBUG = True

    def test_content_modify(self):
        head = {
            "Request Method": "POST",
            "X-Git-Oschina-Event": "Push Hook",
            "X-Gitee-Token": "M4hRWkgtUSQymIvWS/uNM9lot8QhaZREWdOp7QcTFro=",
            "X-Gitee-Event": "Push Hook",
            "User-Agent": "git-oschina-hook",
            "X-Gitee-Timestamp": "1679237741363",
            "X-Gitee-Ping": "False",
            "Content-Type": "application/json",
        }

        with open("./tests/data/gitee_push_event.json", "r") as file:
            data = json.loads(file.read())
        rsp = self.client.post(settings.PUBLISH_URL, data=data, content_type="application/json", **head)
        self.assertEqual(200, rsp.status_code)
