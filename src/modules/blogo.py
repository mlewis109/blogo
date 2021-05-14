#exec(open("C:\\dev\\blender\\blogo\\src\\blogo.py").read())

# TODO
# add multiple named cross sections
# add helper function to create new cross section of add_gap(widths_in_cs1, widths_in_cs2, width1, width2, gap_y)
# add funtion remove_cross_section and remove_gap
#exec(open("C:\\dev\\blender\\blogo\\src\\blogo_utils.py").read())
from blogo_utils import *

import bpy
import math
import numpy as np
import copy


class Mesh:
    """
    """
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.mesh_object = None
        self.needs_start_cap = True
    def copy(self):
        newcopy = Mesh()
        newcopy.__dict__.update(self.__dict__)
        newcopy.vertices = copy.deepcopy(newcopy.vertices)
        newcopy.faces = copy.deepcopy(newcopy.faces)
        return copy
    def deepcopy(self, new_location, relative_location):
        newcopy = self.copy()
        if (newcopy.mesh_object != None):
            newcopy.mesh_object = copy_object(newcopy.mesh_object, new_location, relative_location, copy_mesh=True)[0]
        return copy
    def append_vertex(self, vertex):
        self.vertices.append(vertex)
    def append_face(self, face):
        self.faces.append(face)
    def draw(self, objname, textureFile, alpha, unwrap, smart_project, texture_scale):
        self.mesh_object = BlogoUtils.draw_mesh(objname, self.vertices, self.faces, textureFile, alpha, unwrap, smart_project, texture_scale)
        return self.mesh_object
    def is_empty(self):
        return (self.vertex_count() == 0)
    def vertex_count(self):
        return len(self.vertices)
    def get_object(self):
        return self.mesh_object

class FillMesh:
    """
    """
    def __init__(self, name, from_value, to_value, fill_type, texture, alpha):
        self.name = name
        self.from_value = from_value
        self.to_value = to_value
        self.fill_type = fill_type
        self.texture = texture
        self.alpha = alpha
        self.unwrap = False
        self.smart_project = False
        self.mesh = Mesh()
        self.lastVertexBottom = None
        self.lastVertexTop = None
        self.texture_scale = None
    def copy(self):
        newcopy = FillMesh(self.name, self.from_value, self.to_value, self.fill_type, self.texture, self.alpha)
        newcopy.__dict__.update(self.__dict__)
        return newcopy
    def deepcopy(self, new_location, relative_location):
        newcopy = self.copy()
        newcopy.mesh = newcopy.mesh.deepcopy(new_location, relative_location)
        return newcopy
    def get_object(self):
        return self.mesh.get_object()
        
    def draw(self):
        count = len(self.mesh.vertices)
        if (count < 4):
            return None
        #face = [count-2, 0, 1, count-1]
        face = [count-1, 1, 0, count-2]
        self.mesh.append_face(face)
        faces = ([], [])
        for v in range(0, len(self.mesh.vertices), 2):
            faces[0].append(v)
            faces[1].append(v+1)
        faces[1].reverse()
        self.mesh.append_face(faces[0])
        self.mesh.append_face(faces[1])
        
        obj = self.mesh.draw(self.name, self.texture, self.alpha, self.unwrap, self.smart_project, self.texture_scale)
        return obj
    def append_vertices(self, vertexBottom, vertexTop):
        if (self.lastVertexBottom == vertexBottom and self.lastVertexTop == vertexTop):
            return
        self.lastVertexBottom = vertexBottom
        self.lastVertexTop = vertexTop
        
        self.mesh.append_vertex(vertexBottom)
        self.mesh.append_vertex(vertexTop)
        count = len(self.mesh.vertices)
        if (count > 2):
            #face = [count-4, count-2, count-1, count-3]
            face = [count-3, count-1, count-2, count-4]
            self.mesh.append_face(face)
    def set_unwrap(self, unwrap):
        self.unwrap = unwrap
    def set_texture_scale(self, texture_scale):
        self.texture_scale = texture_scale

class TurtlePosition:
    """Class to keep track of where the turtle is and which way it faces.
    
    Contains fields:
    
    - position - A 3D nparray saying where in space the turtle currently is
    - fd_vec - A 3-tuple containing the unit vector to describe the direction of forward
    - up_vec - A 3-tuple containing the unit vector to describe the direction of up
    - tilt_v_angle - An angle in degrees specifying how the cross section should be rotated vertically (pitch)
    - tilt_h_angle - An angle in degrees specifying how the cross section should be rotated horizontally (yaw)
    - tilt_r_angle - An angle in degrees specifying how the cross section should be rotated round (roll)
    """
    def __init__(self, turtle=None):
        """
        Create a new turtle
        
        Create a new turtle, which is either put at zero facing in the default direction,
        or is a copy of the turtle passed in to it
        :param turtle: TurtlePosition to copy or None to put in default position
        :type turtle: TurtlePosition
        """
        if (turtle == None):
            self.home()
        else:
            self.copy(turtle)
    
    def copy(self, turtle):
        self.position = turtle.position
        self.fd_vec = turtle.fd_vec
        self.up_vec = turtle.up_vec
        self.tilt_v_angle = turtle.tilt_v_angle
        self.tilt_h_angle = turtle.tilt_h_angle
        self.tilt_r_angle = turtle.tilt_r_angle
        
    def home(self):
        self.position = (0.0, 0.0, 0.0)
        self.fd_vec = np.array((0.0, 1.0, 0.0))
        self.up_vec = np.array((0.0, 0.0, 1.0))
        self.tilt_v_angle = 0
        self.tilt_h_angle = 0
        self.tilt_r_angle = 0
        
    def get_copy(self):
        return TurtlePosition(self)
        
    def add_position(self, x, y, z):
        self.position = (self.position[0] + x,
                         self.position[1] + y,
                         self.position[2] + z
        )
        
    def roll_vec(self):
        return np.cross(self.fd_vec, self.up_vec)
        
def parse(text, var=None, var_name="var"):
    if (Blogo.last_turtle == None):
        turtle = Blogo()
    Blogo.last_turtle.parse(text, var, var_name)
def parse_file(file, var=None, var_name="var"):
    if (Blogo.last_turtle == None):
        turtle = Blogo()
    Blogo.last_turtle.parse_file(file, var, var_name)
    
class Blogo:
    """
    A class which describes a turtle and has functions to move it in space.
    """
    __instances = []
    __origin = (0, 0, 0)
    last_turtle = None
    
    def __init__(self, name="Blogo"):
        """
        Create a new instance of a turtle, ready to draw
        
        :param name: 
        :type name: string
        """
        Blogo.last_turtle = self
        Blogo.__instances.append(self)
        self.name = name
        self.turtle = TurtlePosition()
        self.reset(True)
        
    def copy(self, deep_copy=False, new_location=(0,0,0), relative_location=True):
        """
        Returns a copy of the current Blogo instance
        
        :param deep_copy: If True then the existing Blender objects will be duplicated, if False the copy is still fairly deep, but no new objects
        :type deep_copy: bool
        :param new_location: The new location of the copy, either absolute or relative
        :type new_location: tuple
        :param relative_location: Indicates if new_location should be absolute or moved relative to the current turtle position
        :type relative_location: bool
        
        :rtype: Blogo
        """
        if (not relative_location):
            new_location = BlogoUtils.add_locations(new_location, self.turtle.position, -1)
            relative_location = True
            
        newcopy = Blogo(name)
        newcopy.__dict__.update(self.__dict__)
        newcopy.turtle = self.turtle.get_copy()
        
        newcopy.multipliers = copy.deepcopy(self.multipliers)
        newcopy.length_counters = copy.deepcopy(self.length_counters)
        newcopy.width_func = copy.deepcopy(self.width_func)
        newcopy.width_args = copy.deepcopy(self.width_args)
        newcopy.followers = copy.deepcopy(self.followers)
        
        newcopy.path = copy.deepcopy(self.path)
        newcopy.cross_section = copy.deepcopy(self.cross_section)
        
        if (deep_copy):
            newcopy.mesh_objects = self.mesh_objects.deepcopy(new_location, relative_location)
            newcopy.fillMeshes = self.fillMeshes.deepcopy(new_location, relative_location)
        else:
            newcopy.mesh_objects = self.mesh_objects.copy()
            newcopy.fillMeshes = self.fillMeshes.copy()
            
        newcopy.turtle.position = BlogoUtils.add_locations(new_location, newcopy.turtle.position)
        newpath = []
        for length, turtle in newcopy.path:
            turtle.position = BlogoUtils.add_locations(new_location, turtle.position)
            newpath.append((length, turtle))
        newcopy.path = newpath
        return newcopy
    
    def clean_up():
        """
        Draw all outstanding Blogo instances
        """
        for i in Blogo.__instances:
            i.__draw_mesh()
        Blogo.__instances = []
        #bpy.context.scene.update()
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
    def set_global_origin(origin=0, origin_y=0, origin_z=0):
        """
        Change the origin used by all instances of Blogo.
        
        :param origin: Either a tuple containing the origin's location or the x location
        :param origin_y: y coordinate of the origin (defaults to either 0 or value given in origin if tuple)
        :param origin_z: z coordinate of the origin (defaults to either 0 or value given in origin if tuple)
        :type origin: tuple, int, float
        :type origin_y: int, float
        :type origin_z: int, float
        """
        if BlogoUtils.is_sequence(origin):
            origin_x = origin[0] if (len(origin) > 0) else 0
            origin_y = origin[1] if (len(origin) > 1) else origin_y
            origin_y = origin[2] if (len(origin) > 2) else origin_z
        else:
            origin_x = origin
        Blogo.__origin = (origin_x, origin_y, origin_z)
    def get_global_origin():
        """
        Return the origin used by all instances of Blogo.
        
        :returns: Location of global origin
        :rtype: tuple
        """
        return Blogo.__origin
    def set_origin(self, origin=0, origin_y=0, origin_z=0):
        """
        Change the origin used by this turtle.
        
        :param origin: Either a tuple containing the origin's location or the x location
        :param origin_y: y coordinate of the origin (defaults to either 0 or value given in origin if tuple)
        :param origin_z: z coordinate of the origin (defaults to either 0 or value given in origin if tuple)
        :type origin: tuple, int, float
        :type origin_y: int, float
        :type origin_z: int, float
        """
        if BlogoUtils.is_sequence(origin):
            origin_x = origin[0] if (len(origin) > 0) else 0
            origin_y = origin[1] if (len(origin) > 1) else origin_y
            origin_y = origin[2] if (len(origin) > 2) else origin_z
        else:
            origin_x = origin
        self.__local_origin = (origin_x, origin_y, origin_z)
    def get_origin(self):
        """
        Return the origin used by this turtle.
        
        :returns: Location of local origin
        :rtype: tuple
        """
        return self.__origin
        
    def reset(self, init=False):
        """
        Return the turtle to the origin and remove all modifiers
        """
        self.history = []
        self.mesh_objects = []
        self.cs_mul_h = {}
        self.cs_mul_v = {}
        self.reset_multipliers()
        if (not init):
            self.__draw_mesh()
        self.length_counters = {}
        self.reset_length_counter("full_length")
        self.reset_length_counter("line_length", 1)
        #self.full_length = 0.0
        self.relative_length = 0.0
        #self.line_length = 0.0
        self.length_incr = 0.1
        self.length_incr_mul = 0.01
        self.width_func = {}
        self.width_args = {}
        self.followers = []
        
        self.mesh = {}
        self.lastPointInserted = {}
        self.skipped_point = {}
        self.last3DVertices = {}
        self.needs_start_cap = {}
        self.home()
        self.__start_mesh("")
        self.pen_down()
        self.reset_cross_section()
        self.set_texture(None)
        self.set_alpha(1.0)
        self.set_unwrap(True)
        self.set_smart_project(False)
        self.fillMeshes = []
        self.path = []
        self.path_length = 0.0
        self.texture_scale = None        
        self.gap_widths = {}
        self.__local_origin = (0, 0, 0)
        
    def reset_multipliers(self, cs_name=None):
        """
        Reset width multipliers to 1
        """
        if (cs_name == None):
            self.multipliers = {}
            cs_name = ""
            
        self.multipliers[cs_name] = {
            "left": 1.0,
            "right": 1.0,
            "above": 1.0,
            "below": 1.0
        }
        self.cs_mul_h[cs_name] = 1
        self.cs_mul_v[cs_name] = 1
        
    def reset_cross_section(self):
        """
        Reset the cross section to a square
        """
        self.cross_section = {}
        self.set_cross_section("square")
    
    def home(self):
        """
        Return the turtle to the origin
        """
        self.turtle.home()

    def get_objects(self):
        """
        Return the blender objects for this turtle.
        
        :returns: A list of blender objects
        """
        self.__draw_mesh()
        return self.mesh_objects
        
    def __roll_vec(self):
        return np.cross(self.turtle.fd_vec, self.turtle.up_vec)
        
    def left(self, angle):
        """
        Turn left by angle degrees

        :param angle: Number of degrees to turn left by
        """
        self.history.append(("left", angle))
        
        # rotate fd_vec around up_vec
        self.turtle.fd_vec = BlogoUtils.rotate_axis(self.turtle.up_vec, self.turtle.fd_vec, angle)
        for f in self.followers:
            f.left(angle)
    def lt(self, angle):
        """
        Turn left by angle degrees

        :param angle: Number of degrees to turn left by
        """
        return self.left(angle)
    def right(self, angle):
        """
        Turn right by angle degrees

        :param angle: Number of degrees to turn right by
        """
        return self.left(-angle)
    def rt(self, angle):
        """
        Turn right by angle degrees

        :param angle: Number of degrees to turn right by
        """
        return self.right(angle)
        
    def up(self, angle):
        """
        Rotate upwards by angle degrees

        :param angle: Number of degrees to rotate upwards by
        """
        self.history.append(("up", angle))
        roll_vec = self.__roll_vec()
        self.turtle.fd_vec = BlogoUtils.rotate_axis(roll_vec, self.turtle.fd_vec, angle)
        self.turtle.up_vec = BlogoUtils.rotate_axis(roll_vec, self.turtle.up_vec, angle)
        for f in self.followers:
            f.up(angle)
    def down(self, angle):
        """
        Rotate downwards by angle degrees

        :param angle: Number of degrees to rotate downwards by
        """
        return self.up(-angle)
    def dn(self, angle):
        """
        Rotate downwards by angle degrees

        :param angle: Number of degrees to rotate downwards by
        """
        return self.down(angle)
        
    def clockwise(self, angle):
        """
        Rotate clockwise by angle degrees

        :param angle: Number of degrees to rotate clockwise by
        """
        self.history.append(("clockwise", angle))
        self.turtle.up_vec = BlogoUtils.rotate_axis(self.turtle.fd_vec, self.turtle.up_vec, angle)
        for f in self.followers:
            f.clockwise(angle)
    def anticlockwise(self, angle):
        """
        Rotate anti-clockwise by angle degrees

        :param angle: Number of degrees to rotate anti-clockwise by
        """
        return self.clockwise(-angle)
        
    def tilt_h(self, angle):
        """
        Tilt the cross section in the horizontal axis by angle degrees

        :param angle: Number of degrees to tilt horizontally by
        """
        self.history.append(("tilt_h", angle))
        self.turtle.tilt_h_angle = BlogoUtils.normalize_angle(self.turtle.tilt_h_angle + angle)
        for f in self.followers:
            f.tilt_h(angle)
    def tilt_v(self, angle):
        """
        Tilt the cross section in the vertical axis by angle degrees

        :param angle: Number of degrees to tilt vertically by
        """
        self.history.append(("tilt_v", angle))
        self.turtle.tilt_v_angle = BlogoUtils.normalize_angle(self.turtle.tilt_v_angle + angle)
        for f in self.followers:
            f.tilt_v(angle)
    def tilt_r(self, angle):
        """
        Roll the cross section by angle degrees

        :param angle: Number of degrees to roll by
        """
        self.history.append(("tilt_r", angle))
        self.turtle.tilt_r_angle = BlogoUtils.normalize_angle(self.turtle.tilt_r_angle + angle)
        for f in self.followers:
            f.tilt_r(angle)

    def forward(self, dist):
        """Move the turtle forward by dist
        
        Move the turtle forward (or backwards if negative) by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.
        
        :param dist: Distance to move
        :type dist: int, float
        """
        self.history.append(("forward", dist))
        dist_param = dist
        flip = 1
        if (dist < 0):
            flip = -1
            dist = -dist
        self.lastPointInserted = {}
        self.skipped_point = {}
        dist = float(dist)
        non_zero_dist = dist if (dist!=0) else 1
        
        length_incr = self.length_incr
        if (length_incr > dist * self.length_incr_mul):
            length_incr = dist * self.length_incr_mul
            
        width_funcs = self.__has_width_funcs()
        if (not width_funcs and not self.penDown):
            length_incr = dist
            
        self.relative_length = 0.0
        self.reset_length_counter("line_length", include_bk=1)
        self.__insert_cross_section(True)
        
        while (dist > length_incr):
            self.turtle.add_position(flip * self.turtle.fd_vec[0] * length_incr,
                                     flip * self.turtle.fd_vec[1] * length_incr,
                                     flip * self.turtle.fd_vec[2] * length_incr)
            if (width_funcs):
                self.__insert_cross_section(False)
                
            if (self.penDown):
                self.path_length += length_incr
                self.path.append((self.path_length, self.turtle.get_copy()))
            
            dist -= length_incr
            self.__update_length_counters(flip, length_incr)
            self.relative_length = min(1.0, self.get_length_counter("line_length") / non_zero_dist)
            
        self.turtle.add_position(flip * self.turtle.fd_vec[0] * dist,
                                 flip * self.turtle.fd_vec[1] * dist,
                                 flip * self.turtle.fd_vec[2] * dist)
                                 
        self.__update_length_counters(flip, length_incr)
        self.relative_length = min(1.0, self.get_length_counter("line_length") / non_zero_dist)
        self.__insert_cross_section(True)
        if (self.penDown):
            self.path_length += dist
            self.path.append((self.path_length, self.turtle.get_copy()))
            
        for f in self.followers:
            f.forward(dist_param)
            
    def fd(self, dist):
        """Move the turtle forward by dist

        Move the turtle forward (or backwards if negative) by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.

        :param dist: Distance to move
        :type dist: int, float
        """
        self.forward(dist)
    def backward(self, dist):
        """Move the turtle backward by dist

        Move the turtle backwards (or forwards if negative) by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.

        :param dist: Distance to move
        :type dist: int, float
        """
        self.forward(-dist)
    def bk(self, dist):
        """Move the turtle backward by dist

        Move the turtle backwards (or forwards if negative) by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.

        :param dist: Distance to move
        :type dist: int, float
        """
        self.backward(dist)

    def strafe(self, dist):
        """
        Move the turtle sideways by dist

        Move the turtle sideways by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.

        :param dist: Distance to move
        :type dist: int, float
        """
        self.history.append(("strafe", dist))
        self.__insert_cross_section()
        self.turtle.add_position(self.turtle.roll_vec()[0] * dist,
                                 self.turtle.roll_vec()[1] * dist,
                                 self.turtle.roll_vec()[2] * dist)
        self.__insert_cross_section()        
        for f in self.followers:
            f.strafe(dist)
        
    def strafe_v(self, dist):
        """
        Move the turtle upwards by dist

        Move the turtle upwards (or down if negative) by dist.
        If the pen is down it will trail behind it defined by the current
        cross section and width modifiers.

        :param dist: Distance to move
        :type dist: int, float
        """
        self.history.append(("strafe_v", dist))
        self.__insert_cross_section()
        self.turtle.add_position(self.turtle.up_vec[0] * dist,
                                 self.turtle.up_vec[1] * dist,
                                 self.turtle.up_vec[2] * dist)
        self.__insert_cross_section()        
        for f in self.followers:
            f.strafe_v(dist)
        
    def arc(self, angle, radius, steps=None):
        """
        Move the turtle in an arc

        The turtle will move in an arc round for angle degrees, with a given radius.
        If steps is specified the arc will be made up of that made straight sections.

        :param angle:  The interior angle of the arc in degrees.  If this is positive the arc moves round to the right, otherwise to the left.
        :param radius: The distance from the centre of the arc
        :param steps: The number of straight lines to construct the arc from (default = angle)
        """
        if (steps == None):
            steps = int(abs(angle))
        turn = abs(float(angle) / steps)
        circumference = 2.0 * math.pi * radius * abs(angle/360.0)
        dist = circumference / steps
        total_dist = 0.0
        total_turn = 0.0
        turnFunc = self.rt
        if (angle < 0):
            angle = -angle
            turnFunc = self.lt
        for i in range(0, int(steps)):
            self.fd(dist)
            turnFunc(turn)
            total_dist += dist
            total_turn += turn
        self.fd(circumference - total_dist)
        turnFunc(angle - total_turn)
        
    def circle(self, radius, direction="right", steps=None):
        """
        Draw a circle with a given radius

        :param radius: The radius of the circle.
        :param direction:  The side the circle should be draw on, "right" (default) or "left"
        :param steps: The number of straight lines to draw the circle from.  Default: 360
        """
        angle = 360
        if (direction  == "left" or 
            (type(direction) == float or type (direction) == int) and direction < 0):
            angle = -360
        self.arc(angle, radius, steps)
        
    def polygon(self, sides, lengths, angles=None):
        """
        Draw a polygon with a given number of sides.

        Draws a polygon.  If the number of lengths or angles given is equal to the number of sides,
        then the polygon may not be closed

        :param sides: The number of sides the polygon should have
        :param lengths: Either an int/float giving the length of every side, or a list of the lengths of each side
        :param angles: If given then either an int/float giving every angle, or a list of the angles after each side.
        """
        start_pos = self.get_pos()
        if (not BlogoUtils.is_sequence(lengths)):
            lengths = [lengths]
        if (angles == None):
            angles = [360.0 / sides]
        elif (not BlogoUtils.is_sequence(angles)):
            angles = [angles]
        closed = True
        if (len(angles) >= sides or len(lengths) >= sides):
            closed = False
        else:
            sides -= 1
        total_turn = 0
        for i in range(sides):
            self.fd(lengths[i % len(lengths)])
            angle = angles[i % len(angles)]
            total_turn += angle
            self.rt(angle)
        if closed:
            self.fd(0)
            self.set_pos(start_pos)
            self.fd(0)
        self.rt(360 - total_turn)
        self.fd(0)
    def triangle(self, length, angles=None):
        """
        Draw a three sided polygon.

        :param length: Either an int/float giving the length for an equilateral triangle, or a list giving the length of the sides.
        :param angles: If not given then a closed triangle will be drawn from the given lengths, otherwise an int/float or list of angles (triangle may not be closed)
        """
        self.polygon(3, length, angles)
    def square(self, length):
        """
        Draws a polygon with four equal sides

        :param length: The length of the sides.
        """
        self.polygon(4, length)
    def rectangle(self, length1, length2):
        """
        Draws a rectangle

        :param length1: The length of the first and third sides
        :param length2: The length of the second and fourth sides
        """
        self.polygon(4, [length1, length2])
    
    def curve_to(self, end_position, end_direction, start_strength=1.0, end_strength=1.0):
        """
        Draw a cubic Bézier curve between the current position and then end position.
        
        :param end_position: The final position of the curve
        :param end_direction: A vector for the tangent at the end of the curve
        :param start_strength: The proportion of the curve which should be influenced by the start direction.
        :param end_strength: The proportion of the curve which should be influenced by the end direction.
        :type end_position: tuple
        :type end_direction: tuple
        :type start_strength: int, float
        :type end_strength: int, float
        """
        p1_dist = start_strength / (start_strength + end_strength)
        p2_dist = end_strength / (start_strength + end_strength)
        end_direction = BlogoUtils.unit_vector(end_direction)
        p0 = np.array(self.turtle.position)
        p3 = np.array(end_position)
        p1 = np.array((p0[0] + p1_dist * self.turtle.fd_vec[0],
                       p0[1] + p1_dist * self.turtle.fd_vec[1],
                       p0[2] + p1_dist * self.turtle.fd_vec[2]
        ))
        p2 = np.array((p3[0] - p2_dist * end_direction[0],
                       p3[1] - p2_dist * end_direction[1],
                       p3[2] - p2_dist * end_direction[2]
        ))
        
        dist = abs(p3[0] - p0[0]) \
             + abs(p3[1] - p0[1]) \
             + abs(p3[2] - p0[2])
        length_incr = self.length_incr
        if (length_incr > dist * self.length_incr_mul):
            length_incr = dist * self.length_incr_mul
        num_steps = 2 + int(float(dist) / length_incr)
        for i in range(num_steps+1):
            t = i / num_steps
            B = (1-t)**3 * p0 \
              + 3*(1-t)**2 * t * p1 \
              + 3*(1-t) * t**2 * p2 \
              + t**3 * p3
            self.set_heading_towards(tuple(B))
            self.set_pos(tuple(B))
            self.fd(0)
            
    def ellipse(self, radius1, radius2, angle=360, steps=None):
        """
        Draw an ellipse starting at radius1 from the centre of the ellipse,
        curving to the extreme radius2 from the centre on the other axis and then looping round

        :param radius1: Distance from centre of ellipse to starting point
        :param radius2: Distance from centre of ellipse to the point on the ellipse at 90°
        :param angle: Number of degrees to go round ellipse (default: complete ellipse)
        :param steps: Number of straight lines to draw the ellipse from (default = angle)
        """


        if (steps == None):
            steps = int(abs(angle))
        turn = 2 * math.pi * (angle/360.0) / steps
        x0 = radius2 * math.cos(math.pi / 2)
        y0 = radius1 * math.sin(math.pi / 2)
        total_turn = 0
        dist = 0
        for t in range(1, steps):
            x1 = radius2 * math.cos(t * turn + math.pi / 2)
            y1 = radius1 * math.sin(t * turn + math.pi / 2)
            x_diff = x1 - x0
            y_diff = y1 - y0
            
            theta = math.atan2(y_diff, -x_diff)
            dist = math.sqrt(x_diff**2 + y_diff**2)
            
            turn_angle = theta - total_turn
            self.left(math.degrees(turn_angle))
            self.fd(dist)
            x0 = x1
            y0 = y1
            total_turn += turn_angle
        self.left(angle - math.degrees(total_turn))
        self.fd(dist)
        
    def fill(self, from_value, to_value, texture, fill_type='relative'):
        """
        Fill the current shape when either finished or the pen is put up.
        
        The gap between the centre of the cross section and the limits from from_value to to_value
        is filled with the given texture.  If fill_type is 'relative' then the limits with be
        a floating point value (generally between 0 and 1) where 0 is the lowest point on the cross
        section and 1 is the highest point.  If the fill_type is 'relative-reversed' then it is the
        same as 'relative', but measured down from the top. If fill_type is 'absolute' then to_value
        and from_value refer to actual measurements from the base of the cross section.  If fill_type
        is 'absolute-reversed' then to_value and from_value refer to actual measurements from the top
        of the cross section.
        
        :param from_value: The bottom vertical position to fill from
        :param to_value: The top vertical position to fill to
        :param texture: The texture to fill with
        :param fill_type: One of 'relative', 'relative-reversed', 'absolute', 'absolute-reversed'
        :return: A mesh object, which can be passed to fill_stop to stop filling.
        """
        fillMesh = FillMesh(self.name, from_value, to_value, fill_type, texture, self.alpha)
        self.fillMeshes.append(fillMesh)
        return fillMesh
    def fill_stop(self, fill_mesh=None):
        """
        Remove either all or one single fill from the current turtle.

        :param fillMesh: The mesh (returned by `fill` to remove, or if `None` then all fills will be removed (default None)
        """
        fillMeshesAfter = []
        for fm in self.fillMeshes:
            if (fill_mesh == None or fill_mesh == fm):
                obj = fm.draw()
                if (obj != None):
                    self.mesh_objects.append(obj)
            else:
                fillMeshesAfter.append(fm)
        self.fillMeshes = fillMeshesAfter
    
    def copy_pos(self, turtle):
        """
        Move the turtle and the orientation to the same as another turtle.
        
        :param turtle: The turtle to copy
        :type turtle: TurtlePosition
        """
        self.turtle.copy(turtle.turtle)
    
    def add_follower(self, turtle):
        """
        Add a follower turtle to this turtle.
        
        Each action which causes a turn or a forward to the current turtle will also be made to the follower turtle

        :param turtle: The turtle who should follow the current turtle.
        :type turtle: Blogo
        """
        self.followers.append(turtle)
    def remove_follower(self, turtle):
        """
        Remove a follower turtle that has been added with `add_follower`

        :param turtle: The turtle who should not follow the current turtle.
        :type turtle: Blogo
        """
        while turtle in self.followers:
            self.followers.remove(turtle)
            
    def get_turtle(self):
        """
        Return a copy of the current turtle position and orientation.

        :return: A copy of the current turtle position
        :rtype: TurtlePosition
        """
        return self.turtle.get_copy()
    def set_turtle(self, turtle):
        """
        Set the turtle position to a copy of turtle

        :param turtle: The turtle to copy
        :type turtle: TurtlePosition
        """
        self.turtle = TurtlePosition(turtle)
        
    def get_path_position(self, pos, units='relative'):
        """
        Get the position that the turtle was in a certain way along the current path.
        
        This can be used to place other objects along the route that this turtle has taken.

        :param pos: A distance along the current path
        :param units: Either 'relative' for pos to be interpretted as the whole path between 0 and 1, or 'absolute' to give a distance along the path.
        :return: A position and orientation of a turtle
        :rtype: TurtlePosition
        """
        if (units == "relative"):
            pos = pos * self.path_length
        for (dist, this_pos) in self.path:
            if (dist >= pos):
                return this_pos
        return None
    
    def get_pos(self):
        """
        Return the current turtle position

        :return: Value of the current position
        :rtype: tuple (x, y, z)
        """
        return self.turtle.position

    def set_pos(self, position, move_type='absolutely-relative'):
        """
        Set the position of the turtle.
        
        If any values in the position tuple are left out or set to None then the current position in
        that axis will be kept.

        :param position: A tuple of the position to move to
        :type position: tuple
        :param move_type: One of 'absolute' (move to that location), 'relative' (move by that much) or 'absolutely-relative' (move to that position, but any followers should move by the relative equivalent)
        """
        
        y = None
        z = None
        if (type(position) == type(int)):
            x = position
        elif (len(position) == 1):
            x, = position
        elif (len(position) == 2):
            x,y = position
        else:
            x,y,z = position
        if (x == None):
            x = self.turtle.position[0] if (move_type != 'relative') else 0
        if (y == None):
            y = self.turtle.position[1] if (move_type != 'relative') else 0
        if (z == None):
            z = self.turtle.position[2] if (move_type != 'relative') else 0

        follower_position = position
        follower_move_type = move_type
        if (move_type == 'absolutely-relative'):
            follower_position = (x - self.turtle.position[0],
                                 y - self.turtle.position[1],
                                 z - self.turtle.position[2],
            )
            follower_move_type = 'relative'
        
        if (move_type == 'relative'):
            x += self.turtle.position[0]
            y += self.turtle.position[1]
            z += self.turtle.position[2]
        
        self.turtle.position = (x, y, z)
        self.history.append(("set_pos", follower_position, follower_move_type))
        for f in self.followers:
            f.set_pos(follower_position, follower_move_type)
            
    def set_xyz(self, x, y, z):
        """
        Set the position of the turtle.

        :param x: The position to set the turtle on the x axis
        :param y: The position to set the turtle on the y axis
        :param z: The position to set the turtle on the z axis
        """
        self.set_pos((x, y, z))
    def set_xy(self, x, y):
        """
        Set the position of the turtle without changing the z axis position

        :param x: The position to set the turtle on the x axis
        :param y: The position to set the turtle on the y axis
        """
        self.set_pos((x, y, None))
    def set_xz(self, x, z):
        """
        Set the position of the turtle without changing the y axis position

        :param x: The position to set the turtle on the x axis
        :param z: The position to set the turtle on the z axis
        """
        self.set_pos((x, None, z))
    def set_yz(self, y, z):
        """
        Set the position of the turtle without changing the x axis position

        :param y: The position to set the turtle on the y axis
        :param z: The position to set the turtle on the z axis
        """
        self.set_pos((None, y, z))
    def set_x(self, x):
        """
        Set the x axis position of the turtle

        :param x: The position to set the turtle on the x axis
        """
        self.set_pos((x, None, None))
    def set_y(self, y):
        """
        Set the y axis position of the turtle

        :param y: The position to set the turtle on the y axis
        """
        self.set_pos((None, y, None))
    def set_z(self, z):
        """
        Set the z axis position of the turtle

        :param z: The position to set the turtle on the z axis
        """
        self.set_pos((None, None, z))
        
    def get_heading(self):
        """
        Returns the heading angle of the turtle, from 0 to 360 degrees.

        :return: The heading of the turtle
        """
        x = self.turtle.fd_vec[0]
        y = self.turtle.fd_vec[1]
        if (x == 0 and y == 0):
            return None
        value = BlogoUtils.normalize_angle(math.degrees(math.atan2(y, x)))
        return value
    def set_heading(self, angle):
        """
        Set the heading angle of the turtle, from 0 to 360 degrees.

        :param angle: The new heading, 0 - 360 or 'north', 'east', 'south', 'west'
        """
        angles = {"north": 0, "east": 90, "south": 180, "west": 270}
        if (angle in angles):
            angle = angles[angle]
        
        cur_angle = self.get_heading()
        self.left(angle - cur_angle)
    def set_heading_vec(self, vec):
        """
        Set the heading to be the same as the given vector

        :param vec: A tuple giving a vector
        """
        left = BlogoUtils.get_projected_angle(vec, self.turtle.fd_vec, self.turtle.up_vec)
        self.left(left)
        
        up = BlogoUtils.get_projected_angle(vec, self.turtle.fd_vec, self.__roll_vec())
        self.up(up)
        
        left = BlogoUtils.get_projected_angle(vec, self.turtle.fd_vec, self.turtle.up_vec)
        self.left(left)
        
    def set_heading_towards(self, coord):
        """
        Set the heading to be towards the given coordinate

        :param coord: A tuple giving a position
        """
        vec = (coord[0] - self.turtle.position[0],
               coord[1] - self.turtle.position[1],
               coord[2] - self.turtle.position[2]
        )
        self.set_heading_vec(vec)
        
    def get_v_heading(self):
        """
        Returns the vertical heading of the turtle, from 0 to 360 degrees.

        :return: The vertical heading of the turtle
        """
        x = self.turtle.up_vec[2]
        y = self.turtle.up_vec[0]
        if (x == 0 and y == 0):
            return None
        value = BlogoUtils.normalize_angle(math.degrees(math.atan2(y, x)))
        return value
    def set_v_heading(self, angle):
        """
        Set the heading of the turtle, from 0 to 360 degrees.

        :param angle: The new vertical heading, 0 - 360 or 'up', 'backward', 'down', 'forward'
        """
        angles = {"up": 0, "backward": 90, "down": 180, "forward": 270}
        if (angle in angles):
            angle = angles[angle]
        
        cur_angle = self.get_v_heading()
        self.up(angle - cur_angle)
    def set_v_heading_vec(self, vec):
        """
        Set the heading to be the same as the given vector

        :param vec: A tuple giving a vector
        """
        self.set_heading_vec(vec)
    def set_v_heading_towards(self, coord):
        """
        Set the heading to be towards the given coordinate

        :param coord: A tuple giving a position
        """
        self.set_heading_towards(coord)
        
    def pen_down(self):
        """
        Put the pen down.
        
        Putting the pen down means that a trail will be left behind the turtle in the shape
        of the current cross section.
        """
        self.history.append(("pen_down", ))
        self.penDown = True
        for cs_name in self.mesh:
            self.mesh[cs_name].needs_start_cap = True
        for f in self.followers:
            f.pen_down()
    def pd(self):
        """
        Put the pen down.
        
        Putting the pen down means that a trail will be left behind the turtle in the shape
        of the current cross section.
        """
        self.pen_down();
    def pen_up(self):
        """
        Put the pen up.
        
        Putting the pen up means that a trail will not be left behind the turtle.
        """
        self.history.append(("pen_up", ))
        self.penDown = False
        for cs_name in self.mesh:
            if (not self.mesh[cs_name].needs_start_cap):
                self.add_end_cap(cs_name)
            self.mesh[cs_name].needs_start_cap = True
        
        for f in self.followers:
            f.pen_up()
    def pu(self):
        """
        Put the pen up.
        
        Putting the pen up means that a trail will not be left behind the turtle.
        """
        self.pen_up();
        
    def label(self, name):
        """
        Insert a named label into the command history
        
        :param name: The name to give the label - for reference in `replay`
        """
        self.history.append(("label", name))
        for f in self.followers:
            f.label(name)
            
    def __check_command_types(allowed_command_types, command):
        command_types = {
            'all': ('left', 'up', 'clockwise', 'tilt_h', 'tilt_v', 'tilt_r', 'forward', 'strafe', 'strafe_v', 'set_pos', 'pen_down', 'pen_up', 'label', 'set_width', 'add_width_func', 'reset_length_counter', 'parse', 'join_objects'),
            'movement': ('forward', 'strafe', 'strafe_v', 'set_pos'),
            'direction': ('left', 'up', 'clockwise', 'tilt_h', 'tilt_v', 'tilt_r'),
            'pen': ('pen_down', 'pen_up'),
            'width': ('set_width', 'add_width_func', 'reset_length_counter'),
        }
        translations = {
            'lt': 'left', 'right': 'left', 'rt': 'left', 'fd': 'forward', 'backward': 'forward', 'bk': 'forward', 
            'set_xyz': 'set_pos', 'set_xy': 'set_pos', 'set_xz': 'set_pos', 'set_yz': 'set_pos', 'set_x': 'set_pos', 'set_y': 'set_pos', 'set_z': 'set_pos',
            'pu': 'pen_up', 'pd': 'pen_down',
            'parse_file': 'parse',
        }
        for command_type in allowed_command_types:
            if (command_type in translations):
                command_type = translations[command_type]
            if (command_type == command):
                return True
            if (command_type in command_types):
                if (command in command_types[command_type]):
                    return True
        return False
        
    def replay(self, turtle, from_label='start', to_label='end', allowed_command_types='all'):
        """
        Replay a number of commands from this turtle in another turtle's context
        
        :param turtle:
        :param from_label:
        :param to_label:
        :param allowed_command_types:
        """
        within_range = False
        if (from_label == 'start'):
            within_range = True
        for h in history:
            if (not within_range and h[0] == "label" and h[1] == from_label):
                within_range = True
            elif (within_range and h[0] == "label" and h[1] == to_label):
                within_range = False
            elif (within_range):
                if (self.__check_command_types(command_types, h[0])):
                    command = h[0] + "("
                    args = []
                    for arg in h[1:]:
                        if (type(arg) == str):
                            args = '"' + arg + '"'
                        else:
                            args += str(arg)
                    command += ",".join(args)
                    command += ")"
                    turtle.parse(command)
    
    def get_texture(self):
        """
        Return the current texture used.

        :return: The current texture
        """
        return self.texture
    def set_texture(self, texture):
        """
        Set a new texture for the cross section to be drawn covered in.
        
        The texture can be a tuple of rgb colours (each in range 0 -> 1), or a named colour
        or an image filename.

        :param texture: The texture to use.
        """
        for cs_name in self.mesh:
            if (not self.mesh[cs_name].is_empty()):
                self.__draw_mesh(cs_name)
                self.__start_mesh(cs_name)
        self.texture = texture
    def set_texture_scale(self, texture_scale):
        """
        Set the texture scale.
        
        When using a image as a texture this will scale the image.  A value of 0 will give an attempt to scale
        the image proportionally to the size of the object.  Any other number will scale the image by that
        amount.  A value of `None` will leave the scale as Blender's default.

        :param texture_scale: The scale factor to use, or 0 for auto.
        """
        self.texture_scale = texture_scale
    def set_fill_texture_scale(self, texture_scale):
        """
        Set the texture scale of the current fill.
        
        When using a image as a fill texture this will scale the image.  A value of 0 will give an attempt 
        to scale the image proportionally to the size of the object.  Any other number will scale the image
        by that amount.  A value of `None` will leave the scale as Blender's default.

        :param texture_scale: The scale factor to use, or 0 for auto.
        """
        for fillMesh in self.fillMeshes:
            fillMesh.set_texture_scale(texture_scale)
    def set_alpha(self, alpha):
        """
        Set the alpha (transparency) value for the current texture.
        
        If a texture is a rgba colour tuple, then this value will be multiplied by the tuple alpha value.

        :param alpha: A value between 0 (completely transparent) and 1 (completely opaque) to set the texture alpha to
        """
        self.alpha = alpha
    def set_unwrap(self, unwrap):
        """
        Sets whether the mesh should be unwrapped before applying the texture.
        
        Some textured Blogo shapes look better with unwrapping on, but it will take longer to create the objects.

        :param unwrap: True or False depending on whether to unwrap the object before applying the texture or not.
        """
        self.unwrap = unwrap
    def set_fill_unwrap(self, unwrap):
        """
        Sets whether the mesh should be unwrapped before applying the texture to the current fill.
        
        Some textured Blogo shapes look better with unwrapping on, but it will take longer to create the objects.

        :param unwrap: True or False depending on whether to unwrap the object before applying the fill texture or not.
        """
        for fillMesh in self.fillMeshes:
            fillMesh.set_unwrap(unwrap)
    def set_smart_project(self, smart_project):
        """
        Sets whether the texture should be smart projected.
        
        Some textured Blogo shapes look better with smart project on, but it will take longer to create the objects.

        :param smart_project: True or False depending on whether to smart project the texture or not.
        """
        self.smart_project = smart_project
    def set_fill_smart_project(self, smart_project):
        """
        Sets whether the fill texture should be smart projected.
        
        Some textured Blogo shapes look better with smart project on, but it will take longer to create the objects.

        :param smart_project: True or False depending on whether to smart project the fill texture or not.
        """
        for fillMesh in self.fillMeshes:
            fillMesh.set_unwrap(smart_project)
        
    def set_cross_section(self, shape, multiplier_h=1.0, multiplier_v=None, name=""):
        """
        Set the cross section shape of the current turtle.
        
        The shape can either be a list of two dimensional points or one of 'square' or 'circleN', where
        N is an integer specifying how many points the circle should be made up of (just 'circle' will
        use a value of N=100).
        
        A 'square' cross section will create a unit square from (-0.5, -0.5) to (0.5, 0.5)

        :param shape: Either a list of points or 'square', 'circle', 'circle10', 'circle500', etc
        :param multiplier_h: A multiplier to multiply the left and right by (default: 1.0)
        :param multiplier_v: A multiplier to multiply the top and bottom by.  If `None` it will use the same value as multiplier_h (default: None)
        :param name: The name of the cross section to change
        """
        for cs_name in self.mesh:
            if (not self.mesh[cs_name].is_empty()):
                self.__draw_mesh(cs_name)
            
        if (multiplier_v == None):
            multiplier_v = multiplier_h

        self.cs_mul_v[name] = multiplier_v
        self.cs_mul_h[name] = multiplier_h
        if (type(shape) == str):
            if (shape == 'square'):
                shape = [(-0.5*multiplier_h, -0.5*multiplier_v),
                         (-0.5*multiplier_h, +0.5*multiplier_v),
                         (+0.5*multiplier_h, +0.5*multiplier_v),
                         (+0.5*multiplier_h, -0.5*multiplier_v)
                ]
            elif (shape.startswith('circle')):
                label = shape[6:]
                if (label == ""):
                    max_i = 100
                else:
                    max_i = int(label)
                shape = []
                for i in range(0, max_i):
                    t = (float(i) / max_i) * 2 * math.pi
                    x = multiplier_h * math.cos(t)
                    y = multiplier_v * math.sin(t)
                    shape.append((x, y))
        else:
            new_shape = []
            for i in shape:
                new_shape.append((i[0] * multiplier_h, i[1] * multiplier_v))
            shape = new_shape
        self.cross_section[name] = shape
        if (name not in self.multipliers):
            self.reset_multipliers(name)
        self.__start_mesh()
        self.__set_cross_section_extremes()
        
    def remove_cross_section(self, name):
        for cs_name in self.mesh:
            if (not self.mesh[cs_name].is_empty()):
                self.__draw_mesh(cs_name)
        
        if (name in self.mesh):
            del self.mesh[name]
        if (name in self.cross_section):
            del self.cross_section[name] 
        if (name in self.multipliers):
            del self.multipliers[name]
        self.__start_mesh()
        self.__set_cross_section_extremes()
    
    def set_length_incr(self, incr, incr_mul=None):
        """
        Set how often any width functions should be called when moving forwards or backwards.
        
        The incr value gives a maximum distance to move before recalculating the width.  The
        incr_mul value gives the maximum proportion of the line to move before recalculating.
        For example, incr=0.1 and incr_mul=0.01 will mean that to draw a line 8 long, incr says
        width must be recalculated every 0.1, but incr_mul says it must be done every 0.08, therefore
        the forward will be done in steps of 0.08.  To draw a line 80 long, incr says it must be
        done in steps of 0.1, but incr_mul says the steps should be no longer than 0.8 - therefore
        the forward will be done in steps of 0.1
        
        If either incr or incr_mul are `None` then their values will not be changed.
        
        :param incr: An absolute maximum length of step before recalulating the width of the line.
        :param incr_mul: A maximum length of step before recalulating the width of the line, relative to the length of the line
        """
        if (incr != None):
            self.length_incr = incr
        if (incr_mul != None):
            self.length_incr_mul = incr_mul
        
    def set_width(self, name, value=1.0, cs_name=""):
        """
        Set one or more of the width modifiers to a named value.
        
        If only a number parameter is supplied then it will set both left and right to that
        multiplier.

        :param name: The name or names of the sides to set, or a value to set left and right to if a number
        :param value: The value to set the modifier to.  The cross section distance from the middle is multiplied by this value
        :param cs_name: The name of the cross section affected (default="")
        """
        self.history.append(("set_width", name, value))
        if (type(name) == int or type(name) == float):
            value = name
            name = ("left", "right")
        if (type(name) == str):
            name = (name,)
        
        for n in name:
            n = self.__translate_direction_name(n)
            if (BlogoUtils.is_sequence(n)):
                self.set_width(n, value, cs_name)
            else:
                self.multipliers[cs_name][n] = value
        self.__set_cross_section_extremes()
    def set_height(self, name, value=1.0, cs_name=""):
        """
        Set one or more of the width modifiers to a named value.
        
        If only a number parameter is supplied then it will set both above and below to that
        multiplier.

        :param name: The name or names of the sides to set, or a value to set above and below to if a number
        :param value: The value to set the modifier to.  The cross section distance from the middle is multiplied by this value
        :param cs_name: The name of the cross section affected (default="")
        """
        if (type(name) == int or type(name) == float):
            value = name
            name = ("above", "below")
        self.set_width(name, value, cs_name) 
    def get_width(self, direction, cs_name="", loopCount=10):
        """
        Get the width modifier for a particular direction.

        :param direction: One of 'left', 'right', 'above' or 'below'
        :param cs_name: The name of the cross section affected (default="")
        """
        if (loopCount <= 0):
            raise RuntimeError("Width look up caused loop '"+direction+"'")
        value = self.multipliers[cs_name][direction]
        if (type(value) == int or type(value) == float):
            return value
        return self.get_width(value, cs_name, loopCount-1)
    def __translate_direction_name(self, name):
        if (name == "all"):
            return ("left", "right", "above", "below")
        if (name == "sides"):
            return ("left", "right")
        if (name == "verticals"):
            return ("above", "below")
        return name
    def __has_width_funcs(self, cs_name=None):
        if (cs_name == None):
            cs_name = self.width_func.keys()
        elif (not BlogoUtils.is_sequence(cs_name)):
            cs_name = (cs_name,)
        for n in ("above", "below", "left", "right"):
            for name in cs_name:
                if n in self.width_func[name]:
                    if (self.width_func[name][n] != None and len(self.width_func[name][n]) > 0):
                        return True
        return False
    def __set_defaults(args, **kwargs):
        for key in kwargs:
            if key not in args:
                args[key] = kwargs[key]
                
    def add_width_func(self, name, func=None, cs_name="", **kwargs):
        """
        Add either a width function to a side

        :param name: The side of the cross section to deal with.  This can be a single side, ('left', 'right', 'above', 'below') or it can be a list of those sides or it can be a description of multiple sides ('sides', 'verticals', 'all')
        :param func: The function to add, or `None` to remove all functions
        :param kwargs: User data to pass on to the function when called
        """
        self.history.append(("add_width_func", name, func, cs_name, kwargs))
        name = self.__translate_direction_name(name)
        if (func == "curve_start"):
            func = Blogo.curve_start
            Blogo.__set_defaults(kwargs, eccentricity=1, curve_length=0.5, curve_width=0)
        elif (func == "curve_end"):
            func = Blogo.curve_end
            Blogo.__set_defaults(kwargs, eccentricity=1, curve_length=0.5, curve_width=0)
        if (BlogoUtils.is_sequence(name)):
            for n in name:
                self.add_width_func(n, func, cs_name, **kwargs)
            return
        if (func == None):
            self.width_func[cs_name][name] = []
            self.width_args[cs_name][name] = []
        else:
            if cs_name not in self.width_func:
                self.width_func[cs_name] = {}
                self.width_args[cs_name] = {}
            if name not in self.width_func[cs_name]:
                self.width_func[cs_name][name] = []
                self.width_args[cs_name][name] = []
            self.width_func[cs_name][name].append(func)
            self.width_args[cs_name][name].append(kwargs)
    def remove_width_func(self, name, func, remove_all=True):
        """
        Remove either a specific width function from a side, or remove all width functions from that side.

        :param name: The side of the cross section to deal with.  This can be a single side, ('left', 'right', 'above', 'below') or it can be a list of those sides or it can be a description of multiple sides ('sides', 'verticals', 'all')
        :param func: The function to remove, or `None` to remove all functions
        :param remove_all: If `True` then if a function has been added more than once then all will be removed, otherwise only the first occurance will be. (default: True)
        """
        name = self.__translate_direction_name(name)
        if (BlogoUtils.is_sequence(name)):
            for n in name:
                self.remove_width_func(n, func)
            return
        while (func in self.width_func[name] or func==None):
            i = self.width_func[name].index(func)
            del self.width_func[name][i]
            del self.width_args[name][i]
            if (not remove_all):
                break
    def add_gap(self, name, start_height, end_height, widths1=('above', 'left', 'right'), widths2=('below', 'left', 'right'), gap_cs_shape='square', cs_splitting=""):
        """
        Add a window in the middle of a cross section
        
        The gap is made by squashing the original cross section to the bottom and adding in a new cross section above.
        
        :param name: The name of the new cross section area
        :param start_height: The height of the bottom of the gap
        :param end_height: The height of the top of the gap
        :param widths1: The edges of the original cross section to copy into the new cross section (default ('above', 'left', 'right') - i.e. the new cross section goes at the top, with the same width)
        :param widths2: The edges of the original cross section to leave in the original cross section (default ('below', 'left', 'right') - i.e. the original cross section goes at the bottom, with the same width)
        :param gap_cs_shape: Cross section shape to make the additional cross section (Default: 'square')
        :param cs_splitting: The name of the cross section to split.  (Default "", i.e. the main cross section)
        """

        all_directions = ('above', 'below', 'left', 'right')
        
        turtle.set_cross_section(gap_cs_shape, self.cs_mul_h[cs_splitting], self.cs_mul_v[cs_splitting], name)
        self.width_func[name] = {}
        self.width_args[name] = {}
        # First copy existing widths to new cross section
        for direction in widths1:
            turtle.set_width(direction, self.multipliers[cs_splitting][direction], name)
            if ((cs_splitting in self.width_func) and (direction in self.width_func[cs_splitting])):
                self.width_func[name][direction] = self.width_func[cs_splitting][direction]
                self.width_args[name][direction] = self.width_args[cs_splitting][direction]
                
        # Then remove no longer needed widths from existing cross section
        for direction in all_directions:
            if (direction not in widths2):
                self.multipliers[cs_splitting][direction] = 1
                if ((cs_splitting in self.width_func) and (direction in self.width_func[cs_splitting])):
                    self.width_func[cs_splitting][direction] = []
                    self.width_args[cs_splitting][direction] = []
        
        # Finally set new widths at gap edges
        # TODO: Add different types of position_types here
        gap_top_dirs = BlogoUtils.list_missing(all_directions, widths1)
        gap_bottom_dirs = BlogoUtils.list_missing(all_directions, widths2)
        
        all_top_dirs = BlogoUtils.list_missing(widths2, widths1)
        all_bottom_dirs = BlogoUtils.list_missing(widths1, widths2)
        
        for direction in gap_top_dirs:
            turtle.set_width(direction, -end_height, name)
        for direction in gap_bottom_dirs:
            turtle.set_width(direction, start_height, cs_splitting)
                    
        self.gap_widths[name] = (widths1, widths2, cs_splitting)

    def remove_gap(self, name):
        """
        Remove a gap that has been previously added by`add_gap`
        
        :param name: The name of the gap to remove
        """
        
        if (name in self.gap_widths):
            widths1, widths2, cs_split = self.gap_widths[name]
            for direction in BlogoUtils.list_missing(widths1, widths2):
                turtle.set_width(direction, self.multipliers[name][direction], cs_split)
                if ((name in self.width_func) and (direction in self.width_func[name])):
                    self.width_func[cs_split][direction] = self.width_func[name][direction]
                    self.width_args[cs_split][direction] = self.width_args[name][direction]
        self.remove_cross_section(name)
                
                
    def reset_length_counter(self, name, include_bk=-1, include_pu=False, value=0.0):
        """
        Reset a value used by a length counter
        
        Sets the given length counter to value, specifies how backward movements should be treated,
        and whether the counter should be increased when the pen is up.
        
        :param name: The name of the length counter to reset
        :param include_bk: 0 to ignore backwards movements, 1 to include backwards movements, -1 to subtract backwards movements
        :param include_pu: True to increase the counter when the pen is up, False to leave the counter when the pen is up
        :param value: The value to reset the counter to.
        :type name: string
        :type include_bk: int
        :type include_pu: bool
        :type value: int, float
        """
        self.history.append(("reset_length_counter", name, include_bk, include_pu, value))
        self.length_counters[name] = (value, include_bk, include_pu)
    def __update_length_counters(self, flip, length_incr):
        for name in self.length_counters:
            value, include_bk, include_pu = self.length_counters[name]
            if (flip > 0 or include_bk != 0):
                if (self.penDown or include_pu):
                    if (flip < 0 and include_bk < 0):
                        value -= length_incr
                    else:
                        value += length_incr
            self.length_counters[name] = (value, include_bk, include_pu)
            
    def get_length_counter(self, name):
        """
        Get the length counter specified by name
        
        :param name: The name of the length counter to return
        :type name: string
        :returns: None if the length counter does not exist, otherwise the value of the counter
        """
        if (name not in self.length_counters):
            return None
        return self.length_counters[name][0]
        
    def __get_width_adjustment(self, cs_name, name):
        if (not cs_name in self.width_func):
            return []
        if (not name in self.width_func[cs_name]):
            return []
        retval = []
        for i in range(0, len(self.width_args[cs_name][name])):
            func = self.width_func[cs_name][name][i]
            args = self.width_args[cs_name][name][i]
            for lc_name in self.length_counters:
                args[lc_name] = self.length_counters[lc_name][0]
            args["relative_length"] = self.relative_length
            retval.append(func(args))
        return retval
    def __set_cross_section_extremes(self):
        self.crossSectionHighest = None
        self.crossSectionLowest = None
        for cs_name in self.cross_section:
            for cs in self.cross_section[cs_name]:
                y = cs[1]
                if (y < 0):
                    y *= self.get_width("below", cs_name)
                else:
                    y *= self.get_width("above", cs_name)
                if ((self.crossSectionHighest is None) or (y > self.crossSectionHighest)):
                    self.crossSectionHighest = y
                if ((self.crossSectionLowest is None) or (y < self.crossSectionLowest)):
                    self.crossSectionLowest = y
                
    
    def __draw_mesh(self, cs_name=None):
        mesh_list = []
        if (cs_name in self.mesh):
            mesh_list.append(cs_name)
        elif (cs_name == None):
            mesh_list = self.mesh.keys()
        for mesh_name in mesh_list:
            if (not self.mesh[mesh_name].is_empty()):
                if (self.penDown):
                    self.add_end_cap(mesh_name)
                    self.mesh[mesh_name].needs_start_cap = True
                
                obj = self.mesh[mesh_name].draw(self.name, self.texture, self.alpha, self.unwrap, self.smart_project, self.texture_scale)
                if (obj != None):
                    self.mesh_objects.append(obj)

        for fillMesh in self.fillMeshes:
            obj = fillMesh.draw()
            if (obj != None):
                self.mesh_objects.append(obj)
        self.__start_mesh(cs_name)
    def __start_mesh(self, cs_name=None):
        if (cs_name == None):
            cs_name = self.cross_section.keys()
        else:
            cs_name = (cs_name, )
        for name in cs_name:
            self.mesh[name] = Mesh()
        
            self.lastPointInserted[name] = None
            self.last3DVertices[name] = None
            self.skipped_point[name] = None
        
        newFillMeshes = []
        try:
            for fm in self.fillMeshes:
                fillMesh = FillMesh(self.name, fm.from_value, fm.to_value, fm.fill_type, fm.texture, self.alpha)
                fillMesh.unwrap = fm.unwrap
                fillMesh.smart_project = fm.smart_project
                newFillMeshes.append(fillMesh)
        except AttributeError:
            pass
        self.fillMeshes = newFillMeshes
        
        
    def __do_adjustment(self, cs_name, value, direction, direction_name):
        # First apply static width multipliers
        value *= self.get_width(direction_name, cs_name)
        
        # Then apply width function
        adj_list = self.__get_width_adjustment(cs_name, direction_name)
        
        for adj in adj_list:
            if (not BlogoUtils.is_sequence(adj)):
                adj = (adj, direction)
            adj_value = adj[0]
            adj_op = adj[1]
            if (adj_op == "+-"):
                adj_op = direction
            
            if (adj_op == "+"):
                value += adj_value
            elif (adj_op == "-"):
                value -= adj_value
            elif (adj_op == "*"):
                value *= adj_value
            elif (adj_op == "/"):
                value /= adj_value
            elif (adj_op == "="):
                value = adj_value
        return value
        
    def __insert_cross_section(self, lastPoint=True):
        if (not self.penDown):
            return
        for cs_name in self.cross_section:
            cross_section = self.cross_section[cs_name]
            numCSVertices = len(cross_section)
            points = []
            
            for i in range(0, numCSVertices):
                x = cross_section[i][0]
                if (x < 0):
                    x = self.__do_adjustment(cs_name, x, "-", "left")
                else:
                    x = self.__do_adjustment(cs_name, x, "+", "right")
                y = cross_section[i][1]
                if (y < 0):
                    y = self.__do_adjustment(cs_name, y, "-", "below")
                else:
                    y = self.__do_adjustment(cs_name, y, "+", "above")
                roll_vec = self.__roll_vec()
                up_vec = BlogoUtils.rotate_axis(roll_vec, self.turtle.up_vec, self.turtle.tilt_v_angle)
                fd_vec = BlogoUtils.rotate_axis(roll_vec, self.turtle.fd_vec, self.turtle.tilt_v_angle)
                
                roll_vec = BlogoUtils.rotate_axis(self.turtle.up_vec, roll_vec, self.turtle.tilt_h_angle)
                fd_vec = BlogoUtils.rotate_axis(self.turtle.up_vec, fd_vec, self.turtle.tilt_h_angle)
                
                up_vec = BlogoUtils.rotate_axis(self.turtle.fd_vec, up_vec, self.turtle.tilt_r_angle)
                roll_vec = BlogoUtils.rotate_axis(self.turtle.fd_vec, roll_vec, self.turtle.tilt_r_angle)
                
                
                point = (roll_vec[0] * x + up_vec[0] * y,
                         roll_vec[1] * x + up_vec[1] * y,
                         roll_vec[2] * x + up_vec[2] * y
                )
                points.append(point)
            if (cs_name in self.lastPointInserted and
                    points == self.lastPointInserted[cs_name] and 
                    not lastPoint):
                self.skipped_point[cs_name] = (self.turtle.position, points)
                return
            
            if (cs_name in self.skipped_point and self.skipped_point[cs_name] != None):
                self.__insert_3d_points(cs_name, self.skipped_point[cs_name][0], self.skipped_point[cs_name][1])
                self.skipped_point[cs_name] = None
            self.__insert_3d_points(cs_name, self.turtle.position, points)
            self.lastPointInserted[cs_name] = points
                
    def __insert_3d_points(self, cs_name, position, points):
        position = tuple(np.add(position, Blogo.__origin))
        position = tuple(np.add(position, self.__local_origin))
        
        numVerticesBefore = self.mesh[cs_name].vertex_count()
        numCSVertices = len(self.cross_section[cs_name])
        i = 0
    
        newVertices = []
        for point in points:
            newVertices.append(tuple(np.add(position, point)))
        if (cs_name in self.last3DVertices and newVertices == self.last3DVertices[cs_name]):
            return
        lastVertices = self.last3DVertices[cs_name]
        self.last3DVertices[cs_name] = newVertices
        
        for newVertex in newVertices:
            self.mesh[cs_name].append_vertex(newVertex)
            
            if (not self.mesh[cs_name].needs_start_cap):
                im = i
                if (i == (numCSVertices-1)):
                    im = i - numCSVertices
                newFace = [i + numVerticesBefore - numCSVertices,
                           im + numVerticesBefore - numCSVertices + 1,
                           im + numVerticesBefore + 1,
                           i + numVerticesBefore
                ]
                self.mesh[cs_name].append_face(newFace)
            i += 1
        if (self.mesh[cs_name].needs_start_cap):
            self.add_start_cap(cs_name)
        if (cs_name == ""):
            for fillMesh in self.fillMeshes:
                high = self.crossSectionHighest
                low = self.crossSectionLowest
                if (fillMesh.fill_type == "relative"):
                    y = (low + (high-low)*fillMesh.from_value)
                elif (fillMesh.fill_type == "relative-reversed"):
                    y = (high - (high-low)*fillMesh.from_value)
                elif (fillMesh.fill_type == "absolute"):
                    y = (low + fillMesh.from_value)
                elif (fillMesh.fill_type == "absolute-reversed"):
                    y = (high - fillMesh.from_value)
                point = (self.turtle.up_vec[0] * y,
                         self.turtle.up_vec[1] * y,
                         self.turtle.up_vec[2] * y
                )
                newVertexFrom = tuple(np.add(position, point))
                
                if (fillMesh.fill_type == "relative"):
                    y = (low + (high-low)*fillMesh.to_value)
                elif (fillMesh.fill_type == "relative-reversed"):
                    y = (high - (high-low)*fillMesh.to_value)
                elif (fillMesh.fill_type == "absolute"):
                    y = (low + fillMesh.to_value)
                elif (fillMesh.fill_type == "absolute-reversed"):
                    y = (high + fillMesh.to_value)
                point = (self.turtle.up_vec[0] * y,
                         self.turtle.up_vec[1] * y,
                         self.turtle.up_vec[2] * y
                )
                newVertexTo = tuple(np.add(position, point))
                
                fillMesh.append_vertices(newVertexFrom, newVertexTo)
    def add_start_cap(self, cs_name=""):
        """
        Put in a cap in the shape of the current cross section, facing backwards
        """
        self.add_cap(True, cs_name)
    def add_end_cap(self, cs_name=""):
        """
        Put in a cap in the shape of the current cross section, facing forwards
        """
        self.add_cap(False, cs_name)
    def add_cap(self, is_start_cap, cs_name=""):
        """
        Put in a cap in the shape of the current cross section, facing forwards or backwards

        :param is_start_cap: If `True` then the cap will face backwards, otherwise forwards
        """
        # if start_cap add 
        endFace = []
        numVertices = len(self.cross_section[cs_name])
        
        start = self.mesh[cs_name].vertex_count() - numVertices
        for i in range(numVertices):
            endFace.append(start + i)
        if (is_start_cap):
            endFace.reverse()
            self.mesh[cs_name].needs_start_cap = False
        self.mesh[cs_name].append_face(endFace)
    
    def parse(self, text, var=None, var_name="var"):
        """
        This will parse a block of text and then execute it.
        
        Any function used which is a member function in Blogo will be modified to run in the context
        of this turtle.  Any brackets missing around member functions arguments will be added.
        Thus::
        
            turtle.parse("fd 10; rt 90; fd 10; rt 90") 
        
        will be executed as::
        
            turtle.fd(10)
            turtle.rt(90)
            turtle.fd(10)
            turtle.rt(90)
            
        The argument `var` can be a dictionary used to pass in variables and have the code block read 
        and modify them, with `var_name` specifying what name the dictionary is refered to by in the
        code block. e.g.::
        
            data["size"] = 10
            turtle.parse('fd data["size"];rt 90;fd data["size"]', data, "data")
            
        Will move forward 10, turn right, then move forward 10 again.
        
        Any valid python can be passed in to the code block, but could get fragile if too much code 
        is passed in.

        :param text: Block of code to parse
        :param var: Dictionary to be able to get and set variables in code block
        :param var_name: Name of the variable used to hold the dictionary in the code block
        """
        self.history.append(("parse", text, var, var_name))
        if (var == None):
            var = {}
        before_command = True
        in_command = False
        after_command = False
        add_brackets = None
        new_text = ""
        command = ""
        after_text = ""
        for ch in text + ";":
            if (before_command):
                if (not (ch.isalnum() or ch == "_")):
                    new_text += ch
                else:
                    before_command = False
                    in_command = True
                    command += ch
            elif (in_command):
                if (ch.isalnum() or ch == "_"):
                    command += ch
                else:
                    in_command = False
                    after_command = True
                    func = getattr(self, command, None)
                    if (func != None):
                        command = "self."+command
                        add_brackets = None
                    else:
                        add_brackets = False
                    new_text += command
            elif (after_command):
                if (ch == ";" or ch == "\r" or ch == "\n"):
                    if (add_brackets == None):
                        add_brackets = True
                    if (add_brackets):
                        new_text += "("
                    new_text += after_text
                    if (add_brackets):
                        new_text += ")"
                    new_text += ch
                    after_command = False
                    before_command = True
                    command = ""
                    after_text = ""
                    add_brackets = None
                else:
                    if (add_brackets == None and not ch.isspace()):
                        if (ch == "("):
                            add_brackets = False
                        else:
                            add_brackets = True
                        after_text += ch
                    else:
                        after_text += ch
        new_text = new_text.replace(var_name, "var")
        exec(new_text)
        
        for f in self.followers:
            f.parse(text, var, var_name)
        
    def parse_file(self, file, var=None, var_name="var"):
        """
        Open a file and call `parse` with the contents of the file

        :param file: Name of file containing a block of code to parse
        :param var: Dictionary to be able to get and set variables in code block
        :param var_name: Name of the variable used to hold the dictionary in the code block
        """
        fh = open(file)
        text = fh.read()
        fh.close()
        self.parse(text, var, var_name)
        
    def join_objects(self, union=False):
        """
        Join the underlying blender objects of this turtle into one object

        :param union: If `True` the joined objects will be merged into one block with a binary operation, otherwise they will be separatable by using unjoin.
        """
        self.history.append(("join_objects", union))
        objects = self.get_objects()
        for fillMesh in self.fillMeshes:
            objects.append(fillMesh.get_object())
        if (len(objects) <= 1):
            return
            
        if (union):
            BlogoUtils.boolean_op(objects[0], "UNION", objects[1:])
        else:
            BlogoUtils.join_objects(objects)

    def curve_start(args):
        eccentricity = args["eccentricity"]
        curve_width = args["curve_width"]
        curve_length = args["curve_length"]
        length_along = args["relative_length"]
        
        if (length_along > curve_length):
            width = 1
        else:
            length_along /= curve_length
            circle_width = math.sqrt(1 - (1-length_along)**2)
            circle_width = curve_width + (1 - curve_width) * circle_width
            if (abs(eccentricity) == 1):
                width = circle_width * eccentricity
            elif (abs(eccentricity) > 1):
                width = -1 + 2 * (eccentricity + circle_width) / (eccentricity + 1)
            else:
                straight_width = length_along * (1 - curve_width) + curve_width
                width = eccentricity * circle_width + (1-eccentricity) * straight_width
        return (width, "*")
    def curve_end(args):
        orig_relative_length = args["relative_length"]
        args["relative_length"] = 1 - args["relative_length"]
        retval = Blogo.curve_start(args)
        args["relative_length"] = orig_relative_length
        return retval
        
def register():
    pass

def unregister():
    pass

if __name__ == "__main__":
    register()