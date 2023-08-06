========
 Djpush
========

Manage programatic *Push Notifications* from Django admin.

Features
========
 - Define notifications via the admin
 - Categorize notifications
 - Schedule notifications by category
 - Choose your provider(APNS/apns2, GCM/gcm, OneSignal/yaosac). Actually you must install one.
 - (optional) Multiple language support via django-modelstranslation

Important Dependencies
======================
 - celery
 - django-timezone-field
 - pytz

Usage
=====
.. code-block:: python

   # Get a notification, you define them in the admin
   notification = models.Notification.objects.get(slug='a-slug', enabled=True)

   # Create a notification instance
   notification_instance = models.NotificationInstance.objects.create(notification=notification, tokens=tokens, data=data)

   # Send the notification
   notification_instance.send()

Development
===========

Update migrations
-----------------
::

   DJANGO_SETTINGS_MODULE=migration_settings django-admin makemigrations

Run tests
---------
::

   ./runtests.py

Build/Publish
-------------
::

   python setup.py sdist bdist_wheel
   twine upload dist/*
