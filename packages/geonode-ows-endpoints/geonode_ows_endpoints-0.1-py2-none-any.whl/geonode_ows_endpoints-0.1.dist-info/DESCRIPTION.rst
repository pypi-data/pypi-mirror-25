GeoNode OWS endpoints
---------------------

This is simple application that will list used OWS (WMS, WFS and other) endpoints used by GeoNode instance. If integrated with directions from this file, endpoints should be available at `/api/ows_endpoints/` path.

Requirements
============

*GeoNode<2.7 instance*. GeoNode 2.7 and newer have this application in core. This package is a backport of that application for older installations.

Installation
============

1. install package with PIP:

```
pip install geonode-ows-endpoints
```

2. customize urls


 If you have customized urls, add following code to your urls file:

```

urlpatterns +=  [url('^', include('geonode_ows_endpoints.urls'))]

```
 If you don't have customized urls, you can use urlpatterns provided by this application in `geonode_ows_endpoints.custom_urls`.  Then, you should also add following line to your settings file:

```
ROOT_URLCONF = 'geonode_ows_endpoints.custom_urls'
```


3. update your settings

Include this in your settings.py file (or settings module pointed by `DJANGO_SETTINGS_MODULE`):

```
INSTALLED_APPS += ('geonode_ows_endpoints',)

```

Usage
=====

This application exposes URL which lists endpoints to OWS used by layers. It is used by GeoHealthCheck to automatically populate monitored resources from URL to home page of GeoNode instance.


