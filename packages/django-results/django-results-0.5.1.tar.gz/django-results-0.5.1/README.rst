==============
django-results
==============

提供django下结果页

Quick start
-----------
1. Install::

    pip install django_results

2. Add "results" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'results',
    ]

3. No Migrations

4. Create results view::

    # config in urls
    from results.views import ResultView
    from sample import views as sample_views
    urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='sample/index.html')),

        url('^result-view-class/$',
            ResultView.as_view(template_name='results/result.html',
                               title='sample出错标题',
                               message='sample出错信息',
                               type='info'),
            name='result_view_class'),

        url(r'^form-error/$', sample_views.form_error_view, name='form_error'),

        url(r'^error-result/$', ResultView.error_view, dict(title='出错标题', message='ResultView.error_view'),
            name='error_result'),
        url(r'^error-result/object-does-not-exist/$', ResultView.error_view, dict(error=ObjectDoesNotExist()),
            name='error_result_object_does_not_exist'),

        url(r'^result-view/success/$',
            ResultView.success_view,
            {"title": "success的标题", "message": "success的消息"}, name='result_view_success'),
        url(r'^result-view/danger/$',
            ResultView.error_view,
            {"title": "danger的标题", "message": "danger的消息"}, name='result_view_danger'),
        url(r'^result-view/info/$',
            ResultView.info_view,
            {"title": "info的标题", "message": "info的消息"}, name='result_view_info'),
    ]

    # handle form error in views
    def form_error_view(request):
        class TestForm(forms.Form):
            required_field = forms.CharField(required=True)

            invalid_field = forms.CharField(max_length=1)

            def clean(self):
                raise forms.ValidationError('non field error happened')

        form = TestForm(data={'invalid_field': 'xxxxx'})

        return ResultView.error_view(request, title='这里有一个错误', message='不知道当讲不当讲，算了我还是讲了', error=form.errors)

