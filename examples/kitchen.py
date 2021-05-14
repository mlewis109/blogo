from blogo import *

take_pictures = False
take_3d_pictures = False

base_config = {
    "hide_fourth_wall": False,
    "show_ceiling": False,
    "individual_lights": False,
    "draw_blinds": False,
    "door_angle": 0,
    "peninsula_angle": 0,
    "fridge_beside_oven": True,
    "peninsula_end_type": "square",
    "peninsula_width": 0.45,
    #"peninsula_circle_diameter": 0.75,
    "peninsula_circle_diameter": 0.6,
    "door_space": 0.15,
    "sink_cupboards": (0.6, 0.45, 0.3),
    "doorPos1": (2.2, 0.76),
    "doorPos2": (1.25, 0.76),
    "flip_door1": False,
    "flip_door2": False,
    "door_height": 2,
    "ceiling_height": 2.3,
    "window_width": 1.75,
    "room_width": 0.3+0.6+0.5+0.8+0.5+0.6,
    "room_length": 6.0,
    "fudge_bk": 0,
    "peninsula_cupboards": (0.6, 0.6),
    "oven_cupboards_with_fridge": ((0.6, 0, 2.3), (0.6, 0, 2.3), (0.45, 3), (0.6, 2), 0.45),
    "oven_cupboards": ((0.3, 0, 2.3), (0.6, 0, 2.3), (0.5, 3), (0.8, 2), 0.5),
    "oven_wall_cupboards_with_fridge": (0.45, (0.6, 0.35, 0.45), 0.45, 0.45),
    "oven_wall_cupboards": (0.6, (0.6, 0.35, 0.45), 0.6, 0.3),
    "door_fridge_gap": 0.3,
    "round_fridge_shelf": False,
    "table_pos": (4.3, 1.9),
    "table_width": 0.80,
    "table_length": 1.30,
    "table_height": 0.75,
    "table_angle": 0,
    "peninsula_side": "lane",
    "put_wall_back_for_some_reason": False,
    "fridge_wall_cupboards": [],
    "dining_room_cupboards": (0.6, 0.6),
    "dining_wall_cupboards": [],
    "stagger_pen_cupboards": False,
    "table_shape": "rectangle",
    "stud_round_fridge": False,
    "more_space_round_back_door": "line",
    "more_space_round_back_door_gap": False,
    # x, y, w, d, h, heading
    "sideboards": [(6, 0.47, 1.1, 0.47, 0.85, 180),
                   (6-0.03, 0.39, 1.04, 0.39, 1.85, 180),
                   (6-1.1, 0.42, 1.48, 0.42, 0.75, 180),
    ],
}
configs = []
#sink_cupboards = (0.6, 0.6)

baseDir = "textures\\"
floorTex = baseDir + "floortiles.png"
worktopTex = baseDir + "worktop.png"
cupboardTex = "ivory"
wallTex = (80/255, 0, 0)#"maroon"
#fridgeTex = "slategrey"
fridgeTex = baseDir + "brushed_metal.png"
doorTex = baseDir + "wood.png"
white_cloth_tex = baseDir + "white_cloth.png"
diningWallTex = "palegoldenrod"

BlogoUtils.start_fresh()
if (not base_config["individual_lights"]):
    BlogoUtils.add_light_area()

def lights(config):
    origin = Blogo.get_global_origin()
    ceiling_height = config["ceiling_height"]
    width = config["room_width"]
    length = 6
    num_lights_x = 3
    num_lights_y = 5
    x_spacing = width / (num_lights_x)
    y_spacing = length / (num_lights_y)
    x_start = x_spacing / 2
    y_start = y_spacing / 2
    if (y_start < 0.7):
        y_start = 0.7
    for x in range(num_lights_x):
        for y in range(num_lights_y):
            location = (origin[1] + y*y_spacing + y_start,
                        origin[0] + x*x_spacing + x_start,
                        origin[2] + ceiling_height)
            BlogoUtils.add_light_bulb(location=location, energy=100, angle=70)

def blinds(config):
    bottom_window = 1.1
    turtle = Blogo("blinds")
    turtle.set_texture("lemonchiffon")
    turtle.set_xyz(0, config["room_width"], bottom_window)
    turtle.rt(90)
    turtle.set_width("above", 2*(config["door_height"] - bottom_window))
    turtle.set_width("below", 0)
    turtle.set_width("sides", 0.1)
    turtle.fd(config["window_width"])
    
def window_nook(config):
    bottom_window = 1.1
    turtle = Blogo("window_nook")
    turtle.set_texture(worktopTex)
    turtle.set_smart_project(True)
    turtle.set_xyz(0, config["room_width"], bottom_window)
    turtle.rt(90)
    turtle.set_width("above", 0)
    turtle.set_width("below", 0.0125*2)
    turtle.set_width("left", 0.15*2)
    turtle.set_width("right", 0)
    turtle.fd(config["window_width"])
    turtle.up(90)
    turtle.set_texture(wallTex)
    turtle.fd(config["door_height"] - bottom_window)
    turtle.up(90)
    turtle.set_texture(diningWallTex)
    turtle.fd(config["window_width"])
    turtle.up(90)
    turtle.set_texture(wallTex)
    turtle.fd(config["door_height"] - bottom_window)

def area(config, turtle, hide_doors, texture_kitchen=None, texture_dining=None):
    if (texture_kitchen != None):
        turtle.set_texture(texture_kitchen)
    window_width = config["window_width"]
    turtle.fd(config["room_width"])
    turtle.rt(90)
    if (hide_doors):
        turtle.set_width("below", -2*config["door_height"])
    turtle.fd(window_width)
    if (hide_doors):
        turtle.set_width("below", 0)
        ceiling_height = turtle.get_width("above")
        turtle.set_width("above", 2*1.1)
    turtle.rt(180)
    turtle.fd(window_width)
    turtle.rt(180)
    turtle.fd(window_width)
    if (hide_doors):
        turtle.set_width("below", 0)
        turtle.set_width("above", ceiling_height)
    extra = 0.35
    turtle.fd(extra)
    if (texture_dining != None):
        turtle.set_texture(texture_dining)
    turtle.fd(config["doorPos1"][0]-window_width-extra)
    if (hide_doors):
        turtle.set_width("below", -2*config["door_height"])
    turtle.fd(config["doorPos1"][1])
    if (hide_doors):
        turtle.set_width("below", 0)
    turtle.fd(config["room_length"] - config["doorPos1"][0] - config["doorPos1"][1])
    turtle.rt(90)
    if (hide_doors and config["hide_fourth_wall"]):
        turtle.pu()
    turtle.fd(0.7)
    turtle.lt(90)
    turtle.fd(2)
    turtle.rt(90)
    turtle.fd(config["room_width"] - 0.7 - 0.9)
    turtle.rt(90)
    turtle.fd(2)
    turtle.lt(90)
    turtle.fd(0.9)
    turtle.rt(90)
    
    fridgePos = config["doorPos2"][0] + config["doorPos2"][1]-0.02 + 0.6 + config["door_fridge_gap"]
    doorPos = config["doorPos2"][0] + config["doorPos2"][1]
    turtle.fd(config["room_length"] - fridgePos)
    if (config["put_wall_back_for_some_reason"]):
        turtle.rt(90)
        peninsula_length = config["door_space"] + 0.6
        for cb in config["peninsula_cupboards"]:
            peninsula_length += cb
        turtle.fd(peninsula_length)
        turtle.rt(180)
        turtle.fd(peninsula_length)
        turtle.rt(90)
    turtle.fd(fridgePos - doorPos)
    if (hide_doors):
        turtle.set_width("below", -2*config["door_height"])
    turtle.fd(config["doorPos2"][1])
    if (hide_doors):
        turtle.set_width("below", 0)
    turtle.fd(config["doorPos2"][0])

def floor(config):
    turtle = Blogo("floor")
    turtle.set_width("all", 0)
    turtle.set_texture(floorTex)
    turtle.fill(0, 1, floorTex)
    turtle.set_fill_texture_scale(7)
    area(config, turtle, False)
    
def ceiling(config):
    turtle = Blogo("floor")
    turtle.set_z(config["ceiling_height"])
    turtle.set_width("all", 0)
    turtle.set_texture((1,1,1,1))
    turtle.fill(0, 1, (1,1,1,1))
    
    area(config, turtle, False)
    
def walls(config):
    turtle = Blogo("walls")
    turtle.set_width("left", 0.01)
    turtle.set_width("right", 0)
    turtle.set_width("below", 0)
    turtle.set_width("above", 2*2.4)
    turtle.set_texture(wallTex)
    area(config, turtle, True, wallTex, diningWallTex)
    return turtle.get_objects()

def sink_hole(config, turtle):
    #turtle.rectangle(0.4, 0.5)
    #turtle.fd(0.4)
    #turtle.rt(90)
    turtle.fd(0.45)
    turtle.rt(90)
    turtle.fd(0.38)
    turtle.rt(90)
    turtle.fd(0.15)
    turtle.lt(90)
    turtle.fd(0.17)
    turtle.rt(90)
    turtle.fd(0.30)
    turtle.rt(90)
    turtle.fd(0.38 + 0.17)
    turtle.rt(90)

def worktop(config):
    turtle = Blogo("worktop")
    turtle.set_z(0.9)
    turtle.set_x(0.6)
    turtle.set_height("below", 0.0125)
    turtle.set_height("above", 0)
    turtle.set_width("left", 0)
    turtle.set_width("right", 0)
    turtle.set_texture(worktopTex)
    turtle.fill(0, 1, worktopTex)
    for cb in config["oven_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            cb = (cb, 0, 0.9)
        if (len(cb) < 3):
            cb += (0.9,)
        if (cb[1] > 0.9):
            turtle.pen_up()
        turtle.fd(cb[0])
        if (cb[1] > 0.9):
            turtle.pen_down()
    # larder
    #turtle.fd(0.30)
    # oven
    #turtle.fd(0.60)
    #turtle.pen_down()
    # space
    #turtle.fd(0.60)
    # hob
    #turtle.fd(0.60)
    # space
    #turtle.fd(0.60)
    turtle.rt(90)
    # sink
    #turtle.fd(0.60)
    turtle.fd(0.025)
    turtle.lt(90)
    turtle.fd(0.05)
    sink_hole(config, turtle)
    turtle.lt(180)
    turtle.fd(0.05)
    turtle.lt(90)
    turtle.fd(0.575)
    #space
    sink_space = 0
    for w in config["sink_cupboards"]:
        sink_space += w
    turtle.fd(sink_space - 0.6)
    if (config["peninsula_side"] == "lane"):
        if (config["more_space_round_back_door"]):
            turtle.bk(0.3)
        turtle.rt(90)
        if (config["more_space_round_back_door"]):
            turtle.fd(0.3)
    elif (type(config["peninsula_side"]) == tuple):
        old_turtle = turtle
        turtle = Blogo("peninsula")
        
        turtle.set_height("below", 0.0125)
        turtle.set_height("above", 0)
        turtle.set_width("left", 0)
        turtle.set_width("right", 0)
        turtle.set_texture(worktopTex)
        turtle.fill(0, 1, worktopTex)
        turtle.pu()
        turtle.set_z(0.9)
        turtle.set_x(config["peninsula_side"][0])
        turtle.set_y(config["peninsula_side"][1])
        pen_start_pos = turtle.get_pos()
        turtle.pd()
    else:
        old_turtle = turtle
        turtle = Blogo("peninsula")
        
        turtle.set_height("below", 0.0125)
        turtle.set_height("above", 0)
        turtle.set_width("left", 0)
        turtle.set_width("right", 0)
        turtle.set_texture(worktopTex)
        turtle.fill(0, 1, worktopTex)
        turtle.pu()
        turtle.set_z(0.9)
        turtle.set_x(config["doorPos2"][0] + config["doorPos2"][1]-0.02 + config["peninsula_width"] + config["door_fridge_gap"])
        if (config["fridge_beside_oven"]):
            turtle.set_y(0)
        else:
            turtle.set_y(config["door_space"] + 0.6)
        pen_start_pos = turtle.get_pos()
        turtle.pd()
    
    turtle.lt(config["peninsula_angle"])
    # peninsula
    for cb in config["peninsula_cupboards"]:
        turtle.fd(cb)
    # peninsula end
    peninsula_end_type = config["peninsula_end_type"]
    peninsula_width = config["peninsula_width"]
    if (peninsula_end_type == "square"):
        turtle.lt(90)
        turtle.fd(peninsula_width)
        turtle.lt(90)
    elif (peninsula_end_type == "rounded"):
        turtle.arc(-180, peninsula_width/2)
    elif (peninsula_end_type == "rounded-flattened"):
        turtle.arc(-90, peninsula_width/4)
        turtle.fd(peninsula_width/2)
        turtle.arc(-90, peninsula_width/4)
    elif (peninsula_end_type == "rounded-squashed"):
        turtle.ellipse(-peninsula_width/2, peninsula_width/4, 180)
    elif (peninsula_end_type == "circle"):
        turtle.arc(-270, max(peninsula_width/2, 0.45))
        turtle.right(90)
        turtle.set_x(0.6+sink_space+peninsula_width)
        turtle.fd(0)
    elif (peninsula_end_type == "circle-middle"):
        w = peninsula_width / 2

        big_r = config["peninsula_circle_diameter"]/2
        t = math.degrees(math.asin(w / big_r))
        turtle.bk(2*math.sqrt(big_r*big_r - w*w))
    
        turtle.rt(90 - t)
        turtle.arc(2*t - 360, big_r)
        turtle.rt(90 - t)
        #turtle.right(22)
        #turtle.arc(-270, max(peninsula_width, 0.45))
        #turtle.left(22)
        turtle.right(90)
    elif (peninsula_end_type == "tear"):
        big_r = config["peninsula_circle_diameter"]/2
        turtle.arc(-225, big_r)
        little_r = (big_r * (1 + sin(radians(45))) - peninsula_width) / (1 - cos(radians(45)))
        
        turtle.arc(45, little_r)
    elif (peninsula_end_type == "bulb"):
        #turtle.bk(0.75)
        #turtle.arc(45, 0.25)
        #turtle.arc(-270, 0.8/2)
        #turtle.arc(45, 0.25)
        
        
        w = peninsula_width / 2

        big_r = config["peninsula_circle_diameter"]/2
        little_r = (w - big_r * sin(radians(45))) / (sin(radians(45)) - 1)
        big_h = big_r * sin(radians(45))
        little_h = little_r * sin(radians(45))
        
        t = math.degrees(asin(w / big_r))
        a = math.sqrt(4 * (big_r+w) * (big_r-w))
        bk = a / 2 + math.sqrt(big_r**2 - big_h**2) + math.sqrt(little_r**2 - little_h**2)
        #turtle.bk(2*math.sqrt(big_r*big_r - w*w))
        turtle.bk(bk - config["fudge_bk"])
    
        #turtle.rt(90 - t)
        turtle.arc(45, little_r)
        turtle.arc(-270, big_r)
        turtle.arc(45, little_r)
        #turtle.rt(90 - t)
    #turtle.set_pos((config["room_width"]-0.6, -(0.6+sink_space+peninsula_width), 0.9))
    if (config["stagger_pen_cupboards"]):
        turtle.fd(config["peninsula_cupboards"][-1])
        peninsula_width = 0.45
    if (config["peninsula_side"] == "lane"):
        if (config["more_space_round_back_door"]):
            if (config["more_space_round_back_door"] == 'ellipse'):
                turtle.set_pos((0.6+sink_space+peninsula_width-0.3, config["room_width"]-0.6-0.3, 0.9))
                turtle.fd(0)
                
                turtle.lt(90)
                turtle.ellipse(0.6, 0.3, 90)
                #turtle.bk(1)
                turtle.lt(90)
            elif (config["more_space_round_back_door"] == 'cubic'):
                start_x, start_y, start_z = (0.6+sink_space+peninsula_width-0.3, config["room_width"]-0.6-0.3, 0.9)
                end_x, end_y, end_z = (0.6+sink_space+peninsula_width-0.6, config["room_width"]-0.45, 0.9)
                turtle.set_pos((start_x, start_y, start_z))
                turtle.fd(0)
                def f(x):
                    return 0.5 * (x ** 3) + 5*x
                max_x = 100
                max_y = f(max_x/50)
                for x in range(-max_x, max_x):
                    xdiff = x / 50.0
                    ydiff = ((f(xdiff) / max_y) + 1) / 2
                    xdiff = (x + max_x) / (2 * max_x)
                    turtle.set_pos((start_x+xdiff*(end_x-start_x),
                                    start_y+ydiff*(end_y-start_y),
                                    end_z))
                    turtle.fd(0)
                    
                turtle.lt(90)
            elif (config["more_space_round_back_door"] == 'bezier'):
                turtle.set_pos((0.6+sink_space+peninsula_width-0.3, config["room_width"]-0.6-0.3, 0.9))
                turtle.fd(0)
                turtle.curve_to((0.6+sink_space+peninsula_width-0.6, config["room_width"]-0.45, 0.9), (0, 1.0, 0), 10, 10)
                
                turtle.lt(90)
            else:
                turtle.set_pos((0.6+sink_space+peninsula_width-0.3, config["room_width"]-0.6-0.3, 0.9))
                turtle.fd(0)
                turtle.set_pos((0.6+sink_space+peninsula_width-0.6, config["room_width"]-0.5, 0.9))
                turtle.fd(0)
        else:
            turtle.set_pos((0.6+sink_space+peninsula_width, config["room_width"]-0.6, 0.9))
            turtle.fd(0)
    else:
        if (type(config["peninsula_side"]) == tuple):
            length = 0
            for cb in config["peninsula_cupboards"]:
                length += cb
            #turtle.set_x(config["peninsula_side"][0])
            #turtle.set_y(config["peninsula_side"][1])
            for cb in config["peninsula_cupboards"]:
                turtle.fd(cb)
        else:
            turtle.set_x(config["doorPos2"][0] + config["doorPos2"][1]-0.02 + config["door_fridge_gap"])
            if (config["fridge_beside_oven"]):
                turtle.set_y(0)
            else:
                turtle.set_y(config["door_space"] + 0.6)
        turtle.fd(0)
        turtle.set_pos(pen_start_pos)
        turtle.fd(0)
        turtle = old_turtle
        
    # peninsula angle
    #turtle.set_pos((config["room_width"], -1.95, 0.9))
    end_cupboard_pos = 0.6
    for cb in config["sink_cupboards"]:
        end_cupboard_pos += cb
    turtle.set_pos((end_cupboard_pos, config["room_width"], 0.9))
    #turtle.set_heading_towards((config["room_width"], 0, 0.9))
    turtle.set_heading_towards((0, config["room_width"], 0.9))
    
    # window
    turtle.fd(end_cupboard_pos)
    turtle.lt(90)
    
    # oven wall
    turtle.fd(0.60)
    turtle.fd(0.60)
    turtle.fd(0.60)
    turtle.fd(0.60)
    
def cupboard(config, turtle, width, depth=0.6, height=0.89, sideTex=(0.5,0.5,0.5,1), topTex=None):
    prev_texture = turtle.get_texture()
    #turtle.set_z(0)
    topMod = 0
    if (topTex != None):
        topMod = 0.02
    start_pos = turtle.get_pos()
    turtle.set_width("right", 0)
    turtle.set_width("left", 2*depth)
    turtle.set_width("above", 2*height - topMod)
    turtle.set_width("below", 0)
    if (sideTex != None):
        turtle.set_texture(sideTex)
    turtle.fd(0.01)
    turtle.set_texture(prev_texture)
    turtle.fd(width-0.02)
    if (topTex != None):
        turtle.set_texture(topTex)
        turtle.pu()
        turtle.set_z(start_pos[2] + height)
        turtle.bk(width-0.01)
        turtle.set_width("above", topMod)
        turtle.pd()
        turtle.fd(width)
        turtle.set_width("above", 2*height - topMod)
        turtle.set_texture(prev_texture)
        turtle.pu()
        turtle.bk(0.01)
        turtle.pd()
    if (sideTex != None):
        turtle.set_texture(sideTex)
    turtle.set_z(start_pos[2])
    turtle.fd(0.01)
    turtle.set_texture(prev_texture)
    
def drawer_cupboard(config, turtle, width, num_drawers, height=0.89, depth=0.6):
    drawer_height = (height / num_drawers)
    last_drawer = False
    topTex=(0.5,0.5,0.5,1)
    for i in range(num_drawers):
        if (i == (num_drawers-1)):
            last_drawer = True
            topTex = None
        turtle.set_z(i * drawer_height)
        if (last_drawer):
            drawer_height -= 0.02
        cupboard(config, turtle, width, depth=depth, height=drawer_height, topTex=topTex)
        if (not last_drawer):
            turtle.pu()
            turtle.bk(width)
            turtle.pd()
    turtle.set_z(0)
    
def cupboards(config):
    turtle = Blogo("cupboards")
    turtle.set_texture(cupboardTex)
    turtle.set_x(0.60)
    first = True
    for cb in config["oven_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            cb = (cb, 0, 0.89)
        if (len(cb) < 3):
            cb += (0.9,)
        if (cb[1] > 0):
            drawer_cupboard(config, turtle, cb[0], cb[1], height=cb[2])
        else:
            cupboard(config, turtle, cb[0], height=cb[2])
        
    #cupboard(config, turtle, 0.30, height=2)
    #cupboard(config, turtle, 0.60, height=2)
    
    #drawer_cupboard(config, turtle, 0.50, 3)
    #drawer_cupboard(config, turtle, 0.80, 2)
    #cupboard(config, turtle, 0.50)
    turtle.rt(90)
    for w in config["sink_cupboards"]:
        cupboard(config, turtle, w)
    turtle.pu()

    if (config["peninsula_side"] == "lane"):
        if(config["more_space_round_back_door"]):
            turtle.pu()
            turtle.bk(0.3)
            turtle.pd()
        turtle.rt(90)
        if(config["more_space_round_back_door"]):
            if (config["more_space_round_back_door_gap"]):
                turtle.pu()
                turtle.fd(0.3)
                turtle.pd()
            else:
                cupboard(config, turtle, 0.3, 0.3)
    elif (type(config["peninsula_side"]) == tuple):
        turtle.set_x(config["peninsula_side"][0])
        turtle.set_y(config["peninsula_side"][1])
        turtle.lt(90)
    else:
        turtle.set_x(config["doorPos2"][0] + config["doorPos2"][1]-0.02 + config["peninsula_width"] + config["door_fridge_gap"])
        if (config["fridge_beside_oven"]):
            turtle.set_y(0)
        else:
            turtle.set_y(config["door_space"] + 0.6)
        turtle.lt(90)
    turtle.pd()
    depth = 0.6
    if (config["peninsula_width"] < 0.6):
        depth = 0.3
    elif (config["peninsula_width"] >= 1.2):
        depth = 1.2
    first = True
    turtle.lt(config["peninsula_angle"])
    for cb in config["peninsula_cupboards"]:
        this_depth = depth
        if (first and config["stagger_pen_cupboards"]):
            first = False
            this_depth = 0.3
        if (cb < 0):
            drawer_cupboard(config, turtle, -cb, 3, depth=this_depth)
        else:
            cupboard(config, turtle, cb, depth=this_depth)

def fridge(config):
    turtle = Blogo("fridge")
    turtle.set_texture(fridgeTex)
    turtle.set_heading(0)
    if (not config["fridge_beside_oven"]):
        turtle.set_x(config["doorPos2"][0] + config["doorPos2"][1]-0.02)
        turtle.set_y(config["door_space"])
        
        start_pos = turtle.get_pos()
        turtle.set_width("all", 0)
        
        if (config["round_fridge_shelf"] != None):
            turtle.fill(0.89, 0.9, worktopTex, "absolute")
            turtle.fd(config["door_fridge_gap"])
            turtle.lt(90)
            turtle.fd(0.6)
            if (config["round_fridge_shelf"]):
                turtle.lt(90)
                turtle.arc(-90, config["door_fridge_gap"])
            turtle.set_pos(start_pos)
            turtle.set_heading(0)
            turtle.fill_stop()
        turtle.pu()
        
        turtle.fd(config["door_fridge_gap"])
        turtle.pd()
    else:
        turtle.set_x(0.02)
    cupboard(config, turtle, 0.60, height=1.8, sideTex=None)
    if (not config["fridge_beside_oven"]):
        turtle.set_texture(cupboardTex)
        depth = 0.6
        if (config["stud_round_fridge"]) :
            depth = 0.75
            turtle.pu()
            turtle.set_y(0)
            turtle.pd()
        for cb in config["dining_room_cupboards"]:
            cupboard(config, turtle, cb, height=0.9, depth=depth, sideTex=None, topTex=worktopTex)

def wall_cupboards(config):
    height = 0.9
    gap = 2.3 - height - 0.9
    turtle = Blogo("wall_cupboards")
    turtle.set_texture(cupboardTex)
    turtle.pu()
    for cb in config["oven_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            break
        if (len(cb) < 3 or cb[2] != 2.3):
            break
        turtle.fd(cb[0])
    turtle.pd()
    
    for cb in config["oven_wall_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            cb = (cb, 0.9, 0.3)
        turtle.set_z(2.3-cb[1])
        turtle.set_x(cb[2])
        cupboard(config, turtle, cb[0], depth=cb[2], height=cb[1])
    turtle.pu()
    #turtle.rt(180)
    fridgePos = config["doorPos2"][0] + config["doorPos2"][1]-0.02 + 0.6 + config["door_fridge_gap"]
    fridge_wall_length = config["door_space"] + 0.6
    wall_cbs = []
    for cb in config["fridge_wall_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            cb = (cb, 0.9, 0.3)
        fridge_wall_length += cb[0]
        wall_cbs.append(cb)
    turtle.set_y(fridge_wall_length)
    turtle.rt(180)
    for cb in wall_cbs:
        turtle.pu()
        
        turtle.set_z(2.3-cb[1])
        turtle.set_x(fridgePos-cb[2])
        turtle.pd()
        cupboard(config, turtle, cb[0], depth=cb[2], height=cb[1])
        
    wall_cbs = []
    dining_wall_length = 0
    for cb in config["dining_wall_cupboards"]:
        if (not BlogoUtils.is_sequence(cb)):
            cb = (cb, 0.9, 0.3)
        dining_wall_length += cb[0]
        wall_cbs.append(cb)
    turtle.set_x(fridgePos + dining_wall_length)
    turtle.rt(0)
    for cb in wall_cbs:
        turtle.pu()
        
        turtle.set_z(2.3-cb[1])
        turtle.set_y(cb[2] + config["door_space"])
        turtle.pd()
        cupboard(config, turtle, cb[0], depth=cb[2], height=cb[1])
    if (config["stud_round_fridge"]):
        turtle.pu()
        turtle.set_texture(diningWallTex)
        turtle.set_x(fridgePos)
        turtle.set_y(0)
        turtle.set_z(0)
        turtle.set_width("sides", 0.05)
        turtle.set_width("below", 0)
        turtle.set_width("above", 2*config["ceiling_height"])
        turtle.set_heading(90)
        turtle.rt(90)
        turtle.fd(0.05)
        turtle.lt(90)
        turtle.pd()
        turtle.fd(0.65 + config["door_space"])
        turtle.lt(90)
        turtle.fd(0.65)
        
        turtle.pu()
        turtle.set_heading(90)
        start_pos = turtle.get_pos()
        turtle.set_x(fridgePos)
        turtle.set_y(0)
        turtle.set_z(0)
        turtle.set_width("left", 0)
        turtle.set_width("right", 2*0.3)
        turtle.set_width("above", 2*0.7)
        turtle.set_width("below", 0)
        
        turtle.set_z(2.3 - 0.9)
        turtle.set_texture(cupboardTex)
        turtle.pd()
        turtle.fd(config["door_space"])
        turtle.fd(0.65)
        pos = turtle.get_pos()
        turtle.set_width("left", 0)
        turtle.set_width("right", 2*0.3)
        turtle.set_width("above", 0.05)
        turtle.set_width("below", 0)
        for i in range(90):
            turtle.lt(1)
            turtle.fd(0)
        turtle.pu()
        turtle.set_pos(pos)
        turtle.rt(90)
        turtle.set_z(2.3 - 0.3)
        turtle.pd()
        for i in range(90):
            turtle.lt(1)
            turtle.fd(0)
        turtle.pu()
        turtle.set_z(2.3 - 0.9)
        turtle.set_width("left", 0)
        turtle.set_width("right", 2*0.3)
        turtle.set_width("above", 2*0.7)
        turtle.set_width("below", 0)
        turtle.pd()
        turtle.fd(0.65)
            
        turtle.pd()

def hob(config):
    turtle = Blogo("hob")
    turtle.set_z(0.9)
    turtle.set_x(0.6)
    turtle.set_height("below", 0)
    turtle.set_height("above", 2*0.0125)
    turtle.set_width("left", 0)
    turtle.set_width("right", 0)
    turtle.set_texture((0,0,0))
    turtle.fill(0, 1, (0,0,0))
    turtle.pen_up()
    # larder
    turtle.fd(0.30)
    if (config["fridge_beside_oven"]):
        turtle.fd(config["door_space"])
    # oven
    turtle.fd(0.60)
    # space
    turtle.fd(0.60)
    # hob
    turtle.lt(90)
    turtle.fd(0.05)
    turtle.pd()
    turtle.rectangle(0.50, 0.60)
    
def oven(config, pos, height):
    turtle = Blogo("oven")
    turtle.set_pos(pos)
    turtle.set_x(0.61)
    turtle.set_y(config["oven_cupboards"][0][0])
    turtle.set_height("below", 0.0125)
    turtle.set_height("above", 0.0125)
    turtle.set_width("left", 2*0.0125)
    turtle.set_width("right", 2*0.0125)
    turtle.set_texture((0,0,0))
    turtle.fill(0, 1, (0,0,0))
    turtle.pu()
    turtle.fd(0.025)
    turtle.pd()
    turtle.fd(0.55)
    turtle.up(90)
    turtle.fd(height)
    turtle.up(90)
    turtle.fd(0.55)
    turtle.up(90)
    turtle.fd(height)

def soil_pipe(config):
    depth = 0.2
    turtle = Blogo("soil_pipe")
    turtle.set_texture(cupboardTex)
    turtle.set_x(1.82)
    turtle.set_y(config["room_width"] - depth)
    turtle.rt(90)
    cupboard(config, turtle, 0.175, height=2.4, depth=depth, sideTex=None)
    
def door(config, start, width, angle, frame_only, flip):
    height = 2.0
    turtle = Blogo("door")
    
    
    turtle.set_width("all", 0.035)
    turtle.set_texture(doorTex)
        
    if (not frame_only):
        turtle.set_width("sides", 0.002)
        turtle.set_texture((0,0,0))
        turtle.fill(0, 1, doorTex)
    turtle.set_pos(start)
    turtle.rt(90)
    angle_dir = 1
    if (flip and not frame_only):
        turtle.pu()
        turtle.bk(width)
        turtle.rt(180)
        angle_dir = -1
        turtle.pd()
    turtle.rt(angle_dir * angle)
    turtle.anticlockwise(90)
    turtle.rectangle(width, height)
    if (angle % 180 != 0):
        angle = angle - angle%180 + 180
        door(config, start, width, angle, True, flip)

def table_leg(turtle, config, pos):
    tablePos = config["table_pos"]
    turtle.set_z(config["table_height"])

    table_rel_pos(config, turtle, pos[0], pos[1])
    
    turtle.pu()
    turtle.down(90)
    turtle.fd(0.02)
    turtle.pd()
    turtle.set_width("all", 0.08)
    turtle.fd(config["table_height"] - 0.02)
    turtle.pu()
    turtle.up(90)

def table_rel_pos(config, turtle, x, y):
    tablePos = config["table_pos"]
    
    turtle.pu()
    turtle.set_x(tablePos[0])
    turtle.set_y(tablePos[1])
    turtle.set_heading(config["table_angle"])
    turtle.bk(config["table_length"] / 2)
    turtle.lt(90)
    turtle.fd(config["table_width"] / 2)
    
    turtle.rt(90)
    turtle.fd(x)
    turtle.rt(90)
    turtle.fd(y)
    turtle.lt(90)
    turtle.pd()
    
def chair(config, x, y, angle):
    width = 0.40
    length = 0.47
    turtle = Blogo("chair")
    turtle.set_texture(white_cloth_tex)
    tablePos = config["table_pos"]
    
    turtle.set_width("below", 0)
    turtle.set_width("above", 0.64 * 2)
    turtle.set_width("sides", width)
    
    table_rel_pos(config, turtle, x, y)
    turtle.set_z(0.36)
    
    turtle.rt(angle)
    turtle.fd(0.07)
    turtle.set_width("above", 0.1 * 2)
    turtle.fd(length - 0.07)
    turtle.pu()
    
    turtle.set_texture(doorTex)
    turtle.set_width("all", 0.03)
    #turtle.down(90)
    turtle.set_z(0.36)
    table_rel_pos(config, turtle, x, y)
    turtle.rt(angle)
    turtle.pu()
    
    turtle.fd(0.02)
    turtle.rt(90)
    turtle.bk(width / 2)
    turtle.fd(0.02)
    legs = (width - 0.04, length - 0.04,
            width - 0.04, length - 0.04,
    )
    for dist in legs:
        turtle.down(90)
        turtle.pd()
        turtle.fd(0.36)
        turtle.pu()
        turtle.bk(0.36)
        turtle.up(90)
        turtle.fd(dist)
        turtle.lt(90)
        #turtle.set_xyz(x+x_rel, y+mul * y_rel, 0.36)
        #turtle.pd()
        #turtle.fd(0.36)
        #turtle.pu()
    
def pool_table(config):
    width = 1
    length = 1.8
    turtle = Blogo("table")
    turtle.set_texture("green")
    tablePos = config["table_pos"]
    
    turtle.set_z(config["table_height"] + 0.05)
    turtle.set_width("sides", width)
    turtle.set_width("sides", width)
    turtle.set_width("above", 0)
    turtle.set_width("below", 0.05)
    table_rel_pos(config, turtle, (config["table_length"] - length)/2, (config["table_width"] ) / 2)
    turtle.fd(length)
    turtle = Blogo("cue")
    turtle.set_width("all", 0.03)
    turtle.set_z(config["table_height"] + 0.1)
    turtle.set_texture("red")
    
    cue_length = 1.15
    table_rel_pos(config, turtle, (config["table_length"] - length)/2, (config["table_width"] - width) / 2)
    turtle.pu()
    turtle.rt(90)
    for dist in (width, length, width, length):
        turtle.fd(dist/2)
        turtle.rt(90)
        turtle.pd()
        turtle.fd(cue_length)
        turtle.pu()
        turtle.bk(cue_length)
        turtle.lt(90)
        turtle.fd(dist/2)
        turtle.rt(45)
        turtle.pd()
        v_angle = 10
        turtle.up(v_angle)
        turtle.fd(cue_length)
        turtle.pu()
        turtle.bk(cue_length)
        turtle.down(v_angle)
        turtle.lt(45)
        turtle.lt(90)
    
    
def table(config):
    turtle = Blogo("table")
    
    turtle.set_texture(doorTex)
    tablePos = config["table_pos"]
    table_rel_pos(config, turtle, 0, config["table_width"] / 2)

    turtle.set_z(config["table_height"])
    turtle.set_width("above", 0)
    turtle.set_width("below", 0.05)
    
    if (config["table_shape"] == "rectangle"):
        
        turtle.set_width("sides", config["table_width"])
        turtle.fd(config["table_length"])
        
        table_leg(turtle, config, (0.07, 0.07))
        table_leg(turtle, config, (0.07, config["table_width"] - 0.07))
        table_leg(turtle, config, (config["table_length"] - 0.07, 0.07))
        table_leg(turtle, config, (config["table_length"] - 0.07, config["table_width"] - 0.07))
        chair(config, 0.4,  - 0.15, 90)
        chair(config, 0.4, 0.15 + config["table_width"] , -90)
        chair(config, config["table_length"] - 0.4, 0.15 + config["table_width"], -90)
        chair(config, config["table_length"] - 0.4, - 0.15, 90)
    elif (config["table_shape"] == "circle"):
        turtle.pu()
        turtle.fd(config["table_width"]/2)
        turtle.lt(90)
        turtle.set_width("sides", 0.01)
        turtle.fill(0, 1, doorTex)
        turtle.pd()
        turtle.circle(config["table_width"]/2)
        chair(config, 1*config["table_width"]-config["table_width"]/2-0.2, config["table_width"]*0.5, 0)
        chair(config, 1*config["table_width"], config["table_width"]*0.5-config["table_width"]/2-0.2, 90)
        chair(config, 1*config["table_width"]+config["table_width"]/2+0.2, config["table_width"]*0.5, 180)
        chair(config, 1*config["table_width"], config["table_width"]*0.5+config["table_width"]/2+0.2, 270)
        
            
    
def sideboard(config):
    sideboards = config["sideboards"]
    turtle = Blogo("sideboard")
    turtle.set_texture(doorTex)
    for x, y, w, d, h, heading in sideboards:
        turtle.pu()
        turtle.set_heading(heading)
        turtle.set_xy(x, y)
        turtle.pd()
        cupboard(config, turtle, w, d, h, doorTex, doorTex)

def kitchen(config):
    if (config["individual_lights"]):
        lights(config)
    floor(config)
    if (config["show_ceiling"]):
        ceiling(config)
    walls(config)
    if (config["draw_blinds"]):
        blinds(config)
    window_nook(config)
    worktop(config)
    hob(config)
    cupboards(config)
    wall_cupboards(config)
    fridge(config)
    oven(config, (0.45, -0.6, 0.9-0.25), 0.5)
    oven(config, (0.45, -0.6, 0.9+0.25+0.05), 0.3)
    soil_pipe(config)
    door_angle = config["door_angle"]
    doorPos1 = config["doorPos1"]
    doorPos2 = config["doorPos2"]
    door(config, ((doorPos1[0]+doorPos1[1]),config["room_width"]), doorPos1[1], 180-door_angle, False, config["flip_door1"])
    if (config["hide_fourth_wall"]):
        door_angle = 0
    door(config, ((doorPos2[0]), 0), doorPos2[1], -door_angle, config["hide_fourth_wall"], config["flip_door2"])
    table(config)
    #pool_table(config)
    sideboard(config)

def add_config(**kwargs):
    global configs
    config = base_config.copy()
    for k in kwargs:
        config[k] = kwargs[k]
    if (config["fridge_beside_oven"]):
        config["oven_cupboards"] = config["oven_cupboards_with_fridge"]
        config["oven_wall_cupboards"] = config["oven_wall_cupboards_with_fridge"]
    configs.append(config)
        
def make_photo_sphere(file, cam_loc, pic_loc):
    cam = BlogoUtils.add_camera("Cam", cam_loc, [pic_loc], angle=90)
    
    bpy.context.scene.render.engine = 'CYCLES'

    bpy.context.scene.render.resolution_x = 2000
    bpy.context.scene.render.resolution_y = 1000
    cam.data.type = 'PANO'
    cam.data.cycles.panorama_type = 'EQUIRECTANGULAR'
    bpy.context.scene.camera = cam
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = file
    bpy.ops.render.render(use_viewport = True, write_still=True)
    
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.data.objects.remove(cam, do_unlink=True)
def main():
    
    narrow_middle = (0.60, 0.60)
    current_middle = (0.60, 0.60, 0.30)
    wider_pen = 0.60
    double_pen = 1.20
    
    table_middle = (4.3, 1.9)
    table_away = (4.7, 2.65)
    table_away_angle = 90
    island_length = 1.2
    
    doorPos =  base_config["doorPos2"][0] + base_config["doorPos2"][1]
    roomWidth = base_config["room_width"]
    
    living_room_peninsula = (doorPos + 0.3 + 1.2, 0)
    Lpeninsula_door_fridge_gap = 0.05
    Lpeninsula_peninsula = (doorPos + Lpeninsula_door_fridge_gap + 1.2, 0)
    island_peninsula = (0.6 + 0.9 + island_length, roomWidth - 0.6 - 0.9)
    
    long_peninsula = (0.6, 0.6, 0.6)
    longer_peninsula = (0.75, 0.6, 0.6)
    
    sideboards_current = [(6, 0.47, 1.1, 0.47, 0.85, 180),
                          (6-0.03, 0.39, 1.04, 0.39, 1.85, 180),
    ]
    sideboards_additional = sideboards_current + [(6-1.1, 0.42, 1.48, 0.42, 0.75, 180)]
    #for end_type in ("square", "rounded", "tear", "bulb", "circle", "circle-middle"):
    #for end_type in ("square", "rounded", "rounded-squashed", "rounded-flattened"):
    #    add_config(peninsula_end_type=end_type, flip_door1=True)
    #    
    #    add_config(peninsula_end_type=end_type, sink_cupboards=narrow_middle, peninsula_width=wider_pen, fudge_bk=0.17)
    #    if (end_type == "square"):
    #        add_config(peninsula_end_type=end_type, sink_cupboards=narrow_middle, peninsula_width=wider_pen, fudge_bk=0.17, round_fridge_shelf=True)
    #add_config(sink_cupboards=narrow_middle, peninsula_width=wider_pen, round_fridge_shelf=True)
    
    show = []
    #show.append("peninsula_lane_side_pool")
    #show.append("peninsula_lane_side")
    #show.append("peninsula_lane_side_more_space")
    #show.append("peninsula_lane_side_fridge_out")
    #show.append("peninsula_other_side")
    #show.append("peninsula_other_side_with_wall")
    #show.append("baking_station_pool")
    #show.append("baking_station")
    #show.append("baking_station_fridge_out")
    #show.append("island")
    show.append("Lpeninsula")
    #show = []
    #show.append("baking_station_studded")
    if ("peninsula_lane_side_pool" in show):
        add_config(sink_cupboards=narrow_middle, peninsula_width=wider_pen, round_fridge_shelf=True,
                   table_pos=table_middle)
    if ("peninsula_lane_side" in show):
        add_config(sink_cupboards=narrow_middle, peninsula_width=wider_pen, round_fridge_shelf=True,
                   table_pos=table_away, table_angle=table_away_angle, peninsula_end_type="rounded")
    if ("peninsula_lane_side_more_space" in show):
        curve = "line"
      #for curve in ("cubic", "ellipse", "bezier", "line"):
        add_config(sink_cupboards=current_middle, peninsula_width=wider_pen, round_fridge_shelf=True,
                   table_pos=table_away, table_angle=table_away_angle, peninsula_end_type="square",
                   more_space_round_back_door=curve)
    if ("peninsula_lane_side_fridge_out" in show):
        add_config(sink_cupboards=narrow_middle, peninsula_width=wider_pen, round_fridge_shelf=True,
                   table_pos=table_away, table_angle=table_away_angle, fridge_beside_oven=False)
    if ("peninsula_other_side_with_wall" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=wider_pen, round_fridge_shelf=None,\
                   peninsula_side="living_room", dining_room_cupboards=[], 
                   put_wall_back_for_some_reason=True, fridge_wall_cupboards=(0.6, 0.6))
    if ("peninsula_other_side" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=wider_pen, round_fridge_shelf=None,\
                   peninsula_side="living_room", dining_room_cupboards=[],
                   table_pos=table_away, table_angle=table_away_angle,
                   peninsula_cupboards=long_peninsula, sideboards=sideboards_current)
    if ("Lpeninsula" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=wider_pen, round_fridge_shelf=None,\
                   peninsula_side=Lpeninsula_peninsula, dining_room_cupboards=[],
                   table_angle=table_away_angle, door_space=0,
                   peninsula_cupboards=long_peninsula, sideboards=sideboards_current,
                   fridge_beside_oven=False, door_fridge_gap=Lpeninsula_door_fridge_gap,
                   table_pos=table_away)
    if ("Lpeninsula-circle-table" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=wider_pen, round_fridge_shelf=None,\
                   peninsula_side=Lpeninsula_peninsula, dining_room_cupboards=[],
                   table_angle=45, door_space=0,
                   peninsula_cupboards=long_peninsula, sideboards=sideboards_current,
                   fridge_beside_oven=False, door_fridge_gap=Lpeninsula_door_fridge_gap,
                   table_pos=(4.7, 2), table_shape="circle", table_width=1.1)
    if ("baking_station_pool" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=double_pen, round_fridge_shelf=None,\
                   peninsula_side=living_room_peninsula, peninsula_cupboards=[0.6, 0.6],
                   table_pos=(4.6, 1.75), table_angle=0)
    if ("baking_station" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=double_pen, round_fridge_shelf=None,\
                   peninsula_side=living_room_peninsula, peninsula_cupboards=[0.6, 0.6], dining_room_cupboards=[0.6],
                   table_pos=table_away, table_angle=table_away_angle, sideboards=sideboards_current)
    if ("baking_station_fridge_out" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=double_pen, round_fridge_shelf=None,\
                   peninsula_side=living_room_peninsula, peninsula_cupboards=[0.6, 0.6], dining_room_cupboards=[0.6],
                   table_pos=table_away, table_angle=table_away_angle, fridge_beside_oven=False)
    if ("baking_station_studded" in show):
        double_pen = 1.30
        add_config(sink_cupboards=current_middle, peninsula_width=double_pen, round_fridge_shelf=None,\
                   peninsula_side="living_room", peninsula_cupboards=[0.7], dining_room_cupboards=[0.7],
                   table_pos=table_away, table_angle=table_away_angle, stud_round_fridge=True)
                   
    if ("island" in show):
        add_config(sink_cupboards=current_middle, peninsula_width=0.6, round_fridge_shelf=None,\
                   peninsula_side=island_peninsula, peninsula_cupboards=[island_length], dining_room_cupboards=[0.6],
                   table_pos=table_away, table_angle=table_away_angle,
                   peninsula_angle=90) 
    
    width = int(math.sqrt(len(configs)))
    lemgth = int(math.sqrt(len(configs)))
    
    x = 0
    y = 0
    for c in configs:
        Blogo.set_global_origin(10*y,5*x,0)
        if (len(configs) == 1 and take_3d_pictures):
            c["show_ceiling"] = True
            c["individual_lights"] = True
        kitchen(c)
        
        x += 1
        if (x >= width):
            x = 0
            y += 1
    
    Blogo.clean_up()
    
    if (len(configs) == 1 and take_pictures):
        baseFile = "pictures/kitchen-"+show[0]
        BlogoUtils.take_picture(baseFile+"1.png", (1.75,1.75,4), [(0,0,0), (3.5,3.5,0)], angle=1.5, roll=-pi/2)
        BlogoUtils.take_picture(baseFile+"2.png", (5,3,2.5), [(0,0,0), (3.5,3.5,0)], angle=1.5)
        BlogoUtils.take_picture(baseFile+"3.png", (5,0.5,2.5), [(0,0,0), (3.5,3.5,0)], angle=1.5)
    if (len(configs) == 1 and take_3d_pictures):
        baseFile = "pictures/3d-kitchen-"+show[0]
        #make_photo_sphere(baseFile+"1.png", (1, 2, 1.6), (0, 2, 1.6))
        #make_photo_sphere(baseFile+"2.png", (2.6, 3.1, 1.6), (0, 2, 1.6))
        #make_photo_sphere(baseFile+"3.png", (1.6, 0.15, 1.6), (0, 2, 1.6))
        make_photo_sphere(baseFile+"4.png", (3.6, 1.8, 1.6), (0, 2, 1.6))
        #make_photo_sphere(baseFile+"5.png", (6, 2, 1.6), (0, 2, 1.6))
    
    BlogoUtils.unselect_objects()
    BlogoUtils.show_objects()

main()
