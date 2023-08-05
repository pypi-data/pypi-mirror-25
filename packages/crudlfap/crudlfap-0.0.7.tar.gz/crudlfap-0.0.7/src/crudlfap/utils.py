from django.urls.base import get_resolver, get_urlconf
from django.core.urlresolvers import reverse


def view_reverse(url_name, urlconf=None):
    """Return the View class for a url name."""
    urlconf = urlconf or get_urlconf()
    resolver = get_resolver(urlconf)

    for url_pattern in resolver.url_patterns:
        if url_pattern.name == url_name:
            return url_pattern.callback.view_class
