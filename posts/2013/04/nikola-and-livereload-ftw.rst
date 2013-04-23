.. link: 
.. description: 
.. tags: 
.. date: 2013/04/23 14:35:47
.. title: Nikola and Livereload, dynamically editing a static site
.. slug: nikola-and-livereload-ftw

I've blogged about `using python-livereload </2013/01/live-sphinx-documentation-preview/>`_ before. It's a great little tool which

* given a tree of directories and files, watches them for changes, then takes some action when they happen
* serves up another directory of content to a browser, and pushes a little websocket notification to it when the content's updated, so it can reload.

This is perfect for `Nikola <http://nikola.ralsina.com.ar/>`_, the static blog
and site generator that I use for this very site.

Normally, you

* update your content
* ``nikola build``
* ``nikola serve``
* check it out in your browser, going to http://localhost:8000 and, if you
  already have it up, hitting reload.


With ``livereload``, you just:

* run ``livereload -b output``
* write!

Your changes show up live in the browser.

How To
======

Install ``livereload``
~~~~~~~~~~~~~~~~~~~~~~

.. code:: 

    $ pip install livereload

If you'd installed it before, now is a good time to upgrade.

Create a ``Guardfile``
~~~~~~~~~~~~~~~~~~~~~~

Put a file like this in your top level nikola directory. (The same one you
usually run ``nikola build`` from.)

.. code:: python

    #!/usr/bin/env python
    from livereload.task import Task
    from livereload.compiler import shell

    for path in ['conf.py', 'files/', 'galleries/', 'plugins/', 'posts/', 'stories/', 'themes/']:
        Task.add(path, shell('nikola build'))

You may want to customize the list of files and directories here; these are the
ones in my install that contain content I edit.

Run it
~~~~~~

From the directory now containing the ``Guardfile``, 

.. code::

    $ livereload -b output

This will

* Pick an unused high port
* start a web server serving the contents of your output/ folder on said high
  port
* Open a new tab in your primary browser with that page loaded.

So navigate to the post you're working on, start writing, and the browser will
always have the latest version. This is also great for working on themes,
plugins, or anything at all that ``nikola build`` can detect.
