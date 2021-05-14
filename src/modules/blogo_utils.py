#exec(open("C:\\dev\\blender\\blogo\\src\\blogo.py").read())

import bpy
import math
import mathutils
import numpy as np
import runpy

#exec(open("C:\\dev\\blender\\blogo\\src\\blogo_colours.py").read())
import blogo_colours
import blogo

# TODO
#  Clean up functions
#  Add config file reading (with defaults and options)
#  Use contexts to stop updating real scene everytime, instead only link at end
#  Add ability to set cross section from logo?
#  Add fd_rt() and fd_lt() which go forward by dist - cs_width, then slowly arc before subtracting cs_width off the next fd to give a smooth turn
#  Investigate being able to copy another turtle, but add in other commands, eg:
#       turtle1.fd(10), turtle1.rt(90), turtle1.fd(10), turtle1.add_stop("first"), turtle1.fd(10), turtle1.circle(10), turtle1.add_stop("second"), turtle1.fd(10)
#       turtle2.pu(), turtle2.replay_to_stop(turtle1, "first"), turtle2.pd(), turtle2.replay_to_stop(turtle1, "second")
#  Cross section from image

def dump(obj):
    """
    Helper function to print what is inside a python object
    """
    for attr in dir(obj):
        try:
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
        except:
            print("fail on "+str(attr))

last_run_file = None
def run(file=None, **kwargs):
    """
    Run a python script specified by file

    :param file: The name of the file to load, or `None` to reload the last file loaded
    :param kwargs: User data which can be used by the script.
    """
    global last_run_file
    if (file == None):
        file = last_run_file
    last_run_file = file
    #exec(open(file).read(), globals(), locals())
    globs = runpy.run_path(file, globals())
    for key in globs:
        globals()[key] = globs[key]
    blogo.Blogo.clean_up()

def show(file=None, **kwargs):
    """
    Run a python script specified by file and then show the rendered results

    :param file: The name of the file to load, or `None` to reload the last file loaded
    :param kwargs: User data which can be used by the script.
    """
    run(file, **kwargs)
    BlogoUtils.unselect_objects()
    BlogoUtils.show_objects()

class BlogoUtils:
    """
    A class of useful helper functions to be used when programming with Blender
    """
    __objcounter = 0
    __nullnparray = np.array((0,0,0))
    
    def is_sequence(var):
        """
        Tell whether a variable is a sequence, i.e. a list or tuple
        """
        return (type(var) == tuple or type(var) == list or type(var) == type(BlogoUtils.__nullnparray))
        
    def object_counter():
        """
        Return a unique number
        """
        BlogoUtils.__objcounter += 1
        return BlogoUtils.__objcounter
        
    def start_fresh(leave_types=[]):
        """
        Delete everything, so that we can start again
        """
        BlogoUtils.remove_data_block(bpy.data.meshes)
        BlogoUtils.remove_data_block(bpy.data.materials)
        BlogoUtils.remove_data_block(bpy.data.textures)
        BlogoUtils.remove_data_block(bpy.data.images)
        BlogoUtils.remove_data_block(bpy.data.lights)
        BlogoUtils.remove_data_block(bpy.data.cameras)
        BlogoUtils.remove_data_block(bpy.data.actions)
        BlogoUtils.remove_data_block(bpy.data.node_groups)
        BlogoUtils.remove_data_block(bpy.data.objects)
        BlogoUtils.clear_info()
        
    def remove_data_block(data, only_orphans=False):
        for block in data:
            if ((not only_orphans) or (block.users == 0)):
                data.remove(block)
        return
    def clear_info():
        """
        Clear all lines from the info screen
        """
        prev_ui_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'INFO'
        bpy.ops.info.select_all()
        bpy.ops.info.report_delete()
        bpy.context.area.ui_type = prev_ui_type

    def copy_object(objects, location, relative_location=True, copy_mesh=True):
        """
        Copy an object and insert it into a new location
        """
        if (not BlogoUtils.is_sequence(objects)):
            objects = (objects,)
        #sce = bpy.context.scene
        copies = []

        for object in objects:
            copy = object.copy()
            if (relative_location):
                copy.location[0] += location[0]
                copy.location[1] += location[1]
                copy.location[2] += location[2]
            else:
                copy.location = location.copy()
                
            if (copy_mesh):
                copy.data = copy.data.copy()
            
            bpy.context.collection.objects.link(copy)
            copies.append(copy) 

        #sce.update() 
        return copies
        
    def join_objects(objects):
        """
        Join multiple objects together
        """
        #scene = bpy.context.scene

        ctx = bpy.context.copy()

        # one of the objects to join
        ctx['active_object'] = objects[0]

        ctx['selected_editable_objects'] = objects

        bpy.ops.object.join(ctx)
    def mode_set(mode):
        """
        Set the given mode, e.g. "OBJECT" or "EDIT"
        """
        try:
            bpy.ops.object.mode_set(mode=mode)
        except:
            # need to stop this from ever getting an exception
            pass
            
    def list_missing(full_list, partial_list):
        """
        Return the items that are in full_list, but not in partial_list
        
        e.g. list_missing((1, 2, 3, 4), (1, 3, 5)) ==> (2, 4)
        
        :param full_list: The full list of items
        :param partial_list: full_list with some items missing
        :returns: The difference between the lists
        """
        missing_list = []
        for item in full_list:
            if (item not in partial_list):
                missing_list.append(item)
        return missing_list
        
    def rotation_matrix(axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
                         
    def rotate_axis(axis, vec, angle):
        """
        Rotate a vector around an axis by an angle in degrees
        """
        if (angle == 0):
            return vec
        return np.dot(BlogoUtils.rotation_matrix(axis, math.radians(angle)), vec)
        
    def normalize_angle(angle):
        """
        Return an angle between 0 and 360 giving the same heading as angle
        """
        while (angle < 0):
            angle += 360
        while (angle >= 360):
            angle -= 360
        return angle
        
    def dot_product(a, b):
        """
        Return the dot product of two vectors
        """
        return sum([a[i] * b[i] for i in range(len(a))])
    def cross_product(a, b):
        """
        Return the cross product of two vectors
        """
        x = a[1]*b[2] - a[2]*b[1]
        y = a[2]*b[0] - a[0]*b[2]
        z = a[0]*b[1] - a[1]*b[0]
        return (x, y, z)

    def norm(vec):
        """
        Return the norm of the vector
        """
        return math.sqrt(BlogoUtils.dot_product(vec, vec))

    def normalize(vec):
        """
        Normalise a vector
        """
        return [vec[i] / BlogoUtils.norm(vec) for i in range(len(vec))]

    def project_onto_plane(vec, normal):
        """
        Project a vector onto a plane defined by a normal to that plane
        """
        unit_normal = BlogoUtils.normalize(normal)
        return BlogoUtils.cross_product(normal, BlogoUtils.cross_product(vec, normal))
        
    def unit_vector(vector):
        """
        Returns the unit vector of a vector
        """
        return vector / np.linalg.norm(vector)

    def angle_between(a, b):
        """
        Return the angle between two vectors
        """
        return math.atan2(BlogoUtils.norm(BlogoUtils.cross_product(a,b)), BlogoUtils.dot_product(a,b))
    def line_length(line):
        """
        Return the length of a line
        """
        total = 0
        for part in line:
            total += part * part
        return math.sqrt(total)
    def get_projected_angle(vec, vec_on_plane, plane_normal):
        """
        Get the angle between the component of vector on a plane and a vector on that plane
        """
        EPS = 0.0001
        angle = 0
        p = BlogoUtils.project_onto_plane(vec, plane_normal)
        if (BlogoUtils.line_length(p) > EPS):
            angle = math.degrees(BlogoUtils.angle_between(p, vec_on_plane))
        return angle
    
    def add_locations(location1, location2, mul2=1, mul1=1):
        """
        Add two locations or vectors together
        """
        return (mul1 * location1[0] + mul2 * location2[0],
                mul1 * location1[1] + mul2 * location2[1],
                mul1 * location1[2] + mul2 * location2[2])
        
    def unselect_objects():
        """
        Unselect all objects
        """
        bpy.ops.object.select_all(action='DESELECT')
        
    def select_objects():
        """
        Select all objects
        """
        bpy.ops.object.select_all(action='SELECT')
    
    def show_objects():
        """
        Move to the screen showing rendered objects
        """
        bpy.context.area.ui_type = 'VIEW_3D'
        bpy.context.space_data.shading.type = 'RENDERED'
        
    def create_object(objname, vertices, faces):
        """
        Create an object from a list vertices and faces
        """       
        mesh = bpy.data.meshes.new(objname)

        obj = bpy.data.objects.new(objname, mesh)

        bpy.context.collection.objects.link(obj)

        # Generate mesh data
        mesh.from_pydata(vertices, [], faces)

        # Calculate the edges
        mesh.update(calc_edges=True)
        
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True);
        bpy.context.view_layer.objects.active = obj
        BlogoUtils.mode_set('EDIT')
        bpy.ops.mesh.vert_connect_concave()
        BlogoUtils.mode_set('OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

        return (obj, mesh)
        
    def select_object(obj, mode='EDIT'):
        """
        Select a single object and move into a new mode
        """
        
        current_mode = bpy.context.object.mode
        if (mode == None):
            mode = current_mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True);
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode=mode)
        return current_mode
    def unselect_object(obj, prev_mode=None):
        """
        Unselect an object
        """
        if (prev_mode == None):
            prev_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(False);
        bpy.ops.object.mode_set(mode=prev_mode)
        
    def unwrap_object(obj):
        """
        Run UV unwrap for an object
        """
        current_mode = BlogoUtils.select_object(obj)
        bpy.ops.uv.unwrap()
        BlogoUtils.unselect_object(obj, current_mode)
        
    def smart_project_object(obj):
        """
        Run smart project for an object
        """
        current_mode = BlogoUtils.select_object(obj)
        bpy.ops.uv.smart_project()
        BlogoUtils.unselect_object(obj, current_mode)

    def add_texture(obj, textureFile, alpha=1.0, unwrap=False, smart_project=False, texture_scale=None):
        """
        Add texture to an object
        """
        uv_coord_type = "Generated"
        
        colours = blogo_colours.all_colours()
        if (type(textureFile) == tuple or textureFile in colours):
            name = "Mat-"+str(textureFile);
            if (textureFile in colours):
                textureTuple = colours[textureFile]
            else:
                textureTuple = textureFile
                while (len(textureTuple) < 4):
                    textureTuple += (1.0,)
                

            material = bpy.data.materials.get(name)
            if material is None:
                material = bpy.data.materials.new(name)
            material.use_nodes = True
            principled_bsdf = material.node_tree.nodes['Principled BSDF']
            if principled_bsdf is not None:
                principled_bsdf.inputs[0].default_value = textureTuple
            alpha *= textureTuple[3]
            if (alpha < 1):
                obj.show_transparent = True
                material.blend_method = 'BLEND'
                principled_bsdf.inputs[18].default_value = alpha
            obj.active_material = material
            
            
            return obj

        name = "Mat-"+textureFile + "-" + str(texture_scale) + str(unwrap)
        if (smart_project):
            name += str(BlogoUtils.object_counter())
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(textureFile)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

            if (texture_scale != None and texture_scale != 1):
                mapping = mat.node_tree.nodes.new('ShaderNodeMapping')
            
                mat.node_tree.links.new(texImage.inputs['Vector'], mapping.outputs['Vector'])
                
                
                mapping.inputs[3].default_value[0] = texture_scale
                mapping.inputs[3].default_value[1] = texture_scale
                mapping.inputs[3].default_value[2] = texture_scale            
            else:
                mapping = texImage
            
            if not unwrap:
                tex_coordinate = mat.node_tree.nodes.new("ShaderNodeTexCoord")
                outputs = tex_coordinate.outputs['Generated']
                mat.node_tree.links.new(mapping.inputs['Vector'], outputs)
            else:
                uv_coord_type = "UV"
                tex_coordinate = mat.node_tree.nodes.new("ShaderNodeTexCoord")
                outputs = tex_coordinate.outputs['UV']
                mat.node_tree.links.new(mapping.inputs['Vector'], outputs)
            mat.node_tree.links.new(mapping.inputs['Vector'], tex_coordinate.outputs[uv_coord_type])
                
            if (alpha < 1):
                obj.show_transparent = True
                mat.blend_method = 'BLEND'
                bsdf.inputs[18].default_value = alpha
        
        # Assign it to object
        if len(obj.data.materials) > 0:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        for f in obj.data.polygons:
            f.material_index = 0
            f.select = True

        obj.data.update()
        
        if unwrap:
            BlogoUtils.unwrap_object(obj)
            
        if smart_project:
            BlogoUtils.smart_project_object(obj)
        
        return obj
        
    def draw_mesh(objname, vertices, faces, textureFile, alpha=1.0, unwrap=False, smart_project=False, texture_scale=None):
        """
        Create an object from the given lists of vertices and faces and with the given texture
        """
        objname = objname+"-"+str(alpha)+"-"+str(BlogoUtils.object_counter())

        if (texture_scale == 0):
            minX = vertices[0][0]
            maxX = vertices[0][0]
            for vertex in vertices:
                if (vertex[0] > maxX):
                    maxX = vertex[0]
                if (vertex[0] < minX):
                    minX = vertex[0]
            texture_scale = (maxX - minX) / 10.0
            texture_scale = round(texture_scale, 3)
            if (texture_scale <= 0):
                texture_scale = 0.001
        obj,mesh = BlogoUtils.create_object(objname, vertices, faces)
        if (textureFile != None):
            BlogoUtils.add_texture(obj, textureFile, alpha, unwrap, smart_project, texture_scale)
        return obj

    def draw_plane_from_func(name, func, pts, closed_x=False, closed_y=False, texture=None, **kwargs):
        """
        Draw an object defined by a function giving the position of either point in the grid of the plane.

        The function given should be of the form: def my_func(x, y, rx, ry, \*\*kwargs):
            where x, y is the current position in the plane, and rx, ry is the position in the plane from 0 to 1

        :param name: The name the new object will have
        :param func: A function to pass each point in the plane to
        :param pts: A tuple giving either (x_max, y_max) or (x_min, y_min, x_max, y_max).  x_min and y_min default to 0
        :param closed_x: If True then the in the x direction 0 will be connected to max_x (default False)
        :param closed_y: If True then the in the y direction 0 will be connected to max_y (default False)
        :param texture: The texture to draw on the plane
        :param kwargs: User data to pass on to func
        """
        x_min = pts[0]
        y_min = pts[1]
        if (len(pts) < 3):
            x_max = x_min
            x_min = 0
        else:
            x_max = pts[2]
        if (len(pts) < 4):
            y_max = y_min
            y_min = 0
        else:
            y_max = pts[3]
        points = []
        vertex_mapping = []
        faces = []
        vertices = []
        for x in range(x_min, x_max):
            column = []
            column_mapping = []
            x_rel = float(x - x_min) / (x_max - x_min)
            for y in range(y_min, y_max):
                y_rel = float(y - y_min) / (y_max - y_min)
                vertex = func(x, y, x_rel, y_rel, **kwargs)
                column.append(vertex)
                if (vertex != None):
                    column_mapping.append(len(vertices))
                    vertices.append(vertex)
                else:
                    column_mapping.append(None)
            points.append(column)
            vertex_mapping.append(column_mapping)
        
        for x in range(x_max - x_min):
            column = points[x]
            for y in range(y_max - y_min):
                xplus1 = x + 1
                yplus1 = y + 1
                if (x >= (len(points)-1)):
                    if (closed_x):
                        xplus1 = 0
                    else:
                        break
                if (y >= (len(column)-1)):
                    if (closed_y):
                        yplus1 = 0
                    else:
                        break
                if (points[x][y] != None and
                    points[xplus1][y] != None and
                    points[x][yplus1] != None and
                    points[xplus1][yplus1] != None):
                    face = [vertex_mapping[x][y],
                            vertex_mapping[x][yplus1],
                            vertex_mapping[xplus1][yplus1],
                            vertex_mapping[xplus1][y]
                    ]
                    faces.append(face)
        return BlogoUtils.draw_mesh(name, vertices, faces, texture)
        
    def add_blend_file(filepath, coll_name, link=True):
        """
        Load a .blend file and put in the current scene

        :param filepath: The name of the file to load
        :param coll_name: The collection name to add it to
        :param link: If true then the file is only linked, otherwise it is appended
        """
        
        # link all collections starting with 'MyCollection'
        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]

        # link collection to scene collection
        for coll in data_to.collections:
            if coll is not None:
               bpy.context.scene.collection.children.link(coll)
               
    def boolean_op(a_list, op, b_list):
        """
        Perform either union, intersection or difference between two objects or lists of objects

        :param a_list: Either a blender object, or a list of blender objects
        :param op: The operation to perform, one of 'DIFFERENCE', 'UNION' or 'INTERSECTION'
        :param b_list: Either a blender object, or a list of blender objects
        :return:
        """
        op = op.upper()
        op_map = {"MINUS": "DIFFERENCE", "PLUS": "UNION", "EQUAL": "INTERSECTION"}
        if (op in op_map):
            op = op_map[op]
            
        if (not BlogoUtils.is_sequence(a_list)):
            a_list = [a_list]
        if (not BlogoUtils.is_sequence(b_list)):
            b_list = [b_list]
        count = 0
        BlogoUtils.unselect_objects()
        print(str(a_list) + " minus "+str(b_list))
        for b in b_list:
            for a in a_list:
                print(str(a) + " minus "+str(b))
                if (a != b):
                    op_name = "bool op "+str(BlogoUtils.object_counter())
                    bool_op = a.modifiers.new(type="BOOLEAN", name=op_name)
                    bool_op.object = b
                    bool_op.operation = op
                    a.select_set(True)
                    bpy.context.view_layer.objects.active = a
                    bpy.ops.object.modifier_apply(modifier=op_name)
                    a.select_set(False)
                    
        for b in b_list:        
            bpy.data.objects.remove(b)
            #b.hide_render = True
            #b.hide_viewport = True
            #b.hide_select = True
    
    def add_light(name, location, point_at, size, energy, type, shape, use_shadow):
        """
        Add a light to a scene

        :param name:
        :param location:
        :param point_at:
        :param size:
        :param energy:
        :param type:
        :param shape:
        :param use_shadow:
        :return:
        """
        # TOFIX: A crash here causes a problem with set mode next time?
        if (name == None):
            name = "Light-" + str(BlogoUtils.object_counter())
        try:
            lightObj = bpy.data.objects[name]
        except:
            light_data = bpy.data.lights.new(name=name,type="AREA")
            lightObj = bpy.data.objects.new(name=name, object_data=light_data)
            bpy.context.collection.objects.link(lightObj)
            bpy.context.view_layer.objects.active = lightObj
        lightObj.location = location
        lightObj.data.type = type
        try:
            lightObj.data.shape = shape
        except:
            pass
        try:
            lightObj.data.size = size
        except:
            pass
        try:
            lightObj.data.spot_size = size
        except:
            pass
        lightObj.data.specular_factor = 0.25
        lightObj.data.use_shadow = use_shadow
        lightObj.data.energy = energy
        lightObj.rotation_euler[0] = 0
        lightObj.rotation_euler[1] = 0
        lightObj.rotation_euler[2] = 0
    
    def add_light_area(name=None, location=(0,0,2*1609.34), size=10000, energy=1.21e+09, shape='SQUARE'):
        """
        Add a light in the form of a plane

        :param name:
        :param location:
        :param size:
        :param energy:
        :param shape:
        :return:
        """
        BlogoUtils.add_light(name, location, None, size, energy, "AREA", shape, False)
    def add_light_bulb(name=None, location=(0,0,2*1609.34), angle=120, energy=100):
        """
        Add a spot light to a scene

        :param name:
        :param location:
        :param angle:
        :param energy:
        :return:
        """
        area = 4 * pi
        proportion = (angle / 720)
        size = area * proportion
        energy = energy / proportion
        BlogoUtils.add_light(name, location, None, size, energy, "SPOT", None, True)
        
    def hide_cameras_and_lights():
        """
        Stop the renderer from showing camera and light objects, but still show their light
        """
        bpy.context.space_data.overlay.show_extras = False
        
    def add_camera(name, from_location, central_locations, capture_locations=None, angle=None, roll=0):
        """
        Place a camera at a particular location and point it at another location

        :param from_location:  The location of the camera
        :param central_locations: A list of locations to point the camera towards the middle of
        :param capture_locations: A list of locations that should be in frame (not yet implemented)
        :param angle: The angle in radians over which the camera should capture
        :param roll: The angle in radians to roll the camera round
        """
        x_sum = 0
        y_sum = 0
        z_sum = 0
        for x, y, z in central_locations:
            x_sum += x
            y_sum += y
            z_sum += z
        focus_location = mathutils.Vector((x_sum / len(central_locations),
                                           y_sum / len(central_locations),
                                           z_sum / len(central_locations),
        ))
        looking_direction = mathutils.Vector(from_location) - focus_location
        rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')
        rot_quat = looking_direction.to_track_quat('Z', 'Y')
        rot_quat = rot_quat.to_matrix().to_4x4() @ rollMatrix

        rotation_euler = rot_quat.to_euler()
        
        cam = bpy.data.cameras.new(name)

        if (angle != None):
            max_x_angle = angle
            max_y_angle = angle
        else:
            # TODO
            pass

        # create the first camera object
        cam.angle_x = max_x_angle
        if (cam.angle_y < max_y_angle):
            cam.angle_y = max_y_angle
            
        cam_obj = bpy.data.objects.new(name, cam)
        cam_obj.location = from_location
        cam_obj.rotation_euler = rotation_euler
        
        bpy.context.collection.objects.link(cam_obj)
        return cam_obj
        
    def take_picture(file, from_location, central_locations, capture_locations=None, angle=None, roll=0):
        """
        Place a camera at a particular location, point it at another location and save that picture to disk.

        :param file: The name of the file to save to.
        :param from_location:  The location of the camera
        :param central_locations: A list of locations to point the camera towards the middle of
        :param capture_locations: A list of locations that should be in frame (not yet implemented)
        :param angle: The angle in radians over which the camera should capture
        :param roll: The angle in radians to roll the camera round
        """
        cam_obj = BlogoUtils.add_camera("TempCamera", from_location, central_locations, capture_locations, angle, roll)
        bpy.context.scene.camera = cam_obj
        bpy.context.scene.render.image_settings.file_format='PNG'
        bpy.context.scene.render.filepath = file
        bpy.ops.render.render(use_viewport = True, write_still=True)
        bpy.data.objects.remove(cam_obj, do_unlink=True)


def register():
    pass

def unregister():
    pass

if __name__ == "__main__":
    register()