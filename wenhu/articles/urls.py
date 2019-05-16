from django.urls import path
from wenhu.articles import views


app_name = "articles" # 注意这里哈
urlpatterns = [

    path("", views.ArticlesListView.as_view(), name="list"),


]
