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
		min_x = None
		min_y = None
		min_z = None
		max_x = None
		max_y = None
		max_z = None
		
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

			if min_x is None or x < min_x:
				min_x = x
			if min_y is None or y < min_y:
				min_y = y
			if min_z is None or z < min_z:
				min_z = z

			if max_x is None or x > max_x:
				max_x = x
			if max_y is None or y > max_y:
				max_y = y
			if max_z is None or z > max_z:
				max_z = z
				
			verts.append((x,y,z))
		
		offset_x = max_x - (max_x-min_x) / 2
		offset_y = max_y - (max_y-min_y) / 2
		offset_z = max_z - (max_z-min_z) / 2				
		
		
		for i in range(0,len(verts)):
			verts[i]=(verts[i][0]-offset_x,verts[i][1]-offset_y,verts[i][2]-offset_z)
			
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