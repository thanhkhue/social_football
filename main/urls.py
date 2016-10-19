from django.conf.urls import include, url
from . import views


urlpatterns = [
    # url(r'^stadium/$', views.CityList.as_view(), name='stadium_list'),
    url(r'^field/(?P<pk>\d+)/$',views.FieldDetail.as_view(), name='field_detail'),
    url(r'^fields/$', views.FieldList.as_view(), name='field_list'),
    ]