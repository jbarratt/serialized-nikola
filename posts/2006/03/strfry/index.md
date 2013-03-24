<!--
.. title: strfry()
.. date: 2006/03/19 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

I am not making this up.

{% codeblock lang:text %}
    NAME
        strfry - randomize a string

    SYNOPSIS
        #include <string.h>

        char *strfry(char *string);

    DESCRIPTION
        The  strfry()  function  randomizes  the  contents  of  string by using
        rand(3) to randomly swap characters in the string.  The  result  is  an
        anagram of string.

    RETURN VALUE
        The strfry() functions returns a pointer to the randomized string.

    CONFORMING TO
        The  strfry()  function  is  unique  to  the  Linux C Library and GNU C
        Library.
{% endcodeblock %}
