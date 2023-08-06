#!/usr/bin/env python

from docker import Client
import docker, os, json, zipfile, urllib
from StringIO import StringIO
from yac.lib.container.api import get_docker_client
from yac.lib.template import apply_templates_in_dir

def build_image(
            image_tag,
            sources_path,
            connection_str = "",
            rm = "false",
            buildargs={}):

    print 'Getting docker client for connection_str=%s' % (connection_str)

    docker_client = get_docker_client( connection_str )

    # build the image
    for line in docker_client.build(tag=image_tag,
                                    path=sources_path,
                                    rm=rm,
                                    buildargs=buildargs):

        line_json = json.loads(line)

        if 'stream' in line_json:
            print line_json['stream']
        else:
            print line_json

def get_image_versions_local(connection_str, image_name):

    docker_client = get_docker_client( connection_str )

    # get the image
    images = docker_client.images()

    versions = []

    # print "local images: %s"%(images)

    for image in images:

        if ('RepoTags' in image and image['RepoTags']):
            for tag in image['RepoTags']:

                if image_name in tag:

                    versions = versions + [parse_image_version(tag)]
                    break;

    return versions

def get_rendered_dockerpath(image_tag):

    # define a page where rendered dockerfiles can written

    home = os.path.expanduser("~")

    dockerfile_path = ""

    build_path = os.path.join(home,'.yac','dockerfiles', image_tag)

    return build_path 

def download_dockerfile(image_tag, repo_url):

    home = os.path.expanduser("~")

    dockerfile_path = ""

    build_path = get_rendered_dockerpath(image_tag)

    tmp_path = os.path.join(home,'.yac',"tmp")

    name = os.path.join(tmp_path, 'temp.zip')
    try:
        name, hdrs = urllib.urlretrieve(repo_url, name)
    except IOError, e:
        print "Can't download %r to %r: %s" % (repo_url, name, e)
        return
    
    try:
        z = zipfile.ZipFile(name)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (repo_url, e)
        return
    for n in z.namelist():
        dest = os.path.join(build_path, n)
        destdir = os.path.dirname(dest)

        if "Dockerfile" in dest:
            dockerfile_path = destdir

        if not os.path.exists(destdir):
            os.makedirs(destdir)

        if not os.path.isdir(dest):
            data = z.read(n)
            f = open(dest, 'w')
            f.write(data)
            f.close()

    z.close()
    os.unlink(name)

    return dockerfile_path

def get_image_name(image, version):

    return "%s:%s"%(image,version)

def parse_image_version(image_tag):

    image_parts = image_tag.split(':')

    return image_parts[1]