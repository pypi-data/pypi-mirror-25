import pytest

from django.db import models

from .jinja2 import get_view
from .routers import Router
from .views.generic import View


class Artist(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False


class ExampleView(View):
    pass


test_urls = [
    Router(Artist).urlpatterns(),
    ExampleView.as_url(),
]


@pytest.mark.urls('crudlfap.test_utils.test_urls')
def test_get_view_by_url_name():
    pass
