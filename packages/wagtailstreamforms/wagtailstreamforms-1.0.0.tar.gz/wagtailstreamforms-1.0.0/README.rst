Wagtail StreamForms
===================

|CircleCI| |Coverage Status|

This package is currently a concept but allows you to add add forms that
are built in the cms admin area to any streamfield. You can also create
your own form templates which will then appear as a template choice when
you build your form. This allows you to decide how the form is submitted
and to where.

Documentation is currently being worked on but the basics are below

Whats included?
---------------

-  Forms can be built in the cms admin and used site wide in any
   streamfield.
-  You can create your own form templates to display/submit how ever you
   wish to do it.
-  We have included a mixin which will handle the form post if it is
   being submitted to a wagtail page.
-  Forms are catagorised by their class in the cms admin for easier
   navigation.
-  Form submissions are also listed by their form which you can filter
   by date and are ordered by newest first.
-  Recaptcha can be added to a form.
-  You can also add site wide regex validators fo use in regex fields.

Screen shots
------------

.. figure:: https://github.com/AccentDesign/wagtailstreamforms/raw/master/images/screen1.png
   :alt: Screen1

.. figure:: https://github.com/AccentDesign/wagtailstreamforms/raw/master/images/screen2.png
   :alt: Screen2

.. figure:: https://github.com/AccentDesign/wagtailstreamforms/raw/master/images/screen3.png
   :alt: Screen3

.. figure:: https://github.com/AccentDesign/wagtailstreamforms/raw/master/images/screen4.png
   :alt: Screen4

.. figure:: https://github.com/AccentDesign/wagtailstreamforms/raw/master/images/screen5.png
   :alt: Screen5

General setup
-------------

Add wagtailstreamforms to your INSTALLED\_APPS:

::

    INSTALLED_APPS = [
        ...
        'wagtailstreamforms'
        ...
    ]

Next define the form templates in your settings.py:

::

    # this is the defaults 
    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )

and if you want to the admin base area label:

::

    # this is the default
    WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = 'Streamforms'

Add the urls to urls.py:

::

    from wagtailstreamforms import urls as streamforms_urls

    urlpatterns = [
        ...
        url(r'^streamforms/', include(streamforms_urls)),
        ...
    ]

Optionally enable recaptcha
---------------------------

Has been enabled via the
`django-recaptcha <https://github.com/praekelt/django-recaptcha>`__
package. Please note that only one recapcha should be used per page,
this is a known issue and we are looking to fix it.

Just add captcha to your INSTALLED_APPS:

::

    INSTALLED_APPS = [
        ...
        'captcha'
        ...
    ]

Add the required keys in your settings.py which you can get from
google's recapcha service:

::

    RECAPTCHA_PUBLIC_KEY = 'xxx'
    RECAPTCHA_PRIVATE_KEY = 'xxx'
     
    # To use the new No Captcha reCaptcha
    NOCAPTCHA = True

Defining your own form functionality
------------------------------------

Currently we have defined two different types of forms one which just
enables saving the submission and one to addionally email the results of
the submission, As shown
`here <https://github.com/AccentDesign/wagtailstreamforms/blob/master/wagtailstreamforms/models/form.py#L112>`__.

You can easily add your own all you have to do is create a model that
inherits from our form base class add any addional fields/properties and
this will be added to the cms admin area.

Example:

::

    from wagtailstreamforms.models import BaseForm

    class SomeForm(BaseForm):

        def process_form_submission(self, form):
            super(SomeForm, self).process_form_submission(form) # handles the submission saving
            # do your own stuff here

Choosing a form in a streamfield
--------------------------------

The below is an example of a page model with the form block in a stream
field. It inherits from our form submission mixin fo that the forms can
be posted to the page they appear on.

::

    from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailcore.models import Page
    from wagtailstreamforms.blocks import WagtailFormBlock
    from wagtailstreamforms.models import StreamFormPageMixin


    class BasicPage(StreamFormPageMixin, Page):

        body = StreamField([
            ('form', WagtailFormBlock())
        ])

        content_panels = Page.content_panels + [
            StreamFieldPanel('body'),
        ]

Example site with docker
------------------------

Run the docker container

.. code:: bash

    $ docker-compose up

Create yourself a superuser

.. code:: bash

    $ docker exec -it <container_name> bash
    $ python manage.py createsuperuser

Go to http://127.0.0.1:8000

Testing
-------

Install dependencies

You will need pyenv installed see https://github.com/pyenv/pyenv

Also tox needs to be installed

.. code:: bash

    $ pip install tox

Install python versions in pyenv

.. code:: bash

    $ pyenv install 3.4.4
    $ pyenv install 3.5.3
    $ pyenv install 3.6.2

Set local project versions

.. code:: bash

    $ pyenv local 3.4.4 3.5.3 3.6.2

Run the tests

.. code:: bash

    $ tox

or run for a single environment

.. code:: bash

    $ tox -e py36-dj111-wt112

.. |CircleCI| image:: https://circleci.com/gh/AccentDesign/wagtailstreamforms/tree/master.svg?style=svg
   :target: https://circleci.com/gh/AccentDesign/wagtailstreamforms/tree/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/AccentDesign/wagtailstreamforms/badge.svg?branch=master
   :target: https://coveralls.io/github/AccentDesign/wagtailstreamforms?branch=master
