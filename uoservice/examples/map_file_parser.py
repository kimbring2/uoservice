from io import StringIO
from io import BytesIO
import struct
import utils
from numpy import int8

files_map_name = "map1LegacyMUL.uop"
files_statics_name = "statics0.mul"
files_index_statics_name = "staidx1.mul"

UOP_MAGIC_NUMBER = hex(0x50594d)
_has_extra = False
total_entries_count = 0;
hashes_dict = {}
file_size = 0

MapsDefaultSize = {7168 >> 3, 4096 >> 3}

files_map = open(files_map_name, 'rb')
p_files_map = files_map.read()
files_map_reader = utils.FileReader(BytesIO(p_files_map))
files_map_size = files_map_reader.size

files_statics = open(files_statics_name, 'rb')
p_files_statics = files_statics.read()
files_statics_reader = utils.FileReader(BytesIO(p_files_statics))
files_statics_size = files_statics_reader.size

files_index_statics = open(files_index_statics_name, 'rb')
p_files_index_statics = files_index_statics.read()
files_index_statics_reader = utils.FileReader(BytesIO(p_files_index_statics))
files_index_statics_size = files_index_statics_reader.size

files_map_reader.seek(0)
files_statics_reader.seek(0)
files_index_statics_reader.seek(0)

uop_magic_number = hex(files_map_reader.read_uint32())

if uop_magic_number != UOP_MAGIC_NUMBER:
    raise NameError('Bad uop file')

version = files_map_reader.read_uint32()
format_timestamp = files_map_reader.read_uint32()
next_block = files_map_reader.read_long()
block_size = files_map_reader.read_uint32()
count = files_map_reader.read_uint32()

files_map_reader.seek(next_block)
total = 0;
real_total = 0;

while next_block != 0:
    files_count = files_map_reader.read_uint32()
    next_block = files_map_reader.read_long()
    total += files_count;

    for i in range(0, files_count):
        offset = files_map_reader.read_long()
        header_length = files_map_reader.read_uint32()
        compressed_length = files_map_reader.read_uint32()
        decompressed_length = files_map_reader.read_uint32()
        hash_value = files_map_reader.read_long()
        data_hash = files_map_reader.read_uint32()
        flag = files_map_reader.read_short();
        length = compressed_length if flag == 1 else decompressed_length;

        #print("i: {0}, offset: {1}".format(i, offset))

        if offset == 0:
            continue

        real_total += 1
        offset += header_length

        hashes_dict[hash_value] = utils.UOFileIndex(file_size, offset, compressed_length, 
                                                    decompressed_length)

    files_map_reader.seek(next_block)

total_entries_count = real_total;
print("total_entries_count: ", total_entries_count)

pattern = "build/map1legacymul/{:08d}.dat"

Entries = []
for i in range(0, total_entries_count):
    file = pattern.format(i)
    hash_value = utils.CreateHash(file)
    hash_data = hashes_dict[hash_value]
    Entries.append(hash_data)

mapblocksize = 196
staticidxblocksize = 12
staticblocksize = 7

uopoffset = 0
file_number = -1;
maxblockcount = 896 * 512

print("len(Entries): ", len(Entries))

start_remaining = files_map_reader.remaining
for block in range(0, maxblockcount):
    realmapaddress = 0
    realstaticaddress = 0
    realstaticcount = 0

    blocknum = block;
    blocknum &= 4095;

    shifted = block >> 12;

    if file_number != shifted:
        file_number = shifted

        if shifted < len(Entries):
            uopoffset = Entries[shifted].offset

    address = uopoffset + (blocknum * mapblocksize);

    if address < files_map_size:
        realmapaddress = address

    '''
    #files_map_reader.seek(33759002)
    files_map_reader.seek(realmapaddress)

    header = files_map_reader.read_uint32()
    #print("header: ", header)
    for y in range(0, 8):
        pos = y << 3
        for x in range(0, 8):
            tile_id = files_map_reader.read_short();
            z = int8(files_map_reader.read_byte());
            tile_id = (tile_id & 0x3FFF);
            #print("tile_id: ", tile_id)
            #print("z: ", z)

    end_remaining = files_map_reader.remaining
    read_length = (start_remaining - end_remaining)
    '''

    stidxaddress = (block * staticidxblocksize);

    files_index_statics_reader.seek(stidxaddress)

    position = files_index_statics_reader.read_uint32()
    size = files_index_statics_reader.read_uint32()
    unknown = files_index_statics_reader.read_uint32()

    if stidxaddress < files_index_statics_size and size > 0 and position != 0xFFFFFFFF:
        address1 = position
        if address1 < files_statics_size:
            realstaticaddress = address1;
            realstaticcount = int(size / staticblocksize)
            #realstaticcount = utils.int32_to_uint32(realstaticcount)

            #if realstaticcount != 0 and block < 20000:
            #    print("block: {0}, size: {1}, realstaticcount: {2}".format(block, size, realstaticcount))

            if realstaticcount > 1024:
                realstaticcount = 1024;

    if block % 1000 == 0 and realstaticcount != 0:
        print("block: {0}, realmapaddress: {1}, realstaticaddress: {2}, realstaticcount: {3}".format(block, 
              realmapaddress, realstaticaddress, realstaticcount))
        pass


