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


grpc_port = 60051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)

selected_target_serial = None
player_serial = None


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


mountable_list = ['a hellsteed', 'a horse']

def parse_response(response):
  global grpc_port
  global selected_target_serial
  global player_serial
  global mountable_list

  player_skills_dict = {}
  mobile_dict = {}
  mountable_mobile_dict = {}
  world_item_dict = {}
  equipped_item_dict = {}
  backpack_item_dict = {}
  ground_item_dict = {}
  corpse_dict = {}
  corpse_item_dict = {}
  vendor_dict = {}
  vendor_item_dict = {}
  teacher_dict = {}
  player_skill_dict = {}
  popup_menu_list = []
  cliloc_data_list = []

  mobile_data = response.mobileList.mobile
  equipped_item_data = response.equippedItemList.item
  backpack_item_data = response.backpackItemList.item
  corpse_item_data = response.corpseItemList.item
  popup_menu_data = response.popupMenuList.menu

  player_status_data = response.playerStatus
  #print("player_status_data: ", player_status_data)

  player_skills_data = response.playerSkillList.skills
  for skill in player_skills_data:
    '''
    print("skill.name: ", skill.name)
    print("skill.index: ", skill.index)
    print("skill.isClickable: ", skill.isClickable)
    print("skill.value: ", skill.value)
    print("skill.base: ", skill.base)
    print("skill.cap: ", skill.cap)
    print("skill.lock: ", skill.lock)
    print("")
    '''
    player_skills_dict[skill.name] = [skill.index, skill.isClickable, skill.value, skill.base, skill.cap, skill.lock]

  static_object_screen_x_data = response.staticObjectInfoList.screenXs
  static_object_screen_y_data = response.staticObjectInfoList.screenYs
  #print("static_object_screen_x_data: ", static_object_screen_x_data)
  #print("static_object_screen_y_data: ", static_object_screen_y_data)

  vendor_item_data = response.vendorItemObjectList.gameObject

  cliloc_data = response.clilocDataList.clilocData
  for data in cliloc_data:
    cliloc_dict = {}
    cliloc_dict['text'] = data.text
    cliloc_dict['affix'] = data.affix
    cliloc_data_list.append(cliloc_dict)

  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameSimpleObject

  for menu_data in popup_menu_data:
    popup_menu_list.append(menu_data)

  screen_image = np.zeros((172,137,4), dtype=np.uint8)

  for obj in item_object_data:
    ground_item_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

    if obj.isCorpse:
      corpse_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

    if 'Door' in obj.name:
      #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
      #    format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 153
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255
    else:
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  for obj in vendor_item_data:
    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
    #      format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
    vendor_item_dict[obj.serial] = [obj.name, obj.type, obj.price, obj.amount, obj.title]

  #print("len(mobile_object_data): ", len(mobile_object_data))
  for obj in mobile_object_data:
    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, is_corpse:{6}, title:{7}'.
    #    format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.isCorpse, obj.title))
    if obj.name in mountable_list:
      mountable_mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

    vendor_title = isVendor(obj.title)
    #print("vendor_title: ", vendor_title)
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
      #print("teacher_title: ", teacher_title)
      teacher_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, teacher_title]

  for obj in player_mobile_object_data:
    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
    #      format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
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

  if len(mobile_data) == 0 or len(equipped_item_data) == 0:
    return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, \
          corpse_dict, corpse_item_dict, vendor_dict, vendor_item_dict, mountable_mobile_dict, \
          teacher_dict, popup_menu_list, cliloc_data_list, player_skills_dict

  for mobile in mobile_data:
    #print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, mobile.x, mobile.y, mobile.race,
    #                                                                   mobile.serial))
    mobile_dict[mobile.serial] = [mobile.name, int(mobile.x), int(mobile.y), mobile.race]

    if mobile.x >= 1600 or mobile.y >= 1280:
      continue

    if mobile.race == 1:
      color = (0, 255, 0)
    elif mobile.race == 0:
      color = (0, 0, 255)
    else:
      color = (255, 0, 0)

    '''
    screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    cv2.putText(screen_image, text=mobile.name, org=center_coordinates, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0, color=color, thickness=2, lineType=cv2.LINE_4)
    '''

  for item in equipped_item_data:
    #print('name: {0}, layer: {1}, serial: {2}, amount: {3}'.format(item.name, item.layer, 
    #                                                               item.serial, item.amount))
    equipped_item_dict[item.serial] = [item.name, item.layer, item.amount]

  for item in backpack_item_data:
     backpack_item_dict[item.serial] = [item.name, item.layer, item.amount]

  for item in corpse_item_data:
     corpse_item_dict[item.serial] = [item.name, item.layer, item.amount]

  if (selected_target_serial not in mobile_dict) and selected_target_serial != None:
    selected_target_serial = None

  if selected_target_serial == None and len(mobile_dict) != 0:
    selected_target_serial = random.choice(list(mobile_dict.keys()))
    selected_target = mobile_dict[selected_target_serial]

  if selected_target_serial != None:
    selected_target = mobile_dict[selected_target_serial]

    color = (255, 0, 0)
    start_point = (selected_target[1] - 40, selected_target[2] - 40)
    end_point = (selected_target[1] + 40, selected_target[2] + 40)
    #screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)

  return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
      corpse_item_dict, vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, \
      popup_menu_list, cliloc_data_list, player_skills_dict


def get_serial_by_name(item_dict, name):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if v[0] == name:
      return k, keys.index(k)

  return None, None


def get_serial_by_title(item_dict, title):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if v[5] == title:
      return k, keys.index(k)

  return None, None


def get_serial_of_gold(item_dict):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if "Gold" in v[0]:
      return k, keys.index(k)

  return None, None


def main():
  action_index = 0
  #test_action_sequence = [3, 5, 6, 4]
  #test_action_sequence = [7]
  #test_action_sequence = [10, 11, 3, 16]
  test_action_sequence = [0, 0, 0]

  player_mobile_serial = None
  target_item_serial = None
  target_mobile_serial = None
  opened_corpse = None
  menu_index = 0
  opened_vendor_serial = None
  item_amount = 1
  for ep in range(0, 10000):
    #print("ep: ", ep)

    stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                        mobileSerial=1,
                                        walkDirection=1,
                                        index=menu_index, 
                                        amount=1))
    
    stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
    stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

    res = stub.ReadObs(UoService_pb2.Config(name='you'))

    mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
        corpse_item_dict, vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, \
        popup_menu_list, cliloc_data_list, player_skills_dict = parse_response(res)

    target_item_serial = 0
    target_mobile_serial = 0
    healer_vendor_serial = None

    for step in range(1, 100000):
      #if 'Swordsmanship' in player_skills_dict:
        #print("player_skills_dict['Swordsmanship']: ", player_skills_dict['Swordsmanship'])

      #print("vendor_dict: ", vendor_dict)
      #print("popup_menu_list: ", popup_menu_list)
      #print("vendor_item_dict: ", vendor_item_dict)
      #print("backpack_item_dict: ", backpack_item_dict)
      #print("teacher_dict: ", teacher_dict)
      #target_mobile_serial, index = get_serial_by_title(teacher_dict, 'warrior')
      healer_vendor_serial, index = get_serial_by_title(vendor_dict, 'healer')

      #if len(corpse_item_dict) != 0:
        #print("corpse_dict: ", corpse_dict)
        #print("corpse_item_dict: ", corpse_item_dict)
        #print("\n")

      if action_index != len(test_action_sequence) and step % 100 == 0:
        #print("popup_menu_list: ", popup_menu_list)
        #print("mountable_mobile_dict: ", mountable_mobile_dict)
        #print("corpse_dict: ", corpse_dict)
        #print("corpse_item_dict: ", corpse_item_dict)
        #print("")

        if test_action_sequence[action_index] == 0:
            if len(corpse_dict) != 0: 
              target_item_serial = list(corpse_dict.keys())[0]

        if test_action_sequence[action_index] == 2:
          #player_mobile_serial, index = get_serial_by_name(mobile_dict, "masterkim")
          #mountable_mobile_serial, index = get_serial_by_name(mountable_mobile_dict, "a hellsteed")
          #distance = mountable_mobile_dict[mountable_mobile_serial][4]
          target_mobile_serial = healer_vendor_serial

        if test_action_sequence[action_index] == 3:
          #target_item_serial, index = get_serial_of_gold(corpse_item_dict)
          #print("target_item_serial: ", target_item_serial)
          #print("backpack_item_dict:)
          target_item_serial, index = get_serial_of_gold(backpack_item_dict)

          #print("cliloc_data_list: ", cliloc_data_list)
          for cliloc_dict in cliloc_data_list:
            #print("cliloc_dict: ", cliloc_dict)
            if cliloc_dict['affix']:
              item_amount = cliloc_dict['affix'].replace(" ", "")
              if item_amount:
                item_amount = int(item_amount)
                #print("item_amount: ", item_amount)

        if test_action_sequence[action_index] == 6:
          target_item_serial, index = get_serial_by_name(ground_item_dict, 'Valorite Longsword')

        if test_action_sequence[action_index] == 8:
          target_item_serial = opened_corpse

        if len(corpse_dict) != 0: 
          if test_action_sequence[action_index] == 7 or test_action_sequence[action_index] == 9:
            target_item_serial = list(corpse_dict.keys())[0]
            opened_corpse = target_item_serial

        if test_action_sequence[action_index] == 10:
          target_mobile_serial, index = get_serial_by_title(vendor_dict, 'healer')
          #target_mobile_serial, index = get_serial_by_title(teacher_dict, 'warrior')
          opened_vendor_serial = target_mobile_serial

        if test_action_sequence[action_index] == 11:
          #menu_index = 1
          print("popup_menu_list: ", popup_menu_list)
          if 'Train Swordsmanship' in popup_menu_list :
            menu_index = popup_menu_list.index('Train Swordsmanship')

          print("menu_index: ", menu_index)
          print("opened_vendor_serial: ", opened_vendor_serial)

        if test_action_sequence[action_index] == 12:
          target_item_serial, index = get_serial_by_name(vendor_item_dict, "Clean Bandage")
          target_mobile_serial = opened_vendor_serial

        if test_action_sequence[action_index] == 13:
          target_item_serial, index = get_serial_by_name(vendor_item_dict, "clean bandage")
          target_mobile_serial = opened_vendor_serial

        if test_action_sequence[action_index] == 16:
          target_mobile_serial = opened_vendor_serial
          print("target_mobile_serial: ", target_mobile_serial)

        stub.WriteAct(UoService_pb2.Actions(actionType=test_action_sequence[action_index], 
                                            mobileSerial=target_mobile_serial,
                                            itemSerial=target_item_serial,
                                            walkDirection=2,
                                            index=menu_index, 
                                            amount=item_amount))

        action_index += 1
      else:
        stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                            mobileSerial=target_mobile_serial,
                                            itemSerial=target_item_serial,
                                            walkDirection=2,
                                            index=menu_index, 
                                            amount=item_amount))
      
      stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
      stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

      res_next = stub.ReadObs(UoService_pb2.Config(name='you'))

      mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
        corpse_item_dict, vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, \
        popup_menu_list, cliloc_data_list, player_skills_dict = parse_response(res_next)


if __name__ == '__main__':
  main()