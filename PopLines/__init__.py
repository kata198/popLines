#!/usr/bin/env python
#
#    Copyright (c) 2016 Timothy Savannah All Rights Reserved
#  under terms of the GPL version 2. You should have recieved a copy of this with distribution,
#  as LICENSE. You may also find the full text at https://github.com/kata198/popLines/LICENSE
#

#  This program turns files into queues. You can pop off the head or tail of a file to stdout.
#   So your file can contain a list of items to process, and you can use this to pop off that queue.

#vim: set ts=4 sw=4 expandtab
import os
import random
import sys


POP_TYPES = ('head', 'tail', 'random')

__version__ = '1.0.0'
__version_tuple__ = (1, 0, 0)

__all__ = ('POP_TYPES', 'popLines', 'popHead', 'popTail', 'popRandom')

def popLines(popType, numLines, filename):
    '''
        popLines - Remove lines from a given file, and return them.

            @param popType <str> - one of the modes provided in POP_TYPES
            @param numLines <int> - Number of lines to remove from filename. If there are not this many lines, all that can be removed will be removed.
            @param filename <str> - Path to the filename to pop lines


            @raises ValueError - Raised if invalid argument passes
            @raises IOError - If any error during reading/writing to file

        @return list<str> - A list of the lines removed from the file. If converting to a string, join with "\n", and if length > 0 then add a final newline.
    '''

    if popType not in POP_TYPES:
        raise ValueError('Given popType %s does not match available pop types: ( %s )' %(str(popType), ', '.join(POP_TYPES)))

    try:
        numLines = int(numLines)
        if numLines <= 0:
            raise ValueError('negative number')
    except:
        raise ValueError('Number of lines must be a positive integer.')

    
    if not os.path.exists(filename):
        raise IOError('No such file or directory: %s' %(filename,))

    if not os.path.isfile(filename):
        raise IOError('Not a file: %s' %(filename,))

    try:
        with open(filename, 'rt') as f:
            contents = f.read()
    except Exception as e:
        raise IOError('Unable to read from file: %s (%s)' %(filename, str(e)) )

    lines = contents.split('\n')
    if not lines[-1]:
        lines.pop()

    if popType == 'head':
        output = lines[:numLines]
        lines = lines[numLines:]
    elif popType == 'tail':
        startPos = max(0, len(lines) - numLines)
        output = lines[startPos:]
        lines = lines[:startPos]
    elif popType == 'random':
        output = []
        if numLines >= len(lines):
            # If we are asking for more random elements than the file contains, return a shuffled list of the whole thing.
            output = lines
            lines = []
        else:
            # Otherwise, generate a list of non-duplicate random numbers, and assemble both lists using that.
            #  Do this instead of .pop for performance
            randNumbers = []
            maxNumber = len(lines) - 1
            minNumber = 0
            for i in range(numLines):
                nextNumber = random.randint(minNumber, maxNumber)
                while nextNumber in randNumbers:
                    # No duplicates
                    nextNumber = random.randint(minNumber, maxNumber)
                if nextNumber == minNumber:
                    minNumber += 1
                    while minNumber in randNumbers:
                        minNumber += 1
                elif nextNumber == maxNumber:
                    maxNumber -= 1
                    while maxNumber in randNumbers:
                        maxNumber -= 1

                randNumbers.append(nextNumber)
            output = []
            newLines = []
            for i in range(len(lines)):
                if i in randNumbers:
                    output.append(lines[i])
                else:
                    newLines.append(lines[i])
            lines = newLines

        # Randomize the result order
        random.shuffle(output)

    try:
        with open(filename, 'wt') as f:
            f.write('\n'.join(lines))
            if len(lines) > 0:
                f.write('\n')
    except Exception as e:
        raise IOError('Unable to write to %s (%s)\n' %(filename, str(e)))

    return output
        

def popHead(numLines, filename):
    '''
        popHead - Pops a given number of lines from the head of a file.

        @see popLines

        Shortcut for popLines('head', numLines, filename)
    '''
    return popLines('head', numLines, filename)

def popTail(numLines, filename):
    '''
        popTail - Pops a given number of lines from the tail of a file.

        @see popLines

        Shortcut for popLines('head', numLines, filename)
    '''
    return popLines('tail', numLines, filename)

def popRandom(numLines, filename):
    '''
        popRandom - Pops a given number of lines from random positions within a given file.

        @see popLines

        Shortcut for popLines('head', numLines, filename)
    '''
    return popLines('random', numLines, filename)
