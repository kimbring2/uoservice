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

print("grpc.__file__: ", grpc.__file__)

from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoService import UoService
import uoservice.utils

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
  pick_up_flag = True
  drop_flag = False
  vendor_flag = False
  open_vendor_flag = False
  open_corpse_flag = False
  change_skill_flag = False
  war_mode_flag = False
  hold_item = 0
  opened_vendor = 0

  war_mode = False

  uo_service = UoService(grpc_port, window_width, window_height)
  uo_service._open_grpc()

  obs = uo_service.reset()
  for step in range(0, 100000):
    #print("step: ", step)

    #if 10284 in obs["cliloc_dict"]:
    #  print("cliloc_dict: ", obs["cliloc_dict"][10284])
    #print("cliloc_dict: ", obs["cliloc_dict"])
    #for k, v in obs["cliloc_dict"].items():
    #  print("k: {0}, v: {1}", k, v)

    #print("corpse_dict: ", obs["corpse_dict"])
    #print("opened_corpse_list: ", obs["opened_corpse_list"])
    #print("backpack_item_data: ", obs["backpack_item_data"])
    #print("bank_item_data: ", obs["bank_item_data"])
    #print("vendor_data: ", obs["vendor_data"])

    print("vendor_data: ", obs["vendor_data"])

    #if len(obs["popup_menu_data"]) != 0:
      #print("popup_menu_data: ", obs["popup_menu_data"])

    if 'Swordsmanship' in obs["player_skills_data"]:
      #print("Swordsmanship skill info: ", obs["player_skills_data"]['Swordsmanship'])
      pass

    item_serial = 0
    mobile_serial = 0
    index = 0
    if len(obs["bank_item_data"]) != 0:
      item_serial, index = get_serial_by_name(obs["backpack_item_data"], "Lesser Heal Potion")
      print("item_serial: ", item_serial)

    if len(obs["bank_item_data"]) != 0 and open_vendor_flag == True:
      item_serial, index = utils.get_serial_by_name(obs["bank_item_data"], "Lesser Heal Potion")
      #print("item_serial: ", item_serial)

    if len(obs["vendor_data"]) != 0 and vendor_flag == True:
      #print("len(obs[\"vendor_data\"]) != 0  and vendor_flag == True",)
      for k, v in obs["vendor_data"].items():
        if "blacksmith" in v[5]:
          #print("k: {0}, v: {1}".format(k, v))
          mobile_serial = k
      #print("")

    if len(obs["corpse_data"]) != 0 and open_corpse_flag == True:
      item_serial = list(obs["corpse_dict"].keys())[0]
      print("item_serial: ", item_serial)

    if (change_skill_flag == True) and ('Swordsmanship' in obs["player_skills_data"]):
      #print("Swordsmanship skill info: ", obs["player_skills_data"]['Swordsmanship'])
      index = obs["player_skills_data"]['Swordsmanship'][0]

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
      elif vendor_flag == True and mobile_serial != 0:
        action['action_type'] = 10
        action['mobile_serial'] = mobile_serial
        action['amount'] = 1
        vendor_flag = False
        open_vendor_flag = True
        opened_vendor = mobile_serial
        print("action: ", action)
      elif open_vendor_flag == True:
        action['action_type'] = 11
        action['mobile_serial'] = opened_vendor
        action['index'] = 1
        open_vendor_flag = False
        print("action: ", action)
      elif open_corpse_flag == True:
        action['action_type'] = 7
        action['item_serial'] = item_serial
        action['index'] = 1
        open_corpse_flag = False
        print("action: ", action)
      elif change_skill_flag == True:
        action['action_type'] = 8
        action['index'] = index
        change_skill_flag = False
        print("action: ", action)
      elif war_mode_flag == True:
        action['action_type'] = 19
        action['index'] = war_mode
        war_mode = not war_mode

    obs_next = uo_service.step(action)

    obs = obs_next

if __name__ == '__main__':
  main()