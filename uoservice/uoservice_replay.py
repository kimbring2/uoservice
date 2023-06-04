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
 

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
surface = pygame.display.set_mode([1280,1370])
clock = pygame.time.Clock()

grpc_port = 60051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)


def isVendor(title):
  vendor_name_list = ['healer', 'armourer']
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


mobile_object_data_list = []

def parse_response(step, response):
  global mobile_object_data_list

  # Action data parse
  player_actions = response.replayActions
  action_type = player_actions.actionType
  mobile_serial = player_actions.mobileSerial
  item_serial = player_actions.itemSerial
  index = player_actions.index
  amount = player_actions.amount

  # Commnon data parse
  mobile_data = response.mobileList.mobile
  equipped_item_data = response.equippedItemList.item
  backpack_item_data = response.backpackItemList.item
  corpse_item_data = response.corpseItemList.item
  popup_menu_data = response.popupMenuList.menu
  cliloc_data = response.clilocDataList.clilocData

  # Game object data parse
  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameSimpleObject
  vendor_item_data = response.vendorItemObjectList.gameObject
  static_object_screen_x_data = response.staticObjectInfoList.screenXs
  static_object_screen_y_data = response.staticObjectInfoList.screenYs

  # Player stat data parse
  player_status_data = response.playerStatus
  player_skills_data = response.playerSkillList.skills

  # Save the parsed data for visualize
  mobile_object_data_list.append(mobile_object_data)


def vis_object(mobile_object_data):
  screen_image = np.zeros((1720,1370,3), dtype=np.uint8)

  for obj in mobile_object_data:
    screen_image[int(obj.screenX), int(obj.screenY), 0] = 255
    screen_image[int(obj.screenX), int(obj.screenY), 1] = 255
    screen_image[int(obj.screenX), int(obj.screenY), 2] = 255

  surf = pygame.surfarray.make_surface(screen_image)
  surface.blit(surf, (0,0))
  pygame.display.flip()


def vis_response():
  print("vis_response()")
  global mobile_object_data_list
  print("len(mobile_object_data_list): ", len(mobile_object_data_list))

  replay_step = 0
  while True:
    #print("while True")

    # creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False

    keys = pygame.key.get_pressed()

    #print("keys[pygame.K_LEFT]:: ", keys[pygame.K_LEFT])
    #print("keys[pygame.K_RIGHT]:: ", keys[pygame.K_RIGHT])

    if keys[pygame.K_LEFT]:
      if replay_step >= 1:
        replay_step -= 1
        print("replay_step: ", replay_step)
      else:
        print("This is start step of replay")

    if keys[pygame.K_RIGHT]:
      if replay_step < len(mobile_object_data_list) - 1:
        replay_step += 1
        print("replay_step: ", replay_step)
      else:
        print("This is end step of replay")

    vis_object(mobile_object_data_list[replay_step])
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
  replay_file_name = 'kimbring2-2023-6-4-20-21-39.uoreplay'

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