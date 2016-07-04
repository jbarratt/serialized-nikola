<!-- 
.. title: TaskPaper + Vim + Dropbox + Editorial = GTD & Checklist Perfection
.. slug: taskpaper-+-vim-+-dropbox-+-editorial-checklist-perfection
.. date: 2016-07-04 07:07:55 UTC
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

I have tried worryingly many methods for tracking my personal and professional projects, some of which I have written about here before. I finally boiled down what I wanted to:

1. _The ability to edit things with Vim._ I feel so much more productive when writing in Vim, and even more productive when reorganizing things in Vim, that using another tool always felt frustrating.
2. _The ability to capture while mobile._ While I can use Vim on iOS, it's not the same. I wanted to the ability to add new things to my todo list, mark things off, review my projects while in a meeting, and so on.

I've finally found something that works for me, and works well.

* [Editorial](http://omz-software.com/editorial/): a fantastic, programmable with python, iOS text editor
* The [TaskPaper](http://omz-software.com/editorial/docs/ios/editorial_writing_todo_lists.html) text file format, supported excellently by both Editorial and Vim
* [Vim](http://www.vim.org/), my favorite editor when I have a full keyboard, with a [TaskPaper](https://github.com/davidoc/taskpaper.vim) plugin installed
* And finally, [Dropbox](http://dropbox.com) to keep the files in sync.

### Taskpaper

If you've never used Taskpaper, it's wonderfully simple. You can create projects, tasks, subtasks, and general tags with very little syntax.

    Blog About TaskPaper:
    - Gather links to the relevant projects @home
    - Get blog software working again after a blogging hiatus
        - Upgrade to the python3 version @done(2016-07-03)
        - Check for broken configuration @today

And that's about it. You can use the tags to filter your views of things or, in editorial, show things as checked/completed, or color coded.

It's just enough capability for Todo/GTD type work. I find when my `todo.taskpaper` file becomes unwieldy, it's a good sign that I'm tracking too many things that will never get done anyway, and it's time to archive or delete projects.

### Vim

Two small changes made Vim work great in this setup. First, with `taskpaper.vim` installed, you get a lot of nice hotkeys for things like:

* focusing on a single project
* marking tasks done
* archiving all completed tasks
* marking tasks as due today, and focusing only on today's tasks

I generally have a vim running with my `todo.taskpaper` file open at all times.
However, that's not ideal for the 'ubiquitous capture.' If I have the file open, and I haven't saved all my edits, I may clobber them if editing on mobile. Similarly, if I make a mobile edit, and don't reopen the file in vim, I'll lose those changes.

Some small settings in `.vimrc` make this a non-issue. (Using `Vundle` syntax here to show the plugins needed.)

    " Autosave taskpaper files                    
    Plugin 'vim-scripts/vim-auto-save' 
    Plugin 'djoshea/vim-autoread'      
    autocmd filetype taskpaper let g:auto_save = 1
    autocmd filetype taskpaper :WatchForChanges!  

Translating to English -- if the filetype is one that's used by the taskpaper extension, then auto-save the files on edit, and do a force-reload if file changes are detected on the filesystem. Because I'm the only one actually editing this file, the risk of a race condition here is nearly nil.

### Editorial

I can't say enough about the Editorial app. It's incredibly useful to be able to simply extend it with Python, when needed, and even without that capability it's wonderful out of the box. If you work in Markdown at all, give it a look.

Because it supports Dropbox, the synchronization is easy. As long as I'm online, it's got the latest versions of all my files. The UI for working with taskpaper files is great, very easy to drag things around to reorganize them, fold projects to focus on specific ones, and most importantly, check things off as they're completed.

### Bonus Use Case: Checklists!

These tools together have provided me pretty much everything I need for day to day GTD/To Do. But I discovered another use case that's very handy: frequently used checklists!

For example, I have a `car_camping.taskpaper` file for camping trips, which looks like so:

    Pantry:
    - Pancake Mix
    - Olive Oil
    - Salt & Pepper
    ...
    Equipment:
    - 6 person tent
    - Sun shade
    - Head Lamp

When I'm ready to actually go camping, I can make a new copy of the basic taskpaper config:

    $ cp car_camping.taskpaper 2016_06_beverly_beach_camping.taskpaper

Then I can add extra planning sections for this particular trip, like removing equipment that's only needed in colder weather, or planning meals and shopping trips:

    Meals:
    - Monday
        - Breakfast: Pancakes, Eggs, Fruit
    ...
    Shopping:
    - Propane Bottles
    - Bubble Solution

Then, as I confirm that I have indeed purchased or packed any item, I can check it off.
I do all the planning with a nice keyboard, and access to vim, and check things off on my phone as I go. The best of both worlds!

And finally, it's nice to have the completed checklists as records of the past. ("What did we eat last trip? The kids seemed to do really well with that.")

### Plain Text Saves The Day

It's fairly surprising, with how duct-taped this solution is together, how happy I've been with it, and how it handles two somewhat different use cases (daily project management, and periodic checklist execution) with basically the same workflow.

It's a real testament to the power of simple, plain text formats and what we can do when there's consensus around them.
