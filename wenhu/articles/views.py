from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DetailView
from wenhu.articles.models import Article
from django.urls import reverse_lazy
from .forms import ArticleForm
from django.urls import reverse
from wenhu.helpers import AuthorRequireMixin


#
# class ArticlesListView(LoginRequiredMixin, ListView):
#     """已发布的文章列表"""
#     model = Article
#     paginate_by = 10
#     context_object_name='articles'
#     template_name = 'articles/article_list.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['popular_tags'] = Article.objects.get_counted_tags()
#         return context
#
#     def get_queryset(self):
#         print(Article.objects.all())
#         return Article.objects.all()
#
# class DraftListView(ArticlesListView):
#     """草稿箱文章列表"""
#     def get_queryset(self):
#         return Article.objects.filter(user=self.request.user).get_drafts()
#
#
# class ArticleCreateView(LoginRequiredMixin, CreateView):
#     model = ArticleForm
#     form_class = ArticleForm
#     template_name = 'articles/article_create.html'
#     messages = "您的文章发表成功"
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         """创建成功后调跳转"""
#         messages.success(self.request, self.messages)
#         return reverse_lazy("articles:list")


class ArticlesListView(LoginRequiredMixin, ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 20
    context_object_name = "articles"
    template_name = "articles/article_list.html"  # 可省略

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        # TODO 这个get_published() 有问题 返回空的queryset
        print(Article.objects.filter(status='D'))
        return Article.objects.get_published()


class DraftsListView(ArticlesListView):
    """草稿箱文章列表"""

    def get_queryset(self, **kwargs):
        # 当前用户的草稿
        return Article.objects.filter(user=self.request.user).get_drafts()


class CreateArticleView(LoginRequiredMixin, CreateView):
    """创建文章"""
    model = Article
    message = "您的文章已创建成功！"  # Django框架中的消息机制
    form_class = ArticleForm
    template_name = 'articles/article_create.html'

    def form_valid(self, form):
        print(self.request)
        form.instance.user = self.request.user
        return super(CreateArticleView, self).form_valid(form)

    def get_success_url(self):
        """创建成功后跳转"""

        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse('articles:list')


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """用户浏览文章"""
    model = Article
    template_name = 'articles/article_detail.html'


class ArticleEditView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    model = Article
    message = "文章编辑成功"
    form_class = ArticleForm
    template_name = 'articles/article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('articles:article', kwargs={"slug": self.get_object().slug})
