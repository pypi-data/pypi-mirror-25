=====
FidusWriter-Citation-API-import
=====

FidusWriter-Citation-API-import is a Fidus Writer plugin to allow for import of
citations from external sources via API.

Currently these citation sources are supported: Sowiport, Crossref,
Datacite.


Installation
-----------

1. Install Fidus Writer if you haven't done so already.

2. Within the virtual environment set up for your Fidus Writer instance, install the version of the plugin corresponding to your Fidus Writer installation. If you are running Fidus Writer 3.2, the command is::

    pip install "fiduswriter-citation-api-import<3.3"

3. Add "citation-api-import" to your INSTALLED_APPS setting in the
   configuration.py file like this::

    INSTALLED_APPS += (
        ...
        'citation-api-import',
    )

4. Run `python manage.py transpile` to create the needed JavaScript files.

5. (Re)start your Fidus Writer server


Credits
-----------

This plugin has been developed by the `Opening Scholarly Communications in the Social Sciences (OSCOSS) <http://www.gesis.org/?id=10714>`_ project, financed by the German Research Foundation (DFG) and executed by the University of Bonn and GESIS – Leibniz Institute for the Social Sciences.

Lead Developer: `Niloofar Azizi <https://github.com/NiloofarAzizi>`_
