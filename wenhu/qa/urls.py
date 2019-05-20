from django.urls import path
from wenhu.qa import views


app_name = 'qa' # 注意这里哈
urlpatterns = [

    path("", views.UnAnsweredQuestionListView.as_view(), name="unanswered_q"),
    path("answered/", views.AnsweredQuestionListView.as_view(), name="answered_q"),
    path("indexed/", views.QuestionListView.as_view(), name="all_q"),
    # path("write-new-article/", views.CreateArticleView.as_view(), name="write_new"),
    # path("drafts/", views.DraftsListView.as_view(), name="drafts"),
    # path("<str:slug>/", views.ArticleDetailView.as_view(), name="article"),
    # path("edit/<int:pk>/", views.ArticleEditView.as_view(), name="edit_article"),


]
