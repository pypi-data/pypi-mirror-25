#!/usr/bin/env python
import sys
import os
import datetime
import boto3
import time
import vmtools

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *

class Iam():
    """Class to manipulate aws iam resources

    public methods:

    instance variables:
    self.aws_profile
    self.aws_region
    self.session
    self.iam
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
        # aws iam object (mainly used for creating and modifying iam user, groups, etc)
        self.iam = self.session.resource('iam', region_name=self.aws_region)

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
