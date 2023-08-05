==================
Django UTF-8 Field
==================

.. image:: https://travis-ci.org/megasnort/django-utf8field.svg
    :target: https://travis-ci.org/megasnort/django-utf8field/
    :alt: Build status

.. image:: https://coveralls.io/repos/github/megasnort/django-utf8field/badge.svg?branch=master
    :target: https://coveralls.io/github/megasnort/django-utf8field?branch=master
    :alt: Coverage

This package was created because at my work, `Language and Translation Technology Team`_ at the University of Ghent, we often create demos on the web that allow the user to input and process text or files. These texts are then processed by other scripts that expect clean UTF-8-texts.
This library extends the Django FileField, CharField and TextField by checking if the content of a submitted file or text is clean UTF-8. If not, it generates an error. Extra checks are executed for four byte long characters and NULL characters.


Requirements
------------
Django >= 1.8


Installation
------------
::

    pip install django-utf8field


Usage
-----

Add the app to your settings:

::

    INSTALLED_APPS = (
        ...
        'utf8field',
        ...


FileField
^^^^^^^^^
Create a model like you would do normally, but instead of using FileField you use UTF8FileField:

::

    from django.db import models
    from utf8field.fields import UTF8FileField

    class YourModel(models.Model):
        title = models.CharField(max_length=255)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8FileField()


You also have the option to provide the option `max_content_length` to limit the number of characters in the file. If the content is longer an error will be displayed.

::

    text = models.UTF8FileField(max_content_length=1000)



CharField
^^^^^^^^^
Create a model like you would do normally, but instead of using CharField you use UTF8CharField:

::

    from django.db import models
    from utf8field.fields import UTF8CharField

    class YourModel(models.Model):
        title = models.CharField(max_length=255)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8CharField(max_length=1000)


TextField
^^^^^^^^^
Create a model like you would do normally, but instead of using TextField you use UTF8TextField:

::

    from django.db import models
    from utf8field.fields import UTF8TextField

    class YourModel(models.Model):
        title = models.CharField(max_length=255)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8TextField()




Development
-----------
To run the tests make sure Django is installed (`pip install django`) and execute

::

    python manage.py test


To create extra translations, execute

::

    pm makemessages --locale=nl --extension=py --ignore=dev_example --ignore=build


... and modify the resulting `django.po` file in `utf8field/locale/nl/LC_MESSAGES`.



.. _`Language and Translation Technology Team`: https://lt3.ugent.be