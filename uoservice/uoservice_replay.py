# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` UoService.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. UoService.proto --proto_path /home/kimbring2/uoservice/uoservice/protos/

from __future__ import print_function
from concurrent import futures

import grpc
import UoService_pb2
import UoService_pb2_grpc

import io
from PIL import Image
import time
import numpy as np
import cv2
import random
import pygame
import sys
from enum import Enum
 
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

screen_width = 1370
screen_height = 1280

main_surface = pygame.display.set_mode([screen_width + 500, screen_height + 350])
screen_surface = pygame.Surface((screen_width, screen_height))
equip_item_surface = pygame.Surface((600, screen_height))
status_surface = pygame.Surface((screen_width, 350))

clock = pygame.time.Clock()

grpc_port = 60051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)


class Layers(Enum):
  Invalid = 0
  OneHanded = 1
  TwoHanded = 2
  Shoes = 3
  Pants = 4
  Shirt = 5
  Helmet = 6
  Gloves = 7
  Ring = 8
  Talisman = 9
  Necklace = 10
  Hair = 11
  Waist = 12
  Torso = 13
  Bracelet = 14
  Face = 15
  Beard = 16
  Tunic = 17
  Earrings = 18
  Arms = 19
  Cloak = 20
  Backpack = 21
  Robe = 22
  Skirt = 23
  Legs = 24
  Mount = 25
  ShopBuyRestock = 26
  ShopBuy = 27
  ShopSell = 28
  Bank = 29

print(Layers(20).name)

action_type_list = []
walk_direction_list = []
mobile_serial_list = []
item_serial_list = []
index_list = []
amount_list = []

mobile_object_data_list = []
player_mobile_object_data_list = []

equipped_item_list = []
backpack_item_list = []

player_status_list = []

def parse_response(step, response):
  global action_type_list
  global walk_direction_list
  global mobile_serial_list
  global item_serial_list
  global index_list
  global amount_list

  global player_mobile_object_data_list
  global mobile_object_data_list

  global equipped_item_list
  global backpack_item_list

  global player_status_list

  # Action data parse
  player_actions = response.replayActions
  action_type = player_actions.actionType
  walk_direction = player_actions.walkDirection
  mobile_serial = player_actions.mobileSerial
  item_serial = player_actions.itemSerial
  index = player_actions.index
  amount = player_actions.amount

  action_type_list.append(action_type)
  walk_direction_list.append(walk_direction)
  mobile_serial_list.append(mobile_serial)
  item_serial_list.append(item_serial)
  index_list.append(index)
  amount_list.append(amount)

  # Commnon data parse
  mobile_data = response.mobileList.mobile
  equipped_item_data = response.equippedItemList.item
  backpack_item_data = response.backpackItemList.item
  corpse_item_data = response.corpseItemList.item
  popup_menu_data = response.popupMenuList.menu
  cliloc_data = response.clilocDataList.clilocData

  equipped_item_list.append(equipped_item_data)
  backpack_item_list.append(backpack_item_data)

  # Game object data parse
  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameSimpleObject
  vendor_item_data = response.vendorItemObjectList.gameObject
  static_object_screen_x_data = response.staticObjectInfoList.screenXs
  static_object_screen_y_data = response.staticObjectInfoList.screenYs

  player_mobile_object_data_list.append(player_mobile_object_data)
  mobile_object_data_list.append(mobile_object_data)

  # Player stat data parse
  player_status_data = response.playerStatus
  player_skills_data = response.playerSkillList.skills

  player_status_list.append(player_status_data)


def vis_object(screen_image, mobile_object_data, color):
  for obj in mobile_object_data:
    screen_image[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 0] = color[0]
    screen_image[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 1] = color[1]
    screen_image[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 2] = color[2]

  return screen_image


def parse_player_status(player_status_grpc):
  player_status_dict = {}
  '''
  str: 100
  dex: 62
  intell: 133
  hits: 121
  hitsMax: 121
  stamina: 70
  staminaMax: 70
  mana: 148
  gold: 47196
  physicalResistance: 88
  weight: 677
  weightMax: 450
  '''
  player_status_dict['str'] = player_status_grpc.str
  player_status_dict['dex'] = player_status_grpc.dex
  player_status_dict['intell'] = player_status_grpc.intell
  player_status_dict['hits'] = player_status_grpc.hits
  player_status_dict['hitsMax'] = player_status_grpc.hitsMax
  player_status_dict['stamina'] = player_status_grpc.stamina
  player_status_dict['staminaMax'] = player_status_grpc.staminaMax
  player_status_dict['mana'] = player_status_grpc.mana
  player_status_dict['gold'] = player_status_grpc.gold
  player_status_dict['physicalResistance'] = player_status_grpc.physicalResistance
  player_status_dict['weight'] = player_status_grpc.weight
  player_status_dict['weightMax'] = player_status_grpc.weightMax

  return player_status_dict


def vis_response():
  print("vis_response()")
  global action_type_list
  global walk_direction_list
  global mobile_serial_list
  global item_serial_list
  global index_list
  global amount_list

  global player_mobile_object_data_list
  global mobile_object_data_list

  global equipped_item_list
  global backpack_item_list

  global player_status_list

  print("len(mobile_object_data_list): ", len(mobile_object_data_list))

  replay_step = 0
  while True:
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      if replay_step >= 1:
        replay_step -= 1
        #print("replay_step: ", replay_step)
      else:
        print("This is start step of replay")

    if keys[pygame.K_RIGHT]:
      if replay_step < len(mobile_object_data_list) - 1:
        replay_step += 1
        #print("replay_step: ", replay_step)
      else:
        print("This is end step of replay")

    screen_image = np.zeros((172,137,3), dtype=np.uint8)

    player_mobile_object_data = player_mobile_object_data_list[replay_step]
    #print("player_mobile_object_data: ", player_mobile_object_data)

    screen_image = vis_object(screen_image, mobile_object_data_list[replay_step], (255, 0, 0))
    screen_image = vis_object(screen_image, player_mobile_object_data_list[replay_step], (0, 255, 0))
    screen_image = cv2.resize(screen_image, (1370, 1280), interpolation = cv2.INTER_AREA)
    screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
    screen_image = cv2.flip(screen_image, 1)

    surf = pygame.surfarray.make_surface(screen_image)
    screen_surface.blit(surf, (0, 0))

    font = pygame.font.Font('freesansbold.ttf', 32)
    replay_step_surface = font.render("step: " + str(replay_step), True, (255, 255, 255))
    screen_surface.blit(replay_step_surface, (0, 0))

    action_type_surface = font.render("action type: " + str(action_type_list[replay_step]), True, (255, 255, 255))
    screen_surface.blit(action_type_surface, (0, 30))

    action_type_surface = font.render("walk direction: " + str(walk_direction_list[replay_step]), True, (255, 255, 255))
    screen_surface.blit(action_type_surface, (0, 60))

    pygame.draw.line(screen_surface, (255, 255, 255), (screen_width - 1, 0), (screen_width - 1, screen_height))
    pygame.draw.line(screen_surface, (255, 255, 255), (0, screen_height - 1), (screen_width, screen_height - 1))

    for backpack_item in backpack_item_list[replay_step]:
      #print("backpack_item: ", backpack_item)
      #replay_step_surface = font.render("step: " + str(replay_step), True, (255, 255, 255))
      #screen_surface.blit(replay_step_surface, (0, 0))
      pass

    equip_item_surface.fill(((0, 0, 0)))
    font = pygame.font.Font('freesansbold.ttf', 32)
    item_surface = font.render("Equip Items", True, (255, 0, 255))
    equip_item_surface.blit(item_surface, (0, 0))
    for i, equipped_item in enumerate(equipped_item_list[replay_step]):
      #print("i: ", i)
      #print("equipped_item.name: ", equipped_item.name)
      font = pygame.font.Font('freesansbold.ttf', 20)
      item_surface = font.render(str(Layers(int(equipped_item.layer)).name) + ": " + str(equipped_item.name), True, (255, 255, 255))
      equip_item_surface.blit(item_surface, (0, 25 * (i + 1) + 20))

    player_status_grpc = player_status_list[replay_step]
    player_status_dict = parse_player_status(player_status_grpc)
    status_surface.fill(((0, 0, 0)))
    font = pygame.font.Font('freesansbold.ttf', 25)
    text_surface = font.render("Player Status", True, (255, 0, 255))
    status_surface.blit(text_surface, (0, 0))
    for i, k in enumerate(player_status_dict):
      #print("k: ", k)
      #print("player_status_dict[k]: ", player_status_dict[k])
      font = pygame.font.Font('freesansbold.ttf', 16)
      text_surface = font.render(str(k) + ": " + str(player_status_dict[k]), True, (255, 255, 255))
      status_surface.blit(text_surface, (0, 20 * (i + 1) + 10))

    #print("")

    #main_surface = pygame.display.set_mode([width, height])
    #screen_surface = pygame.Surface((width - 600, height))
    #equip_item_surface = pygame.Surface((600, height))

    main_surface.blit(screen_surface, (0, 0))
    main_surface.blit(equip_item_surface, (screen_width, 0))
    main_surface.blit(status_surface, (0, screen_height))

    pygame.display.update()

    clock.tick(100)

  '''
  vendor_dict = {}
  vendor_item_dict = {}
  player_skills_dict = {}

  #mobile_data = response.mobileList.mobile
  #equipped_item_data = response.equippedItemList.item
  #backpack_item_data = response.backpackItemList.item
  #cliloc_data = response.clilocDataList.clilocData

  popup_menu = response.popupMenuList
  player_status_data = response.playerStatus
  player_gold = player_status_data.gold
  player_actions = response.replayActions

  if player_actions.actionType != 0:
    print("step: ", step)
    print("player_actions.actionType: ", player_actions.actionType)
    print("player_actions.mobileSerial: ", player_actions.mobileSerial)
    print("player_actions.itemSerial: ", player_actions.itemSerial)
    print("")

  if popup_menu:
    #print("step: ", step)
    #print("popup_menu: ", popup_menu)
    #print("")
    pass

  player_skills_data = response.playerSkillList.skills
  for skill in player_skills_data:
    player_skills_dict[skill.name] = [skill.index, skill.isClickable, skill.value, skill.base, skill.cap, skill.lock]  

  if 'Swordsmanship' in player_skills_dict:
    #print("step: ", step)
    #print("player_skills_dict['Swordsmanship']: ", player_skills_dict['Swordsmanship'])
    #print("")
    pass

  for data in cliloc_data:
    cliloc_dict = {}
    cliloc_dict['text'] = data.text
    cliloc_dict['affix'] = data.affix

  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameSimpleObject

  static_object_screen_x_data = response.staticObjectInfoList.screenXs
  static_object_screen_y_data = response.staticObjectInfoList.screenYs

  vendor_item_data = response.vendorItemObjectList.gameObject

  vendor_item_dict = {}
  for obj in vendor_item_data:
    vendor_item_dict[obj.serial] = [obj.name, obj.type, obj.price, obj.amount, obj.title]

  for k in vendor_item_dict.keys():
    print("vendor_item_dict: ", k)
    break

  #print("backpack_item_data: ", backpack_item_data)
  #print("item_dropable_land_data: ", item_dropable_land_data)

  screen_image = np.zeros((172,137,4), dtype=np.uint8)

  for obj in item_object_data:
    if 'Door' in obj.name:
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 153
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255
    else:
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  for obj in mobile_object_data:
    vendor_title = isVendor(obj.title)
    if vendor_title:
      obj.title = vendor_title
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

      vendor_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
    else:
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

    teacher_title = isTeacher(obj.title)
    if teacher_title:
      teacher_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, teacher_title]

  for obj in player_mobile_object_data:
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 0
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  for i in range(0, len(static_object_screen_x_data)):
    screen_image[int(static_object_screen_x_data[i] / 10), int(static_object_screen_y_data[i] / 10), 0] = 120
    screen_image[int(static_object_screen_x_data[i] / 10), int(static_object_screen_y_data[i] / 10), 1] = 120
    screen_image[int(static_object_screen_x_data[i] / 10), int(static_object_screen_y_data[i] / 10), 2] = 120

  vis = False
  if vis:
    dim = (1600, 1280)
    screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)
    screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
    screen_image = cv2.flip(screen_image, 1)
    cv2.imshow('screen_image_' + str(grpc_port), screen_image)
    cv2.waitKey(1)

  for mobile in mobile_data:
    if mobile.x >= 1600 or mobile.y >= 1280:
      continue

    if mobile.race == 1:
      color = (0, 255, 0)
    elif mobile.race == 0:
      color = (0, 0, 255)
    else:
      color = (255, 0, 0)
  '''


def main():
  replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay/'
  replay_file_name = 'kimbring2-2023-6-5-00-02-13.uoreplay'

  stub.ReadMPQFile(UoService_pb2.Config(replayName=replay_path + replay_file_name))

  replay_step = 0
  while True:
    res = stub.ReadReplay(UoService_pb2.Config(name="test"))

    parse_response(replay_step, res)

    #print("res.replayParseEnd: ", res.replayParseEnd)
    if res.replayParseEnd:
      break

    replay_step += 1

  vis_response()


if __name__ == '__main__':
  main()