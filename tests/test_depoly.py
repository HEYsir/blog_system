import json
import os
from django.test import TestCase
from django.conf import settings


class ServerUpdateTests(TestCase):
    def setUp(self) -> None:
        settings.DEBUG = False
    
#     def test_server_release_illegal_action(self):
#         head = {
#             "User-Agent": "GitHub-Hookshot/12dd831",
#             "X-GitHub-Delivery": "ed768cd0-c8c7-11ed-8872-a6054ecd29cb",
#             "X-GitHub-Event": "release",
#             "X-GitHub-Hook-ID": "405847292",
#             "X-GitHub-Hook-Installation-Target-ID": "118770247",
#             "X-GitHub-Hook-Installation-Target-Type": "repository",
#             "X-Hub-Signature": "sha1=9eacaced69ec7306ad0ed61dc3390423f78748a3",
#             "X-Hub-Signature-256": "sha256=b7f78f2072b414e3039513b9240756f057385c1e7789e1899531a092e5cb0ca0",
#         }

#         with open('./tests/data/github_release_notpublished.json', 'r') as file:
#             data = json.loads(file.read())
#         req_url = settings.DEPLOY_URL.replace('<str:srvtype>/', 'server/')
#         rsp = self.client.post(req_url, data=data, content_type='application/json', **head)
#         print(rsp.content.decode('utf-8'))
#         self.assertEqual(200, rsp.status_code)


    def test_server_release_ok(self):
        head = {
            "HTTP_USER_AGENT": "GitHub-Hookshot/12dd831",
            "X-GitHub-Delivery": "ed7d1c80-c8c7-11ed-8984-7b8a39e5852f",
            "HTTP_X_GITHUB_EVENT": "release",
            "HTTP_X_GITHUB_HOOK_ID": "405847292",
            "HTTP_X_GITHUB_HOOK_INSTALLATION_TARGET_ID": "118770247",
            "HTTP_X_GITHUB_HOOK_INSTALLATION_TARGET_TYPE": "repository",
            "X-Hub-Signature": "sha1=a9c32dd9e04f850c0d3ca3e5399484f1d11cee37",
            "HTTP_X_HUB_SIGNATURE_256": "sha256=40ef019805b7adcd8e98566d78e658805b33ef5d0ef3449e418a8926c8253e53",
        }

        with open('./tests/data/github_release_published.json', 'r') as file:
            a = file.read()
            print(type(a),len(a))
            data = json.loads(a)
        req_url = settings.DEPLOY_URL.replace('<str:srvtype>/', 'server/')
        print(req_url)
        rsp = self.client.post(req_url, data=data, content_type='application/json', **head)
        print(rsp.content.decode('utf-8'))
        self.assertEqual(200, rsp.status_code)