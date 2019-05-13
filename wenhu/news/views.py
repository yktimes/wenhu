from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from wenhu.news.models import News
# Create your views here.

class NewsListView(LoginRequiredMixin,ListView):
    """首页动态"""

    model = News
    paginate_by = 20 # url中的?page
    #context_object_name = 'news_list'  # 默认值是 模型类名_list 或者 object_list
    template_name = 'news/news_list.html'  # 不写默认为 模型类名_list.html

    # def get_ordering(self):
    #     pass
    #
    # def get_paginate_by(self, queryset):
    #     pass
    #
    def get_queryset(self):
        return News.objects.filter(reply=False)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """添加额外的上下文"""
    #     context = super().get_context_data()
    #     context["view"]=100
    #     return context

