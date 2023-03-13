from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255


# class Template(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]  # noqa: E800
#     title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)  # noqa: E800
#     template_content = models.TextField(_('template_content'), blank=False)  # noqa: E800
#     template_short_description = models.TextField(_('template_short'), blank=False)  # noqa: E800
#     template_files = models.FilePathField(path='templates/', allow_folders=True, allow_files=False)  # noqa: E800

#     class Meta:  # noqa: E800
#         verbose_name = _('Template')  # noqa: E800
#         verbose_name_plural = _('Templates')  # noqa: E800
#         ordering = ['title']  # noqa: E800

#     def __str__(self):  # noqa: E800
#         return self.title[:15]  # noqa: E800


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
    event_type = models.CharField(max_length=TEXT_FIELD_LEN, choices=EventType.choices, default=EventType.NEW_CONTENT)
    subject = models.TextField(_('subject'), max_length=TEXT_FIELD_LEN, default='')
    template_files = models.FilePathField(path='templates/', allow_folders=True, allow_files=False)
    text_to_promo = models.TextField(max_length=4096, blank=True, default='')
    text_msg = models.TextField(max_length=4096, blank=True, default='')
    user_group = models.CharField(max_length=TEXT_FIELD_LEN, choices=UserGroup.choices, default=UserGroup.ALL_USER)

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']
