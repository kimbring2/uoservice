import cv2
import numpy as np
import struct
import ctypes

noop_action = {}
noop_action['action_type'] = 0
noop_action['source_serial'] = 0
noop_action['target_serial'] = 0
noop_action['walk_direction'] = 0
noop_action['index'] = 0
noop_action['amount'] = 0
noop_action['run'] = False

warrior_npc_title_list = ['healer', 'armourer', 'banker', 'blacksmith', 'weaponsmith', 'armourer', 'armourer']

def get_serial_by_name(item_dict, name):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if name in v["name"]:
      return k, keys.index(k)

  return None, None


def get_serial_amount_from_corpse_item_list(corpse_item_dict, name):
  #print("corpse_item_dict: ", corpse_item_dict)
  for k, v in corpse_item_dict.items():
    #print("corpse item {0}: {1}".format(k, v))
    if name in v["name"]:
      return k, v["amount"]

  return None, 0


def get_walk_direction_to_target(player_position, target_position):
  # UpRight = 0, Right = 1, DownRight = 2, Down = 3, DownLeft = 4, Left = 5, UpLeft = 6, Up = 7
  left = False
  right = False
  up = False
  down = False

  direction = -1

  if abs(player_position[0] - target_position[0]) > 1:
    if player_position[0] > target_position[0]:
      left = True
    else:
      right = True

  if abs(player_position[1] - target_position[1]) > 1:
    if player_position[1] > target_position[1]:
      up = True
    else:
      down = True  

  if left:
    direction = 5
  elif right:
    direction = 1
  elif up:
    direction = 7
  elif down:
    direction = 3

  if left and up:
    direction = 6
  elif left and down:
    direction = 4
  elif right and up:
    direction = 0
  elif right and down:
    direction = 2

  return direction


def isVendor(title):
  title_split = title.split(" ")
  for vendor_name in warrior_npc_title_list:
    if vendor_name in title_split:
      index = title_split.index(vendor_name)
      return title_split[index]

  return None


def isTeacher(title):
  title_split = title.split(" ")
  for teacher_name in warrior_npc_title_list:
    if teacher_name in title_split:
      index = title_split.index(teacher_name)
      return title_split[index]

  return None


def isTeacher(title):
  title_split = title.split(" ")
  for teacher_name in warrior_npc_title_list:
    if teacher_name in title_split:
      index = title_split.index(teacher_name)
      return title_split[index]

  return None


def parseItem(itemGrpc):
    itemDict = {}
    for item in itemGrpc :
      itemDict[item.serial] = [item.name, item.amount]

    return itemDict


def parsePlayerStatus(playerStatusGrpc):
  playerStatusDict = {}

  playerStatusDict['str'] = playerStatusGrpc.str
  playerStatusDict['dex'] = playerStatusGrpc.dex
  playerStatusDict['intell'] = playerStatusGrpc.intell
  playerStatusDict['hits'] = playerStatusGrpc.hits
  playerStatusDict['hitsMax'] = playerStatusGrpc.hitsMax
  playerStatusDict['stamina'] = playerStatusGrpc.stamina
  playerStatusDict['staminaMax'] = playerStatusGrpc.staminaMax
  playerStatusDict['mana'] = playerStatusGrpc.mana
  playerStatusDict['gold'] = playerStatusGrpc.gold
  playerStatusDict['physicalResistance'] = playerStatusGrpc.physicalResistance
  playerStatusDict['weight'] = playerStatusGrpc.weight
  playerStatusDict['weightMax'] = playerStatusGrpc.weightMax

  return playerStatusDict


def visObject(screenImage, ObjectData, color):
  radius = 20
  thickness = 2
  for obj in ObjectData:
    try:
      screenImage = cv2.circle(screenImage, (obj.screenX, obj.screenY), radius, color, thickness)
    except:
      print("screenX: {0}, screenY: {1}", obj.screenX, obj.screenY)

  return screenImage


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)

  return result


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


def int32_to_ulong(i):
    return ctypes.c_ulong(i).value


def create_hash(s):
    eax = ecx = edx = ebx = esi = edi = 0
    ebx = edi = esi = int32_to_uint32(len(s) + 0xDEADBEEF)

    i = 0

    s_ord = []
    for char in s:
        s_ord.append(ord(char))

    while True:
        edi = ((s_ord[i + 7] << 24) | (s_ord[i + 6] << 16) | (s_ord[i + 5] << 8) | s_ord[i + 4]) + edi;
        edi = int32_to_uint32(edi)

        esi = ((s_ord[i + 11] << 24) | (s_ord[i + 10] << 16) | (s_ord[i + 9] << 8) | s_ord[i + 8]) + esi;
        esi = int32_to_uint32(esi)

        edx = ((s_ord[i + 3] << 24) | (s_ord[i + 2] << 16) | (s_ord[i + 1] << 8) | s_ord[i]) - esi;
        edx = int32_to_uint32(edx)

        edx = (edx + ebx) ^ (esi >> 28) ^ (esi << 4);
        edx = int32_to_uint32(edx)

        esi += edi;
        esi = int32_to_uint32(esi)

        edi = (edi - edx) ^ (edx >> 26) ^ (edx << 6);
        edi = int32_to_uint32(edi)

        edx += esi;
        edx = int32_to_uint32(edx)

        esi = (esi - edi) ^ (edi >> 24) ^ (edi << 8);
        esi = int32_to_uint32(esi)

        edi += edx;
        edi = int32_to_uint32(edi)

        ebx = (edx - esi) ^ (esi >> 16) ^ (esi << 16);
        ebx = int32_to_uint32(ebx)

        esi += edi;
        esi = int32_to_uint32(esi)

        edi = (edi - ebx) ^ (ebx >> 13) ^ (ebx << 19);
        edi = int32_to_uint32(edi)

        ebx += esi;
        ebx = int32_to_uint32(ebx)

        esi = (esi - edi) ^ (edi >> 28) ^ (edi << 4);
        esi = int32_to_uint32(esi)

        edi += ebx;
        edi = int32_to_uint32(edi)

        i += 12

        if i + 12 >= len(s):
            #i += 12
            break

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
    esi = int32_to_uint32(esi)

    ecx = (esi ^ ebx) - ((esi >> 21) ^ (esi << 11))
    ecx = int32_to_uint32(ecx)

    edi = (edi ^ ecx) - ((ecx >> 7) ^ (ecx << 25))
    edi = int32_to_uint32(edi)

    esi = (esi ^ edi) - ((edi >> 16) ^ (edi << 16))
    esi = int32_to_uint32(esi)

    edx = (esi ^ ecx) - ((esi >> 28) ^ (esi << 4))
    edx = int32_to_uint32(edx)

    edi = (edi ^ edx) - ((edx >> 18) ^ (edx << 14))
    edi = int32_to_uint32(edi)

    eax = (esi ^ edi) - ((edi >> 8) ^ (edi << 24))
    eax = int32_to_uint32(eax)

    if s == "build/map1legacymul/00000104.dat":
        pass

    return_value = (edi << 32) | eax
    return_value = int32_to_ulong(return_value)

    return return_value


class IndexMap():
    def __init__(self, map_address, static_address, static_count, 
                 original_map_address, original_static_address, original_static_count):
        self.map_address = map_address;
        self.static_address = static_address;
        self.static_count = static_count;
        self.original_map_address = original_map_address;
        self.original_static_address = original_static_address;
        self.original_static_count = original_static_count;