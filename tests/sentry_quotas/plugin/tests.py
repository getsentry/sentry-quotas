import mock
from exam import fixture

from sentry_quotas.plugin import QuotasPlugin
from sentry.testutils import TestCase


class BasePluginTest(TestCase):
    plugin_class = QuotasPlugin

    @fixture
    def plugin(self):
        return self.plugin_class()


class PostProcessTest(BasePluginTest):
    @mock.patch.object(QuotasPlugin, 'incr')
    def test_calls_incr(self, incr):
        self.plugin.post_process(self.group, self.event, is_new=False, is_sample=True)
        incr.assert_called_once_with(self.group.project)


class IsOverQuotaTest(BasePluginTest):
    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'get_usage')
    def test_bails_immediately_without_quota(self, get_usage, get_events_per_minute):
        get_events_per_minute.return_value = None

        result = self.plugin.is_over_quota(self.project)

        get_events_per_minute.assert_called_once_with(self.project)

        assert result is False

    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'get_usage')
    def test_over_quota(self, get_usage, get_events_per_minute):
        get_events_per_minute.return_value = 100
        get_usage.return_value = 101

        result = self.plugin.is_over_quota(self.project)

        get_usage.assert_called_once_with(self.project)

        assert result is True

    @mock.patch.object(QuotasPlugin, 'get_events_per_minute')
    @mock.patch.object(QuotasPlugin, 'get_usage')
    def test_under_quota(self, get_usage, get_events_per_minute):
        get_events_per_minute.return_value = 100
        get_usage.return_value = 99

        result = self.plugin.is_over_quota(self.project)

        get_usage.assert_called_once_with(self.project)

        assert result is False
