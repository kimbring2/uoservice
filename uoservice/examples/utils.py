import struct


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

        return ord(self.stream.read(1))

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

'''
StartAddress,
(uint) Length,
offset + 8,
compressedLength - 8,
decompressedLength,
extra1,
extra2
'''

class UOFileIndex():
    def __init__(self, address, fileSize, offset, length, decompressed, width=0, height=0, hue=0):
        '''
        IntPtr address,
        uint fileSize,
        long offset,
        int length,
        int decompressed,
        short width = 0,
        short height = 0,
        ushort hue = 0
        '''

        self.Address = address;
        self.FileSize = fileSize;
        self.Offset = offset;
        self.Length = length;
        self.DecompressedLength = offset;
        self.Width = width;
        self.Height = height;
        self.Hue = hue;
        self.AnimOffset = 0;