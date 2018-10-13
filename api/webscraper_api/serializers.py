from rest_framework import serializers
from .models import models


class ScrapeEndpointSerializer(serializers.Serializer):
    """Serializes all endpoints for the ESPNWebScraper"""

    league_id = serializers.IntegerField(
        max_value=None, min_value=0, required=True, allow_null=False)
    username = serializers.CharField(
        max_length=50, min_length=1, required=False)
    password = serializers.CharField(
        max_length=50, min_length=1, required=False)
