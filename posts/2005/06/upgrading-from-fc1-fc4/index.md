<!--
.. title: Upgrading from FC1->FC4
.. date: 2005/06/15 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

I've just upgraded my trusty laptop from Fedora Core 1 (FC1) to Fedora Core 4 (FC4), and thought I'd use this to just note down a few of the problems I had and the solutions. The upgrade itself was pretty painless -- or would have been if I'd not been lazy and skipped checking my media. CHECK THE MEDIA.

First, yum wasn't installed. All this required was a trip to a fedora FTP server and a download of yum and some support staff:

* python-elementtree
* python-urlgrabber
* python-sqlite

Next, evolution came up showing no internal icons whatsoever. (all the spaces where they would have been were jarring 'red x' icons like you see when IE can't load an image.)
The fix, after some judicious strace'ing, was that for some reason there were no 'stock' links in the gnome icons tree. I just populated them with the 'hicolor' stock links and Evolution is happy happy.


{% codeblock lang:console %}
$ cd /usr/share/icons/gnome ; for i in *[0-9]x* ; do pushd $i ; ln -s /usr/share/icons/hicolor/$i/stock/ ; popd ; done
{% endcodeblock %}

This is all still in progress -- the #1 priority was getting the latop to where I could use it, as it's my only work machine at the moment.
