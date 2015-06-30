# -*- coding: utf-8 -*-
from urlparse import urljoin
import os
import string

import pandas as pd
import requests
import yaml

# Use compatibility mode. This is needed when renaming columns.
from pandas import compat
compat.PY3 = True

class LabKey(object):

    @classmethod
    def from_yaml_file(cls, config_file_path):
        """Return a collection of LabKey instances from a YAML file.

        Args:

            config_file_path (str): Path to a YAML config files.
        """

        # Expand environment variables.
        config_file_path = os.path.expandvars(config_file_path)

        # Read our config file.
        with open(config_file_path, 'r') as config_file:
            config = yaml.load(config_file)

        default_config = config.get('default', {})

        labkey_instances = []

        for server in config['servers']:

            # Combine our default config with our server config.
            config = default_config.copy()
            config.update(server)

            # Allow use to pass in environment variables to email/password
            config.update(
                email=string.Template(config['email']).substitute(os.environ),
                password=string.Template(config['password']).substitute(os.environ)
            )

            labkey = LabKey(
                host=config['host'],
                email=config['email'],
                password=config['password'],
                project=config['project'],
                schema=config['schema'],
                query_name=config['query_name'],
                columns=config['columns'],
                aliases=config.get('aliases', {}),
                custom_columns=config.get('custom_columns', []),
                column_order=config.get('column_order', [])
            )

            labkey_instances.append(labkey)

        return labkey_instances


    def __init__(self,
                 host=None,
                 email=None,
                 password=None,
                 project=None,
                 schema=None,
                 query_name=None,
                 columns=None,
                 aliases=None,
                 custom_columns=None,
                 column_order=None):
        """Initialize an instance of a LabKey server connection.

        Args:

            host (str): LabKey host
            email (str): User login
            password (str): User password
            project (str): LabKey Project name
            schema (str): LabKey schema used for query_name (Example: 'lists')
            query_name (str): LabKey resource to query
            columns (list): Table columns to return
            aliases (dict): Column alises used for filtering and output
            custom_columns (dict): Custom columns to add to output.
                (Example: {'site': 'Boston'})
        """

        if columns is None:
            columns = []

        if aliases is None:
            aliases = {}

        if custom_columns is None:
            custom_columns = {}

        if column_order is None:
            column_order = []

        self.host = host
        self.email = email
        self.password = password
        self.project = project
        self.schema = schema
        self.query_name = query_name
        self.columns = columns
        self.aliases = aliases
        self.custom_columns = custom_columns
        self.column_order = column_order

        # Create a session object for this LabKey instance.
        self.session = requests.Session()


    def query(self, filters=None, aliases=None):
        """Query a Labkey instance using a collection of filters.

        Args:

            filters (dict): A hash of LabKey-compliant filters.

            aliases (dict): A dict containing column mapping names.

        Examples:

            >>> filters = {
                    "specimen_id/donor_sex~eq": "Male",
                    "specimen_id/donor_age_at_diagnosis~lte": 40
                    }
            >>> df = labkey.query(filters)
        """

        if filters is None:
            filters = {}

        if aliases is None:
            aliases = {}

        query_url = self.url("query/{0}/selectRows.api".format(self.project))

        # We need to reverse our alias map.
        reverse_aliases = {value: key for key, value in self.aliases.iteritems()}

        # Note that we have to take the column specified by the user (i.e.,
        # "gender" and map it to the original column name (i.e.,
        # "specimen_id/donor_sex").
        columns = [reverse_aliases.get(column, column) for column in self.columns]

        params = {
            "schemaName": self.schema,
            "query.queryName": self.query_name,
            "query.columns": ','.join(columns)
        }

        # Iterate through the filters and prepend 'query.' to each key. Note
        # that we use the reversed_alias so that when a user queries on something
        # like 'gender', we will use the actual column name 'speciman_id/donor_sex'.
        filter_params = {}

        for key, value in filters.iteritems():

            column, operator = key.split("~")

            labkey_column = reverse_aliases.get(column, column)

            expression = "query.{0}~{1}".format(labkey_column, operator)

            filter_params[expression] = value

        # Add our default options to our query params
        params.update(filter_params)

        response = self.session.get(query_url, params=params)

        # If we got an error code, raise an exception.
        response.raise_for_status()

        # Parse the response as JSON.
        response_data = response.json()

        rows = response_data["rows"]

        # Delete rows from our response and use the rest of the response as metadata.
        del response_data["rows"]
        metadata = response_data

        # Read our rows into a Pandas data frame.
        data_frame = pd.DataFrame.from_dict(rows)

        # Attach our metadata to the data frame
        data_frame._metadata = metadata

        # Rename our columns
        data_frame.rename(columns=self.aliases, inplace=True)

        # Add our custom columns.
        for key, value in self.custom_columns.iteritems():
            data_frame[key] = value

        # Re-order columns. We treat columns in "column_order" as "priority
        # columns" and the others as "remaining columns".

        priority_columns = self.column_order

        remaining_columns = [column for column in self.columns if column in
                             data_frame.columns and column not in priority_columns]

        data_frame = data_frame[priority_columns + remaining_columns]

        return data_frame


    def login(self, email=None, password=None):
        """Logs into a LabKey instance. Persists JSESSIONID cookie in session.

        Args:

            email (str): User e-mail.
            password (str): User passowrd.

        Examples:

            >>> labkey.login(email="foo@bar.com", password="foobar")
        """

        if email is None:
            email = self.email

        if password is None:
            password = self.password

        login_url = self.url('login/login.post')

        payload = {
            "email": email,
            "password": password
        }

        response = self.session.post(login_url, data=payload)

        # If we got an error code, raise an exception.
        response.raise_for_status()

        # Verify that we received JSESSIONID within our response.
        if not "JSESSIONID" in self.session.cookies:
            raise RuntimeError("Unable to authenticate.")


    def url(self, relative_url):
        """Create a url using a relative path and the host url.

        Args:

            relative_url (str): Relative URL.

        Examples:

            >>> labkey = LabKey(host="http://localhost:9004/labkey/")
            >>> labkey.url('login/login.post')
            "http://localhost:9004/labkey/login/login.post"
        """
        return urljoin(self.host, relative_url)
