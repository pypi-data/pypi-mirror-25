from tests.integration import IntegrationTest
from tests.integration.cli import CliTestCase


class InitializationTest(IntegrationTest, CliTestCase):
    def test_custom_config(self):
        res = self.invoke_cli(['--config=%s' % self.config.path])
        print(res.output)
