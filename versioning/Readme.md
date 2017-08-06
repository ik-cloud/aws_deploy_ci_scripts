# Versioning-Deploy Related Strategies

## Definition 1

> Shared Services Account create application version
> and configuration version template.
> CI deploys specific version to specific accounts, 
> eg. DEV, SIT, PRE-PROD, PROD

| APP Version   | Template Version  | Account  | Update Timestamp |
|---------------|:-----------------:|---------:|   ---            |
| 3.0.1         | 3.0.0             |   SIT    |   23-Jul-2016    |
| 1.0.4-Release | 1.0.4-Release     |   PROD   |   11-May-2015    |
| 6.11.23       | 9.8.11            |   DEV    |   22-Jul-2017    |

#### Requirements

1. Read CSV file locally.
2. Add app version, template version, Account deployed to and timestamp in right format.
3. If current Account already have an entry, update the entry.
4. Make most recent entry be on top of the list.
6. Name of the file should be the same as application name.
7. Read File from S3 bucket in an account.
8. Write file back to S3 bucket in same account. 