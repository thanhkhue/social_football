from rest_framework import serializers

from .models import Account, Field, Match, Slot, City, District, Photo, Comment


class AccountSerializer(serializers.ModelSerializer):
    # name        = serializers.Field(source='get_full_name')

    class Meta:
        model = Account
        exclude = ('password', 'is_active', 
                   'groups', 'is_staff','is_superuser',
                   'created')

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('user', 'comment','date_created')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('img1', 'img2', 'img3')

class FieldSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer()
    class Meta:
        model = Field

class MatchSerializer(serializers.ModelSerializer):

    field_id    = FieldSerializer()
    host_id     = AccountSerializer()
    class Meta:
        model = Match
        fields = ('id', 'sub_match', 'field_id' , 'host_id', 'maximum_players', 'price', 'start_time', 'end_time', 'is_verified', 'slots')

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District

