<!--
.. title: Capturing short-lived programs on Linux
.. date: 2010/06/14 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

One of the things I love most about DTrace is your [ability to do things like this.](http://www.brendangregg.com/DTrace/shortlived.d) Because you can ask the kernel to let you start tracking when something cool happens (like forking a new program), you can instrument it.

```
// Measure parent fork time
syscall::*fork*:entry { /* save start of fork */
	self->fork = vtimestamp;
}
```

Sadly, those tools aren't available on a standard issue Linux machine. (You can do it with [SystemTap](http://sourceware.org/systemtap/wiki/systemtapstarters), but it's not on every server I end up looking at.) Today I was trying to track down some processes that were making very odd DNS lookups. I isolated the user ID making these calls via iptables logging:

```
iptables -I OUTPUT 1 -m string --string "BADZONE" -d 127.0.0.1 -p udp --destination-port 53 --algo bm -j LOG --log-uid --log-prefix "BADZONE: "
```

But this user's PHP scripts were getting launched and dying again quickly. How to find out what was going on inside them? This hacky little trick actually worked really well. You can download it from [my git utilities directory.](http://axis.serialized.net/gitweb/?p=utilities.git;a=blob_plain;f=auto_stracer;hb=HEAD)

Basically, we check the process list as fast as we can for any owned by that user; If you find one, stick an strace on it. The script will 'hang around' until all the strace processes have finished. You end up with a directory full of trace files which you can then post-grep through to get what you need.

The short version is I was able to catch one of that user's programs doing the odd behaviour within about 30 seconds of running this tool, which was great!

``` perl
#!/usr/bin/perl

use warnings;
use strict;
use Getopt::Long;

my $opt = {};
GetOptions($opt, "uid=i", "number=i", "help", "man");

if($opt->{help} || $opt->{man} || !defined($opt->{uid})) {
    print "Usage: auto_stracer --number <processes to capture> --uid <numeric uid>\n";
    exit; 
}
$opt->{number} ||= 5;

my $traced = 0;
my %seen = ();
my @pids = ();
my %ourpid = ();
$ourpid{$$}++;

$SIG{INT} = sub { kill 9, @pids; print "Interrupt: Killed all running strace processes and quitting.\n"; exit;};

while ($traced < $opt->{number}) {
    for my $line (split(/\n/, `ps -Ao 'uid,pid'`)) {
        $line =~ s/^\s+//g; # eat leading spaces
        my($uid, $pid) = split(/\s+/, $line);
        next if($ourpid{$pid}); # don't run on something we are tracking
        if($pid && $uid eq $opt->{uid} && !$seen{$pid}) {
            $seen{$pid}++;
            my $st_pid = do_strace($pid);
            $ourpid{$st_pid}++;
            push(@pids, $st_pid);
            $traced++;
            last if ($traced >= $opt->{number});
        }
    
    }
}

print "Traced $opt->{number}, waiting for all to finish\n";
my $kid = 0;
do {
      $kid = waitpid(-1, 0);
} while($kid>0);
print "All processes completed, exiting.\n";
exit;

sub do_strace {
    my($pid) = @_;
    my $ourpid = fork();
    return $ourpid if($ourpid != 0);
    my $cmd = "strace -p $pid -f -s 65535 -o trace.$pid.$$ -v";
    print "\tcmd: $cmd\n";
    system($cmd);
    exit;
}
```

So, very brute force compared to the elegance of systemtap or DTrace, but when you need it, it's still handy.
