from django.contrib import admin, messages
from django.utils.translation import ngettext

# Register your models here.
from noinf.models import Ad, Article, NavCategory, Category, MySiteInfo, Topic, Tag, Comment, Links, User

admin.site.register(User)
admin.site.register(NavCategory)
admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)


class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "/static/kindeditor/kindeditor-all-min.js",
            "/static/kindeditor/lang/zh-CN.js",
            "/static/kindeditor/config.js",
        )

    # admin 选项控制变更列表所显示的列
    list_display = ("title", "desc", "date_publish", "click_count", "status")
    # admin 选项控制变更列表可以链接的列
    list_display_links = (
        "title",
        "desc",
    )
    # admin 选项控制变更列表可以直接编辑的列
    #   list_editable = ('click_count',)
    fieldsets = (
        (None, {"fields": ("title", "desc", "content", "topic")}),
        (
            "高级设置",
            {
                # 'classes': ('collapse',),
                "fields": ("is_recommend", "category", "tag")
            },
        ),
    )
    # 自定义动作
    actions = ["publish_status", "withdraw_status"]

    # 添加admin动作（发表文章）
    def publish_status(self, request, queryset):
        updated = queryset.update(status="p")
        self.message_user(
            request,
            ngettext(
                "所选文章已发布 ",
                "所选文章已发布",
                updated,
            ),
            messages.SUCCESS,
        )

    # 指定后台界面动作的关键词
    publish_status.short_description = "发布文章"

    # 添加admin动作（撤回文章）
    def withdraw_status(self, request, queryset):
        withdraw = queryset.update(status="w")
        self.message_user(
            request,
            ngettext(
                "所选文章已撤回 ",
                "所选文章已撤回",
                withdraw,
            ),
            messages.SUCCESS,
        )

    withdraw_status.short_description = "撤回文章"

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# 使用自定义的ModelAdmin来注册
admin.site.register(Article, ArticleAdmin)


@admin.register(MySiteInfo)
class MySiteInfoAdmin(admin.ModelAdmin):
    # 控制不允许增加和删除
    def has_add_permission(self, request):
        beian = MySiteInfo.objects.all()
        return not beian.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# 使用自定义的ModelAdmin来注册
admin.site.register(Topic)
