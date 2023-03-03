from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin

TEXT_FIELD_LEN = 255


class Template(UUIDMixin, TimeStampedMixin):  # type: ignore[misc]
    title = models.CharField(_('title'), max_length=TEXT_FIELD_LEN, unique=True)
    template_content = models.TextField(_('template_content'), blank=True)

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['title']
