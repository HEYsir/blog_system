from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

# 用户(User)模型
# 采用的继承方式扩展用户信息
class User(AbstractUser):
    # 在继承的基础上新增字段
    nicename = models.CharField(
        "昵称", max_length=32, unique=True,
        help_text='Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.')
    avatar = models.ImageField("头像", upload_to='avatar/%Y/%m', default='avatar/default.png',
                               max_length=200, blank=True, null=True)
    mobile = models.CharField("手机号码", max_length=11, blank=True, null=True, unique=True)
    qq = models.CharField("QQ", max_length=20, blank=True, null=True)
    url = models.URLField("个人网页地址", max_length=100, blank=True, null=True)
    github = models.URLField("github", max_length=100, blank=True, null=True)
    weibo = models.URLField("新浪微博", max_length=100, blank=True, null=True)
    wechat = models.URLField("微信", max_length=100, blank=True, null=True)

    # 使用内部的class Meta 定义模型的元数据
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        # ordering：如排序选项，这里以id降序来排序
        ordering = ['-id']

    # 对象的字符串表达式(unicode格式)
    def __unicode__(self):
        return self.username



