# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` UoService.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. UoService.proto --proto_path /home/kimbring2/uoservice/uoservice/protos/

from __future__ import print_function
from concurrent import futures
import io
from PIL import Image
import time
import numpy as np
import cv2
import random
import argparse
import sys
import grpc
import utils
from enum import Enum

import UoService_pb2
import UoService_pb2_grpc
from UoService import UoService

#replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
#file_name = 'kimbring2-2023-6-6-01-56-41'

parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--game_path', type=str, help='root directory of UO execution')
parser.add_argument('--window_width', type=int, help='window width of game client')
parser.add_argument('--window_height', type=int, help='window height of game client')

arguments = parser.parse_args()

grpc_port = 60051
window_width = 1370
window_height = 1280


def main():
  pick_up_flag = False
  drop_flag = False
  bank_vendor_flag = True
  hold_item = 0

  # username, password, grpc_port, window_width, window_height, replay=None, human_play=None
  uo_service = UoService(grpc_port, window_width, window_height)
  uo_service._open_grpc()

  obs = uo_service.reset()
  for step in range(0, 100000):
    #print("step: ", step)

    #print("backpack_item_data: ", obs["backpack_item_data"])
    #print("bank_item_data: ", obs["bank_item_data"])
    #print("vendor_data: ", obs["vendor_data"])

    item_serial = 0
    #if len(obs["bank_item_data"]) != 0:
    #  item_serial, index = get_serial_by_name(obs["backpack_item_data"], "Lesser Heal Potion")
    #  print("item_serial: ", item_serial)

    if len(obs["bank_item_data"]) != 0:
      item_serial, index = get_serial_by_name(obs["bank_item_data"], "Lesser Heal Potion")
      #print("item_serial: ", item_serial)

    if len(obs["vendor_data"]) != 0:
      mobile_serial = list(obs["vendor_data"].keys())[0]
      print("mobile_serial: ", mobile_serial)

    action = {}
    action['action_type'] = 0
    action['item_serial'] = 0
    action['mobile_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0

    if step % 100 == 0:
      print("step: ", step)

      if pick_up_flag == True and item_serial != 0:
        action['action_type'] = 3
        action['item_serial'] = item_serial
        action['amount'] = 1
        pick_up_flag = False
        drop_flag = True
        hold_item = item_serial
        print("action: ", action)
      elif drop_flag == True and item_serial != 0:
        action['action_type'] = 4
        action['item_serial'] = hold_item
        action['amount'] = 1
        drop_flag = False
        print("action: ", action)
      elif bank_vendor_flag == True:
        action['action_type'] = 10
        action['mobile_serial'] = mobile_serial
        action['amount'] = 1
        bank_vendor_flag = False
        print("action: ", action)

    obs_next = uo_service.step(action)

    obs = obs_next

if __name__ == '__main__':
  main()