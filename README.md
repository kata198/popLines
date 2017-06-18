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

For all actions which provide a line number, the numbers are 1-origin (first line is "1", second is "2").

The followings modes and their associated command name are given:

**Head** - popHead \[numLines\] \[filename\] - Removes "numLines" from the top of provided "filename", and prints them on stdout.

If *numLines* is a negative number, -N, popHead will pop lines starting from head up until the Nth-to-last line. For example, calling popHead -2 on a file with 6 lines will pop the first 4.


**Tail** - popTail \[numLines\] \[filename\] - Removes "numLines" from the bottom of provided "filename", and prints them on stdout.

If *numLines* is a negative number, -N, popTail will pop lines starting from tail up until the Nthline. For example, calling popTail -3 on a file with 8 lines will pop the last 5.


**Random** - popRandom \[numLines\] \[filename\] - Removes "numLines" from random positions within provided "filename", and prints to stdout in a random order.


You can pass the --ordered flag, and the randomly-selected lines will be output in the same order they appear in the file. By default, the random lines will be output in random order.


**Range** - popRange \[start\] \[stop\] (optional: \[step\]) \[filename\] - Removes lines using inclusive 1-origin start, stop, and optional step, and prints to stdout. Negative numbers are supported to mean "from the end", -1 is last line, -2 is second-to-last line.

**These** - popThese \[line1\] \[...lineN\] \[filename\] - Removes specific lines given 1-origin numbers. If numbers are out of range, that number will be ommited. Lines are returned in provided order, and duplicates are allowed. Negative numbers are supported to mean "from the end".


Peeking
-------

By default, the pop\* commands are designed to implement queues, and thus they perform real "pops" and remove the elements extracted from the source file.

If you'd just like to "peek" (extract lines but keep them in the source), add "--peek" when invoking any of the pop\* commands.


Module
------

Functionality is exposed through a module, PopLines, which can perform all the same operations.

You can checkout the pydoc here: http://pythonhosted.org/AdvancedHTMLParser/
