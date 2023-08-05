import tempfile
import unittest

from click.testing import CliRunner

from pyutrack import Credentials
from pyutrack import cli
from pyutrack.config import Config


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config(tempfile.mkstemp()[1])
        self.config.credentials = Credentials('root', 'root')
        self.config.persist()

    def invoke_cli(self, *args, **kwargs):
        runner = CliRunner()
        return runner.invoke(cli.cli, *args, **kwargs)
