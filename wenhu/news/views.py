from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy

from wenhu.news.models import News
from wenhu.helpers import ajax_required,AuthorRequireMixin


# Create your views here.

class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""

    model = News
    paginate_by = 20  # url中的?page
    # context_object_name = 'news_list'  # 默认值是 模型类名_list 或者 object_list
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


class NewsDeleteView(LoginRequiredMixin,AuthorRequireMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    #slug_url_kwarg = 'slug'  # 通过url传入要删除的对象主键id，默认值是slug
    #pk_url_kwarg = 'pk'  # 通过url传入要删除的对象主键id，默认值是pk
    success_url = reverse_lazy("news:list") # 在项目 URLConf 未加载前使用



@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """发送动态，ajax post请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空")
