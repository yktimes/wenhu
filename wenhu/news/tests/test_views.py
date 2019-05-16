from test_plus.test import TestCase
from wenhu.news.models import News
from django.test import Client
from django.urls import reverse


class NewViewsTest(TestCase):

    def setUp(self):
        self.user = self.make_user('user01')
        self.other_user = self.make_user('user02')

        self.client = Client()
        self.other_client = Client()

        self.client.login(username='user01', password="password")
        self.other_client.login(username='user01', password="password")

        self.first_news = News.objects.create(
            user=self.user,
            content='第一条动态'
        )

        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )

        self.third_news = News.objects.create(
            user=self.other_user,
            content="第一条动态的评论",
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        """测试动态列表页"""
        response = self.client.get(reverse('news:list'))
        assert response.status_code == 200
        assert self.first_news in response.context['news_list']
        assert self.third_news not in response.context['news_list']

    def test_delete_news(self):
        """删除动态"""
        initial_count = News.objects.count()
        response = self.client.post(reverse('news:delete_news', kwargs={'pk': self.second_news.pk}))
        assert response.status_code == 302
        assert News.objects.count() == initial_count - 1

    def test_post_news(self):
        initial_count = News.objects.count()
        response = self.client.post(reverse('news:post_news'), {'post': "我是杨凯"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        assert response.status_code == 200
        assert News.objects.count() == initial_count + 1

    def test_like_news(self):
        response = self.client.post(
            reverse('news:like_post'), {'news': self.first_news.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"  # 发送ajax请求

        )
        assert response.status_code == 200
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.get_likers()
        assert response.json()["likes"] == 1
