# Generated by Django 3.1.7 on 2022-05-17 23:22

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import noinf.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                (
                    "nicename",
                    models.CharField(
                        help_text="Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=32,
                        unique=True,
                        verbose_name="昵称",
                    ),
                ),
                ("motto", models.CharField(blank=True, max_length=128, null=True, verbose_name="签名")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        default="avatar/default.png",
                        max_length=200,
                        null=True,
                        upload_to=noinf.models.user_avatar_path,
                        verbose_name="头像",
                    ),
                ),
                ("mobile", models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name="手机号码")),
                ("qq", models.CharField(blank=True, max_length=20, null=True, verbose_name="QQ")),
                ("url", models.URLField(blank=True, max_length=100, null=True, verbose_name="个人网页地址")),
                ("github", models.URLField(blank=True, max_length=100, null=True, verbose_name="github")),
                ("weibo", models.URLField(blank=True, max_length=100, null=True, verbose_name="新浪微博")),
                ("wechat", models.URLField(blank=True, max_length=100, null=True, verbose_name="微信")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["-id"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Ad",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="广告标题")),
                ("description", models.CharField(max_length=200, verbose_name="广告描述")),
                ("image_url", models.ImageField(upload_to=noinf.models.ad_image_path, verbose_name="图片路径")),
                ("callback_url", models.URLField(blank=True, null=True, verbose_name="回调url")),
                ("date_publish", models.DateTimeField(auto_now_add=True, verbose_name="发布时间")),
                ("index", models.IntegerField(default=999, verbose_name="排列顺序(从小到大)")),
            ],
            options={
                "verbose_name": "Ad",
                "verbose_name_plural": "Ad",
                "ordering": ["index", "id"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(db_index=True, max_length=50, unique=True, verbose_name="文章标题")),
                ("desc", models.CharField(max_length=50, verbose_name="文章描述")),
                ("content", models.TextField(verbose_name="文章内容")),
                ("click_count", models.IntegerField(default=0, verbose_name="点击次数")),
                ("likes_count", models.IntegerField(default=0, verbose_name="点赞次数")),
                ("is_recommend", models.BooleanField(default=False, verbose_name="是否推荐")),
                ("date_publish", models.DateTimeField(auto_now_add=True, verbose_name="发布时间")),
                ("date_modify", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                (
                    "status",
                    models.CharField(choices=[("d", "草稿"), ("p", "发布"), ("w", "撤回")], default="d", max_length=1),
                ),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Article",
                "ordering": ["-date_publish"],
            },
        ),
        migrations.CreateModel(
            name="Links",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="标题")),
                ("description", models.CharField(max_length=200, verbose_name="友情链接描述")),
                ("callback_url", models.URLField(verbose_name="url地址")),
                ("date_publish", models.DateTimeField(auto_now_add=True, verbose_name="发布时间")),
                ("index", models.IntegerField(default=999, verbose_name="排列顺序(从小到大)")),
            ],
            options={
                "verbose_name": "Links",
                "verbose_name_plural": "Links",
                "ordering": ["index", "id"],
            },
        ),
        migrations.CreateModel(
            name="MySiteInfo",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("beian_police", models.CharField(blank=True, max_length=50, null=True, verbose_name="公安备案号")),
                ("beian_miit", models.CharField(blank=True, max_length=50, null=True, verbose_name="ICP备案号")),
            ],
            options={
                "verbose_name": "网站信息",
                "verbose_name_plural": "网站信息",
            },
        ),
        migrations.CreateModel(
            name="NavCategory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, verbose_name="导航名称")),
            ],
            options={
                "verbose_name": "nav_name",
                "verbose_name_plural": "nav_name",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, verbose_name="标签名称")),
            ],
            options={
                "verbose_name": "tag",
                "verbose_name_plural": "tag",
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="专题名称")),
                ("desc", models.CharField(blank=True, max_length=50, null=True, verbose_name="专题描述")),
            ],
            options={
                "verbose_name": "专题文章",
                "verbose_name_plural": "专题文章",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(verbose_name="评论内容")),
                ("username", models.CharField(blank=True, max_length=30, null=True, verbose_name="用户名")),
                ("email", models.EmailField(blank=True, max_length=50, null=True, verbose_name="邮箱地址")),
                ("url", models.URLField(blank=True, max_length=100, null=True, verbose_name="个人网页地址")),
                ("date_publish", models.DateTimeField(auto_now_add=True, verbose_name="发布时间")),
                (
                    "article",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="noinf.article",
                        verbose_name="文章",
                    ),
                ),
                (
                    "pid",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="noinf.comment",
                        verbose_name="父级评论",
                    ),
                ),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comment",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, verbose_name="分类名称")),
                (
                    "pid",
                    models.ForeignKey(
                        blank=True,
                        default=noinf.models.get_NavCategory_default_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="noinf.navcategory",
                        verbose_name="父级分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Category",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=noinf.models.get_Category_default_id,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="noinf.category",
                verbose_name="分类",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="tag",
            field=models.ManyToManyField(blank=True, to="noinf.Tag", verbose_name="标签"),
        ),
        migrations.AddField(
            model_name="article",
            name="topic",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="noinf.topic", verbose_name="主题"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="用户"
            ),
        ),
    ]
