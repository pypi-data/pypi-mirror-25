from __future__ import unicode_literals

from django.views.generic.base import (
    TemplateResponseMixin, View, TemplateView, RedirectView)

from linkeddt.views.generic.base import SysConfContextMixin, PermissionMixin
from linkeddt.views.generic.detail import DetailView
from linkeddt.views.generic.edit import (
    FormView, CreateView, UpdateView, DeleteView, ImportView,
    MimeTypePostView, MimeTypeGetView, PkContextMixin, MimeTypeContextMixin)
from linkeddt.views.generic.list import ListView


__all__ = [
    'TemplateResponseMixin', 'View', 'TemplateView', 'RedirectView', 'DetailView', 'FormView',
    'CreateView', 'UpdateView', 'DeleteView', 'ImportView', 'ListView', 'GenericViewError', 'SysConfContextMixin',
    'PermissionMixin, MimeTypePostView', 'MimeTypeGetView', 'PkContextMixin', 'MimeTypeContextMixin'
]


class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
