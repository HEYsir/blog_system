from django.contrib import admin

# Register your models here.
from noinf.models import *

admin.site.register(User)
admin.site.register(NavCategory)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
