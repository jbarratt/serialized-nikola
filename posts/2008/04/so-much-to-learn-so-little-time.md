<!--
.. title: So much to learn, so little time.
.. date: 2008/04/18 13:37
.. slug: so-much-to-learn-so-little-time
.. tags:
.. link:
.. description:
-->

I am looking at my lists of [books to read](http://www.goodreads.com/review/list/702622?shelf=to-read) and [books I'm actually reading](http://www.goodreads.com/review/list/702622?shelf=currently-reading) and feeling a little overwhelmed by how much good stuff there is to do right now.

I'm learning [linux HA](http://www.linux-ha.org/), which is going well. I needed to do something that probably could have been done in a r1-style config, but I went with a CRM r2 style config because having owned that, I can do way more interesting things. One very useful model is the loadbalancerless cluster. For 'N' servers, assign 'N' IP's with heartbeat ensuring that each IP will be hosted SOMEWHERE, preferring a server that either (a) doesn't have one, or (b) has lower load. Set up all these IP's in Round Robin DNS. That way if you lose a server, the most lightly loaded server with grab it's additional IP. Availability and simple load balancing without additional hardware. (Obviously suitable to only certain kinds of workloads, but interesting.)

We're moving away from home-rolled configuration management, and [puppet](http://reductivelabs.com/projects/puppet/) looks like the best next thing, which means it's finally time to learn Ruby so we can get more of our magic working.

And, now that we have more Solaris around,  I'm spending more time with [Dtrace](http://en.wikipedia.org/wiki/DTrace) which means learning more about Solaris internals so I can learn true ninja status.

I'm pushing more and more into automated testing and deployment and making things repeatable, so there's always things to learn about packaging, testing, and deployment -- we have a test [ganeti](http://code.google.com/p/ganeti/) cluster running which is helping with some of that.

So there's tons of data flying around and I want to be grabbing (and crunching), so we might as well be using the funding over at yahoo -- [hadoop](http://hadoop.apache.org/core/) and [hbase](http://wiki.apache.org/hadoop/Hbase) are on the list for sure.

Then of course visualization is a big deal when you're trying to understand data, so you'll see some books on [processing](http://processing.org/) and I'm also really looking at [nodebox](http://nodebox.net/code/index.php/Home).

And the web is changing -- apache is looking more and more like your dad's big lumbering caddy compared to [lighttpd](http://www.lighttpd.net/) and [nginx](http://nginx.net/). Toss [varnish](http://en.wikipedia.org/wiki/Varnish_cache) and some horizontal filesystem magic in the form of [mogilefs](http://www.danga.com/mogilefs/).

And then there are things that are just cool -- I already wanted to learn [haskell](http://www.haskell.org/) due to it being functional without parentheses eye-bleeding, and it being what parrot is based on -- but now I found out I [know one of the creators](http://www.flickr.com/photos/harmoniousmanic/2419342543/in/set-72157604581860717/).

WHY, world, WHY? WHY MUST YOU BE SO FILLED WITH AWESOME AND SO DEVIOD OF TIME?

That is all.
