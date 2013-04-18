<!--
.. title: Managing volatile files with puppet
.. date: 2009/04/15 13:37
.. slug: managing-volatile-files-with-puppet
.. tags:
.. link:
.. description:
-->

I'm managing [Linux HA](http://linux-ha.org) (heartbeat2) from [Puppet](http://reductivelabs.com) and I had a problem.
There is a file called `cib.xml` used by heartbeat which I needed to manage. For a variety of boring reasons, when you make changes to this file, you must have a number in it which is the highest the
app has ever seen.

To make things easy, I use the current timestamp for this, as I've never seen that number go backwards.

Ok, not the normal kind of thing you do with Puppet, but it can be done. We just need to know what time it is in the template.

Thankfully Puppet lets us define custom facts, so here we go...
in the module's plugins/facter directory, I created `epoch_time.rb`.

``` ruby
    Facter.add("epoch_time") do
            setcode do
                    Time.now.to_i
            end
    end
```

Then I could use that in `templates/heartbeat/cib.xml`:

``` xml
 <cib admin_epoch="<%= epoch_time %>">
```

Well, that works fine, except for one little issue.

When puppet manages a file it does this:
1. Renders out the templates and takes an md5sum of that
1. Sends that to the client, which checks it's own md5sum
1. If the sums are different, the client overwrites the file with the old one
1. The client then updates anything 'subscribed' to that file (for example, restarting a service.)

So since puppet runs about every 30 minutes, that's not good. I don't want to be reloading the CIB database every 30 minutes. That's bad.

This is what we get:

```
    debug: File[/etc/ha.d/ha.cf]/checksum: Initializing checksum hash
    debug: File[/etc/ha.d/ha.cf]: Creating checksum {md5}18530322762561ce59f1d414340b4c43
    debug: File[/etc/ha.d/cib.xml]/checksum: Initializing checksum hash
    debug: File[/etc/ha.d/cib.xml]: Creating checksum {md5}a02f0ca8a3cce64d7913faa3268e530b
    debug: File[/etc/ha.d/cib.xml]/content: Executing 'diff /etc/ha.d/cib.xml /tmp/puppet-diffing20090415-3486-ska653-0'
    1c1
    < <cib admin_epoch="1239318580">
    ---
    >  <cib admin_epoch="1239815009">
    debug: File[/etc/ha.d/cib.xml]: Changing content
    debug: File[/etc/ha.d/cib.xml]: 1 change(s)
    </cib>
```


So here was my solution, and as inelegant as it is, it pretty much works.

1. Manage a file called 'cib.xml-puppet' instead
1. In this file, set admin_epoch="0"
1. When THAT file changes, do a chained action which sets the epoch time correctly, and writes out the actual cib.xml file
1. Run the command to reload the CIB database in that and only that case.

So the puppet code to make this happen:
```
        exec { "add-epoch-cib-xml":
                command => "sed 's/admin_epoch=\"0\"/admin_epoch=\"${epoch_time}\"/' /etc/ha.d/cib.xml-puppet > /etc/ha.d/cib.xml && cibadmin -R -x /etc/ha.d/cib.xml",
                path => ["/bin", "/usr/sbin/"],
                subscribe => File["/etc/ha.d/cib.xml-puppet"],
                refreshonly => true,
        }
        file { "/etc/ha.d/cib.xml-puppet" :
                type => 'file',
                ensure => 'present',
                content => template("ha_nfsroot/heartbeat/cib.xml");
        }
```

So I still get to use my very first custom fact (it gets interpolated into the 'sed' command) but I also don't run that terrifying update every time.

If any puppetmasters or Linux HA gurus want to tell me exactly how I'm doing it wrong I would love to hear that. This certianly doesn't feel "elegant."
However, since it feels "functional", functionality trumps elegance for today.
