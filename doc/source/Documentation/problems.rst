Potential Problems
==================

These are some problems you may find and how to fix them
########################################################

If nothing is drawn or large sections are missing
*************************************************
At the end of your code you need to call Blogo.clean_up() which will cause the 
objects to be rendered, otherwise they are just meshes in memory.

Alternatively, you may have done something silly like put the pen up and forgotten to put it down again?

Or it may be a bug - if you think it is, then please let me know.

----

The width is not changing as it should
**************************************
By default the width function is called every 0.1m or 100 times, which every is smaller.
This means that if you have a 10m line, which is supposed to have a smooth curve, then you will
only get changes to the width every 0.1m, and it won't look smooth.  You can change how often
the width function is called to occur more often.

Alternatively, if the line is defined by several calls to `set_pos` then the line segments will
only be drawn when forward is called, so after each position change you can run `fd(0)` and it
will insert another cross section at that location.

----

Everything is dark
******************
All of the lights in your scene may have be deleted.  To illuminate the scene with a large bright light
overhead call::

    BlogoUtils.add_light_area()

