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


def parse_response(response):
  mobile_data = response.mobileList.mobile
  world_item_data = response.worldItemList.item
  equipped_item_data = response.equippedItemList.item
  backpack_item_data = response.backpackItemList.item

  cliloc_data = response.clilocDataList.clilocData
  for data in cliloc_data:
    cliloc_dict = {}
    cliloc_dict['text'] = data.text
    cliloc_dict['affix'] = data.affix

  player_mobile_object_data = response.playerMobileObjectList.gameObject
  mobile_object_data = response.mobileObjectList.gameObject
  item_object_data = response.itemObjectList.gameObject
  item_dropable_land_data = response.itemDropableLandList.gameSimpleObject

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

  vis = True
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


def main():
  for ep in range(0, 10000):
    stub.ReadMPQFile(UoService_pb2.Config(name='kimbring2-2023-5-29-13-54-03'))

    for step in range(1, 100000):
      res = stub.ReadReplay(UoService_pb2.Config(name='you'))
      parse_response(res)


if __name__ == '__main__':
  main()