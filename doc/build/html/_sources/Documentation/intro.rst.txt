Introduction
============

Blender is a wonderful tool that anyone can download for free and start using to create 3D objects
and scenes.  These can be incredibly life-like and realistic, and there are many tutorials in how
to get started.  If you are artistically minded then these tutorials will be very helpful and there
are many more to continue learning how to sculpt things into the shapes you want to build.  If, 
however, you come from a programming background and just want to make a model to protype something,
then a tutorial explaining how to move and rotate a cube, then add another point to make the shapes
slightly more complicated can seem a bit frustrating.  Blender includes a python interpretter, so
you could try to dive into that and manipulate objects without having to tweak points in three
dimensions.  You will soon find that the python API seems to be written in a way that probably makes
a lot of sense if you understand the internals of Blender, but not so much when you're new.  What's
more you'll find a myriad of once helpful script examples which refer to a previous version of the
API and no longer work.  Eventually, you'll just about scrape together some code that you think
should work and you'll run it, expecting to see an array of lovely textures, and your model will be
about the right size and shape, but grey and lifeless, because no one told you which button you have
to press to see the textures rendered!
\</rant\>

The aim of Blogo is to allow anyone with knowledge of python create 3d structures in a simple and
intuitive way.  With an API that doesn't change and which does most of the little things for you.
It is not designed to be able to give photo perfect renderings, but it does output something that
can be manipulated in Blender manually if you want to do that.  It does this by providing a Logo-like
interface to python.

The basic idea is that each Blogo object describes a two dimensional cross section (defaulting to a
square) which is moved through space leaving behind a trail where it has been.  It is moved through
space using simple commands such as *forward*, *left*, *right*, *up*, *down*.  The cross section can
be modified to give any shape and can further be modified by multipliers, i.e. each of the points 
on the right of the cross section can be placed twice as far from the middle.  This allows a wall,
for example, to be constructed easily by saying that the square cross section should have the left
and right sides 0.05 metres away from the middle and the bottom should be 0 metres from the middle 
and the top 2.4 metres from the middle.  Then by repeating four times *move forward by 10 metres*, 
*turn right 90 degrees* you will get a wall around a 10m x 10m square.

The interface is designed to make it simple to do things that people are likely to want.  If you 
want to add a texture to that wall, then you can use the *add_texture* function and give it a filename
and that image will be on the wall, if you want a particular colour then a tuple of RGBA colour values
can be used instead.

