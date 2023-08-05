#!/usr/bin/env python

from geonode.urls import urlpatterns, include, url

urlpatterns +=  [url('^', include('geonode_ows_endpoints.urls'))]
