"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
import re

from django.conf.urls import url
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.views import generic


class ViewMixin(object):
    """
    Mixin to make crudlfa+ love a view.

    .. py:attribute:: slug

        Slug name of this view, often properly automatically generated
        from view class name uppon registration.

    .. py:attribute:: verbose_slug

        Verbose slug of the view for display.

    .. py:attribute:: url_pattern

        URL pattern to use for this view.
    """

    slug = None
    url_pattern = None
    style = 'default'
    fa_icon = 'question'
    material_icon = 'priority high'

    def get_template_names(self):
        """Give a chance to default_template_name."""
        template_names = super().get_template_names()
        default_template_name = getattr(self, 'default_template_name', None)
        if default_template_name:
            template_names.append(default_template_name)
        return template_names

    @classmethod
    def get_fa_icon(cls):
        return (
            getattr(cls, 'fa_icon', None) or
            getattr(cls.router, 'fa_icon', '')
        )

    @classmethod
    def as_url(cls, **kwargs):
        """Return the Django url object."""
        if kwargs:
            cls = type(cls.__name__, (cls,), kwargs)
        router = getattr(cls, 'router', None)
        prefix = router.prefix if router else ''
        return url(
            '{}{}'.format(prefix, cls.get_url_pattern()),
            cls.as_view(),
            name=cls.get_url_name(),
        )

    @classmethod
    def get_url_pattern(cls):
        """Return the url pattern for this view."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.get_slug())
        return '{}/$'.format(cls.get_slug())

    @classmethod
    def get_app_label(cls):
        """
        Return the app label for this view, used to prefix url name.

        If the view has an app_label attribute then return it.
        If the view has a model then return it's app label.
        Otherwise return the root module containing this class, this might
        work, might not, depending on your use case, I recommend to set
        app_label if the guess doesn't work for you.
        """
        import ipdb; ipdb.set_trace()
        app_label = getattr(cls, 'app_label', None)
        if app_label:
            return app_label

        model = getattr(cls, 'model', None)
        if model:
            return model._meta.app_label

        return cls.__module__.split('.')[0]

    @classmethod
    def get_slug(cls, remove=None):
        """
        Generate a slug from the view class.

        Strip  and 'View' suffix from view class name, will be added
        by router, YourModelCreateView gets the 'create' slug.
        """
        slug = getattr(cls, 'slug', None)
        if slug:
            return slug

        name = cls.__name__
        if remove:
            name = name.replace(remove, '')

        name = name.replace('View', '')
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def get_url_name(cls):
        """Return the url name for this view which has a router."""
        parts = []
        model = getattr(cls, 'model', None)
        if model:
            parts.append(model._meta.model_name)
        parts.append(cls.get_slug())
        return '_'.join(parts)

    @classmethod
    def get_url_args(cls, *args):  # pylint: disable=unused-argument
        """Return url reverse args given these args."""
        return args

    @classmethod
    def reverse(cls, *args):
        """Reverse a url to this view with the given args."""
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy(
            cls.get_url_name(),
            args=cls.get_url_args(*args)
        )

    def get_title_html(self):
        """Return text for HTML title tag."""
        return self.title

    def get_title_heading(self):
        """Return text for page heading."""
        return self.title


class View(ViewMixin, generic.View):
    """Base view for crudlfap+."""


class ModelViewMixin(ViewMixin):
    """Mixin for views using a Model class but no instance."""

    menus = ['model']

    @property
    def title(self):
        return '{} {}'.format(
            _(self.slug),
            self.model._meta.verbose_name_plural,
        ).capitalize()

    @property
    def fields(self):
        """Return router.fields or None, field names if ``__all__``."""
        fields = getattr(self.router, 'fields', None)
        if fields == '__all__':
            fields = [
                f.name for f in self.model._meta.fields
                if not f.primary_key or not getattr(
                    self, 'with_pk', False)
            ]
        return fields

    @property
    def exclude(self):
        """Return router.exclude or None, field names if ``__all__``.."""
        return getattr(self.router, 'ecxlude', None)


class ObjectViewMixin(ModelViewMixin):
    """Mixin for views using a Model instance."""

    menus = ['object']

    @classmethod
    def get_url_args(cls, *args):
        if '<slug>' in cls.get_url_pattern():
            return [args[0].slug]
        return [args[0].pk]

    @classmethod
    def get_url_pattern(cls):
        """Identify the object by slug or pk in the pattern."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.slug)

        try:
            cls.model._meta.get_field('slug')
        except FieldDoesNotExist:
            return r'(?P<pk>\d+)/{}/$'.format(cls.slug)
        else:
            return r'(?P<slug>[\w\d_-]+)/{}/$'.format(cls.slug)

    @property
    def title(self):
        return '{} {} "{}"'.format(
            _(self.slug),
            self.model._meta.verbose_name,
            self.object
        ).capitalize()


class FormViewMixin(ViewMixin):
    """Mixin for views which have a Form."""
    success_url_next = True

    def get_success_url(self):
        url = super().get_success_url()
        if self.success_url_next and '_next' in self.request.POST:
            url = self.request.POST['_next']
        return url


class FormView(FormViewMixin, generic.FormView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'crudlfap/form.html'


class ModelFormViewMixin(ModelViewMixin, FormViewMixin):
    """ModelForm ViewMixin using readable"""

    def form_invalid(self, form):
        messages.error(
            self.request,
            _(
                '{} {} error'.format(
                    self.slug,
                    self.model._meta.verbose_name
                ).capitalize()
            )
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(
            self.request,
            _(
                '%s %s: {}' % (self.slug, self.model._meta.verbose_name)
            ).format(form.instance).capitalize()
        )
        return super().form_valid(form)


class ObjectFormViewMixin(ObjectViewMixin, ModelFormViewMixin):
    """Custom form view mixin on an object."""


class ObjectFormView(ObjectFormViewMixin, generic.FormView):
    """Custom form view on an object."""


class CreateView(ModelFormViewMixin, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    fa_icon = 'plus'
    material_icon = 'add'
    default_template_name = 'crudlfap/create.html'
    target = 'modal'


class DeleteView(ObjectFormViewMixin, generic.DeleteView):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    target = 'modal'
    success_url_next = True

    def get_success_url(self):
        messages.success(
            self.request,
            _(
                '%s %s: {}' % (self.slug, self.model._meta.verbose_name)
            ).format(self.object).capitalize()
        )
        return self.router['list'].reverse()


class DetailView(ObjectViewMixin, generic.DetailView):
    """Templated model object detail view which takes a field option."""

    fa_icon = 'search-plus'
    material_icon = 'search'
    default_template_name = 'crudlfap/detail.html'

    @property
    def title(self):
        return str(self.object)

    def get_context_data(self, *a, **k):
        c = super(DetailView, self).get_context_data(*a, **k)
        c['fields'] = [
            {
                'field': self.model._meta.get_field(field),
                'value': getattr(self.object, field)
            }
            for field in self.fields
        ]
        return c

    @classmethod
    def get_url_pattern(cls):
        """Identify the object by slug or pk in the pattern."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.slug)

        try:
            cls.model._meta.get_field('slug')
        except FieldDoesNotExist:
            return r'(?P<pk>\d+)/$'
        else:
            return r'(?P<slug>[\w\d_-]+)/$'


class ListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'
    url_pattern = '$'
    paginate_by = 10
    fa_icon = 'table'
    material_icon = 'list'
    menus = ['main']


class UpdateView(ObjectFormViewMixin, generic.UpdateView):
    """Model update view."""

    fa_icon = 'edit'
    material_icon = 'edit'
    default_template_name = 'crudlfap/update.html'
    target = 'modal'
