import datetime
from http import HTTPStatus
from typing import Type

import requests
from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from jinja2 import Template
from jinja2.exceptions import TemplateSyntaxError

from .models import Content, ContentType, Notification, Subscription
from .models import User as UserNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    pass


class Arts(models.TextChoices):
    FILM = 'film', 'Film'
    SERIES = 'series', 'Series'


class NewEpisodeMailForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_id', 'art', 'event']

    art = forms.ChoiceField(choices=Arts.choices)
    event = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        content_id = self.cleaned_data.get('content_id')
        content_type = ContentType.NEW_FILM
        content = {'art': self.cleaned_data.get('art'), 'event': self.cleaned_data.get('event')}

        content_instance = super().save(commit=False)
        content_instance.content_type = content_type
        content_instance.content = content
        commit_content_instance = super().save(commit=commit)

        payload = {'content_id': str(content_id), 'content': {}}
        response = requests.post(settings.API_URL + settings.API_NEW_FILM_MAIL_ENDPOINT, json=payload)
        assert response.status_code == HTTPStatus.OK

        return commit_content_instance


class NewEpisodeMailAdmin(admin.ModelAdmin):
    """Редактор уведомлений по новому фильму или по новому сериалу"""

    form = NewEpisodeMailForm

    def get_queryset(self, request):
        return self.model.objects.filter(content_type=ContentType.NEW_FILM)


class UserRoles(models.TextChoices):
    UNAUTH = 'unauth', 'Unauthorized'
    SUB = 'sub', 'Subscribers'
    MOD = 'mod', 'Moderators'
    ALL = 'all', 'All'


class CustomMailForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_id', 'user_role', 'template']

    user_role = forms.ChoiceField(choices=UserRoles.choices)
    template = forms.CharField(widget=forms.Textarea)

    @staticmethod
    def validate_template(template):
        try:
            Template(template)
        except TemplateSyntaxError:
            raise forms.ValidationError('Template has incorrect syntax')

    @staticmethod
    def save_template_file(template):
        template_name = f'custom_mail_{datetime.datetime.now().isoformat()}.html'
        with open(settings.TEMPLATE_DIR / template_name, mode='w', encoding='utf-8') as f:
            f.write(template)
        return template_name

    def clean_template(self):
        template = self.cleaned_data.get('template')
        self.validate_template(template)
        return template

    def save(self, commit=True):
        content_id = self.cleaned_data.get('content_id')
        content_type = ContentType.CUSTOM_MAIL
        user_role = self.cleaned_data.get('user_role')
        template = self.cleaned_data.get('template')

        self.validate_template(template)

        template_path = self.save_template_file(template)

        content = {'user_role': user_role, 'template_path': template_path}

        content_instance = super().save(commit=False)
        content_instance.content_type = content_type
        content_instance.content = content
        commit_content_instance = super().save(commit=commit)

        nots_instance = Notification(content_id=content_id, content_type=content_type)
        nots_instance.save()

        payload = {'content_id': str(content_id), 'content': content}
        response = requests.post(settings.API_URL + settings.API_CUSTOM_MAIL_ENDPOINT, json=payload)
        assert response.status_code == HTTPStatus.OK

        return commit_content_instance


class CustomMailAdmin(admin.ModelAdmin):
    """Редактор групповой рассылки"""

    form = CustomMailForm

    def get_queryset(self, request):
        return self.model.objects.filter(content_type=ContentType.CUSTOM_MAIL)


def create_modeladmin(modeladmin, name: str, model: Type[Content]):
    """Регистрирует разные экземпляры админки для одной модели"""

    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


create_modeladmin(NewEpisodeMailAdmin, name='NewEpisodeMail', model=Content)
create_modeladmin(CustomMailAdmin, name='CustomMail', model=Content)
