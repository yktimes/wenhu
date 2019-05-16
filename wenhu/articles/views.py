from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView,CreateView,UpdateView,DetailView,DetailView
from wenhu.articles.models import Article


class ArticlesListView(LoginRequiredMixin,ListView):

    model = Article
    paginate_by = 10
    context_object_name = 'articles/article_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Article.objects.get_counted_tags()

    def get_queryset(self):
        return Article.objects.get_published()
