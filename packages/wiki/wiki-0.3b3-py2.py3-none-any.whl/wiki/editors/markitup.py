# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from wiki.core.compat import BuildAttrsCompat
from wiki.editors.base import BaseEditor

# Due to deprecation of django.forms.util in Django 1.9
try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

# Historical name of force_text(). Only available under Python 2.
try:
    from django.utils.encoding import force_unicode
except ImportError:
    def force_unicode(x):
        return(x)


class MarkItUpAdminWidget(BuildAttrsCompat, forms.Widget):

    """A simplified more fail-safe widget for the backend"""

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'markItUp',
                         'rows': '10', 'cols': '40', }
        if attrs:
            default_attrs.update(attrs)
        super(MarkItUpAdminWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs_compat(attrs, name=name)
        return mark_safe(
            '<textarea%s>%s</textarea>' %
            (flatatt(final_attrs),
             conditional_escape(
                force_unicode(value))))


class MarkItUpWidget(BuildAttrsCompat, forms.Widget):

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'markItUp',
                         'rows': '10', 'cols': '40', }
        if attrs:
            default_attrs.update(attrs)
        super(MarkItUpWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs_compat(attrs, name=name)
        return mark_safe(
            '<div><textarea%s>%s</textarea></div>' %
            (flatatt(final_attrs),
             conditional_escape(
                force_unicode(value))))


class MarkItUp(BaseEditor):
    editor_id = 'markitup'

    def get_admin_widget(self, instance=None):
        return MarkItUpAdminWidget()

    def get_widget(self, instance=None):
        return MarkItUpWidget()

    class AdminMedia:
        css = {
            'all': ("wiki/markitup/skins/simple/style.css",
                    "wiki/markitup/sets/admin/style.css",)
        }
        js = ("wiki/markitup/admin.init.js",
              "wiki/markitup/jquery.markitup.js",
              "wiki/markitup/sets/admin/set.js",
              )

    class Media:
        css = {
            'all': ("wiki/markitup/skins/simple/style.css",
                    "wiki/markitup/sets/frontend/style.css",)
        }
        js = ("wiki/markitup/frontend.init.js",
              "wiki/markitup/jquery.markitup.js",
              "wiki/markitup/sets/frontend/set.js",
              )
