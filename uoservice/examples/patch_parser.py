from io import StringIO
from io import BytesIO
import struct
import utils

files_patch_name = "patch_0.mul"

file_patch = open(files_patch_name, 'rb')
p_file_patch = file_patch.read()
files_patch_reader = utils.FileReader(BytesIO(p_file_patch))

files_patch_reader.seek(7)

patches_count = files_patch_reader.read_uint32_be()
print("patches_count: ", patches_count)

for i in range(0, patches_count):
	print("i: ", i)

	map_patches_count = files_patch_reader.read_uint32_be()
	print("map_patches_count: ", map_patches_count)

	static_patches_count = files_patch_reader.read_uint32_be()
	print("static_patches_count: ", static_patches_count)