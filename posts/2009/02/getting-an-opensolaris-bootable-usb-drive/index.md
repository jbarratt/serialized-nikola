<!--
.. title: Getting an OpenSolaris bootable USB drive
.. date: 2009/02/24 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

This was not a straightforward process.

What I would have loved would be a 'dd'able image. That way, from a linux server I could (as far as I know) write the image out and be done.

In any case, this was not to be.
First problem, I needed a Solaris system to create the USB image from.
For this I figured I could use Virtualbox, which I upgraded before starting.

I'm not sure if I needed to upgrade 2008.05 to 2008.11, but I figured I'd do it while I was at it. I found good instructions on the [OpenSolaris site](http://www.opensolaris.org/os/project/indiana/resources/relnotes/200805/image-update/): Basically,

``` console
$ BUILD=`uname -v | sed -e "s/snv_//" -e "s/[a-z]//"`
$ pfexec pkg refresh
$ pfexec pkg install entire@0.5.11-0.${BUILD}
$ pfexec pkg install SUNWipkg@0.5.11-0.${BUILD}
$ pfexec pkg install SUNWinstall-libs 
$ pfexec pkg image-update
```

This took a LONG TIME in VirtualBox (running on a pretty new MacBook Pro even) and my whole machine wasn't all that usable during the process, but hey.

Then I rebooted into the new OS (and it looks shiny!) which this time detected the windows-formatted partition on my USB disk, a convenient improvement.

I then shortcutted one of the steps in this [article about building distros on USB sticks](http://blogs.sun.com/clayb/entry/creating_opensolaris_usb_sticks_is) by downloading a canned image from [genunix.org](http://genunix.org): Specifically [http://www.genunix.org/distributions/indiana/osol-0811.usb](http://www.genunix.org/distributions/indiana/osol-0811.usb)

I unmounted the USB device, and then installed the new-ish Sun "dist build" tools:

    `pkg install SUNWdistro-const`

And then ran the newly-installed 'usbcopy' tool:

    `/usr/bin/usbcopy osol-0811.usb`

And, about 20 minutes later, it was done!

I have now tested it by booting from it on an eeePC 1000HA and it worked great. I've ripped the image in linux with dd, and we'll be testing it to see if it's portable that way. (Surely would be a lot less work than _my_ way.)
