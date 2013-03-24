<!--
.. title: Great WordPress Plugin: WP Widget Cache
.. date: 2009/10/24 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

Using [WP Widget Cache](http://wordpress.org/extend/plugins/wp-widget-cache/), I improved my site load time by about 600% by just starting to cache the widgets.

Here are some screenshots from my strace-based 'magic profiler' (which I still promise to talk more about later.)
It lets you attach to a process which is about to render your website, and then trace all the interactions it has with the underlying system while it renders it.

That includes network traffic, file server traffic, DNS resolver lookups -- everything your app does to communicate to the outside world. The timing is always going to look slower than normal (at least a bit) as the tracing does impose some overhead, but it's relatively pretty accurate.

Here's what I saw right after telling WP Widget Cache to clear the caches.

![With a freshly cleaned Widget cache](/images/serialized_net_cleared_cache.jpg "With a freshly cleaned Widget cache")

And here is what I saw on the second hit:

![With WP Widget Cache working like it should](/images/serialized_net_widgets_cached.jpg "With WP Widget Cache working like it should")

I have widgets to load Flickr, (the entry with 'flickr' in it) delicious bookmarks, (the yahoo one) and Twitter. (The naked IP. Apparently they don't like PTR records.) Those three external calls dominated my total time to generate the page. Now, it's down to a very quick MySQL lookup and a chatty conversation with a fileserver.

One feature I especially appreciate is the ability to tune cache times per widget. If I want new Flickr photos to be available hourly, sure. If my tweets need to be there within 5 minutes, not a problem. And because the widgets are there every time anyone uses any part of the site (even the rarer ones) it plays really well with the other WP Cache Plugins.
