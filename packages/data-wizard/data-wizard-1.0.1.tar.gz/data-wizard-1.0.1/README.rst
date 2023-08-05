**Django Data Wizard** is an interactive tool for mapping structured
data (e.g. Excel, XML) into a normalized database structure via
`wq.io <https://wq.io/wq.io>`__ and the `Django REST
Framework <http://www.django-rest-framework.org/>`__. Django Data Wizard
allows novice users to map spreadsheet columns to serializer fields (and
cell values to foreign keys) on-the-fly during the import process. This
reduces the need for preset spreadsheet formats, which most data import
solutions require.


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/02-columns.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/02-columns.png
   :width: 33 %
   :alt: Column Choices
 
.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/08-data75.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/08-data75.png
   :width: 33 %
   :alt: Auto Import - Progress Bar
 
.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/10-records.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/10-records.png
   :width: 33 %
   :alt: Imported Records


By default, Django Data Wizard supports any format supported by
`wq.io <https://wq.io/wq.io>`__ (Excel, CSV, JSON, and XML). Additional
formats can be integrating by creating a `custom wq.io
class <https://wq.io/docs/custom-io>`__ and then registering it with the
wizard. For example, the `Climata
Viewer <https://github.com/heigeo/climata-viewer>`__ uses Django Data
Wizard to import data from
`climata <https://github.com/heigeo/climata>`__'s wq.io-based web
service client.

The Data Wizard supports straightforward one-to-one mappings from
spreadsheet columns to database fields, as well as more complex
scenarios like `natural
keys <https://github.com/wq/django-natural-keys>`__ and
`Entity-Attribute-Value <https://wq.io/docs/eav-vs-relational>`__ (or
"wide") table mappings. It was originally developed for use with the
`ERAV data model <https://wq.io/docs/erav>`__ provided by
`vera <https://wq.io/vera>`__.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Usage
=====

Django Data Wizard provides a JSON (and HTML) API for specifying a data
set to import (by referencing a previously-uploaded file), selecting a
serializer, mapping the data columns and identifiers, and
(asynchronously) importing the data into the database.

Installation
------------

.. code:: bash

    # Recommended: create virtual environment
    # python3 -m venv venv
    # . venv/bin/activate

    pip install data-wizard

See https://github.com/wq/django-data-wizard to report any issues.

Initial Configuration
---------------------

Within a new or existing Django or wq project, configure the following:

1. Celery / Redis
2. A model for (up)loading source data
3. One or more serializers for populating the destination models
4. wq/progress.js plugin (if using wq)

Celery
~~~~~~

Django Data Wizard requires `Celery <http://www.celeryproject.org/>`__
to handle asynchronous tasks, and is usually used with
`Redis <https://redis.io/>`__ as the memory store. These should be
configured first or the REST API may not work. On Ubuntu, run the
following command:

.. code:: bash

    # Install redis on Ubuntu
    sudo apt-get install redis-server

Once Redis is installed, you should be able to add the following to your
project settings:

.. code:: python

    # myproject/settings.py

    INSTALLED_APPS = (
       # ...
       'data_wizard',
       'myapp',
    )

    CELERY_RESULT_BACKEND = BROKER_URL = 'redis://localhost:6379/1'

Then, define a celery app:

.. code:: python

    # myproject/celery.py
    from __future__ import absolute_import
    from celery import Celery
    from django.conf import settings
    app = Celery('myproject')
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

And reference it from your project:

.. code:: python

    # myproject/__init__.py
    from .celery import app as celery_app

Finally, make sure that celery is running in the background. You can
test with the following command, then move to a more stable
configuration (e.g.
`daemonization <http://docs.celeryproject.org/en/latest/userguide/daemonizing.html>`__).

.. code:: bash

    # celery.sh
    export DJANGO_SETTINGS_MODULE=myproject.settings
    celery -A myproject worker -l info

Note that any time you change your serializer registration, you should
reload celery in addition to restarting the Django WSGI instance.

Data Loader
~~~~~~~~~~~

To use Data Wizard with the default configuration, your project should
provide a Django model with a ``FileField`` named ``file``. You will
want to provide your users with the ability to upload spreadsheets and
other files to this model, for example by registering it with
`wq.db <https://wq.io/wq.db>`__. The actual import process can then be
triggered after the file is uploaded, for example by adding a form to
the detail page (`see below <#new-run>`__).

.. code:: python

    # myapp/models.py
    from django.db import models

    class FileModel(models.Model):
        file = models.FileField(upload_to='spreadsheets')
        # ...

.. code:: python

    # myapp/rest.py
    from wq.db import rest
    from .models import FileModel

    rest.router.register_model(
        FileModel,
        fields="__all__",
    )

Custom FileField Name
^^^^^^^^^^^^^^^^^^^^^

You can use a model with a different ``FileField`` name by extending
``data_wizard.loaders.FileLoader`` and setting ``DATA_WIZARD_LOADER``:

.. code:: python

    # myapp/models.py
    from django.db import models

    class FileModel(models.Model):
        spreadsheet = models.FileField(upload_to='spreadsheets')

.. code:: python

    # myapp/loaders.py
    from data_wizard import loaders

    class FileLoader(loaders.FileLoader):
        file_attr = 'spreadsheet'

.. code:: python

    # myapp/settings.py
    DATA_WIZARD_LOADER = 'myapp.loaders.FileLoader'

Custom Data Source
^^^^^^^^^^^^^^^^^^

You can also customize the loader to load data from a `custom wq.io
class <https://wq.io/docs/custom-io>`__. For example, the `Climata
Viewer <https://github.com/heigeo/climata-viewer>`__ uses
`climata <https://github.com/heigeo/climata>`__ classes to load data
directly from third-party webservices. To do this, extend
``data_wizard.loaders.BaseLoader`` with a custom ``load_io()`` function
that returns the data from wq.io:

.. code:: python

    # myapp/models.py
    from django.db import models

    class WebSource(models.Model):
        url = models.URLField()

.. code:: python

    # myapp/loaders.py
    from data_wizard import loaders

    class UrlLoader(loaders.BaseLoader):
        def load_io(self):
            source = self.run.content_object
            from wq.io import load_url # or e.g. JsonNetIO
            return load_url(source.url)

.. code:: python

    # myapp/settings.py
    DATA_WIZARD_LOADER = 'myapp.loaders.UrlLoader'

Note that there still should be a custom model to define the parameters
for the IO class, even though there is no file being stored.

Serializer Registration
~~~~~~~~~~~~~~~~~~~~~~~

Data Wizard uses wq.io classes (via the loader) to determine the *source
columns* present on the spreadsheet or other data source. It uses Django
REST Framework's `ModelSerializer
class <http://www.django-rest-framework.org/api-guide/serializers/#modelserializer>`__
to determine the *destination fields* on the database model. You can
register serializers by creating a ``wizard.py`` in your app directory
(analogous to Django's ``admin.py`` and wq.db's ``rest.py``). Multiple
serializers can be registered with the wizard to support multiple import
configurations and destination models.

.. code:: python

    # myapp/wizard.py
    from rest_framework import serializers
    from data_wizard import registry
    from .models import TimeSeries

    class TimeSeriesSerializer(serializers.ModelSerializer):
        class Meta:
            model = TimeSeries
            fields = '__all__'

    registry.register("Time Series", TimeSeriesSerializer)

At least one serializer should be registered in order to use the wizard.
Note the use of a human-friendly serializer label when registering. This
name should be unique throughout the project, but can be changed later
on without breaking existing data. (The class path is used as the actual
identifier behind the scenes.)

Progress Bar Support
~~~~~~~~~~~~~~~~~~~~

If you are using the built-in Data Wizard interface for wq, be sure to
enable the `wq/progress.js <https://wq.io/docs/progress-js>`__ plugin.

.. code:: javascript

    // myapp/main.js
    define(['wq/app', 'wq/progress', ...],
    function(app, progress, ...) {
        app.use(progress);
        app.init(config).then(...);
    });

Run-Time Usage (REST API)
-------------------------

The Data Wizard REST API provides the following capabilities. If you are
using wq.db, the wizard will automatically register itself with the
router. Otherwise, be sure to include ``data_wizard.urls`` in your URL
configuration:

.. code:: python

    # with wq.db (automatic)
    # rest.router.register_model(data_wizard.models.Run, ...)

    # without wq.db
    from django.conf.urls import include, url

    urlpatterns = [
        # ...
        url(r'^', include('data_wizard.urls')),
    ]

The API is accessible as JSON and as HTML - though the HTML interface is
(currently) only accessible when using the Mustache template engine
(i.e. with wq.db).

New Run
~~~~~~~

``POST /datawizard/``
^^^^^^^^^^^^^^^^^^^^^

Create a new instance of the wizard (i.e. a ``Run``). The returned run
``id`` should be used in all subsequent calls to the API. Each ``Run``
is tied to the model containing the actual data via a `generic foreign
key <https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/>`__.

+---------------------+-------------------------------------------+
| parameter           | description                               |
+=====================+===========================================+
| ``object_id``       | The id of the object containing the data  |
|                     | to be imported.                           |
+---------------------+-------------------------------------------+
| ``content_type_id`` | The app label and model name of the       |
|                     | referenced model (in the format           |
|                     | ``app_label.modelname``).                 |
+---------------------+-------------------------------------------+
| ``loader``          | (Optional) The class name to use for      |
|                     | loading the dataset via wq.io. The        |
|                     | default loader                            |
|                     | (``data_wizard.loaders.FileLoader``)      |
|                     | assumes that the referenced model         |
|                     | contains a ``FileField`` named ``file``.  |
+---------------------+-------------------------------------------+
| ``serializer``      | (Optional) The class name to use for      |
|                     | serialization. This can be left unset to  |
|                     | allow the user to select it during the    |
|                     | wizard run.                               |
+---------------------+-------------------------------------------+

If you are using wq.db, you could allow the user to initiate an import
run by adding the following to the detail HTML for your model:

.. code:: html

    <!-- filemodel_detail.html -->
    <h1>{{label}}</h1>
    <a href="{{rt}}/media/{{file}}" rel="external">Download File</a>

    <form action="{{rt}}/datawizard/" method="post" data-ajax="true" data-wq-json="false">
      {{>csrf}}
      <input type="hidden" name="content_type_id" value="myapp.filemodel">
      <input type="hidden" name="object_id" value="{{id}}">
      <button type="submit">Import Data from This File</button>
    </form>

auto
~~~~

``POST /datawizard/[id]/auto``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/06-data25.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/06-data25.png
   :width: 320 px
   :height: 240 px
   :alt: Auto Import - Progress Bar
   :align: right


The ``auto`` task attempts to run the entire data wizard process from
beginning to end. If any input is needed, the import will halt and
redirect to the necessary screen. If no input is needed, the ``auto``
task is equivalent to starting the ``data`` task directly. This is an
asynchronous method, and returns a ``task_id`` to be used with the
status API.

The default
`run\_detail.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_detail.html>`__
template provides an example form to initiate the ``auto`` task.

status
~~~~~~

``GET /datawizard/[id]/status.json?task=[task]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``status`` API is used to check the status of an asynchronous task
(one of ``auto`` or ``data``). The API is designed to be used in
conjunction with the `wq/progress.js <https://wq.io/docs/progress-js>`__
plugin for `wq.app <https://wq.io/wq.app>`__, which can be used as a
reference for custom implementations. Unlike the other methods, this API
should always be called as JSON (either as ``status.json`` or
``status?format=json``). An object of the following format will be
returned:

.. code:: js

    {
        // General properties
        "status": "PROGRESS", // or "SUCCESS", "FAILURE"
        "stage": "meta",      // or "data"
        "current": 23,        // currently processing row
        "total": 100,         // total number of rows
        
        // "FAILURE"
        "error": "Error Message",

        // Task complete ("SUCCESS")
        "action": "records",        // or "serializers", "columns" "ids"
        "message": "Input Needed",  // if action is not "records"
        "skipped": [...],           // rows that could not be imported
        "location": "/datawizard/[id]/records",
    }

Note that the ``status`` field is directly derived from the underlying
`Celery task
state <http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-states>`__.
When running an ``auto`` task, the result is ``SUCCESS`` whenever the
task ends without errors, even if there is additional input needed to
fully complete the run.

The default
`run\_auto.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_auto.html>`__
and
`run\_data.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_data.html>`__
templates include a ``<progress>`` element for use with
`wq/progress.js <https://wq.io/docs/progress-js>`__ and the status task.

serializers
~~~~~~~~~~~

``GET /datawizard/[id]/serializers``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/00-serializers.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/00-serializers.png
   :width: 320 px
   :height: 240 px
   :alt: Serializer Choices
   :align: right


The ``serializers`` task provides a list of all registered serializers.
This screen is shown by the ``auto`` task if a serializer was not
specified when the ``Run`` was created. The default
`run\_serializers.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_serializers.html>`__
template includes an interface for selecting a registered serializer. If
a serializer is already selected, the template will display the label
and a button to (re)start the ``auto`` task.

updateserializer
~~~~~~~~~~~~~~~~

``POST /datawizard/[id]/updateserializer``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``updateserializer`` task updates the specified ``Run`` with the
selected serializer class name. This is typically called from `the
form <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_serializers.html>`__
generated by the ``serializers`` task, and will redirect to that task
when complete.

+----------------+-------------------------------------------+
| parameter      | description                               |
+================+===========================================+
| ``serializer`` | The class name (or label) of the          |
|                | serializer to use for this run.           |
+----------------+-------------------------------------------+

columns
~~~~~~~

``GET /datawizard/[id]/columns``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/02-columns.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/02-columns.png
   :width: 320 px
   :height: 240 px
   :alt: Column Choices
   :align: right


The ``columns`` task lists all of the columns found in the dataset (i.e.
spreadsheet) and their mappings to serializer fields. This screen is
shown by the ``auto`` task if there are any column names that could not
be automatically mapped. The potential mappings are one of:

-  simple serializer field names (e.g. ``field``)
-  nested field names (for `natural
   keys <https://github.com/wq/django-natural-keys>`__, e.g.
   ``nested[record][field]``)
-  `EAV <https://wq.io/docs/eav-vs-relational>`__ attribute-value
   mappings (e.g. ``values[][value];attribute_id=1``).

To enable a natural key mapping, the registered serializer should be an
instance of ``NaturalKeyModelSerializer``, as in `this
example <https://github.com/wq/django-data-wizard/blob/master/tests/naturalkey_app/wizard.py>`__.
To enable an EAV mapping, the registered serializer should include a
nested serializer with ``many=True`` and at least one foreign key to the
attribute table, as in `this
example <https://github.com/wq/django-data-wizard/blob/master/tests/eav_app/wizard.py>`__.

The default
`run\_columns.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_columns.html>`__
template includes an interface for mapping data columns to serializer
fields. If all columns are already mapped, the template will display the
mappings and a button to (re)start the ``auto`` task.

updatecolumns
~~~~~~~~~~~~~

``POST /datawizard/[id]/updatecolumns``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``updatecolumns`` task saves the specified mappings from data
columns to serializer fields. This is typically called from `the
form <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_columns.html>`__
generated by the ``columns`` task, and will redirect to that task when
complete.

+-----------------+-------------------------------------------+
| parameter       | description                               |
+=================+===========================================+
| ``rel_[relid]`` | The column to map to the specified        |
|                 | serializer field. The ``relid`` and the   |
|                 | complete list of possible mappings will   |
|                 | be provided by the ``columns`` task.      |
+-----------------+-------------------------------------------+

ids
~~~

``GET /datawizard/[id]/ids``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/04-ids.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/04-ids.png
   :width: 320 px
   :height: 240 px
   :alt: Identifier Choices
   :align: right


The ``ids`` task lists all of the identifiers found in the dataset (i.e.
spreadsheet) that are in a column known to correspond to a foreign key.
This screen is shown by the ``auto`` task if there are any identifiers
that could not be automatically mapped to foreign key values. The
potential mappings depend on the serializer field used to represent the
foreign key.

-  Existing record ID or slug (for
   `PrimaryKeyRelatedField <http://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield>`__,
   `SlugRelatedField <http://www.django-rest-framework.org/api-guide/relations/#slugrelatedfield>`__,
   and
   `NaturalKeySerializer <https://github.com/wq/django-natural-keys>`__)
-  ``"new"`` (``NaturalKeySerializer`` only)

The primary difference is that ``NaturalKeySerializer`` allows for the
possibility of creating new records in the foreign table on the fly,
while the regular related fields do not.

The default
`run\_ids.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_ids.html>`__
template includes an interface for mapping row identifiers to foreign
key values. If all ids are already mapped (or indicated to be new
natural keys), the template will display the mappings and a button to
(re)start the ``auto`` task.

updateids
~~~~~~~~~

``POST /datawizard/[id]/updateids``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``updateids`` task saves the specified mappings from row identifiers
to foreign key values. This is typically called from `the
form <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_ids.html>`__
generated by the ``ids`` task, and will redirect to that task when
complete.

+------------------------+-------------------------------------------+
| parameter              | description                               |
+========================+===========================================+
| ``ident_[identid]_id`` | The identifier to map to the specified    |
|                        | foreign key value. The ``identid`` and    |
|                        | the complete list of possible mappings    |
|                        | will be provided by the ``ids`` task.     |
+------------------------+-------------------------------------------+

data
~~~~

``POST /datawizard/[id]/data``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/08-data75.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/08-data75.png
   :width: 320 px
   :height: 240 px
   :alt: Auto Import - Progress Bar
   :align: right


The ``data`` task starts the actual import process (and is called by
``auto`` behind the scenes). Unlike ``auto``, calling ``data`` directly
will not cause a redirect to one of the other tasks if any meta input is
needed. Instead, ``data`` will attempt to import each record as-is, and
report any errors that occured due to e.g. missing fields or unmapped
foreign keys.

This is an asynchronous method, and returns a ``task_id`` to be used
with the ``status`` API. The default
`run\_data.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_data.html>`__
template includes a ``<progress>`` element for use with
`wq/progress.js <https://wq.io/docs/progress-js>`__ and the status task.

records
~~~~~~~

``GET /datawizard/[id]/records``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. image:: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/320/10-records.png
   :target: https://raw.githubusercontent.com/wq/django-data-wizard/master/images/10-records.png
   :width: 320 px
   :height: 240 px
   :alt: Imported Records
   :align: right


The ``records`` task provides a list of imported rows (including
errors). It is redirected to by the ``auto`` and ``data`` tasks upon
completion. When used with wq.db, the ``records`` task includes links to
the detail page for each newly imported record. The default
`run\_records.html <https://github.com/wq/django-data-wizard/blob/master/data_wizard/mustache/run_records.html>`__
template includes an interface for displaying the record details.

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/data-wizard.svg
   :target: https://pypi.python.org/pypi/data-wizard
.. |Release Notes| image:: https://img.shields.io/github/release/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/releases
.. |License| image:: https://img.shields.io/pypi/l/data-wizard.svg
   :target: https://wq.io/license
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/django-data-wizard.svg
   :target: https://travis-ci.org/wq/django-data-wizard
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/data-wizard.svg
   :target: https://pypi.python.org/pypi/data-wizard
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9%2C%201.10%2C%201.11-blue.svg
   :target: https://pypi.python.org/pypi/data-wizard
