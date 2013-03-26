<!--
.. title: Adding iSCSI exports to OpenSolaris for remote Time Machine
.. date: 2010/03/15 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

There are 3 ways to Time Machine over the network (that I know of)
<ol>
<li>Use a Time Capsule</li>
<li>Run Snow Leopard Server, which allows you to set remote drives as Time Machine volumes</li>
<li>Mount the iSCSI share via an "initiator", and use it like it was a normal hard drive.</li>
</ol>

I'm not sure I'd want to use the iSCSI option with a laptop, so I use a hybrid of the second and third options.

I'm running Snow Leopard Server on a Mac Mini with limited disk space. I've got a large server running OpenSolaris about which I [blogged previously.](/2009/02/the-littlest-thumper-opensolaris-nas-on-an-msi-wind-pc/)

Here are the brief steps you need to take to get it working.

On the Snow Leopard Server, install the [ISCSI initiator from GlobalSan.](http://www.studionetworksolutions.com/products/product_detail.php?t=more&pi=11)

On your OpenSolaris server, make sure you've installed the support packages needed.
``` console
# pkg install SUNWiscsi SUNWiscsitgt
```

Now, from one of your available disk pools, create the virtual hard drives for your servers to mount, (making sure you make them about 1.5x larger than the disks you're trying to back up, so you can get historical information from them.

``` console
# zfs create -o shareiscsi=on -s -V 160GB mypool/laptop_tm
# zfs create -o shareiscsi=on -s -V 140GB mypool/server_tm
```

To find out what the "target ID's" are, run this:
``` console
# iscsitadm list target
```
shows the target names to paste into the initiator.

You can follow the instruction at this [blog on sun.com](http://blogs.sun.com/constantin/entry/zfs_and_mac_os_x) which has screenshots of the rest of the process.

At this point the drives are just like regular disks, from the perspective of your Mac (desktop or server) -- and can be formatted and used for Time Machine. Very convenient and the data that you're backing up will be in the safe, safe hands of ZFS in the event of a disk failure.
