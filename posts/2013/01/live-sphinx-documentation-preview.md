<!--
.. title: Live Sphinx Documentation Preview
.. date: 2013/01/30 07:18
.. slug: live-sphinx-documentation-preview
.. tags:
.. link:
.. description:
-->


**Update** (_2013-04-23_): ``livereload`` now has a 'shell' compiler, which simplifies the ``Guardfile``. The post has been modified to reflect this.

## The big idea

I've been working with [Middleman][] quite a bit, and really enjoyed their integration with [livereload.js][].
When you save a change to a document you're working on, the content is regenerated, and the browser is pretty seamlessly reloaded (including preserving the point you're scrolled to.)

I'm now in the process of writing a lot of technical documentation with [Sphinx][], including sequence diagrams with [PlantUML][] and graphs with [Graphviz][], so doing:

1. Save file in editor
2. `make html`
3. ⌘-Tab to the browser
4. ⌘ R

... was getting old when I'd been used to Middleman, where all you need to do is step **1**.

I wanted a Python tool for this, since I didn't want to make other people working on these documents to need to have both working Python and Ruby environments. Thankfully, there's [python-livereload][]. The only problem was that a Sphinx documentation tree looks like

```
    sphinx/
        build/
            html/
            latex/
        source/
```

and by default, `python-livereload` wanted to watch and serve from only the current working directory. One small [pull request][] later and the problem was fixed.

## Using it

It's as easy as:

1. Install python-livereload
2. Create a `Guardfile`
3. Tweak the Sphinx `Makefile`

### Install livereload

This part's easy.

```
    $ pip install livereload
```

(or however else you like to install python modules.)

If it's already installed, upgrade it -- newer releases have some required features.

### Create a Guardfile

Create this file in the root of your [Sphinx][] documentation tree. (Next to the `Makefile`.)

``` python
#!/usr/bin/env python
from livereload.task import Task
from livereload.compiler import shell

# You may have a different path, e.g. _source/
Task.add('source/', shell('make html'))
```

### Run livereload

I chose to do this from the `Makefile`, so I get a new target: `make livehtml`.
You have to make changes in 3 different spots in the file:

``` make
# Add the new target to the other .PHONY targets.
.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext livehtml

# Add a note to the help
@echo "  livehtml   build html and point livereload server at them"

# And now the target; depends on 'make html', since livereload will only build if things change.
# We need to make sure the docs are current with any existing changes
livehtml: html
    livereload -b $(BUILDDIR)/html
```

So all you have to do is

```
$ make livehtml
```

and start editing.

The `-b` option was another pull request; it will actually open the browser and point it at `localhost:<port>`, which is a feature I'd never seen in other livereload implementations, but seemed quite convenient.

### Enjoy!

You still need to navigate to the page that you're editing, though I discussed some ways to support 'jump to the last file I edited' with the `python-livereload` author. But after that, sphinx will rebuild, and your content will be updated, every time you save a file.

[PlantUML]: http://plantuml.sourceforge.net/sequence.html
[Graphviz]: http://www.graphviz.org/
[Sphinx]: http://sphinx-doc.org
[python-livereload]: https://github.com/lepture/python-livereload
[livereload.js]: https://github.com/livereload/livereload-js
[Middleman]: http://middlemanapp.com/
[pull request]: https://github.com/lepture/python-livereload/pull/16
