Quickstart
==========

This page should give you all the information needed to create something in blender very quickly

#. First you need to download and install Blender.  This can be done from https://www.blender.org/download/
#. Next copy the files from Blogo/src/ into \<blender_install_dir\>/scripts/ 
   (there are two directories in /src/ which should both already exist in scripts, the contents should be merged in)
#. Then run Blender, choose "New File/General" and you should see a cube floating in the middle of a pair of axes.
#. Hit Shift+F4 on your keyboard to take you to the python console.
   (There is a scripting section which will let you edit code in Blender, I prefer to edit code outside Blender)
#. Create a file somewhere which contains

   .. literalinclude:: ../../../examples/first.py

   Let's assume this file is called "c:/dev/first.py"
#. Back in the Blender python console type

    .. code-block::

	    show("c:/dev/first.py")

   and press ENTER.
#. After a short pause you should see a pretty yellow flower.  You can click on the X/Y/Z in the top
   right corner of the view to rotate round it and use the magnifying glass to zoom in or out, the hand
   to pan around it.
#. Now either play around with the files in examples/ or adding some more code to first.py

