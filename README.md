# Blogo

## Introduction

The aim of Blogo is to allow anyone with knowledge of python create 3d structures in [Blender](https://www.blender.org/) in a simple and intuitive way. With an API that doesn’t change and which does most of the little things for you. It is not designed to be able to give photo perfect renderings, but it does output something that can be manipulated in Blender manually if you want to do that. It does this by providing a Logo-like interface to python.

The basic idea is that each Blogo object describes a two dimensional cross section (defaulting to a square) which is moved through space leaving behind a trail where it has been. It is moved through space using simple commands such as forward, left, right, up, down. The cross section can be modified to give any shape and can further be modified by multipliers, i.e. each of the points on the right of the cross section can be placed twice as far from the middle. This allows a wall, for example, to be constructed easily by saying that the square cross section should have the left and right sides 0.05 metres away from the middle and the bottom should be 0 metres from the middle and the top 2.4 metres from the middle. Then by repeating four times move forward by 10 metres, turn right 90 degrees you will get a wall around a 10m x 10m square.

The interface is designed to make it simple to do things that people are likely to want. If you want to add a texture to that wall, then you can use the add_texture function and give it a filename and that image will be on the wall, if you want a particular colour then a tuple of RGBA colour values can be used instead.

## Getting Started

Assuming you already have Blender installed, simply copy the files from blogo/src/ into <blender_install_dir>/scripts/ and restart Blender.  Now it is installed and can be used.  Check the quickstart in the help for more details and what to do to make shapes.

