================
Boto3 Extensions
================

Overview
--------
This module adds more resource files to the Boto3 library and includes some functionality enhancements.

Quick Start
-----------
First, install the library:

.. code-block:: sh

    $ pip install boto3_extensions

Follow the Boto3 docs on setting up your region and credentials (https://github.com/boto/boto3).

Then, from a Python interpreter:

.. code-block:: python

    >>> import boto3
    >>> import boto3_extensions
    >>> r = boto3.resource('cloudtrail', region_name='us-east-1')
    >>> for trail in r.trails.all():
          print(trail.trail_arn)

Resource Files
--------------
The following resource files are **added** to the Boto3 library.

  * acm
  * autoscaling
  * cloudfront
  * cloudtrail
  * cur
  * datapipeline
  * directconnect
  * elasticache
  * elb
  * elbv2
  * emr
  * glue
  * health
  * kinesis
  * lambda
  * rds
  * redshift
  * route53
  * support

The following resource files are **updated** in the Boto3 library.

  * dynamodb
  * ec2
  * iam
  * s3


RefreshableAssumeRoleProvider
-----------------------------
If your code needs to AssumeRole into another role before performing actions against the AWS API (be it in the same or another AWS account), you run the risk that the credentials you are using expire during their use. You can either add code to your application to constantly check the credential expiry time or using this extension offload the credential refresh to boto3 itself. By using the ConnectionManager in boto3_extensions not only will it automattically assumeRole when the credentials get below 15 mins left, but it will also cache the credentials. This means that if your application is calling boto3 to get credentials for another role more than once the ConnectionManager will cache the first call and then hand out the same session for the subsequent calls. 

.. code-block:: python

    >>> role_arn = 'arn:aws:iam::1234567890:role/test-role'
    >>> role_session_name = 'test'
    >>> connections = boto3_extensions.ConnectionManager(region_name='us-east-1')
    >>> session = connections.get_session(role_arn=role_arn, role_session_name=role_session_name)
    >>>
    >>> r = session.resource('cloudtrail', region_name='us-east-1')
    >>> for trail in r.trails.all():
    >>>     print(trail.trail_arn)


ARN Patch
---------
It would be nice to have a consistent way to get the ARN of resources. The ARN patch feature of boto3_extensions allows you to get the arn from resources via an arn attribute. 

.. code-block:: python

    >>> import boto3
    >>> import boto3_extensions
    >>> from imp import reload
    >>> boto3_extensions.arn_patch_boto3()
    >>> reload(boto3)
    >>> 
    >>> r = boto3.resource('rds', region_name='us-east-1')
    >>> for db in r.db_instances.all():
    >>>   print(db.arn)


Getting Help
------------
Please raise issue ticket inside our Bitbucket repo: https://bitbucket.org/atlassian/boto3_extensions/issues
