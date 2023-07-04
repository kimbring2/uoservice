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
  unequip_item_serial = None
  drop_item_serial = None
  picked_up_item_serial = None

  step = 0
  while True:
    backpack_item_data = uo_service.backpack_item_dict
    #print("backpack_item_data: ", backpack_item_data)
    for k_backpack, v_backpack in backpack_item_data.items():
      #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
      pass

    #for k_mobile, v_mobile in uo_service.world_mobile_dict.items():
    #  print("world_mobile {0}: {1}".format(k_mobile, v_mobile))

    #for k_item, v_item in uo_service.world_item_dict.items():
    #  print("world_item {0}: {1}".format(k_item, v_item))

    equipped_item_dict = uo_service.equipped_item_dict
    #print("equipped_item_dict: ", equipped_item_dict)

    #for k_equip, v_equip in equipped_item_dict.items():
    #  print("equipped item {0}: {1}".format(k_equip, v_equip))

    ## Player holded item
    hold_item_serial = uo_service.hold_item_serial
    #print("hold_item_serial: ", hold_item_serial)

    #print("uo_service.picked_up_item: ", uo_service.picked_up_item)
    #print("uo_service.bank_serial: ", uo_service.bank_serial)
    #print("uo_service.backpack_serial: ", uo_service.backpack_serial)

    unequip_item_serial = None
    if "OneHanded" in equipped_item_dict:
      #print("OneHanded equip item {0}", equipped_item_dict["OneHanded"])
      unequip_item_serial = equipped_item_dict["OneHanded"]["serial"]
      pass

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    cliloc_dict = uo_service.cliloc_dict
    #print("cliloc_dict: ", cliloc_dict)

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
      if unequip_item_serial != None:
        #print("unequip_item_serial: ", unequip_item_serial)
        #print("unequip_item: ", unequip_item)

        action['action_type'] = 3
        action['item_serial'] = unequip_item_serial

        unequip_item = uo_service.world_item_dict[unequip_item_serial]
        uo_service.picked_up_item = unequip_item

        drop_item_serial = unequip_item_serial
        unequip_item_serial = None
      elif drop_item_serial != None:
        print("Pick up equipped item from player")
        action['action_type'] = 3
        action['item_serial'] = unequip_item_serial
        drop_item_serial = None
      elif uo_service.bank_serial != 0:
        #print("Drop item into backpack")
        action['action_type'] = 4
        #action['item_serial'] = uo_service.bank_serial

      obs = uo_service.step(action)

    #obs = uo_service.step(action)
    obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Start the main function
if __name__ == '__main__':
  main()