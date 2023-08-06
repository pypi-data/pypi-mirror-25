Cinder Authentications
===============================



.. image:: https://img.shields.io/pypi/v/cinder_auths.svg
   :target: https://pypi.python.org/pypi/cinder_auths

.. image:: https://img.shields.io/travis/akrog/cinder_auths.svg
   :target: https://travis-ci.org/akrog/cinder_auths

.. image:: https://readthedocs.org/projects/cinder-auths/badge/?version=latest
   :target: https://cinder-auths.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/cinder_auths.svg
   :target: https://pypi.python.org/pypi/cinder_auths

.. image:: https://pyup.io/repos/github/akrog/cinder_auths/shield.svg
     :target: https://pyup.io/repos/github/akrog/cinder_auths/
     :alt: Updates

.. image:: https://img.shields.io/:license-apache-blue.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0


Cinder Authentication Examples

* Free software: Apache Software License 2.0
* Documentation: https://cinder-auths.readthedocs.io.

This repository is just meant as an example of the basic mechanism of Cinder
Authentication, how we can create custom plugins, and what are the current
limitations in Cinder in this regard and how to work around them.

In this repository there are 2 examples implemented:

* Plain Passwords: Authenticate using plain passwords.
* OTP: Authenticate usingone time passwords.

Cinder, and most if not all OpenStack projects, use Paste Deployment (a system
for finding and configuring WSGI applications and servers) as well as WebOb
(WSGI request and response objects) on the API services, that is where the
authentication and authorization occurs.

This means that to create a custom Authentication mechanism we'll need to make
the API service receive the authentication parameters -user, project,
token/password- from the client and do the authentication.  Due to the nature
of the Cinder architecture all internal communications between Cinder services
are considered secure and will not perform any additional validations and the
user and project present in the request's context will be considered truthful.

The steps to create a custom authenticator is:

1- Create a filter factory (library)
2- Install the authentication library
3- Add the pipelines to Cinder's api-paste configuration
4- Configure cinder to use this newly created authentication
5- Restart the Cinder-API services


Creating a filter factory
-------------------------

This repository creates 2 simple filter factories:

- cinder_auths.plain_pwd_factory: Also accessible as
  cinder_auths.cinder_auths.BaseAuthFilter.factory
- cinder_auths.otp_factory: Also accessible as
  cinder_auths.cinder_auths.OTPAuthFilter.factory

To illustrate the different mechanisms that can be used to configure these
plugins, and not because it makes sense from an engineering perspective, we
have added 2 configuration parameters and one of them can be configure in 2
different ways.

The 2 ways we can use to pass configuration parameters are via api-paste
configuration file (/etc/cinder/api-paste.ini) and via cinder configuration
file (/etc/cinder/cinder.conf).

Of the two configuration parameters we have added the first and mandatory one
is the list of authorized users which are defined in the api-paste.ini file
under the name `passwords` in the filter.

This parameters is a list of space separated tuples in the form of
User:Project:Password.

The second configuration parameter is optional and allows us to define the
password of an admin user, since all other users will be non-admin.

This configuration option can be configured in the api-paste file using the
`admin_password` parameter or the cinder conf using the same name under the
`[DEFAULT]` section.  If both of them are defined the one in the api-paste file
takes precedence.

If this configuration option is defined, and it's not empty, the code will
automatically add an admin user in the admin project.

The clients will use the `X-Auth-Token` header to provide the user, project,
and password using the `:` separator: `user:project:password`.



Installing the library
----------------------

We can install this directly using `sudo pip install cinder_auths`.



Adding api-paste pipelines
--------------------------

We have to edit the file /etc/cinder/api-paste.ini file to add the filter we
want to use together with its configuration as well as creating a pipeline for
this authenticator on each of the different API versions we currently have.

This means that we have to add to `[composite:openstack_volume_api_v1]` one
line with `plain_pwd = cors http_proxy_to_wsgi request_id faultwrap sizelimit
osprofiler plain_pwd apiv1`, to `[composite:openstack_volume_api_v2]` the line
`plain_pwd = cors http_proxy_to_wsgi request_id faultwrap sizelimit osprofiler
plain_pwd apiv2`, and to `[composite:openstack_volume_api_v3]` the line
`plain_pwd = cors http_proxy_to_wsgi request_id faultwrap sizelimit osprofiler
plain_pwd apiv3`.  All these are a copy of the respective `noauth` pipelines
replacing noauth with `plain_pwd`.

Then we add the `plain_pwd` filter with the desired configuration::

  [filter:plain_pwd]
  paste.filter_factory = cinder_auths:plain_pwd_factory
  passwords = user1:project1:password1 user2:project2:password2
  admin_password = geguileo



Cinder configuration
--------------------

Here we need to configure the `auth_strategy` we want Cinder to use under the
`[DEFAULT]` group.  This configuration option defaults to `keystone`, so we'll
have to set it to `plain_pwd` which is the pipeline name we have added, the
name of the filter is irrelevant even if in this case we have used the same
name.

We can also add the `admin_password` option under `[DEFAULT]` if we didn't do
it in the api-paste configuration file.

And here's were we find a problem with the existing Cinder code, because right
now it only accepts 2 names `keystone` and `noauth`, so we can't really set
`auth_strategy = palin_pwd` without changing the code.

So the solutions we have right now, until we change Cinder, are:

- Replace the `noauth` filter with our `plain_pwd` configuration and configure
  cinder with `auth_strategy = noauth`.
- Manually change the cinder code in `/usr/lib/python2.7/site-packages/cinder/
  common/config.py` and replace `choices=['noauth', 'keystone'],` with
  `choices=['noauth', 'keystone', 'plain_pwd', 'otp'],`.



Testing it
----------

Once we have restarted the Cinder-API service we can just list volumes with::

  $ curl -i http://192.168.121.165:8776/v3/admin/volumes/detail -H "Accept: application/json" -H "X-Auth-Token: admin:admin:geguileo"

The URL may be different depending on which version of openstack you are using.
