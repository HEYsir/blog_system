from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


def user_avatar_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'avatar/user_{0}/{1}'.format(instance.nicename, filename)

# 用户(User)模型
# 采用的继承方式扩展用户信息
class User(AbstractUser):
    # 在继承的基础上新增字段
    nicename = models.CharField(
        "昵称", max_length=32, unique=True,
        help_text='Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.')
    avatar = models.ImageField("头像", upload_to=user_avatar_path, default='avatar/default.png',
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


# 分类(Top navigateion)模型
class NavCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='导航名称')
    index = models.IntegerField(default=999, verbose_name='分类的排序')

    class Meta:
        verbose_name = 'nav_name'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name


# 分类(category)模型
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类的排序')
    pid = models.ForeignKey(NavCategory, on_delete=models.CASCADE, blank=True, null=True, verbose_name="父级分类")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name


# 标签(tag)模型
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章(aticle)模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    date_modify = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    #
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='分类')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


# 评论(comment)模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    #
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# 友情链接(links)模型
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = 'Links'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


def ad_image_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/ad_<id>_<title>/<filename>
        return 'ad/ad_{0}_{1}/{2}'.format(instance.id, instance.title, filename)


# 广告(ad)模型
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to=ad_image_path, verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# 网站信息(siteInfo)模型
class MySiteInfo(models.Model):
    title = "网站信息"
    beian_police = models.CharField(max_length=50, null=True, blank=True, verbose_name='公安备案号')
    beian_miit = models.CharField(max_length=50, null=True, blank=True, verbose_name='ICP备案号')

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
