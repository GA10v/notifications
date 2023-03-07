from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

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
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    save_as = True