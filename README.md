## LabKey Multisite Query Tool ##

Command-line tool for querying across mutltiple LabKey instances.

### Installing ###

Until a release on PyPi, you can install this tool with:

```
pip install git+git://github.com/OHSUCompBio/labkey_multisite_query_tool
```

After that's done, you should be able to view the tool documentation with
`labkey --help`.

### Overview ###

This library provides an executable that allows you to query across multiple
LabKey instances. Running `labkey --help` provides you everything you need to
know:

```
› labkey --help
LabKey Multisite Query Tool.

Usage:
  labkey [--config-file=<file.yml>] [--output-format=<format>] [<filters>...]


Options:
  -h --help                      Show this screen.
  --config-file=<file.yml>       Specify the path to a YAML file containing
                                 configuration information for LabKey instances.
                                 [default: $HOME/.labkey.yml]
  --output-format=<format>       Output format that is rendered in standard out.
                                 [default: json]
  --version                      Show version.


Supported Formats:

    json, tsv, csv, html


About Filters:

    Filters should be provided as they would be passed into LabKey. Please make
    sure to wrap each argument in quotes. Filtered column names should use the
    aliased column names that are listed in the configuration file.

    Examples:

        # Using $HOME/.labkey.yml
        $ labkey gender~eq=Male donor_age~gte=40 > results.json

        # Using a custom .labkey.yml file
        $ labkey --config-file=/path/to/.labkey.yml gender~eq=Male donor_age~gte=40

        # Rendering an HTML output of results
        $ labkey --output-format=html gender~eq=Male donor_age~gte=40 > results.html


Example Configuration:

    Server configuration is done via a YAML file with a default location of
    $HOME/.labkey.yml. You can also provide your own custom path if need be.
    Note that for each server configuration, options from "default" are merged
    into that server configuration.

    Example .labkey.yml:

        default:

          schema: lists

          aliases:
            specimen_id/donor_sex: gender
            specimen_id/donor_age_at_diagnosis: donor_age

          columns:
            - CCC_DID
            - pair_id
            - pair_direction
            - dataset_collection_name

        servers:

          - host: 'http://host1.server.com:9005/labkey'
            email: 'foo@bar.com'
            password: 'foobar'
            project: 'my_project'
            custom_columns:
              site_name: Boston

          - host: 'http://host2.server.com:8005/labkey'
            email: 'foo@bar.com'
            password: 'foobar'
            project: 'my_other_project'
            aliases:
              specimen_id/donor_age: donor_age
            custom_columns:
              site_name: Austin
```
