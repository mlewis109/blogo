import math

try:
    isLib = libRun
    libRun = False
except:
    isLib = False

if not isLib:
    from blogo import *

import random

if not isLib:
    baseDir = "textures\\"
    grassTex = baseDir + "grass.png"
    brownTex = baseDir + "brown.png"
    pinkTex = baseDir + "pink.png"
    cobblesTex = baseDir + "test.png"

    BlogoUtils.start_fresh()
    BlogoUtils.add_light_area()

def head_func(args):
    #curve_end_width = 0.5
    curve_end_width = args["curve_end_width_top"]
    #curve_start_length = 0.4
    curve_start_length = args["curve_start_length_top"]
    length_along = args["relative_length"]
    print("length along = "+str(length_along))
    global eighth
    if (length_along > 0.5):
        length_along = 1 - length_along
        curve_end_width = 0
        curve_end_width = args["curve_end_width_bottom"]
        curve_start_length = args["curve_start_length_bottom"]
    
    if (length_along > curve_start_length):
        width = 1
    else:
        #width = 0.4 - width
        length_along /= curve_start_length
        width = math.sqrt(1**2 - (1-length_along)**2)
        width = curve_end_width + (1 - curve_end_width) * width
    
        
    return (width, "*")

def draw_person(height, location=(0,0,0)):
    skin = (209/255, 163/255, 164/255)
    global eighth
    eighth = height / 8
    legs_apart = 0.2
    foot_length = 0.25
    leg_length = 4 * eighth
    turtle = Blogo("person")
    turtle.set_pos(location)
    turtle.rt(90)
    turtle.set_texture("black")
    turtle.set_cross_section("circle", 0.5)
    leg_width = 0.1
    turtle.set_width("all", leg_width)
    start_pos = turtle.get_turtle()
    turtle.pu()
    turtle.rt(90)
    turtle.fd(legs_apart)
    turtle.pd()
    turtle.lt(90)
    turtle.set_width("below", 0)
    turtle.add_width_func("all", head_func,
                          curve_end_width_top=1, curve_start_length_top=0.01, 
                          curve_end_width_bottom=0, curve_start_length_bottom=0.2)
    turtle.fd(foot_length)
    turtle.add_width_func("all")
    turtle.pu()
    turtle.bk(foot_length)
    turtle.pd()
    turtle.set_width("below", leg_width)
    turtle.set_texture("darkblue")
    turtle.up(90)
    turtle.lt(5)
    turtle.down(5)
    turtle.fd(2 * eighth)
    turtle.up(8)
    turtle.fd(2 * eighth)
    turtle.pu()
    turtle.set_turtle(start_pos)
    turtle.rt(-90)
    turtle.fd(legs_apart)
    turtle.pd()
    turtle.lt(-90)
    turtle.set_width("below", 0)
    turtle.set_texture("black")
    turtle.add_width_func("all", head_func, 
                          curve_end_width_top=1, curve_start_length_top=0.01, 
                          curve_end_width_bottom=0, curve_start_length_bottom=0.2)
    turtle.fd(foot_length)
    turtle.add_width_func("all")
    turtle.pu()
    turtle.bk(foot_length)
    turtle.pd()
    turtle.set_width("below", leg_width)
    turtle.set_texture("darkblue")
    turtle.up(90)
    turtle.rt(5)
    turtle.down(5)
    turtle.fd(2 * eighth)
    turtle.up(8)
    turtle.fd(2 * eighth)
    turtle.pu()
    turtle.set_turtle(start_pos)
    turtle.up(90)
    turtle.down(5)
    turtle.fd(2 * eighth)
    turtle.up(8)
    turtle.fd(2 * eighth)
    
    # torso
    turtle.set_texture("red")
    torso_width = 0.35
    torso_depth = 0.2
    turtle.set_width(("left","right"), torso_width)
    turtle.set_width(("above","below"), torso_depth)
    turtle.pd()
    turtle.add_width_func(("above", "below"), head_func,
                          curve_end_width_top=1, curve_start_length_top=0.01, 
                          curve_end_width_bottom=0.25, curve_start_length_bottom=0.2)
    
    turtle.fd(2.5 * eighth)
    turtle.add_width_func(("above", "below"))
    
    # neck
    turtle.set_texture(skin)
    neck_width = 0.08
    turtle.set_width("all", neck_width)
    turtle.fd(0.5 * eighth)
    
    # head
    #turtle.set_cross_section("circle", 0.002, 0.005)
    head_width = 0.14
    head_depth = 0.20
    turtle.set_width(("left","right"), head_width)
    turtle.set_width(("above","below"), head_depth)
    
    turtle.add_width_func("all", head_func, 
                          curve_end_width_top=0.5, curve_start_length_top=0.4,
                          curve_end_width_bottom=0, curve_start_length_bottom=0.4)
    turtle.fd(eighth)
    
    turtle.add_width_func("all")
    #turtle.add_width_func("left")
    #turtle.add_width_func("above")
    #turtle.add_width_func("below")
    
    turtle.pu()
    turtle.bk(1.5 * eighth)
    neck_pos = turtle.get_turtle()
    
    # arms
    arm_width = 0.08
    hand_width = 0.1
    hand_depth = 0.03
    turtle.rt(90)
    turtle.fd(torso_width / 2)
    turtle.rt(80)
    turtle.pd()
    turtle.set_width("all", arm_width)
    turtle.add_width_func("left", head_func,
                          curve_end_width_top=0, curve_start_length_top=0.4,
                          curve_end_width_bottom=1, curve_start_length_bottom=0.4)
    turtle.set_texture("red")
    turtle.down(5)
    turtle.fd(.5 * eighth)
    turtle.add_width_func("left")
    turtle.set_texture(skin)
    turtle.fd(eighth)
    turtle.down(5)
    turtle.fd(eighth)
    
    turtle.set_width(("left","right"), hand_width)
    turtle.set_width(("above","below"), hand_depth)
    turtle.add_width_func("all", head_func,
                          curve_end_width_top=0.8, curve_start_length_top=0.4, 
                          curve_end_width_bottom=0.2, curve_start_length_bottom=0.4)
    turtle.fd(eighth)
    turtle.add_width_func("all")
    
    turtle.pu()
    turtle.set_turtle(neck_pos)
    turtle.lt(90)
    turtle.fd(torso_width / 2)
    turtle.lt(80)
    turtle.pd()
    turtle.set_width("all", arm_width)
    turtle.set_texture("red")
    turtle.add_width_func("right", head_func,
                          curve_end_width_top=0, curve_start_length_top=0.4,
                          curve_end_width_bottom=1, curve_start_length_bottom=0.4)
    turtle.down(5)
    turtle.fd(.5 * eighth)
    turtle.add_width_func("right")
    turtle.set_texture(skin)
    turtle.fd(eighth)
    turtle.down(5)
    turtle.fd(eighth)
    
    turtle.set_width(("left","right"), hand_width)
    turtle.set_width(("above","below"), hand_depth)
    turtle.add_width_func("all", head_func,
                          curve_end_width_top=0.8, curve_start_length_top=0.4, 
                          curve_end_width_bottom=0.2, curve_start_length_bottom=0.4)
    turtle.fd(eighth)
    turtle.add_width_func("all")

if not isLib:
    draw_person(1.88)

    Blogo.clean_up()
    BlogoUtils.unselect_objects()
    BlogoUtils.show_objects()