<!--
.. title: Migrating live filesystems to LVM
.. date: 2006/04/04 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

These days, we build all of our new (linux) hosts with LVM. This is great since it allows us to quickly bring in new storage in a given file system, be it local or network attached. It also allows a nice graceful way to 'hop' a given volume from one storage device to another -- you simply add the new device, then use 'pvmove' to move the blocks (while the file system is 'live') from one device to the other, then you remove the old device, and you're done. All with nary a blip as far as the noble users of the system are concerned.

The tricky thing is when you need to do the same thing -- and the host you're working on is a regular old block device formatted with ext3. What to do? It's important not to have downtime. This is a big filesystem with lots and lots of data, and even more nastily, lots and lots of hard links. It takes something like rsync 3 hours just to start up, let alone start copying data.

The trick came as a flash of insight to one of my esteemed colleagues. Linux has a wonderful software raid facility. In mirror ('raid 1') mode, it synchronizes 2 block devices. It doesn't care what filesystem (if any) they are running. It doesn't care if they're real devices or other 'synthetic' block devices like LVM. And when they're in sync, you have 2 block devices that are both identical and 'normal'. If you reboot and mount either of the members of the raid, they have full, 'normal' filesystems on them.

So the technique becomes so simple it's almost self-evident.

0. BACKUP BACKUP BACKUP
1. Create your new (LVM'd, if that's what you wanted) storage
2. Create, with `mdadm`, a raid 1 where the primary disk is your existing filesystem.
3. Remount your mount point using your new md device
4. Watch `/proc/mdstat` as your drives magically synchronize, staying accessible and live all the while.
5. Unmount the `/dev/md*` device, remount your shiny new filesystem, and go away, happy as a clam.

It really illustrates the power of abstracted block devices. We went to a talk given by an engineer from Google who was talking about the future of commodity storage at Google -- they're looking at building clustered storage which, at the back end, consists of block devices bolted together with [ddraid](http://sourceware.org/cluster/ddraid/) and some similar but seemingly yet unpublished tools. It's a cool time to be getting to play with computers for a living.
