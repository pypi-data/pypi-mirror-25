Piglet Template Engine
======================

Piglet is a text and HTML template engine in the kid/genshi/kajiki templates
family.

The Piglet template engine offers:

- Template inhertitance through py:extends/py:block (similar to Jinja2)
- Compiles templates to fast python byte code.
- HTML aware templating: output is well formed and content is
  escaped, preventing XSS attacks.
- Reusable template functions, deep nesting of template inheritance,
  flexible translations and embedded python expressions

`Documentation <https://ollycope.com/software/piglet/>`_
\| `Bitbucket repository <https://bitbucket.org/ollyc/piglet>`_

This is what a piglet template looks like:

.. code:: html

    <py:extends href="layout.html">

        <py:block name="content">
            <h1>This is the content block.</h1>
            <p>
                Hello $user.firstnames $user.lastname!
            </p>

            <!--!
              The following paragraph is marked for translation.

              The i18n:name attribute substitues the python code interpolation
              with a simple placeholder, so translators see this message:

                'Today is ${day}'
            -->
            <p i18n:message="">
              Today is <span i18n:name="day">${date.strftime('%a')}</span>.
            </p>

            <p py:choose="today.weekday()">
                <py:when test="0">
                    I don't like Mondays
                </py:when>
                <py:when test="day == 4">
                    I never could get the hang of Thursdays
                </py:when>
                <py:otherwise>Is it the weekend yet?</py:otherwise>
            </p>

            <p py:for="verse in in poem">
                <py:for each="line in verse">$line<br/></py:for>
            </p>

        </py:block>


There's a text templating mode too:

.. code::

    Hello $user.firstnames $user.lastname!

    {% trans %}
    Today is {% transname "day" %}${date.strftime('%a')}{% end %}
    {% end %}.

    {% for verse in poem %}
        {% for line in verse %}$line
        {% end %}
    {% end %}


Installation
------------

To install the latest release using pip (recommended):

.. code:: sh

    pip install piglet


To install the latest source:

.. code:: sh

    hg clone https://bitbucket.org/ollyc/piglet
    cd piglet
    python setup.py install



Rendering templates from the Python API
---------------------------------------

A simple example of rendering a template from python code:

.. code:: python

    from piglet import HTMLTemplate

    template = HTMLTemplate('<p>$greeting</p)')
    print(template.render({'greeting': 'Bonjour!'}))


Loading templates from disk:

.. code:: python

    from piglet import TemplateLoader

    loader = TemplateLoader(['./templates/'])
    template = loader.load('mytemplate.html')
    print(template.render({'greeting': 'Hello!'})


A fully loaded example:

.. code:: python

    from piglet import TemplateLoader
    import gettext

    loader = TemplateLoader(
        # List of directories to search for template files
        ['./templates/'],

        # Auto reload templates when files are modified? Defaults to False,
        # use True for development
        auto_reload=True,

        # The template class to use - either HTMLTemplate or TextTemplate
        template_cls=HTMLTemplate,

        # File encoding to use by default
        default_encoding='UTF-8',

        # A persistent on disk cache for piglet templates
        cache_dir='.cache/piglet'

        # A factory function returning a gettext Translations instance
        # or compatible object. For example Django users could plug in
        # `lambda: django.utils.translation`. If your app isn't translated
        # omit this argument.
        translations_factory=lambda: gettext.translation(...),

    )
    template = loader.load('mytemplate.html', encoding='UTF-8')

Templates can also be rendered as a stream. This might be useful for generating
long documents that you don't want to hold in memory all at once:

.. code:: python

    template = loader.load('huge.html', encoding='UTF-8')
    for s in template({'data': load_massive_dataset()}):
        sys.stdout.write(s)



Inheritance
-----------

The layout template should be marked up with `<py:block>` tags
to indicate customization points:

.. code:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title py:block="title">Default title</title>
    </head>
    <body>
        <py:block name="content">
        Content goes here
        </py:block>
    </body>
    </html>


Child templates then use ``<py:extends href="...">`` to pull in the parent's
layout.


You can also define template functions:

.. code:: html

    <!--! File: widgets.html
    -->
    <py:def function="modal(content, title='hello')">
        <div class="modal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" data-dismiss="modal">X</button>
                        <h4 class="modal-title">$title</h4>
                    </div>
                    <div class="modal-body">
                        ${content() if callable(content) else content}
                    </div>
                    <div class="modal-footer">
                        <button type="button">Close</button>
                        <button type="button">Save changes</button>
                    </div>
                </div>
            </div>
        </div>
    </py:def>


Template functions can be imported into other templates:

.. code:: html

    <py:import href="widgets.html" alias="widgets"/>
    <p>
        ${widgets.modal(content="Hello world!")}
    </p>


Did you notice the ``${content() if callable content else content}``
interpolation in the function body? That's to support ``py:call``, which can
pass chunks of template code as keyword arguments:

.. code:: html

        <py:call function="widgets.modal(fullpage=True)">
            <py:keyword name="content">
                This is the modal content. You can include
                <a href="#">markup here</a> too!
            </py:keyword>
        </py:call>


License
-------

Piglet is licensed under the Apache license version 2.0.

Piglet is developed by
`Olly Cope <https://ollycope.com/>`_
and was created for `skot.be <https://skot.be/>`_
