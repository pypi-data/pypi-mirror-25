Django Portmaster
=================

Django Portmaster is a network port allocation and management
microservice. With Portmaster, you can assign port ranges to different
services and register ports to different instances of those service.
This way you can prevent assigning the same port twice, thus preventing
assignement collision.

Installation
------------

1. Install using PIP.

::

    pip install django-portmaster

2. Add app to your Django project's settings file and include offer
   cleanup middleware.

.. code:: python

    INSTALLED_APPS = [
        [..]
        'django_portmaster'
    ]

    MIDDLEWARE = [
        [..]
        'django_portmaster.middleware.CleanOldOffersMiddleware'
    ]

3. Include Portmaster's URLs into your Django project's urls file.

.. code:: python

    from django_portmaster.urls import portmaster_urlpatterns
    urlpatterns += portmaster_urlpatterns

4. Optionally, you can override the time offers are kept before they are
   deleted. Add the following code to you settings.py file.

.. code:: python

    # Default value is 30 minutes
    PM_DELETE_OFFERS_AFTER_MINUTES = 10

API
---

-  Define port range by creating a service.

.. code:: javascript

    POST /v1/services

    {
       "name": "django",
       "description": "Django service",
       "start": 5000,
       "end": 10000
    }

-  Request a port from the range by providing a service instance name.

.. code:: javascript

    POST /v1/services/django/offers

    {
        "name": "web-01"
    }

Response

.. code:: javascript

    {
        "service": "django",
        "name": "web-01",
        "port": 5000,
        "secret": "6f8ffc86-d98a-49ba-848a-a7cbaaea9360",
        "created": "2017-09-08T14:16:39.277408Z"
    }

-  Port will not be allocated immediately. Instead it will be reserved
   until the client accepts the port by posting to the dedicated URL
   using the provided secret code:

.. code:: javascript

    POST /v1/services/django/offers/6f8ffc86-d98a-49ba-848a-a7cbaaea9360/accept

Response

.. code:: javascript

    {
        "service": "django",
        "name": "web-01",
        "port": 5000,
        "created": "2017-09-08T14:18:04.094357Z"
    }

-  Alternatively, you can reject the offer. Offers that are not accepted
   are automatically deleted by Portmaster middleware after they reach
   threshold set by ``PM_DELETE_OFFERS_AFTER_MINUTES`` setting (default
   value is 30 minutes).

.. code:: javascript

    POST /v1/services/django/offers/6f8ffc86-d98a-49ba-848a-a7cbaaea9360/reject

-  You can list all port alocations for a particular service.

.. code:: javascript

    GET /v1/services/django/ports

-  Find one by port number

.. code:: javascript

    GET /v1/services/django/ports/5000

-  Or find one by service instance name

.. code:: javascript

    GET /v1/services/django/ports/web-01

Safe guards
-----------

Portmaster includes multiple error checks and corner case handlers, so:

-  Service name needs to be unique
-  Port ranges can not overlap
-  Port range can not overlap with privileged ports (<1024) or IANA
   defined ephemeral port range (>49152)
-  Port can be assigned only once at any given time
-  Service instance name needs to be unique


