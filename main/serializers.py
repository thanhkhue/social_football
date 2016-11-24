from rest_framework import serializers

from .models import Account, Field, Match, Slot, City, District, Photo


class AccountSerializer(serializers.ModelSerializer):
    # name        = serializers.Field(source='get_full_name')

    class Meta:
        model = Account
        exclude = ('password', 'is_active', 
                   'groups', 'is_staff','is_superuser',
                   'created')

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('source_size_og','source_size_lg',
            'source_size_md', 'source_size_sm', 'source_size_xs', 'source_size_ss' )

class FieldSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer()
    # source_url = serializers.ReadOnlyField(source='photos', read_only=True)
    class Meta:
        model = Field
        fields = ('id', 'name', 'address', 'lat', 'lng', 'photo')

class MatchSerializer(serializers.ModelSerializer):

    field_id    = FieldSerializer()
    host_id     = AccountSerializer()
    class Meta:
        model = Match
        fields = ('id', 'field_id' , 'host_id', 'status', 'maximum_players', 'price', 'start_time', 'end_time', 'is_verified', 'slots')

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = City