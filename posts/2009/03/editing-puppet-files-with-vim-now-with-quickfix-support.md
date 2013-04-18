<!--
.. title: Editing puppet files with vim: now with 'quickfix' support.
.. date: 2009/03/31 13:37
.. slug: editing-puppet-files-with-vim-now-with-quickfix-support
.. tags:
.. link:
.. description:
-->

So the puppet guys provide some notes and files on running puppet with vim.
One thing I didn't see anything that provided a 'compiler', so I could edit a '.pp' file, then do :make to check for errors. (Check out <code>:help make</code> in your vim for more information about the quickfix tool.)

This little tar contains all the files you need to make this work. Careful with it, as I have provided a minimalist .vimrc so don't unpack this in your home directory.

 [puppet_vim.tar.gz](/images/puppet-vimtar.gz)
