import json
import requests
from enum import Enum

from admin_views.admin import AdminViews
from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django_json_widget.widgets import JSONEditorWidget

from .models import Notification, Subscription, User as UserNotification, ContentType


class NotificationAdmin(admin.ModelAdmin):
    """Общий редактор уведомлений"""
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


ART = (
    ('film', 'Film'),
    ('series', 'Series'),
)


class NotificationNewEpisodeForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['last_notification_send', 'art', 'event']

    art = forms.ChoiceField(choices=ART)
    event = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        content_type = ContentType.NEW_FILM

        content = {
            'art': self.cleaned_data.get('art'),
            'template_path': self.cleaned_data.get('event')
        }

        instance = super().save(commit=False)
        instance.content_type = content_type
        instance.content = content
        commit_instance = super().save(commit=commit)

        payload = {
            'notification_id': commit_instance.id,
            'content': content
        }
        requests.post('...', data=payload)

        return commit_instance


class NotificationNewEpisodeAdmin(admin.ModelAdmin):
    """Редактор уведомлений по новому фильму или по новому сериалу"""
    form = NotificationNewEpisodeForm

    def get_queryset(self, request):
        return Notification.objects.filter(content_type=ContentType.NEW_FILM)


USER_ROLES = (
    ('unauth', 'Unauthorized'),
    ('sub', 'Subscribers'),
    ('mod', 'Moderators'),
    ('all', 'All')
)


class NotificationExtraForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['last_notification_send', 'user_role', 'template']

    user_role = forms.ChoiceField(choices=USER_ROLES)
    template = forms.CharField(widget=forms.Textarea)

    @staticmethod
    def validate_template(template):
        return True

    @staticmethod
    def save_template_file(template):
        template_name = 'example.html'
        with open(settings.TEMPLATE_DIR / template_name, mode='w', encoding='utf-8') as f:
            f.write(template)
        return template_name

    def save(self, commit=True):
        content_type = ContentType.EXTRA_MAIL
        user_role = self.cleaned_data.get('user_role')
        template = self.cleaned_data.get('template')

        if not self.validate_template(template):
            pass

        template_path = self.save_template_file(template)

        content = {
            'user_role': user_role,
            'template_path': template_path
        }

        instance = super().save(commit=False)
        instance.content_type = content_type
        instance.content = content
        commit_instance = super().save(commit=commit)

        payload = {
            'notification_id': commit_instance.id,
            'content': content
        }
        requests.post('...', data=payload)

        return commit_instance


class NotificationExtraAdmin(admin.ModelAdmin):
    """Редактор внеочередной рассылки"""
    form = NotificationExtraForm

    def get_queryset(self, request):
        return Notification.objects.filter(content_type=ContentType.EXTRA_MAIL)


def create_modeladmin(modeladmin, name, model):
    """Регистрирует разные экземпляры админки для одной модели"""
    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


create_modeladmin(NotificationAdmin, name='notification-all', model=Notification)
create_modeladmin(NotificationNewEpisodeAdmin, name='notification-new', model=Notification)
create_modeladmin(NotificationExtraAdmin, name='notification-extra', model=Notification)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    pass

