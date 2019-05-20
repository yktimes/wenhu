from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DetailView
from wenhu.qa.models import Question,Vote
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from wenhu.helpers import AuthorRequireMixin
from wenhu.helpers import ajax_required



class QuestionListView(LoginRequiredMixin,ListView):

    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView,self).get_context_data()
        context['popular_tags'] = Question.objects.get_counted_tags()
        context["active"] = "all"

        return context

class AnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题"""
    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuestionListView, self).get_context_data()
        context['popular_tags'] = Question.objects.get_counted_tags()
        context["active"] = "answered" # 这是给前端 Tab 栏设置的

        return context

class UnAnsweredQuestionListView(QuestionListView):
    """没有答案的问题"""
    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnAnsweredQuestionListView, self).get_context_data()

        context["active"] = "unanswered" # 这是给前端 Tab 栏设置的

        return context
