import struct
import ctypes


class FileReader(object):
    def __init__(self, stream):
        self.stream = stream
        stream.seek(0, 2)
        self.size = stream.tell()
        self.remaining = self.size
        stream.seek(0)

        self.pos = 0
        self.bit_count = 0
        self.bit_val = 0

    def seek(self, position):
        self.stream.seek(position)

    def more(self):
        return self.remaining > 0

    def nibble(self, length):
        self.remaining -= length
        if self.remaining < 0:
            raise ValueError("Not enough data")

    def read_byte(self):
        self.nibble(1)

        value = self.stream.read(1)
        #print("value: ", value)

        value = int.from_bytes(value, "little")
        return value

        #return float(self.stream.read(1))

    def read(self, length=None):
        if length is None:
            length = self.remaining

        self.nibble(length)

        return self.stream.read(length)

    def read_int32(self):
        self.nibble(4)

        return struct.unpack("i", self.stream.read(4))[0]

    def read_uint32(self):
        self.nibble(4)

        return struct.unpack("I", self.stream.read(4))[0]

    def read_short(self):
        value = self.read_bytes(2)
        value = int.from_bytes(value, "little")

        return value

    def read_long(self):
        value = self.read_bytes(8)
        value = int.from_bytes(value, "little")

        return value

    def read_boolean(self):
        return self.read_bits(1) == 1

    def next_byte(self):
        self.pos += 1
        if self.pos > self.size:
            print('nextByte: insufficient buffer ({} of {})'.format(self.pos, self.size))
        
        value = self.stream.read(1)
        value = ord(value)

        return value

    def read_byte_test(self):
        if self.bit_count == 0:
            return self.next_byte()

        return self.read_bits(8)

    def read_bytes(self, n):
        buf = bytearray()
        for i in range(n):
            data = self.read_bits(8)
            buf.extend(bytes([data]))

        return bytes(buf)

    def read_bits(self, n):
        while n > self.bit_count:
            nextByte = self.next_byte()
            self.bit_val |= nextByte << self.bit_count
            self.bit_count += 8

        x = (self.bit_val & ((1 << n) - 1))
        self.bit_val >>= n
        self.bit_count -= n
        
        return x


class UOFileIndex():
    def __init__(self, file_size, offset, compressed_length, decompressed_length, 
                 width=0, height=0, hue=0):
        self.file_size = file_size;
        self.offset = offset;
        self.compressed_length = compressed_length;
        self.decompressed_length = decompressed_length;
        self.width = width;
        self.height = height;
        self.hue = hue;
        self.anim_offset = 0;


def int32_to_uint32(i):
    return ctypes.c_uint32(i).value


def CreateHash(s):
    eax = ecx = edx = ebx = esi = edi = 0
    ebx = edi = esi = int32_to_uint32(len(s) + 0xDEADBEEF)

    # ebx: 3735928591
    if s == "build/map1legacymul/00000104.dat":
        print("edi: ", edi)
        print("len(s): ", len(s))

    i = 0

    s_ord = []
    for char in s:
        #print("char: ", char)
        s_ord.append(ord(char))

    while True:
        edi = ((s_ord[i + 7] << 24) | (s_ord[i + 6] << 16) | (s_ord[i + 5] << 8) | s_ord[i + 4]) + edi;
        edi = int32_to_uint32(edi)

        #print("type(edi): ", type(edi))
        if s == "build/map1legacymul/00000104.dat":
            print("i: {0}, edi: {1}".format(i, edi))

        esi = ((s_ord[i + 11] << 24) | (s_ord[i + 10] << 16) | (s_ord[i + 9] << 8) | s_ord[i + 8]) + esi;
        esi = int32_to_uint32(esi)

        edx = ((s_ord[i + 3] << 24) | (s_ord[i + 2] << 16) | (s_ord[i + 1] << 8) | s_ord[i]) - esi;
        edx = int32_to_uint32(edx)

        edx = (edx + ebx) ^ (esi >> 28) ^ (esi << 4);
        esi += edi;
        edi = (edi - edx) ^ (edx >> 26) ^ (edx << 6);
        edx += esi;
        esi = (esi - edi) ^ (edi >> 24) ^ (edi << 8);
        edi += edx;
        ebx = (edx - esi) ^ (esi >> 16) ^ (esi << 16);
        esi += edi;
        edi = (edi - ebx) ^ (ebx >> 13) ^ (ebx << 19);
        ebx += esi;
        esi = (esi - edi) ^ (edi >> 28) ^ (edi << 4);
        edi += ebx;

        i += 12

        if i + 12 >= len(s):
            #i += 12
            break

    #eax: 0
    #ecx: 0
    #edx: 2016057418
    #ebx: 3029140339
    #esi: 3187656610
    #edi: 1094223076
    if s == "build/map1legacymul/00000104.dat":
        print("eax: ", eax)
        print("ecx: ", ecx)
        print("edx: ", edx)
        print("ebx: ", ebx)
        print("esi: ", esi)
        print("edi: ", edi)

    switch_value = len(s) - i
    #print("switch_value: ", switch_value)

    # switch_value == 8
    #esi += s_ord[i + 11] << 24
    #esi += s_ord[i + 10] << 16
    #esi += s_ord[i + 9] << 8
    #esi += s_ord[i + 8]
    edi += int32_to_uint32(s_ord[i + 7] << 24)
    edi += int32_to_uint32(s_ord[i + 6] << 16)
    edi += int32_to_uint32(s_ord[i + 5] << 8)
    edi += s_ord[i + 4]
    ebx += int32_to_uint32(s_ord[i + 3] << 24)
    ebx += int32_to_uint32(s_ord[i + 2] << 16)
    ebx += int32_to_uint32(s_ord[i + 1] << 8)
    ebx += s_ord[i];

    esi = (esi ^ edi) - ((edi >> 18) ^ (edi << 14))
    ecx = (esi ^ ebx) - ((esi >> 21) ^ (esi << 11))
    edi = (edi ^ ecx) - ((ecx >> 7) ^ (ecx << 25))
    esi = (esi ^ edi) - ((edi >> 16) ^ (edi << 16))
    edx = (esi ^ ecx) - ((esi >> 28) ^ (esi << 4))
    edi = (edi ^ edx) - ((edx >> 18) ^ (edx << 14))
    eax = (esi ^ edi) - ((edi >> 8) ^ (edi << 24))

    return_value = (edi << 32) | eax
    if s == "build/map1legacymul/00000104.dat":
        print("return_value: ", return_value)

    return return_value