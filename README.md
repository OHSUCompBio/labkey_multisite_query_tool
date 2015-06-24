## LabKey Multisite Query Tool ##


Commandline tool for querying across mutltiple LabKey instances.

* Free software: BSD license
* Documentation: https://labkey_multisite_query_tool.readthedocs.org.


### Example .labkey.yml configuration file ###

```yaml
  default:
  
      schema: lists
  
      aliases:
          fastq_forward: fastq_forward_ccc_did
          fastq_forward: fastq_forward_ccc_did
          fastq_reverse: fastq_reverse_ccc_did
          specific_diagnosis: diagnosis
          specimen_id/disease_state: disease_state
          specimen_id/donor_age_at_diagnosis: donor_age
          specimen_id/donor_gender: donor_gender
          specimen_id/specimen_type: specimen_type
  
      columns:
        - diagnosis
        - disease_state
        - donor_age
        - donor_gender
        - fastq_forward_ccc_did
        - fastq_reverse_ccc_did
        - specimen_type
  
  
  servers:
  
    - host: http://localhost:9004/labkey/
      email: foo@bar.com
      password: foobar
      project: ccc
      query_name: genome_data
      custom_columns:
        site_name:  Austin
  
    - host: http://localhost:9004/labkey/
      email: foo@bar.com
      password: foobar
      project: ccc
      query_name: genome_data
      custom_columns:
        site_name:  Boston

```
