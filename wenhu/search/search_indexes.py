
import datetime
from haystack import indexes
from wenhu.news.models import News
from wenhu.articles.models import Article
from wenhu.qa.models import Question
from django.contrib.auth import get_user_model
from taggit.models import Tag


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """文章模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/articles_text.txt')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated.
            当索引有更新时
        """
        return self.get_model().objects.filter(status="P",updated_at__lte=datetime.datetime.now())



class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    """对News模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/news_text.txt')

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(reply=False, updated_at__lte=datetime.datetime.now())


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    """对Question模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/questions_text.txt')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """对User模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/users_text.txt')

    def get_model(self):
        return get_user_model()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())


class TagsIndex(indexes.SearchIndex, indexes.Indexable):
    """对Tags模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/tags_text.txt')

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
