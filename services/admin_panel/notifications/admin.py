from django import forms
from django.contrib import admin
from django.db import models  # noqa: F401
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE  # noqa: F401

from .models import Template

admin.site.site_title = _('My site name')
admin.site.site_header = _('My site header')
admin.site.index_title = _('My index title')


class TemplateAdminForm(forms.ModelForm):
    """Form to use with cleanup extra tinymce stuff."""

    class Meta:
        """Just regular Meta class."""

        model = Template
        fields = '__all__'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = TemplateAdminForm
    # formfield_overrides = {  # noqa: E800
    #     models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},  # noqa: E800
    # }   # noqa: E800
    save_as = True
