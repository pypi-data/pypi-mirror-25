========
zuul_get
========

Retrieves job URLs from OpenStack Zuul for a particular review number.

Installation
------------

The easiest method is to use pip:

.. code-block:: console

   pip install zuul_get


Running the script
------------------

Provide a six-digit gerrit review number as an argument to retrieve the CI job
URLs from Zuul's JSON status file:

.. code-block:: console

   $ zuul_get 356016
   +------------------------------------------------------------+---------+----------------------+
   | Jobs for 356016                                            |         |                      |
   +------------------------------------------------------------+---------+----------------------+
   | gate-openstack-ansible-security-docs-ubuntu-xenial         | Queued  |                      |
   | gate-openstack-ansible-security-linters-ubuntu-xenial      | Queued  |                      |
   | gate-openstack-ansible-security-releasenotes               | Queued  |                      |
   | gate-openstack-ansible-security-ansible-func-centos-7      | Success | https://is.gd/pUeKRT |
   | gate-openstack-ansible-security-ansible-func-ubuntu-trusty | Queued  |                      |
   | gate-openstack-ansible-security-ansible-func-ubuntu-xenial | Queued  |                      |
   +------------------------------------------------------------+---------+----------------------+

If the job is in progress, a telnet link will appear. If the job has completed,
a link to the results will be provided.

Contributing
------------

Pull requests and GitHub issues are always welcome!
