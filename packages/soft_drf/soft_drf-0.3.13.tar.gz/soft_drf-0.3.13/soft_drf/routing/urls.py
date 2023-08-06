# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url

from soft_drf.doc.views import DRFDocsView


urlpatterns = [
    url(r'^v1/', include('soft_drf.routing.v1.urls', namespace='v1')),
]

if settings.SHOW_DOCUMENTATION:
    urlpatterns += [url(r'^docs/$', DRFDocsView.as_view(), name='docs')]
