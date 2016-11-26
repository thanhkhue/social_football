from haystack import indexes
from .models import Field


class FieldIndex(indexes.SearchIndex, indexes.Indexable):
    text            = indexes.EdgeNgramField(document=True, use_template=True)
    location        = indexes.LocationField()

    def get_model(self):
        return Field

    def prepare(self, obj):
        prepared_data = super(FieldIndex, self).prepare(obj)
        return prepared_data

    def prepare_location(self, obj):
        return "%s,%s" % (obj.lat, obj.lng)

    def index_queryset(self, using=None):
        return self.get_model().objects.all()