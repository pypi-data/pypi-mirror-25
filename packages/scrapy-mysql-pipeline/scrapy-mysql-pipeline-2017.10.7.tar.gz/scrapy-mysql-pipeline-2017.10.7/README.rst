.. figure:: https://img.shields.io/badge/Python-3.6-blue.svg
   :alt: Python 3.6

   Python 3.6

scrapy-mysql-pipeline
---------------------

Asynchronous mysql `Scrapy <https://doc.scrapy.org/en/latest/>`__ item
pipeline

Installation
^^^^^^^^^^^^

.. code:: bash

    pip install scrapy-mysql-pipeline

Configuration
^^^^^^^^^^^^^

Add pipeline

.. code:: python

    ITEM_PIPELINES = {
        'scrapy_mysql_pipeline.MySQLPipeline': 300,
    }

Default values:

.. code:: python

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = None
    MYSQL_PASSWORD = ''
    MYSQL_DB = None
    MYSQL_TABLE = None
    MYSQL_UPSERT = False
    MYSQL_RETRIES = 3
    MYSQL_CLOSE_ON_ERROR = True

MYSQL\_TABLE variable must be set in settings.py
