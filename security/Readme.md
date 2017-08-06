# Cloud Security - Amazon Web Services


### Substitute Secret Example
1. Application Configuration file  `*.json` format
```json
    [
      {     
       "Value": "{{bucket:key:placeholder}}"
      }
    ]
```
2. S3 Bucket with policy where CI is a principal
```aws s3
  ${BUCKET}:${ENV}:${KEY}
```
3. File on S3 bucket may have following format
```json
  {
   "placeholder" : "value"
  } 
```
4. [AWS KMS](https://aws.amazon.com/kms/) can be set.  
5. Execute script
```bash
  scripts/substitue.sh
```
6. AWS UI and CLI access should be disabled for USERS/GROUPS with insufficient
 priviledges.
