from io import StringIO
from io import BytesIO
import struct
import utils
from numpy import int8
import os
import threading

class UoServiceGameFileParser:
	'''UoServiceGameFileParser class including Binary file reader'''
	def __init__(self, uo_installed_path):
		self.uo_installed_path = uo_installed_path

		self.files_map_name = "map0LegacyMUL.uop"
		self.files_statics_name = "statics0.mul"
		self.files_index_statics_name = "staidx0.mul"
		self.files_tiledata_name = "tiledata.mul"

		self.files_map_path = os.path.join(self.uo_installed_path, self.files_map_name)
		self.files_statics_path = os.path.join(self.uo_installed_path, self.files_statics_name)
		self.files_index_statics_path = os.path.join(self.uo_installed_path, self.files_index_statics_name)
		self.files_tiledata_path = os.path.join(self.uo_installed_path, self.files_tiledata_name)

		self.UOP_MAGIC_NUMBER = hex(0x50594d)
		self._has_extra = False
		self.total_entries_count = 0
		self.hashes_dict = {}
		self.file_size = 0

		self.MapsDefaultSize = {7168 >> 3, 4096 >> 3}

		self.block_data = []
		self.land_data_dict = {}
		self.static_data_dict = {}

		self.files_map = open(self.files_map_path, 'rb')
		self.p_files_map = self.files_map.read()
		self.files_map_reader = utils.FileReader(BytesIO(self.p_files_map))
		self.files_map_size = self.files_map_reader.size

		self.files_statics = open(self.files_statics_path, 'rb')
		self.p_files_statics = self.files_statics.read()
		self.files_statics_reader = utils.FileReader(BytesIO(self.p_files_statics))
		self.files_statics_size = self.files_statics_reader.size

		self.files_index_statics = open(self.files_index_statics_path, 'rb')
		self.p_files_index_statics = self.files_index_statics.read()
		self.files_index_statics_reader = utils.FileReader(BytesIO(self.p_files_index_statics))
		self.files_index_statics_size = self.files_index_statics_reader.size

		self.file_tiledata = open(self.files_tiledata_path, 'rb')
		self.p_file_tiledata = self.file_tiledata.read()
		self.files_tiledata_reader = utils.FileReader(BytesIO(self.p_file_tiledata))

		self.files_map_reader.seek(0)
		self.files_statics_reader.seek(0)
		self.files_index_statics_reader.seek(0)
		self.files_tiledata_reader.seek(0)

	def load(self):
		#self.load_map_file()
		#self.load_tile_data()
		thread_1 = threading.Thread(target=self.load_map_file, daemon=True, args=())
		thread_2 = threading.Thread(target=self.load_tile_data, daemon=True, args=())

		thread_1.start()
		thread_2.start()

		thread_1.join()
		thread_2.join()

	def load_map_file(self):
		print("load_map_file()")

		uop_magic_number = hex(self.files_map_reader.read_uint32())
		if uop_magic_number != self.UOP_MAGIC_NUMBER:
		    raise NameError('Bad uop file')

		version = self.files_map_reader.read_uint32()
		format_timestamp = self.files_map_reader.read_uint32()
		next_block = self.files_map_reader.read_long()
		block_size = self.files_map_reader.read_uint32()
		count = self.files_map_reader.read_uint32()

		self.files_map_reader.seek(next_block)
		total = 0;
		real_total = 0;
		while next_block != 0:
		    files_count = self.files_map_reader.read_uint32()
		    next_block = self.files_map_reader.read_long()
		    total += files_count;

		    for i in range(0, files_count):
		        offset = self.files_map_reader.read_long()
		        header_length = self.files_map_reader.read_uint32()
		        compressed_length = self.files_map_reader.read_uint32()
		        decompressed_length = self.files_map_reader.read_uint32()
		        hash_value = self.files_map_reader.read_long()
		        data_hash = self.files_map_reader.read_uint32()
		        flag = self.files_map_reader.read_short();
		        length = compressed_length if flag == 1 else decompressed_length;

		        if offset == 0:
		            continue

		        real_total += 1
		        offset += header_length

		        self.hashes_dict[hash_value] = utils.UOFileIndex(self.file_size, offset, compressed_length, 
		                                                         decompressed_length)

		    self.files_map_reader.seek(next_block)

		total_entries_count = real_total;

		pattern = "build/map0legacymul/{:08d}.dat"

		entries = []
		for i in range(0, total_entries_count):
		    file = pattern.format(i)
		    hash_value = utils.create_hash(file)
		    hash_data = self.hashes_dict[hash_value]
		    entries.append(hash_data)

		mapblocksize = 196
		staticidxblocksize = 12
		staticblocksize = 7

		uopoffset = 0
		file_number = -1;
		maxblockcount = 896 * 512

		for block in range(0, maxblockcount):
		    realmapaddress = 0
		    realstaticaddress = 0
		    realstaticcount = 0

		    blocknum = block;
		    blocknum &= 4095;

		    shifted = block >> 12;
		    if file_number != shifted:
		        file_number = shifted

		        if shifted < len(entries):
		            uopoffset = entries[shifted].offset

		    address = uopoffset + (blocknum * mapblocksize);

		    if address < self.files_map_size:
		        realmapaddress = address

		    stidxaddress = (block * staticidxblocksize);

		    self.files_index_statics_reader.seek(stidxaddress)
		    position = self.files_index_statics_reader.read_uint32()
		    size = self.files_index_statics_reader.read_uint32()
		    unknown = self.files_index_statics_reader.read_uint32()
		    if stidxaddress < self.files_index_statics_size and size > 0 and position != 0xFFFFFFFF:
		        address1 = position
		        if address1 < self.files_statics_size:
		            realstaticaddress = address1;
		            realstaticcount = int(size / staticblocksize)

		            if realstaticcount > 1024:
		                realstaticcount = 1024;

		    index_map = utils.IndexMap(realmapaddress, realstaticaddress, realstaticcount, 
		                               realmapaddress, realstaticaddress, realstaticcount)

		    self.block_data.append(index_map)

	def load_tile_data(self):
		#print("load_tile_data()")

		for i in range(0, 512):
		    self.files_tiledata_reader.read_uint32()

		    for j in range(0, 32):
		        idx = i * 32 + j
		        flags = self.files_tiledata_reader.read_long();
		        text_id = self.files_tiledata_reader.read_short();

		        buffer_string = ""
		        for k in range(0, 20):
		            byte_data = self.files_tiledata_reader.read_byte()
		            if byte_data != 0:
		                buffer_string += chr(byte_data)

		        #print("land buffer_string: ", buffer_string)

		        self.land_data_dict[idx] = {"flags": flags, "text_id": text_id, "name": buffer_string}

		for i in range(0, 2048):
		    self.files_tiledata_reader.read_uint32()

		    for j in range(0, 32):
		        idx = i * 32 + j
		        flags = self.files_tiledata_reader.read_long()
		        weight = self.files_tiledata_reader.read_byte()
		        layer = self.files_tiledata_reader.read_byte()
		        count = self.files_tiledata_reader.read_uint32();
		        anim_id = self.files_tiledata_reader.read_short();
		        hue = self.files_tiledata_reader.read_short();
		        light_index = self.files_tiledata_reader.read_short();
		        height = self.files_tiledata_reader.read_byte();

		        buffer_string = ""
		        for k in range(0, 20):
		            byte_data = self.files_tiledata_reader.read_byte()
		            if byte_data != 0:
		                buffer_string += chr(byte_data)

		        #print("static buffer_string: ", buffer_string)

		        if buffer_string == 'water':
		        	#print("idx: ", idx)
		        	#print("buffer_string: ", buffer_string)
		        	pass

		        self.static_data_dict[idx] = {"flags": flags, "weight": weight, "layer": layer, "count": count,
		                                      "anim_id": anim_id, "hue": hue, "light_index": light_index,
		                                      "height": height, "name": buffer_string }

	def get_index(self, x, y):
		block = x * 512 + y;

		return self.block_data[block]

	def get_tile_data(self, x, y):
	    im = self.get_index(x, y)
	    self.files_map_reader.seek(im.map_address)
	    header = self.files_map_reader.read_uint32()

	    land_data_list = []
	    static_data_list = []

	    bx = x << 3
	    by = y << 3

	    print("im.map_address: {0}".format(im.map_address))
	    print("by: {0}, by: {1}".format(bx, by))
	    for y in range(0, 8):
	        pos = y << 3
	        tile_y = by + y
	        for x in range(0, 8):
	            tile_id = self.files_map_reader.read_short()
	            z = int8(self.files_map_reader.read_byte())
	            tile_id = (tile_id & 0x3FFF)

	            tile_x = bx + x

	            land_data = self.land_data_dict[tile_id]
	            land_data["game_x"] = tile_x
	            land_data["game_y"] = tile_y

	            #print("land x: {0}, y: {1}, tile_id: {2}, z: {3}, name: {4}".format(x, y, tile_id, z, land_data["name"]))
	            land_data_list.append(land_data)

	    if im.static_address != 0:
	    	static_address = im.static_address
	    	self.files_statics_reader.seek(static_address)

	    	#print("static_address: ", static_address)

	    	for i in range(0, im.static_count):
	    		color = self.files_statics_reader.read_short()
	    		x = self.files_statics_reader.read_byte()
	    		y = self.files_statics_reader.read_byte()
	    		z = self.files_statics_reader.read_byte()
	    		hue = self.files_statics_reader.read_short()

	    		#print("color: ", color)
	    		static_data = self.static_data_dict[color]
	    		static_data["game_x"] = bx + x
	    		static_data["game_y"] = by + y

	    		#print("static_address: ", static_address)

	    		if "wood" in static_data["name"]:
	    			print("Color: {0}, X: {1}, Y: {2}, Name: {3}".format(color, bx + x, by + y, static_data["name"]))
	    			print("static_data: {0}".format(static_data))

	    		static_data_list.append(static_data)

	    		#print("color: ", color)
	    		#print("x: ", x)
	    		#print("y: ", y)
	    		#print("z: ", y)

	    		#static_address += 7

	    	print("")

	    return land_data_list, static_data_list