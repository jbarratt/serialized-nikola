<!--
.. title: Using Ogres to Improve Your Designs
.. date: 2011/10/21 18:01
.. slug: using-ogres-to-improve-your-designs
.. tags:
.. link:
.. description:
-->


## The problem

Creating new designs (in whatever domain) is always a bit of a tightrope walk -- especially as an organization grows. How much do we try and figure out in advance, vs learning and adjusting as we go? How many people do we involve at what stage of the process?

When the design you're working on will be largely owned and maintained by a 24x7 operations team, this "involvement" aspect can be particularly vital. It's hard to imagine building a great and coherent design with 20+ people, but 20+ people still have to be full educated about how the system works, (largely) satisfied with the decisions that are made -- and, more importantly, have **years** of collective experience that can help find weak points or make vital improvement suggestions.

## An approach

Our current strategy is:

* have a small team produce designs/prototypes/working code
* have periodic larger-scale reviews for education, analysis and feedback.

What those "reviews" look like is a design that is, itself, undergoing incremental learning and feedback.

Our first stabs at it were fine, but clearly could be improved a lot. We brought the team together, walked through some slides, and did Q&A. In that format, though, there's a pretty low upper bound on the number of people that can contribute at any moment. 20+ people in a "one person talks" scenario means a lot of standing around, which isn't a great use of anyone's time, and isn't likely to even end up granting much attention and focus.
 
This week, we attempted at "version 2", which while still not perfect, was a lot better.

# Objectives

1. Actually make the product great. (Or, barring that, "better.")
2. Create more (actual) shared ownership and understanding of the design.
3. Enhance the social network between the teams so that ad-hoc collaboration becomes more likely in future.
4. Improve shared vocabulary and methods around value and risk management (which we are [bad at doing intuitively](http://discovermagazine.com/2011/jul-aug/11-what-you-dont-know-can-kill-you))
5. Make good use of everyone's time: be engaging and effective.
6. Have fun!

# How It Works, and what was that you were saying about Ogres?

## Background 

I love the book [Gamestorming](http://goo.gl/GMR8e). It's full of frameworks and patterns for having more than a few people interact in ways that's both engaging and effective.

The review we did was based on the Gamestorming game [Challenge Cards](http://www.gogamestorm.com/?p=572).
In brief, you form two teams: one team creates challenges to the design, the other creates solutions.

> The challenge team picks a card from the deck and plays it on the table, describing a scene or event where the issue might realistically arise. The solution team must then pick a card from their deck that addresses the challenge. If they have a solution they get a point, and if they don’t have a solution the challenge team gets a point. The teams then work together to design a card that addresses that challenge.

For fun, and to emphasize the game aspect (and dampen issues with taking criticism personally), I brought in a silly element of making the "solution team" be Knights, defending a castle -- and the "challenge team" be gnarly Ogres. 

The art and concepts were introduced in some pre-made cards for playing the game, and in the slide deck that introduced the game to the players. (All of that can be downloaded at the end of the post.)

## Gameplay

<img src='/images/KnightRoundtableSmall.jpg' align='right' width='240' height='180' title='The Knights prepare their defense' alt='The Knights prepare their defense'/>
The basic flow of the event (which took about 90 minutes total, each step being timeboxed) was:

1. Get together, and do a brief review of the current design (focusing on recent changes, and in-progress work.) People get handouts of the architecture to review through the game.
2. Split into two teams, Knights and Ogres, both of whom headed to their own rooms. (Anyone could choose to be on either team.)
3. As a group, use the [Heuristic Ideation Technique](http://www.gogamestorm.com/?p=470) (more on that below) to brainstorm approaches for solution/challenge.
4. Form smaller groups, and create the cards for the Challenge.
5. Meet back up, and play through the decks as described above.
6. Reconvene as a larger group and debrief.

<img src='/images/InCombatSmall.jpg' align='right' width='240' height='180'/>
## Heuristic Ideation?

This is a clunky name for a [simple and cool idea](http://www.gogamestorm.com/?p=470). 

I used it to help brainstorm points of potential weakness in the design -- breaking things down into "attributes and actions" and "components."

Attributes are things *about* the system: Capacity, Security, Reliability, ...
Actions are things we know can *change* in the system: Upgrade, Deploy, Replace, Fail, ....

Components cover *physical* things: Hard Drive, Network Port, Switch, CPU, DIMM, ....
They also cover *logical* things, like Authentication System, Filesystem, User Interface, ...

I knew we'd end up with large enough lists that the grid layout called for in Heuristic Ideation wouldn't work -- our boards aren't that big -- so opted for this 2 column layout:

<img src='/images/HeuristicIdeationRiff.jpg' width='480' height='360'/>
You can apply each attribute or action in the left column to each of the
components on the right; by the time you get through all of them, you'll
have really thought through possible fragile areas of the system.

For example, take 'Filesystem' as a component; we can discuss it's
capacity, security, reliability, as well as what happens if we upgrade
it, run a deploy of new code, if it fails, ... and so on. Then, think
about all of those attributes and actions applied to the next component!
(Say, a network switch.)

## Comparative Risk

Instead of just using blank index cards, I threw a bit of layout at it.

<img src='/images/CompletedCards.jpg'/>
The extra fields help scope the risk a bit. (Obviously they are all going to be wild-ass guesses, but they still let us group things by order of magnitude.) Primarily, they're just there to get people talking in these kinds of terms about relative possible impacts of unlikely things.

The **#ragemode** tag came from one of our customers who was on the bad end of a miscommunication surrounding some backups, and how fresh they were, (a bit _too_ fresh, in his case), leading to them losing some data. It refers to the fact that some things, when they go wrong, give us the reaction "hey, it's the internet, these things happen." Others are **infuriating**. So it's an attempt to let us weight possible failures by emotional impact.

When 2 cards are paired up, you can just do the math:

(Time to detect + Time to repair) * Customers Impacted * Expected times per year that this freakish thing might happen * #ragemode == A very fuzzy estimate of "customer-minutes of impact per year."

## Lessons

It was a lot of fun, and met (to at least some degree) all of the objectives I had for it. We're still going through the cards and learning from them.

However, there was a lot of room for improvement.

First, Heuristic Ideation is awesome. We can use that in all kinds of different scenarios. I'm writing up a list of the Components/Actions/Attributes the teams brainstormed for the wiki, so we can use and further develop them in the future.

The biggest improvement to the game is in the Challenge/Solution dynamic. The Challenges tended to be very specific. ("Filesystem gets corrupted.") However, the Solutions have to be pretty generic. ("Reinstall the server from scratch and restore from backup.") Technically, that counted as a point-worthy exchange for the defense, but it didn't really help us explore the problem.

<img src='/images/GiveUpSmall.jpg' align='right' width='180' height='240' title='A good example of an overly generic defense' alt='A good example of an overly generic defense'/>
I'd like to try it this way:

* Still have the Knights do their defensive planning, but not actually make cards in advance
* When the challenge card is played, come up with (on the fly) the best solution we can currently execute.
  * If that is "good enough" (as decided by the players, or arbitrated by the facilitator), the Knights get a point.
  * If it's not, then the Ogres get the point, and then the two teams move on to collaboratively coming up with the solution.
  
That should keep the focus more on what really matters, and at the level of specifics, and less on the technicalities of "is your vague defensive card applicable here or not."

A neat thing we discovered was that if someone proposed an attack for which our "defenses" were already good enough, that was a good data point that training/documentation/education needed to be beefed up around that aspect.

One of the Operations Managers had a great suggestion: now that everyone gets the basics, use this framework for fire drills. (Now known as "surprise attacks" or "Ogre Rush!") Just pop into the NOC with a few of the "Attack" cards all filled out, and make sure people are solid on what the procedure would be to deal with that.

# Share and Enjoy

Please feel free to rip off any part of this that was useful at all.
I have compiled both PDF versions of the instructional slide deck and playing cards, as well as the original Keynote files.

[Knights vs Ogres Game Materials](http://serialized.net/images/KnightsVOgres.zip)

I made my best effort to track down royalty free art -- please contact me if I've inadvertently used something of yours!
