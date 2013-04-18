<!--
.. title: vim and CVS todo lists
.. date: 2005/04/28 13:37
.. slug: vim-and-cvs-todo-lists
.. tags:
.. link:
.. description:
-->

We keep our todo lists in CVS -- it's not as classy as using a web app, I guess, but it is nice to be able to edit what turns out to be a fairly rich space using the wonderfully powerful text-flingy-ness of vim.

The thing is, I used to always launch my todo list from a terminal, then keep that terminal around so I could commit and update. I suddenly realized that a simple :map would make things a lot easier -- since when I launch vim, it keeps the same working directory that it starts with.

So sticking this in my `.vimrc`:

``` vim
map <F8> :!cvs commit -m ""<CR><CR>
```


means by hitting F8 (arbitrary choice) I can commit the current document. Nice. If it gets to it I could add in the other features, like update, but for now I digs it.
