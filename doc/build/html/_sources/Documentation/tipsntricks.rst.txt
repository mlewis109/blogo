Tips 'n' Tricks
===============

These are some tips that could be useful

----

To make a square edge, go forward by the width, then back by the same amount.

----

A cross section is only laid down when `forward` or `backward` are invoked.  This means, for
example, that repeated calls to `set_pos` will not show up.  To get them to show up then 
insert::

    fd(0)




