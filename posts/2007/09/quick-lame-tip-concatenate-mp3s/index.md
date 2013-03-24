<!--
.. title: Quick LAME tip: concatenate mp3's
.. date: 2007/09/24 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

If you want to join, append, or concatenate multiple MP3's without packing them into a container (like 'mp3join' does), you can do so with 'find' and 'lame.' This example also transcodes down to a mono file (-a) and drops the bitrate to 96 (-b 96) -- I was converting spoken word from iTunes default rips.

<code>find . -name '*.mp3' -exec lame --decode '{}' - ';' | lame -a --tt "Title" --tl "Album" --ta "Artist" -b 96 - concatenat.mp3</code>

I was annoyed enough by trying to solve this via google that I figured I'd cache it here for myself and the rest of humanity.
