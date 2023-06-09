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

import UoService_pb2
import UoService_pb2_grpc
from UoService import UoService

#replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
#file_name = 'kimbring2-2023-6-6-01-56-41'

parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--game_path', type=str, help='root directory of UO execution')
parser.add_argument('--window_width', type=int, help='root directory of UO execution')

arguments = parser.parse_args()

grpc_port = 60051
window_width = 1370
window_height = 1280
human_play = False
replay = None


def get_serial_by_name(item_dict, name):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if v[0] == name:
      return k, keys.index(k)

  return None, None


def main():
  pick_up_flag = True
  drop_flag = False
  hold_item = 0

  # username, password, grpc_port, window_width, window_height, replay=None, human_play=None
  uo_service = UoService(grpc_port, window_width, window_height)
  uo_service._open_grpc()

  obs = uo_service.reset()
  for step in range(0, 100000):
    #print("step: ", step)

    #print("obs[\"backpack_item_data\"]: ", obs["backpack_item_data"])
    #print("obs[\"bank_item_data\"]: ", obs["bank_item_data"])

    target_serial = 0
    if len(obs["bank_item_data"]) != 0:
      target_serial, index = get_serial_by_name(obs["backpack_item_data"], "2 Lesser Heal Potion")
      #print("selected_serial: ", selected_serial)

    action = {}
    action['action_type'] = 0
    action['selected_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0

    if step % 100 == 0:
      print("step: ", step)

      if pick_up_flag == True and target_serial != 0:
        action['action_type'] = 3
        action['selected_serial'] = 0
        action['target_serial'] = target_serial
        action['walk_direction'] = 0
        action['index'] = 0
        action['amount'] = 1
        pick_up_flag = False
        drop_flag = True
        hold_item = target_serial

        print("action: ", action)
      elif drop_flag == True and target_serial != 0:
        action['action_type'] = 18
        action['selected_serial'] = 0
        action['target_serial'] = hold_item
        action['walk_direction'] = 0
        action['index'] = 0
        action['amount'] = 1
        drop_flag = False

        print("action: ", action)

    obs_next = uo_service.step(action)

    obs = obs_next

if __name__ == '__main__':
  main()