<!--
.. title: Debugging Python Tests
.. date: 2012/08/29 14:58
.. slug: index
.. tags:
.. link:
.. description:
-->


One of my favorite things about testing is that you build these little
environments that exercise your code in certain scenarios. When you mix in a
debugger, boom, you've got a REPL that comes pre-primed to help you investigate a part of your code.

If 

* you're using `nose` (and I haven't found a reason not to be) 
* your test is failing

you can just run

```
$ nosetests --pdb
```

or

```
$ nosetests --pdb-failures
```

and that gets you a debugger right aimed at your failing tests. (Not sure why
you sometimes need one vs the other.)

If your test isn't failing, or you want to trap things higher up the stack than what actually ends up making the test fail, you can also do it manually.
Just run python with `-m pdb` to run the debugger, and set the breakpoint:

```
$ python -m pdb `which nosetests`
(Pdb) b mymodule/tests.py:33
  Breakpoint 1 at ...mymodule/tests.py:33
(Pdb) c
```

The `which` is needed because when you run `python -m pdb` it expects a full
path to the script to run.

Using the python debugger is pretty simple:

* `?`: get some nice help. `? <command>` shows help for specific command
* `bt`: show a backtrace. Useful for `nosetests --pdb` to find out where the
  heck you are in the code
* `l`: List the code "near" us, with an indicator for where we currently are
* `pp`: Pretty Print a variable. `pp self.__dict__` is useful to introspect the current object.
* `s`: step to the next line of code
* `r`: continue running until the current function returns
* `up`: don't change the execution of the code, but go 'up' a level of the stack
* `c`: continue running the code

... and more things you can find with `?`. These are my gotos.

Especially when you're doing TDD style development (write the test so it fails, write the code until it stops failing) I've found it to be very efficient to write the code you **think** will do the trick, then just `nosetests --pdb` with an interactive environment to explore just why you were wrong.
