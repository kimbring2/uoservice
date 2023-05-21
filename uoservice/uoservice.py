# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` helloworld.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. helloworld.proto --proto_path /home/kimbring2/grpc/examples/protos/

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


grpc_port = 50051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)

selected_target_serial = None
player_serial = None


def isVendor(title):
  vendor_name_list = ['healer']
  title_split = title.split(" ")
  for vendor_name in vendor_name_list:
    if vendor_name == title_split[-1]:
      return title_split[-1]

  return None


def parse_response(response):
  global selected_target_serial
  global player_serial

  mobile_dict = {}
  world_item_dict = {}
  equipped_item_dict = {}
  backpack_item_dict = {}
  ground_item_dict = {}
  corpse_dict = {}
  corpse_item_dict = {}
  vendor_dict = {}

  mobile_data = response.mobileList.mobile
  world_item_data = response.worldItemList.item
  equipped_item_data = response.equippedItemList.item
  backpack_item_data = response.backpackItemList.item
  corpse_item_data = response.corpseItemList.item

  land_object_data = response.landObjectList.gameObject
  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  static_object_data = response.staticObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameObject

  screen_image = np.zeros((172,137,4), dtype=np.uint8)
  for obj in land_object_data:
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

  for obj in static_object_data:
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  for obj in item_dropable_land_data:
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 0
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

  for obj in item_object_data:
    ground_item_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

    if obj.isCorpse:
      corpse_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  for obj in mobile_object_data:
    vendor_title = isVendor(obj.title)

    if vendor_title:
      obj.title = vendor_title
      #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, is_corpse:{6}, title:{7}'.
      #  format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.isCorpse, obj.title))

      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 255
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

      vendor_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
    else:
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 0
      screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 255

  for obj in player_mobile_object_data:
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 0] = 255
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 1] = 0
    screen_image[int(obj.screenX / 10), int(obj.screenY / 10), 2] = 0

  dim = (1600, 1280)
  screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)
  screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
  screen_image = cv2.flip(screen_image, 1)
  cv2.imshow('screen_image', screen_image)
  cv2.waitKey(1)

  if len(mobile_data) == 0 or len(world_item_data) == 0 or len(equipped_item_data) == 0:
    return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, \
          corpse_dict, corpse_item_dict, vendor_dict

  for mobile in mobile_data:
    '''
    print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, mobile.x, mobile.y, mobile.race,
                                                                       mobile.serial))
    '''
    if mobile.race != 1:
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

  #cv2.imshow('screen_image', screen_image)
  #cv2.waitKey(1)

  return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
      corpse_item_dict, vendor_dict


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
  #test_action_sequence = [7, 9, 3, 4, 8]
  test_action_sequence = [10, 11]

  target_weapon_serial = None
  opened_corpse = None
  for ep in range(0, 10000):
    print("ep: ", ep)

    stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                        mobileSerial=1,
                                        walkDirection=UoService_pb2.WalkDirection(direction=1)))
    
    stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
    stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

    res = stub.ReadObs(UoService_pb2.Config(name='you'))

    mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
        corpse_item_dict, vendor_dict = parse_response(res)

    for step in range(1, 100000):
      if selected_target_serial != None and selected_target_serial in mobile_dict:
        selected_target = mobile_dict[selected_target_serial]
        target_x = selected_target[1]
        target_y = selected_target[2]
        target_serial = selected_target_serial
      elif player_serial != None:
        player = mobile_dict[player_serial]
        target_x = player[1]
        target_y = player[2]
        target_serial = player_serial
      else:
        target_x = 500
        target_y = 500
        target_serial = 1

      #print("vendor_dict: ", vendor_dict)

      if action_index != len(test_action_sequence) and step % 100 == 0:
        #print("action_index: ", action_index)
        #print("test_action_sequence[action_index]: ", test_action_sequence[action_index])
        #print("equipped_item_dict: ", equipped_item_dict)
        #print("ground_item_dict: ", ground_item_dict)

        target_item_serial = 0
        if test_action_sequence[action_index] == 3:
          print("corpse_item_dict: ", corpse_item_dict)
          #target_item_serial, index = get_serial_by_name(equipped_item_dict, 'Valorite Longsword')
          target_item_serial, index = get_serial_of_gold(corpse_item_dict)
        
        if test_action_sequence[action_index] == 6:
          #target_item_serial, index = get_serial_by_name(ground_item_dict, 'Valorite Longsword')
          pass

        if test_action_sequence[action_index] == 8:
          target_item_serial = opened_corpse

        if test_action_sequence[action_index] == 10 or test_action_sequence[action_index] == 11:
          target_mobile_serial, index = get_serial_by_title(vendor_dict, 'healer')
          print("target_mobile_serial: ", target_mobile_serial)

        if len(corpse_dict) != 0: 
          if test_action_sequence[action_index] == 7 or test_action_sequence[action_index] == 9:
            print("corpse_dict: ", corpse_dict)
            target_item_serial = list(corpse_dict.keys())[0]
            opened_corpse = target_item_serial
            #print("target_item_serial: ", target_item_serial)

        #target_item_serial = 0

        #print("target_item_serial: ", target_item_serial)
        print("test_action_sequence[action_index]: ", test_action_sequence[action_index])
        stub.WriteAct(UoService_pb2.Actions(actionType=test_action_sequence[action_index], 
                                            mobileSerial=target_mobile_serial,
                                            itemSerial=target_item_serial,
                                            walkDirection=UoService_pb2.WalkDirection(direction=2)))

        action_index += 1
      else:
        stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                            mobileSerial=target_serial,
                                            itemSerial=target_weapon_serial,
                                            walkDirection=UoService_pb2.WalkDirection(direction=2)))
      
      stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
      stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

      res_next = stub.ReadObs(UoService_pb2.Config(name='you'))

      mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, corpse_dict, \
        corpse_item_dict, vendor_dict = parse_response(res_next)

      #time.sleep(0.5)

    #cv2.destroyAllWindows()


if __name__ == '__main__':
  main()