from pyutrack import Connection, Issue
from pyutrack import Credentials
from pyutrack.errors import LoginError, NotFoundError
from tests.integration import IntegrationTest


class IssueTests(IntegrationTest):
    def setUp(self):
        super(IssueTests, self).setUp()
        self.connection  = Connection(
            credentials=Credentials(username='root', password='root'),
            base_url='http://localhost:9876'
        )

    def test_missing_issue(self):
        issue = Issue(self.connection, id='TEST-1')
        self.assertRaises(NotFoundError, issue.get)

    def test_hydrated_issue(self):
        issue = Issue(self.connection, id='PR0-1', hydrate=True)
        self.assertEqual(issue.id, 'PR0-1')
        self.assertEqual(issue.summary, 'issue 0')
        self.assertEqual(issue.description, 'issue 0')
