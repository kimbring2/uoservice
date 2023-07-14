from io import StringIO
from io import BytesIO
import struct
import utils
from numpy import int8

filename = "map1LegacyMUL.uop"
UOP_MAGIC_NUMBER = hex(0x50594d)
_has_extra = False
total_entries_count = 0;
hashes_dict = {}
file_size = 0

MapsDefaultSize = {7168 >> 3, 4096 >> 3}

f = open(filename, 'rb')

p = f.read()
reader = utils.FileReader(BytesIO(p))
file_size = reader.size

reader.seek(0)

uop_magic_number = hex(reader.read_uint32())

if uop_magic_number != UOP_MAGIC_NUMBER:
    raise NameError('Bad uop file')

version = reader.read_uint32()
format_timestamp = reader.read_uint32()
next_block = reader.read_long()
block_size = reader.read_uint32()
count = reader.read_uint32()

reader.seek(next_block)
total = 0;
real_total = 0;

while next_block != 0:
    files_count = reader.read_uint32()
    next_block = reader.read_long()
    total += files_count;

    for i in range(0, files_count):
        offset = reader.read_long()
        header_length = reader.read_uint32()
        compressed_length = reader.read_uint32()
        decompressed_length = reader.read_uint32()
        hash_value = reader.read_long()
        data_hash = reader.read_uint32()
        flag = reader.read_short();
        length = compressed_length if flag == 1 else decompressed_length;

        #print("i: {0}, offset: {1}".format(i, offset))

        if offset == 0:
            continue

        real_total += 1
        offset += header_length

        hashes_dict[hash_value] = utils.UOFileIndex(file_size, offset, compressed_length, 
                                                    decompressed_length)

    reader.seek(next_block)

total_entries_count = real_total;
print("total_entries_count: ", total_entries_count)

pattern = "build/map1legacymul/{:08d}.dat"

Entries = []
for i in range(0, total_entries_count):
    file = pattern.format(i)
    hash_value = utils.CreateHash(file)
    hash_data = hashes_dict[hash_value]
    Entries.append(hash_data)

uopoffset = 0
file_number = -1;
maxblockcount = 896 * 512
maxblockcount = 5

print("len(Entries): ", len(Entries))

start_remaining = reader.remaining
for block in range(0, maxblockcount):
    blocknum = block;

    blocknum &= 4095;
    shifted = block >> 12;

    if file_number != shifted:
        file_number = shifted

        if shifted < len(Entries):
            uopoffset = Entries[shifted].offset
            print("block: {0}, shifted: {1}, uopoffset: {2}".format(block, shifted, uopoffset))

    reader.seek(33759002)

    header = reader.read_uint32()
    #print("header: ", header)
    for y in range(0, 8):
        pos = y << 3
        for x in range(0, 8):
            tile_id = reader.read_short();
            z = int8(reader.read_byte());

            tile_id = (tile_id & 0x3FFF);
            #print("tile_id: ", tile_id)
            #print("z: ", z)

    end_remaining = reader.remaining
    read_length = (start_remaining - end_remaining)
    #print("read_length: ", read_length)
