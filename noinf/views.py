from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    beian_police = ""
    beian_miit = ""
    beian = MySiteInfo.objects.all()
    if beian:
        # 由于返回的是列表，这里不增加列表索引会出错
        beian_police = beian[0].beian_police
        beian_miit = beian[0].beian_miit

    return render(request, 'index.html', locals())
