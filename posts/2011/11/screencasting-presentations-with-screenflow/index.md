<!--
.. title: Screencasting Presentations With Screenflow
.. date: 2011/11/18 12:42
.. slug: index
.. tags:
.. link:
.. description:
-->


I've been really enjoying screencasting my presentations, and have come
up with a nice workflow using the (commercial) Mac app [ScreenFlow](http://www.telestream.net/screen-flow/).

Watch the video for the full details, but the basic process is:

* Record the screen while you give the presentation in "presenter mode" (so notes are available)
* Also record video from your computer's camera
* Crop down to just the slide portion of the presenter view
* Overlay the video on the slides and make it fully transparent (Opacity 0%)
* Skim through the video, watching for slide changes as cues
* Insert video actions (⌘K) and flip the Opacity between (100%/0%) to
  show the slide or the video.

At this point, I can come up with a very nice 'canned version' of a
presentation in only slightly more than the time it takes to simply give the presentation. It's also a great way to rehearse!

In the video I also recommend the [Samson Go Mic](http://www.amazon.com/gp/product/B001R76D42?ie=UTF8&tag=httpserianet-20&linkCode=shr&camp=213733&creative=393185&creativeASIN=B001R76D42&ref_=sr_1_1&qid=1321651654&sr=8-1), ($40) which I've been nothing but happy with.

(The full list of [Screenflow Keyboard Shortcuts](http://www.telestream.net/pdfs/technical/screenflow-shortcuts.pdf) is good to keep handy.)

<iframe src="http://player.vimeo.com/video/32279774?title=0&amp;byline=0&amp;portrait=0" width="400" height="255" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>

A technical side note: the video quality in the beginng of the video is a
little off. The actual "presentation" was in 4:3, but the application
demo was widescreen. This meant a bit of `ffmpeg` magic, (attaching
'letterboxes' to the sides to make it effectively widescreen) so I could glue
the two videos together. When you actually use this method to simply
give a presentation, it ends up looking even nicer.

```
$ ffmpeg -i Presentation.mov -s 560x416 -r 30000/1001 -padleft 46 -padright 48 -vcodec libx264 -vpre hq -acodec libf@c -ac 2 -ar 48000 -ab 192k PresentationLetterbox.mov
```
