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

def branch(turtle, leaves, detailed_tree, branch_length, tree_height, branch_depth, depth=0):
    length = branch_length / (depth+1)
    length *= 1.0 + random.uniform(-0.1, 0.1)
    
    cs_width = tree_height * 0.075 / (2 ** depth)
    turtle.set_width("all", cs_width)
    
    turtle.fd(length)
    
    position = turtle.get_turtle()
    
    num_branches = 2
    if (depth == 0):
        num_branches = 4
    elif (depth == 1):
        num_branches = 3
    elif (depth == branch_depth-2):
        num_branches = 3
    elif (depth >= branch_depth-1):
        num_branches = 4
        
    if (depth < branch_depth):
        for i in range(num_branches):
            turtle.pen_up()
            turtle.set_turtle(position)
            turtle.pen_down()
            draw_branch(turtle, detailed_tree, i, num_branches)
            branch(turtle, leaves, detailed_tree, branch_length, tree_height, branch_depth, depth+1)
    if ((detailed_tree and depth >= branch_depth-2) or (depth >= branch_depth-1)):
        leaves.append((length, position))
    return leaves
        

def draw_branch(turtle, detailed_tree, branch_num, total_branches):
    branch_width = 360 / total_branches
    
    start_angle = branch_num * branch_width
    end_angle = start_angle + branch_width / 2
    
    angle = random.randrange(start_angle, end_angle)
    if (detailed_tree):
        up = random.randrange(15, 50)
    else:
        up = random.randrange(5, 70)
    turtle.clockwise(angle)
    turtle.up(up)

def sphere_func(x, y, rx, ry, **kwargs):
    i = kwargs["map_to_use"]
    rx *= math.pi
    ry *= 2 * math.pi
    position = kwargs["position"].position
    radius = kwargs["radius"]
    #radius *= random.uniform(0.9, 1.1)
    radius *= 1.0 + radiusMap[i][x][y]
    xp = position[0] + radius * math.sin(rx) * math.cos(ry)
    yp = position[1] + radius * math.sin(rx) * math.sin(ry)
    zp = position[2] + radius * math.cos(rx)
    return (xp,yp,zp)
    
def draw_leaves(turtle, leaves, detailed_tree, branch_depth):
    if (detailed_tree):
        cs_width = 0.5 / (2 ** branch_depth) / 10.0
        turtle.set_cross_section("square", cs_width)
        for length,position in leaves:
            turtle.set_turtle(position)
            
            leaf(turtle, length, 16.0 / (2 ** branch_depth), cs_width)
    else:
        global radiusMap
        radiusMap = []
        for i in range(10):
            radiusMapSingle = []
            for x in range(100):
                line = []
                for y in range(100):
                    line.append(1.0)
                radiusMapSingle.append(line)
            radiusMap.append(radiusMapSingle)
        
        for n in range(200000):
            i = random.randrange(10)
            x = random.randrange(100)
            y = random.randrange(100)
            amount = random.uniform(-0.1, 0.1)
            radiusMap[i][x][y] += amount
            amount /= 2.0
            radiusMap[i][(x+1)%100][y] += amount
            radiusMap[i][(x-1)%100][y] += amount
            radiusMap[i][x][(y+1)%100] += amount
            radiusMap[i][x][(y-1)%100] += amount
            amount /= 2.0
            radiusMap[i][(x+1)%100][(y+1)%100] += amount
            radiusMap[i][(x+1)%100][(y-1)%100] += amount
            radiusMap[i][(x-1)%100][(y-1)%100] += amount
            radiusMap[i][(x-1)%100][(y+1)%100] += amount
        print("Num leaves = "+str(len(leaves)))
        for length,position in leaves:
            
            BlogoUtils.draw_plane_from_func("leaves", sphere_func, (100,100), True, True, "green", radius=length*.5, position=position, map_to_use=random.randrange(10))
        
def leaf(turtle, branch_length, size, cs_width):
    #size = 0.2
    
    
    draw_leaf(turtle, size)
    turtle.rt(180)
    turtle.fd(branch_length/10.0)
    draw_leaf(turtle, size)
    
    turtle.fd(branch_length/10.0)
    turtle.clockwise(90)
    draw_leaf(turtle, size)
    turtle.fd(branch_length/10.0)
    turtle.rt(180)
    
    draw_leaf(turtle, size)
    turtle.rt(180)
    
    turtle.fd(branch_length/10.0)
    turtle.clockwise(45)
    draw_leaf(turtle, size)
    turtle.fd(branch_length/10.0)
    turtle.rt(180)
    draw_leaf(turtle, size)
    turtle.rt(180)
    
    turtle.fd(branch_length/10.0)
    turtle.clockwise(90)
    draw_leaf(turtle, size)
    turtle.fd(branch_length/10.0)
    turtle.rt(180)
    draw_leaf(turtle, size)
    turtle.rt(180)
    
def draw_leaf(turtle, size):
    turtle.fill(0, 1, "green")
    turtle.set_fill_unwrap(True)
    turtle.circle(size, 10)
    turtle.fill_stop()

def draw_tree(tree_height, location=(0,0,0), detailed_tree=False):
    if (detailed_tree):
        branch_length = tree_height / 2.5
        branch_depth = 5
    else:
        branch_length = tree_height / 2.2
        branch_depth = 2
        
    turtle = Blogo()
    turtle.set_pos(location)
    turtle.set_texture("saddlebrown")
    turtle.set_cross_section("circle")
    turtle.set_v_heading(90 + random.uniform(-10, 10))
    turtle.set_cross_section("circle10", 1)
    leaves = branch(turtle, [],  detailed_tree, branch_length, tree_height, branch_depth)
    draw_leaves(turtle, leaves, detailed_tree, branch_depth)

if not isLib:
    draw_tree(10.0, False)

    Blogo.clean_up()
    BlogoUtils.unselect_objects()
    BlogoUtils.show_objects()