import bpy
import math
import os

#clear the terminal window
os.system('cls' if os.name == 'nt' else 'clear')

##print all the objects in a scene in the Python console
#for obj in bpy.data.objects:
#    print(obj.name)

def rotate_axis():

    #active selection workflow    
    axis_obj = bpy.context.scene.objects['RotatingEmpty']       #define the object
    bpy.context.view_layer.objects.active = axis_obj            #activate the desired object

    #set the rotation mode and object context
    axis_obj.rotation_mode = 'XYZ'
    axis_obj = bpy.context.object
    
    #CLOCK CONTROL
    #--------------------------------------------------------------------------------------
    #settings for the clock hand that will be rotating for the duration of the song
    
    obj_rotation = 0     #initial euler angle 
    obj_keyframe = 0     #initial keyframe
    inc_angle = 360      #rotation amount
    wait_frames = 15     #number of frames to wait
    
    #drop the initial keyframe
    bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
    axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe) 

    #initialize the starting key frame used in the loop
    start_key = obj_keyframe

    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        
        for line in f:
            
            end_key = int(line.strip())
            
            if end_key < 8503:
                #drop the rotation keyframe
                obj_keyframe = end_key
                obj_rotation += inc_angle
                bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
                axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe)
                
                #drop the pause keyframe
                obj_keyframe = end_key + wait_frames
                axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe)
            
            elif end_key >= 8503 and end_key < 9291:
                #linear acceleration
                inc_angle -= 15
                
                #drop the rotation keyframe
                obj_keyframe = end_key
                obj_rotation += inc_angle
                bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
                axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe)
                
            elif end_key >= 9291:
                #drop the rotation keyframe
                obj_keyframe = end_key
                obj_rotation += inc_angle
                bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
                axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe)
            
    #active selection workflow    
    axis_obj = bpy.context.scene.objects['RotatingEmptyWaves']       #define the object
    bpy.context.view_layer.objects.active = axis_obj            #activate the desired object

    #set the rotation mode and object context
    axis_obj.rotation_mode = 'XYZ'
    axis_obj = bpy.context.object
    
    #ROTATING LIGHTS & WAVE GENERATORS CONTROL
    #--------------------------------------------------------------------------------------
    #settings for the lights that will be rotating for the duration of the song
    
    obj_rotation = 18     #initial euler angle 
    obj_keyframe = 0     #initial keyframe
    inc_angle = 450      #rotation amount
    
    #drop the initial keyframe
    bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
    axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe) 

    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        
        skip_count = 4
        
        for line in f:
            
            obj_keyframe = int(line.strip())
            
            if obj_keyframe < 5995:
                continue
            
            elif obj_keyframe >= 5995 and skip_count == 4:
                 
                skip_count = 1
                
                #drop the rotation keyframe
                bpy.context.active_object.rotation_euler[2] = math.radians(obj_rotation)
                axis_obj.keyframe_insert(data_path='rotation_euler', frame=obj_keyframe)
                obj_rotation += inc_angle
            
            else:
                skip_count += 1

def hand_emiss_control():
    
    #define the blink time and intensity
    blink_dur = 15
    blink_int = 10
    
    #define the names of the target object and property
    matl = 'ClockhandEmission'
    emiss = 'Emission'
    
    #establish the data path for the emission strength property
    emiss_matl = bpy.data.materials[matl].node_tree.nodes[emiss].inputs[1]
    
    #clear animation data from the material
    bpy.data.materials[matl].animation_data_clear()

    #drop the first key
    keyframe = 0
    emiss_matl.default_value = 1
    emiss_matl.keyframe_insert(data_path = 'default_value', frame = keyframe)

    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        for line in f:
            
            #skip some keyframes in the text file
            blink_key = int(line.strip())
            if blink_key < 350:
                continue
            
            else:
                #drop the starting and ending keyframes
                emiss_matl.default_value = 1
                obj_keyframe = blink_key - blink_dur
                emiss_matl.keyframe_insert(data_path = 'default_value', frame = obj_keyframe)
                
                obj_keyframe = blink_key + blink_dur
                emiss_matl.keyframe_insert(data_path = 'default_value', frame = obj_keyframe)
                
                #drop the peak of the blink
                emiss_matl.default_value = blink_int
                obj_keyframe = blink_key
                emiss_matl.keyframe_insert(data_path = 'default_value', frame = obj_keyframe)
                
    #TRANSPARENCY CONTROL
    #--------------------------------------------------------------------------------------
    emiss_matl = bpy.data.materials[matl].node_tree.nodes["Mix Shader"].inputs[0]
    emiss_matl.default_value = 1
    keyframe = 0
    emiss_matl.keyframe_insert(data_path = 'default_value', frame = keyframe)
    keyframe = 9369
    emiss_matl.keyframe_insert(data_path = 'default_value', frame = keyframe)
    
    emiss_matl.default_value = 0
    keyframe = 9975
    emiss_matl.keyframe_insert(data_path = 'default_value', frame = keyframe)
    
def light_emiss_control():

    #initialize stuff
    start_key = 0
    light_src = ['Point2', 'Point3', 'Point1']
    
    sector_colors = [
        [16, 5, 64],     #deep blue
        [82, 11, 57],    #deep magenta
        [38, 54, 165]]   #blue
    
    sector_colors_expanded = [
        [200, 32, 14],   #deep orange
        [16, 5, 64],     #deep blue
        [238, 85, 25],   #orange
        [82, 11, 57],    #deep magenta
        [238, 85, 25],   #dark tangerine 
        [38, 54, 165]]   #blue
    
    blink_dur = 15
    blink_int = 2
        
    slow_dur = 180
    slow_int = 1
     
    #SHORT DURATION LIGHTS
    #--------------------------------------------------------------------------------------
    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        
        sector = 0
        
        for line in f:
            
            #control flow for blinking individually
            for light in light_src:
                bpy.data.lights[light].color = [1,1,1]
            
            blink_key = int(line.strip())
            if blink_key < 1518:
                pass
 
            elif blink_key < 4412:
                #drop the starting and ending keyframes
                bpy.data.lights[light_src[sector]].energy = 0
                obj_keyframe = blink_key - blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                obj_keyframe = blink_key + blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #setting the white boundary values
                bpy.data.lights[light_src[sector]].color = [1,1,1]
                    
                obj_keyframe = blink_key - blink_dur - 1
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                    
                obj_keyframe = blink_key + blink_dur + 1
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                   
                #setting color between the boundary values
                bpy.data.lights[light_src[sector]].color = sector_colors[sector]
                
                obj_keyframe = blink_key - blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                obj_keyframe = blink_key + blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                #drop the peak of the blink
                bpy.data.lights[light_src[sector]].energy = blink_int
                obj_keyframe = blink_key
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #this rotates through the sector
                if sector != 2:
                    sector += 1
                elif sector == 2:
                    sector = 0

    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        
        sector = 1
        color_option = 0
        
        for line in f:

            #control flow for extra blinking and some color
            blink_key = int(line.strip())
            if blink_key < 3074:
                pass
            
            elif blink_key < 4412:
                #subtract off some keyframes
                blink_key -= 30
                
                #drop the starting and ending keyframes
                bpy.data.lights[light_src[sector]].energy = 0
                obj_keyframe = blink_key - blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)

                obj_keyframe = blink_key + blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #setting the white boundary values
                bpy.data.lights[light_src[sector]].color = [1,1,1]
                    
                obj_keyframe = blink_key - blink_dur - 1
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                    
                obj_keyframe = blink_key + blink_dur + 1
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                   
                #setting color between the boundary values
                bpy.data.lights[light_src[sector]].color = sector_colors[sector]
                
                obj_keyframe = blink_key - blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                obj_keyframe = blink_key + blink_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                #drop the peak of the blink
                bpy.data.lights[light_src[sector]].energy = blink_int
                obj_keyframe = blink_key
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #this rotates through the sectors  
                if sector != 2:
                    sector += 1
                elif sector == 2:
                    sector = 0
    
    #LONG DURATION LIGHTS
    #--------------------------------------------------------------------------------------
    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
        
        sector = 0
        color_options = 0
        skip_count = 4
        
        for line in f:                
            
            blink_key = int(line.strip())
            if blink_key < 4412:
                continue
 
            elif blink_key < 6704 and skip_count == 4:
                
                skip_count = 1
                
                bpy.data.lights[light_src[sector]].color = sector_colors[sector]
                
                obj_keyframe = blink_key -30
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                obj_keyframe = blink_key + slow_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                #drop the starting and ending keyframes
                bpy.data.lights[light_src[sector]].energy = 0
                obj_keyframe = blink_key -30
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                obj_keyframe = blink_key + slow_dur
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #drop the peak of the blink
                bpy.data.lights[light_src[sector]].energy = slow_int
                obj_keyframe = blink_key + slow_dur / 2
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
            
                #this rotates through the sector
                if sector != 2:
                    sector += 1
                elif sector == 2:
                    sector = 0
            
            elif blink_key >= 6704 and blink_key < 8371:
                
                if blink_key == 6704:
                    skip_count = 2
            
                if skip_count == 2:
                
                    bpy.data.lights[light_src[sector]].color = sector_colors[sector]
                    
                    obj_keyframe = blink_key -30
                    bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                    
                    obj_keyframe = blink_key + slow_dur
                    bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                    
                    #drop the starting and ending keyframes
                    bpy.data.lights[light_src[sector]].energy = 0
                    obj_keyframe = blink_key - 30
                    bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                    
                    obj_keyframe = blink_key + slow_dur
                    bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                    
                    #drop the peak of the blink
                    bpy.data.lights[light_src[sector]].energy = slow_int
                    obj_keyframe = blink_key + slow_dur / 2
                    bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                else:
                    skip_count += 1
                
                #this rotates through the sectors
                if sector != 2:
                    sector += 1
                elif sector == 2:
                    sector = 0
              
            elif blink_key >= 8371:
                
                bpy.data.lights[light_src[sector]].color = sector_colors_expanded[color_options]
                
                obj_keyframe = blink_key - 60
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                obj_keyframe = blink_key + 60
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'color', frame = obj_keyframe)
                
                #drop the starting and ending keyframes
                bpy.data.lights[light_src[sector]].energy = 0
                obj_keyframe = blink_key - 60
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                obj_keyframe = blink_key + 60
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
                
                #drop the peak of the blink
                bpy.data.lights[light_src[sector]].energy = slow_int
                obj_keyframe = blink_key + 60 / 2
                bpy.data.lights[light_src[sector]].keyframe_insert(data_path = 'energy', frame = obj_keyframe)
            
                #this rotates through the sectors
                if sector != 2:
                    sector += 1
                elif sector == 2:
                    sector = 0
                    
                #this rotates through the color options
                print(sector_colors_expanded[color_option])
                print(blink_key)
                if color_options != 5:
                    color_options += 1
                elif color_options == 5:
                    color_options = 0
            
            else:
                skip_count += 1
                
def wave_master():
    
    #starting at the specified key frame, do wave generation
    #the waves are generated every fourth flag in the timeline
    
    spheres = {
        'Sphere1':(0,1.75,1), 
        'Sphere2':(-1.516,-0.875,1), 
        'Sphere3':(1.516,-0.875,1)}
    
    with open('/home/perry/Documents/projection_mapping/keyframes.txt') as f:
 
        sector = 1
        
        for line in f:
            
            wave_key = int(line.strip())
            if wave_key < 4412:
                continue
            
            elif wave_key >= 4412 and wave_key < 6704:
                
                if wave_key == 4412:
                    skip_count = 4
                    
                if skip_count == 4:
                    
                    skip_count = 1
                    sphere = 'Sphere' + str(sector)
                    sphere_obj = bpy.data.objects[sphere]
                    
                    sphere_obj.location = spheres[sphere]
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key - 15)
                
                    coord_temp = list(spheres[sphere])
                    coord_temp[2] -= 1
                    sphere_obj.location = tuple(coord_temp)
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key)
                    
                    sphere_obj.location = spheres[sphere]
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key + 15)
                        
                else:
                    skip_count += 1
                
                if sector != 3: 
                    sector += 1
                else:
                    sector = 1   
            
            elif wave_key >= 6704 and wave_key < 8033:

                if wave_key == 6704:
                    skip_count = 2
                
                if skip_count == 2:
                    
                    skip_count = 1
                
                    sphere = 'Sphere' + str(sector)
                    sphere_obj = bpy.data.objects[sphere]
                    
                    sphere_obj.location = spheres[sphere]
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key - 45)
                
                    coord_temp = list(spheres[sphere])
                    coord_temp[2] -= 1
                    sphere_obj.location = tuple(coord_temp)
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key)
                    
                    sphere_obj.location = spheres[sphere]
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key + 45)
                    
                else:
                    skip_count += 1    
                
                if sector != 3:
                    sector += 1
                else:
                    sector = 1  
                    
            elif wave_key >= 8033 and  wave_key < 9291:
            
                sphere = 'Sphere' + str(sector)
                sphere_obj = bpy.data.objects[sphere]
                
                sphere_obj.location = spheres[sphere]
                sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key - 45)
            
                coord_temp = list(spheres[sphere])
                coord_temp[2] -= 1
                sphere_obj.location = tuple(coord_temp)
                sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key)
                
                sphere_obj.location = spheres[sphere]
                sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key + 45)    
                
                if sector != 3:
                    sector += 1
                else:
                    sector = 1  
                
            elif wave_key >= 9291:
                
                print('test')
                print(skip_count)
                
                if wave_key == 9291:
                    skip_count = 2
                
                if skip_count == 2:
                    skip_count = 1
            
                    sphere = 'SphereCenter'
                    sphere_obj = bpy.data.objects[sphere]
                    
                    sphere_obj.location = (0,0,1)
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key - 45)
                
                    coord_temp = [0,0,1]
                    coord_temp[2] -= 1
                    sphere_obj.location = tuple(coord_temp)
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key)
                    
                    sphere_obj.location = (0,0,1)
                    sphere_obj.keyframe_insert(data_path = 'location', frame = wave_key + 45)
                    
                else:
                    skip_count += 1
                                 
if __name__ == '__main__':
    rotate_axis()
    hand_emiss_control()
    light_emiss_control()
    wave_master()
