===========
delta 11888
===========



.. image:: https://pyup.io/repos/github/dimkl/giaola_xml_delta/shield.svg
     :target: https://pyup.io/repos/github/dimkl/giaola_xml_delta/
     :alt: Updates


11888 delta app for das admin



Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Create table Section

# create database using SQL
`CREATE DATABASE delta;`

# create table
```
>>> from xml_delta.storages import models
>>> from xml_delta import settings
>>> from sqlalchemy import create_engine
>>> engine = create_engine(settings.STORAGE_DATABASE_URL, echo=True)

>>> from giaola_xml_delta import settings
>>> from sqlalchemy import create_engine
>>> engine = create_engine(settings.STORAGE_DATABASE_URL, echo=True)
>>> models.Base.metadata.create_all(engine)
```

# run package
1. edit settings using .env file
2. execute: ` python -m giaola_xml_delta.giaola_xml_delta <sample_data>`
