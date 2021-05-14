from blogo import *

import random
import os

BlogoUtils.start_fresh()
BlogoUtils.add_light_area()

subsection = 1

def cross_sections():
    if (subsection == 0):
        turtle.fd(0)
    elif (subsection == 1):
        turtle.fd(10)
    else:
        turtle.set_cross_section([(-0.01, 0.07), (-0.05, 0.07), (-0.05, 0.09), (0.05, 0.09), (0.05, 0.07), (0.01, 0.07),
                                  (0.01, -0.07), (0.05, -0.07), (0.05, -0.09), (-0.05, -0.09), (-0.05, -0.07), (-0.01, -0.07)])
        turtle.fd(10)
        turtle.rt(90)
        turtle.fd(10)

def pen_up_and_down():
    turtle.fd(2)
    turtle.pen_up()
    turtle.fd(2)
    turtle.pen_down()
    turtle.fd(2)
    turtle.pen_up()
    turtle.fd(2)
    turtle.pen_down()
    turtle.fd(2)

def the_third_dimension():
    turtle.fd(5)
    turtle.rt(90)
    turtle.fd(5)
    turtle.up(90)
    turtle.fd(5)
    turtle.down(90)
    turtle.fd(5)

def rotating():
    turtle.set_cross_section([(-0.01, 0.07), (-0.05, 0.07), (-0.05, 0.09), (0.05, 0.09), (0.05, 0.07), (0.01, 0.07),
                              (0.01, -0.07), (0.05, -0.07), (0.05, -0.09), (-0.05, -0.09), (-0.05, -0.07), (-0.01, -0.07)])
    turtle.fd(1)
    turtle.clockwise(22.5)
    turtle.fd(1)
    turtle.clockwise(22.5)
    turtle.fd(1)
    turtle.clockwise(22.5)
    turtle.fd(1)
    turtle.clockwise(22.5)
    turtle.fd(1)

def cross_section_adjustments():
    turtle.fd(5)
    turtle.pen_up()
    turtle.tilt_h(45)
    turtle.fd(2)
    turtle.pen_down()
    turtle.fd(5)
    turtle.pen_up()
    turtle.tilt_h(-45)
    turtle.tilt_v(45)
    turtle.fd(2)
    turtle.pen_down()
    turtle.fd(5)
    turtle.pen_up()
    turtle.tilt_v(-45)
    turtle.tilt_r(45)
    turtle.fd(2)
    turtle.pen_down()
    turtle.fd(5)

def sideways():
    turtle.fd(2)
    turtle.strafe(2)
    turtle.fd(2)
    turtle.pen_up()
    turtle.strafe_v(2)
    turtle.pen_down()
    turtle.fd(2)

def putting_together_turns():
    for angle in range(360):
        turtle.fd(0.1)
        turtle.rt(1)

def moving_around():
    for i in range(20):
        turtle.set_pos((random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)))
        turtle.fd(1)
    for i in range(20):
        turtle.pen_up()
        turtle.set_xyz(-random.uniform(0, 10), -random.uniform(0, 10), -random.uniform(0, 10))
        turtle.pen_down()
        turtle.fd(1)

def textures():
    turtle.fd(2)
    turtle.set_texture("red")
    turtle.fd(2)
    turtle.set_texture((0.25, 0.5, 1))
    turtle.fd(2)
    turtle.set_texture(os.path.abspath("./textures/grass.png"))
    turtle.fd(2)
    
def filling_areas():
    turtle.set_texture("red")
    turtle.fill(0.1, 0.2, "green", "relative")
    turtle.fill(0.5, 0.9, "blue", "relative")
    turtle.fd(10)
    turtle.rt(90)
    turtle.fd(10)

def expanding_the_cross_section():
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("left", 2)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("right", 2)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("above", 2)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("below", 2)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("sides", 3)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("verticals", 3)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)
    turtle.set_width("all", 4)
    turtle.set_texture((random.random(), random.random(), random.random()))
    turtle.fd(2)

def height_func(args):
    absolute_length_along = args["full_length"]
    return int(absolute_length_along) % 2
    
def width_func(args):
    relative_length_along = args["relative_length"]
    return (4 * sin(relative_length_along * pi), "*")
    
def expanding_the_cross_section_more():
    if (subsection == 0):
        turtle.add_width_func("above", height_func)
        turtle.add_width_func("sides", width_func)
        turtle.fd(20)
    elif (subsection == 1):
        turtle.set_length_incr(0.005)
        turtle.add_width_func("all", "curve_start", curve_length=0.1, eccentricity=0)
        turtle.add_width_func("all", "curve_end", curve_length=0.1)
        turtle.fd(10)

def adding_gaps():
    turtle.set_width("above", 3)
    turtle.set_width("below", 0)
    turtle.set_width("sides", 0.1)
    turtle.fd(3)
    turtle.set_length_incr(1, 1)
    
    turtle.add_gap("window", 1, 2)
    turtle.fd(4)
    turtle.remove_gap("window")
    
    turtle.fd(3)

turtle = Blogo()

cross_sections()
#pen_up_and_down()
#the_third_dimension()
#rotating()
#cross_section_adjustments()
#sideways()
#putting_together_turns()
#moving_around()
#textures()
#filling_areas()
#expanding_the_cross_section()
#expanding_the_cross_section_more()
#adding_gaps()

Blogo.clean_up()
BlogoUtils.unselect_objects()
BlogoUtils.show_objects()
