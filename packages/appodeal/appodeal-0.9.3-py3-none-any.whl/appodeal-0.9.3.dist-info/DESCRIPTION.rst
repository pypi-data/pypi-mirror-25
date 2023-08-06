============
 DjAppodeal
============

Django application for `Appodeal <https://www.appodeal.com/home/>`_ integration.

Install
=======

  - Add 'appodeal' to `INSTALLED_APPS`
  - Add `url(r'^/', include('appodeal.urls')),` to `urls.py`
  - (optional) Add `APPODEAL_SECRET_ANDROID`  to `settings.py`
  - (optional) Add `APPODEAL_SECRET_IOS` to `settings.py`
  - Add `APPODEAL_REWARD_CREATE_HANDLER` to `settings.py`
  - Run `python manage.py migrate`. 
  - Add the callback URL in Appodeal "{https://example.com/reward/}?data1={data1}&data2={data2}"

Handler
=======

It will be called with:

:output:
  A `dict` with the decrypted data from Appodeal
:rewards:
  A `appodeal.Reward` `QuerySet` with all the records with the same `impression_id`.

Should return a string that will be stored as `result` in the reward record.

If your handler fails the exception representation will be stored as the `result`.

`output` example
----------------

.. code-block:: python

   {
     'user_id': user_id,
     'amount': amount,
     'currency': currency,
     'impression_id': impression_id,
     'timestamp': timestamp,
     'hash': hash,
     'output': output
   }


Run tests
---------

::

   ./runtests.py

Build/Publish
-------------

::

   python setup.py sdist bdist_wheel
   twine upload dist/*


