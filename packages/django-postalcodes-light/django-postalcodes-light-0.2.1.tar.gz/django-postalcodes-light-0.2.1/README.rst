Django Postal Codes
===================

A simple data model for storing postal codes with placenames and location.

.. image:: https://badge.fury.io/py/django-postalcodes-light.svg
    :target: https://badge.fury.io/py/django-postalcodes-light

Installing
----------

The recommended installing method is with `pip`::

    pip install django-postalcodes-light

You can also clone the repository and install from source::

    python setup.py install

Getting data
------------

Postal code data is available from a number of sources, typically on a country
by country basis. The United States Census Bureau maintains the `Gazetteer
database <http://www.census.gov/geo/www/gazetteer/gazette.html>`_, including
detailed postal code data. The `GeoNames geographical database
<http://download.geonames.org/export/zip/>`_ also provides postal code data
for international postal codes (and other places).

This project uses the column names specified by GeoNames and includes a
management to import and update data from GeoNames::

    python manage.py import_postalcodes US

Additional files can be imported by specifying each country code. Multiple
country codes may be provided on one line, e.g.::

    python manage.py import_postalcodes FR IT
