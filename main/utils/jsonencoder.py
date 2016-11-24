import datetime
import decimal
import json as json_mod
from bson import ObjectId
from social_football import settings

from rest_framework.views import APIView
from rest_framework.renderers import XMLRenderer



class JSONEncoder(json_mod.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.date):
            return o.strftime(settings.DATETIME_FORMAT_TIMEZONE)
        if isinstance(o, datetime.datetime):
            return o.strftime(settings.DATETIME_FORMAT_TIMEZONE)
        if isinstance(o, datetime.time):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return float(o)
        return json_mod.JSONEncoder.default(self, o)

class MultiRenderersAPIView(APIView):
    def get_renderers(self):
        output = self.request.REQUEST.get('output', 'json')
        if output == 'xml':
            return [XMLRenderer()]
        return super(MultiRenderersAPIView, self).get_renderers()        