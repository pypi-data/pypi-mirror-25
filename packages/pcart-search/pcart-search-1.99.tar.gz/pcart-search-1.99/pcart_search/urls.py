from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^quick-search/$', views.quick_search, name='quick-search'),
]
