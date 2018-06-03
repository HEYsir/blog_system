from django.db import models

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


# 用户元数据(UserMeta)模型
class UserMeta(models.Model):
    username_validator = UnicodeUsernameValidator()

    nicename = models.CharField(
        "昵称", max_length=32, unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
    )
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
        # verbose_name：数据库表名名称，这里表名称为“用户”
        verbose_name = 'UserEx'
        # verbose_name_plural：人类可读的单复数名称，这里“用户”复数名称为“用户”
        verbose_name_plural = verbose_name
        # ordering：如排序选项，这里以id降序来排序
        ordering = ['-id']

    # 对象的字符串表达式(unicode格式)
    def __unicode__(self):
        return self.nicename


# 用户(User)模型
# 采用的继承方式扩展用户信息
class User(AbstractUser):
    # 在继承的基础上新增2个字段
    last_login = models.DateTimeField(_('date joined'), default=timezone.now)
    usermeta = models.OneToOneField(UserMeta, verbose_name='用户扩展信息')

    # 使用内部的class Meta 定义模型的元数据
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # ordering：如排序选项，这里以id降序来排序
        ordering = ['-id']

    # 对象的字符串表达式(unicode格式)
    def __unicode__(self):
        return self.username


