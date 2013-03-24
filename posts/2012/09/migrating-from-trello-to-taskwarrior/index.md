<!--
.. title: Migrating from Trello to Taskwarrior
.. date: 2012/09/04 21:47
.. slug: index
.. tags:
.. link:
.. description:
-->


I'm a big fan of [Trello](http://trello.com) and still regularly use it. It's a
fantastic tool, especially when working with teams.
However, on the personal side, I've long used (and largely been happy with) the [GTD](http://en.wikipedia.org/wiki/Getting_Things_Done) methodology. I was experimenting with Trello to do a more [Personal Kanban](http://www.personalkanban.com/pk/personal-kanban-101/) style and it wasn't working for me. I kept finding myself not using the tool to guide my day to day work, but rather relying on my fallible head, which means the return of being stressed about things I should and shouldn't be doing.

There were a few issues which made me reach for a larger change than just
incremental improvement. Trello was missing things I'd come to enjoy from [Omnifocus](http://www.omnigroup.com/products/omnifocus/) like recurring tasks, hiding things that weren't yet ready to be acted on, review cycles, etc -- which help cut down on the noise and help you focus and relax. My next step would probably have been multiple boards to represent the different elevation levels, but that felt like it would be clunky to use. Also, even with the many and wonderful keyboard shortcuts, I found myself going to the mouse way more often than I wanted.

I do like parts of both PK and GTD, and think the sweet spot is probably [somewhere in between](http://www.personalkanban.com/pk/applications/gtd-kanban-similarities-differences-synergies-between-the-two/).

I was just going to switch back to Omnifocus, but these days I'm spending most
of my time in the a full screened terminal ([vim](http://vim.org), [tmux](http://tmux.sourceforge.net), [irssi](http://irssi.org)+[bitlbee](http://www.bitlbee.org/main.php/news.r.html), [gcalcli](https://github.com/insanum/gcalcli), and so on) and ran across [Taskwarrior](http://taskwarrior.org/projects/show/taskwarrior). I liked the premise and, after poking at the docs a bit and doing the [excellent tutorial](http://taskwarrior.org/projects/taskwarrior/wiki/Tutorial), figured it was worth a shot. (Especially since I could probably get closer to a hybrid PK/GTD system via the rich abilities to extend it.)

There wasn't a direct translation layer between Trello's information model and
Taskwarrior's, and because Trello allows you to make your own conventions, I
don't think there'd be a good way to do a generic "port". So, I [whipped up a script](https://github.com/jbarratt/trello_to_task) that did a "good enough" job doing the export.

### Running it

#### Safety first 

You might want to open up `~/.taskrc` and  set
`data.location=/some/temp/place` so you can test importing without messing with
any of your real tasks.

#### Let's do this

Huge props to Trello for making the data available and easy to get at. Just open
the board, click the board name in the top left, select 'Share, Print and
Export', and select 'Export JSON'. Once you've saved the json file,

```
$ git clone https://github.com/jbarratt/trello_to_task.git && cd trello_to_task
$ ./trello_to_task.py my_board.json taskwarrior_format.json
$ task import taskwarrior_format.json
```

### Customization help

If you're trying to do this conversion, there's a good chance the assumptions I made won't be the same as you'd like to make.
Depending on how you were using Trello, what each of the columns represented,
what comments and checklists were used for, etc you might want to make some
different choices. Here's what I ended up with:

* The date on everything is set to the current date. I didn't care about when in
  the past I'd created something.
* Everything comes in with `project:home`
* All comments are converted to annotations
* Column names are converted to tags (So card in a column named 'Someday Maybe' becomes tagged 'somedaymaybe')
* Anything that was in a column named 'Done' is ignored
* If a card had a checklist on it
    * The name of the card is mashed up (strip spaces and lowercase it)
    * That makes a new project under home (So 'Buy Car' => `home.buycar`)
    * All the checklist items become tasks in that project, as does the
      (originally named) main task itself
    * The main task depends on all the checklist items

Hopefully if any of these assumptions don't work for you (and you're trying to
do this conversion) the code will be straightforward enough to modify.
