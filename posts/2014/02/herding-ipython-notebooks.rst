.. title: Herding IPython Notebooks
.. slug: herding-ipython-notebooks
.. date: 2014/02/27 15:07:13
.. tags: 
.. link: 
.. description: 
.. type: text

I've recently been using `IPython Notebook <http://ipython.org/notebook>`_
a lot. Enough that, if it was a chemical substance, people might be thinking
about staging an intervention.

It's the ideal tool for a lot of the work I end up doing -- ad-hoc data
analysis (and conversion), illustrated examples of techniques, coaching/training, and so on.

One issue that it currently has (at least in the stable v1 series) is that
you run an ``ipython notebook`` in a directory, and that lets you see all your
notebooks just in that directory. This is actually really nice for keeping your
work separate; keep a few notepads for python experiments in a private repo,
keep the notepads you're using for a given work project in another, and so on.

However, I hit the situation enough that I hopped into a directory of notebooks
and wondered 'am I already running a notebook server here?' that I created
a quick tool, that I share with you, dear reader.


You can grab `nblist <https://gist.github.com/jbarratt/ae8026493fedc79f122b>`_
from as a gist, and drop it in an executable directory.

It allows you to do 

::

    $ nblist
        http://127.0.0.1:8088 | /Users/me/work/notebooks
        http://127.0.0.1:8089 | /Users/me/work/otherproject
        http://127.0.0.1:8090 | /Users/me/work/employer/thirdproject

in a terminal. Bonus tip: ⌘--click on a URL in ``Terminal.app`` will open it in
the default system browser.


**Update 2014-08-22:**
My original version of nblist was OSX only and depended on scraping through
processes, looking at their environments, and checking which had open ports --
which worked, but was janky. Thanks to some feedback from `Thomas Kluyver
<https://twitter.com/takluyver>`_ on the mailing list, it's been improved so it
will work on all POSIX systems using techniques that will be exposed in IPython
3.x.
