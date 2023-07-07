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

  pickaxe_serial = None
  equip_item_flag = False
  unequip_item_serial = None
  pickaxe_item_serial = None
  onehanded_item_serial = None
  drop_item_serial = None
  picked_up_item_serial = None

  mining_prepare_flag = False
  mining_ready_flag = False

  targeting_type = None

  one_time_trial = True

  step = 0
  while True:
    backpack_item_data = uo_service.backpack_item_dict
    for k_backpack, v_backpack in backpack_item_data.items():
      #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
      pass

    equipped_item_dict = uo_service.equipped_item_dict
    #print("equipped_item_dict: ", equipped_item_dict)

    #for k_equip, v_equip in equipped_item_dict.items():
    #  print("equipped item {0}: {1}".format(k_equip, v_equip))

    ## Player holded item
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state

    unequip_item_serial = None
    pickaxe_item_serial = None
    if "OneHanded" in equipped_item_dict:
      #print("OneHanded equip item {0}", equipped_item_dict["OneHanded"])

      if equipped_item_dict["OneHanded"]["name"] != "Pickaxe":
        unequip_item_serial = equipped_item_dict["OneHanded"]["serial"]
      elif equipped_item_dict["OneHanded"]["name"] == "Pickaxe":
        onehanded_item_serial = equipped_item_dict["OneHanded"]["serial"]
        if mining_ready_flag == False:
          mining_prepare_flag = True
    else:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
        if v_backpack["name"] == "Pickaxe":
          pickaxe_item_serial = k_backpack

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    cliloc_dict = uo_service.cliloc_dict
    print("cliloc_dict: ", cliloc_dict)

    pickaxe_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if pickaxe_serial in backpack_item_data:
      pickaxe_serial = backpack_item_data[pickaxe_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    if step % 100 == 0:
      #print("step: ", step)
      print("targeting_state: ", targeting_state)

      if unequip_item_serial != None:
        print("Pick up the equipped item from player")

        action['action_type'] = 3
        action['target_serial'] = unequip_item_serial

        unequip_item = uo_service.world_item_dict[unequip_item_serial]
        uo_service.picked_up_item = unequip_item

        drop_item_serial = unequip_item_serial
        unequip_item_serial = None
      elif drop_item_serial != None and uo_service.backpack_serial: 
        print("Drop the holded item into backpack")

        action['action_type'] = 4
        action['target_serial'] = uo_service.backpack_serial
        drop_item_serial = None
      elif pickaxe_item_serial != None:
        print("Pick up the Pickaxe item from backpack")
        action['action_type'] = 3
        action['target_serial'] = pickaxe_item_serial
        equip_item_flag = True
      elif equip_item_flag == True:
        print("Equip the holded item")
        action['action_type'] = 6
        equip_item_flag = False
      elif mining_prepare_flag == True and one_time_trial == True:
        print("Double click the Pickaxe item")
        action['action_type'] = 2
        action['target_serial'] = onehanded_item_serial

        mining_prepare_flag = False
        mining_ready_flag = True
        one_time_trial = False
      elif mining_ready_flag == True:
        print("Mining the land target")

        # GameX: 3527, GameY: 2753, index:8
        if len(uo_service.near_land_object_dict) != 0:
          #print("len(uo_service.near_land_object_dict): ", len(uo_service.near_land_object_dict))
          for k, v in uo_service.near_land_object_dict.items():
            #print("Near land {0}: {1}".format(k, uo_service.near_land_object_dict[k]))
            if v['gameX'] == 3527 and v['gameY'] == 2753:
              print("Near land {0}: {1}".format(k, uo_service.near_land_object_dict[k]))
              action['action_type'] = 5
              action['index'] = k
              mining_ready_flag = False

      obs = uo_service.step(action)

    #obs = uo_service.step(action)
    obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Start the main function
if __name__ == '__main__':
  main()