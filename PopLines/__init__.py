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


# POP_TYPES - All available pop types as modes for picking which lines to remove-and-return
#
#    head     - Remove from the top, numLines items
#    tail     - Remove from the bottom, numLines items
#    random   - Remove and sort randomly, numLines items
#    range    - Remove an inclusive range. numLines is a tuple of (start, finish)
#    these    - Remove specific lines, 0-origin. numLines is an array of 0-origin line numbers to remove.
POP_TYPES = ('head', 'tail', 'random', 'range', 'these')

__version__ = '1.1.1'
__version_tuple__ = (1, 1, 1)

__all__ = ('POP_TYPES', 'popLines', 'popHead', 'popTail', 'popRandom', 'popRange', 'popThese')


def popLines(popType, numLines, filename):
    '''
        popLines - Remove lines from a given file, and return them.

            @param popType <str> - The mode of selection to use when picking which lines to pop.

              Types are:

                head     - Remove from the top, numLines items
                tail     - Remove from the bottom, numLines items
                random   - Remove and sort randomly, numLines items
                range    - Remove an inclusive 1-origin range. numLines is a tuple of (start, finish) or (start, finish, step). Use of negatives is allowed 
                            [e.x. (3, -1) returns the third line and all further, up to and including the final line]
                these     - Remove specific lines, 1-origin. numLines is an array of 1-origin line numbers to remove.
                            [e.x. [3, 5, 6, 8] removes the third, fifth, sixth, and eigth lines.]


            @param numLines <int/tuple(see below)> - Generally, number of lines to remove from filename. If there are not this many lines, every line in the file will be removed. Some values of #popType overload this value, see above.


            @param filename <str> - Path to the filename to pop lines

            @raises ValueError - Raised if invalid argument passes
            @raises IOError - If any error during reading/writing to file

        @return list<str> - A list of the lines removed from the file. If converting to a string, join with "\n", and if length > 0 then add a final newline.
    '''

    if popType not in POP_TYPES:
        raise ValueError('Given popType %s does not match available pop types: ( %s )' %(str(popType), ', '.join(POP_TYPES)))

    if popType in ('head', 'tail', 'random'):
        try:
            numLines = int(numLines)
            if numLines <= 0:
                raise ValueError('negative number')
        except:
            raise ValueError('Number of lines must be a positive integer.')
    elif popType in ('range', 'these'):
        if not issubclass(numLines.__class__, (tuple, list, set, frozenset)):
            try:
                # Try to cast to a tuple
                numLines = tuple(numLines)
            except:
                raise ValueError('Invalid type for numLines. Given pop type %s, numLines should be an array. See help(popLines) for more info.' %(popType, ))
        if popType == 'range':
            numLinesLen = len(numLines)
            if numLinesLen == 2:
                # (start, end)
                (rangeStart, rangeStop) = numLines
                rangeStep = 1
                #  To validate or not to validate... I think not.  Better to return nothing than trash the file.
            elif numLinesLen == 3:
                # (start, end, step)
                (rangeStart, rangeStop, rangeStep) = numLines
                if rangeStep <= 0:
                    raise ValueError('Step must be an integer > 0')
                if rangeStart == 0:
                    raise ValueError('Invalid start for "range" pop type. Must be 1-origin. 0 was provided.')
                if rangeStop == 0:
                    raise ValueError('Invalid end for "range" pop type.  Must be 1-origin. 0 was provided.')
                    
            else:
                raise ValueError('Wrong number of arguments for "numLines" param with "range" pop type. Should be 1-origin inclusive (start, stop) or (start, stop, step)')

            # 1-origin to 0-origin
            if rangeStart > 0:
                rangeStart -= 1
        elif popType == 'these':
            if 0 in numLines or '0' in numLines:
                raise ValueError('Specific line numbers are 1-origin. 0 was given.')
                
                

    
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
    elif popType == 'range':
        if rangeStart < 0:
            rangeStart = len(lines) + rangeStart
        if rangeStop < 0:
            rangeStop = len(lines) + rangeStop + 1
            
        
        if rangeStop == 0:
            # Don't want a zero-length string because they asked for up-to-and-including the last line
            output = lines[rangeStart : : rangeStep ]
        else:
            # Grab the output range
            output = lines[rangeStart : rangeStop : rangeStep]

        # Now, generate remaining file
        if rangeStep == 1:
            # Simple range
            lines = lines[:rangeStart] + lines[rangeStop:]
        else:
            lines = lines[:rangeStart] + \
                [lines[rangeStart+i] for i in range(rangeStop - rangeStart) if i % rangeStep == 0] + \
                lines[rangeStop:]
    elif popType == 'these':
        specificItems = []
        for num in numLines:
            try:
                num = int(num)
            except:
                raise ValueError('Non-integer provided as specific line numbers. Should be one-origin integers.')
            if num < 0:
                num = len(lines) + num + 1
                if num <= 0:
                    continue

            if num <= len(lines):
                specificItems.append(num-1)

        
        output = [lines[i] for i in specificItems]
        lines = [lines[i] for i in range(len(lines)) if i not in specificItems]

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

def popRange(start, stop, step, filename):
    '''
        popRange - Pops a given range (1-origin, inclusive) from a file.

        @see popLines

        Shortcut for popLines('range', (start, stop, step), filename)
    '''
    return popLines('range', (start, stop, step), filename)

def popThese(lineNumbers, filename):
    '''
        popThese - Pops specific lines (1-origin) from a file

        @see popLines

        Shortcut for popLines('these', lineNumbers, filename)
    '''
    return popLines('these', lineNumbers, filename)

