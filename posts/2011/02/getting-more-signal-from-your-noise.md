<!--
.. title: Getting more Signal from your Noise
.. date: 2011/02/24 13:37
.. slug: getting-more-signal-from-your-noise
.. tags:
.. link:
.. description:
-->


At [SCALE 9x](http://www.socallinuxexpo.org/scale9x/) I presented a talk in the DevOps track called [Getting more Signal from your Noise.](http://www.socallinuxexpo.org/scale9x/presentations/signal-noise).
You can download the slides  ([with notes](/images/Signal_Noise_With_Notes.pdf), [without notes](/images/Signal_Noise_No_Notes.pdf)), and this is a companion post which contains links and further information.
I'd recommend reviewing that before reading more, as I won't rehash what I covered there.
Due to the 30 minute timebox, I cut out even discussing a few large areas that I can address (briefly) here.

# The Point

* Data + Open Source is an explosively growing field.
* The complexity of our software systems -- the way we deliver applications and services -- is exploding.
* The number of people trying/needing to build systems like this is exploding. (Not just Flickr and Facebook anymore.)
* The demands on our time and attention are exploding.
* The data that's available to us from our infrastructures AND the "world around" (finance, customers, social media, etc) is exploding

The other thing that's exploding are the number of businesses who will provide you some form of "shrink-wrapped" delivery of the kinds of tools (or at least results) discussed here. Depending on your business, going DIY and duct-taping together what you need may be the wrong idea. However, there are a few major reasons that DIY *can be* a good idea.
* Flexibility: We are learning every day the kinds of things we need our systems to tell us in a hurry. Being able to quickly tune them makes a difference.
* Latency and Connectivity: When you're using a system for real-time decisionmaking, at least having it on-premise means you can throw GB/sec at it, and have results in seconds.


# The Data Stack

In the talk, I introduced a model for thinking about what types of functionality the different tools available provide.

* Collect
* Transport
* Process
* Store
* Present

Many tools provide just one part of this stack, but more than that are 'hybrids'. Getting the data you need often means mixing and matching.

I called out [graphite](http://graphite.wikidot.com/), [collectd](http://collectd.org/), [OpenTSDB](http://opentsdb.net/), [reconnoiter](https://labs.omniti.com/labs/reconnoiter), [esper](http://esper.codehaus.org/), and [protovis](http://vis.stanford.edu/protovis/) as being particularly worth at least knowning about.

Other projects and ecosystems worth studying:

## Hadoop

The literal elephant in the room that I discussed only tangentially, [Hadoop](http://hadoop.apache.org/) (and the huge family of tools around it) can be an incredible asset to learning more about your world via storing/managing/questioning your data. [Cloudera](http://www.cloudera.com/) remains a great source of both software and education, and is a good place to start.

It's now possible to get real-er time information from a Hadoop system, but historically it's been essentially for things that are more time sensitive on the 1-day/1-month time range. (Trends, capacity, etc.)

## Log Processing and Management

The state of the art with log management used to be syslog + logrotate = done. There are a lot more options today.

* Many people are using [HDFS](http://hadoop.apache.org/hdfs/) (before or after processing) for both it's scalability, resilience, and ability to integrate with the larger Hadoop family. Orbitz (awesome at sharing, first graphite, now this) have a great [presentation about 'Hadoop for Logs'](http://files.meetup.com/1634302/CHUG_HadoopLogsAtOrbitz.pdf) which is a good overview of what you'd be getting into.
* [Logstash](http://code.google.com/p/logstash/) and [graylog2](http://www.graylog2.org/) can bring some of the utility of Splunk without the (ahem) cost structures. While graylog2 stores data in MongoDB, Logstash can optionally use [ElasticSearch](http://www.elasticsearch.org/), which is a nicely packaged "throw text in and RESTfully search" engine. (Thanks to the author of Graylog2, [@lennart](http://twitter.com/_lennart), for clarifying that.) [@timetabling](http://twitter.com/timetabling) suggests you can [glue ElasticSearch to MongoDB](http://www.elasticsearch.org/blog/2010/02/25/nosql_yessearch.html), so that when the data changes you index it -- but out of the box, that's not an option.
* A new entrant, [Luwak](https://github.com/basho/luwak) runs on top of Riak, so you get the availability + scalability and a Map/Reduce interface to boot.
* [Flume](https://github.com/cloudera/flume) and [Scribe](https://github.com/facebook/scribe) (as well as messaging systems like [RabbitMQ](http://www.rabbitmq.com/)) can replace syslog as the way to shovel raw logs around.
* Google's [Sawzall](http://code.google.com/p/szl/) is more on the processing side, but it allows you to describe patterns of information you want from your logs, and then in a map/reduce-like way aggregate them.

## Data Analysis

A basic-to-advanced knowledge of statistics is becoming essential. There are powerful tools (like [R](http://www.r-project.org/), and many libraries available for different languages like [SciPy](http://www.scipy.org/)) -- but if you don't know what operation you want them to do, they won't help.

Our tax dollars have actually provided a pretty useful introduction, the [NIST Handbook](http://www.itl.nist.gov/div898/handbook/).
I have been overwhelmingly happy with how useful the book [Data Analysis with Open Source Tools](http://amzn.to/hFzX8H) has been -- it takes some decent energy to get through, especially if your background is not so math/dev heavy, but it's insanely rewarding.

## Machine Learning

"Machine Learning" is still a pretty intimidating thing to Google for unless you've got a C.S. PhD. However, it's starting to be packaged and democratized enough that mere mortals can start to play.

[Apache Mahout](http://mahout.apache.org/) has a lot of potential to be of tremendous use here. Many people are using it more in text-related spaces, but the ability to find patterns and trends across multiple disparate systems is exactly what we need for things like botnet combat. I've just started looking at this and so far am very inspired to dig further. 

# People to Watch

This is a by-no-means-comprehensive list of the people whose tweets, software, and writing I've found useful to keep exploring the possibilities and pitfalls here:

* [Jordan Sissel](http://www.semicomplete.com/) (author of [Logstash](http://code.google.com/p/logstash/), [Grok](ihttp://code.google.com/p/semicomplete/wiki/Grok) and [Fex](http://semicomplete.com/projects/fex/))
* Strata (The ORA Data Conference) Speakers: [Lanyrd List](http://lanyrd.com/2011/strata/speakers/) (and Lanyrd's awesome [Writeup List](http://lanyrd.com/2011/strata/writeups/)).
* [Dr. Neil Gunther](http://www.perfdynamics.com/Bio/njg.html)
* [Patrick Debois](http://twitter.com/patrickdebois)
* [Regis Giadot](http://regis.gaidot.net/)
* [Theo Schlossnagle](http://lethargy.org/~jesus/about.html)
* [Percona](http://www.percona.com/) (Including the very nice implementation of Dr. Gunther's [Universal Scalability Law](http://aspersa.googlecode.com/svn/html/usl.html))

# And so

Short of a series of books, updated monthly, all I can really provide is an appetiser. Hopefully you've been inspired to move on to your own data hacking "main course."
