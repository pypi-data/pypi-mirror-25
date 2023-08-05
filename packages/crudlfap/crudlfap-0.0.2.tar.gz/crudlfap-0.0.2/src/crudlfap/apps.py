"""Django AppConfig for the crudlfap module."""

from django import apps

from .views import generic


class DefaultConfig(apps.AppConfig):
    """Default AppConfig."""

    name = 'crudlfap'

    def get_default_views(self):  # pylint: disable=no-self-use
        """Return the default views to use in a new router."""
        return [
            generic.DeleteView,
            generic.UpdateView,
            generic.DetailView,
            generic.CreateView,
            generic.ListView,
        ]
