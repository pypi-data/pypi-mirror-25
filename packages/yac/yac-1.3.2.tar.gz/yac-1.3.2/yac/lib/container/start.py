#!/usr/bin/env python

import sys
import docker.utils, os, json, subprocess, urlparse
from docker import Client
from yac.lib.container.api import get_docker_client, get_connection_str, find_container_by_name


# cp a file to an s3 buckert
# raises an Error if source file does not exists
# raises an subprocess.CalledProcessError if cp fails
def cp_to_s3(source_file, destination_s3_url):

    # make sure source file exists
    if os.path.exists(source_file):            

        # form aws cp command for this file
        aws_cmd = "aws s3 cp %s %s"%( source_file, destination_s3_url)

        subprocess.check_output( aws_cmd , stderr=subprocess.STDOUT, shell=True )

    else:
        raise Exception("Source file does not exist")

def load_image(image_source, image_name, docker_client):

    # if image source is docker hub, pull down image for this container
    # o.w. assume image is local
    if image_source == "hub":
        docker_client.pull( image_name )

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


# converts a volumes_from list of container aliases to a list with container id's
def volumnes_from_with_ids(volumes_from, connection_str):

    volumes_from_ids = []

    for container_alias in volumes_from:

        # get the container
        container = find_container_by_name(container_alias, connection_str)

        volumes_from_ids.append(container.get('Id'))

    return volumes_from_ids


# start a container from an image
def start(
        image_tag,
        envs,
        alias,
        volumes_bindings,
        volume_mapping,
        volumes_from,
        port_bindings,
        connection_str,
        start_cmd,
        files_to_load,        
        template_vars,
        image_source='local',
        create_only=False):

    docker_client = get_docker_client( connection_str )

    # create the volumne host config from the volume_mapping
    volume_host_config = docker_client.create_host_config(binds=volume_mapping)

    # make sure container with same name/alias doesn't already exist
    if alias:

        existing_container = find_container_by_name( alias, connection_str )

        if existing_container:

            print "stopping existing %s container"%alias

            # stop container gracefully (giving it a full 30 secs)
            docker_client.stop(container=existing_container.get('Id'),
                               timeout=30)

            # remove container
            docker_client.remove_container( existing_container, force=True)

    # load the image on the host
    load_image(image_source, image_tag, docker_client)

    # load any files specified
    if files_to_load:

        load_files(files_to_load, template_vars)

    # render templates in environment variables
    if template_vars:
        rendered_envs = _render_env_variables(envs, template_vars)
    else:
        rendered_envs = envs

    # create new container

    # if starting with a command other than the stock CMD in the dockerfile ...
    if start_cmd:

        container = docker_client.create_container(image=image_tag, 
                                                   name=alias, 
                                                   environment=rendered_envs,
                                                   volumes=volumes_bindings,                                               
                                                   host_config=volume_host_config,
                                                   command=start_cmd,
                                                   stdin_open=True,
                                                   tty=True)

    else:
        container = docker_client.create_container(image=image_tag, 
                                                   name=alias, 
                                                   environment=rendered_envs,
                                                   volumes=volumes_bindings,                                               
                                                   host_config=volume_host_config,
                                                   stdin_open=True,
                                                   tty=True)
    # start container
    if (container and container.get("Id") and not create_only):

        response = docker_client.start(container=container.get('Id'), 
                            port_bindings=port_bindings,
                            volumes_from = volumnes_from_with_ids(volumes_from,connection_str)  )

        if response:
            print "%s container created and started. Response from Docker: %s"%(alias,response)
        else:
            print "%s container created and started."%(alias)

    else:
        print "%s container was not started successfully"%alias

# execute a command in an existing container
def execute(
        container_name,
        exec_cmd,
        connection_str):

    docker_client = get_docker_client( connection_str )
    
    # create the execution thread
    execution = docker_client.exec_create(container=container_name,
                                           cmd=exec_cmd, 
                                           stdout=True,
                                           stderr=True,
                                           tty=True)

    # if execution succeeded, start the command
    if execution and  execution.get('Id'):

        response = docker_client.exec_start(exec_id=execution.get('Id'), 
                                             tty=True)

        if response:
            print "Response from Docker:\n %s"%(response)

    else:
        print "%s command in %s container was not started successfully"%(exec_cmd, container_name)
