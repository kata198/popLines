# popLines
Tools to pop (remove and return) lines from files, with a variety of modes.

This allows you to treat a file on disk as a queue, or to easily strip lines from a file, and many other uses.


Example
-------

	[cmd]$ cat test # Show original file
	one
	two
	three
	four
	five

	[cmd]$ popHead 2 test # Remove two lines from head of the file
	one
	two

	[cmd]$ cat test # Show that lines have been removed from file
	three
	four
	five



Modes
-----

The followings modes and their associated command name are given:

**Head** - popHead \[numLines\] \[filename\] - Removes "numLines" from the top of provided "filename", and prints them on stdout.

**Tail** - popTail \[numLines\] \[filename\] - Removes "numLines" from the bottom of provided "filename", and prints them on stdout.

**Random** - popRandom \[numLines\] \[filename\] - Removes "numLines" from random positions within provided "filename", and prints to stdout in a random order.

**Range** - popRange \[start\] \[stop\] (optional: \[step\]) \[filename\] - Removes lines using inclusive 1-origin start, stop, and optional step, and prints to stdout. Negative numbers are supported to mean "from the end", -1 is last line, -2 is second-to-last line.

**These** - popThese \[line1\] \[...lineN\] \[filename\] - Removes specific lines given 1-origin numbers. If numbers are out of range, that number will be ommited. Lines are returned in provided order, and duplicates are allowed. Negative numbers are supported to mean "from the end".

Module
------

Functionality is exposed through a module, PopLines, which can perform all the same operations.


