=============================
django-n3-templateplugins
=============================

.. image:: https://badge.fury.io/py/dj-n3-templateplugins.svg
    :target: https://badge.fury.io/py/dj-n3-templateplugins

.. image:: https://travis-ci.org/Jaredn/dj-n3-templateplugins.svg?branch=master
    :target: https://travis-ci.org/Jaredn/dj-n3-templateplugins

.. image:: https://codecov.io/gh/Jaredn/dj-n3-templateplugins/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Jaredn/dj-n3-templateplugins

Extensible Template Plugins for Django

Documentation
-------------

The full documentation is at https://dj-n3-templateplugins.readthedocs.io.

Quickstart
----------

Install django-n3-templateplugins::

    pip install dj-n3-templateplugins

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_n3_templateplugins.apps.DjN3TemplatepluginsConfig',
        ...
    )

Features
--------

If you want to build an extensible platform, you may find the need to allow the developers that use your app to alter
or add on to the functionality that you provide.  This django package attempts to add 'plugin' functionality to
your django app.

To give an example of why I'm creating this... My company built an in-house django asset management system that we want to open-source, but there is a bunch of business-logic throughout the Templates and Views that wouldn't make sense in an open-sourced app.  So in order to open source our asset management system we needed to make our custom business-logic pluggable.  Plus, anyone that used our asset management system would probably want a similar feature for their own business logic.

How it works:

End-Users of your app create a 'plugin', which is just a Python Class which requires two methods to be created:

.. code-block:: python

    # plugin.py
    class Plugin(TemplatePlugin):
        def get_context_data():
            # How the plugin adds extra data to your Views/Templates
            return {'foo': 'some context'}

        def render_html():
            # How the plugin uses the context (and any provided by your view) to return HTML code (Full Django Template
            # syntax is allowed here!)
            return '<p><b>I am HTML</b> and I can use my context like this: {{ plugins.plugin_name.context.foo }}</p>'


These plugins get placed in the configurable directory:

.. code-block:: python

    # settings.py
    N3PLUGINS_PLUGIN_DIR = '/some/path/with/plugins'


You then use the provided decorator @load_plugins to decorate your views like this:

.. code-block:: python

    # views.py
    @load_plugins
    class TestView(ListView):
        model = SomeModel
        template_name = 'some_template.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plugins'] = self.plugins
            return context

This decorator will set a class property called self.plugins which is a dictionary.  You then use this at any point
in your view's code and make sure it gets added to the Context object that is passed in for Template rendering.


In your template you then use django-n3-templateplugins provided templatetag to render the plugin's html, which looks
something like this:

.. code-block:: python

    # some_template.html
    {% load render_plugin %}
    {% for k, v in plugins.items %}
        {% render_plugin v.plugin_object %}
    {% endfor %}

And that's it!

* TODO
* Note: This early implementation only works with class-based views (as we set a class property with a decorator. This
isn't possible with a function).

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
