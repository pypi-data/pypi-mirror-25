Introduction
============

.. image:: https://travis-ci.org/guillotinaweb/guillotina_rediscache.svg?branch=master
   :target: https://travis-ci.org/guillotinaweb/guillotina_rediscache


`guillotina_rediscache` implements redis into guillotina with an additional
in-memory layer cache.

In order to coordinate invalidating the in-memory cache, `guillotina_rediscache`
utilizes the pub/sub feature redis provides.



Configuration
-------------

app_settings for this::

    {
      "redis": {
          'host': 'localhost',
          'port': 6379,
          'ttl': 3600,
          'memory_cache_size': 1000,
          'pool': {
              'minsize': 5,
              'maxsize': 100
          }
      }
    }


TODO
----

- stats
- api endpoint to...
  - inspect, get stats
  - clear

1.0.5 (2017-10-02)
------------------

- Track all keys needing invalidation and do invalidation in an async task
  so the request can finish faster.
  [vangheem]


1.0.4 (2017-05-29)
------------------

- Test fixes
  [vangheem]


1.0.3 (2017-05-26)
------------------

- Fix delete not properly invalidating cache
  [vangheem]


1.0.2 (2017-05-15)
------------------

- Fix channel publishing invalidations
  [vangheem]


1.0.1 (2017-05-15)
------------------

- Fix release


1.0.0 (2017-05-15)
------------------

- initial release


