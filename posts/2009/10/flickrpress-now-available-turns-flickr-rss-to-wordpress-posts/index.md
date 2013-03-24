<!--
.. title: FlickrPress now available: Turns Flickr RSS to Wordpress Posts
.. date: 2009/10/16 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->


**Update**: This software is no longer maintained (and is a lot less important now that there is oEmbed support, to be honest.)

I'm leaving the legacy content here for a record... the code is still available on [github](http://github.com/jbarratt/FlickrPress).

---------------------

My wife and I like to post a lot of photos of our son to [his blog](http://carterbarratt.com).

![Carter's Site](/images/carterbarratt_dontlikethiseither.jpg)

After using WordPress from both the browser and the iPhone client, I just wasn't that happy using it for our pictures. On the other hand, we both love (and already use, and have Pro accounts on) Flickr.

Having the photos "live" on Flickr means some handy things.
<ol>
<li>They let you get an RSS feed of a tag. (We use 'carterbarratt.') This means we don't even have to use an API key, which is convenient.</li>
<li>They always have an image available that's sized to 500 on the longest side. This turns out to be a perfect image size (either height or width) for a lot of WordPress themes.</li>
<li>They handle video and make the thumbnails look exactly like a "non-video image" in the RSS feed.</li>
<li>Lots of things can upload to Flickr -- we use mostly the desktop uploader (after exporting from Lightroom) and the new Flickr native client on our iPhones.</li>
<li>The exact same stuff (title, description) that I'd want on a photo blog is available when I upload to Flickr.</li>
</ol>

So, FlickrPress was born. It's a fairly simple perl script, intended to be run as a cron job, which uses [WordPress::Post](http://search.cpan.org/perldoc?WordPress::Post) to create new blog posts for every flickr photo it finds with a certain tag, from certain users.

![FlickrPress Workflow](/images/FlickrPress-flow.png)

