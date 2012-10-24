"""
sentry_quotas.plugin
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from nydus.db import create_cluster
from sentry.plugins import Plugin

import logging
import time
import sentry_quotas

if not getattr(settings, 'SENTRY_QUOTAS', None):
    raise ImproperlyConfigured('You need to configure SENTRY_QUOTAS')


def get_cluster(hosts=None, router='nydus.db.routers.keyvalue.PartitionRouter'):
    if hosts is None:
        hosts = {
            0: {}  # localhost / default
        }

    return create_cluster({
        'engine': 'nydus.db.backends.redis.Redis',
        'router': router,
        'hosts': hosts,
    })

redis = get_cluster(settings.SENTRY_QUOTAS['redis'])


def get_default_events_per_minute():
    # It'd be nice if this were configurable via the sentry web interface (system level)
    return settings.SENTRY_QUOTAS.get('default_events_per_minute')


def get_per_minute_help_text():
    if get_default_events_per_minute():
        return _('The maximum events per minute before dropping data (system default is %s).') % get_default_events_per_minute()
    return _('The maximum events per minute before dropping data.')


class QuotasOptionsForm(forms.Form):
    per_minute = forms.CharField(label=_('Events / Minute'),
        help_text=get_per_minute_help_text())


class QuotasPlugin(Plugin):
    author = 'Sentry Team'
    author_url = 'https://github.com/getsentry/sentry'
    version = sentry_quotas.VERSION
    description = "Integrates quotas."
    resource_links = [
        ('Bug Tracker', 'https://github.com/getsentry/sentry-quotas/issues'),
        ('Source', 'https://github.com/getsentry/sentry-quotas'),
    ]

    slug = 'quotas'
    title = _('Quotas')
    conf_title = title
    conf_key = 'quotas'
    project_conf_form = QuotasOptionsForm

    logger = logging.getLogger('sentry_quotas')

    def get_events_per_minute(self, project):
        proj_setting = self.get_option('per_minute', project)
        if proj_setting is None:
            return int(get_default_events_per_minute())
        return int(proj_setting)

    def is_configured(self, project, **kwargs):
        return bool(self.get_events_per_minute(project))

    def incr(self, project, client=redis):
        # we store a key per minute
        key = 'sentry_quotas:%s:%s' % (project.id, int(time.time() / 60))
        with client.map() as conn:
            result = conn.incr(key)
            conn.expire(key, 60)

        return int(result)

    def is_over_quota(self, project):
        quota = self.get_events_per_minute(project)
        if not quota:
            return False

        if self.incr(project) > quota:
            return True

    def has_perm(self, user, perm, *objects, **kwargs):
        if perm == 'create_event':
            project = objects[0]

            if self.is_over_quota(project):
                self.logger.info('Project %r was over quota, event not recorded', project.slug)
                return False

        return None
