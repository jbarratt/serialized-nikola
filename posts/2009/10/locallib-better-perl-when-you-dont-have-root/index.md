<!--
.. title: local::lib: Better perl when you don't have root.
.. date: 2009/10/19 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

These days as we move increasingly to 'the clouds', it's becoming common to get a server where you've got local root. However, those (from a provider and a user perspective) aren't always the best way to go. Those are more expensive to provide (dedicated IP's, more dedicated resources on the server) and thus more expensive to buy. Also, in some use cases they might not scale so well if you're buying a lower end one -- if you buy 256MB of RAM, it's pretty easy to push that into the red. On the administration side, the bar is raised for what you need to be able to do to solve simple problems. Adding an email account, or setting up the web server -- all of these are solvable, and control panels can help, but what if you just want to serve some content? Why deal with it?

So, we still have shared hosting, in it's various forms. I like the [(mt) Grid Server](http://mediatemple.net), but I will admit to being biased (a lot.)

So with shared hosting, you don't have root. And managing software you need (to get useful web applications up and running) can be a pain -- a lot of the documentation is biased towards the idea that you have a full server, be it virtual or physical.

If you don't have root on your server, and you're using perl (for any of the amazing Modern Perl tools and stacks out there,) I recommend checking out the awesome [local::lib](http://search.cpan.org/perldoc?local::lib).

Once you follow their 'bootstrapping config' and set up your bashrc, it makes things feel like you're on your own server. Just 'cpan -i WordPress::Post' or './Build install', and it just works!

So a full install using local::lib would look like:
Download and unpack local::lib:
(Warning, update the link to the latest version, this is the current release:)
{% codeblock lang:console %}
$ mkdir tmp
$ cd tmp
$ wget http://search.cpan.org/CPAN/authors/id/A/AP/APEIRON/local-lib-1.004008.tar.gz
$ tar -zxvf local-lib-1.004008.tar.gz
{% endcodeblock %}

cd into the local::lib directory, and then run:
{% codeblock lang:console %}
$ perl Makefile.PL --bootstrap
$ make test && make install
$ echo 'eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)' >>~/.bash_profile
$ . ~/.bash_profile
{% endcodeblock %}

And you're done! Every time you ssh in, your environment will be set up to use your whole local tree. So even if you want perl's New Fancy Hotness, all it takes is:
{% codeblock lang:console %}
$ cpan -i Moose
{% endcodeblock %}

One caveat if you're using local::lib and trying to run this tool from cron, is that you'll probably want to use a wrapper script to correctly set up the environment. (Sometimes you'll need to set up the environment for your web apps, too -- that can be done via .htaccess.)

Here's an example wrapper script, set up to work on my MediaTemple (gs) account and work with my local::lib setup:
{% codeblock lang:bash %}
#!/bin/bash

#set up environment
HOME=/home/12345/users/.home
eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)

# run the script
$HOME/perl5/bin/mycron.pl
{% endcodeblock %}

To make things work with your webapp, you need some 'SetEnv' commands in the .htaccess. You can do this by just loading the local::lib module and checking the output:
{% codeblock lang:console %}
$ perl -I$HOME/perl5/lib/perl5 -Mlocal::lib 
export MODULEBUILDRC="/home/12345/users/.home/perl5/.modulebuildrc"
export PERL_MM_OPT="INSTALL_BASE=/home/12345/users/.home/perl5"
export PERL5LIB="/home/68601/users/.home/perl5/lib/perl5:/home/12345/users/.home/perl5/lib/perl5/i386-linux-thread-multi:$PERL5LIB"
export PATH="/home/12345/users/.home/perl5/bin:$PATH"
{% endcodeblock %}

Each one of those EXPORT statements needs to become a SetEnv statement.
{% codeblock lang:text %}
# so this:
#export MODULEBUILDRC="/home/12345/users/.home/perl5/.modulebuildrc"
# becomes:
SetEnv MODULEBUILDRC "/home/12345/users/.home/perl5/.modulebuildrc"
{% endcodeblock %}

Repeat that for each one of the variable 'export' lines, and you should be good to go! Affordable, scalable, low management overhead shared hosting and an easy way to get modern perl. 
