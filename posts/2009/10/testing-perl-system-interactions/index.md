<!--
.. title: Testing perl system interactions
.. date: 2009/10/06 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->


**Update**: I have refined this technique and uploaded a more full-stack example to GitHub. [Testing Perl code that runs commands](/2010/09/testing-perl-code-that-runs-commands/).

A lot of the code I end up needing to work on makes calls to various executables to read and process system state. It might be DTrace, or one of the tools that comes with the Virtuozzo/OpenVZ management suite, or one of the HP hardware monitoring tools -- they all want to be called from the command line.

In the old days, I probably would have just used perl backticks to run the command and capture the output. I'd "test" on a machine that had those tools installed, and call it a day.

``` perl
my $output = `some system command`;
# process the output here
```

However, that's pretty evil, and it's essentially untestable.

Here's a pattern that works pretty well.

The IPC::Run module includes a 'run' command, which in the simple form takes 4 references: To a list of a command and it's arguments, and then scalar references for the contents of Standard In, Standard Out, and Standard Error.

If all you care about is capturing STDOUT, you might call it like:

``` perl
my @raidstate = ("hpacucli", "'controller slot=0 physicaldrive all show'")
my $raid_output;
IPC::Run::run(\@raidstate, \undef, \$raid_output, \undef);
```

Ok, but how does that help us test?
Enter the venerable Test::MockModule.

All I need to do is override the run() function for the module in my test!

``` perl
use Test::MockModule;

my $module = new Test::MockModule('IPC::Run');
$module->mock('run', \&mock_ipc_run);
```

Ok, so how do I get the right content to get in the $raid_output?

It depends on how exactly you're calling run: I hand-tuned this for the specific use case I'm doing right now, where I just care about capturing output.

What we do is store a list of command lines in the data block, followed by their output. When someone calls 'run()' with one of those command lines, we send that output back to them.
 
``` perl
sub mock_ipc_run {
    my($cmd, $stdin, $stdout, $stderr) = @_;
    # very important to rewind DATA so this subroutine can be called more than once
    seek(DATA, 0, 0);
    my $cmd_str = join(" ", @$cmd);
    while(<DATA>) {
        # iterate until we match the command name with '*' @ the beginning
        if(/^\* $cmd_str/) {
            while(<DATA>) {
                # until we find another command entry...
                if(/\*\s/) {
                    return;
                } else {
                    # pack the results into the $stdout reference we were given
                    $$stdout .= $_;
                }
            }
        }
    }
}
```

And the matching section in the DATA block:

```
__END__
* hpacucli 'controller slot=0 physicaldrive all show'

Smart Array P400i in Slot 0

  array A
   physicaldrive 1I:1:1 (port 1I:box 1:bay 1, SAS, 73.4 GB, OK)
   physicaldrive 1I:1:2 (port 1I:box 1:bay 2, SAS, 73.4 GB, OK)
   physicaldrive 1I:1:3 (port 1I:box 1:bay 3, SAS, 73.4 GB, OK)
   physicaldrive 1I:1:4 (port 1I:box 1:bay 4, SAS, 73.4 GB, OK)
   physicaldrive 2I:1:5 (port 2I:box 1:bay 5, SAS, 73.4 GB, OK)
   physicaldrive 2I:1:6 (port 2I:box 1:bay 6, SAS, 73.4 GB, OK)
```

And you're done! This is nice and easily extensible. If you have several specific use cases (like output that actually starts with '* ', for example, or needing STDIN/STDERR) you'd need to modify it. It's a handy general pattern for making "sysadmin code" a lot more like "developer code", though. (The great thing is I was able to write and test this whole code suite on a VM that didn't even have an HP raid controller, let alone hpacucli installed, for example.)
