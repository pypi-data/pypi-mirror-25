=======
ec2-ssh
=======

.. image:: https://img.shields.io/pypi/v/ec2-ssh.svg
    :target: https://pypi.python.org/pypi/ec2-ssh

.. image:: https://travis-ci.org/YPlan/ec2-ssh.svg?branch=master
    :target: https://travis-ci.org/YPlan/ec2-ssh


A pair of command line utilities for finding and SSH-ing into your Amazon EC2
instances by tag (such as 'Name').

Forked from Instagram original code by YPlan.

Installation
------------

>From pip:

.. code-block:: bash

    pip install ec2-ssh

Usage
-----

.. code-block:: bash

    # ec2-ssh

    % ec2-ssh nginx2
    # equivalent to
    # ssh ubuntu@ec2-123-45-67-89.compute-1.amazonaws.com

    % ec2-ssh root@appserver
    % ec2-ssh deploy@nginx2 sudo restart nginx

    # Specifying the user with an environment variable
    % EC2_SSH_USER=deploy ec2-ssh nginx2

    # ec2-host

    # w/o arg: prints all active instances
    % ec2-host
    ec2-123-45-67-89.compute-1.amazonaws.com
    ec2-132-45-67-89.compute-1.amazonaws.com
    ec2-231-45-67-89.compute-1.amazonaws.com

    # w/ arg
    % ec2-host backend
    ec2-132-45-67-89.compute-1.amazonaws.com
    ec2-132-45-67-90.compute-1.amazonaws.com

    # w/ tag arg too
    % ec2-host -t environment production
    ec2-132-45-67-90.compute-1.amazonaws.com
    ec2-111-45-67-90.compute-1.amazonaws.com




History
=======

Pending
-------

* Next version release notes here

1.9.0 (2017-09-08)
------------------

* Both ``ec2-host`` and ``ec2-ssh`` now only show/use instances in the
  ``running`` state.
* Use the Public IP for an instance if EC2 no Public DNS for a public instance.
  It turns out EC2 may not return the Public DNS even when a Public IP is
  assigned.

1.8.0 (2017-07-19)
------------------

* Use private IP addresses for instances that don't have public ones. Such
  instances are not guaranteed to be accessible from the current host,
  depending on networking setup, but it's better the tool let's you try it.

1.7.0 (2017-04-23)
------------------

* Rewrite to use ``setup.py``'s ``entry_points`` feature, rather than
  ``scripts``. This makes everything importable from the ``ec2_ssh`` module and
  makes ``ec2-ssh`` faster as calling the ``ec2-host`` behaviour no longer
  requires ``subprocess``.

1.6.0 (2017-04-13)
------------------

* ``ec2-ssh`` supports specifying the username with the ``-u``/``--user`` flag
  or the ``EC2_SSH_USER`` environment variable.

1.5.3 (2017-03-23)
------------------

* Acquired the PyPI name ``ec2-ssh``, moved fork back there from
  ``ec2-ssh-yplan``.

1.5.2 (2016-08-17)
------------------

* Fix Python 3 bug with subprocess output type

1.5.1 (2016-01-21)
------------------

* Pip failed to receive wheel in version 1.5.0, re-uploading

1.5.0 (2016-01-21)
------------------

* Now using ``boto3``

1.4.0 (2016-01-07)
------------------

* ``ec2-ssh`` rewritten in Python. As part of this, the automatic 'pretty
  prompt' has been removed.

1.3.0 (2016-01-06)
------------------

* Forked by YPlan
* Output from ec2-host is now in random order, allowing ec2-ssh to spread
  logins between similar instances
* Python 3 compatibility

1.2.1 (2011-11-27)
------------------
* Fix issue when ec2-host finds one offline instance with same name as an online instance

1.2 (2011-11-27)
----------------

* Merged pull requests to add region and tag support

1.1.1 (2011-11-17)
------------------

* Add line echoing host before establishing SSH connection

1.1 (2011-11-15)
----------------

* override prompt (PS1) to show tag name

1.0 (2011-09-05)
----------------

* initial release


