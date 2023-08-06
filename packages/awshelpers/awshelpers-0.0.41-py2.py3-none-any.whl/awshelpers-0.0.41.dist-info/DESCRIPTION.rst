==========
Awshelpers
==========

This package represents a collection of "helper" modules to increase efficiency when working
with AWS's Python SDK.

Searching though readthedocs.io is fine however having to constantly refer back to function signatures while
composing Lambda's is time consuming and repetitive.

The ``awshelpers`` package attempts to address this issue in a variety of ways.

Type Hinting
    Where ever possible and warranted proper docstrings have been added to expose data types within function
    signatures. When coupled with an IDE like Pycharm importing these commented functions into your code will allow
    for faster and more accurate composition.

Predictable Naming Conventions
    AWS has created an SDK that follows sensible naming conventions like ``get_*``, ``list_*``, ``describe_*`` etc. The
    ``awshelpers`` package follows a similar style. Since keywords like ``get``, ``list``, ``send`` can be shared across
    modules it is suggested that the various modules you may ``import`` use ``as`` keyword when importing these modules
    avoiding naming collisions.

    Below are two examples::
        >>> from awshelpers.ssm import get as ssm_get
        >>> from awshelpers.s3 import get as s3_get

Event
=====

A module for displaying Lambda event/payload data. Capable of...

- formatted dump of event data
- parsing specific AWS Services (SNS) Message payloads

To use simply do::
    >>> from awshelpers.event import dump as evt_dump
    >>> d = evt_dump.payload(event)


Simple Systems Manager
======================

A module that interacts with EC2 instances that have the SSM agent installed.
http://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html

To use simply do::
    >>> from awshelpers.ssm import get as ssm_get, list as ssm_list, send as ssm_send
    >>> command_result = ssm_send.command(['xx-xxxxxx'],'AWS-RunShellScript', 240, 'My SSM command',['ls -alh','ping -c 3 8.8.8.8'], 'us-west-2', 'ssm-command-bucket', 'service-name')

S3
====

A module that interacts with S3.

To use simply do::
    >>> from awshelpers.s3 import get as s3_get
    >>> s = s3_get.item('bucket-name','path/to/my/file.txt','/tmp/output.txt')

EC2
===

A module that interacts with EC2.

To use simply do::
    >>> from awshelpers.ec2 import describe as ec2_describe

Elastic IPs
-----------

List the elastic IPs associated to one or more instances::
    >>> ec2_describe.eip_addresses(['eni-xxxxxx','eni-yyyyyy'], 'PublicIp')

Tags
----

List the tags associated with an instance::
    >>> ec2_describe.tags([i-xxxxxxxxxxxxxxxxx])



