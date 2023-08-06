#!/usr/bin/env python
import os, json, urlparse, boto3, subprocess, shutil, jmespath, sys, time, imp
import datetime as dt
from botocore.exceptions import ClientError
from sets import Set
from yac.lib.file import FileError, file_in_registry, get_file_contents, localize_file, get_dump_path
from yac.lib.file import FileError, file_in_registry, get_file_contents, localize_file, get_dump_path
from yac.lib.file import dump_file_contents
from yac.lib.template import apply_templates_in_file, apply_templates_in_dir
from yac.lib.paths import get_config_path
from yac.lib.intrinsic import apply_fxn
from yac.lib.variables import get_variable, set_variable
from yac.lib.naming import get_stack_name
from yac.lib.file import get_localized_script_path

UPDATING = "Updating"
BUILDING = "Building"

STACK_STATES = ['CREATE_IN_PROGRESS','CREATE_FAILED','CREATE_COMPLETE','ROLLBACK_IN_PROGRESS',
                'ROLLBACK_FAILED','ROLLBACK_COMPLETE','DELETE_IN_PROGRESS','DELETE_FAILED',
                'DELETE_COMPLETE','UPDATE_IN_PROGRESS','UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                'UPDATE_COMPLETE','UPDATE_ROLLBACK_IN_PROGRESS','UPDATE_ROLLBACK_FAILED',
                'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS','UPDATE_ROLLBACK_COMPLETE']


CREATE_IN_PROGRESS_STATE = 'CREATE_IN_PROGRESS'
NEWLY_CREATED_STATE = 'CREATE_COMPLETE'

UPDATABLE_STATES = ['CREATE_COMPLETE','UPDATE_COMPLETE']

UNKNOWN_STATE = "unknown"

NON_EXISTANT = "non-existant"


NEWLY_CREATED_STATE = 'CREATE_COMPLETE'

UPDATE_COMPLETE_STATE = 'UPDATE_COMPLETE'
UPDATE_COMPLETE_STATES = ['UPDATE_COMPLETE','UPDATE_ROLLBACK_COMPLETE']

UPDATE_IN_PROGRESS_STATE = 'UPDATE_IN_PROGRESS'

UPDATABLE_STATES = ['CREATE_COMPLETE','UPDATE_COMPLETE','UPDATE_ROLLBACK_COMPLETE']

UNKNOWN_STATE = "unknown"

MAX_TEMPLATE_LEN = 51200

# determine cost of a new stack
def cost_stack( template_string="", stack_params = None , template_staging_path = None):

    cost_response = ""
    cost_error = ""

    client = boto3.client('cloudformation')

    try:

        if (len(template_string) > MAX_TEMPLATE_LEN and
            template_staging_path):

            # upload the template to the s3 location specified
            template_url = upload_template_to_s3(template_string, template_staging_path)

            response = client.estimate_template_cost(TemplateURL = template_url,
                                                     Parameters = stack_params)

            cost_response = str(response['Url'])

        elif (len(template_string) > MAX_TEMPLATE_LEN and
            not template_staging_path):

            cost_error =  ("Cost can't be calculated because the template string exceeds Amazon's character limit." +
                   "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter.")

        else:
            response = client.estimate_template_cost(TemplateBody=template_string,
                                                     Parameters = stack_params)

            cost_response = str(response['Url'])

    except ClientError as e:
        
        cost_error = 'Stack costing failed: %s'%str(e)

    return cost_response, cost_error

def create_stack( stack_name , 
                  template_string="", 
                  stack_params = [],
                  template_staging_path = None,
                  stack_tags = []):

    create_response = ""
    create_error = ""

    client = boto3.client('cloudformation')

    try:

        if (len(template_string) > MAX_TEMPLATE_LEN and
            template_staging_path):

            # upload the template to the s3 location specified
            template_url = upload_template_to_s3(template_string, template_staging_path)

            response = client.create_stack(StackName=stack_name,
                                         TemplateURL=template_url,
                                         Parameters = stack_params,
                                         Tags=stack_tags,
                                         Capabilities=['CAPABILITY_IAM'])

            create_response = str(response['StackId'])

        elif (len(template_string) > MAX_TEMPLATE_LEN and
            not template_staging_path):

            create_error =  ("Cost can't be calculated because the template string exceeds Amazon's character limit." +
                   "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter.")

        else:
            response = client.create_stack(StackName=stack_name,
                                         TemplateBody=template_string,
                                         Parameters = stack_params,
                                         Tags=stack_tags,
                                         Capabilities=['CAPABILITY_IAM'])

            create_response = str(response['StackId'])

    except ClientError as e:
        
        create_error = 'Stack creation failed: %s'%str(e)

    return create_response, create_error

def update_stack( stack_name , 
                  template_string="", 
                  stack_params = [],
                  stack_tags = []):

    update_response = ""
    update_error = ""

    client = boto3.client('cloudformation')

    try:

        if (len(template_string) > MAX_TEMPLATE_LEN and
            template_staging_path):

            # upload the template to the s3 location specified
            template_url = upload_template_to_s3(template_string, template_staging_path)

            response = client.update_stack(StackName=stack_name,
                                           TemplateURL=template_url,
                                           Parameters = stack_params,
                                           Capabilities=['CAPABILITY_IAM'])

            update_response = str(response['StackId'])

        elif (len(template_string) > MAX_TEMPLATE_LEN and
            not template_staging_path):

            create_error =  ("Cost can't be calculated because the template string exceeds Amazon's character limit." +
                   "\nTo resolve, specify an S3 path to stage the template using the 'template-staging-s3-path' parameter.")

        else:
            response = client.update_stack(StackName=stack_name,
                                           TemplateBody=template_string,
                                           Parameters = stack_params,
                                           Capabilities=['CAPABILITY_IAM'])

            update_response = str(response['StackId'])

    except ClientError as e:
    
        # we care about all errors exept those resulting from a no-op update    
        if "No updates are to be performed" not in str(e):
            update_error = 'Stack creation failed: %s'%str(e)

    return update_response, update_error
      

def upload_template_to_s3(template_string, template_staging_path):

    # dump the file to a tmp location
    file_path = dump_file_contents(template_string, 'staging', "cf.json")
    
    # copy the file to s3
    cp_file_to_s3( file_path, "s3://%s"%template_staging_path)

    return "https://s3.amazonaws.com/%s"%template_staging_path

def get_stack_state( stack_name ):

    client = boto3.client('cloudformation')

    if stack_exists( stack_name ):

        response = client.describe_stacks(StackName=stack_name)

        states = jmespath.search("Stacks[*].StackStatus",response)

        if len(states) == 1:
            state = states[0]
        else:
            state = UNKNOWN

    else:
        state = NON_EXISTANT

    return state 

def get_stack_templates(service_descriptor, service_parameters):

    service_template = {}

    # get the template from the service_descriptor
    if 'stack-template' in service_descriptor:

        # get the template from the descriptor
        service_template_with_refs = service_descriptor['stack-template']

        # render intrinsics
        service_template = apply_fxn(service_template_with_refs, service_parameters)

    return service_template  

# returns stack template as a dictionary.
# render any yac intrinsics present in the dictionary
def get_stackdef_from_file(template_path, service_parmeters={}):

    stack_definitions = {}

    stack_defs_str = get_file_contents(template_path)

    if stack_defs_str:
        
        stack_definitions = json.loads(stack_defs_str)

        # render yac intrinsics in the stack definition
        stack_definitions = apply_fxn(stack_definitions, service_parmeters) 

    return stack_definitions

def stack_exists(stack_name):

    client = boto3.client('cloudformation')

    try:
        response = client.describe_stacks(StackName=stack_name)
        stack_count = len(response['Stacks'])
        return stack_count>0
    except:
        return False

def deploy_stack_files(service_descriptor, service_parmeters, servicefile_path): 

    # deploy any individual files that the service needs before booting
    # (default to empty array in case variable is not defined)
    files_for_boot = get_variable(service_descriptor, 'deploy-for-boot', [], 'files')

    # render service parmeters in the files then deploy 'em
    _load_files(files_for_boot, service_parmeters, servicefile_path)

    # deploy any directories that the service needs before booting
    dirs_for_boot = get_variable(service_descriptor, 'deploy-for-boot', [], 'directories')

    # render service parmeters in the files contained in the directories then deploy
    # the directory structure to destination
    _load_dirs(dirs_for_boot, service_parmeters)


# Render service parmeters into file body, then load files to destination
# Only s3 destinations are currently supported.
def _load_files(files, service_parmeters, servicefile_path):

    # assume the file path is relative to the location
    # of the service descriptor file (just like Dockerfile!)
    servicefile_path = get_variable(service_parmeters,"servicefile-path")

    for this_ifile in files:

        # render intrinsics in the file dictionary
        this_file = apply_fxn(this_ifile, service_parmeters)      

        # if necessary, localize file
        localized_file = localize_file(this_file['src'], servicefile_path)

        # render the file into the local 'dump' directory
        rendered_file_path = get_dump_path(get_variable(service_parmeters,"service-name","unknown"))

        if os.path.exists(localized_file):

            # replace any service parmeters variables in the file body and return the 
            # name+path of the "rendered" file
            rendered_file = apply_templates_in_file(localized_file, service_parmeters, rendered_file_path)
  
            # if destination is s3 bucket
            if (is_s3_destination(this_file['dest']) and rendered_file):

                # copy rendered file to s3 destination 
                cp_file_to_s3( rendered_file, this_file['dest'])

            # if destination is another local file (mostly used for testing)
            else:

                # make sure destination directory exists
                if not os.path.exists(os.path.dirname(this_file['dest'])):
                    os.makedirs(os.path.dirname(this_file['dest']))

                # copy rendered file to the destination
                shutil.copy(rendered_file,this_file['dest']) 

        else:

            raise FileError( "%s file deploy was not performed. Source file is missing"%localized_file )


# Render service parmeters into file body, then load files to destination
# Only s3 destinations are currently supported.
def _load_files_new(files, service_parmeters):

    # assume the file path is relative to the location
    # of the service descriptor file (just like Dockerfile!)
    servicefile_path = get_variable(service_parmeters,"servicefile-path")

    for this_ifile in files:

        # render intrinsics in the file dictionary
        this_file = apply_fxn(this_ifile, service_parmeters)      

        source_path = os.path.join(servicefile_path,this_file['src'])

        # render the file into a 'tmp' directory under the servicefile dir
        rendered_file_path = os.path.join(servicefile_path,'tmp')

        if os.path.exists(source_path):

            # replace any service parmeters variables in the file body and return the 
            # name+path of the "rendered" file
            rendered_file = apply_templates_in_file(source_path, service_parmeters, rendered_file_path)
  
            # if destination is s3 bucket
            if (is_s3_destination(this_file['dest']) and rendered_file):

                # copy rendered file to s3 destination 
                cp_file_to_s3( rendered_file, this_file['dest'])

            # if destination is another local file (mostly used for testing)
            else:

                # make sure destination directory exists
                if not os.path.exists(os.path.dirname(this_file['dest'])):
                    os.makedirs(os.path.dirname(this_file['dest']))

                # copy rendered file to the destination
                shutil.copy(rendered_file,this_file['dest']) 

        else:

            raise FileError( "%s file deploy was not performed. Source file is missing"%source_path )

def _load_dirs(directories, service_parmeters):

    # assume the directory path is relative to the location
    # of the service descriptor file (just like Dockerfile!)
    servicefile_path = get_variable(service_parmeters,"servicefile-path","")

    for this_idir in directories:

        # render intrinsics in the file dictionary
        this_dir = apply_fxn(this_idir, service_parmeters)      

        source_path = os.path.join(servicefile_path,this_dir['src'])

        # render files into a 'tmp' directory under the servicefile dir
        rendered_dir_path = os.path.join(servicefile_path,'tmp',this_dir['src'])

        if os.path.exists(source_path):

            # replace any service parmeters variables in the file body and return the 
            # "rendered" file contents as a string
            apply_templates_in_dir(source_path, service_parmeters, rendered_dir_path)

            # if destination is s3 bucket
            if is_s3_destination(this_dir['dest']):

                # sync directories to s3 destination
                sync_dir_to_s3( rendered_dir_path, this_dir['dest'])

            # if destination is another local dir (mostly used for testing)
            else:

                # clear destination dir if it exists
                if os.path.exists(this_dir['dest']):
                    shutil.rmtree(this_dir['dest'])

                # recursively copy tmp dir to the destination
                shutil.copytree(rendered_dir_path,this_dir['dest']) 
        else:

            raise FileError( "%s directory deploy was not performed. Source dir is missing"%source_path )


# returns true if file to be loaded is configured for an s3 destination
def is_s3_destination( destination ):

    s3_destination = False

    # S3 destinations are URL's with s3 as the scheme
    # Use this to detect an S3 destination

    # attempt to parse the destination as a URL
    url_parts = urlparse.urlparse(destination)

    if (url_parts and url_parts.scheme and url_parts.scheme == 's3'):

        s3_destination = True

    return s3_destination

# cp a file to an s3 bucket
# raises an Error if source file does not exists
# or if s3 cp fails
def cp_file_to_s3(source_file, destination_s3_url):

    # make sure source file exists
    if os.path.exists(source_file):            

        # form aws cp command for this file
        aws_cmd = "aws s3 cp %s %s"%( source_file, destination_s3_url)

        try:
            subprocess.check_output( aws_cmd , stderr=subprocess.STDOUT, shell=True )

        except subprocess.CalledProcessError as e:
            raise FileError("Error copying file to s3 destination: %s"%e)

    else:
        raise FileError("Source file %s does not exist"%source_file)

# sync a directory to an s3 bucket
# raises an Error if source dir does not exists
# or if s3 sync fails
def sync_dir_to_s3(source_dir, destination_s3_url):

    # make sure source file exists
    if os.path.exists(source_dir):            

        # form aws sync command for this directory
        # use --delete option to remove any files or directories already in s3 
        # destination that aren't in source_dir
        aws_cmd = "aws s3 sync %s %s %s"%( source_dir, destination_s3_url,"--delete")

        try:
            subprocess.check_output( aws_cmd , stderr=subprocess.STDOUT, shell=True )

        except subprocess.CalledProcessError as e:
            raise FileError("Error copying directory to s3 destination: %s"%e)

    else:
        raise FileError("Source directory %s does not exist"%source_dir)

# Get the running ec2 instances in a stack identified by stack_name
def get_running_ec2s( stack_name , name_search_string=""):

    # filters for stack_id in cloudformation tag
    filters = [{'Name':"tag:aws:cloudformation:stack-name", 'Values' : [stack_name]}]

    # if specifying a Name, filter on that name
    if name_search_string:
        filters.append({'Name':"tag:Name", 'Values' : [name_search_string]})

    #pull response with instances matching filters
    client = boto3.client('ec2')
    reservations = client.describe_instances(Filters=filters)

    # get the private or public ip address of instances that are running
    instances = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*]", reservations)        

    # because the of the reservations in the outer layer, the search above will return 
    # the IP array in a out array, e.g.
    # [[ip1, ip2, etc.]]

    if len(instances) == 1:
        # we need to get rid of outer array
        return instances[0]
    else:
        # no instances found
        return []

# Get the ip addresses of ec2 instances in a stack identified by stack_name
# with a name containing name_search_string.
# If no name_search_string provided, returns IP addresses of all stack EC2 instances
def get_ec2_ips( stack_name , name_search_string="", publicIP=False):

    # filters for stack_id in cloudformation tag
    filters = [{'Name':"tag:aws:cloudformation:stack-name", 'Values' : [stack_name]}]

    # if specifying a Name, filter on that name
    if name_search_string:
        filters.append({'Name':"tag:Name", 'Values' : [name_search_string]})

    #pull response with instances matching filters
    client = boto3.client('ec2')
    instances = client.describe_instances(Filters=filters)

    # get the private or public ip address of instances that are running
    if publicIP:
        ips = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*].PublicIpAddress", instances)        
    else:
        ips = jmespath.search("Reservations[?Instances[?State.Name=='running']].Instances[*].PrivateIpAddress", instances)

    # because the of the reservations in the outer layer, the search above will return 
    # the IP array in a out array, e.g.
    # [[ip1, ip2, etc.]]

    # we need to get rid of outer array
    if len(ips)==1:
        return ips[0]
    else:
        return ""

def get_ec2_sgs( stack_name , name_search_string=""):

    # filters for stack_id in cloudformation tag
    filters = [{'Name':"tag:aws:cloudformation:stack-name", 'Values' : [stack_name]}]

    # if specifying a Name, filter on that name
    if name_search_string:
        filters.append({'Name':"tag:Name", 'Values' : [name_search_string]})

    #pull response with instances matching filters
    client = boto3.client('ec2')
    sgs = client.describe_security_groups(Filters=filters)

    # we need to get rid of outer array
    return sgs['SecurityGroups']

# get the RDS endpoints associated with a stack
def get_rds_endpoints( stack_name ):

    endpoints = []

    # get the resources associated with the stack
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)

    rds_id = ""

    if 'StackResources' in resources:

        for resource in resources['StackResources']:

            if resource['ResourceType'] == 'AWS::RDS::DBInstance':

                rds_id = resource['PhysicalResourceId']

    if rds_id:

        client = boto3.client('rds')
        instances = client.describe_db_instances(DBInstanceIdentifier=rds_id)

        # print "instances: %s"%json.dumps(instances,indent=2)

        endpoints = jmespath.search("DBInstances[*].{Address: Endpoint.Address, Port: Endpoint.Port, Status: DBInstanceStatus}", instances)

    return endpoints

# get the ECS services associated with a stack
def get_ecs_service( stack_name , name_search_string):

    to_ret={}

    # get the resources associated with the stack
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)

    service_id = ""
    cluster_name = ""

    if 'StackResources' in resources:

        for resource in resources['StackResources']:

            if resource['ResourceType'] == 'AWS::ECS::Service':

                if name_search_string in resource['PhysicalResourceId']:
                    service_id = resource['PhysicalResourceId']
                    #print "ecs service: %s"%service_id

            if resource['ResourceType'] == 'AWS::ECS::Cluster':

                cluster_name = resource['PhysicalResourceId']
                #print "ecs cluster: %s"%cluster_name                    

    if service_id and cluster_name:

        client = boto3.client('ecs')
        services = client.describe_services(cluster=cluster_name, 
                                            services=[service_id])

        #print "ecs services: %s"%services
        for service in services['services']:
            if name_search_string in service['serviceName']:
                to_ret = service
                break

    return to_ret       

# get the ECS services associated with a stack
def get_stack_elbs( stack_name , name_search_string):

    to_ret={}

    # get the resources associated with the stack
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)

    elb_id = ""

    if 'StackResources' in resources:

        for resource in resources['StackResources']:

            if resource['ResourceType'] == 'AWS::ElasticLoadBalancing::LoadBalancer':

                if name_search_string in resource['PhysicalResourceId']:
                    elb_id = resource['PhysicalResourceId']
                    break
                                    

    if elb_id:

        client = boto3.client('elb')
        elbs = client.describe_load_balancers(LoadBalancerNames=[elb_id])

        for elb in elbs['LoadBalancerDescriptions']:
            if name_search_string in elb['LoadBalancerName']:
                to_ret = elb
                break
    return to_ret    

def get_rds_instance_ids( stack_name ):

    instances_ids = []

    # get the resources associated with the stack
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)

    rds_id = ""

    if 'StackResources' in resources:

        for resource in resources['StackResources']:

            if resource['ResourceType'] == 'AWS::RDS::DBInstance':

                rds_id = resource['PhysicalResourceId']

    if rds_id:

        client = boto3.client('rds')
        instances = client.describe_db_instances(DBInstanceIdentifier=rds_id)

        instances_ids = jmespath.search("DBInstances[*].DBInstanceIdentifier", instances)

    return instances_ids    

# get the name of the elastic cache endpoint associated with a stack
def get_cache_endpoint( stack_name ):

    endpoint = {}

    # get the resources associated with the stack
    cloudformation = boto3.client('cloudformation')
    resources = cloudformation.describe_stack_resources(StackName=stack_name)

    cache_id = ""

    if 'StackResources' in resources:

        for resource in resources['StackResources']:

            if resource['ResourceType'] == 'AWS::ElastiCache::ReplicationGroup':

                cache_id = resource['PhysicalResourceId']

    if cache_id:

        client = boto3.client('elasticache')
        response = client.describe_replication_groups(ReplicationGroupId=cache_id)

        if ('ReplicationGroups' in response and len(response['ReplicationGroups'])>0):

            this_rep_group = response['ReplicationGroups'][0]

            for node in this_rep_group['NodeGroups']:

                if 'PrimaryEndpoint' in node:

                    endpoint = node['PrimaryEndpoint']

    return endpoint    

# get the subnets associated with an auto-scaling groups
def get_asg_subnet_ids( asg_name ):

    #pull response with instances matching filters
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
    else:
        asg = {}

    subnet_ids = []

    if asg:
        subnet_id_str = asg['VPCZoneIdentifier']
        subnet_ids = subnet_id_str.split(',')
        
    return subnet_ids  

# get the iam role associated with an auto-scaling groups
def get_stack_iam_role( params ):

    asg_name = get_resource_name(params,'asg')

    #pull response with instances matching filters
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
        launchConfigName = asg['LaunchConfigurationName']
    else:
        launchConfigName = ""

    iam_role = ""

    if launchConfigName:
        response = client.describe_launch_configurations(LaunchConfigurationNames=[launchConfigName])

        if response['LaunchConfigurations']:
            iam_role = response['LaunchConfigurations'][0]['IamInstanceProfile']
        
    return iam_role      

# get the ssh key associated with an auto-scaling groups
def get_stack_ssh_keys( params ):

    asg_name = get_resource_name(params,'asg')

    #pull response with instances matching filters
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    if response['AutoScalingGroups']:
        asg = response['AutoScalingGroups'][0]
        launchConfigName = asg['LaunchConfigurationName']
    else:
        launchConfigName = ""

    ssh_key = ""

    if launchConfigName:
        response = client.describe_launch_configurations(LaunchConfigurationNames=[launchConfigName])

        if response['LaunchConfigurations']:
            ssh_key = response['LaunchConfigurations'][0]['KeyName']
        
    return ssh_key   

# get the ssl cert associated with an elb
def get_stack_ssl_cert( params ):

    ielb_name = get_resource_name(params,'i-elb')
    eelb_name = get_resource_name(params,'e-elb')

    #pull response with instances matching filters
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[ielb_name,eelb_name])

    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}

    ssl_cert = ""

    if elb:
        ssl_certs = jmespath.search('[*].Listener.SSLCertificateId',elb['ListenerDescriptions'])
        if (ssl_certs and len(ssl_certs)==1):
            ssl_cert = ssl_cert[0]
        
    return ssl_cert     

# returns true if an existing stack has external (public) access
def stack_has_external_access( params ):

    external_access = False

    eelb_name = get_resource_name(params,'e-elb')

    #pull response with instances matching filters
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[eelb_name])

    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}

    # if the e-elb was found, stack provides external access
    if elb:
        external_access = True

    return external_access

# get vpc associated with an existing stack
def get_stack_vpc( params ):

    stack_name = get_stack_name(params)

    vpc_id = ""

    if stack_name:

        # get the stack
        cloudformation = boto3.client('cloudformation')

        try:
            stack = cloudformation.describe_stacks(StackName=stack_name)

            # get the first stack's 'stack id'
            stack_id = stack['Stacks'][0]['StackId']

            # filters for stack_id in cloudformation tag
            filters = [{'Name':"tag:aws:cloudformation:stack-id", 'Values' : [stack_id]}]

            #pull response with instances matching filters
            client = boto3.client('ec2')

            reservations = client.describe_instances(Filters=filters)

            intances = jmespath.search('Reservations[*].Instances',reservations)

            if len(intances)>=1:

                # use the vpd id of the first instance
                # print intances[0][0]
                vpc_id = intances[0][0]['VpcId']

                vpcs = client.describe_vpcs(VpcIds=[vpc_id])

                if 'Vpcs' in vpcs and len(vpcs['Vpcs'])==1:
                    vpc =  vpcs['Vpcs'][0]
                    vpc_id = vpc["VpcId"]

        except ClientError as e:
            print "existing stack not found"

        return vpc_id   

# get the subnets associated with an internal load balancer
def get_elb_subnet_ids( load_balancer_name ):

    #pull response with instances matching filters
    client = boto3.client('elb')
    response = client.describe_load_balancers(LoadBalancerNames=[load_balancer_name])

    if response['LoadBalancerDescriptions']:
        elb = response['LoadBalancerDescriptions'][0]
    else:
        elb = {}

    subnet_ids = []

    if elb:
        subnet_ids = elb['Subnets']
        
    return subnet_ids

def get_stack_param_value( stack_name , stack_param_name ):
    
    client = boto3.client('cloudformation')

    response = client.describe_stacks(StackName=stack_name)
    
    if response['Stacks']:
        stack = response['Stacks'][0]
    else:
        stack = {}

    value = ""

    if (stack and 'Parameters' in stack):
        for param in stack['Parameters']:
            if param['ParameterKey'] == stack_param_name:
                value = param['ParameterValue'] 
        
    return value

# get the value from a tag
def get_stack_tag_value( service_params , stack_tag_name ):

    stack_name = get_stack_name(service_params)
    
    client = boto3.client('cloudformation')

    response = client.describe_stacks(StackName=stack_name)
    
    if response['Stacks']:
        stack = response['Stacks'][0]
    else:
        stack = {}

    value = ""

    if (stack and 'Tags' in stack):
        for param in stack['Tags']:
            if param['Key'] == stack_tag_name:
                value = param['Value'] 
        
    return value
   
def stop_service_blocking(stack_name, name_search_string):

    ecs_service = get_ecs_service(stack_name, name_search_string)

    if ecs_service and ecs_service['runningCount'] == 1:

        print "Stopping the %s service ..."%ecs_service['serviceName']

        # stop the service by setting the desired count to 0
        client = boto3.client('ecs')
        client.update_service(cluster=ecs_service['clusterArn'],
                              service=ecs_service['serviceName'],
                              desiredCount=0)

        timer_start=dt.datetime.now()

        # wait for the running count to change to "0"
        while ( ecs_service['runningCount'] != 0 ):

            now=dt.datetime.now()
            elapsed_secs = (now-timer_start).seconds
            sys.stdout.write('\r')
            msg = ("After %s seconds, the service is still running ...")%(elapsed_secs)
            sys.stdout.write(msg)
            sys.stdout.flush()

            # sleep for 5 seconds then check service state again
            time.sleep(5)

            # check the state of the service
            ecs_service = get_ecs_service(stack_name, name_search_string)

        # print an empty line to insert a cr
        print ""  

def start_service(stack_name, name_search_string):

    ecs_service = get_ecs_service(stack_name, name_search_string)

    if ecs_service and ecs_service['runningCount'] == 0:

        # stop the service by setting the desired count to 0
        client = boto3.client('ecs')
        client.update_service(cluster=ecs_service['clusterArn'],
                              service=ecs_service['serviceName'],
                              desiredCount=1)            