from django.shortcuts import render

from rest_framework import generics


from .models import Field, Account
from .serializers import FieldSerializer
# Create your views here.


class FieldList(generics.ListAPIView,
               generics.GenericAPIView):
    ''' Only let view a list of city '''
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FieldDetail(generics.RetrieveAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
