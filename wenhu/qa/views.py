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
# def question_vote(request):
#     """给问题投票"""
#     question_id = request.POST("question")
#     # U 赞 D 踩
#
#     value =  True if request.POST['value']=='U' else False
#     question = Q
#     users = question_id

