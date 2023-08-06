==================
Django UTF-8 Field
==================

.. image:: https://travis-ci.org/megasnort/django-utf8field.svg
    :target: https://travis-ci.org/megasnort/django-utf8field/
    :alt: Build status

This package was created because at my work, `Language and Translation Technology Team`_ at the University of Ghent, we often create demos on the web that allow the user to input and process text or files. These texts are then processed by other scripts that expect clean UTF-8-texts.
This library extends the Django FileField, CharField and TextField by checking if the content of a submitted file or text is clean. If not, it generates an error. Checks are executed for four byte long characters and NULL characters.


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


You also have the option to provide the option `max_content_length` to limit the number of characters in the file. If the content is longer an error will be displayed. If you want to enable `four_byte_detection` set the parameter to True.


::

    text = models.UTF8FileField(max_content_length=1000, four_byte_detection=True)



CharField
^^^^^^^^^
Create a model like you would do normally, but instead of using CharField you use UTF8CharField. If you want to enable `four_byte_detection` set the parameter to True.

::

    from django.db import models
    from utf8field.fields import UTF8CharField

    class YourModel(models.Model):
        title = models.CharField(max_length=255, four_byte_detection=True)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8CharField(max_length=1000)


TextField
^^^^^^^^^
Create a model like you would do normally, but instead of using TextField you use UTF8TextField. If you want to enable `four_byte_detection` set the parameter to True.

::

    from django.db import models
    from utf8field.fields import UTF8TextField

    class YourModel(models.Model):
        title = models.CharField(max_length=255)
        created_on = models.DateTimeField(auto_add_on=True)
        text = models.UTF8TextField(four_byte_detection=True)



Django Rest Framework
^^^^^^^^^^^^^^^^^^^^^
The necessary serializers and automatic mapping of fields is provided so you should not be doing anything yourself to get the texts or files validated when using a ModelSerializer.


Development
-----------
To run the tests make sure Django, Django Rest Framework and coverage are installed (`pip install django djangorestframework coverage`) and execute

::

    python manage.py test


To create extra translations, execute

::

    pm makemessages --locale=nl --extension=py --ignore=dev_example --ignore=build


... and modify the resulting `django.po` file in `utf8field/locale/nl/LC_MESSAGES`.



.. _`Language and Translation Technology Team`: https://lt3.ugent.be