popLines
==========

Tools to pop lines from the head/tail of a file to stdout. You can also remove random items from the given files to stdout.

This allows you to treat a file on disk as a queue.


Modes
-----

**Head** - popHead [numLines] [filename] - Removes "numLines" from the top of provided "filename", and prints them on stdout.


**Tail** - popTail [numLines] [filename] - Removes "numLines" from the bottom of provided "filename", and prints them on stdout.


**Random** - popRandom [numLines] [filename] - Removes "numLines" from random positions within provided "filename", and prints to stdout in a random order.


Module
------

Also comes with a module, PopLines, which can perform the same operations within a script.


