sentry-quotas
===============

An extension for Sentry which allows setting hard limits.

Install
-------

Install the package via ``pip``::

    pip install sentry-quotas



Configuration
-------------

Configure ``SENTRY_QUOTAS`` in your ``sentry.conf.py``:


::

    SENTRY_QUOTAS = {
        'redis': {
            'hosts': {
                # for more information on configuring hosts, see the documentation for the
                # Nydus python package
                0: {
                    'host': 'localhost',
                    'port': 6379
                }
            }
        },
        'default_events_per_minute': 100,
    }

The ``default_events_per_minute`` setting is optional.

Per Project Settings
~~~~~~~~~~~~~~~~~~~~

You'll find a setting under each project that the plugin is enabled for which allows overriding the default
events per minute setting.
