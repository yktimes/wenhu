from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DetailView
from wenhu.qa.models import Question, Vote, Answer
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from wenhu.helpers import AuthorRequireMixin
from wenhu.helpers import ajax_required
from .forms import QuestionForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
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
        context["active"] = "answered"  # 这是给前端 Tab 栏设置的

        return context


class UnAnsweredQuestionListView(QuestionListView):
    """没有答案的问题"""

    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnAnsweredQuestionListView, self).get_context_data()

        context["active"] = "unanswered"  # 这是给前端 Tab 栏设置的

        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    message = "问题已提交"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:all_q")


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ('content',)
    message = "您的问题已提交"
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('qa:question_detail', kwargs={"pk": self.kwargs['question_id']})


@login_required
@ajax_required
@require_http_methods(['POST'])
def question_vote(request):
    """给问题投票"""
    question_id = request.POST["question"]
    # U 赞 D 踩
    value = True if request.POST['value'] == 'U' else False
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户

    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": question.total_votes()})


# # 1 用户首次操作，点赞/踩
#  if request.user.pk not in users:
#      question.votes.update_or_create(user=request.user,value=value)
#
# # 2 用户已经赞过，要取消踩/赞一下
#  elif question.votes.get
# # 3 用户已经踩过，取消踩/赞一下


@login_required
@ajax_required
@require_http_methods(['POST'])
def answer_vote(request):
    """给答案投票"""
    answer_id = request.POST["answer"]
    # U 赞 D 踩
    value = True if request.POST['value'] == 'U' else False
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)  # 当前问题的所有投票用户

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})

@login_required
@ajax_required
@require_http_methods(['POST'])
def accept_answer(request):
    """接受回答  Ajax Post请求"""


    answer_id = request.POST["answer"]
    answer = Answer.objects.get(pk=answer_id)

    #如果当前登录不是提问者，抛出权限拒绝错误

    if answer.question.user.username!=request.user.username:
        raise PermissionDenied

    answer.accept_answer()
    return JsonResponse({"status":"true"})


