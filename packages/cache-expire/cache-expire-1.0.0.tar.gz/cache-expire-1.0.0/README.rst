Cache expire
============

Memoize decorator with expire timeout.


Usage
-----

.. code-block:: python

   import requests
   from cache_expire import cache_with_timeout

   # It memoize return value with `*args` and `**kwargs`.
   @cache_with_timeout(60)
   def get_my_ip():
       # Slow-y network job here
       return requests.get('https://httpbin.org/ip').json()['origin']


