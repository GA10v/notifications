import uuid

from django.db import models


class ContentType(models.TextChoices):
    NEW_FILM = 'new_film'
    NEW_USER = 'new_user'
    REVIEW_LIKE = 'review_like'
    CUSTOM_MAIL = 'custom'


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_id = models.UUIDField(db_index=True)
    content_type = models.CharField(choices=ContentType.choices, max_length=15)
    last_update = models.DateTimeField(auto_now=True, null=True)
    last_notification_send = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notification'
        constraints = [
            models.UniqueConstraint(fields=['content_id', 'content_type'], name='idx_notification'),
        ]


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_id = models.UUIDField(db_index=True)
    content_type = models.CharField(choices=ContentType.choices, max_length=15)
    content = models.JSONField()

    class Meta:
        db_table = 'content'
        constraints = [
            models.UniqueConstraint(fields=['content_id', 'content_type'], name='idx_content'),
        ]


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    notification_id = models.UUIDField(db_index=True)
    last_notification_send_to_user = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'subscription'


class CommunicationType(models.TextChoices):
    WS = 'ws'
    EMAIL = 'email'
    TELEGRAM = 'telegram'


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    communication_method = models.CharField(choices=CommunicationType.choices, max_length=15)
    allow_communication = models.BooleanField()

    class Meta:
        db_table = 'user'
