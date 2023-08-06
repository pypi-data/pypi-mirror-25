###########
Puppetboard
###########

.. image:: https://travis-ci.org/voxpupuli/puppetboard.svg?branch=master
   :target:  https://travis-ci.org/voxpupuli/puppetboard

.. image:: https://coveralls.io/repos/github/voxpupuli/puppetboard/badge.svg?branch=master
   :target:  https://coveralls.io/github/voxpupuli/puppetboard?branch=master

Puppetboard is a web interface to `PuppetDB`_ aiming to replace the reporting
functionality of `Puppet Dashboard`_.

Puppetboard relies on the `pypuppetdb`_ library to fetch data from PuppetDB
and is built with the help of the `Flask`_ microframework.

As of version 0.1.0 and higher, Puppetboard **requires** PuppetDB 3.

.. _pypuppetdb: https://pypi.python.org/pypi/pypuppetdb
.. _PuppetDB: http://docs.puppetlabs.com/puppetdb/latest/index.html
.. _Puppet Dashboard: http://docs.puppetlabs.com/dashboard/
.. _Flask: http://flask.pocoo.org
.. _FlaskSession: http://flask.pocoo.org/docs/0.11/quickstart/#sessions

At the current time of writing, Puppetboard supports the following Python versions:
    * Python 2.6
    * Python 2.7

.. image:: screenshots/overview.png
   :alt: View of a node
   :width: 1024
   :height: 700
   :align: center

.. contents::

Word of caution
===============

Puppetboard is very, very young but it works fairly well.

That being said a lot of the code is very experimental, just trying
to figure out what works and what not, what we need to do different
and what features we need on the PuppetDB side of things.

As such you should be at least comfortable handling a few errors
this might throw at you.

Installation
============

Puppetboard is now packaged and available on PyPi.

Production
----------

Puppet module
^^^^^^^^^^^^^
There is a `Puppet module`_ by `Spencer Krum`_ that takes care of installing Puppetboard for you.

You can install it with:

    puppet module install puppet-puppetboard

.. _Spencer Krum: https://github.com/nibalizer
.. _Puppet module: https://forge.puppetlabs.com/puppet/puppetboard

Manual
^^^^^^

To install it simply issue the following command:

.. code-block:: bash

   $ pip install puppetboard

This will install Puppetboard and take care of the dependencies. If you
do this Puppetboard will be installed in the so called site-packages or
dist-packages of your Python distribution.

The complete path on Debian and Ubuntu systems would be ``/usr/local/lib/pythonX.Y/lib/dist-packages/puppetboard`` and on Fedora would be ``/usr/lib/pythonX.Y/site-packages/puppetboard``

where X and Y are replaced by your major and minor python versions.

You will need this path in order to configure your HTTPD and WSGI-capable
application server.

Packages
^^^^^^^^
Native packages for your operating system will be provided in the near future.

+-------------------+-----------+--------------------------------------------+
| OS                | Status    |                                            |
+===================+===========+============================================+
| Debian 6/Squeeze  | planned   | Requires Backports                         |
+-------------------+-----------+--------------------------------------------+
| Debian 7/Wheezy   | planned   |                                            |
+-------------------+-----------+--------------------------------------------+
| Ubuntu 13.04      | planned   |                                            |
+-------------------+-----------+--------------------------------------------+
| Ubuntu 13.10      | planned   |                                            |
+-------------------+-----------+--------------------------------------------+
| CentOS/RHEL 5     | n/a       | Python 2.4                                 |
+-------------------+-----------+--------------------------------------------+
| CentOS/RHEL 6     | planned   |                                            |
+-------------------+-----------+--------------------------------------------+
| `OpenSuSE 12/13`_ | available | Maintained on `OpenSuSE Build Service`_    |
+-------------------+-----------+--------------------------------------------+
| `SuSE LE 11 SP3`_ | available | Maintained on `OpenSuSE Build Service`_    |
+-------------------+-----------+--------------------------------------------+
| `ArchLinux`_      | available | Maintained by `Tim Meusel`_                |
+-------------------+-----------+--------------------------------------------+
| `OpenBSD`_        | available | Maintained by `Sebastian Reitenbach`_      |
+-------------------+-----------+--------------------------------------------+

.. _ArchLinux: https://aur.archlinux.org/packages/python2-puppetboard/
.. _Tim Meusel: https://github.com/bastelfreak
.. _Sebastian Reitenbach: https://github.com/buzzdeee
.. _OpenBSD: http://www.openbsd.org/cgi-bin/cvsweb/ports/www/puppetboard/
.. _OpenSuSE Build Service: https://build.opensuse.org/package/show/systemsmanagement:puppet/python-puppetboard
.. _OpenSuSE 12/13: https://build.opensuse.org/package/show/systemsmanagement:puppet/python-puppetboard
.. _SuSE LE 11 SP3: https://build.opensuse.org/package/show/systemsmanagement:puppet/python-puppetboard

Docker Images
^^^^^^^^^^^^^

A `Dockerfile`_ was added to the source-code in the 0.2.0 release. An officially
image is planned for the 0.2.x series.

.. _Dockerfile: https://github.com/voxpupuli/puppetboard/blob/master/Dockerfile

Usage:
.. code-block:: bash
  $ docker build -t puppetboard .
  $ docker run -it -p 9080:80 -v /etc/puppetlabs/puppet/ssl:/etc/puppetlabs/puppet/ssl \
    -e PUPPETDB_HOST=<hostname> \
    -e PUPPETDB_PORT=8081 \
    -e PUPPETDB_SSL_VERIFY=/etc/puppetlabs/puppetdb/ssl/ca.pem \
    -e PUPPETDB_KEY=/etc/puppetlabs/puppetdb/ssl/private.pem \
    -e PUPPETDB_CERT=/etc/puppetlabs/puppetdb/ssl/public.pem \
    -e INVENTORY_FACTS='Hostname,fqdn, IP Address,ipaddress' \
    -e ENABLE_CATALOG=true \
    -e GRAPH_FACTS='architecture,puppetversion,osfamily' \
    puppetboard

Development
-----------

If you wish to hack on Puppetboard you should fork/clone the Github repository
and then install the requirements through:

.. code-block:: bash

   $ pip install -r requirements-test.txt

You're advised to do this inside a virtualenv specifically created to work on
Puppetboard as to not pollute your global Python installation.

Configuration
=============
The following instructions will help you configure Puppetboard and your HTTPD.

Puppet
------
Puppetboard is built completely around PuppetDB which means your environment
needs to be configured `to do that`_.

In order to get the reports to show up in Puppetboard you need to configure
your environment to store those reports in PuppetDB. Have a look at
`the documentation`_ about this, specifically the *Enabling report storage*
section.

.. _to do that: https://docs.puppetlabs.com/puppetdb/latest/connect_puppet_master.html#step-2-edit-config-files
.. _the documentation: https://docs.puppetlabs.com/puppetdb/latest/connect_puppet_master.html#edit-puppetconf

Settings
--------
Puppetboard will look for a file pointed at by the ``PUPPETBOARD_SETTINGS``
environment variable. The file has to be identical to ``default_settings.py``
but should only override the settings you need changed.

You can grab a copy of ``default_settings.py`` from the path where pip
installed Puppetboard to or by looking in the source checkout.

If you run PuppetDB and Puppetboard on the same machine the default settings
provided will be enough to get you started and you won't need a custom
settings file.

Assuming your webserver and PuppetDB machine are not identical you will at
least have to change the following settings:

* ``PUPPETDB_HOST``
* ``PUPPETDB_PORT``

By default PuppetDB requires SSL to be used when a non-local client wants to
connect. Therefor you'll also have to supply the following settings:

* ``PUPPETDB_SSL_VERIFY = /path/to/ca/keyfile.pem``
* ``PUPPETDB_KEY = /path/to/private/keyfile.pem``
* ``PUPPETDB_CERT = /path/to/public/keyfile.crt``

For information about how to generate the correct keys please refer to the
`pypuppetdb documentation`_.

Other settings that might be interesting in no particular order:

* ``SECRET_KEY``: Refer to `Flask documentation`_, section sessions: How to
  generate good secret keys, to set the value. Defaults to a random 24-char
  string generated by os.random(24)
* ``PUPPETDB_TIMEOUT``: Defaults to 20 seconds but you might need to increase
  this value. It depends on how big the results are when querying PuppetDB.
  This behaviour will change in a future release when pagination will be
  introduced.
* ``UNRESPONSIVE_HOURS``: The amount of hours since the last check-in after
  which a node is considered unresponsive.
* ``LOGLEVEL``: A string representing the loglevel. It defaults to ``'info'``
  but can be changed to ``'warning'`` or ``'critical'`` for less verbose
  logging or ``'debug'`` for more information.
* ``ENABLE_QUERY``: Defaults to ``True`` causing a Query tab to show up in the
  web interface allowing users to write and execute arbitrary queries against
  a set of endpoints in PuppetDB. Change this to ``False`` to disable this.
* ``GRAPH_TYPE```: Specify the type of graph to display.   Default is
  pie, other good option is donut.   Other choices can be found here:
  `_C3JS_documentation`
* ``GRAPH_FACTS``: A list of fact names to tell PuppetBoard to generate a
  pie-chart on the fact page. With some fact values being unique per node,
  like ipaddress, uuid, and serial number, as well as structured facts it was
  no longer feasible to generate a graph for everything.
* ``INVENTORY_FACTS``: A list of tuples that serve as the column header and
  the fact name to search for to create the inventory page. If a fact is not
  found for a node then ``undef`` is printed.
* ``ENABLE_CATALOG``: If set to ``True`` allows the user to view a node's
  latest catalog. This includes all managed resources, their file-system
  locations and their relationships, if available. Defaults to ``False``.
* ``REFRESH_RATE``: Defaults to ``30`` the number of seconds to wait until
  the index page is automatically refreshed.
* ``DEFAULT_ENVIRONMENT``: Defaults to ``'production'``, as the name
  suggests, load all information filtered by this environment value.
* ``REPORTS_COUNT``: Defaults to ``10`` the limit of the number of reports
  to load on the node or any reports page.
* ``OFFLINE_MODE``: If set to ``True`` load static assets (jquery,
  semantic-ui, etc) from the local web server instead of a CDN.
  Defaults to ``False``.
* ``DAILY_REPORTS_CHART_ENABLED``: Enable the use of daily chart graphs when
  looking at dashboard and node view.
* ``DAILY_REPORTS_CHART_DAYS``: Number of days to show history for on the daily
  report graphs.
* ``DISPLAYED_METRICS``: Metrics to show when displying node summary. Example:
  ``'resources.total'``, ``'events.noop'``.
* ``TABLE_COUNT_SELECTOR``: Configure the dropdown to limit number of hosts to
  show per page.
* ``LITTLE_TABLE_COUNT``: Default number of reports to show when when looking at a node.
* ``NORMAL_TABLE_COUNT``: Default number of nodes to show when displaying reports
  and catalog nodes.
* ``LOCALISE_TIMESTAMP``: Normalize time based on localserver time.
* ``DEV_LISTEN_HOST``: For use with `dev.py` for development.  Default is localhost
* ``DEV_LISTEN_PORT``: For use with `dev.py` for development.  Default is 5000


.. _pypuppetdb documentation: http://pypuppetdb.readthedocs.org/en/v0.1.0/quickstart.html#ssl
.. _Flask documentation: http://flask.pocoo.org/docs/0.10/quickstart/#sessions
.. _C3JS_documentation:  http://c3js.org/examples.html#chart

Puppet Enterprise
-----------------

Puppet Enterprise maintains a certificate white-list for which certificates
are allowed to access data from PuppetDB. This whitelist is maintained in
``/etc/puppetlabs/puppetdb/certificate-whitelist`` and you have to add the
certificate name to that file.

Afterwards you'll need to restart ``pe-puppetdb`` and you should be able to
query PuppetDB freely now.

Development
-----------

You can run it in development mode by simply executing:

.. code-block:: bash

   $ python dev.py

Use ``PUPPETBOARD_SETTINGS`` to change the different settings or patch
``default_settings.py`` directly. Take care not to include your local changes on
that file when submitting patches for Puppetboard. Place a settings.py file
inside the base directory of the git repository that will be used, if the
environment variable is not set.

Production
----------
To run Puppetboard in production we provide instructions for the following
scenarios:

* Apache + mod_wsgi
* Apache + mod_passenger
* nginx + uwsgi
* nginx + gunicorn

If you deploy Puppetboard through a different setup we'd welcome a pull
request that adds the instructions to this section.

Installation On Linux Distros
^^^^^^^^^^^^^^^^^^^^^^^^

`Debian Jessie Install`_.

.. _Debian Jessie Install: docs/Debian-Jessie.md


Apache + mod_wsgi
^^^^^^^^^^^^^^^^^

First we need to create the necessary directories:

.. code-block:: bash

   $ mkdir -p /var/www/html/puppetboard

Copy Puppetboard's ``default_settings.py`` to the newly created puppetboard
directory and name the file ``settings.py``. This file will be available
at the path Puppetboard was installed, for example:
``/usr/local/lib/pythonX.Y/lib/dist-packages/puppetboard/default_settings.py``.

Change the settings that need changing to match your environment and delete
or comment with a ``#`` the rest of the entries.

If you don't need to change any settings you can skip the creation of the
``settings.py`` file entirely.

Now create a ``wsgi.py`` with the following content in the newly created
puppetboard directory:

.. code-block:: python

    from __future__ import absolute_import
    import os

    # Needed if a settings.py file exists
    os.environ['PUPPETBOARD_SETTINGS'] = '/var/www/html/puppetboard/settings.py'
    from puppetboard.app import app as application

Make sure this file is readable by the user the webserver runs as.

Flask requires a static secret_key, see `FlaskSession`_, in order to protect
itself from CSRF exploits.  The default secret_key in ``default_settings.py``
generates a random 24 character string, however this string is re-generated
on each request under httpd >= 2.4.

To generate your own secret_key create a python script with the following content
and run it once:

.. code-block:: python

    import os
    os.urandom(24)
    '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

Copy the output and add the following to your ``wsgi.py`` file:

.. code-block:: python

   application.secret_key = '<your secret key>'

The last thing we need to do is configure Apache.

Here is a sample configuration for Debian and Ubuntu:

.. code-block:: apache

    <VirtualHost *:80>
        ServerName puppetboard.example.tld
        WSGIDaemonProcess puppetboard user=www-data group=www-data threads=5
        WSGIScriptAlias / /var/www/html/puppetboard/wsgi.py
        ErrorLog /var/log/apache2/puppetboard.error.log
        CustomLog /var/log/apache2/puppetboard.access.log combined

        Alias /static /usr/local/lib/pythonX.Y/dist-packages/puppetboard/static
        <Directory /usr/local/lib/pythonX.X/dist-packages/puppetboard/static>
            Satisfy Any
            Allow from all
        </Directory>

        <Directory /usr/local/lib/pythonX.Y/dist-packages/puppetboard>
            WSGIProcessGroup puppetboard
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Here is a sample configuration for Fedora:

.. code-block:: apache

    <VirtualHost *:80>
        ServerName puppetboard.example.tld
        WSGIDaemonProcess puppetboard user=apache group=apache threads=5
        WSGIScriptAlias / /var/www/html/puppetboard/wsgi.py
        ErrorLog logs/puppetboard-error_log
        CustomLog logs/puppetboard-access_log combined

        Alias /static /usr/lib/pythonX.Y/site-packages/puppetboard/static
        <Directory /usr/lib/python2.X/site-packages/puppetboard/static>
            Satisfy Any
            Allow from all
        </Directory>

        <Directory /usr/lib/pythonX.Y/site-packages/puppetboard>
            WSGIProcessGroup puppetboard
            WSGIApplicationGroup %{GLOBAL}
            Require all granted
        </Directory>
    </VirtualHost>


Note the directory path, it's the path to where pip installed Puppetboard; X.Y
must be replaced with your python version. We also alias the ``/static`` path
so that Apache will serve the static files like the included CSS and Javascript.

Apache + mod_passenger
^^^^^^^^^^^^^^^^^^^^^^

It is possible to run Python applications through Passenger. Passenger has
supported this since version 3 but it's considered experimental. Since the
release of Passenger 4 it's a 'core' feature of the product.

Performance wise it also leaves something to be desired compared to the
mod_wsgi powered solution. Application start up is noticeably slower and
loading pages takes a fraction longer.

First we need to create the necessary directories:

.. code-block:: bash

   $ mkdir -p /var/www/puppetboard/{tmp,public}

Copy Puppetboard's ``default_settings.py`` to the newly created puppetboard
directory and name the file ``settings.py``. This file will be available
at the path Puppetboard was installed, for example:
``/usr/local/lib/pythonX.Y/lib/dist-packages/puppetboard/default_settings.py``.

Change the settings that need changing to match your environment and delete
or comment with a ``#`` the rest of the entries.

If you don't need to change any settings you can skip the creation of the
``settings.py`` file entirely.

Now create a ``passenger_wsgi.py`` with the following content in the newly
created puppetboard directory:

.. code-block:: python

    from __future__ import absolute_import
    import os
    import logging

    logging.basicConfig(filename='/path/to/file/for/logging', level=logging.INFO)

    # Needed if a settings.py file exists
    os.environ['PUPPETBOARD_SETTINGS'] = '/var/www/puppetboard/settings.py'

    try:
        from puppetboard.app import app as application
    except Exception, inst:
        logging.exception("Error: %s", str(type(inst)))

Unfortunately due to the way Passenger works we also need to configure logging
inside ``passenger_wsgi.py`` else application start up issues won't be logged.

This means that even though ``LOGLEVEL`` might be set in your ``settings.py``
this setting will take precedence over it.

Now the only thing left to do is configure Apache:

.. code-block:: apache

   <VirtualHost *:80>
       ServerName puppetboard.example.tld
       DocumentRoot /var/www/puppetboard/public
       ErrorLog /var/log/apache2/puppetboard.error.log
       CustomLog /var/log/apache2/puppetboard.access.log combined

       RackAutoDetect On
       Alias /static /usr/local/lib/pythonX.Y/dist-packages/puppetboard/static
   </VirtualHost>

Note the ``/static`` alias path, it's the path to where pip installed
Puppetboard. This is needed so that Apache will serve the static files like
the included CSS and Javascript.

nginx + uwsgi
^^^^^^^^^^^^^
A common Python deployment scenario is to use the uwsgi application server
(which can also serve rails/rack, PHP, Perl and other applications) and proxy
to it through something like nginx or perhaps even HAProxy.

uwsgi has a feature that every instance can run as its own user. In this
example we'll use the ``www-data`` user but you can create a separate user
solely for running Puppetboard and use that instead.

First we need to create the necessary directories:

.. code-block:: bash

   $ mkdir -p /var/www/puppetboard

Copy Puppetboard's ``default_settings.py`` to the newly created puppetboard
directory and name the file ``settings.py``. This file will be available
at the path Puppetboard was installed, for example:
``/usr/local/lib/pythonX.Y/lib/dist-packages/puppetboard/default_settings.py``.

Change the settings that need changing to match your environment and delete
or comment with a ``#`` the rest of the entries.

If you don't need to change any settings you can skip the creation of the
``settings.py`` file entirely.

Now create a ``wsgi.py`` with the following content in the newly created
puppetboard directory:

.. code-block:: python

    from __future__ import absolute_import
    import os

    # Needed if a settings.py file exists
    os.environ['PUPPETBOARD_SETTINGS'] = '/var/www/puppetboard/settings.py'
    from puppetboard.app import app as application

Make sure this file is owned by the user and group the uwsgi instance will run
as.

Now we need to start uwsgi:

.. code-block:: bash

   $ uwsgi --socket :9090 --wsgi-file /var/www/puppetboard/wsgi.py

Feel free to change the port to something other than ``9090``.

The last thing we need to do is configure nginx to proxy the requests:

.. code-block:: nginx

   upstream puppetboard {
       server 127.0.0.1:9090;
   }

   server {
       listen      80;
       server_name puppetboard.example.tld;
       charset     utf-8;

       location /static {
           alias /usr/local/lib/pythonX.Y/dist-packages/puppetboard/static;
       }

       location / {
           uwsgi_pass puppetboard;
           include    /path/to/uwsgi_params/probably/etc/nginx/uwsgi_params;
       }
   }

If all went well you should now be able to access to Puppetboard. Note the
``/static`` location block to make nginx serve static files like the included
CSS and Javascript.

Because nginx natively supports the uwsgi protocol we use ``uwsgi_pass``
instead of the traditional ``proxy_pass``.

nginx + gunicorn
^^^^^^^^^^^^^
You can use gunicorn instead of uwsgi if you prefer, the process doesn't
differ too much. As we can't use ``uwsgi_pass`` with gunicorn, the nginx configuration file is going to differ a bit:

.. code-block:: nginx

    server {
        listen      80;
        server_name puppetboard.example.tld;
        charset     utf-8;

        location /static {
            alias /usr/local/lib/pythonX.Y/dist-packages/puppetboard/static;
        }

        location / {
            add_header Access-Control-Allow-Origin *;
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_connect_timeout 10;
            proxy_read_timeout 10;
            proxy_pass http://127.0.0.1:9090;
        }
    }

Now, for running it with gunicorn:

.. code-block:: bash

   $ cd /usr/local/lib/pythonX.Y/dist-packages/puppetboard
   $ gunicorn -b 127.0.0.1:9090 puppetboard.app:app

As we may want to serve in the background, and we need ``PUPPETBOARD_SETTINGS`` as an environment variable, is recommendable to run this under supervisor. An example supervisor config with basic settings is the following:

.. code-block:: ini

    [program:puppetboard]
    command=gunicorn -b 127.0.0.1:9090 puppetboard.app:app
    user=www-data
    stdout_logfile=/var/log/supervisor/puppetboard/puppetboard.out
    stderr_logfile=/var/log/supervisor/puppetboard/puppetboard.err
    environment=PUPPETBOARD_SETTINGS="/var/www/puppetboard/settings.py"


For newer systems with systemd (for example CentOS7), you can use the following service file (``/usr/lib/systemd/system/gunicorn@.service``):

.. code-block:: ini

    [Unit]
    Description=gunicorn daemon for %i
    After=network.target

    [Service]
    ExecStart=/usr/bin/gunicorn --config /etc/sysconfig/gunicorn/%i.conf %i
    ExecReload=/bin/kill -s HUP $MAINPID
    PrivateTmp=true
    User=gunicorn
    Group=gunicorn

And the corresponding gunicorn config (``/etc/sysconfig/gunicorn/puppetboard.app\:app.conf``):

.. code-block:: ini

    import multiprocessing

    bind    = '127.0.0.1:9090'
    workers = multiprocessing.cpu_count() * 2 + 1
    chdir   = '/usr/lib/python2.7/site-packages/puppetboard'
    raw_env = ['PUPPETBOARD_SETTINGS=/var/www/puppetboard/settings.py', 'http_proxy=']

Security
--------

If you wish to make users authenticate before getting access to Puppetboard
you can use one of the following configuration snippets.

Apache
^^^^^^

Inside the ``VirtualHost``:

.. code-block:: apache

    <Location "/">
        AuthType Basic
        AuthName "Puppetboard"
        Require valid-user
        AuthBasicProvider file
        AuthUserFile /path/to/a/file.htpasswd
    </Location>

nginx
^^^^^

Inside the ``location / {}`` block that has the ``uwsgi_pass`` directive:

.. code-block:: nginx

    auth_basic "Puppetboard";
    auth_basic_user_file /path/to/a/file.htpasswd;

Getting Help
============
This project is still very new so it's not inconceivable you'll run into
issues.

For bug reports you can file an `issue`_. If you need help with something
feel free to hit up the maintainers by e-mail or on IRC. They can usually
be found on `IRCnet`_ and `Freenode`_ and idles in #puppetboard.

There's now also the #puppetboard channel on `Freenode`_ where we hang out
and answer questions related to pypuppetdb and Puppetboard.

There is also a `GoogleGroup`_ to exchange questions and discussions. Please
note that this group contains discussions of other Puppet Community projects.

.. _issue: https://github.com/voxpupuli/puppetboard/issues
.. _IRCnet: http://www.ircnet.org
.. _Freenode: http://freenode.net
.. _GoogleGroup: https://groups.google.com/forum/?hl=en#!forum/puppet-community

Third party
===========
Some people have already started building things with and around Puppetboard.

`Hunter Haugen`_ has provided a Vagrant setup:

* https://github.com/hunner/puppetboard-vagrant

.. _Hunter Haugen: https://github.com/hunner

Packages
--------
* An OpenBSD port is being maintained by `Sebastian Reitenbach`_ and can be viewed `here <http://www.openbsd.org/cgi-bin/cvsweb/ports/www/puppetboard/>`_.

* A Docker image is being maintained by `Julien K.`_ and can be viewed `here <https://registry.hub.docker.com/u/kassis/puppetboard/>`_.

.. _Sebastian Reitenbach: https://github.com/buzzdeee
.. _Julien K.: https://github.com/juliengk

Contributing
============
We welcome contributions to this project. However, there are a few ground
rules contributors should be aware of.

License
-------
This project is licensed under the Apache v2.0 License. As such, your
contributions, once accepted, are automatically covered by this license.

Commit messages
---------------
Write decent commit messages. Don't use swear words and refrain from
uninformative commit messages as 'fixed typo'.

The preferred format of a commit message:

::

    docs/quickstart: Fixed a typo in the Nodes section.

    If needed, elaborate further on this commit. Feel free to write a
    complete blog post here if that helps us understand what this is
    all about.

    Fixes #4 and resolves #2.

If you'd like a more elaborate guide on how to write and format your commit
messages have a look at this post by `Tim Pope`_.

.. _Tim Pope: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

Examples
========

`vagrant-puppetboard`_

.. _vagrant-puppetboard: https://github.com/visibilityspots/vagrant-puppet/tree/puppetboard

A vagrant project to show off the puppetboard functionallity using the puppetboard puppet module on a puppetserver with puppetdb.

Screenshots
===========

.. image:: screenshots/overview.png
   :alt: Overview / Index / Homepage
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/nodes.png
   :alt: Nodes view, all active nodes
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/node.png
   :alt: Single node page / overview
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/report.png
   :alt: Report view
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/facts.png
   :alt: Facts view
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/fact.png
   :alt: Single fact, with graphs
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/fact_value.png
   :alt: All nodes that have this fact with that value
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/metrics.png
   :alt: Metrics view
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/metric.png
   :alt: Single metric
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/query.png
   :alt: Query view
   :width: 1024
   :height: 700
   :align: center

.. image:: screenshots/broken.png
   :alt: Error page
   :width: 1024
   :height: 700
   :align: center

#########
Changelog
#########

This is the changelog for Puppetboard.

0.3.0
=====

* Core UI Reowrk
* Update to pypuppetdb 0.3.3
* Fix sorty on data for index
* Update debian documentation
* Offline mode fix
* Fix fact attrbitue error on paths
* Enhanced testing
* Radiator CSS uses same coloring
* Markdown in config version
* Update Flask
* Cleanup requirements.txt
* Update package maintainer for OpenBSD

0.2.1
=====

* Daily Charts
* Fixed missing javascript files on radiator view.
* TravisCI and Coveralls integration.
* Fixed app crash in catalog view.
* Upgrade pypuppetdb to 0.3.2
* Enhanced queries for Node and Report (#271)
* Optimize Inventory Code.
* Use certname instead of hostname to identify nodes when applicable.
* Add environment filter for facts.
* Update cs.js to 0.4.11
* Fix radiator column alignment
* Security checks with bandit
* Dockerfile now uses gunicorn and environment variables for
  configuration.
* Handle division by zero errors.
* Implement new Jquery Datatables.
* JSON output for radiator. * Move javascript to head tag.
* Optimize reports and node page queries.
* Fix all environments for PuppetDB 3.2
* Fact graph chart now configurable.
* Support for Flask 0.12 and Jinja2 2.9
* Fix misreporting noops as changes.

0.2.0
=====

* Full support for PuppetDB 4.x
* Updating Semantic UI to 2.1.8
* Updating Flask-WTF requirements to 0.12
* Updating WTForms to 2.x
* Restored CSRF protection on the Query Tab form
* Updating Pypuppetdb requirement to 0.3.x
* New configuration option OVERVIEW_FILTER allows users to add custom
  PuppetDB query clauses to include/exclude nodes displayed on the
  index page
* Adding Radiator view similar to what is available in Puppet Dashboard
* Adding a drop-down list in the Reports tab to configure the number of
  reports displayed
* Removing unneeded report_latest() endpoint. This endpoint was deprecated
  with the addition of the `latest_report_hash` field in the Nodes
  PuppetDB endpoint
* Enhancing Report pagination
* Using the OOP Query Builder available in Pypuppetdb 0.3.x
* Allowing PQL queries in the Query Tab
* Fixing double url-quoting bug on Metric endpodint calls
* Adding a Boolean field to the Query form to prettyprint responses from
  PuppetDB
* Fixing corner-case where empty environments would trigger a ZeroDivisionError
  due to the Number of Nodes divided by the Number of Resources calculation
* Adding additional logging in `utils.py`

0.1.2
====

* Add configuration option to set the default environment with new
  configuration option DEFAULT_ENVIRONMENT, defaults to 'production'.
* Loading all available environments with every page load.
* Adding an "All Environments" item to the Environments dropdown to
  remove all environment filters on PuppetDB data.
* Updating README.rst to update links and describe new configuration
  options.
* Fixing Query form submission problem by disabling CSRF protection.
  Needs to be re-implemented.
* Updating the pypuppetdb requirement to >= 0.2.1, using information
  available in PuppetDB 3.2 and higher
** latest_report_hash and latest_report_status fields from the Nodes
   endpoint, this effectively deprecates the report_latest() function
** code_id from the Catalogs endpoint (current unused)
* Adding a automatic refresh on the overview page to reload the page
  every X number of seconds, defaults to 30. This is configurable
  with the configuration option REFRESH_RATE
* Fixing the table alignment in the catalog_compare() page by switching
  to fixed tables from basic tables.
* Using colors similar to Puppet Dashboard and Foreman for the status
  counts sections

0.1.1
====

* Fix bug where the reports template was not generating the report links
  with the right environment

0.1.0
====

* Requires pypuppetdb >= 0.2.0
* Drop support for PuppetDB 2 and earlier
* Full support for PuppetDB 3.x
* The first directory location is now a Puppet environment which is filtered
  on all supported queries. Users can browse different environments with a
  select field in the top NavBar
* Using limit, order_by and offset parameters adding pagaination on the Reports
  page (available in the NavBar). Functionality is available to pages that
  accept a page attribute.
* The report page now directly queries pypuppetdb to match the report_id
  value with the report hash or configuration_version fields.
* Catching and aborting with a 404 if the report and report_latest function
  queries do not return a generator object.
* Adding a Catalogs page (similar to the Nodes page) with a form to compare
  one node's catalog information with that of another node.
* Updating the Query Endpoints for the Query page.
* Adding to ``templates/_macros.html`` status_counts that shows node/report
  status information, like what is avaiable on the index and nodes pages,
  available to the reports pages and tables also.
* Showing report logs and metrics in the report page.
* Removing ``limit_reports`` from ``utils.py`` because this helper function
  has been replaced by the limit PuppetDB paging function.

**Known Issues**

* fact_value pages rendered from JSON valued facts return no results. A more
  sophisticated API is required to make use of JSON valued facts (through the
  factsets, fact-paths and/or fact-contents endpoints for example)

0.0.5
=====

* Now requires WTForms versions less than 2.0
* Adding a Flask development server in ``dev.py``.
* Adding CSRF protection VIA the flask_wtf CsrfProtect object.
* Allowing users to configure the report limit on pages where reports are
  listed with the LIMIT_REPORTS configuration option.
* Adding an inventory page to users to be able to see all available nodes
  and a configure lists of facts to display VIA the INVENTORY_FACTS
  configuration option.
* Adding a page to view a node's catalog information if enabled, disabled
  by default. Can be changed with the ENABLE_CATALOG configuration attribute.
* New configuration option GRAPH_FACTS allows the user to choose which graphs
  will generate pie on the fact pages.
* Replacing Chart.js with c3.js and d3.js.
* Adding Semantic UI 0.16.1 and removing unused bootstrap styles.
* Adding an OFFLINE_MODE configuration option to load local assets or from a
  CDN service. This is useful in environments without internet access.

0.0.4
=====

* Fix the sorting of the different tables containing facts.
* Fix the license in our ``setup.py``. The license shouldn't be longer than
  200 characters. We were including the full license tripping up tools like
  bdist_rpm.

0.0.3
=====
This release introduces a few big changes. The most obvious one is the
revamped Overview page which has received significant love. Most of the work
was done by Julius Härtl. The Nodes tab has been given a slight face-lift
too.

Other changes:

* This release depends on the new pypuppetdb 0.1.0. Because of this the SSL
  configuration options have been changed:

  * ``PUPPETDB_SSL`` is gone and replaced by ``PUPPETDB_SSL_VERIFY`` which
    now defaults to ``True``. This only affects connections to PuppetDB that
    happen over SSL.
  * SSL is automatically enabled if both ``PUPPETDB_CERT`` and
    ``PUPPETDB_KEY`` are provided.

* Display of deeply nested metrics and query results have been fixed.
* Average resources per node metric is now displayed as a natural number.
* A link back to the node has been added to the reports.
* A few issues with reports have been fixed.
* A new setting called ``UNRESPONSIVE_HOURS`` has been added which denotes
  the amount of hours after which Puppetboard will display the node as
  unreported if it hasn't checked in. We default to ``2`` hours.
* The event message can now be viewed by clicking on the event.

Puppetboard is now neatly packaged up and available on PyPi. This should
significantly help reduce the convoluted installation instructions people had
to follow.

Updated installation instructions have been added on how to install from PyPi
and how to configure your HTTPD.

0.0.2
=====
In this release we've introduced a few new things. First of all we now require
pypuppetdb version 0.0.4 or later which includes support for the v3 API
introduced with PuppetDB 1.5.

Because of changes in PuppetDB 1.5 and therefor in pypuppetdb users of the v2
API, regardless of the PuppetDB version, will no longer be able to view reports
or events.

In light of this the following settings have been removed:

* ``PUPPETDB_EXPERIMENTAL``

Two new settings have been added:

* ``PUPPETDB_API``: an integer, defaulting to ``3``, representing the API
  version we want to use.
* ``ENABLE_QUERY``: a boolean, defaulting to ``True``, on wether or not to
  be able to use the Query tab.

We've also added a few new features:

* Thanks to some work done during PuppetConf together with Nick Lewis (from
  Puppet Labs) we now expose all of PuppetDB's metrics in the Metrics tab. The
  formatting isn't exactly pretty but it's a start.
* Spencer Krum added the graphing capabilities to the Facts tab.
* Daniel Lawrence added a feature so that facts on the node view are clickable
  and take you to the complete overview of that fact for your infrastructure
  and made the nodes in the complete facts list clickable so you can jump to a
  node.
* Klavs Klavsen contributed some documentation on how to run Puppetboard with
  Passenger.

0.0.1
=====
Initial release.


