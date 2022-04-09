# ---------------- ADDON'S INFOS ----------------
bl_info = {
    "name": "Camera Injector",
    "author" : "Corentin, Dorian, Jihed",
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "3D Viewport",
    "description": "Add-on to inject some moves in this old camera..."
}

# ---------------- IMPORTED LIBRARIES ----------------

import bpy
import math


# ---------------- VARIABLES ----------------

class Properties(bpy.types.PropertyGroup):
     
    enumSelectionPreset : bpy.props.EnumProperty(
    name = "Presets",
    description = "What type of camera effect or movement would you like ?",
    items = [
    ('Option 1', "Select a preset", ""),
    ("Option 2", "Zoom In", "The camera will move towards the focus point"),
    ("Option 3", "Zoom Out", "The camera will move away from the focus point"),
    ("Option 4", "Turnaround", "The camera will turn around the focus point"),
    ("Option 5", "Vertigo", "")]
    )
     
    endFrame : bpy.props.IntProperty(
    name="last frame",
    description="When do you want your camera movement to stop ?",
    default = 250,
    min = 2,
    soft_max = 43200,
    )
    
    beginFrame : bpy.props.IntProperty(
    name="first frame",
    description="When do you want your camera movement to start ?",
    default = 1,
    min = 1,
    soft_max = 43199,
    )
    
    beginValue : bpy.props.FloatProperty(
    name = "low value",
    description="How much zoomed in should the camera be ?",
    default = 0.6,
    min = 0,
    )
    
    endValue : bpy.props.FloatProperty(
    name = "max value",
    description = "How much zoomed out should the camera be ?",
    default = 1,
    min = 0,
    )
    
    
#sert à créer l'UI de selection d'objets    
bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)   


# ---------------- UI ----------------

class VIEW3D_PT_CameraInjectorInterface(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Camera Injector"
    bl_label = "Camera Injector"
    
    def draw(self, context):
        #variables to simplify and shorten the script
        layout = self.layout
        scene = context.scene
        propertiesTool = scene.propertiesTool
        row = layout.row()
        targetSelected = context.scene.target
        
        layout.prop(propertiesTool, "enumSelectionPreset")
        row.operator("caminject.op")
        
        if propertiesTool.enumSelectionPreset == "Option 2":
            
            layout.prop(propertiesTool, "beginValue", text="Close Position")
            layout.prop(propertiesTool, "endValue", text="Far Position")
            layout.prop(propertiesTool, "beginFrame", text="First frame")
            layout.prop(propertiesTool, "endFrame", text="Last frame")
 
        elif propertiesTool.enumSelectionPreset == "Option 4": 
            layout.prop_search(scene, "target", scene, "objects", text="Target")
            layout.prop(propertiesTool, "endValue", text = "Circle radius")
            layout.prop(propertiesTool, "beginFrame", text = "First frame")
            layout.prop(propertiesTool, "endFrame", text = "Last frame")
            
# ---------------- OPERATOR ----------------

class CAMINJECT_OT_mainOperator(bpy.types.Operator):
    """The operator that reference all the camera movements functions"""
    bl_idname = "caminject.op"
    bl_label = "INJECT"
    bl_options = {'REGISTER', 'UNDO'}
      
    
    def execute(self, context):
    
        #variables to simplify and shorten the script
        layout = self.layout
        scene = context.scene
        propertiesTool = scene.propertiesTool
        targetSelected = context.scene.target
        text=str(targetSelected) if targetSelected else ""
        
        if propertiesTool.enumSelectionPreset == "Option 2":
            zoomIn()
            
        if propertiesTool.enumSelectionPreset == "Option 4":
            circle = bpy.context.scene.objects.get("Circle")
            
            if circle:
                ob = bpy.data.objects['Circle']
                cam = bpy.data.objects['Camera']
                bpy.data.objects.remove(ob)
                bpy.data.objects.remove(cam)
            turnAround(targetSelected)

        return {'FINISHED'}


# ---------------- FUNCTIONS ----------------

def zoomIn():
    
    propertiesTool = bpy.context.scene.propertiesTool

    cameraZoomIn = bpy.context.scene.objects.get("Camera with Zoom In")
    
    #detect is there is already a camera with a zoom in effect,
    # and if so delete it and all that was created for this movement to exist.
    if cameraZoomIn:
        targetZoomIn = bpy.data.objects['Camera target']
        scalerZoomIn = bpy.data.objects['Scale me to adjust the camera zoom']
        camZoomIn = bpy.data.objects['Camera with Zoom In']
        objectsPreviouslyAdded = [targetZoomIn, scalerZoomIn, camZoomIn]
        for objectsToDelete in objectsPreviouslyAdded:
            bpy.data.objects.remove(objectsToDelete)
     
#setting up the scene and the components's behaviour
    
    #create an empty object
    bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(50, 50, 50))
    cameraTarget = bpy.context.active_object
    cameraTarget.name = "Camera target"

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    cameraScaler = bpy.context.active_object
    #rename the active object
    cameraScaler.name = "Scale me to adjust the camera zoom"


    #create a camera
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(7, -10, 8), rotation=(59.0, 0.0, 35.0), scale=(2, 2, 2))
    #save the cam in a new variable
    camera = bpy.context.active_object
    camera.name = "Camera with Zoom In"

    #add a contraint of type "track to" and use the empty "cameraTarget" as the target
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = cameraTarget

    #parent the camera to the scaler
    camera.parent = cameraScaler
        
    #camera keying, for the movement

    cameraScaler.scale = (propertiesTool.beginValue , propertiesTool.beginValue, propertiesTool.beginValue)
    cameraScaler.keyframe_insert(data_path="scale", frame = propertiesTool.beginFrame)
        
    cameraScaler.scale = (propertiesTool.endValue, propertiesTool.endValue, propertiesTool.endValue)
    cameraScaler.keyframe_insert(data_path="scale", frame = propertiesTool.endFrame)  


def turnAround(targetSelected):     


    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(bpy.context.scene.propertiesTool.endValue, 0, 0), rotation=(0.0, 0.0, 0.0), scale=(2, 2, 2))
    Camera = bpy.context.selected_objects[0]
    scene = bpy.context.scene
    bpy.data.objects['Camera'].select_set(True)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = targetSelected


    #Create Circle

    bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    global Circle
    Circle = bpy.context.selected_objects[0]
    Circle.scale[0] = bpy.context.scene.propertiesTool.endValue
    Circle.scale[1] = bpy.context.scene.propertiesTool.endValue
    Circle.scale[2] = bpy.context.scene.propertiesTool.endValue


    #Parent Camera to Circle

    Camera.select_set(True)
    Circle.select_set(True)
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    deselect()

    #Replace Circle
    Circle.select_set(True)
    Circle.location = (0, 0, 5)
    Circle.scale[0] = Circle.scale[0] * 1.5
    Circle.scale[1] = Circle.scale[1] * 1.5


    #Keyframing
    scene.frame_start = bpy.context.scene.propertiesTool.beginFrame
    scene.frame_end = bpy.context.scene.propertiesTool.endFrame = 272

    scene.frame_set(bpy.context.scene.propertiesTool.beginFrame)
    bpy.ops.anim.keyframe_insert_menu(type='Rotation')


    scene.frame_set(bpy.context.scene.propertiesTool.endFrame)
    Circle.rotation_euler[2] = degreeToEuler(360)
    bpy.ops.anim.keyframe_insert_menu(type='Rotation')

    AnimCurves = Circle.animation_data.action.fcurves
    for point in AnimCurves:
        for pointCurve in point.keyframe_points:
            pointCurve.interpolation = 'LINEAR'
    
def degreeToEuler(degree):
    return ((2 * math.pi) * 360) / degree
    
def deselect():
    for obj in bpy.data.objects:
        obj.select_set(False)
# ---------------- ADDON REGISTRATION ----------------  
    
classes = [VIEW3D_PT_CameraInjectorInterface, Properties, CAMINJECT_OT_mainOperator]

#to register and unregister the addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.propertiesTool = bpy.props.PointerProperty(type = Properties)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.propertiesTool

#line to load the script directly in the blender text editor ; no point to it if it's an addon.      
if __name__ == "__main__":
        register()