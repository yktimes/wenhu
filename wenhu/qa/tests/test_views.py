from test_plus.test import TestCase
from django.test import RequestFactory
from wenhu.users.views import UserUpdateView
from PIL import Image
import tempfile
from django.test import override_settings


class ArticleViewsTest(TestCase):
    @staticmethod
    def get_temp_img():
        """创建并读取临时图片文件"""

        size = (200, 200)
        color = (255, 0, 0, 0)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', size, color)
            image.save(f, 'PNG')
        return open(f.name, mode='rb')

    def setUp(self):
        self.test_image = self.get_temp_img()

    def tearDown(self):
        """测试结束关闭图片临时文件"""
        self.test_image.close()

    def test_index_articles(self):
        """测试文章列表页"""
        pass

    def test_error_404(self):
        """访问一篇不存在的文章"""
        pass

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_article(self):
        """文章创建成功后跳转"""
        pass

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_article(self):
        """测试草稿箱功能"""
        pass
