<!--
.. title: Xnest remote KDE desktop
.. date: 2005/02/28 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

New trick for today -- sometimes I need to remotely modify KDE desktops, and messing around with CLI config files only goes so far. If I SSH into the system, then

/usr/X11R6/bin/Xnest :1 & export DISPLAY=`hostname`:1 ; startkde

then I get a desktop.

This begs a feature -- ssh macros. Openssh already has escape characters. If, in a config file, we could define strings that got dumped to the command line based on a sequence of characters (say, above, ~Mxnest) that'd make the sysadmin's lot a much happier one. (Alternative is running everything from one host with ssh just reaching out and executing remote commands, or having the same .bashrc on every machine.) I don't see people out there talking about it, though it's a feature in some of the GUI ssh tools.
