A Little Box
============

A Little Box is a collection of extensions for the Django and its REST Frameworks, that commonly reuse across our project.

Requirements
------------

* Python: 2.7, 3.6
* Django: 1.11, 2.0

Setup
-----

Install from **pip**:

.. code-block:: sh

    pip install alittlebox

and then add it to your installed apps:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'alittlebox',
        ...
    ]

Configuration
-------------

You will also need to add a ...:

.. code-block:: python

    ALB = [
        ...
    ]

Using the DRY Routers
---------------------

No configuration necessary. Just import either one, declare the app_label and customize it. When you call its url properties it will generate and register all of the app's models you have not explicitly excluded. For example:

.. code-block:: python

    from django.conf.urls import url, include
    from alittlebox import routers, serializers, viewsets
    # use the DefaultRouter extension, alternatively you can use the DrySimpleRouter.
    router = routers.DryDefaultRouter()
    # it is mandatory to declare the app_label
    router.app_label = 'contracts'
    # below we customize the serializer and viewset classes
    # the defaults are ModelSerializer and ModelViewSet
    router.serializer_classes = (serializers.StrMethodModelSerializer, )
    router.viewset_classes = (viewsets.QuerysetModelViewSet, )
    # include the urls as you would with the DRF's routers
    urlpatterns = [
        url(r'^api/', include(router.urls)),
    ]
