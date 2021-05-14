from blogo import *

baseDir = "textures\\"
grassTex = baseDir + "grass.png"
glassTex = baseDir + "glass.png"
wallTex = baseDir + "wall.png"
wallTex2 = baseDir + "wall2.png"
roofTex = baseDir + "roof.png"
cobblesTex = baseDir + "cobbles.png"

golden_ratio = (1.0 + math.sqrt(5)) / 2.0

BlogoUtils.start_fresh()
BlogoUtils.add_light_area()

def dataDefaults(data):
    defaults = {"tower-lower": "none",  # none, rounded, angled, square, circle
                "tower-upper": "none", "tower-top": "none",   #as above
                "tower-shelter": "none", # none, flat, pitched
                "towers-sheltered": "both",  # both, top, bottom
                "crenulation-type": "none",  # none, square, triangle, sin, trochoid, trochoid-inv, trochoid-double
                "crenulation-height": 0.3, "crenulation-incr": 0.01,
                "crenulation-width-down": 0.33, "crenulation-width-up": 0.67,
                "stairs-type": "single",   # single, double, sideways, double-flipped
                "corbel-type": "none",   # none, square, rounded, angle
                "corbel-width-top": 0.4, "corbel-width-bottom": 0.2, "corbel-height": 0.5, "corbel-gap": 1.2,
                "corbel-steps": 3, "corbel-eaves-ratio": 0.8, "corbel-incr": 0.01
    }
    for key in defaults:
        if not (key in data):
            data[key] = defaults[key]
data = {}
def setup():
    global absWallHeight
    absWallHeight = None
    global data
    dataopts = []
    # 0:
    dataopts.append({"tower-lower": "square", "tower-upper": "square", "tower-top": "square",
                     "crenulation-type": "square", "crenulation-incr": 0.01,
                     "stairs-type": "single",
                     "corbel-type": "rounded",
                     "tower-shelter": "none"})
    # 1:
    dataopts.append({"tower-lower": "circle", "tower-upper": "circle", "tower-top": "circle",
                     "crenulation-type": "trochoid-double", "crenulation-incr": 0.01,
                     "trochoid-a": 5, "trochoid-b": 4})
    # 2:
    dataopts.append({"tower-lower": "none", "tower-upper": "angled", "tower-top": "angled",
                     "crenulation-type": "sin", "crenulation-incr": 0.1,
                     "crenulation-width-down": 0.3, "crenulation-width-up": 0.3,
                     "stairs-type": "double"})
    
    data = dataopts[2]
    
    dataDefaults(data)
    
    data["outer-length-n"] = 20
    data["outer-length-w"] = 20
    data["outer-length-s"] = data["outer-length-n"]
    data["outer-length-e"] = data["outer-length-w"]
    
    data["width-n"] = 5
    data["width-w"] = 4
    data["width-s"] = data["width-w"]
    data["width-e"] = data["width-w"]
    
    data["inner-length-n"] = data["outer-length-n"] - data["width-w"] - data["width-e"]
    data["inner-length-w"] = data["outer-length-w"] - data["width-n"] - data["width-s"]
    data["inner-length-s"] = data["outer-length-s"] - data["width-w"] - data["width-e"]
    data["inner-length-e"] = data["outer-length-e"] - data["width-n"] - data["width-s"]
    
    data["basement-start-height"] = -1
    data["basement-height"] = 2
    data["floor-void-height"] = 0.5
    data["ground-floor-height"] = 3
    data["first-floor-height"] = 3
    data["roof-soil-height"] = 0.5
    data["railing-min-height"] = 1.1
    data["shelter-height"] = 2.4
    data["shelter-pitch-height"] = 2.0
    data["upper-ceiling-height"] = data["basement-height"]\
                                 + data["floor-void-height"]\
                                 + data["ground-floor-height"]\
                                 + data["floor-void-height"]\
                                 + data["first-floor-height"]\
                                 + data["floor-void-height"]
                                 #+ data["roof-soil-height"]
    data["lower-ceiling-height"] = data["basement-height"]\
                                 + data["floor-void-height"]\
                                 + data["ground-floor-height"]\
                                 + data["floor-void-height"]
                                 #+ data["roof-soil-height"]
    data["courtyard-height"] = data["basement-start-height"]\
                             + data["basement-height"]\
                             + data["floor-void-height"]
    data["upper-floor-height"] = data["courtyard-height"]\
                               + data["first-floor-height"]\
                               + data["floor-void-height"]\
                               + data["roof-soil-height"]
    data["eaves-overhang-internal"] = 0.5
    data["eaves-overhang-internal-upper"] = 0.5
    data["eaves-overhang-external"] = 0.5
    data["tower-radius"] = 2.0
    data["gateway-width"] = 2.0
    data["gateway-height"] = 2.5
    
    data["window-above-floor"] = 1.0
    data["window-height"] = 1.0
    data["window-width"] = data["window-height"] * 1.618
    data["door-height"] = 2.0
    data["door-width"] = 0.8
    
    gatewayPos = (data["inner-length-n"] - data["gateway-width"]) / 2.0
    door_gap = data["door-width"] * 2
    data["window-layout-n-outer"] = ["w", "w", "w", "w", "w"]
    data["window-layout-n-upper"] = ["d", door_gap, "w", "w", "w", "w", "w", -door_gap, "d"]
    data["window-layout-n-lower"] = ["w", "w", gatewayPos, -gatewayPos, "w", "w"]
    data["window-layout-e"] = ["w", "w", "d", "w", "w"]
    data["window-layout-s"] = data["window-layout-e"]
    data["window-layout-w"] = data["window-layout-e"]
    data["window-layout-s-outer"] = ["w", "w", "w", "w", "w"]
    data["window-layout-gw-w"] = ["d", door_gap]
    data["window-layout-gw-e"] = ["d", door_gap]

    data["stairs-gap-width"] = 1.0
    
    data["stair-rise"] = 0.625 /(2.0 + golden_ratio)
    data["stair-tread"] = data["stair-rise"] * golden_ratio

    if (data["stairs-type"] == "sideways"):
        data["stairs-gap-start"] = 8.0
    elif (data["stairs-type"] == "double-flipped"):
        data["stairs-gap-start"] = -data["eaves-overhang-external"] + data["stairs-gap-width"]
    else:
        data["stairs-gap-start"] = -data["eaves-overhang-external"]
        
    
    
    if ("trochoid-a" in data and "trochoid-b" in data):
        init_trochoid_values(data["trochoid-a"], data["trochoid-b"])
    return data


def init_trochoid_values(a, b, dt=0.01):
    global trochoid_data
    trochoid_data = {}
    t = 0.0
    t_max = 2*math.pi
    x_max = a * t_max - b * math.sin(t_max)
    x_last = 0
    while (t <= t_max):
        x = a * t - b * math.sin(t)
        y = a - b * math.cos(t)
        i = int(1000*(x / x_max))
        trochoid_data[i] = y
        t += dt

def get_trochoid_value(x):
    missing_error = 10000
    adj = 1
    if (x > 0.5):
        adj = -1
    x = int(x*1000)
    while (not x in trochoid_data):
        x += adj
        missing_error -= 1
        if (missing_error < 0):
            raise Exception("Trochoid data missing for x = "+str(x))
    return trochoid_data[x]

def ground():
    turtle = Blogo()
    turtle.set_unwrap(False)
    turtle.set_texture(grassTex)
    turtle.set_texture_scale(0)
    #turtle.set_xyz(0, 0, 0)
    turtle.set_width("above", 0)
    turtle.set_width("below", 0.1)
    turtle.set_width("left", 150)
    turtle.set_width("right", 0)
    #turtle.up(45)
    turtle.fd(data["outer-length-n"])
    def turnRight(angle):
        for i in range(0,angle):
            turtle.rt(1)
            turtle.fd(0)
    turnRight(90)
    turtle.fd(data["outer-length-e"])
    turnRight(90)
    turtle.fd(data["outer-length-s"])
    turnRight(90)
    turtle.fd(data["outer-length-w"])
    turnRight(90)
    turtle.fd(0)

def tower(turtle, pos):
    if (pos != "top"):
        shelter_type = "none"
    else:
        shelter_type = data["tower-shelter"]
    turtle_shelter = Blogo("lower-walls")
    turtle_shelter.set_cross_section("square", 2)
    turtle_shelter.set_texture(wallTex)
    turtle_shelter.set_smart_project(True)
    turtle_shelter.set_texture_scale(50)
    if (shelter_type == "none"):
        turtle_shelter.pu()
    elif (shelter_type == "flat"):
        turtle_shelter.fill(0.99, 1, wallTex, "relative")
    turtle_shelter.set_width("below", 0)
    turtle_shelter.set_width("above", data["shelter-height"])
    turtle_shelter.set_width("left", 0.05)
    turtle_shelter.set_width("right", 0.05)
    turtle_shelter.copy_pos(turtle)
    
    turtle.add_follower(turtle_shelter)
    fill = None
    if (pos != "top"):
        fill = turtle.fill(0.99, 1, wallTex, "relative")
    
    radius = data["tower-radius"]
    overHang = 0
    if (pos == "top"):
        overHang = data["eaves-overhang-external"]
    
    tower_type = data["tower-"+pos]
    if (tower_type == "none"):
        turtle.fd(data["tower-radius"])
        turtle.rt(90)
        turtle.fd(data["tower-radius"])
    elif (tower_type == "rounded"):
        turtle.arc(90, radius + overHang)
    elif (tower_type == "angled"):
        r = radius + 2*overHang
        dist = math.sqrt(r * r / 2.0)
        turtle.lt(45)
        turtle.fd(dist)
        turtle.rt(90)
        turtle.fd(2 * dist)
        turtle.rt(90)
        turtle.fd(dist)
        turtle.lt(45)
    elif (tower_type == "square"):
        turtle.lt(90)
        turtle.fd(radius)
        turtle.rt(90)
        turtle.fd((radius + overHang) * 2)
        turtle.rt(90)
        turtle.fd((radius + overHang) * 2)
        turtle.rt(90)
        turtle.fd(radius)
        turtle.lt(90)
    elif (tower_type == "circle"):
        angle = math.degrees(math.asin(overHang / float(overHang + radius)))
        further = (radius + overHang) * (1 - math.cos(math.radians(angle)))
        turtle.fd(further)
        turtle.lt(90 - angle)
        turtle.arc(270 - 2 * angle, radius + overHang)
        turtle.lt(90 - angle)
        turtle.fd(further)
    else:
        raise Exception("Unknown tower type '"+str(tower_type)+"' for tower-"+pos)
    turtle.remove_follower(turtle_shelter)
    if (fill != None):
        turtle.fill_stop(fill)
    
    if (shelter_type == "pitched"):
        donePitched = True
        turtle_pitched = Blogo("pitched-roof")
        turtle_pitched.set_cross_section("square", 0.2)
        turtle_pitched.set_texture(roofTex)
        turtle_pitched.fill(0, 1, roofTex, "relative")
        
        start_pos = turtle_shelter.get_path_position(0).position
        mid_pos = turtle_shelter.get_path_position(0.5).position
        end_pos = turtle_shelter.get_path_position(1).position
        
        px = (start_pos[0] + mid_pos[0] + end_pos[0]) / 3
        py = (start_pos[1] + mid_pos[1] + end_pos[1]) / 3
        pz = (start_pos[2] + mid_pos[2] + end_pos[2]) / 3
        pz += data["shelter-height"] + data["shelter-pitch-height"]
        pitch_position = (px, py, pz)
        
        num_corners = 10.0
        prev_position = turtle_shelter.get_path_position(0).position
        
        for i in range(1, int(num_corners)+1):
            position = turtle_shelter.get_path_position(i / num_corners).position
            turtle_pitched.pu()
            turtle_pitched.set_pos(prev_position)
            turtle_pitched.set_z(prev_position[2] + data["shelter-height"])
            
            turtle_pitched.pd()
            turtle_pitched.fd(0)
            turtle_pitched.set_pos(position)
            turtle_pitched.set_z(position[2] + data["shelter-height"])
            turtle_pitched.fd(0)
            turtle_pitched.set_pos(pitch_position)
            turtle_pitched.fd(0)
            turtle_pitched.set_pos(prev_position)
            turtle_pitched.set_z(prev_position[2] + data["shelter-height"])
            turtle_pitched.fd(0)
            prev_position = position
    
def walls():
    turtle = Blogo("lower-walls")
    turtle_upper = Blogo("upper-walls")
    #turtle.set_unwrap(False)
    turtle.pu()
    turtle_upper.pu()
    turtle.set_cross_section("square", 2)
    turtle_upper.set_cross_section("square", 2)
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle_upper.set_texture(wallTex)
    turtle_upper.set_smart_project(True)
    turtle_upper.set_texture_scale(50)
    #turtle.set_texture_scale(2)
    #turtle_upper.set_texture_scale(100)
    #turtle.set_smart_project(True)
    turtle.set_width("above", data["lower-ceiling-height"])
    turtle_upper.set_width("above", data["upper-ceiling-height"] - data["lower-ceiling-height"] + 0.02)
    turtle.set_width("below", 0)
    turtle_upper.set_width("below", 0)
    turtle.set_width("left", 0.05)
    turtle_upper.set_width("left", 0.05)
    turtle.set_width("right", 0.05)
    turtle_upper.set_width("right", 0.05)
    turtle.set_z(data["basement-start-height"])
    turtle_upper.set_z(data["basement-start-height"] + data["lower-ceiling-height"] - 0.01)
    turtle.fd(data["tower-radius"])
    turtle_upper.fd(data["tower-radius"])
    turtle_upper.fill(0, 0.01, wallTex, "absolute")
    #turtle_upper.fill(0.99, 1, wallTex, "relative")
    turtle.pd()
    turtle_upper.pd()
    
    turtle.fd((data["outer-length-n"] - data["gateway-width"]) / 2 - data["tower-radius"])
    mul = 100.0
    base = data["courtyard-height"] + data["gateway-height"] + data["gateway-width"] / 2.0
    r = data["gateway-width"] / 2.0
    r2 = r * r
    for i in range(0, int(data["gateway-width"] * mul)):
        x = (i / mul) - r
        x2 = x * x
        h = math.sqrt(r2 - x2)
        turtle.set_width("below", -(base + h))
        turtle.fd(1.0 / mul)
    turtle.set_width("below", 0)
    turtle.fd((data["outer-length-n"] - data["gateway-width"]) / 2 - data["tower-radius"])
    
    turtle_upper.fd(data["outer-length-n"] - 2 * data["tower-radius"])
    
    tower(turtle, "lower")
    turtle.fd(data["width-n"] - data["tower-radius"])
    #turtle.set_width("above", data["lower-ceiling-height"])
    outerWallStart = turtle.path_length
    turtle.fd(data["outer-length-e"] - data["width-n"] - data["tower-radius"])
    tower(turtle, "lower")
    turtle.fd(data["outer-length-s"] - 2 * data["tower-radius"])
    tower(turtle, "lower")
    turtle.fd(data["outer-length-w"] - data["width-n"] - data["tower-radius"])
    #turtle.set_width("above", data["upper-ceiling-height"])
    outerWallEnd = turtle.path_length
    turtle.fd(data["width-n"] - data["tower-radius"])
    tower(turtle, "lower")
    turtle.fd(0)
    
    tower(turtle_upper, "upper")
    turtle_upper.fd(data["width-n"] - data["tower-radius"])
    turtle_upper.rt(90)
    #turtle_upper.fd(data["outer-length-e"] - data["width-n"] - data["tower-radius"])
    #tower(turtle_upper, "upper")
    turtle_upper.fd(data["outer-length-n"])
    #tower(turtle_upper, "upper")
    turtle_upper.rt(90)
    #turtle_upper.fd(data["outer-length-w"] - data["width-n"] - data["tower-radius"])
    turtle_upper.fd(data["width-n"] - data["tower-radius"])
    tower(turtle_upper, "upper")
    turtle_upper.fd(0)
    
    turtle.pu()
    turtle.set_width("above", data["upper-ceiling-height"])
    turtle.set_width("below", -data["lower-ceiling-height"])
    turtle.set_width("left", 0.05)
    turtle.set_width("right", 0.05)
    #turtle.set_xy(0, -data["width-n"])
    turtle.set_xy(data["width-n"], 0)
    
    turtle.pd()
    turtle.fd(data["width-w"])
    turtle.set_width("below", 0)
    #turtle.fd(data["inner-length-n"])
    
    turtle.fd((data["outer-length-n"] - data["gateway-width"]) / 2 - data["width-w"])
    mul = 100.0
    base = data["courtyard-height"] + data["gateway-height"] + data["gateway-width"] / 2.0
    r = data["gateway-width"] / 2.0
    r2 = r * r
    for i in range(0, int(data["gateway-width"] * mul)):
        x = (i / mul) - r
        x2 = x * x
        h = math.sqrt(r2 - x2)
        turtle.set_width("below", -(base + h))
        turtle.fd(1.0 / mul)
    turtle.set_width("below", 0)
    turtle.fd((data["outer-length-n"] - data["gateway-width"]) / 2 - data["width-e"])
    
    turtle.set_width("below", -data["lower-ceiling-height"])
    turtle.fd(data["width-e"])
    turtle.bk(data["width-e"])
    turtle.set_width("below", 0)
    turtle.rt(90)
    turtle.set_width("above", data["lower-ceiling-height"])
    innerWallStart = turtle.path_length
    turtle.fd(data["inner-length-e"])
    turtle.rt(90)
    turtle.fd(data["inner-length-s"])
    turtle.rt(90)
    turtle.fd(data["inner-length-w"])
    turtle.rt(90)
    turtle.fd(0)
    innerWallEnd = turtle.path_length
    
    return ((turtle_upper,0,turtle_upper.path_length,0,data["upper-ceiling-height"] - data["lower-ceiling-height"] + 0.02),
            (turtle,innerWallStart,innerWallEnd,180,data["lower-ceiling-height"]),
            (turtle,outerWallStart,outerWallEnd,0,data["lower-ceiling-height"])
    )
    
def gateway():
    turtle = Blogo()
    turtle.pu()
    turtle.set_cross_section("square", 2)
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle.set_y((data["outer-length-n"] - data["gateway-width"]) / 2)
    turtle.rt(90)
    turtle.up(90)
    turtle.set_width("above", 0)
    turtle.set_width("below", data["width-n"])
    turtle.set_width("left", data["gateway-width"])
    turtle.set_width("right", 0.05)
    turtle.pd()
    turtle.fd(data["courtyard-height"])
    turtle.set_width("left", 0.05)
    turtle.fd(data["gateway-height"])
    
    for i in range(0, 180):
        turtle.fd(data["gateway-width"] * math.pi / 360)
        turtle.lt(1)
        
    turtle.fd(data["gateway-height"])
    
    turtle.pu()
    turtle.set_texture(cobblesTex)
    
    turtle.set_texture_scale(5)
    turtle.set_width("right", 0)
    turtle.set_width("left", data["gateway-width"])
    turtle.set_width("above", 0.1)
    turtle.set_width("below", 0.1)
    turtle.up(90)
    turtle.bk(data["width-n"])
    turtle.pd()
    turtle.fd(data["width-n"])
    turtle.down(20)
    turtle.fd(data["width-n"])
    
def courtyard():
    turtle = Blogo()
    turtle.set_cross_section("square", 2)
    turtle.set_unwrap(False)
    turtle.set_texture(grassTex)
    turtle.set_texture_scale(0)
    turtle.set_xyz(data["width-n"], data["width-w"], data["courtyard-height"])
    turtle.set_width("above", 0)
    turtle.set_width("below", 0.5)
    turtle.set_width("left", 0)
    turtle.set_width("right", data["inner-length-e"])
    turtle.fd(data["inner-length-n"])
    
def crenulation_height(args):
    if (absWallHeight != None):
        return absWallHeight - data["railing-min-height"]
    length_along = args["full_length"]
    height = 0
    cren_type = data["crenulation-type"]
    cren_height = data["crenulation-height"]
    cren_width_down = float(data["crenulation-width-down"])
    cren_width_up = float(data["crenulation-width-up"])
    cren_width = cren_width_down + cren_width_up
    
    whole_lengths_before = int(length_along / cren_width)
    length_along -= whole_lengths_before * cren_width
    
    if (length_along > cren_width_down):
        in_up = True
        relpos = (length_along - cren_width_down) / cren_width_up
    else:
        in_up = False
        relpos = length_along / cren_width_down
    
    if (cren_type == "none"):
        height = 0
    elif (cren_type == "square"):
        if (length_along < cren_width_up):
            height = cren_height
        else:
            height = 0
    elif (cren_type == "triangle"):
        if (relpos > 0.5):
            relpos = 1 - relpos
        if (in_up):
            relpos = 0.5 + relpos
        else:
            relpos = 0.5 - relpos
        height = cren_height * relpos
    elif (cren_type == "sin"):
        if (in_up):
            rel_height = math.sin(math.pi * relpos)
        else:
            rel_height = math.sin(math.pi + math.pi * relpos)
        height = cren_height * (rel_height + 1.0) / 2.0
    elif (cren_type == "trochoid"):
        trochoid_height = get_trochoid_value(length_along / cren_width)
        rel_height = trochoid_height / (data["trochoid-a"] + data["trochoid-b"])
        height = cren_height * rel_height
    elif (cren_type == "trochoid-inv"):
        trochoid_height = get_trochoid_value(length_along / cren_width)
        rel_height = trochoid_height / (data["trochoid-a"] + data["trochoid-b"])
        height = cren_height * (1.0 - rel_height)
    elif (cren_type == "trochoid-double"):
        
        trochoid_height = get_trochoid_value(relpos)
        rel_height = trochoid_height / (data["trochoid-a"] + data["trochoid-b"])
        if (in_up):
            height = cren_height * (0.5 + 0.5*rel_height)
        else:
            height = cren_height * (0.5 * (1.0 - rel_height))
        
    else:
        raise Exception("Unknown crenulation type '"+str(cren_type)+"' for crenulation-type")
    return height

def roof():
    turtle = Blogo("roof-upper")
    
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle.set_cross_section("square", 2)
    turtle.set_width("above", data["railing-min-height"] + data["roof-soil-height"])
    turtle.set_width("below", 0)
    turtle.set_width("left", 0.05)
    turtle.set_width("right", 0.05)
    towerOverhang = data["tower-radius"] + data["eaves-overhang-external"]
    turtle.set_y(towerOverhang)
    turtle.set_x(-data["eaves-overhang-external"])
    turtle.set_z(data["upper-ceiling-height"] + data["basement-start-height"] + 0.02)
    
    
    turtle.fill(0.01, data["roof-soil-height"], grassTex, "absolute")
    turtle.set_fill_texture_scale(0)
    turtle.fill(0, 0.01, wallTex, "absolute")
    #turtle.fd(data["outer-length-n"] + 2*data["eaves-overhang"])
    #testing after

    turtle.add_width_func("above", crenulation_height)
    turtle.set_length_incr(data["crenulation-incr"])
    turtle.fd(data["outer-length-n"] - 2 * towerOverhang)
    tower(turtle, "top")
    turtle.fd(data["width-n"] + data["eaves-overhang-internal-upper"] - towerOverhang)
    turtle.rt(90)
    turtle.fd(data["eaves-overhang-external"] + data["stairs-gap-start"])
    global absWallHeight
    absWallHeight = 0
    turtle.fd(data["stairs-gap-width"])
    absWallHeight = None
    turtle.fd(data["outer-length-n"] - 2*(data["stairs-gap-start"] + data["stairs-gap-width"]))
    absWallHeight = 0
    turtle.fd(data["stairs-gap-width"])
    absWallHeight = None
    turtle.fd(data["eaves-overhang-external"] + data["stairs-gap-start"])
    #turtle.fd(data["outer-length-n"] + 2*data["eaves-overhang-external"])
    turtle.rt(90)
    turtle.fd(data["width-n"] + data["eaves-overhang-internal-upper"] - towerOverhang)
    tower(turtle, "top")
    
    turtle.fd(0)
    
    turtle = Blogo("roof-lower")
    
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle.set_cross_section("square", 2)
    turtle.add_width_func("above", crenulation_height)
    turtle.set_length_incr(data["crenulation-incr"])
    turtle.set_width("above", data["railing-min-height"] + data["roof-soil-height"])
    turtle.set_width("below", 0)
    turtle.set_width("left", 0.05)
    turtle.set_width("right", 0.05)
    turtle.set_y(-data["eaves-overhang-external"])
    turtle.set_x(data["width-n"])
    turtle.set_z(data["lower-ceiling-height"] + data["basement-start-height"] + 0.01)
    
    turtle.fill(0.01, data["roof-soil-height"], grassTex, "absolute")
    turtle.set_fill_texture_scale(0)
    turtle.fill(0, 0.01, wallTex, "absolute")
    turtle.fd(data["width-w"] + data["eaves-overhang-external"] + data["eaves-overhang-internal"])
    turtle.rt(90)
    turtle.fd(data["inner-length-w"] - data["eaves-overhang-internal"])
    turtle.lt(90)
    turtle.fd(data["inner-length-s"] - 2*data["eaves-overhang-internal"])
    turtle.lt(90)
    turtle.fd(data["inner-length-w"] - data["eaves-overhang-internal"])
    turtle.rt(90)
    turtle.fd(data["width-e"] + data["eaves-overhang-internal"] + data["eaves-overhang-external"])
    turtle.rt(90)
    turtle.fd(data["inner-length-e"] + data["width-s"] - towerOverhang)
    #turtle.rt(90)
    tower(turtle, "top")
    turtle.fd(data["outer-length-s"] - 2*towerOverhang)
    #turtle.rt(90)
    tower(turtle, "top")
    turtle.fd(data["inner-length-w"] + data["width-s"] - towerOverhang)
    turtle.rt(90)
    turtle.fd(0)

def draw_window(turtle, layout, length):
    turtle.pu()
    if (len(layout) == 0):
        turtle.fd(length)
        return
    dist_between = length / float(len(layout))
    turtle.fd(dist_between / 2.0)
    
    for item in layout:
        w = 0
        if (item == "d"):
            turtle.set_width("above", data["door-height"])
            turtle.set_width("below", 0)
            w = data["door-width"]
        elif (item == "w"):
            turtle.set_width("above", data["window-above-floor"] + data["window-height"])
            turtle.set_width("below", -data["window-above-floor"])
            w = data["window-width"]
        turtle.bk(w / 2.0)
        turtle.pd()
        turtle.fd(w)
        turtle.pu()
        turtle.bk(w / 2.0)
        turtle.fd(dist_between)
        
    turtle.bk(dist_between / 2.0)
    
def draw_windows(turtle, layout, max_dist):
    all_fixed_layouts = []
    all_fixed_stops = []
    this_fixed_layout = []
    for point in layout:
        if (type(point) == str):
            this_fixed_layout.append(point)
        else:
            all_fixed_layouts.append(this_fixed_layout)
            all_fixed_stops.append(point)
            this_fixed_layout = []
    all_fixed_layouts.append(this_fixed_layout)
    all_fixed_stops.append(max_dist)
    
    next_stop = max_dist
    for i in range(len(all_fixed_stops)-2, -1, -1):
        if (all_fixed_stops[i] < 0):
            all_fixed_stops[i] = next_stop + all_fixed_stops[i]
            next_stop = all_fixed_stops[i]
        else:
            next_stop = all_fixed_stops[i]

    all_fixed_lengths = []
    all_fixed_lengths.append(all_fixed_stops[0])
    for i in range(1, len(all_fixed_stops)):
        all_fixed_lengths.append(all_fixed_stops[i] - all_fixed_stops[i-1])

    for layout,length in zip(all_fixed_layouts, all_fixed_lengths):
        draw_window(turtle, layout, length)
    
def windows():
    turtle = Blogo("windows")
    turtle.set_texture(glassTex)
    turtle.set_cross_section("square", 2)
    turtle.set_width("left", 0.06)
    turtle.set_width("right", 0.06)
    
    turtle.set_xyz(0, data["tower-radius"], data["upper-floor-height"])
    turtle.set_heading(90)
    draw_windows(turtle, data["window-layout-n-outer"], data["outer-length-n"] - 2*data["tower-radius"])
    
    turtle.set_xyz(data["width-n"], 0, data["upper-floor-height"])
    turtle.set_heading(90)
    draw_windows(turtle, data["window-layout-n-upper"], data["outer-length-n"])
    
    turtle.set_xyz(data["width-n"], data["width-w"], data["courtyard-height"])
    turtle.set_heading(90)
    draw_windows(turtle, data["window-layout-n-lower"], data["inner-length-n"])
    
    turtle.set_xyz(data["width-n"], data["width-w"], data["courtyard-height"])
    turtle.set_heading(0)
    draw_windows(turtle, data["window-layout-w"], data["inner-length-w"])
    
    turtle.set_xyz(data["width-n"], data["outer-length-n"]-data["width-e"], data["courtyard-height"])
    turtle.set_heading(0)
    draw_windows(turtle, data["window-layout-e"], data["inner-length-e"])
    
    turtle.set_xyz((data["width-n"]+data["inner-length-e"]), data["width-w"], data["courtyard-height"])
    turtle.set_heading(90)
    draw_windows(turtle, data["window-layout-s"], data["inner-length-s"])
    
    turtle.set_xyz(data["outer-length-e"], data["tower-radius"], data["courtyard-height"])
    turtle.set_heading(90)
    draw_windows(turtle, data["window-layout-s-outer"], data["outer-length-s"] - 2*data["tower-radius"])
    
    turtle.set_xyz(data["width-n"], (data["outer-length-n"]-data["gateway-width"])/2.0, data["courtyard-height"])
    turtle.set_heading(180)
    draw_windows(turtle, data["window-layout-gw-w"], data["width-n"])
    
    turtle.set_xyz(data["width-n"], (data["outer-length-n"]+data["gateway-width"])/2.0, data["courtyard-height"])
    turtle.set_heading(180)
    draw_windows(turtle, data["window-layout-gw-e"], data["width-n"])
    
def draw_stairs(turtle, vdist):
    angle = 90
    if (vdist < 0):
        angle = -90
        vdist =  -vdist
    start_vdist = vdist
    while (vdist > 0):
        turtle.fd(data["stair-tread"])
        turtle.up(angle)
        turtle.fd(data["stair-rise"])
        turtle.down(angle)
        vdist -= data["stair-rise"]
    return vdist
    
def stairs(ref_point, direction):
    stairs_type = data["stairs-type"]
    stairs_gap_start = data["stairs-gap-start"]
    if (stairs_type == "double-flipped"):
        direction *= -1
        stairs_type = "double"
        stairs_gap_start -= 2 * data["stairs-gap-width"]
    brickWidth = 0.1
    angle = math.degrees(math.atan2(data["stair-rise"], data["stair-tread"]))
    turtle = Blogo("stairs-w")
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle.set_width("above", 0)
    turtle.set_width("below", brickWidth)
    turtle.set_width("left", data["stairs-gap-width"])
    turtle.set_width("right", data["stairs-gap-width"])
    turtle.set_xyz(data["width-n"] + data["eaves-overhang-internal-upper"] - brickWidth,\
                   ref_point + direction * (stairs_gap_start + data["stairs-gap-width"]/2),\
                   data["basement-start-height"] + data["upper-ceiling-height"] + data["roof-soil-height"] + brickWidth)
    turtle.rt(90)
    if (stairs_type == "sideways"):
        turtle.fd(data["stairs-gap-width"] + 2 * brickWidth)
        turtle.bk(data["stairs-gap-width"] / 2.0)
        turtle.rt(direction * 90)
        turtle.fd(data["stairs-gap-width"] / 2.0)
             
    vdiff = data["upper-ceiling-height"] - data["lower-ceiling-height"]
    if (stairs_type != "double"):
        vdiff1 = vdiff - draw_stairs(turtle, -vdiff)
        vdiff2 = 0
    else:
        vdiff /= 2.0
        turtle.fd(data["stairs-gap-width"] + 2 * brickWidth)
        vdiff1 = vdiff - draw_stairs(turtle, -vdiff)
        vdiff = (vdiff * 2.0) - vdiff1
        turtle.fd(data["stairs-gap-width"])
        turtle.bk(data["stairs-gap-width"] / 2.0)
        turtle.lt(direction * 90)
        turtle.fd(data["stairs-gap-width"] * 1.5)
        turtle.bk(data["stairs-gap-width"] / 2.0)
        turtle.lt(direction * 90)
        turtle.fd(data["stairs-gap-width"] / 2.0)
        vdiff2 = vdiff - draw_stairs(turtle, -vdiff)
    stairs_length = vdiff1 / math.sin(math.radians(angle))
    stairs_length2 = vdiff2 / math.sin(math.radians(angle))
    
    turtle = Blogo("stairs-w-rw")
    turtle.set_texture(wallTex)
    turtle.set_smart_project(True)
    turtle.set_texture_scale(50)
    turtle.set_xyz(data["width-n"] + data["eaves-overhang-internal-upper"] - brickWidth,\
                   ref_point + direction * stairs_gap_start,\
                   data["basement-start-height"] + data["upper-ceiling-height"] + data["roof-soil-height"] + brickWidth)
    
    turtle.set_width("above", 2)
    turtle.set_width("below", 0)
    turtle.set_width("left", brickWidth)
    turtle.set_width("right", brickWidth)
    
    turtle.rt(90)
    if (stairs_type == "sideways"):
        turtle.fd(2 * brickWidth)
        turtle.rt(direction * 90)
    elif (stairs_type == "double"):
        turtle.fd(data["stairs-gap-width"] + 2 * brickWidth)
    turtle.tilt_v(angle)
    turtle.down(angle)
    turtle.fd(stairs_length)
    turtle.tilt_v(-angle)
    turtle.up(angle)
    if (stairs_type == "double"):
        turtle.fd(data["stairs-gap-width"])
        turtle.lt(direction * 90)
        turtle.fd(data["stairs-gap-width"] * 2.0)
        turtle.lt(direction * 90)
        turtle.fd(data["stairs-gap-width"])
        turtle.tilt_v(angle)
        turtle.down(angle)
        turtle.fd(stairs_length2)
        turtle.tilt_v(-angle)
        turtle.up(angle)
        turtle.rt(180)
    turtle.pu()
    turtle.set_xyz(data["width-n"] + data["eaves-overhang-internal-upper"] - brickWidth,\
                   ref_point + direction * (stairs_gap_start + data["stairs-gap-width"]),\
                   data["basement-start-height"] + data["upper-ceiling-height"] + data["roof-soil-height"] + brickWidth)
    
    turtle.pd()
    if (stairs_type == "sideways"):
        turtle.lt(direction * 90)
        turtle.fd(data["stairs-gap-width"] + 2 * brickWidth)
        turtle.rt(direction * 90)
        turtle.fd(data["stairs-gap-width"])
    elif (stairs_type == "double"):
        turtle.fd(data["stairs-gap-width"] + 2 * brickWidth)
        
    turtle.tilt_v(angle)
    turtle.down(angle)
    turtle.fd(stairs_length)
    if (stairs_type == "double"):
        turtle.up(angle)
        turtle.rt(180)
        turtle.down(angle)
        turtle.fd(stairs_length2)

def draw_corbel(turtle, eaves_size):
    turtle.set_cross_section("square", 1, 2)
    #"corbel-type": "none",   # none, square, rounded, angle
    #            "corbel-width": 0.2, "corbel-height": 1, "corbel-gap": 1.2,
    #            "corbel-steps": 3, "corbel-eaves-ratio": 0.8,
    projection_change_pos = float(data["corbel-height"]) / data["corbel-steps"]
    next_projection_change_pos = projection_change_pos
    projection = float(data["corbel-eaves-ratio"] * eaves_size)
    projection_change = projection / data["corbel-steps"]
    curve_length = data["corbel-width-top"] - data["corbel-width-bottom"]
    width = data["corbel-width-bottom"]
    pos = 0
    incr = data["corbel-incr"]
    turtle.set_width("below", 0)
    while (pos < data["corbel-height"]):
        if (data["corbel-type"] == "rounded" and pos <= curve_length):
            pos_from_bottom = curve_length - pos
            x = math.sqrt(curve_length*curve_length - pos_from_bottom*pos_from_bottom)
            width = data["corbel-width-top"] - x
        turtle.set_width("left", width)
        turtle.set_width("right", width)
        turtle.set_width("above", projection)
        turtle.fd(incr)
        pos += incr
        next_projection_change_pos -= incr
        if (next_projection_change_pos <= 0):
            next_projection_change_pos = projection_change_pos
            projection -= projection_change

def corbels(eaves_paths):
    if (data["corbel-type"] == "none"):
        return
    for (path,start,end,fudge,height) in eaves_paths:
        turtle = Blogo("corbels-"+path.name)
        turtle.set_texture(wallTex2)
        x = data["corbel-width-top"] +  start
        width = data["corbel-gap"]
        length = end - width
        
        while (x < length):
            turtle.pu()
            turtle_pos = path.get_path_position(x, "absolute")
            turtle.set_pos(turtle_pos.position)
            turtle.set_z(turtle_pos.position[2] + height)
            turtle.turtle.fd_vec = turtle_pos.fd_vec
            turtle.turtle.up_vec = turtle_pos.up_vec
            turtle.lt(90+fudge)
            turtle.down(90)
            turtle.pd()
            draw_corbel(turtle, data["eaves-overhang-external"])
            x += width
    
def main():
    setup()
    ground()
    eaves_paths = walls()
    courtyard()
    gateway()
    roof()
    windows()
    stairs(0, 1)
    stairs(data["outer-length-n"], -1)
    corbels(eaves_paths)
    
    global libRun
    libRun = True
    run("person.py")
    draw_person(1.88, (data["width-n"]+0.5, data["outer-length-n"]/2, data["courtyard-height"]))
    
    libRun = True
    run("tree.py")
    draw_tree(3, (data["width-n"] + data["inner-length-e"]/2, data["width-w"] + data["inner-length-n"]/2, data["courtyard-height"]))

main()

Blogo.clean_up()
BlogoUtils.unselect_objects()
BlogoUtils.show_objects()