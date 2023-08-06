from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RSSView.as_view(), name='rss_xml_view'),
]
