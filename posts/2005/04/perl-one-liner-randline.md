<!--
.. title: perl one-liner; 'randline'
.. date: 2005/04/20 13:37
.. slug: perl-one-liner-randline
.. tags:
.. link:
.. description:
-->

I have a directory on my hard drive which has a fair quantity of multimedia content. Occasionally, my listening choices (ok, I gave it away) get somewhat stale. Scrolling through a list of -- well, quite a few choices can be somewhat daunting. I thought "hey! What if I chose entries at random for consideration! I'm sure there's a what I can do that with some shell mumbo-jumbo."

Turns out to be possible, but you need some sed fu, and why not use perl.

So now I can type

``` console
$ ls | randline
```


and get a random selection from the list. If I want to go all crazy and not even screen it, I can go with 

``` console
$ xmms -e `ls | randline`.
```


Here's the `.bashrc` entry I used:

``` bash
    alias randline="perl -we 'srand ; rand(\$.) < 1 && (\$line = \$_) while <STDIN>; chomp(\$line); print \"\$line\\n\";'"
```


The 'guts' came from an entry in the [Perl Cookbook](http://www.unix.org.ua/orelly/perl/cookbook/ch08_07.htm), worth checking out due to their description of how it actually works. It's a neat idea. Basically, you look at each line one by one. Each time you do you have a 1/(line number) chance of choosing that line as the one you'll output. So if you just have one line, you've got a 1/1 chance of choosing that line. If you have 2, you start out with a taking the first line, and then having a 1/2 chance of picking the second -- giving you 50/50 odds you'll have either the first or the second. It extends nicely.

Anyway, thanks to this, I'm currently listening to a cd I forgot I bought years ago which I'm really digging, fit my mood perfectly. [The Blue Moods of Spain](http://www.amazon.com/exec/obidos/ASIN/B000003BKZ)
