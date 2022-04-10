import bpy
from bpy import context
import os
import sys
import argparse
import math

#Delete all Item in scene
def deleteAll():
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)

##Function to deselect all objects
def deselect():
    for obj in bpy.data.objects:
        obj.select_set(False)

def degreeToEuler(degree):
    return ((2 * math.pi) * 360) / degree

deleteAll()
       
scene = bpy.context.scene
#Create Cube (can be an Empty)

CubeScaleX = 1
CubeScaleY = 1
CubeScaleZ = 1

bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(CubeScaleX, CubeScaleY, CubeScaleZ))
Cube = bpy.context.selected_objects[0]


#Camera Track

CameraXLocation = 6

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(CameraXLocation, 0, 0), rotation=(0.0, 0.0, 0.0), scale=(2, 2, 2))
Camera = bpy.context.selected_objects[0]

bpy.data.objects['Camera'].select_set(True)






Camera.select_set(True)


bpy.context.scene.render.engine = 'CYCLES'

bpy.context.object.data.type = 'PANO'
bpy.context.object.data.cycles.panorama_type = 'FISHEYE_EQUIDISTANT'
