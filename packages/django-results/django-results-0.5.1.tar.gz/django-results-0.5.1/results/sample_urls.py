from django import forms
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from results.views import ResultView


def form_error_view(request):
    class TestForm(forms.Form):
        required_field = forms.CharField(required=True)

        invalid_field = forms.CharField(max_length=1)

        def clean(self):
            raise forms.ValidationError('non field error happened')

    form = TestForm(data={'invalid_field': 'xxxxx'})

    return ResultView.error_view(request, title='这里有一个错误', message='不知道当讲不当讲，算了我还是讲了', error=form.errors)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='results/sample_index.html')),

    url(r'^result-view/success/$',
        ResultView.success_view,
        {"title": "success的标题", "message": "success的消息"}, name='result_view_success'),
    url(r'^result-view/danger/$',
        ResultView.error_view,
        {"title": "error的标题", "message": "error的消息"}, name='result_view_error'),
    url(r'^result-view/info/$',
        ResultView.info_view,
        {"title": "info的标题", "message": "info的消息"}, name='result_view_info'),

    url(r'^form-error/$', form_error_view, name='form_error'),
    url(r'^error-result/object-does-not-exist/$', ResultView.error_view, dict(error=ObjectDoesNotExist()),
        name='error_result_object_does_not_exist'),
]
