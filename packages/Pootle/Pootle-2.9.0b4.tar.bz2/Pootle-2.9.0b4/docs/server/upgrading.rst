.. _upgrading:

Upgrading
=========

These are the instructions for upgrading Pootle from an older version to the
current release.


.. _upgrading#stop-pootle:

Stop your running Pootle
------------------------

Stop your running Pootle while you upgrade to prevent updates to your data
during the migration process. If you have RQ workers running stop those also.


.. _upgrading#system-backup:

Backup your system
------------------


.. warning::

   Before upgrading we **strongly** recommend that you
   :ref:`backup your current system <backup>`.


.. _upgrading#db-migration:

Migrate your database
---------------------

If you are currently using SQLite for your database you will need to
:doc:`migrate to either MySQL (InnoDB) or PostgreSQL <database_migration>`
before you upgrade.


.. _upgrading#latest-changes:

Latest changes
--------------

Before upgrading Pootle familiarize yourself with :doc:`important changes
</releases/index>` since the version that you are upgrading from.


.. _upgrading#requirements:

Check Pootle requirements
-------------------------

You should check that you have all of the necessary :ref:`Pootle requirements
<requirements>` and have installed all required :ref:`system packages
<requirements#packages>`.

.. warning::

   Pootle 2.7.0 or newer requires **Python 2.7**

   If you are upgrading from a virtual environment using an earlier Python
   version, you **must** upgrade or rebuild your virtual environment first.


.. _upgrading#activte-virtualenv:

Activate virtualenv
-------------------

These instructions assume that you are using :command:`virtualenv` and you have
activated a virtual environment named ``env`` as follows:

.. code-block:: console

   $ source env/bin/activate
   (env) $


.. _upgrading#update-pip-setuptools:

Update pip and setuptools
-------------------------

You should now upgrade :command:`pip` and :command:`setuptools` to the latest
version:

.. code-block:: console

   (env) $ pip install --upgrade pip setuptools


.. _upgrading#upgrading-2.6:

Upgrading from a version older than 2.6
---------------------------------------

If you are upgrading from a version older than 2.6 you will need to first
upgrade to the latest 2.6.x version and then you will be able to upgrade to the
latest version.

.. code-block:: console

   (env) $ pip install --upgrade "Pootle>=2.6,<2.7"
   (env) $ pootle setup

.. warning::
   The 2.6.x releases are meant only as a migration step.

   You must upgrade immediately to the latest version once setup has
   completed.


.. _upgrading#clean-bytecode:

Clean up stale Python bytecode
------------------------------

You should remove any stale Python bytecode files before upgrading.

Assuming you are in the root of your virtualenv folder you can run:

.. code-block:: console

   (env) $ pyclean .


.. _upgrading#upgrading-latest:

Upgrading from version 2.6.x or later
-------------------------------------

Upgrade to the latest Pootle version:

.. highlight:: console
.. parsed-literal::

   (env) $ pip install |--process-dependency-links --pre| --upgrade Pootle


.. _upgrading#check-settings:

Update and check your settings
------------------------------

You should now update your custom Pootle settings to add, remove or adjust any
settings that have changed. You may want to view the latest
:ref:`available settings <settings#available>`.

You can check to see if there are any issues with your configuration
settings that need to be resolved:

.. code-block:: console

   (env) $ pootle check

.. note:: If you are upgrading from a version of Pootle that uses
   :file:`localsettings.py` then you may want to merge your old custom settings
   with your :ref:`settings conf file <settings#customizing>` (default location
   :file:`~/.pootle/pootle.conf`).


.. _upgrading#start-rq:

Start an RQ Worker
------------------

Statistics tracking and various other background processes are managed by `RQ
<http://python-rq.org/>`_.  The :djadmin:`rqworker` command needs to be run
continuously in order to process the jobs.

If you have not already done so you should
:ref:`install and start a Redis server <requirements#packages>`.

You can start the worker in the background with the following command:

.. code-block:: console

   (env) $ pootle rqworker &

In a production environment you may want to :ref:`run RQ workers as services
<pootle#running_as_a_service>`.

See here for :ref:`further information about RQ jobs in Pootle <rq>`.


.. _upgrading#review-database:

Review your database configuration
----------------------------------

Review the :doc:`MySQL <mysql_installation>` or :doc:`PostgreSQL
<postgresql_installation>` installation instructions for any changes that you
need to make to your database.

If you run MySQL you will almost certainly need to make sure you have
:ref:`Time zone definition files <django:mysql-time-zone-definitions>` loaded
into the database.



.. _upgrading#schema-migration:

Migrate your database schema
----------------------------

Once you have updated your settings you can perform the database schema and
data upgrade by running. This is done as follows:

.. code-block:: console

   (env) $ pootle migrate --fake-initial

You will also need to update the stats data held in Pootle

.. code-block:: console

   (env) $ pootle update_data


.. _upgrading#refresh-checks:

Refreshing checks
-----------------

You must now update the translation checks. You will need to have an
:ref:`RQ worker running <installation#running-rqworker>` to complete this.

.. code-block:: console

   (env) $ pootle calculate_checks

This command will dispatch jobs to the RQ worker and may take some time.

If you wish to run :djadmin:`calculate_checks` in the foreground without using
the RQ worker you can use the :option:`--no-rq` option.



.. _upgrading#refresh-scores:

Refreshing scores
-----------------

If you are upgrading from a version prior to 2.8rc6, you will need to update
user scores using :djadmin:`refresh_scores`.

.. code-block:: console

   (env) $ pootle refresh_scores --reset
   (env) $ pootle refresh_scores


.. _upgrading#drop-cached-snippets:

Drop cached snippets
--------------------

Redis might have cached HTML snippets referring to outdated static assets. In
order for Pootle to return references to the newest assets these cached
snippets must go away:

.. code-block:: console

   (env) $ pootle flush_cache --django-cache


.. _upgrading#setup-users:

Set up users
------------

Any accounts that do not have an email address registered will not be able to
log in. You can set the email for a user using the :djadmin:`update_user_email`
command.

For example to set the email for user ``admin`` to ``admin@example.com``:

.. code-block:: console

   (env) $ pootle update_user_email admin admin@example.com


As of Pootle 2.7 users must now verify their email before they can log in.

You can use the :djadmin:`verify_user` command to bypass email verification for
a specific user.

For example to automatically verify the admin user:

.. code-block:: console

   (env) $ pootle verify_user admin

If you wish to verify all of your existing users please see the
:djadmin:`verify_user` command for further options.


.. _upgrading#next-steps:

Next steps
----------

Now that you have Pootle up and running you may want to consider some of the
following in order to build a production environment.

- :ref:`Run Pootle and RQ workers as a service <pootle#running_as_a_service>`
- :ref:`Re-apply customisations <customization>`
- :doc:`Optimize your setup <optimization>`
- :ref:`Set up a Translation Memory Server <translation_memory>`
- :ref:`Check out any new settings <settings#available>`
- :ref:`Check out Pootle management commands <commands>`
