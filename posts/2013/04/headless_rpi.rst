.. link: 
.. description: 
.. tags: 
.. date: 2013/04/18 23:49:50
.. title: Instantly finding a headless Raspberry Pi
.. slug: headless_rpi

My brother got me a Raspberry Pi for my birthday (thanks!) -- a device I'd
wanted to get for some time, but hadn't quite yet been able to justify. I think those sorts of things make the best gifts.  

You need just a few things to get a Pi up and running, but 2 things on the list (an HDMI-speaking display and an Ethernet port) don't appear in the same room in my house. Thankfully, the latest releases of Raspbian (the rPi Debian
Distribution) come with DHCP and ``ssh`` pre-configured, so if you plug the pi into a network, you'll be able to connect to it.

At first, I was doing an ``nmap`` scan for ``-p 22 --open``, but that's not
actually that quick. I was able to speed it up by tweaking some options::

    $ nmap -T5 -n -p 22 --open --min-parallelism 200 192.168.1.0/24

* ``-T5``: 'Insane' timing profile, very agressive scan rate and low delays.
* ``-n``: Turn off reverse DNS lookup
* ``-p22 --open``: Only look at port ``22``, and find open ones
* ``--min-paralellism 200``: Scan in large (almost subnet-sized) chunks

And it works; you get::

    Nmap done: 256 IP addresses (3 hosts up) scanned in 1.32 seconds

But there's an even quicker way, that's also more precise. After running that 1.32 second scan, I still have to decide which of the port-22-open devices is the pi. It turns out the `Raspberry Pi Foundation <http://hwaddress.com/mac/B827EB-000000.html>`_ actually has a range of MAC addresses all to themselves! And ``arp -a`` runs almost instantly, and dumps the device's local arp table::  

    $ arp -a
    ...
    ? (192.168.1.155) at b8:27:eb:5:63:2c on en0 ifscope [ethernet]

This means we can do::

    $ arp -a | grep b8:27:eb | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    192.168.1.155

which can also be made into a nice ``.bashrc``/``.zshrc`` alias::

    alias rpi_ip = "arp -a | grep b8:27:eb | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'"

To make it even easier, why not skip one more step::

    alias key_rpi="ssh-copy-id pi@`rpi_ip`"

So now when I put a new SD card into my pi, boot it up, all I have to do is::

    $ key_rpi
    pi@192.168.1.155's password:

and it works. I'm keyed, and can ssh in now as easily as ``ssh pi@`rpi_ip```.
(Until I use Ansible to set up ``mDNS`` seconds later, which is probably good to
leave for another post.)

.. warning:: 

    This will need modifications if you're going to have more than 1 pi on the
    same network. ``rpi_ip`` will still run, but it'll output multiple lines.
