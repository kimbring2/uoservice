# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Game scenario 1: Approach to the one of monster
#
# Please reference me when you are going to use this code as reference :)

## general package imports
## general package imports
import io
import time
import numpy as np
import random
import argparse
import sys
import grpc
from tqdm import tqdm
import threading
import cv2

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoService import UoService
from uoservice.UoServiceGameFileParser import UoServiceGameFileParser
import uoservice.utils as utils

## Define the command arguments
parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--window_width', type=int, default=1370, help='Screen width of game')
parser.add_argument('--window_height', type=int, default=1280, help='Screen height of game')
parser.add_argument('--grpc_port', type=int, default=60051, help='Port of grpc')
parser.add_argument('--uo_installed_path', type=str, help='Install path of UO windows client')


## Parse the command argument
arguments = parser.parse_args()
grpc_port = arguments.grpc_port
window_width = arguments.window_width
window_height = arguments.window_height
uo_installed_path = arguments.uo_installed_path


def step(uo_service):
  player_serial = None
  bandage_serial = None
  use_bandage_flag = False
  healing_active = False
  bag_item = None
  backpack_item = None
  backpack_opened = False

  step = 0
  while True:
    world_mobile_data = uo_service.world_mobile_dict
    world_item_data = uo_service.world_item_dict

    player_serial = uo_service.player_serial
    player_status_data = uo_service.player_status_dict
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state
    cliloc_dict = uo_service.cliloc_dict
    hold_item_serial = uo_service.hold_item_serial
    backpack_serial = uo_service.backpack_serial
    bank_serial = uo_service.bank_serial

    if len(player_status_data) != 0:
      player_hit = player_status_data['hits']
      player_hit_max = player_status_data['hitsMax']
      #print("player_hit: ", player_hit)
      #print("player_hit_max: ", player_hit_max)

      if player_hit < player_hit_max:
        use_bandage_flag = True

    player_buff_data = uo_service.player_buff_dict
    if len(player_buff_data) != 0:
      for k_buff, v_buff in player_buff_data.items():
        #print("{0}: {1}".format(k_buff, v_buff["text"]))
        if "Healing" in v_buff["text"]:
          healing_active = True
        else:
          healing_active = False

      #print("")

    backpack_item_data = uo_service.backpack_item_dict
    if len(backpack_item_data) != 0:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
        if "Clean Bandage" in v_backpack["name"]:
          #if v_backpack["amount"] >= 30:
          #print("{0}: {1}, {2}".format(k_backpack, v_backpack["name"], v_backpack["data"]))
          bandage_serial = k_backpack
          pass
          
      #print("")

    bag_serial, index = utils.get_serial_by_name(backpack_item_data, 'Bag')

    if bag_serial in world_item_data:
      bag_item = world_item_data[bag_serial]

    if backpack_serial in world_item_data:
      backpack_item = world_item_data[backpack_serial]

    if bag_item != None:
      print("bag_item['opened']: ", bag_item['opened'])

    if backpack_item != None:
      print("backpack_item['opened']: ", backpack_item['opened'])
      backpack_opened = backpack_item['opened']

    print("")

    if len(cliloc_dict) != 0:
      for k_cliloc, v_cliloc in cliloc_dict.items():
        #print("{0}: {1}".format(k_cliloc, v_cliloc))
        for cliloc in v_cliloc:
          if cliloc["name"] == "System":
            #print("cliloc data {0}: {1}".format(cliloc["name"], cliloc["text"]))
            pass
      #print("")

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    if step % 500 == 0 and step != 0:
      #print("step: ", step)
      #print("use_bandage_flag: ", use_bandage_flag)
      #print("player_serial: ", player_serial)
      #print("bandage_serial: ", bandage_serial)
      #print("healing_active: ", healing_active)
      #print("")

      if backpack_opened != True:
        print("Open the backpack if not")

        action['action_type'] = 2
        action['target_serial'] = backpack_serial
      elif use_bandage_flag == True and player_serial != None and \
          bandage_serial != None and healing_active == False:
        print("Use the bandage to the player")

        action['action_type'] = 14
        action['source_serial'] = bandage_serial
        action['target_serial'] = player_serial

        use_bandage_flag = False

    action['action_type'] = 0
    obs = uo_service.step(action)

    step += 1


## Declare the main function
def main():
  ## Declare the UoService using the parsed argument
  uo_service = UoService(grpc_port, window_width, window_height, uo_installed_path)

  ## Open the gRPC client to connect with gRPC server of CSharp part
  uo_service._open_grpc()

  ## Send the reset signal to gRPC server
  obs = uo_service.reset()

  thread_2 = threading.Thread(target=step, daemon=True, args=(uo_service,))
  thread_1 = threading.Thread(target=uo_service.parse_land_static, daemon=True, args=( ))

  thread_2.start()
  thread_1.start()

  thread_2.join()
  thread_1.join()


## Start the main function
if __name__ == '__main__':
  main()