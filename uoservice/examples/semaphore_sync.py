# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Game scenario 1: Approach to the one of monster
#
# Please reference me when you are going to use this code as reference :)

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
  player_gold = None
  pick_up_flag = True
  drop_flag = False

  step = 0
  while True:
    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    world_item_data = uo_service.world_item_dict
    backpack_item_data = uo_service.backpack_item_dict
    equipped_item_data = uo_service.equipped_item_dict
    ground_item_data = uo_service.ground_item_dict
    
    if len(ground_item_data) != 0:
      for k_ground, v_ground in ground_item_data.items():
        #print("ground {0}: {1}".format(k_ground, v_ground["name"]))
        pass

    if len(uo_service.world_mobile_dict) != 0:
      for k_mobile, v_mobile in uo_service.world_mobile_dict.items():
        #print("world_mobile {0}: {1}".format(k_mobile, v_mobile["name"]))
        pass

    targeting_state = uo_service.targeting_state
    hold_item_serial = uo_service.hold_item_serial
    equipped_item_data = uo_service.equipped_item_dict
    player_status_dict = uo_service.player_status_dict
    gold_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if gold_serial in backpack_item_data:
      gold_info = backpack_item_data[gold_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

    if len(uo_service.player_status_dict) != 0:
      player_gold = uo_service.player_status_dict['gold']
      #print("player_gold: ", player_gold)

    ## Declare the empty action
    if step % 100 == 0:
      if len(world_item_data) != 0:
        for k_world, v_world in world_item_data.items():
          #print("world {0}: {1}".format(k_world, v_world["name"]))
          pass
        #print("")

      if len(equipped_item_data) != 0:
        for k_equipped, v_equipped in equipped_item_data.items():
          #print("equipped {0}: {1}".format(k_equipped, v_equipped["name"]))
          pass
        #print("")

      if len(backpack_item_data) != 0:
        for k_backpack, v_backpack in backpack_item_data.items():
          print("backpack {0}: {1}".format(k_backpack, v_backpack["name"]))
          pass
        print("")

      corpse_dict = {}
      for k, v in uo_service.world_item_dict.items():
        #print("world item {0}: {1}, isCorpse: {2}".format(k, v["name"], v["isCorpse"]))
        if v["isCorpse"] == True:
          #print("world item {0}: {1}, isCorpse: {2}".format(k, v["name"], v["isCorpse"]))
          corpse_dict[k] = v

      corpse_item_dict = {}
      for k_corpse, v_corpse in corpse_dict.items():
        for k_world, v_world in uo_service.world_item_dict.items():
          if k_corpse == v_world["container"]:
            if k_world not in corpse_item_dict:
              corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]
            else:
              corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]

      if len(corpse_item_dict) != 0:
        for k_corpse, v_corpse in corpse_item_dict.items():
          print("corpse item {0}: {1}".format(k_corpse, v_corpse["name"]))
          pass
        print("")

      #print("step: ", step)
      #print("gold_serial: ", gold_serial)
      #print("pick_up_flag: ", pick_up_flag)
      #print("")

      if gold_serial != None and pick_up_flag == True:
        action['action_type'] = 3
        action['target_serial'] = gold_serial
        action['amount'] = 100
        pick_up_flag = False
        drop_flag = True
      elif drop_flag == True:
        action['action_type'] = 4
        action['index'] = 2554
        drop_flag = False

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