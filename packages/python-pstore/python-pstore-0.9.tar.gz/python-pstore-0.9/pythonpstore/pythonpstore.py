import boto3
from botocore.errorfactory import ClientError
import json
from os.path import normpath, basename, dirname


class SecretStore:
    """
    This class facilitates collection of secrets from AWS parameter store.
    """

    def __init__(self, profile=None, region='us-east-1', json_values=False):

        # Check for a profile.
        if profile is not None:

            session = boto3.Session(profile_name=profile)
            self.ssm = session.client('ssm', region_name=region)

        else:

            # Use the default.
            self.ssm = boto3.client('ssm', region_name=region)

        # Retain whether JSON encoded secrets are being used.
        self.json_values = json_values

    def get_secrets_for_path(self, path, recursive=False):
        """
        Fetches all secrets from AWS Parameter Store for the given path. Collects all secrets at each parent
        path if all_levels is true. Secrets in deeper paths take priority and will overwrite secrets with matching
        keys in a path higher up.
        :param path: The path where secrets should be fetched.
        :type path: String
        :param recursive: Whether secrets at parent paths should be collected as well as the destination path.
        :type recursive: Boolean
        :return: A dict with each secret's key value pair. The key does not include the path, only the
        top-level key.
        :rtype: {'<secret_key>': '<secret_value>'...}
        """
        # Trim trailing slash.
        path = path.rstrip('/')

        # Get all paths.
        paths = SecretStore._recurse_paths(path) if recursive else [path]

        # Store secrets.
        secrets = {}
        for path in paths:
            # Get the keys.
            keys = self._get_keys_for_path(path)
            if len(keys) > 0:

                # Set to only return the last path component for each key.
                processor = lambda key: basename(normpath(key)).upper()

                # Get the secrets.
                for secret in self._get_secrets_for_keys_batch(keys, key_processor=processor):

                    # Add it.
                    secrets[secret['key']] = secret['value']

        return secrets

    def get_secrets_for_paths(self, paths, recursive=False):
        """
        Fetches all secrets from AWS Parameter Store for the given paths. Collects all secrets at each parent
        path if all_levels is true. Secrets in deeper paths take priority and will overwrite secrets with matching
        keys in a path higher up. Secrets are fetched for for each path in the order they are passed so the list
        of paths given dictate priority with the first path having lowest priority and the last path having highest
        priority (priority simply means if duplicate keys are found, the highest priority path's secret will be the
        one returned).
        :param paths: The list of paths where secrets should be fetched, prioritizing paths at the end of the list.
        :type path: String
        :param recursive: Whether secrets at parent paths should be collected as well as the destination path.
        :type recursive: Boolean
        :return: A dict with each secret's key value pair. The key does not include the path, only the
        top-level key.
        :rtype: {'<secret_key>': '<secret_value>'...}
        """
        # Iterate through paths.
        secrets = {}
        for path in paths:

            # Get the secrets.
            _secrets = self.get_secrets_for_path(path, recursive)

            # Update them.
            secrets.update(_secrets)

        return secrets

    def get_secrets_for_prefix(self, prefix, key_processor=lambda key: key):
        """
        Fetches all secrets from AWS Parameter Store for the given prefix. Collects all secrets with keys
        that match the passed prefix.
        :param prefix: The prefix with which to filter keys.
        :type prefix: String
        :param key_processor: A lambda express with which to process each secret's key. By default the entire key,
        including prefix, is returned.
        :type key_processor: lambda
        :return: A dict with each secret's key value pair.
        :rtype: {'<secret_key>': '<secret_value>'...}
        """
        # Get the keys.
        keys = self._get_keys_for_prefix(prefix)
        if len(keys) > 0:

            # Get the secrets.
            secrets = {}
            for secret in self._get_secrets_for_keys_batch(keys, key_processor=key_processor):

                # Add it.
                secrets[secret['key']] = secret['value']

            return secrets

        return {}

    def get_secrets_for_prefixes(self, prefixes, key_processor=lambda key: key):
        """
        Fetches all secrets from AWS Parameter Store for the given list of prefixes. Collects all secrets with keys
        that match the passed prefix. If keys are processed such that duplicates are possible, Secrets are fetched
        for each prefix in the order they are passed so the list of prefixes given dictate priority with the first
        prefix having lowest priority and the last prefix having highest priority (priority simply means if duplicate
        keys are found, the highest priority prefix's secret will be the one returned). By default, all keys should
        be unique and no prioritization or overwriting is needed.
        :param prefixes: The prefixes by which to filter keys.
        :type prefixes: [String]
        :param key_processor: A lambda express with which to process each secret's key. By default the entire key,
        including prefix, is returned.
        :type key_processor: lambda
        :return: A dict with each secret's key value pair.
        :rtype: {'<secret_key>': '<secret_value>'...}
        """
        # Iterate through the passed prefixes.
        secrets = {}
        for prefix in prefixes:

            # Get the secrets.
            _secrets = self.get_secrets_for_prefix(prefix, key_processor=key_processor)

            # Add them.
            secrets.update(_secrets)

        return secrets

    def get_secret_for_key(self, name):
        """
        Fetches the secret from AWS Parameter Store for the given key.
        :param name: The prefix with which to filter keys.
        :type name: String
        :return: The secret's value
        :rtype: String
        """
        try:

            param = self.ssm.get_parameter(
                Name=name,
                WithDecryption=True,
            )

            return self._decode_json_secret(param['Parameter']['Value']) if self.json_values \
                else param['Parameter']['Value']

        except ClientError as e:
            print('Parameter not found: {}'.format(e))

            return None

    def _get_keys_for_path(self, path):
        """
        Fetch all keys in parameter store for the given path. If recursive, fetch keys for all
        parent paths as well.
        :param path: The path to search
        :type path: String
        :param recursive: Get keys in all parent paths
        :type recursive: Boolean
        :return: A list of all keys for the given path.
        :rtype: [String]
        """

        # Make the parameter filters.
        filters = [{
            'Key': 'Path',
            'Option': 'OneLevel',
            'Values': [
                path,
            ],
        }]

        # Get 'em all.
        keys = self._get_keys_for_parameter_filters(filters)

        return keys

    def _get_keys_for_prefix(self, prefix):
        """
        Fetch all keys in parameter store for the given prefix. Any key starting with the passed prefix
        is returned.
        :param path: The prefix to search
        :type path: String
        :return: A list of all keys for the given path.
        :rtype: [String]
        """

        # Make the parameter filters.
        filters = [{
            'Key': 'Name',
            'Option': 'BeginsWith',
            'Values': [
                prefix,
            ],
        }]

        # Get 'em all.
        keys = self._get_keys_for_parameter_filters(filters)

        return keys

    def _get_keys_for_parameter_filters(self, filters):
        """
        Accepts a list of parameter filters and fetches all matching keys from AWS parameter
        store. Handles AWS' limit of 50 returned keys by iterating until all have been fetched.
        :param filters: A list of dict describing an AWS parameter filter.
        :type filters: [Dict]
        :return: All keys matching the passed parameter filters.
        :rtype: [String]
        """

        try:
            # Loop while more exist.
            keys = []
            token = None
            while True:

                # Form the request.
                parameters = {
                    'ParameterFilters': filters,
                    'MaxResults': 50
                }

                # Set the token if necessary.
                if token is not None:
                    parameters['NextToken'] = token

                # Make the request.
                response = self.ssm.describe_parameters(**parameters)

                # Slice out the keys and collect them.
                keys.extend([key['Name'] for key in response['Parameters']])

                # Check for the next token.
                token = response.get('NextToken', None)
                if token is None:
                    break

            return keys

        except ClientError as e:
            print('Describing parameter failed: {}'.format(e))

        return None

    def _get_secrets_for_keys_individually(self, keys=[], key_processor=None):
        """
        Accepts a list of keys and fetches all respective secrets from AWS Parameter Store. This method
        fetches each secret individually as opposed to all at once.
        :param keys: The keys of the secrets to be fetched.
        :type keys: [String]
        :return: A list of dict containing each secret's key and each secret's value.
        :rtype: [{'key': <key>, 'value': <value>}]
        """

        # Check for no keys.
        if len(keys) == 0:
            return None

        try:
            # Iterate through them individually.
            secrets = []
            for key in keys:

                # Build the request.
                param = self.ssm.get_parameter(
                    Name=key,
                    WithDecryption=True
                )

                # Check how to process the key.
                key = param['Name']
                if key_processor:
                    key = key_processor(key)

                # Parse the response.
                value = self._decode_json_secret(param['Parameter']['Value']) \
                    if self.json_values else param['Parameter']['Value']

                secrets.append({'key': key, 'value': value})

            return secrets

        except ClientError as e:
            print('Parameters not found: {}'.format(e))

        return None

    def _get_secrets_for_keys_batch(self, keys=[], key_processor=None):
        """
        Accepts a list of keys and fetches all respective secrets from AWS Parameter Store. This method
        fetches secrets in batches of ten at a time (due to AWS limit).
        :param keys: The keys of the secrets to be fetched.
        :type keys: [String]
        :return: A list of dict containing each secret's key and each secret's value.
        :rtype: [{'key': <key>, 'value': <value>}]
        """

        # Check for no keys.
        if len(keys) == 0:
            return None

        try:
            # Store fetched secrets.
            secrets = []

            # Iterate while keys still exist.
            while len(keys) > 0:

                # Build the request to fetch the last 10 (or fewer) items.
                response = self.ssm.get_parameters(
                    Names=keys[-10:],
                    WithDecryption=True,
                )

                # Simplify the response.
                for param in response['Parameters']:

                    # Check how to process the key.
                    key = param['Name']
                    if key_processor:
                        key = key_processor(key)

                    # Get the value.
                    value = self._decode_json_secret(param['Value']) if self.json_values else param['Value']

                    secrets.append({'key': key, 'value': value})

                # Remove the fetched items.
                del keys[-10:]

            return secrets

        except ClientError as e:
            print('Parameters not found: {}'.format(e))

        return None

    @staticmethod
    def _recurse_paths(path):
        """
        Takes a path and returns a list of all parent paths, sorted from top-most level to
        the passed path at the end of the list.
        :param path: Secrets path, must begin with '/'
        :type path: String
        :return: A list of all paths
        :rtype: [String]
        """

        # Trim trailing slash if any.
        path = path.rstrip('/')

        # Collect all paths to check. Keep in order of path to ensure
        # secrets in deeper paths override those before them.
        paths = [path]
        while dirname(path) != '/':
            path = dirname(path)
            paths.insert(0, path)

        return paths

    @staticmethod
    def _decode_json_secret(value):
        """
        Decodes the passed json into a native type.
        :param value: The JSON value.
        :type value: String
        :return: The object type parsed from JSON.
        :rtype: String, Integer, Dict, List, Anything!
        """
        try:
            json_value = json.loads(value)
            return json_value
        except json.JSONDecodeError:
            return value
