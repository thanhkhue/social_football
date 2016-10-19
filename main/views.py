from django.shortcuts import render

from rest_framework import generics


from .models import Field, Account, Match, Slot, City, District
from .serializers import (
    FieldSerializer, MatchSerializer,
    SlotSerializer, CitySerializer,
    DistrictSerializer
    )
# Create your views here.


class FieldList(generics.ListAPIView,
               generics.GenericAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FieldDetail(generics.RetrieveAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class MatchList(generics.ListAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MatchDetail(generics.RetrieveAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class SlotList(generics.ListAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SlotDetail(generics.RetrieveAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)