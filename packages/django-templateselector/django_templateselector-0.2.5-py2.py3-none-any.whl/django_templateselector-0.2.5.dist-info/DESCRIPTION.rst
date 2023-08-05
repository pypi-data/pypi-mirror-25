django-templateselector
=======================

:author: Keryn Knight
:version: 0.2.5

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-template-selector.svg?branch=0.2.5
  :target: https://travis-ci.org/kezabelle/django-template-selector

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-template-selector.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-template-selector

==============  ======
Release         Status
==============  ======
stable (0.2.5)  |travis_stable|
master          |travis_master|
==============  ======


.. contents:: Sections
   :depth: 2

What it does
------------

Provides a new model field, ``fields.TemplateField`` which allows for selection
of a specific `Django`_ template using a nice form field (``fields.TemplateChoiceField``)
and a nicer widget (``widgets.TemplateSelector``) than the standard ``<select>`` dropdown.

Example
^^^^^^^

Below is a screenshot of the admin widget, without any thumbnails set up for
each template, because I'm too lazy for that.

.. image:: https://raw.github.com/kezabelle/django-template-selector/master/screenshot.png
    :alt: Example

Use case
--------

Imagine you have a ``Page`` model, and you want to allow admins or page authors
to choose from a range of templates for the page to use, you could do this::

  from django.db import models
  from templateselector.fields import TemplateField

  class MyPage(models.Model):
    title = models.CharField(max_length=100)
    # ...
    template = TemplateField(match='^myapp/mypage/layouts/.+\.html$')

which would allow them to select any HTML file Django could find in the
appropriate directory.


Available functionality
-----------------------

These fields are really the only public API. There's obviously other stuff, if you
care to rummage around.

``TemplateField``
^^^^^^^^^^^^^^^^^

Extends CharField, and requires a ``match`` argument which ought to be a
string version of a regular expression. The ``match`` will be used to filter
the possible choices. Optionally also takes a ``display_name`` argument, which
is a callable (or ``dotted.string.path.to.one``) that takes a given
string (the selected template path) and returns a nice name for it. The
nice name is available as ``get_<fieldname>_display``, `for consistency with Django`_

The default form field for ``TemplateField`` is ...

``TemplateChoiceField``
^^^^^^^^^^^^^^^^^^^^^^^

Has the same arguments as ``TemplateField``, and can be used independently
in all forms if you want to not use the model field.
The form field, when rendered with the ``TemplateSelector`` widget, will try
and show a preview image for each template, by attempting to load a ``100W x 120H``
image from your staticfiles.
Given a template name of
``path/to/template.htm`` it will try and load ``path/to/template.htm.png`` prefixed
by whatever your ``STATIC_URL`` is. If no file exists, a placeholder image is
shown as a fallback.

Both this and the ``TemplateField`` make use of...

``nice_display_name``
^^^^^^^^^^^^^^^^^^^^^

This function is the default callable for the ``display_name`` arguments on
the ``TemplateField`` and ``TemplateChoiceField``, it tries to provide some
flexibility and sensisble defaults; specifically:

* If your project defines a ``TEMPLATESELECTOR_DISPLAY_NAMES`` setting which
  is a dictionary like ``{'path/to/template.html': "my awesome template"}`` then
  the name ``"my awesome template"`` will be shown by preference.
* If not set, or no key match is found, the function will take the *file name*
  (not the path!) without *any extension* and will attempt to make a pretty, readable
  name of it by replacing most non-alphabet characters with spaces, so
  the template ``test/app/hello_world.html`` would become ``Hello world``

Supported Django versions
-------------------------

The tests are run against Django 1.11 on Python 2.7, and 3.5.
The widget uses the Django 1.11 template-based-rendering, so won't work on
previous versions. Possibly it'll just default back to a normal radiobox? I dunno.


Installation and usage
----------------------

Installation
^^^^^^^^^^^^

You can use `pip`_ to install the ``0.2.5`` version from `PyPI`_::

    pip install django-templateselector==0.2.5

Or you can grab it from  `GitHub`_  like this::

  pip install -e git+https://github.com/kezabelle/django-template-selector.git#egg=django-template-selector

Configuration
^^^^^^^^^^^^^

To get the ``TemplateSelector`` widget to display correctly, you *will* need to
add ``templateselector`` to your project's ``INSTALLED_APPS``.

You may also wish to configure ``TEMPLATESELECTOR_DISPLAY_NAMES = {}`` to provide
nice names (see `nice_display_name`_)

Usage
^^^^^

For using the  `TemplateField`_, try something like this::

  from django.db.models import Model
  from templateselector.fields import TemplateField

  class MyPage(models.Model):
    template = TemplateField(match='^myapp/mypage/layouts/.+\.html$')

For using the `TemplateChoiceField`_ without using the Model field, you'd
do something like::

    from django.forms import Form
    from templateselector.fields import TemplateChoiceField

    class MyForm(Form):
        field = TemplateChoiceField(match="^myapp/[0-9]+.html$")

To get the widget's CSS, don't forget to use ``{{ form.media }}`` in your template!

Altering the widget choice size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you'd like to modify the dimensions used for each option in the widget (eg:
you have landscape template thumbnails instead of portrait) you'll need to
override the following CSS classes::

    .templateselector-list-item {
        width: ???;
    }
    .templateselector-label input {
        top: ???;
    }
    .templateselector-thumb {
        width: ???;
        height: ???;
    }

You can probably use the ``#id_FIELDNAME`` for a given field to provide the
necessary specificity.

You may need to provide a wrapper element if you re-use the same model/form
attribute name (eg: ``{{ myform.selected_file }}``) for multiple things with
different dimensions::

    <!-- target with
    .myform-wrapper #id_selected_file .templateselector-list-item
    etc -->
    <div class="myform-wrapper">{{ myform.selected_file }}</div>

    <!-- target with
    .myapp-wrapper #id_selected_file .templateselector-thumb
     etc -->
    <div class="myapp-wrapper">{{ mymodelform.selected_file }}</div>

Running the tests
^^^^^^^^^^^^^^^^^

If you have a cloned copy, you can do::

  python setup.py test

If you have tox, you can just do::

  tox

Running the demo
^^^^^^^^^^^^^^^^

A barebones demo is provided. It assumes you're using something like `virtualenv`_ and
`virtualenvwrapper`_ but you can probably figure it out otherwise::

    mktmpenv --python=`which python3`
    pip install -e git+https://github.com/kezabelle/django-template-selector.git#egg=django-templateselector

Then probably::

    cd src/django-templateselector
    python demo_project.py runserver

The index page ``/`` will show you a normal version of the selection widget,
while ``/admin/tests/mymodel/add/`` will show the slightly customised version
for the standard `Django`_ admin.

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _Django: https://www.djangoproject.com/
.. _GitHub: https://github.com/
.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _pip: https://pip.pypa.io/en/stable/
.. _PyPI: https://pypi.python.org/pypi
.. _for consistency with Django: https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.get_FOO_display


----

Copyright (c) 2017, Keryn Knight
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

Change history for django-templateselector
------------------------------------------

0.2.5
^^^^^^
* |FIX| Added ``:focus`` visual styles so that keyboard navigation through a form
  including the widget may now indicate when selecting items.

0.2.4
^^^^^^
* |NEW| Added a `system check`_ to ensure that the templates and styles are
  able to be loaded.


0.2.3
^^^^^^
* |FIX| Change the model level field validation (``TemplateField(match=...)`` to
  forcibly check the given value matches the regex, in addition to checking
  whether the given value exists in one of the template loaders.
* |META| Still trying to master automatic deployment from Travis. One day I'll
  get sdist working again!

0.2.2
^^^^^^
* |META| Still trying to master automatic deployment from Travis. No
  functionality change since ``0.2.0``


0.2.1
^^^^^^
* |META| Automatic deployment of new releases from Travis mostly worked, but the
  ``sdist`` is in poor shape (see commit ``44ad2a1542f2f61a73de84e0f7213bccfdb6f265``)
  so I've disabled that for now. Wheels are better anyway, right? No
  functionality change since ``0.2.0``


0.2.0
^^^^^^

* |FIX| prevent the "same" template showing up more than once in the
  widget, which wouldn't be possible when using ``get_template`` (`#1`_)
* |NEW| If the form field (``TemplateChoiceField``) has only **one** valid template
  option, and the form is unbound (ie: its an **add** form or whatever) then
  pre-select the valid choice. Only happens if the field has ``required=True``
* |NEW| using the ``get_<fieldname>_display`` as a value in a ```ModelAdmin.list_display``
  will now allow for sorting by the underlying value in the database. (`#2`_)
* |NEW| if the ``<fieldname>`` is used as part of a ``ModelAdmin.list_filter`` it will
  show the nice display names of any used templates, rather than their internal
  path representation. (`#3`_)

0.1.1
^^^^^^
* |META| First release on PyPI.

0.1.0
^^^^^
* |META| Initial development.


.. |FIX| replace:: **BUGFIX:**
.. |NEW| replace:: **FEATURE:**
.. |META| replace:: **MISC:**
.. _#1: https://github.com/kezabelle/django-template-selector/issues/1
.. _#2: https://github.com/kezabelle/django-template-selector/issues/2
.. _#3: https://github.com/kezabelle/django-template-selector/issues/3
.. _system check: https://docs.djangoproject.com/en/stable/topics/checks/


