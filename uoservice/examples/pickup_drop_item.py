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
from enum import Enum
import os

from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoService import UoService
import uoservice.utils as utils

path = os.path.abspath(utils.__file__)

print("path: ", path)

#replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
#file_name = 'kimbring2-2023-6-6-01-56-41'

parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--window_width', type=int, default=1370, help='screen width of game')
parser.add_argument('--window_height', type=int, default=1280, help='screen height of game')
parser.add_argument('--grpc_port', type=int, default=60051, help='port of grpc')

arguments = parser.parse_args()

grpc_port = arguments.grpc_port
window_width = arguments.window_width
window_height = arguments.window_height

def main():
  uo_service = UoService(grpc_port, window_width, window_height)
  uo_service._open_grpc()

  obs = uo_service.reset()

  pick_up_flag = True
  drop_flag = False
  for step in range(0, 100000):
    #print("step: ", step)

    item_serial = 0
    mobile_serial = 0

    #print("backpack_item_data: ", obs["backpack_item_data"])
    if len(obs["backpack_item_data"]) != 0:
      item_serial, index = utils.get_serial_by_name(obs["backpack_item_data"], "Gold")
      #print("item_serial: ", item_serial)

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
        action['amount'] = 100
        pick_up_flag = False
        drop_flag = True
        print("action: ", action)
      elif drop_flag == True:
        action['action_type'] = 5
        print("action: ", action)
        drop_flag = False

    obs = uo_service.step(action)

if __name__ == '__main__':
  main()