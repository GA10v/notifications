import uuid

from django.db import models


class ContentType(models.TextChoices):
    NEW_FILM = 'new_film'
    NEW_USER = 'new_user'
    REVIEW_LIKE = 'review_like'
    EXTRA_MAIL = 'extra'


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(choices=ContentType.choices, max_length=15)
    content = models.JSONField()
    last_update = models.DateTimeField(auto_now=True)
    last_notification_send = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notification'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    last_notification_send_to_user = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'subscription'


class CommunicationType(models.TextChoices):
    WS = 'ws'
    EMAIL = 'email'
    TELEGRAM = 'telegram'


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    communication_method = models.CharField(choices=CommunicationType.choices, max_length=15)
    allow_communication = models.BooleanField()

    class Meta:
        db_table = 'user'
