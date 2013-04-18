<!--
.. title: Wordpress Plugins and external services
.. date: 2009/04/15 13:37
.. slug: wordpress-plugins-and-external-services
.. tags:
.. link:
.. description:
-->

I noticed this blog was slow from time to time, and decided to do a bit of investigation.

That took the form of a very very sweet hack that I will publish at a later date, but for now I'll just share some of the results.

In the sidebar I am using pretty standard WordPress plugins to load in
<ul>
<li>my latest images from Flickr</li>
<li>my latest tweets from Twitter</li>
<li>my recent bookmarks from del.icio.us</li>
</ul>

These plugins are all implemented as server-side fetches.

Here's the thing, those services aren't always very fast. For example, on a recent run I got these results:

<table>
<tr><th>Host</th><th>Service</th><th>Load Time</th></tr>
<tr><td>128.121.146.228</td><td>Twitter</td><td>1.831s</td></tr>
<tr><td>fe.feeds.del.vip.ac4.yahoo.net</td><td>del.icio.us</td><td>1.148s</td></tr>
<tr><td>www.flickr.vip.mud.yahoo.com</td><td>Flickr</td><td>0.274s</td></tr>
</table>

I guess I need to either switch to using an in-browser widget model, or cron a fetch of that data locally on some reasonable interval. That might be a nice service for WordPress to have internally for widget authors: 'cron/cache mode.' Provide a URL to curl periodically that updates the caches on all your active widgets, as well as a global configuration about how fresh you want your data to be.

I don't care if any of those results are more than an hour up to date, I'd much prefer to have my page load time cut by **3.24 seconds** than have it be up-to-the second accurate.
