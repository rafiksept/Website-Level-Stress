"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from .views import AboutView, HomeListView, deleteView, komentarView, fotoUpdateView, index, loginView, logoutView, register_request, profile
from django.conf.urls.static import static

urlpatterns = [
    url(r'^about/$', AboutView, name='about'),
    url(r'^komentar/(?P<page>\d+)/(?P<pk1>\d+)/(?P<pk>\d+)$', deleteView, name='delete'),
    url(r'^komentar/(?P<page>\d+)/(?P<pk1>\d+)$', komentarView, name= 'komentar'),
    url(r'^cerita/', include('story.urls', namespace = 'cerita')),
    url(r'^login/$',loginView, name='login'),
    url(r'^register/$',register_request, name='register'),
    url(r'^logout/$',logoutView, name='logout'),
    url(r'^(?P<page>\d+)/$', HomeListView.as_view(), name = 'index'),
    url(r'^update/(?P<pk>\d+)/$',fotoUpdateView.as_view(),name='update'),
    url(r'^foto/$', index, name='ubah'),
    url(r'^$',profile, name='home' ),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
