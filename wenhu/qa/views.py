from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DetailView
from wenhu.qa.models import Question,Vote,Answer
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from wenhu.helpers import AuthorRequireMixin
from wenhu.helpers import ajax_required
from .forms import QuestionForm



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



class CreateQuestionView(LoginRequiredMixin,CreateView):

    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    message = "问题已提交"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView,self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,self.message)
        return reverse_lazy("qa:all_q")


class QuestionDetailView(LoginRequiredMixin,DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'


class CreateAnswerView(LoginRequiredMixin,CreateView):

    model = Answer
    fields = ('content',)
    message = "您的问题已提交"
    template_name = 'qa/answer_form.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        form .instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView,self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,self.message)
        return reverse_lazy('qa:question_detail',kwargs={"pk":self.kwargs['question_id']})
