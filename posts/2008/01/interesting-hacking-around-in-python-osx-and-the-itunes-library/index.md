<!--
.. title: Interesting hacking around in python, OSX, and the iTunes Library
.. date: 2008/01/01 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

While working on a project for a friend, Amber accidentally deleted a playlist of music. "Uh oh", she said, "it looks like you can't undo that!". A bit of googling showed that to be the case.

Thankfully, though it's a bit out of date, we've been good(ish) about keeping backups. I thought "I bet I can get the playlist info out of the iTunes library file in the backup!" Sure enough, I mounted the drive, took a look, and there the data was. It wasn't that useful though.


{% codeblock lang:xml %}
 <key>Name</key><string>The Special Playlist</string>
                        <key>Playlist ID</key><integer>14915</integer>
                        <key>Playlist Persistent ID</key><string>F668E7C09FF9F9AC</string>
                        <key>All Items</key><true/>
                        <key>Playlist Items</key>
                        <array>
                                <dict>
                                        <key>Track ID</key><integer>3533</integer>
                                </dict>
                                <dict>
                                        <key>Track ID</key><integer>3532</integer>
                                </dict>
                                <dict>
                                        <key>Track ID</key><integer>3527</integer>
                                </dict>

{% endcodeblock %}

So normally I break out the perl here, and it looked like there was some CPAN modules to get it done, but the iTunes XML parser library looks like it wasn't packaged right and I couldn't install it via CPAN, blah blah blah. I've been trying to break out the python more often, so searched for 'python itunes xml library parse' and found this gem from 2005:

[Airport Express Hates Me](http://bob.pythonmac.org/archives/2005/07/18/airport-express-hates-me/)

In which the author uses a neat trick (the Python/Objective C bindings) to parse the iTunes library. After a bit of a bumpy start, I ended up with the following code:


{% codeblock lang:python %}
    #!/usr/bin/python
    from Foundation import *
    dbFile = "itunes_from_backup.xml"
    db = NSDictionary.dictionaryWithContentsOfFile_(dbFile)
    printtrack = {}

    for playlist in db[u'Playlists'].itervalues():
            if playlist[u'Name'] == u"The Special Playlist":
                    for track in playlist[u'Playlist Items'].itervalues():
                            printtrack[track[u'Track ID']] = 1
                    
    for track in db[u'Tracks'].itervalues():
            try:
                    if printtrack[track[u'Track ID']]:
                            print "%s: %s, %s" % (track[u'Artist'], track[u'Album'], track[u'Name'])
            except:
                    pass

{% endcodeblock %}


<p>Which yeilds a nice list like:
Andrew Bird: Armchair Apocrypha, Scythian Empires
Andrew Bird: Armchair Apocrypha, Self-Torture
Andrew Bird: Armchair Apocrypha, Simple X
Andrew Bird: Armchair Apocrypha, Spare-Ohs
Andrew Bird: Armchair Apocrypha, The Supine
Andrew Bird: Armchair Apocrypha, Yawny at the Apocalypse
Arcade Fire: Funeral, Crown Of Love
Arcade Fire: Funeral, Haiti
Arcade Fire: Funeral, In The Backseat
Arcade Fire: Funeral, Neighborhood 1 - Tunnels
Arcade Fire: Funeral, Neighborhood 2 - Laika</p>



I <em>think</em> there is a way to look up track information from track ID's directly, but I couldn't suss it, hence the double loop with the dictionary for bookkeeping. (Yes, my python looks very perlish, I'm sure.) In any case, the Python Objective C bindings look pretty cool and I plan to explore those further.
