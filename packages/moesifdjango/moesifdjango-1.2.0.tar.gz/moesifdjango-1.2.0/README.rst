Moesif Middleware for Python Django
===================================

Django middleware to log *incoming* REST API calls to Moesif's error
analysis platform.

`Source Code on GitHub <https://github.com/moesif/moesifdjango>`__

`Package on PyPI <https://pypi.python.org/pypi/moesifdjango>`__

This SDK uses the Requests library and will work for Python 2.7 — 3.5.

How to install
--------------

.. code:: shell

    pip install moesifdjango

How to use
----------

In your ``settings.py`` file in your Django project directory, please
add ``moesifdjango.middleware.moesif_middleware`` to the MIDDLEWARE
array.

Because of middleware execution order, it is best to add moesifdjango
middleware **below** SessionMiddleware and AuthenticationMiddleware,
because they add useful session data that enables deeper error analysis.
On the other hand, if you have other middleware that modified response
before going out, you may choose to place Moesif middleware **above**
the middleware modifying response. This allows Moesif to see the
modifications to the response data and see closer to what is going over
the wire.

Django middleware style and setup changed drastically from version 1.10.

For **Django 1.10 or newer**, the please add Middleware this way:

::

    MIDDLEWARE = [
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'moesifdjango.middleware.moesif_middleware'
        ...
    ]

For **Django 1.9 or older**, please add Middleware this way:

::

    MIDDLEWARE_CLASSES = [
        ...
        'moesifdjango.middleware_pre19.MoesifMiddlewarePre19',
        ...
        # other middlewares
    ]

Also, add ``MOESIF_MIDDLEWARE`` to your ``settings.py`` file,

::


    MOESIF_MIDDLEWARE = {
        'APPLICATION_ID': 'Your Application ID Found in Settings on Moesif',
        ...
        # other options see below.
    }

You can find your Application Id from `*Moesif
Dashboard* <https://www.moesif.com/>`__ -> *Top Right Menu* -> *App
Setup*

Configuration options
---------------------

**``APPLICATION_ID``**
^^^^^^^^^^^^^^^^^^^^^^

(**required**), *string*, is obtained via your Moesif Account, this is
required.

**``SKIP``**
^^^^^^^^^^^^

(optional) *(request, response) => boolean*, a function that takes a
request and a response, and returns true if you want to skip this
particular event.

**``IDENTIFY_USER``**
^^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => string*, a function that takes a
request and a response, and returns a string that is the user id used by
your system. While Moesif identify users automatically, and this
middleware try to use the standard Django request.user.username, if your
set up is very different from the standard implementations, it would be
helpful to provide this function.

**``GET_SESSION_TOKEN``**
^^^^^^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => string*, a function that takes a
request and a response, and returns a string that is the session token
for this event. Again, Moesif tries to get the session token
automatically, but if you setup is very different from standard, this
function will be very help for tying events together, and help you
replay the events.

**``GET_METADATA``**
^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => dictionary*, getMetadata is a
function that returns an object that allows you to add custom metadata
that will be associated with the event. The metadata must be a
dictionary that can be converted to JSON. For example, you may want to
save a VM instance\_id, a trace\_id, or a tenant\_id with the request.

**``MASK_EVENT_MODEL``**
^^^^^^^^^^^^^^^^^^^^^^^^

(optional) *(EventModel) => EventModel*, a function that takes an
EventModel and returns an EventModel with desired data removed. Use this
if you prefer to write your own mask function than use the string based
filter options: REQUEST\_BODY\_MASKS, REQUEST\_HEADER\_MASKS,
RESPONSE\_BODY\_MASKS, & RESPONSE\_HEADER\_MASKS. The return value must
be a valid EventModel required by Moesif data ingestion API. For details
regarding EventModel please see the `Moesif Python API
Documentation <https://www.moesif.com/docs/api?python>`__.

**``REQUEST_HEADER_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, is a list of strings for headers that you want
to hide from Moesif. Will be removed in future version. Replaced by the
function based 'MASK\_EVENT\_MODEL' for additional flexibility.

**``REQUEST_BODY_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, is a list of key values in the body that you
want to hide from Moesif. All key values in the body will be recursively
removed before sending to Moesif. Will be removed in future version.
Replaced by the function based 'MASK\_EVENT\_MODEL' for additional
flexibility.

**``RESPONSE_HEADER_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, performs the same function for response
headers. Will be removed in future version. Replaced by the function
based 'MASK\_EVENT\_MODEL' for additional flexibility.

**``RESPONSE_BODY_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, performs the same task for response body. Will
be removed in future version. Replaced by the function based
'MASK\_EVENT\_MODEL' for additional flexibility.

Example:
~~~~~~~~

.. code:: python

    def identifyUser(req, res):
        # if your setup do not use the standard request.user.username
        # return the user id here
        return "user_id_1"

    def should_skip(req, res):
        if "healthprobe" in req.path:
            return True
        else:
            return False

    def get_token(req, res):
        # if your setup do not use the standard Django method for
        # setting session tokens. do it here.
        return "token"

    def mask_event(eventmodel):
        # do something to remove sensitive fields
        # be sure not to remove any required fields.
        return eventmodel

    def get_metadata(req, res):
        return {
            'foo': '12345',
            'bar': '23456',
        }


    MOESIF_MIDDLEWARE = {
        'APPLICATION_ID': 'Your application id',
        'LOCAL_DEBUG': False,
        'IDENTIFY_USER': identifyUser,
        'GET_SESSION_TOKEN': get_token,
        'SKIP': should_skip,
        'MASK_EVENT_MODEL': mask_event,
        'GET_METADATA': get_metadata,
    }

Example
-------

An example Moesif integration based on quick start tutorials of Django
and Django Rest Framework: `Moesif Django
Example <https://github.com/Moesif/moesifdjangoexample>`__

Other integrations
------------------

To view more more documentation on integration options, please visit
**`the Integration Options
Documentation <https://www.moesif.com/docs/getting-started/integration-options/>`__.**
