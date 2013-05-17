import mock
from exam import fixture

from sentry_quotas.plugin import QuotasPlugin
from sentry.testutils import TestCase


class BasePluginTest(TestCase):
    plugin_class = QuotasPlugin

    @fixture
    def plugin(self):
        return self.plugin_class()


class IsOverQuotaTest(BasePluginTest):
    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'incr')
    def test_bails_immediately_without_quota(self, incr, get_events_per_minute):
        get_events_per_minute.return_value = None

        result = self.plugin.is_rate_limited(self.project)

        get_events_per_minute.assert_called_once_with(self.project)
        assert not incr.called
        assert result is False

    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'incr')
    def test_over_quota(self, incr, get_events_per_minute):
        get_events_per_minute.return_value = 100
        incr.return_value = 101

        result = self.plugin.is_rate_limited(self.project)

        incr.assert_called_once_with(self.project)
        assert result is True

    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'incr')
    def test_under_quota(self, incr, get_events_per_minute):
        get_events_per_minute.return_value = 100
        incr.return_value = 99

        result = self.plugin.is_rate_limited(self.project)

        incr.assert_called_once_with(self.project)
        assert result is False
