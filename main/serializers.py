from rest_framework import serializers

from .models import Account, Field, Match, Slot, City, District, Photo


class AccountSerializer(serializers.ModelSerializer):
    # name        = serializers.Field(source='get_full_name')

    class Meta:
        model = Account
        exclude = ('password', 'email',  'is_active', 
                   'groups', 'is_staff','is_superuser',
                   'created', 'time_zone')

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

    def to_native(self, object):
        data = super(MatchSerializer, self).to_native(object)
        print data
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