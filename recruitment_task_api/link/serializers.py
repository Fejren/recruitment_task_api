from rest_framework import serializers

from link.models import ExpiringLink


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = '__all__'
