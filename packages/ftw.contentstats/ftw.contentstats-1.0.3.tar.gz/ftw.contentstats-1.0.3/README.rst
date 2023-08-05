================
ftw.contentstats
================

.. contents:: Table of Contents


Introduction
============

``ftw.contentstats`` is a Plone add-on for collecting and displaying content
statistics.


Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.contentstats


Usage
=====

Visit the ``@@content-stats`` view on a Plone site (requires the
``cmf.ManagePortal`` permission by default).

----

.. image:: https://raw.githubusercontent.com/4teamwork/ftw.contentstats/master/docs/content-stats-view.png


Logging content stats over time
===============================

In order to log content stats to a file, you can use the provided
``bin/dump-content-stats`` script to have stats dumped to a logfile that
contains on JSON entry per line, containing the raw stats for that time.

Usage:

``bin/dump-content-stats -s <plone_site_id>``

The script will cause the stats to be dumped by making a request to the
``@@dump-content-stats`` view. This view is accessible to Anonymous
(``zope.Public``), but *only* when requested from localhost!

So in order for this script to work, you'll have to invoke it on the same
machine where your Zope instances run, and make sure the Plone site is **up
and running**, and reachable from localhost.

The logfile location will be in the same directory as the Z2 log, and the
log will be named ``contentstats-json.log``.

**Note**: In order to figure out the appropriate log directory,
``ftw.contentstats`` needs to derive this information from the eventlog
location. It's therefore important to have an eventlog configured, otherwise
``ftw.contentstats`` will not be able to log any content stats, and complain
noisily through the root logger.


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.contentstats
- Issues: https://github.com/4teamwork/ftw.contentstats/issues
- Pypi: http://pypi.python.org/pypi/ftw.contentstats


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contentstats`` is licensed under GNU General Public License, version 2.
