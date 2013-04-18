<!--
.. title: A simple Taskwarrior Alfred Plugin
.. date: 2012/09/05 14:50
.. slug: a-simple-taskwarrior-alfred-plugin
.. tags:
.. link:
.. description:
-->


### The plugin

I [recently wrote](/2012/09/migrating-from-trello-to-taskwarrior/) about using Taskwarrior for tracking my tasks. One of the things I'd really liked about Omnifocus was the [quick entry](http://www.omnigroup.com/blog/entry/omnifocus-at-school-quick-entry#!prettyPhoto), which allowed (with a hotkey) for capturing tasks -- even setting projects, contexts, priorities, due dates, etc.

Even though I love working with Taskwarrior on the command line, I'm not always at the command line -- and in fact the majority of my tasks are generated when I'm out of that wonderfully productive space. (Main culprits of course being email and Skype.) Especially when pixel constrained, it's not actually that awesome to juggle a Gmail window and a Terminal window.

I use [Alfred](http://alfredapp.com) to get me quick access to application launching, web searching, and awesomely [controlling Spotify](https://github.com/phpfunk/alfred-spotify-controls), so I (using Alfred) Googled for Alfred Taskwarrior integration. Oh hey, look, some [guy on hacker news](http://news.ycombinator.com/item?id=3437971) made it work, but didn't share the plugin, so I had to figure it out on my own.

So, I [made a plugin](https://github.com/jbarratt/AlfredTaskwarrior).

Installing is very simple, just download and run. The plugin is also very simple, you just launch Alfred and it passes everything after `task` to the task command, spitting the results (with ANSI color codes filtered out) back to you.

```
# launch Alfred
$ task add pay my rent
# growl returns something like 'Taskwarrior created task 88.'
$ task add pay my phone bill due:1wk recurs:monthly project:home.bills +sometags
```

That's all fine for simple task creation, but if you need to do more, there's a
nice way to get an interactive display that's built right into Alfred: launching
a terminal with `>`.

```
# launch Alfred
> task project:work burndown.daily
```

### Implementation notes

I didn't see much help in the documentation for actually packaging your Alfred extensions; they essentially point you at other people's code and say 'figure it out'.
Thankfully, that's pretty easy to do. But if you're reading this and you want to make your own extensions, you're welcome. I saved you some time.

The extension files are actually pretty simple: a `.zip` file with no folders in it, containing the
contents of the plugin directory, and named `.alfredextension`.

The contents are (at least the ones I've seen):

* `info.plist`: An OSX [plist](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/PropertyLists/UnderstandXMLPlist/UnderstandXMLPlist.html) file which describes the contents of what goes into the Alfred configuration plane. If this is a script, the body of the script is actually stored in this file.
* `icon.png`: An image file referred to by the plist, used for making your plugin look pro. (Extra cool, it pops up when you get growled at.)
* `kudos.plist`: Where you give yourself (and others) big props
* `update.xml`: Used by the Extension Updater, should have the URL of a file where the current version number can be obtained.
* `myversion.xml`: Points to the actual download location.

You can check out my plugin's repo for examples of all of these things.

I actually set up the repo like:

```
/README.md
/Makefile
/Taskwarrior.alfredextension
/extension
    /info.plist
    /icon.png
    /kudos.plist
    /update.xml
    /taskwarrior-version.xml
```

and the Makefile does the all work of actually building the file.

```
all: Taskwarrior.alfredextension
.PHONY: versionbump

Taskwarrior.alfredextension: extension/icon.png extension/info.plist extension/kudos.plist extension/*.xml
	zip Taskwarrior.alfredextension -j -r extension

versionbump: 
	perl -pi -e 's/(version>\s*\d+\.)(\d+)/$$1 . ($$2 + 1)/e' extension/*.xml
	$(MAKE) all
```

It's pretty handy; assuming any files have changed, `make` builds a new package, and `make versionbump` bumps the
version number (which needs to be kept in sync between the `-version.xml` and `update.xml` files), then builds the package.

That evil perl one liner just says to match a string like `version>1.2` and
replace it with one like `version>1.3`.

Shipping a tweak to the package to all my (**cough** no doubt millions of) users is as
easy as:

```
$ vi extension/info.plist # make some change to the script
$ make versionbump
    perl -pi -e 's/(version>\s*\d+\.)(\d+)/$1 . ($2 + 1)/e' extension/*.xml
    make all
    zip Taskwarrior.alfredextension -j -r extension
    updating: icon.png (stored 0%)
    updating: info.plist (deflated 54%)
    updating: kudos.plist (deflated 30%)
    updating: taskwarrior-version.xml (deflated 23%)
    updating: update.xml (deflated 23%)

$ git status
#       modified:   Taskwarrior.alfredextension
#       modified:   extension/info.plist
#       modified:   extension/taskwarrior-version.xml
#       modified:   extension/update.xml

$ git commit -a -m "stripped ansi codes in output so growl is happy"
$ git push origin master
```
