import pytest

from crudlfap.utils import view_reverse
from crudlfap.views.generic import View


class ExampleView(View):
    pass


class DerivedView(ExampleView):
    pass


def test_example_view():
    assert ExampleView.get_slug() == 'example'
    assert ExampleView.get_url_pattern() == 'example/$'


def test_derived_view():
    assert DerivedView.get_slug() == 'derived'
    assert DerivedView.get_url_pattern() == 'derived/$'


urlpatterns = [
    ExampleView.as_url(),
    ExampleView.as_url(slug='example2'),
]


@pytest.mark.urls('crudlfap.views.test_generic')
def test_view_with_slug():
    view = view_reverse('example')
    assert view.get_slug() == 'example'
    assert view.__name__ == ExampleView.__name__
    assert view.get_url_pattern() == 'example/$'
    assert view.get_app_label() == 'crudlfap'
'''
@pytest.mark.urls('crudlfap.views.test_generic')
def test_view_with_slug():
    view = view_reverse('example2')
    assert view == ExampleView
'''
