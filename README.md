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

        # The default block contains properties used for all servers.
        default:

          # LabKey credentials. Note that we can use environmental variables
          # here that can be parsed.
          email: $LABKEY_EMAIL
          password: $LABKEY_PASSWORD

          # LabKey project information
          project: ccc
          schema: lists
          query_name: genome_data

          # Column aliases for filtering and for output rendering. Listed
          # as <column in LabKey>: <column alias>
          aliases:
            fastq_forward: fastq_forward_ccc_did
            fastq_forward: fastq_forward_ccc_did
            fastq_reverse: fastq_reverse_ccc_did
            specific_diagnosis: diagnosis
            specimen_id/disease_state: disease_state
            specimen_id/donor_age_at_diagnosis: donor_age
            specimen_id/donor_gender: donor_gender
            specimen_id/specimen_type: specimen_type

          # Columns to return. Note that we can use aliases here.
          columns:
            - diagnosis
            - disease_state
            - donor_age
            - donor_gender
            - fastq_forward_ccc_did
            - fastq_reverse_ccc_did
            - specimen_type

          # We can specify column order. The columns below are listed first
          # while the other columns (specified in the "columns" property) are
          # listed in their corresponding order.
          column_order:
            - site_name


        servers:

          - host: http://localhost:9004/labkey/
            custom_columns:
              site_name:  Austin
      
          - host: http://localhost:9004/labkey/
            custom_columns:
              site_name:  Boston
```
