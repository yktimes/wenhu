from django.urls import path
from wenhu.articles import views
from django.views.decorators.cache import cache_page

app_name = 'articles' # 注意这里哈
urlpatterns = [

    path("", views.ArticlesListView.as_view(), name="list"),
    path("write-new-article/", views.CreateArticleView.as_view(), name="write_new"),
    path("drafts/", views.DraftsListView.as_view(), name="drafts"),
    path("<str:slug>/", cache_page(60*5)(views.DetailArticleView.as_view()), name="article"),
    path("edit/<int:pk>/", views.EditArticleView.as_view(), name="edit_article"),


]
