<!--
.. title: Local Python CI with Watchdog and Nose
.. date: 2012/09/13 12:53
.. slug: index
.. tags:
.. link:
.. description:
-->


At work we're working on a new project made up of a number of python packages, but they're all (for convenience) in the same repo.

```
repo/
    package1/
    package2/
    package3/
```

These are a group of modules and services which can be consumed by each other, and we're rapidly adding functionality across all of them. (Putting meat on the [walking skeleton](http://alistair.cockburn.us/Walking+skeleton).)

This means that it can be easy for a change in one module to introduce a regression in another, so it's nice to get immediate feedback if that happens. (This can be especially insidious around merges; the merge didn't have any conflicts, but somehow functionality is now broken.)

After being bitten by 2 such 'merge side effect' issues in 1 day, I had to think that there was some way to test automatically. And there are a lot of tools out there which help with this problem, but none which worked well with my use case of having these multiple project and wanting to trigger tests across all when one changed.

I also wanted to be more liberal in the kinds of files which would kick off the tests -- for example, a `development.ini` from a [pyramid](http://www.pylonsproject.org/) app, or things happening to the directories (including a file getting deleted.)

I found this article about [continuous integration in python using watchdog](http://ginstrom.com/scribbles/2012/05/10/continuous-integration-in-python-using-watchdog/) and it was very close to what I needed.

This multi-package use case turned out to be a little weird. After playing with a few alternatives, I discovered what I generally wanted was 

* If I altered a file in package `X`, then test `X` first, as it's most likely to be the thing I just broke. If it passes, proceed to test the rest of the packages.
* If any test fails, stop processing, and display the output of just the `nosetests` run that failed. Otherwise output only that the tests ran and passed.

I made a few tweaks to support the algorithm I needed, and then hit a wall: running the tests was generating more events as it updated coverage files.  Because I was trapping directory modifications too, it was impossible to tell which was which.

So, when each test run finishes, I force-drain the event queue, assuming all events generated while the tests ran were unwanted side effects.

``` python
queue = self.observer.event_queue
try:
    """ dirty hack to drain any events that this test generated """
    while 1:
        queue.get_nowait()
        queue.task_done()
except Queue.Empty:
    """ this is ok, it's what we expect """
    pass
```

Also, I know this script is rooted in `utilities`, relative to the rest of the packages, so it uses that to figure out where to go looking for package directories.

``` python
self.basedir = os.path.abspath(__file__ + '/../..')
```

One thing that's still weird with this script: if you're using `vim` or another editor which makes temp files, it'll still recognize that as a change. I didn't notice this until some co-workers started using it, because I have vim configured with

```
set nobackup
set noswapfile
```

The full script is available [as a gist](https://gist.github.com/3717117).
