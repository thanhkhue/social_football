from rest_framework import serializers

from .models import Account, Field, Match, Slot, City, District

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field

class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match

class SlotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match

class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = City

class DistrictSerializer(serializers.ModelSerializer):
	class Meta:
		model = City