from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


from django.urls import reverse_lazy

from wenhu.news.models import News
from wenhu.helpers import ajax_required, AuthorRequireMixin
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
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
        return News.objects.filter(reply=False).select_related('user','parent').prefetch_related('liked')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """添加额外的上下文"""
    #     context = super().get_context_data()
    #     context["view"]=100
    #     return context


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    # slug_url_kwarg = 'slug'  # 通过url传入要删除的对象主键id，默认值是slug
    # pk_url_kwarg = 'pk'  # 通过url传入要删除的对象主键id，默认值是pk

    # success_url 必须要定义哦，这是删除成功后要跳转的页面
    success_url = reverse_lazy("news:list")  # reverse_lazy 在项目 URLConf 未加载前使用


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


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    """点赞功能"""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)

    # 取消或添加赞
    news.switch_like(request.user)
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(['GET'])
def get_thread(request):
    """返回动态的评论 AJAX GET 请求"""
    news_id = request.GET.get("news")
    news = News.objects.select_related('user').get(pk=news_id)
    mews_html = render_to_string('news/news_single.html', {'news': news})  # 没有评论的时候
    thread_html = render_to_string('news/news_thread.html', {'thread': news.get_thread()})

    return JsonResponse({
        "uuid": news_id,
        "news": mews_html,
        "thread": thread_html
    })

@login_required
@ajax_required
@require_http_methods(['POST'])
def post_comment(request):
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})

    else:
        return HttpResponseBadRequest("内容不能为空")
@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    """更新互动信息"""
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    return JsonResponse({'likes': news.count_likers(), 'comments': news.comment_count()})
