from django.contrib import admin

# Register your models here.
from noinf.models import *

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
            '/static/kindeditor/kindeditor-all-min.js',
            '/static/kindeditor/lang/zh-CN.js',
            '/static/kindeditor/config.js',
        )

    # admin 选项控制变更列表所显示的列
    list_display = ('title', 'desc', 'date_publish', 'click_count',)
    # admin 选项控制变更列表可以链接的列
    list_display_links = ('title', 'desc',)
    # admin 选项控制变更列表可以直接编辑的列
#   list_editable = ('click_count',)
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content')
        }),
        ('高级设置', {
            # 'classes': ('collapse',),
            'fields': ('is_recommend', 'category', 'tag')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# 使用自定义的ModelAdmin来注册
admin.site.register(Article, ArticleAdmin)
