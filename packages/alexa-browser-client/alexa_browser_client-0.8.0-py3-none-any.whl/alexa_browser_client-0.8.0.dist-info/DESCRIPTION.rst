Alexa Browser Client
====================

|code-climate-image| |circle-ci-image| |codecov-image| |gemnasium-image|

**Alexa client in your browser. Django app. Talk to Alexa from your
desktop, phone, or tablet browser.**

--------------

Dependencies
------------

This project depends on: -
`django-channels <https://channels.readthedocs.io/en/stable/>`__. -
`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__

Install and configure those first.

Snowboy
~~~~~~~

`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__
detects when the wakeword "Alexa" is uttered.

You must compile
`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__
manually. Copy the compiled ``snowboy`` folder to the top level of you
project. By default, the folder structure should be:

::

    .
    ├── ...
    ├── snowboy
    |   ├── snowboy-detect-swig.cc
    |   ├── snowboydetect.py
    |   └── resources
    |       ├── alexa.umdl
    |       └── common.res
    └── ...

If the default folder structure does not suit your needs you can
`customize the wakeword detector <#wakeword>`__.

Installation
------------

::

    pip install alexa_browser_client

Add ``alexa_browser_client`` to your settings ``INSTALLED_APPS``.

Routing and urls
~~~~~~~~~~~~~~~~

Add ``url(r'^', include('alexa_browser_client.config.urls')),`` to
``urls.py`` ``url_patterns``.

Add ``include('alexa_browser_client.config.routing.channel_routing')``
to your ``routing.py`` ``channel_routing``.

Authentication
--------------

This app uses Alexa Voice Service. To use AVS you must first have a
`developer account <http://developer.amazon.com>`__. Then register your
product
`here <https://developer.amazon.com/avs/home.html#/avs/products/new>`__.
Choose "Application" under "Is your product an app or a device"?

Ensure you update your settings.py:

+-------------------------------------+--------------------------------------+
| Setting                             | Notes                                |
+=====================================+======================================+
| ``ALEXA_BROWSER_CLIENT_AVS_CLIENT_I | Retrieve by clicking on the your     |
| D``                                 | product listed                       |
|                                     | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+
| ``ALEXA_BROWSER_CLIENT_AVS_CLIENT_S | Retrieve by clicking on the your     |
| ECRET``                             | product listed                       |
|                                     | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+
| ``ALEXA_BROWSER_CLIENT_AVS_REFRESH_ | You must generate this. `See         |
| TOKEN``                             | here <#refresh-token>`__             |
+-------------------------------------+--------------------------------------+
| ``ALEXA_BROWSER_CLIENT_AVS_DEVICE_T | Retrieve by reading "Product ID"     |
| YPE_ID``                            | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+

Refresh token
~~~~~~~~~~~~~

You will need to login to Amazon via a web browser to get your refresh
token.

To enable this first go
`here <https://developer.amazon.com/avs/home.html#/avs/home>`__ and
click on your product to set some security settings under
``Security Profile``:

+-----------------------+------------------------------------+
| setting               | value                              |
+=======================+====================================+
| Allowed Origins       | https://localhost:9000             |
+-----------------------+------------------------------------+
| Allowed Return URLs   | https://localhost:9000/callback/   |
+-----------------------+------------------------------------+

Then run:

.. code:: sh

    ./manage.py create_amazon_refresh_token

Follow the on-screen instructions shown at ``http://localhost:9000`` in
your web browser. On completion Amazon will return your
``refresh_token``. Set your\ ``ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN``
setting accordingly.

Usage
-----

Once you have all the settings configured:

-  Run django: ``./manage.py runserver``
-  Go to ``http://localhost:8000/alexa-browser-client/`` and start
   talking to Alexa.

Customization
-------------

Wakeword
~~~~~~~~

The default wakeword is "Alexa". You can change this by customizing the
lifecycle's ``audio_detector_class``:

.. code:: py

    # my_project/consumers.py

    import alexa_browser_client
    import command_lifecycle


    class CustomAudioDetector(command_lifecycle.wakeword.SnowboyWakewordDetector):
        wakeword_library_import_path = 'dotted.import.path.to.wakeword.Detector'
        resource_file = b'path/to/resource_file.res'
        decoder_model = b'path/to/model_file.umdl'


    class CustomAudioLifecycle(alexa_browser_client.AudioLifecycle):
        audio_detector_class = CustomAudioDetector


    class CustomAlexaConsumer(alexa_browser_client.AlexaConsumer):
        audio_lifecycle_class = CustomAudioLifecycle

Then in your ``routes.py``:

::

    from my_project import consumers


    channel_routing = [
        consumers.CustomAlexaConsumer.as_route(path='/'),
    ]

Unit test
---------

To run the unit tests, call the following commands:

.. code:: sh

    pip install -r requirements-dev.txt
    ./scripts/tests.sh

To test a specific file, call the following command:

.. code:: sh

    ./scripts/tests.sh /path/to/test-file.py

Other projects
--------------

This project uses `Voice Command
Lifecycle <https://github.com/richtier/voice-command-lifecycle>`__ and
`Alexa Voice Service
Client <https://github.com/richtier/alexa-voice-service-client>`__.

.. |code-climate-image| image:: https://codeclimate.com/github/richtier/alexa-browser-client/badges/gpa.svg
   :target: https://codeclimate.com/github/richtier/alexa-browser-client
.. |circle-ci-image| image:: https://circleci.com/gh/richtier/alexa-browser-client/tree/master.svg?style=svg
   :target: https://circleci.com/gh/richtier/alexa-browser-client/tree/master
.. |codecov-image| image:: https://codecov.io/gh/richtier/alexa-browser-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/richtier/alexa-browser-client
.. |gemnasium-image| image:: https://gemnasium.com/badges/github.com/richtier/alexa-browser-client.svg
   :target: https://gemnasium.com/github.com/richtier/alexa-browser-client


