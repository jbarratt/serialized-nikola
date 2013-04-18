<!--
.. title: How to catch up on a 100-something-challenge
.. date: 2009/01/17 13:37
.. slug: how-to-catch-up-on-a-100-something-challenge
.. tags:
.. link:
.. description:
-->

I have seen a lot of 100 something-or-other challenges online recently -- I'm currently, as I mentioned, doing the 100 burpee challenge from [Crossfit Santa Cruz.](http://www.crossfitsantacruz.com/crossfit_santa_cruz/burpee-challenge-details.html)

Here's the problem: I started the challenge on Jan 1st, and I became a [new dad](http://carterbarratt.com) on Jan 10th. I managed to do [some of them](http://twitter.com/jbarratt/status/1112197431), but I find myself behind.

The rule is, generally, that you need to do all the ones you missed. So if you missed, as I did, the 12th, 13th, 14th, 15th, 16th, 17th, and 18th (yikes) that means I need to do (12+13+14+15+16+17+18) = 105. It's cool, I'm good for it.

But it's kind of annoying to punch all those numbers into a calculator to find the number, and there's a good chance I'd typo something. Thankfully there is a math trick (with a good explanation over at [WikiHow](http://www.wikihow.com/Sum-the-Integers-from-1-to-N) for how to do it and how it works) for finding the sum of all the numbers from 1 to some number 'N'. Short version, the sum is 

```
(N*(N+1))/2
```

So if I want to find how many I missed between the 12th and the 18th, I just need to find the sum of 1 to 18 ( and subtract the part I already did, the sum from 1 to 11). In other words:

```
((18*19)-(11*12))/2, or 105.
```

Hence, a quick and dirty calculator. Just punch in the last count you did, the count you should be doing today, hit enter, and the third box will give you your wonderful total you need to do today (including today's.)

<script language="Javascript" type="text/javascript">
function calc_catchup(form) {
	var last = eval(form.last.value);
	var today = eval(form.today.value);
	var catchup = ((today*(today+1)) - (last*(last+1)))/2;
	form.catchup.value = catchup;
}
</script>

<form method='post' name='catchup_count' action='calc_catchup'>
<table>
<tr><td>Number you last actually did</td><td><input type='text' name='last' size='3' value='11' onchange="calc_catchup(this.form)"/></td></tr>
<tr><td>Number you should do today</td><td><input type='text' name='today' size='3' onchange="calc_catchup(this.form)" value='18'/></td></tr>
<tr><td>Number you need to do to today to be caught up</td><td><input type='text' name='catchup' size='4' value='105' onchange="calc_catchup(this.form)"/></td></tr>
</table>
</form>
