import cv2

noop_action = {}
noop_action['action_type'] = 0
noop_action['item_serial'] = 0
noop_action['mobile_serial'] = 0
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


def get_serial_amount_from_corpse_item_list(corpse_item_list, name):
  for corpse_item in corpse_item_list:
    if name in corpse_item[1]:
      return corpse_item[0], corpse_item[3]

  return None, 0


def get_walk_direction_to_target(player_position, target_position):
  print("player_position: ", player_position)
  print("target_position: ", target_position)
  print("")

  # UpRight = 0, Right = 1, DownRight = 2, Down = 3, DownLeft = 4, Left = 5, UpLeft = 6, Up = 7
  left = False
  right = False
  up = False
  down = False

  direction = -1

  if abs(player_position[0] - target_position[0]) > 10:
    if player_position[0] > target_position[0]:
      left = True
    else:
      right = True

  if abs(player_position[1] - target_position[1]) > 10:
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