import argparse, os, inspect, jmespath, json
from colorama import Fore, Style
from yac.lib.service import get_service, get_service_parmeters, get_service_alias
from yac.lib.stack import get_stack_templates, get_stack_name, get_ec2_ips, deploy_stack_files
from yac.lib.naming import set_namer
from yac.lib.params import get_service_params, NULL_PARAMS, INVALID_PARAMS
from yac.lib.vpc import get_vpc_prefs 
from yac.lib.variables import get_variable,set_variable
from yac.lib.cache import get_cache_value, set_cache_value_dt

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The key file %s does not exist!" % arg)
    else:
        return arg

def main():

    path_help =   'path to the private key file for this service'
    user_help =   'the user to login as'
    public_help = 'connect using the public IP address?'

    parser = argparse.ArgumentParser('ssh into a stack ec2 instance')

    parser.add_argument('servicefile', help='location of the Servicefile (registry key or abspath)')
    parser.add_argument('--path', help=path_help + ' (defaults to previous)',
                                       type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-u','--user', help=user_help + ' (defaults to previous')
    parser.add_argument('-s','--search',help='search string, to support multiple EC2 instances in the same auto-scaling group')
    parser.add_argument('--public',     help=public_help + ' (defaults to previous)', 
                                        action='store_true')
    parser.add_argument('-a',
                        '--alias',  help='service alias for the stack currently supporting this service (deault alias is per Servicefile)')
    parser.add_argument('-p',
                        '--params',  help='path to a file containing additional, static, service parameters (e.g. vpc params, of service constants)') 

    # pull out args
    args = parser.parse_args()

     # determine service defintion, complete service name, and service alias based on the args
    service_descriptor, service_name, servicefile_path = get_service(args.servicefile) 

    # abort if service_descriptor was not loaded successfully
    if not service_descriptor:
        print("The Servicefile input does not exist locally or in registry. Please try again.")
        exit()

    # get vpc preferences in place
    vpc_prefs = get_vpc_prefs()

    # set the resource namer to use with this service
    set_namer(service_descriptor, servicefile_path, vpc_prefs)

    # get the alias to use with this service
    service_alias = get_service_alias(service_descriptor,args.alias)

    # determine service params based on the params arg
    service_params_input, service_params_name = get_service_params(args.params)

    # abort if service params were not loaded successfully
    if args.params and service_params_name == NULL_PARAMS:
        print("The service params specified do not exist locally or in registry. Please try again.")
        exit()
    elif service_params_name == INVALID_PARAMS:
        print("The service params file specified failed validation checks. Please try again.")
        exit()

     # get the service parameters for use with yac-ref's in service templates
    service_parmeters = get_service_parmeters(service_alias, service_params_input, 
                                              service_name, service_descriptor,
                                              servicefile_path, vpc_prefs)

    # get the name of the stack that corresponds to this app and env
    stack_name = get_stack_name(service_parmeters)

    # should we connect using a public ip addr?
    use_public = get_use_public(service_alias, args.public)

    # get the IP address of the ec2 instance for this stack
    ec2_ips = get_ec2_ips(stack_name, args.search, use_public)

    if (ec2_ips and len(ec2_ips)==1):

        ec2_ip = ec2_ips[0]

        # get the user to ssh in as
        ssh_user = get_ssh_user(service_alias, user_help, args.user)

        # get the path to the ssh key for this service
        key_path = get_key_path(service_alias, path_help, args.path)

        # prepare ssh command
        ssh_cmd = "ssh -i %s %s@%s"%(key_path,ssh_user,ec2_ip)

        # add ingress on port 22 to the SG associated with the instance

        # ssh in
        os.system(ssh_cmd)

        print "future versions will remove 22 ingress here..."

    elif (ec2_ips and len(ec2_ips)>1):

        print 'Found multiple EC2 address for the %s app in the %s env. Consider adding a search string.'%(args.app, args,env)

    else:

        print 'Could not find address for the %s app in the %s env'%(args.app, args,env)

def get_use_public(service_alias, arg_input):

    cache_key = "%s:arg:use-public"

    use_public = get_cached_arg_bool('public', arg_input, cache_key)

    return use_public

def get_key_path(service_alias, arg_help, arg_input):

    cache_key = "%s:arg:ssh-key"

    validation_fxn = "os.path.exists"

    key_path = get_cached_arg_val('path', arg_input, cache_key, arg_help, validation_fxn)

    return key_path

def get_ssh_user(service_alias, arg_help, arg_input):

    cache_key = "%s:arg:ssh-user"

    ssh_user = get_cached_arg_val('path', arg_input, cache_key, arg_help)

    return ssh_user

def get_cached_arg_val(arg_name, arg_input, cache_key, input_help, validation_fxn=""):

    cached_arg_val = ""

    if arg_input:
        cached_arg_val = arg_input
    else:
        # see if the arg is in the user's local cache
        cached_arg_val = get_cache_value(cache_key, '')

        if not cached_arg_val:

            print "The %s input is not yet cached locally."%arg_name
            print "Arg description: %s."%arg_help

            input_prompt_msg = "Please enter a value for %s >> "%arg_name

            if validation_fxn:
                while not validation_fxn(cached_arg_val):
                    cached_arg_val = raw_input(input_prompt_msg)                
            else:
                cached_arg_val = raw_input(input_prompt_msg)

    # save pwd back to the local cache for future reference
    # with max timeout
    set_cache_value_dt(cache_key,
                       cached_arg_val)

    return cached_arg_val

def get_cached_arg_bool(arg_name, arg_input, cache_key):

    cached_arg_val = ""

    if arg_input:
        cached_arg_val = arg_input
    else:
        # see if the arg is in the user's local cache
        cached_arg_val = get_cache_value(cache_key, '')

    # save pwd back to the local cache for future reference
    # with max timeout
    set_cache_value_dt(cache_key,
                       cached_arg_val)

    return cached_arg_val
