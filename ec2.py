import csv
import boto3

"""
A tool for retrieving basic information from the running EC2 instances.
"""

# Connect to EC2
session = boto3.Session(profile_name="hc-prod")
ec2 = session.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = list()
for instance in running_instances:
    ec2info.append({
        'Instance Id': instance.id,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time,
        'Tags': instance.tags
        })


header = ['Instance Id', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time', 'Tags']
with open('ec2-details.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(ec2info)
