def get_serial_by_name(item_dict, name):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if name in v[0]:
      return k, keys.index(k)

  return None, None


def isVendor(title):
  vendor_name_list = ['healer', 'armourer', 'banker']
  title_split = title.split(" ")
  for vendor_name in vendor_name_list:
    if vendor_name in title_split:
      index = title_split.index(vendor_name)
      return title_split[index]

  return None


def isTeacher(title):
  teacher_name_list = ['warrior']
  title_split = title.split(" ")
  for teacher_name in teacher_name_list:
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
  for obj in ObjectData:
    try:
      screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 0] = color[0]
      screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 1] = color[1]
      screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 2] = color[2]
    except:
      print("screenX: {0}, screenY: {1}", obj.screenX, obj.screenY)

  return screenImage