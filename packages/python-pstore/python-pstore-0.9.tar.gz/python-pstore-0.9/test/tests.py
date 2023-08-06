import unittest
import mock
import uuid
import random
import string

from pythonpstore.pythonpstore import SecretStore
from mock_client import MockClient


class TestSecret(unittest.TestCase):

    def setUp(self):

        super(TestSecret, self).setUp()

        # Get the secret store.
        self.store = SecretStore()

    def test_secret_for_key(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'included',
            '/project/prod/env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            secret = self.store.get_secret_for_key('/project/dev/env')

            # Check the value.
            self.assertEqual(secrets['/project/dev/env'], secret,
                             msg='The wrong secret was returned')

    def test_secret_for_key_empty(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'included',
            '/project/prod/env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            secret = self.store.get_secret_for_key('/project/test/env')

            # Check the value.
            self.assertIsNone(secret, msg='Something was returned when nothing should be returned')


class TestPathSecrets(unittest.TestCase):

    def setUp(self):

        super(TestPathSecrets, self).setUp()

        # Get the secret store.
        self.store = SecretStore()

    def test_secrets_for_path(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'included',
            '/project/prod/env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev', recursive=False)

            # Check secrets.
            self.assertTrue(len(_secrets) == 1,
                            msg='Only one secret should have been returned')

            # Check the value.
            self.assertEqual(secrets['/project/dev/env'], _secrets['ENV'],
                             msg='Prioritized secret was not returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_path_empty(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'included',
            '/project/prod/env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/test', recursive=False)

            # Check the value.
            self.assertTrue(len(_secrets) == 0, msg='Something was returned when nothing should be returned')

    def test_secrets_priority(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'excluded',
            '/project/dev/testing/env': 'included',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev/testing', recursive=True)

            # Check secrets.
            self.assertTrue(len(_secrets) == 1,
                            msg='Only one secret should have been returned')

            # Check the value.
            self.assertEqual(secrets['/project/dev/testing/env'], _secrets['ENV'],
                             msg='Prioritized secret was not returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets(self):

        # Setup the data.
        secrets = {
            '/project/env': 'excluded',
            '/project/dev/env': 'included',
            '/project/dev/api': 'included',
            '/project/dev/testing/env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev/', recursive=False)

            # Check secrets.
            self.assertTrue(len(_secrets) == 2,
                            msg='Two secrets should have been returned')

            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_recursive(self):

        # Setup the data.
        secrets = {
            '/project/env1': 'included',
            '/project/dev/env2': 'included',
            '/project/dev/env3': 'included',
            '/project/dev/text/env4': 'excluded',
            '/project/prod/env4': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev', recursive=True)

            # Check secrets.
            self.assertTrue(len(_secrets) == 3,
                            msg='Three secrets should have been returned')

            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_paged(self):

        # Setup the data.
        secrets = {}
        for _ in range(random.randint(50, 250)):
            secrets['/project/{}'.format(uuid.uuid4())] = 'excluded'
            secrets['/project/dev/{}'.format(uuid.uuid4())] = 'included'
            secrets['/project/test/dev/{}'.format(uuid.uuid4())] = 'excluded'

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev', recursive=False)

            # Check the number returned.
            self.assertEqual(len(secrets) / 3, len(_secrets), msg='An incorrect number of secrets were returned')

            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_paged_recursive(self):

        # Setup the data.
        secrets = {}
        for _ in range(random.randint(50, 250)):
            secrets['/project/{}'.format(uuid.uuid4())] = 'included'
            secrets['/project/dev/{}'.format(uuid.uuid4())] = 'included'
            secrets['/project/test/dev/{}'.format(uuid.uuid4())] = 'excluded'

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('/project/dev', recursive=True)

            # Check the number returned.
            self.assertEqual(len(secrets) / 3 * 2, len(_secrets), msg='An incorrect number of secrets were returned')

            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')


class TestPrefixSecrets(unittest.TestCase):

    def setUp(self):

        super(TestPrefixSecrets, self).setUp()

        # Get the secret store.
        self.store = SecretStore()

    def test_secrets_for_prefix(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'included',
            'project.prod.env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefix('project.dev')

            # Check secrets.
            self.assertTrue(len(_secrets) == 1,
                            msg='Only one secret should have been returned')

            # Check the value.
            self.assertEqual(secrets['project.dev.env'], _secrets['project.dev.env'],
                             msg='An incorrect secret was returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_for_prefix(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'included',
            'project.dev.api': 'included',
            'project.dev.password': 'included',
            'project.prod.env': 'excluded',
            'project.prod.api': 'excluded',
            'project.prod.password': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefix('project.dev')

            # Check secrets.
            self.assertTrue(len(_secrets) == 3,
                            msg='Three secret should have been returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_prefix_processed(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'included',
            'project.prod.env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Exclude all but the last component.
            processor = lambda key: key.split('.')[-1].upper()

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefix('project.dev', key_processor=processor)

            # Check secrets.
            self.assertTrue(len(_secrets) == 1,
                            msg='Only one secret should have been returned')

            # Check the value.
            self.assertEqual(secrets['project.dev.env'], _secrets['ENV'],
                             msg='Prioritized secret was not returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_for_prefix_processed(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'included',
            'project.dev.api': 'included',
            'project.dev.password': 'included',
            'project.prod.env': 'excluded',
            'project.prod.api': 'excluded',
            'project.prod.password': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Exclude all but the last component.
            processor = lambda key: key.split('.')[-1].upper()

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefix('project.dev', key_processor=processor)

            # Check secrets.
            self.assertTrue(len(_secrets) == 3,
                            msg='Three secret should have been returned')

            # Check secrets.
            for key, secret in _secrets.items():

                # Ensure the key has been trimmed.
                self.assertTrue(len(key.split('.')) == 1)

                # Check secret.
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_prefixes(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'included',
            'project.dev.password': 'included',
            'project.prod.password': 'included',
            'project.prod.env': 'included',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefixes(['project.prod', 'project.dev'])

            # Check secrets.
            self.assertTrue(len(_secrets) == 4,
                            msg='An incorrect number of secrets have been returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_prefixes_duplicates(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.api': 'included',
            'project.dev.env': 'included',
            'project.dev.password': 'included',
            'project.prod.env': 'excluded',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Exclude all but the last component.
            processor = lambda key: key.split('.')[-1].upper()

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefixes(['project', 'project.dev'], key_processor=processor)

            # Check secrets.
            self.assertTrue(len(_secrets) == 3,
                            msg='An incorrect number of secrets have been returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_prefixes_duplicates_prioritized(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'excluded',
            'project.dev.password': 'included',
            'project.prod.env': 'included',
            'project.prod.api': 'included',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Exclude all but the last component.
            processor = lambda key: key.split('.')[-1].upper()

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefixes(['project.dev', 'project.prod'], key_processor=processor)

            # Check secrets.
            self.assertTrue(len(_secrets) == 3,
                            msg='An incorrect number of secrets have been returned')

            # Check secrets.
            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_multiple_secrets_paged(self):

        # Setup the data.
        secrets = {}
        for _ in range(random.randint(50, 250)):
            secrets['project.{}'.format(uuid.uuid4())] = 'excluded'
            secrets['project.dev.{}'.format(uuid.uuid4())] = 'included'
            secrets['project.test.dev.{}'.format(uuid.uuid4())] = 'excluded'

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_prefix('project.dev')

            # Check the number returned.
            self.assertEqual(len(secrets) / 3, len(_secrets), msg='An incorrect number of secrets were returned')

            for secret in _secrets:
                self.assertNotEqual(secret, 'excluded', msg='An excluded key was returned')

    def test_secrets_for_prefix_empty(self):

        # Setup the data.
        secrets = {
            'project.env': 'excluded',
            'project.dev.env': 'excluded',
            'project.dev.password': 'included',
            'project.prod.env': 'included',
            'project.prod.api': 'included',
        }

        # Create a mock client.
        mock_client = MockClient(secrets)

        with mock.patch('botocore.client.BaseClient._make_api_call', new=mock_client.make_api_call):

            # Get the secrets.
            _secrets = self.store.get_secrets_for_path('project.test', recursive=False)

            # Check the value.
            self.assertTrue(len(_secrets) == 0, msg='Something was returned when nothing should be returned')