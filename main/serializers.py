from rest_framework import serializers

from .models import Account, Field

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field