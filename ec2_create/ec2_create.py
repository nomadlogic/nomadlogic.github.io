#!/usr/bin/env python2.7
from boto3 import resource, client
import json
from pprint import pprint
"""
ec2_create.py: Deploy and configure EC2 resources
               using python2.7 and boto3. Config
               is driven by json documents.
"""

ec2_resource = resource('ec2')
tag_client = client('ec2')
r53_client = client('route53')

# Read in configuration data via defined JSON document
ec2dat = json.loads(open('ec2_config.json').read())

def create_ec2_instance():
    """
    Instantiate EC2 instance based on JSON configuration
    parameters and return instance_id for additional use
    """
    instance = ec2_resource.create_instances(
        InstanceType = ec2dat[0]['instance_type'],
        MinCount = 1,
        MaxCount = 1,
        ImageId = ec2dat[0]['image_id'],
        KeyName = ec2dat[0]['key_name'],
        SecurityGroupIds = [ec2dat[0]['security_groups']],
        SubnetId = ec2dat[0]['subnet_id'],
        BlockDeviceMappings = [
            {
                'DeviceName': ec2dat[0]['ebs_vol_dev'],
                'Ebs': {
                    'VolumeSize': int(ec2dat[0]['ebs_vol_size']),
                    'VolumeType': ec2dat[0]['ebs_vol_type'],
                },
            },
        ],
        UserData = ec2dat[0]['user_dat']
    )
    #pprint(instance)
    instance_id = instance[0].id
    return instance_id

def tag_ec2_instance(instance_id):
    """
    Tag a given instance using JSON configuration data
    """
    tag_info = tag_client.create_tags(
        Resources = [instance_id],
        Tags = [
            {
                'Key': 'Name',
                'Value': ec2dat[0]['tag_name']
            },
            {
                'Key': 'env',
                'Value': ec2dat[0]['tag_env']
            },
            {
                'Key': 'hostname',
                'Value': ec2dat[0]['tag_name'] + "." + ec2dat[0]['tag_subdomain']
            },
            {
                'Key': 'subdomain',
                'Value': ec2dat[0]['tag_subdomain']
            },
            {
                'Key': 'vpc',
                'Value': ec2dat[0]['tag_vpc']
            },
        ]
    )
    #pprint(tag_info)

def get_priv_ipaddr(instance_id):
    """
    Return private IP address for a given ec2 instance
    """
    instance_info = ec2_resource.Instance(instance_id)
    pri_ip = instance_info.network_interfaces_attribute[0]['PrivateIpAddress']
    return pri_ip

def r53_register(instance_id, pri_ip):
    """
    Register new instance in iad.tribdev.com subdomain
    using primary private interface and name JSON object
    """
    r53_info = r53_client.change_resource_record_sets(
        # ZoneId is iad.tribdev.com
        HostedZoneId = 'XXXXXXXXXXXXXX',
        ChangeBatch = {
            'Comment': 'Test DNS ENtry',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        # Name needs to be set to the FQDN
                        'Name': ec2dat[0]['tag_name'] + "." + ec2dat[0]['tag_subdomain'],
                        'Type': 'A',
                        #'Region': 'us-east-1',
                        'TTL': 300,
                        'ResourceRecords': [ { 'Value': pri_ip }, ],
                    }
                }
            ]
        }
    )

def main():
    # Create instance and store it's instance-id
    instance_id = create_ec2_instance()
    # Apply custom tags to instance
    tag_ec2_instance(instance_id)
    # Determine the private IP addr of newly created instance
    pri_ip = get_priv_ipaddr(instance_id)
    # Register new instance in Route53
    r53_register(instance_id, pri_ip)

    print "Your system is now available at the following location:"
    print ec2dat[0]['tag_name'] + "." + ec2dat[0]['tag_subdomain']
    print pri_ip

if __name__ == "__main__":
    main()
