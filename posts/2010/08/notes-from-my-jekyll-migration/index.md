<!--
.. title: Notes from my Jekyll Migration
.. date: 2010/08/29 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->


I had a few snags moving to Jekyll that I thought worth sharing.

### Lenny Support Packages

If you're using Debian Lenny, you won't complain about having these packages installed:

{% codeblock lang:console %}
$  sudo apt-get install ruby-dev  libyaml-ruby libzlib-ruby python-pygments libgsl-ruby1.8 sun-java6-jre
{% endcodeblock %}

### Local install of Gems

I didn't want to mess with my system gems, and wanted to have the gems installed in my local directory like I'm used to with Perl's [local::lib](search.cpan.org/perldoc?local::lib). 
This turned out to be harder than you may think. Here's the environment incantation that did the trick:

{% codeblock lang:bash %}
export RUBY_PREFIX="$HOME/.ruby"
export PATH="$RUBY_PREFIX/bin/:$RUBY_PREFIX/lib/ruby/gems/1.8/bin/:$PATH"
export GEM_HOME="$RUBY_PREFIX/lib/ruby/gems/1.8"
export GEM_PATH="$GEM_HOME"
export RUBYLIB="$RUBY_PREFIX/lib/ruby:$RUBY_PREFIX/lib:$RUBY_PREFIX/lib/site_ruby/1.8"
{% endcodeblock %}

And then I grabbed [RubyGems](http://rubyforge.org/frs/?group_id=126) and just

{% codeblock lang:console %}
$ ruby setup.rb all --prefix=$RUBY_PREFIX
{% endcodeblock %}

### Importing Wordpress

I also wanted to use a remote database that I didn't have direct network access to. 
Step 1, use `ssh` to create a nice tunnel (to the arbitrary local port 11122):

{% codeblock lang:console %}
$ ssh -L 11122:host.of.database.com:3306 user@domain.com
{% endcodeblock %}

I needed to tweak the importer tool that ships with Jekyll to support using a host and port:

{% codeblock lang:ruby %}
def self.process(dbname, user, pass, host = '127.0.0.1', port = 11122)
    db = Sequel.mysql(dbname, :user => user, :password => pass, :host => host, :port=> port)
{% endcodeblock %}

There was a whole lot of hideous perl going on to slap around my posts once they were imported since the post bodies were in a strange combination of raw HTML, textile, and other legacy markup fragments. Things seem fairly solid at this point. 

### Optimizing CSS

I'm using some CSS magic from the inspirational [OOCSS project](http://oocss.org/), and that style leaves you with lots of individual files. My [Rakefile](http://github.com/jbarratt/serialized.net/blob/master/Rakefile) is mostly snaked from people like [avdgaag](http://github.com/avdgaag/arjanvandergaag.nl/blob/master/Rakefile), but I added in a useful CSS optimization section.

{% codeblock lang:ruby %}
file "style/merged.css" => ["style/syntax.css", "style/template.css", "style/libraries.css", "style/grids.css", "style/content.css", "style/mod.css"] do |t|
    sh "cat #{t.prerequisites.join(' ')} > #{t.name}.devel"
    sh "java -jar ~/.java/yuicompressor-2.4.2.jar --type css -o style/merged.css #{t.name}.devel"
end
{% endcodeblock %}

I've had to elaborate files by name so they end up in the correct order (one of the least fun things about CSS, aside from 'everything else', is that order matters). So you do have to update the list by hand when adding files, but most of the time I'm sure you'll tend to tweak them instead. I'm using Yahoo's [YUI Compressor](http://developer.yahoo.com/yui/compressor/) which is nice, since if my Javascript gets more complex I can use it for that as well.

For now it shrinks the payload from 14k to 8k, not worth doing super backflips over -- the majority of the gain is in the simple concatenation, turning 6+ HTTP GET's into a single one.
