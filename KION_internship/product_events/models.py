from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class ProductEvent(models.Model):
    """
    Model for storing deduplicated product events from KION platform.

    Stores complete event data in JSON format while maintaining unique UUID identifier.
    All events in this model are guaranteed to be unique (after deduplication process).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('Event ID'),
        help_text=_('Unique identifier for the product event (UUID4)')
    )

    event_data = models.JSONField(
        verbose_name=_('Event Data'),
        help_text=_('Complete product event data in JSON format after deduplication'),
    )

    class Meta:
        verbose_name = _('Product Event')
        verbose_name_plural = _('Product Events')

