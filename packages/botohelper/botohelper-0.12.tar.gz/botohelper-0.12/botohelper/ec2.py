#!/usr/bin/env python
import sys
import os
import boto3
import time
import vmtools

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *

class Ec2():
    """Class to manipulate aws ec2 resources

    public methods:
    delete_vpc
    delete_instances
    create_vpc
    create_subnet
    create_internet_gateway
    get_vpc_id_from_name
    get_default_route_table_object
    get_default_security_group_object
    create_tag
    create_instance

    instance variables:
    self.aws_profile
    self.aws_region
    self.session
    self.client
    self.ec2
    self.availability_zones_list
    """

    def __init__(self, aws_profile, aws_region):
        """set instance variables, set instance aws connections

        keyword arguments:
        :type aws_profile: string
        :param aws_profile: the profile to use from ~/.aws/credentials to connect to aws
        :type aws_region: string
        :param aws_region: the region to use for the aws connection object (all resources will be created in this region)
        """
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        # aws session
        self.session = boto3.Session(profile_name=self.aws_profile)
        # ec2 aws client
        self.client = self.session.client('ec2', region_name=self.aws_region)
        # aws ec2 object (mainly used for creating and modifying resources)
        self.ec2 = self.session.resource('ec2', region_name=self.aws_region)
        # create a list of available availability zones
        availability_zones_state_dict = self.client.describe_availability_zones()
        self.availability_zones_list = []
        for availability_zone_dict in availability_zones_state_dict['AvailabilityZones']:
            if availability_zone_dict['State'] == 'available':
                self.availability_zones_list.append(availability_zone_dict['ZoneName'])

    def delete_vpc(self, vpc_name):
        """Create a vpc return vpc_id
        keyword arguments:
        :type vpc_name: string
        :param vpc_name: the Name tag for the vpc
        :type cidr_block: string
        :param cidr_block: cidr_block for the new vpc (ex '10.0.1.0/24')
        :type environment: string
        :param environment: the enviroment tag for the vpc
        """
        vpc_id = self.get_vpc_id_from_name(vpc_name=vpc_name)
        vpc_object = self.ec2.Vpc(vpc_id)
        self.delete_instances(instance_object_list=list(vpc_object.instances.all()))
        for sec_group in list(vpc_object.security_groups.all()):
            if sec_group.group_name != 'default':
                sec_group.delete()
        for subnet in list(vpc_object.subnets.all()):
            subnet.delete()
        for internet_gateway in list(vpc_object.internet_gateways.all()):
            internet_gateway.detach_from_vpc(VpcId=vpc_id)
            time.sleep(3)
            internet_gateway.delete()
        time.sleep(3)
        vpc_object.delete()

    def delete_instances(self, instance_object_list):
        """Take list of instance objects and delete all instances and associated stuff
        keyword arguments:
        :type instance_object_list: list
        :param instance_object_list: a list of instance objects (ex instance_object = ec2.Instance('<instance_id>'))
        """
        instance_id_list = [ instance_object.instance_id for instance_object in instance_object_list ]
        # walk through and delete all instances
        for instance_object in instance_object_list:
            # if we have a hostname delete dns entries
            if instance_object.tags:
                for tag_dict in instance_object.tags:
                    if tag_dict['Key'] == 'Name':
                        hostname = tag_dict['Value']
                # get the public dns record for instance
                public_dns_record = self.get_route53_record(fqdn=hostname, record_type='A', zone_group_type='public_zones')
                # if public dns record exists delete it
                if public_dns_record:
                    self.modify_a_record(fqdn=hostname, ip_address=public_dns_record['ResourceRecords'][0]['Value'], action='delete', ttl=public_dns_record['TTL'], zone_group_type='public_zones')
                # get the private dns record for instance
                private_dns_record = self.get_route53_record(fqdn=hostname, record_type='A', zone_group_type='private_zones')
                # if private dns record exists delete it
                if private_dns_record:
                    self.modify_a_record(fqdn=hostname, ip_address=private_dns_record['ResourceRecords'][0]['Value'], action='delete', ttl=private_dns_record['TTL'], zone_group_type='private_zones')
            instance_object.terminate()
        # wait for all instances to be terminated
        while instance_id_list:
            for instance_id in instance_id_list:
                instance_object = self.ec2.Instance(instance_id)
                if instance_object.state['Name'] == 'terminated':
                    instance_id_list.remove(instance_id)
            print('''Waiting for instance(s) to terminate''', end='\r')
            time.sleep(5)


       

    def create_vpc(self, vpc_name, cidr_block, environment):
        """Create a vpc return vpc_id
        keyword arguments:
        :type vpc_name: string
        :param vpc_name: the Name tag for the vpc
        :type cidr_block: string
        :param cidr_block: cidr_block for the new vpc (ex '10.0.1.0/24')
        :type environment: string
        :param environment: the enviroment tag for the vpc
        """
        # create the vpc
        response = self.client.create_vpc( CidrBlock = cidr_block)
        vpc_id = response['Vpc']['VpcId']
        # get the vpc object
        vpc_object = self.ec2.Vpc(vpc_id)
        # create Name tag
        self.create_tag(resource_object=vpc_object, tags_list_of_dict=[{'Key': 'Name', 'Value': vpc_name},])
        # create environment tag
        self.create_tag(resource_object=vpc_object, tags_list_of_dict=[{'Key': 'Environment', 'Value': environment},])
        # create internet gateway
        internet_gateway_name='{}_internet_gateway'.format(vpc_name)
        internet_gateway = self.create_internet_gateway(internet_gateway_name=internet_gateway_name)
        internet_gateway.attach_to_vpc(VpcId=vpc_id)
        # find default route table and name
        default_route_table_name = '{}_default_route_table'.format(vpc_name)
        default_route_table = self.get_default_route_table_object(vpc_object=vpc_object)
        self.create_tag(resource_object=default_route_table, tags_list_of_dict=[{'Key': 'Name', 'Value': default_route_table_name},])
        # find default security group and name
        default_security_group_name = '{}_default_security_group'.format(vpc_name)
        default_security_group = self.get_default_security_group_object(vpc_object=vpc_object)
        self.create_tag(resource_object=default_security_group, tags_list_of_dict=[{'Key': 'Name', 'Value': default_security_group_name},])
        # return dictionary with the new objects
        vpc_object_dict = {'vpc_object': vpc_object, 'internet_gateway': internet_gateway, 'default_route_table': default_route_table, 'default_security_group': default_security_group }
        return vpc_object_dict

    def create_subnet(self, vpc_object, subnet_name, cidr_block, availability_zone):
        """Create a subnet in vpc, return subnet object
        keyword arguments:
        :type vpc_object: boto3 vpc object (ex: <class 'boto3.resources.factory.ec2.Vpc'>)
        :param vpc_object: vpc object
        :type subnet_name: string
        :param subnet_name: name for the new subnet
        :type cidr_block: string
        :param cidr_block: cidr_block for the new subnet, must be within the vpc and not overlapping with another subnet (ex '10.0.1.0/24')
        :type availability_zone: string
        :param availability_zone: the availability_zone for the new subnet
        """
        subnet = vpc_object.create_subnet(CidrBlock=cidr_block, AvailabilityZone=availability_zone)
        # create Name tag
        self.create_tag(resource_object=subnet, tags_list_of_dict=[{'Key': 'Name', 'Value': subnet_name},])
        return subnet

    def create_internet_gateway(self, internet_gateway_name):
        """Create an internet gateway return internet gateway object
        keyword arguments:
        :type internet_gateway_name: string
        :param internet_gateway_name: Name tag for the internet gateway
        """
        internet_gateway = self.ec2.create_internet_gateway()
        # create Name tag
        self.create_tag(resource_object=internet_gateway, tags_list_of_dict=[{'Key': 'Name', 'Value': internet_gateway_name},])
        return internet_gateway

    def get_vpc_id_from_name(self, vpc_name):
        """Take vpc_name and return vpc_id
        keyword arguments:
        :type vpc_name: string
        :param vpc_name: the value of the Name tag for the vpc
        """
        filters = [{'Name':'tag:Name', 'Values':[vpc_name]}]
        # filter all vpcs by our vpc name
        result = list(self.ec2.vpcs.filter(Filters=filters))
        if result:
            vpc = list(self.ec2.vpcs.filter(Filters=filters))[0]
        else:
            vpc_not_found_message = 'Vpc with Name tag: {} not found. Nothing to delete. Quitting...'.format(vpc_name)
            print(vpc_not_found_message)
            sys.exit(0)
        vpc_id = vpc.vpc_id
        return vpc_id

    def get_default_route_table_object(self, vpc_object):
        """Find default route table for vpc_object, return default route table object
        IMPORTANT: only run this before any other route tables have been create (it exprects there to be only one route table)
        keyword arguments:
        :type vpc_object: boto3 vpc object (ex: <class 'boto3.resources.factory.ec2.Vpc'>)
        :param vpc_object: vpc object
        """
        route_tables_collection = vpc_object.route_tables
        route_tables_list = list(route_tables_collection.all())
        # make sure we only have 1 route table in the list
        if len(route_tables_list) != 1:
            exception_message = 'Fail: the method "get_default_route_table_object" found: {} route tables for vpc: {}. Expecting only one'.format(len(route_tables_list), vpc_object.vpc_id) 
            raise ValueError(exception_message)
        return route_tables_list[0]

    def get_default_security_group_object(self, vpc_object):
        """Find default security group for vpc_object, return default security group object
        IMPORTANT: only run this before any other security groups have been create (it exprects there to be only one security group)
        keyword arguments:
        :type vpc_object: boto3 vpc object (ex: <class 'boto3.resources.factory.ec2.Vpc'>)
        :param vpc_object: vpc object
        """
        security_groups_collection = vpc_object.security_groups
        security_groups_list = list(security_groups_collection.all())
        # make sure we only have 1 route table in the list
        if len(security_groups_list) != 1:
            exception_message = 'Fail: the method "get_default_security_group_object" found: {} security groups for vpc: {}. Expecting only one'.format(len(security_groups_list), vpc_object.vpc_id) 
            raise ValueError(exception_message)
        return security_groups_list[0]

    def create_tag(self, resource_object, tags_list_of_dict):
        """Create tags for a resource
        keyword arguments:
        :type resource_object: boto3 resource object (ex: <class 'boto3.resources.factory.ec2.Vpc'>)
        :param resource_object: a object that represents an aws resource, one way to get it is filter a collection ex (ec2.vpcs.filter(VpcIds=[vpc_id]))
        :type tags_list_of_dict: list
        :param tags_list_of_dict: a list of dictionaries. One dict for each tag ex: [{'Key': 'Name', 'Value': 'vpctest'},]
        """
        resource_object.create_tags(Tags=tags_list_of_dict)

    def create_instance(self, instance_name, subnet_id, instance_size='t2.medium', public_ip=False, instance_profile_arn=None):
        """Create instance, return instance object
        keyword arguments:
        :type instance_name: string
        :param instance_name:  the Name tag for the new instance
        :type subnet_id: string
        :param subnet_id:  the subnet in which to launch the instance
        :type instance_size: string
        :param instance_size: the size of the instance
        :type public_ip: boolean
        :param public_ip: should instance have a public ip? True of False
        :type instance_profile_arn: string
        :param instance_profile_arn: (optional) the arn of the instance profile to use
        """
        # get environment_dict
        environment_dict = self.get_subnet_environment_dict(subnet_id=subnet_id)
        # get ami_id
        ami_id = self.get_latest_ami().image_id
        # launch instance
        if instance_profile_arn:
            instances_list = self.ec2.create_instances( ImageId=ami_id, MinCount=1, MaxCount=1, KeyName=environment_dict['keypair_name'], InstanceType=instance_size, NetworkInterfaces=[ {'DeviceIndex': 0, 'SubnetId': subnet_id, 'AssociatePublicIpAddress': public_ip} ], IamInstanceProfile={ 'Arn': instance_profile_arn })
        else:
            instances_list = self.ec2.create_instances( ImageId=ami_id, MinCount=1, MaxCount=1, KeyName=environment_dict['keypair_name'], InstanceType=instance_size, NetworkInterfaces=[ {'DeviceIndex': 0, 'SubnetId': subnet_id, 'AssociatePublicIpAddress': public_ip} ])
        instance_object = instances_list[0]
        # create Namte tag
        self.create_tag(resource_object=instance_object, tags_list_of_dict=[{'Key': 'Name', 'Value': instance_name},])
        return instance_object
