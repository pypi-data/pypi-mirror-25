=====
Django-General-Filters
=====

django-general-filters is a liberary of useful custom django filters.

With django-general-filters you can develop django applications faster and 
easier, and no need to deal with some difficult stuff about tags and filters.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "generalfilters" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'generalfilters',
    ]

2. Load the general_filters filter in your templates like this::

    {% load general_filters %}
