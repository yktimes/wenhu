from django.urls import path
from wenhu.articles import views


app_name = 'articles' # 注意这里哈
urlpatterns = [

    path("", views.ArticlesListView.as_view(), name="list"),
    path("write-new-article/", views.CreateArticleView.as_view(), name="write_new"),
    path("drafts/", views.DraftsListView.as_view(), name="drafts"),


]
