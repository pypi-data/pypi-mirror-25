=======================
yac - portable services
=======================

A service, running on your VPC, from nothing to ka-ching, in a few minutes.

-  Have access to an AWS VPC?
-  Want to run a service on your VPC?
-  Have a few spare minutes?

.. image:: http://imgh.us/yac.png

Why yac?
--------

Because services provided by cloud providers are expensive (e.g. RDS, ElasticCache, etc.).

Yac lets you build and share comparable services, effectively crowd-sourcing their evolution.

Yac also lets you build service heirarchies (so, for example, a yac blogging service can levage a yac DB service, etc.).

Over time, durable service patterns should survive and thrive, and service providers will be able to choose from a rich menu of open, crowd-sourced, and crowd-supported services.


How does yac work?
------------------

Coding infrastructure is all about managing templates and template varariables.

YAC makes it easy to create templates and blend variables from multiple sources, including from user prompts.

The resulting infrastruce code can be easily shared with other service providers, allowing others to use and improve on your infrastructure ideas.

Yac lets you use code in your templates - this provides great power and flexibility to service designers.

Yac uses simple cli operations and infrastructure is specified in json files, making CI/CD intergration a breeze.


Quick Start
-----------

Install the cli:

    $ pip install yac

Find a service:

    $ yac service --find=confluence

Print a service:

    $ yac stack atlassian/confluence

What is yac?
------------

*  A workflow system that does for services what docker did for applications

    *  docker helped make it easy to find, run, define, and share individual applications
    *  yac does the same for services
    
*  A cli app that lets you easily find, run, define, and share service templates

    *  yac registry works just like the docker registry
    *  services are defined as templates in json
    *  services templates can be browsed, and instantiated via the yac registry

*  A happy place for service developers, cloud administrators, and service providers

What is a service?
------------------

*  An application that provides some useful function
*  An application that can be implemented using cloud infrastructure

Intruiged?
------------------

Read more at `yac stacks`_ on atlassian.net.

.. _yac stacks: https://yac-stacks.atlassian.net/wiki/display/YAC/Your+Automated+Cloud


Want to contribute?
-------------------

Repo
====

Clone from `yac on bitbucket`_

.. _yac on bitbucket: https://bitbucket.org/thomas_b_jackson/yac

Testing
=======

Get unit tests to pass

    $ python -m unittest discover yac/tests