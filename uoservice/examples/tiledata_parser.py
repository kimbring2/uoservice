from io import StringIO
from io import BytesIO
import struct
import utils

file_name = "tiledata.mul"

file = open(file_name, 'rb')
p_file = file.read()
files_reader = utils.FileReader(BytesIO(p_file))

files_reader.seek(0)

land_data_dict = {}

for i in range(0, 512):
    files_reader.read_uint32()

    for j in range(0, 32):
        idx = i * 32 + j
        flags = files_reader.read_long();
        text_id = files_reader.read_short();

        buffer_string = ""
        for k in range(0, 20):
            byte_data = files_reader.read_byte()
            #print("i: {0}, byte_data: {1}".format(i, byte_data))

            if byte_data != 0:
                buffer_string += chr(byte_data)

        #print("buffer_string: ", buffer_string)
        land_data_dict[idx] = {"flags": flags, "text_id": text_id, "name": buffer_string}


#print("land_data_dict: ", land_data_dict)

static_data_dict = {}
for i in range(0, 2048):
    files_reader.read_uint32()

    for j in range(0, 32):
        idx = i * 32 + j
        flags = files_reader.read_long()
        weight = files_reader.read_byte()
        layer = files_reader.read_byte()
        count = files_reader.read_uint32();
        anim_id = files_reader.read_short();
        hue = files_reader.read_short();
        light_index = files_reader.read_short();
        height = files_reader.read_byte();

        buffer_string = ""
        for k in range(0, 20):
            byte_data = files_reader.read_byte()
            #print("i: {0}, byte_data: {1}".format(i, byte_data))

            if byte_data != 0:
                buffer_string += chr(byte_data)

        static_data_dict[idx] = {"flags": flags, "weight": weight, "layer": layer, "count": count,
                                 "anim_id": anim_id, "hue": hue, "light_index": light_index,
                                 "height": height, "name": buffer_string }

print("static_data_dict: ", static_data_dict)
for k, v in static_data_dict.items():
    if v['name'] != '':
        print("k: {0}, v: {1}".format(k, v))






