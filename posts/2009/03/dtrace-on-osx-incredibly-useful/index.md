<!--
.. title: DTrace on OSX: incredibly useful.
.. date: 2009/03/21 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

So because I am insane and completely unable to master one thing before becoming fascinated with something new, I'm learning Haskell. By "learning" I mean "will be able to do simple apps and have a good sense for what it's good for."

In any case, it's easy to install on a Mac if you've got MacPorts set up:
<code>sudo port install ghc</code>

However, the install takes a LOOOONG time. So long, I was wondering if something had gotten hung. I could see (and hear from the fans doing their best) that the CPU was busy. Running top just showed that a process named ghc (the Haskell compiler itself) was working in some way. But DTrace shows exactly what's going on.

This trivial example (from Brendan Gregg's [DTrace Oneliners](http://www.brendangregg.com/DTrace/dtrace_oneliners.txt)) shows the files getting opened by matching the 'open' system call, when it's entered, and printing out the name of the app that called it (execname) and the first argument to that function -- in other words, the file.

{% codeblock lang:console %}
  $ sudo dtrace -n 'syscall::open*:entry { printf("%s %s",execname,copyinstr(arg0)); }'

  1  17657                       open:entry tclsh8.4 /opt/local/var/macports/software/ghc/6.10.1_9+darwin_9_i386/opt/local/share/ghc-6.10.1/doc/ghc/libraries/directory/LICENSE
  1  17657                       open:entry mdworker /opt/local/var/macports/software/ghc/6.10.1_9+darwin_9_i386/opt/local/share/ghc-6.10.1/doc/ghc/libraries/containers/minus.gif
  1  17657                       open:entry mdworker /opt/local/var/macports/software/ghc/6.10.1_9+darwin_9_i386/opt/local/share/ghc-6.10.1/doc/ghc/libraries/containers/minus.gif

{% endcodeblock %}

And there we go. You can see the installer monkeying around in the documentation directories. 

This technique works for pretty much any installer/process you might be curious about. In the Bad Old Days, I've been able to get this kind of insight from things like strace -- watching as it runs a given process. To me, one of the most beautiful things about the DTrace model is that it doesn't matter if (as happened in this case) there are a lot of processes getting run -- you can still find exactly what you need without stressing with PID's. Strace works on a process, DTrace works on the system.

If you're on a Mac, open up a terminal and have some fun with the one-liners I linked to. You'll be amazed by what your computer's doing when you're not looking.
