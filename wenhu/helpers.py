from django.http import HttpResponseBadRequest
from functools import wraps
from django.views.generic import View
from django.core.exceptions import PermissionDenied
def ajax_required(f):
    """检验是否是ajax请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('不是AJAX请求')
        return f(request, *args, **kwargs)

    return wrap

class AuthorRequireMixin(View):
    """
    验证是否为原作者，用于状态删除、文章编辑
    :param View:
    :return:
    """
    def dispatch(self, request, *args, **kwargs):
        # 状态和文章实例有user属性
        if self.get_object().user.username!=self.request.user.username:
            raise PermissionDenied

        return super().dispatch(request,*args,**kwargs)
