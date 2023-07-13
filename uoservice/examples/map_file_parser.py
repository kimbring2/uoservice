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

with open(filename, 'rb') as f:
    p = f.read()
    reader = utils.FileReader(BytesIO(p))
    file_size = reader.size
    #print("file_size: ", file_size)
    # file_size:  89965544

    reader.seek(0)

    uop_magic_number = hex(reader.read_uint32())
    #print("uop_magic_number: ", uop_magic_number)

    if uop_magic_number != UOP_MAGIC_NUMBER:
        raise NameError('Bad uop file')

    version = reader.read_uint32()
    format_timestamp = reader.read_uint32()

    next_block = reader.read_long()

    block_size = reader.read_uint32()
    count = reader.read_uint32()

    # version: 5
    # format_timestamp: 4246989891
    # nextBlock: 803465
    # block_size: 1000
    # count: 113
    #print("version: ", version)
    #print("format_timestamp: ", format_timestamp)
    #print("next_block: ", next_block)
    #print("block_size: ", block_size)
    #print("count: ", count)

    print("MapsDefaultSize: ", MapsDefaultSize)

    reader.seek(next_block)
    total = 0;
    real_total = 0;

    while next_block != 0:
        files_count = reader.read_uint32()
        next_block = reader.read_long()
        total += files_count;

        # filesCount: 1000
        # nextBlock: 39188041

        print("files_count: ", files_count)
        print("next_block: ", next_block)
        print("total: ", total)

        for i in range(0, files_count):
            #print("i: ", i)

            offset = reader.read_long()
            header_length = reader.read_uint32()
            compressed_length = reader.read_uint32()
            decompressed_length = reader.read_uint32()
            hash_value = reader.read_long()
            data_hash = reader.read_uint32()
            flag = reader.read_short();
            length = compressed_length if flag == 1 else decompressed_length;

            # offset: 35750238
            # headerLength: 136
            # compressedLength: 1120
            # decompressedLength: 1120
            # hash: 854405468887571177
            # data_hash: 2399011230
            # flag: 0
            # length: 1120
            #print("offset: ", offset)
            #print("header_length: ", header_length)
            #print("compressed_length: ", compressed_length)
            #print("decompressed_length: ", decompressed_length)
            #print("hash_value: ", hash_value)
            #print("data_hash: ", data_hash)
            #print("flag: ", flag)
            #print("")

            if offset == 0:
                continue

            real_total += 1
            offset ++ header_length

            #hashes_dict[hash_value] = UOFileIndex(StartAddress, file_size, offset, 
            #                                      compressedLength, decompressedLength)

        reader.seek(next_block)

    total_entries_count = real_total;

    #reader = utils.FileReader(BytesIO(p))
    reader.seek(33759002)

    #print("reader.remaining: ", reader.remaining)


    start_remaining = reader.remaining
    for i in range(0, 1):
        header = reader.read_uint32()
        print("header: ", header)

        step = 0
        for y in range(0, 8):
            pos = y << 3
            for x in range(0, 8):
                tile_id = reader.read_short();
                z = int8(reader.read_byte());

                tile_id = (tile_id & 0x3FFF);
                print("tile_id: ", tile_id)
                print("z: ", z)

            #cells.append
            #print("pos: ", pos)
            step += 1
        
        #print("step: ", step)

        end_remaining = reader.remaining
        read_length = (start_remaining - end_remaining)
        print("read_length: ", read_length)

print("total_entries_count: ", total_entries_count)