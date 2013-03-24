<!--
.. title: Testing Perl code that runs commands
.. date: 2010/09/22 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->


At the September [Los Angeles Perl Mongers](http://losangeles.pm.org/) meetup, [Tommy Stanton](http://tommystanton.com/) presented on an in-progress bit of code he's working on, `App::Git::HomeSync`. ([Presentation](http://tommystanton.com/presentations/20100908-Tommy_Stanton-App-Git-HomeSync/))

As you'd hope and expect from something headed CPAN-ward, he's got lots of tests. As you might have guessed from the name, this module needs to run `git` quite a bit, with different command line arguments. Tommy's approach to testing this is good -- ship the module with some "fixtures" (a directory in a known state which gets unpacked into a temp directory) and then run the command line app in that directory.

There is another way to approach this, and I realized I didn't have any "open sourceable" code which demonstrates this technique.
I got a lot of the way through writing this before realizing I have [blogged a more basic version of this idea before](/2009/10/testing-perl-system-interactions/), but this is a new-and-improved take on things, with much deeper examples.

## `tl;dr`

* Use [IPC::Run](http://search.cpan.org/perldoc/IPC::Run) to run your command line apps
* In your test code, intercept the calls to `IPC::Run::run` and return your own data, based on the command line used
* Store sample command line output inside the test file using [Data::Section](http://search.cpan.org/perldoc/Data::Section)

I've stashed a full, functional example of this idea in my [Acme::System repository on GitHub](http://github.com/jbarratt/Acme-System).

## Code Walkthrough

### Using IPC::Run in your code

First, there's the module code itself. This module does 2 very stupid things.

* It returns the sum of all the PID's (Process ID's) on the system, and it calls `ps` to get this information.
* It returns the value of one of the columns from the `vmstat` tool.

The important thing is to use `IPC::Run::run` to actually run the code, instead of a blind `system()` call. Because it's a module call, and has a very simple interface, it's much easier to mock it ("override the functionality with 'fake' functionality) for testing.

This is in [lib/Acme/System.pm](http://github.com/jbarratt/Acme-System/blob/master/lib/Acme/System.pm). Here's the pidsum method (the `vmstat_col` method is basically the same, check out the full code if you're curious):

{% codeblock lang:perl %}
    =method pidsum
        Return the sum of all the PID's on a system
    =cut

    sub pidsum {
        my @ps_cmd = ("ps", "-Ao", "pid,cmd");
        my ($stdin, $stderr) = (undef, undef);
        my $ps_output;
        IPC::Run::run(\@ps_cmd, \$stdin, \$ps_output, \$stderr);
        return sum(
            map { /^\s*(\d+)/ ? $1 : 0 }
            split(/\n/, $ps_output)
        );
    };
{% endcodeblock %}

So, as I said, stupid code. I only care about getting the output, so I pass in undef for the other values -- `IPC::Run::run` wants you to supply them anyway.

However, that little `sum`/`map`/`split` thing sure looks fancy. How much would be willing to wager that it's bug-free? Probably not much. How would you even test code like that?

So, let's cheat -- run `ps` just the once, stash the results, and use those for testing from there on out.

### Storing the command line output results

Check out the the [whole test file](http://github.com/jbarratt/Acme-System/blob/master/t/00-fakerun.t) to see what's going on overall.

There's a few bits of weirdness, for sure. Down the end you'll see:

{% codeblock lang:text %}
    __DATA__
    __[ ps -Ao pid,cmd ]__
    PID CMD
        1 init [2]
        7 [khelper]
    ....
    1887 /usr/sbin/acpid
    __[ vmstat -n 1 1 ]__
    procs -----------memory---------- ---swap-- -----io---- -system-- ----cpu----
    r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa
    0  0    648  85932 194240 119124    0    0     0     5    2   51  0  0 100  0
    __END__
{% endcodeblock %}

This is the format that `Data::Section` wants. You just need to stash each command you run between the underscored square brackets, and follow it with some sample command line data.

The tricky thing is this -- `Data::Section` was built to be used with Modules, not "plain jane `.t` files."
So to make that work, you need to:

* Give your test a package name. I chose to just stick a `Test::` in front of the module name.
* Give `Data::Section` an instance of that object to stick it's methods into.

{% codeblock lang:perl %}
    # magic; Data::Section wants this to be a module, not a test file.
    # trick into thinking this hashref is a member of Test::Acme::System
    my $data = {}; bless $data;
{% endcodeblock %}

This is the only part of this whole technique that feels truly hacky. If anyone has suggestions for better ways to manage this, let me know.

### Overriding `IPC::Run::run` in a test

There are lots of ways to override a module's methods; I have had good experiences with [Test::MockModule](http://search.cpan.org/perldoc/Test::MockModule). It's pretty easy.

#### Write a callback that emulates `IPC::Run::run`

Here's the code that makes that evil hack above worthwhile. Here's all you have to do to recover those canned program execution results, using the `section_data` method provided by `Data::Section` (and that hacky `$data` reference):

{% codeblock lang:perl %}
    sub mock_ipc_run {
        my($cmd, $stdin, $stdout, $stderr) = @_;
        $$stdout = ${$data->section_data(join(" ", @$cmd))};
    }
{% endcodeblock %}

#### "Mock" that in place

{% codeblock lang:perl %}
    # override the real run object with one that will use the __DATA__ block
    my $module = new Test::MockModule('IPC::Run');
    $module->mock('run', \&mock_ipc_run);
{% endcodeblock %}

### Actually doing the testing

At this point, test away!

{% codeblock lang:perl %}
# Actually "run the tests", using the canned results from the __DATA__ block
cmp_ok(Acme::System::pidsum(), "==", 8278);

cmp_ok(Acme::System::vmstat_col("buff"), "==", 194240);
cmp_ok(Acme::System::vmstat_col("si"), "==", 0);
cmp_ok(Acme::System::vmstat_col("cs"), "==", 51);
cmp_ok(Acme::System::vmstat_col("swpd"), "==", 648);

done_testing;
{% endcodeblock %}

So I can (independently) calculate what the results should have been, given the arbitrary data I've saved in the `__DATA__` block, and test based on those values. Awesome.

{% codeblock lang:perl %}
jbarratt@dev:~/work/Acme-System$ prove -l t/00-fakerun.t 
t/00-fakerun.t .. ok   
All tests successful.
Files=1, Tests=5,  0 wallclock secs ( 0.01 usr  0.03 sys +  0.00 cusr  0.10 csys =  0.14 CPU)
Result: PASS
{% endcodeblock %}

### Trust me, the normal code will still actually call the system

Just for fun, I threw in a [script that actually uses this module to get live data](http://github.com/jbarratt/Acme-System/blob/master/bin/live):

{% codeblock lang:perl %}
    use Acme::System;

    print "Sum of all system PID's: " . Acme::System::pidsum() . "\n";

    print "Current CPU user time: " . Acme::System::vmstat_col("us") . "\n";
    print "Current Free Mem: " . Acme::System::vmstat_col("free") . "\n";
{% endcodeblock %}

And sure enough, if you run it, the data is getting updated live. `IPC::Run` really is working on the live system.
{% codeblock lang:console %}
jbarratt@dev:~/work/Acme-System/lib$ ../bin/live
Sum of all system PID's: 367273
Current CPU user time: 0
Current Free Mem: 70448
jbarratt@dev:~/work/Acme-System/lib$ ../bin/live
Sum of all system PID's: 367291
Current CPU user time: 0
Current Free Mem: 70556
{% endcodeblock %}

## Wrapping it all up

Other than the hackish trick to get `Data::Section` working in what's not really a module, this code is really clean, readable, and easy to maintain. It works well for pretty much any module you might care to use instead of `IPC::Run` -- there are lots of options, but as long as you use one of the module-ized ones, you can hook the module name and go from there.

Especially if you write lots of sysadmin tools, and especially if they have costs or risks associated with running them (`fsck`? `rm -rf`?) this technique can be a lifesaver. It's only as good as the inputs you give it, though. I made a mistake the first time I figured this workflow out of grabbing an output which, in real life, ended up with more whitespace than I'd accounted for, because the counters had gotten bigger between when I snagged my "output to test with" and when it was running on "live output."

I hope it helps, and if you have any suggestions about how to improve the technique, let me know (or send a pull request!)
