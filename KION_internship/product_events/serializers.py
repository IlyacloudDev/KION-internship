from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ProductEventSerializer(serializers.Serializer):
    """
    Serializer for validating and processing product events.
    Validates the core fields used for deduplication with strict type checking.
    """

    # Required fields for deduplication
    client_id = serializers.CharField(
        max_length=64,
        allow_null=True,
        required=True,
        help_text=_('Unique client identifier (LowCardinality String)')
    )

    event_datetime = serializers.DateTimeField(
        required=True,
        help_text=_('Event timestamp in ISO 8601 format (DateTime)')
    )

    event_name = serializers.CharField(
        max_length=255,
        required=True,
        help_text=_('Type/name of the event (LowCardinality String)')
    )

    product_id = serializers.CharField(
        max_length=36,
        required=True,
        help_text=_('UUID identifier for the product (LowCardinality String)')
    )

    sid = serializers.CharField(
        max_length=128,
        required=True,
        help_text=_('Session identifier (LowCardinality String)')
    )

    r = serializers.CharField(
        max_length=128,
        required=True,
        help_text=_('Request identifier (LowCardinality String)')
    )

