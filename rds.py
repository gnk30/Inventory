import csv
import boto3

"""
A tool for retrieving basic information of different RDS Engines.
"""

# Connect to RDS
session = boto3.Session(profile_name="hc-prod")
rds = session.client('rds')

# Get information for all running instances
response = rds.describe_db_instances(
    Filters = [{
        "Name" : "engine",
        "Values" : ["docdb"]
    }]
)

rdsinfo = list()
for instance in response['DBInstances']:
    tags = rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn']).get('TagList')
    rdsinfo.append({
        'Name': instance['DBInstanceIdentifier'],
        'Class': instance['DBInstanceClass'],
        'Status': instance['DBInstanceStatus'],
        'Engine': instance['Engine'],
        'EngineVersion': instance['EngineVersion'],
        'Endpoint': instance['Endpoint']['Address'],
        'Tags': tags
        })

header = ['Name', 'Class', 'Status', 'Engine', 'EngineVersion', 'Endpoint', 'Tags']
with open('docdb-details.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(rdsinfo)

