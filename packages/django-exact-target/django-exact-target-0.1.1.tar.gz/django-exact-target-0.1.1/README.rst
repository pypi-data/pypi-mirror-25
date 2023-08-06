===================
django-exact-target
===================

|  |license| |kit| |format| |downloads|

This library serves as a connector between `django` and the `Exact Target REST API <https://code.exacttarget.com/apis-sdks/rest-api/v1/routes.html>`_. It will support more of the API in the future, but currently only supports TriggeredSends.


Installation
============

Install using pip.::

    $ pip install django-exact-target

Add your exact target client settings to your Django project's settings.py file.::

    EXACT_TARGET_CLIENT_ID = 'my-client-id...'
    EXACT_TARGET_CLIENT_SECRET = 'my-client-secret...'

Usage
=====

Dispatch a `TriggeredSend`. See also `message definition sends <https://code.exacttarget.com/apis-sdks/rest-api/v1/messaging/messageDefinitionSends.html>`_.::

    from exacttarget.messages import TriggeredSend

    sender = TriggeredSend('my-triggered-send-id')
    sender.dispatch('foo@example.com', {
        # SubscriberAttributes
        "Region": "West",
        "City": "Indianapolis",
        "State": "IN"
    })


Changelog
=========

0.1.0
------------------
- Initial release.



.. |license| image:: https://img.shields.io/pypi/l/django-exact-target.svg
    :target: https://pypi.python.org/pypi/django-exact-target
.. |kit| image:: https://badge.fury.io/py/django-exact-target.svg
    :target: https://pypi.python.org/pypi/django-exact-target
.. |format| image:: https://img.shields.io/pypi/format/django-exact-target.svg
    :target: https://pypi.python.org/pypi/django-exact-target
.. |downloads| image:: https://img.shields.io/pypi/dm/django-exact-target.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/django-exact-target
