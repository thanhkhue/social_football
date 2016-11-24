from django.conf.urls import include, url
from . import views


urlpatterns = [
    # url(r'^stadium/$', views.CityList.as_view(), name='stadium_list'),
    url(r'^field/(?P<pk>\d+)/$',views.FieldDetail.as_view(), name='field_detail'),
    url(r'^fields/$', views.FieldList.as_view(), name='field_list'),
    url(r'^fieldlist/$', views.FieldListViewSet.as_view({'get': 'list'})),
    url(r'^match/(?P<pk>\d+)/$',views.MatchDetail.as_view(), name='match_detail'),
    url(r'^matches/$', views.MatchList.as_view(), name='match_list'),
    url(r'^slots/$', views.SlotList.as_view(), name='slot_list'),
    url(r'^slot/(?P<pk>\d+)/$',views.SlotDetail.as_view(), name='slot_detail'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^account/$', views.AccountView.as_view(), name='account_view'),
    url(r'^account/(?P<pk>\d+)/$', views.AccountDetail.as_view(), name='account_detail'),
    url(r'^comment/$', views.CommentList.as_view(), name='comments')
    ]