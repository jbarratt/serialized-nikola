<!--
.. title: Permanently converting from textile markup
.. date: 2009/01/06 13:37
.. slug: permanently-converting-from-textile-markup
.. tags:
.. link:
.. description:
-->

So, I have resurrected the blog!

There were some victims -- at one of the transitions along the way, many of my posts got truncated to just 'summary' length and the 'real data' is gone. (Moment of silence.) Moving on to brighter and better things.

Wordpress was able to connect to my textile database and inhale all my posts. (Thanks!) Unfortunately, it was all in Textile markup. [And they didn't seem to plan on supporting that.](http://faq.wordpress.com/2006/04/20/markdown-textile/) 

What to do? 

I made a quick YAML config to store database options in, config.yml:
``` yaml
    ---
    dbserver: mydbserver.com
    dbuser: mydbuser
    dbpass: doilookthatdumb
    db: my_wp_db
    dbtable: wp_posts
    dbcolumn: post_content
    dbkeycolumn: ID 
```

I didn't hard code it in the doc so I could generically do this kind of thing later if I wanted.

And then, the cowboy perl to inhale the markup and go from Textile to HTML, using the handy [Formatter::HTML::Textile](http://search.cpan.org/~kjetilk/Formatter-HTML-Textile-0.7/lib/Formatter/HTML/Textile.pm):

``` perl
    #!/usr/bin/perl

    use strict;
    use warnings;

    use YAML qw(LoadFile);
    use DBI;
    use Formatter::HTML::Textile;

    my $c = LoadFile("config.yml");

    my $dbh = DBI->connect("dbi:mysql:$c->{db}:$c->{dbserver}",$c->{dbuser},$c->{dbpass}) || die "Can't connect to database: $!\n";

    my $q = "select $c->{dbkeycolumn},$c->{dbcolumn} from $c->{dbtable}";
    my $uq = "update $c->{dbtable} set $c->{dbcolumn} = ? where $c->{dbkeycolumn} = ?";

    my $sth = $dbh->prepare($q);
    my $usth = $dbh->prepare($uq);

    $sth->execute;
    while (my ($key,$text) = $sth->fetchrow_array) {
        my $formatter = Formatter::HTML::Textile->format( $text );
        my $newtext = $formatter->fragment();
        $usth->execute($newtext, $key);
    }
```

And in a fraction of a second, all my old blog posts were converted, in all their (arguable) glory. From now on I'm only blogging in XHTML, suckers.

Update: 08/2010, moment of silence as I am back-converting from HTML to Markdown. Sigh.
