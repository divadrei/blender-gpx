from xml.dom.minidom import parse, parseString
import math
import bpy
from bpy_extras.io_utils import ImportHelper


bl_info = {
	'name': 'Import GPX Format (.gpx)',
	'author': 'David Charbonnier',
	'version': (1, 0, 0),
	'blender': (2, 6, 3),
	'location': 'File > Import > Gpx (.gpx)',
	'description': 'Import files in the GPX format (.gpx)',
	'category': 'Import-Export',
	}



class ImportGPX(bpy.types.Operator, ImportHelper):
	'''Load a GPX file'''

	bl_idname = "import.gpx"
	bl_label = "Import GPX"

	filename_ext = ".gpx"
	filter_glob = bpy.props.StringProperty(default="*.gpx", options={'HIDDEN'})

	def execute(self, context):
		dom1 = parse(self.properties.filepath)
		verts = []
		for t in dom1.getElementsByTagName('trkpt'):
			lat = math.radians(float(t.getAttribute('lat')))
			lon = math.radians(float(t.getAttribute('lon')))
			alt = float(t.getElementsByTagName('ele')[0].childNodes[0].data)
			alt += 6371000
			x = math.sin(lat) * math.cos(lon) * alt
			y = math.sin(lat) * math.sin(lon) * alt
			z = math.cos(lat) * alt
			verts.append((x,y,z))
		
		mesh = bpy.data.meshes.new("trace")
		object = bpy.data.objects.new("trace", mesh)
		object.location = bpy.context.scene.cursor_location
		bpy.context.scene.objects.link(object)
		edges = [(i-1,i) for i in range(1,len(verts))]
		mesh.from_pydata(verts, edges, [])
		mesh.update(calc_edges=True) 

		return {'FINISHED'}  

def menu_func_import(self, context):
	self.layout.operator(ImportGPX.bl_idname, text="gpx (.gpx)")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()