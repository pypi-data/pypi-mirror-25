import re, boto3, os, json, jmespath, sys, argparse, botocore
from subprocess import call
from yac.lib.variables import get_variable, set_variable
from yac.lib.file import get_file_contents, dump_dictionary
from yac.lib.cache import get_cache_value, set_cache_value_dt, delete_cache_value
from yac.lib.inputs import string_validation

STATE_CACHE_KEY_PREFIX="yac/lib/state"

# state is persisted in a json file in s3
def load_state_s3(s3_bucket, s3_path, service_alias):

    state = {}

    s3 = boto3.resource('s3')

    state_filename = get_state_filename(service_alias)

    state_file_local_path_full = get_state_local_path(s3_path,service_alias)

    s3_file_path = "%s/%s"%(s3_path,state_filename)

    if state_exists(s3_bucket, s3_file_path):

        # pull file down to the local dir
        s3.meta.client.download_file(s3_bucket, 
                                     s3_file_path, 
                                     state_file_local_path_full)

        # pull contents into a dictionary
        file_contents = get_file_contents(state_file_local_path_full)
        state = json.loads(file_contents)

    else:
        print "stack state doesn't exist at %s:%s..."%(s3_bucket,s3_path)

    return state

# state is persisted in a json file in s3 but the bucket used is either:
# 1) per the service alias, or
# 2) per user prompt/cache
def load_state(s3_path, service_alias):

    state = {}
    state_filename = get_state_filename(service_alias)

    # add to path as necessary to ensure the service name is represented in either 
    # the bucket name or the s3 object path
    s3_full_path = get_s3_full_path(s3_path, service_alias)

    # find bucket based on presence in local cache and presence of state data in bucket
    s3_bucket = find_bucket_with_state_in_cache(s3_full_path, service_alias)
    
    if not s3_bucket:    
        
        # find bucket based on bucket name and presence of state data in bucket
        s3_bucket = find_bucket_with_state_by_name(s3_full_path, service_alias)

        if not s3_bucket:

            # prompt user for a bucket
            s3_bucket = prompt_for_bucket(service_alias)

        else:
            msg = ("Loading service state from " +
                   "s3://%s/%s/%s.\n"%(s3_bucket, s3_path,state_filename) +
                   "(hint: to use a different bucket either move or rename the state file and re-run 'yac stack ...')")
            print msg

    else:
        msg = ("Loading service state from " +
               "s3://%s/%s/%s.\n"%(s3_bucket, s3_path,state_filename) +
               "(hint: to use a different bucket either move or rename the state file and re-run 'yac stack ...')")
        print msg
    
    state_file_local_path_full = get_state_local_path(s3_full_path,service_alias)

    s3_file_path = "%s/%s"%(s3_full_path,state_filename)

    # print "s3 bucket: %s, s3 path: %s"%(s3_bucket,s3_file_path)

    if state_exists(s3_bucket, s3_file_path):

        s3 = boto3.resource('s3')

        # pull file down to the local dir
        s3.meta.client.download_file(s3_bucket, 
                                     s3_file_path, 
                                     state_file_local_path_full)

        # pull contents into a dictionary
        file_contents = get_file_contents(state_file_local_path_full)
        state = json.loads(file_contents)

    else:
        print "stack state doesn't exist at %s ..."%(s3_file_path)


    return state, s3_bucket

def get_s3_full_path(s3_path, service_alias):

    s3_full_path = "%s/%s"%(service_alias,s3_path)

    return s3_full_path

def state_exists(s3_bucket,s3_path):

    object_exists = False

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    objs = list(bucket.objects.filter(Prefix=s3_path))
    if len(objs) > 0 and objs[0].key == s3_path:
        object_exists = True

    return object_exists

def save_state(s3_path, service_alias, state, s3_bucket=""):

    state_filename = get_state_filename(service_alias)

    if not s3_bucket:

        # find bucket based on presence in local cache and presence of state data in bucket
        s3_bucket = find_bucket_in_cache(service_alias)
        
        if not s3_bucket:    
            
            # find bucket based on bucket name
            s3_bucket = find_bucket_by_name(service_alias)

            if not s3_bucket:

                # prompt user for a bucket
                s3_bucket = prompt_for_bucket(service_alias)

            else:
                msg = ("Saving service state to s3://%s/%s/%s.\n"%(s3_bucket, s3_path, state_filename))
                print msg

        else:
            msg = ("Saving service state to s3://%s/%s/%s.\n"%(s3_bucket, s3_path, state_filename))
            print msg

    # add to path as necessary to ensure the service name is represented in either 
    # the bucket name or the s3 object path
    s3_path = get_s3_full_path(s3_path,service_alias)

    state_file_local_path_full = get_state_local_path(s3_path, service_alias)

    # print "full path: %s"%state_file_local_path_full

    # write state dictionary to the file
    state_str = json.dumps(state, indent=2)

    # make sure dir exists
    state_file_local_path = os.path.basename(state_file_local_path_full)
    
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    with open(state_file_local_path_full, 'w') as file_arg_fp:
        file_arg_fp.write(state_str)
        
    state_filename = get_state_filename(service_alias)            
    s3_file_path = "%s/%s"%(s3_path,state_filename)

    # write file to s3
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(state_file_local_path_full, 
                               s3_bucket,
                               s3_file_path)

    return s3_bucket

def save_state_s3(s3_bucket, s3_path, service_alias, state):

    s3 = boto3.resource('s3')

    state_file_local_path_full = get_state_local_path(s3_path, service_alias)

    # write state dictionary to the file
    state_str = json.dumps(state, indent=2)

    # make sure dir exists
    state_file_local_path = os.path.basename(state_file_local_path_full)
    
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    with open(state_file_local_path_full, 'w') as file_arg_fp:
        file_arg_fp.write(state_str)
        
    state_filename = get_state_filename(service_alias)            
    s3_file_path = "%s/%s"%(s3_path,state_filename)

    # write file to s3
    s3.meta.client.upload_file(state_file_local_path_full, 
                               s3_bucket,
                               s3_file_path)

def get_state_filename(service_alias):

    state_filename = "%s-state.json"%(service_alias)

    return state_filename

def get_state_local_path(s3_full_path,service_alias):

    home = os.path.expanduser("~")
    # s3_full_path = get_s3_full_path(s3_path,service_alias)
    state_file_local_path = os.path.join(home, '.yac', s3_full_path)
    state_filename = get_state_filename(service_alias)
    state_file_local_path_full = os.path.join(state_file_local_path,state_filename)

    # make sure local path exists
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    return state_file_local_path_full

def get_state_s3_bucket(service_alias):

    # default place for state to be saved is a bucket with the same name as 
    # the service alias

    s3_bucket = ""

    # verify bucket exists
    if bucket_exists(service_alias):

        # the bucket to use is the same as the service name
        s3_bucket = service_alias

    return s3_bucket    

def get_state_s3_bucket_old(service_alias):

    # default place for state to be saved is a bucket with the same name as 
    # the service alias

    s3_bucket = ""

    # verify bucket exists
    if bucket_exists(service_alias):

        # the bucket to use is the same as the service name
        s3_bucket = service_alias

    return s3_bucket    

def find_bucket_in_cache(service_alias):

    # see if the user has cached the desired bucket for state values
    state_cache_key = get_state_cache_key(service_alias)

    # see if the name of the s3 bucket to use for state is in
    # the users cache
    s3_bucket = get_cache_value(state_cache_key, "")

    return s3_bucket

def get_state_cache_key(service_alias):

    return "%s/%s"%(STATE_CACHE_KEY_PREFIX,service_alias)

def find_bucket_with_state_in_cache(this_s3_path, service_alias):

    s3_bucket = ""

    s3_bucket_candidate = find_bucket_in_cache(service_alias)

    if s3_bucket_candidate:

        if state_file_exists(s3_bucket_candidate, service_alias, this_s3_path):
            
            print "state file exists ..."
            s3_bucket = s3_bucket_candidate

    return s3_bucket

def find_bucket_by_name(search_str):

    s3_bucket = ""

    s3 = boto3.client('s3')
    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:

        if ( search_str in bucket['Name'] ):
            
            # this is the bucket
            s3_bucket = bucket['Name']

    return s3_bucket

def find_bucket_with_state_by_name(this_s3_path, service_alias):

    s3_bucket = ""

    s3_bucket_candidate = find_bucket_by_name(service_alias)

    if s3_bucket_candidate:

        # print "checking %s bucket against %s path"%(s3_bucket_candidate, this_s3_path)

        if state_file_exists(s3_bucket_candidate, service_alias, this_s3_path):
            
            # this is the bucket
            s3_bucket = s3_bucket_candidate

    return s3_bucket

def prompt_for_bucket(service_alias):

    s3_bucket = ""
    while True:

        print "The service needs an S3 bucket that can be used to save its state. Available buckets include:"
        print str(get_buckets_names()) + "\n"

        msg = "Please enter the name a bucket >> "
        s3_bucket = raw_input(msg)

        if bucket_exists(s3_bucket):

            # save bucket to the cache for future reference
            set_state_cache(service_alias, s3_bucket)

            break
        else:
            print "bucket doesn't exist ... try again"

    return s3_bucket

def set_state_cache(service_alias, s3_bucket):

    state_cache_key = get_state_cache_key(service_alias)

    # save to cache with max timeout
    set_cache_value_dt(state_cache_key,
                       s3_bucket)

def clear_state_cache(service_alias):

    state_cache_key = get_state_cache_key(service_alias)
    
    delete_cache_value(state_cache_key)

def get_state_s3_bucket_cached_old(service_alias):

    s3_bucket = ""

    # see if the user has cached the desired bucket for state values
    STATE_CACHE_KEY = "yac/lib/state/%s"%service_alias

    while True:

        # see if the name of the s3 bucket to use for state is in
        # the users cache
        jira_state_s3 = get_cache_value(STATE_CACHE_KEY, {})

        if ('state-bucket' not in jira_state_s3):

            msg = "Please enter the name of the S3 buckets that this app uses to persist its state >> "
            s3_bucket = raw_input(msg)

            if bucket_exists(s3_bucket):

                # save pwd back to the secrets cache for future reference
                # with max timeout
                jira_state_s3['state-bucket'] = s3_bucket
                set_cache_value_dt(STATE_CACHE_KEY,
                                   jira_state_s3)

                break
            else:
                print "bucket doesn't exist ... try again"

        else:
            msg = ("Loading service state from the '%s' S3 buckets ('enter' to continue, 'n' to specify " +
                   "a different bucket)  >> ")%jira_state_s3['state-bucket']
            re_load = raw_input(msg)

            if not re_load:
                s3_bucket = jira_state_s3['state-bucket']
                break
            else:
                delete_cache_value(STATE_CACHE_KEY)

    return s3_bucket    

def create_state_s3_bucket(service_alias):
    
    s3 = boto3.resource('s3')

    # bucket name should match the service alias
    response = client.create_bucket(
        ACL='private',
        Bucket=service_alias)

    # state bucket should be versioned
    response = client.put_bucket_versioning(
        Bucket=service_alias,
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled'
        }
    )

 

def state_file_exists(s3_bucket, service_alias, s3_path):

    state_file_exists = False

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)

    state_filename = get_state_filename(service_alias)

    s3_file_path = "%s/%s"%(s3_path,state_filename)

    # print "bucket: %s, path: %s"%(s3_bucket,s3_file_path)
    try:
        objs = list(bucket.objects.filter(Prefix=s3_file_path))

        if objs:
            state_file_exists = True

    except botocore.exceptions.ClientError as e:
        state_file_exists = False

    return state_file_exists 

def bucket_exists(s3_bucket):

    bucket_exists = True

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    try:
        objs = list(bucket.objects.filter(Prefix="/"))
        bucket_exists = True
    except botocore.exceptions.ClientError as e:
        bucket_exists = False

    return bucket_exists 

def edit_state(s3_path, service_alias, state_params):

    s3_full_path = get_s3_full_path(s3_path,service_alias)
    
    tmp_file_name = "%s-state.json"%service_alias

    # write the params to the file
    state_file_local_path_full = dump_dictionary(state_params, service_alias, tmp_file_name)

    # open an editor session so user can edit the file
    EDITOR = os.environ.get('EDITOR','nano')

    call([EDITOR, state_file_local_path_full])

    # load the file contents back into a dictionary
    file_contents = get_file_contents(state_file_local_path_full)

    # pull the service params from file
    if file_contents:

        new_state_params = json.loads(file_contents)
        state_params.clear()
        state_params.update(new_state_params)    

def state_change_prompter(msg):

    validation_failed = True
    change = False

    # accept y, n, or empty string
    options = ['y','n', '']

    while validation_failed:

        input = raw_input(msg)

        # validate the input
        validation_failed = string_validation(input, options, False)

    # change iff 'y' was input
    if (input and input == 'y'):
        change = True

    return change

def get_buckets_names():

    bucket_names = []

    s3 = boto3.client('s3')
    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:

        bucket_names = bucket_names + [bucket['Name']]

    return bucket_names    