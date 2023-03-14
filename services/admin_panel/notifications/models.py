from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255


class Template(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]
    class EventType(models.TextChoices):
        WELCOME = 'welcome_message'
        NEW_CONTENT = 'new_content'
        NEW_LIKES = 'new_likes'
        PROMO = 'promo'

    class UserGroup(models.TextChoices):
        ALL_USER = 'all'
        GROUP_1 = 'group_1'
        GROUP_2 = 'group_2'
        GROUP_3 = 'group_3'
        GROUP_4 = 'group_4'

    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    event_type = models.CharField(
        _('event_type'),
        max_length=TEXT_FIELD_LEN,
        choices=EventType.choices,
        default=EventType.NEW_CONTENT,
    )
    subject = models.CharField(_('subject'), max_length=TEXT_FIELD_LEN, default='')
    template_files = models.FilePathField(_('template_files'), path='templates/', allow_folders=True, allow_files=False)
    text_to_promo = models.TextField(_('text_to_promo'), max_length=4096, blank=True, default='')
    text_msg = models.TextField(_('text_msg'), max_length=4096, blank=True, default='')
    user_group = models.CharField(
        _('user group'),
        max_length=TEXT_FIELD_LEN,
        choices=UserGroup.choices,
        default=UserGroup.ALL_USER,
    )

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']

    def __str__(self):
        return f'{self.title:15} - {self.event_type:15} - {self.subject:15}'
