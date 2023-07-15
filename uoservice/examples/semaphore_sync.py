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

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoService import UoService
import uoservice.utils as utils

## Define the command arguments
parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--window_width', type=int, default=1370, help='screen width of game')
parser.add_argument('--window_height', type=int, default=1280, help='screen height of game')
parser.add_argument('--grpc_port', type=int, default=60051, help='port of grpc')

## Parse the command argument
arguments = parser.parse_args()
grpc_port = arguments.grpc_port
window_width = arguments.window_width
window_height = arguments.window_height

## Declare the main function
def main():
  ## Declare the UoService using the parsed argument
  uo_service = UoService(grpc_port, window_width, window_height)

  ## Open the gRPC client to connect with gRPC server of CSharp part
  uo_service._open_grpc()

  ## Send the reset signal to gRPC server
  obs = uo_service.reset()

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

    backpack_item_data = uo_service.backpack_item_dict
    #print("backpack_item_data: ", backpack_item_data)
    for k_backpack, v_backpack in backpack_item_data.items():
      #print("backpack {0}: {1}".format(k_backpack, v_backpack))
      pass

    #for k_mobile, v_mobile in uo_service.world_mobile_dict.items():
    #  print("world_mobile {0}: {1}".format(k_mobile, v_mobile))

    equipped_item_data = uo_service.equipped_item_dict
    #print("equipped_item_data: ", equipped_item_data)

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

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

    if len(uo_service.near_land_object_dict) != 0:
      #print("len(uo_service.near_land_object_dict): ", len(uo_service.near_land_object_dict))
      for k, v in uo_service.near_land_object_dict.items():
        print("Near land {0}: {1}".format(k, uo_service.near_land_object_dict[k]))
      print("")

    ## Declare the empty action
    if step % 150 == 0:
      print("step: ", step)
      #print("gold_serial: ", gold_serial)
      if gold_serial != None and pick_up_flag == True:
        action['action_type'] = 0
        action['target_serial'] = gold_serial
        action['amount'] = 100
        pick_up_flag = False
        drop_flag = True
      elif drop_flag == True:
        if len(uo_service.near_land_object_dict) != 0:
          action['action_type'] = 4

          near_land_object_dict = uo_service.near_land_object_dict
          print("len(near_land_object_dict): ", len(near_land_object_dict))
          #GameX: 3522, GameY: 2752, index:16

          drop_index = random.randint(0, len(near_land_object_dict))
          action['index'] = drop_index
          drop_flag = False

      obs = uo_service.step(action)
    else:
      obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Start the main function
if __name__ == '__main__':
  main()