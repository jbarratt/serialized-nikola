<!--
.. title: Useful Electronics: Cat Accident Preventer
.. date: 2009/02/23 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

I am the owner of a generally very awesome product -- a [Litter Robot](http://litter-robot.com) automated cat litter box.

However, we occasionally have an issue where the box malfunctions in some way. This is either because
<ul>
<li>The switch which gets tripped when the cats go in stops working, thus never initiating the self-cleaning service. Horrible consequence: the house starts to smell because the crap stays in the sand.</li>
<li>The box ends up stuck in the 'dumping out the crap' state (upside down.) Horribler Consequence: the cats refuse to use the box, thus finding alternative (and far less pleasant) places to relieve themselves.</li>
</ul>

If you are familiar at all with the delicate scents of cat defecates you will appreciate my desire to eliminate both of these issues.

So, I thought to myself that if I only had some way to track when the box was in it's normal state, and not in it's normal state, I would be able to alert my wife and I to either malfunction state soon enough that we could deal with it.

Hence, the below design was born.

![Litter Robot Malfunction Detector](/images/litter-robot-malfunction-detector.png)

It uses a very nice and yet simple sensor (with a pullup resistor to get a clean signal) called a [Reed Switch](http://www.sparkfun.com/commerce/product_info.php?products_id=8642) which creates a closed circuit when it's near a magnetic field. I can epoxy this to the un-moving base of the Litter Robot, and epoxy a small magnet to the corresponding spot on the inside of the dome. (Inside rather than outside so it does not interfere with the dome's rotation.)

I then read this sensor from an [Arduino](http://www.sparkfun.com/commerce/product_info.php?products_id=666) board. This would be ridiculous overkill just to get a simple binary signal into a computer, but I'll be using the Arduino for other home automation tasks. (Temperature Sensing, power switch control, etc.) Whenever it changes state, it can send a message over the Serial-over-USB cable to my very low power home NAS. (Which will probably be another blog entry, as it's a work in progress.) This can store in a local database every time the state changes, and have a simple Perl script wake up every 20 minutes to see
<ul>
<li>If the box has not rotated for more than 6 hours</li>
<li>If the box has been off the 'home' position for more than 40 minutes.</li>
</ul>

It then sends us an SMS (just an email to `10 digit number`@txt.att.net) to alert us. This is a nice form of alert because if I'm home, it might wake me, but not anyone else. If I'm at work, I'm close enough to make a quick lunch break trip home and resolve it before anything stinky happens. If I'm on a trip, I can give a friend with house keys a quick call and ask for a favor.

I have ordered all the parts for this project and should be ready to go soon. Other than the Arduino, the whole thing can be built for about $2 in parts. I'll hopefully be posting an entry soon with the Arduino and Perl code that makes it all work and photos. (That is, unless I fail in an epic fashion.)
