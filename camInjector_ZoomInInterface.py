bl_info = {
    "name": "Zoom in Operator",
    "author" : "Dorantu",
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "Operator Search",
    "description": "Add-on to add camera with a zoom in movement"
}


import bpy


# ---- operator class

class CAMINJECT_OT_zoomin(bpy.types.Operator):
    """The operator that make a zoom-in movement"""
    bl_idname = "caminject.zoomin"
    bl_label = "Camera Injector - Zoom In"
    bl_options = {'REGISTER', 'UNDO'}
    
    
# ---- variables definition
    
    zoomedInFrame : bpy.props.IntProperty(
    name="zoomed in frame",
    description="When do you want you camera movement to stop ?",
    default = 250,
    min = 2,
    soft_max = 43200,
    )
    
    zoomedOutFrame : bpy.props.IntProperty(
    name="zoomed out frame",
    description="When do you want you camera movement to start ?",
    default = 1,
    min = 1,
    soft_max = 43199,
    )
    
    zoomedInValue : bpy.props.FloatProperty(
    name = "zoomed in value",
    description="How much zoomed in should the camera be ?",
    default = 0.6,
    min = 0,
    )
    
    zoomedOutValue : bpy.props.FloatProperty(
    name = "zoomed out value",
    description = "How much zoomed out should the camera be ?",
    default = 1,
    min = 0,
    )
    
    
    def execute(self, context):
        
# ---- setting up the scene and the components's behaviour

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

        #add a contraint of type "track to" and use the empty "cameraTarget" as the target
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = cameraTarget

        #parent the camera to the scaler
        camera.parent = cameraScaler
        
        
# ---- camera keying, for the movement

        cameraScaler.scale = (self.zoomedOutValue , self.zoomedOutValue, self.zoomedOutValue)
        cameraScaler.keyframe_insert(data_path="scale", frame = self.zoomedOutFrame)
        
        cameraScaler.scale = (self.zoomedInValue, self.zoomedInValue, self.zoomedInValue)
        cameraScaler.keyframe_insert(data_path="scale", frame = self.zoomedInFrame)
        
        return {'FINISHED'}
    
    
# ---- panel class, for the UI
class VIEW3D_PT_zoomin(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Camera Injector"
    bl_label = "Camera Injector"
    
    def draw(self, context):
        self.layout.operator("caminject.zoomin", text="Zoom In")
        


def register():
        bpy.utils.register_class(CAMINJECT_OT_zoomin)
        bpy.utils.register_class(VIEW3D_PT_zoomin)
        
def unregister():
        bpy.utils.unregister_class(CAMINJECT_OT_zoomin)
        bpy.utils.unregister_class(VIEW3D_PT_zoomin)

# ---- line to load the script directly in the blender text editor ; no point to it if it's an addon.      
#if __name__ == "__main__":
#        register()