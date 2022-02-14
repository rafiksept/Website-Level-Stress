from unicodedata import name
from django.conf.urls import url
from .views import ceritaView, CeritaDetailView, CeritaListView, CeritaDeleteView
urlpatterns = [
    url(r'^riwayat/delete/(?P<pk>\d+)$', CeritaDeleteView.as_view(), name='delete'),
    url(r'^riwayat/(?P<page>\d+)$', CeritaListView.as_view(), name='riwayat'),
    url(r'^detail/(?P<pk>\d+)$', CeritaDetailView.as_view(), name='detail'),
    url('^tambah/$', ceritaView, name='tambah')
]