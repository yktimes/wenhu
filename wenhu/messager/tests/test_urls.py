from test_plus.test import TestCase
from django.urls import reverse, resolve


class TestUserURLs(TestCase):

    def setUp(self):
        self.user = self.make_user()

    # 反向解析 从命名反向网址
    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={'username': 'testuser'}), '/users/testuser/')

    # 字符串的网址解析到命名路由
    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/testuser/').view_name, 'users:detail')

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), '/users/update/')

    # 字符串的网址解析到命名路由
    def test_update_resolve(self):
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')
