from django.core.management.base import BaseCommand

from haystack.query import SearchQuerySet
from haystack.utils.geo import Point, D

from main.models import Field



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        all_fields = Field.objects.all()
        for f in all_fields:
            location = Point(float(f.lng),float(f.lat))
            print location
            Field.objects.filter(pk=f.id).update(location=location)
