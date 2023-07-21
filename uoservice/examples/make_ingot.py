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
parser.add_argument('--window_width', type=int, default=1370, help='screen width of game')
parser.add_argument('--window_height', type=int, default=1280, help='screen height of game')
parser.add_argument('--grpc_port', type=int, default=60051, help='port of grpc')

## Parse the command argument
arguments = parser.parse_args()
grpc_port = arguments.grpc_port
window_width = arguments.window_width
window_height = arguments.window_height


def step(uo_service):
  pick_up_ore_flag = True
  drop_ore_flag = False
  forging_flag = False
  ore_bulk_serial = None
  ore_serial = None

  double_click_ore_flag = False

  forge_serial = None

  step = 0
  while True:
    if len(uo_service.world_item_dict) != 0:
      for k_world, v_world in uo_service.world_item_dict.items():
        #print("name: {0}, layer: {1}".format(v_world['name'], v_world['layer']))
        if "Forge" in v_world["name"]:
          forge_serial = k_world

        pass
      #print("")

    backpack_item_data = uo_service.backpack_item_dict
    if len(backpack_item_data) != 0:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))

        if "Ore" in v_backpack["name"] and "Gold" not in v_backpack["data"]:
          if v_backpack["amount"] >= 50:
            #print("{0}: {1}, {2}".format(k_backpack, v_backpack["name"], v_backpack["data"]))
          
            if ore_bulk_serial == None:
              ore_bulk_serial = k_backpack
              pick_up_ore_flag = True
          else:
            ore_serial = k_backpack

      pass

      #print("")

    ## Player holded item
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state

    cliloc_dict = uo_service.cliloc_dict
    #print("cliloc_dict: ", cliloc_dict)

    hold_item_serial = uo_service.hold_item_serial
    backpack_serial = uo_service.backpack_serial
    bank_serial = uo_service.bank_serial

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
      print("step: ", step)
      #print("pick_up_ore_flag: ", pick_up_ore_flag)
      print("ore_bulk_serial: ", ore_bulk_serial)
      print("ore_serial: ", ore_serial)
      print("forge_serial: ", forge_serial)
      print("targeting_state: ", targeting_state)
      print("")

      if pick_up_ore_flag == True and ore_bulk_serial != None:
        print("Pick up the item from player")

        action['action_type'] = 3
        action['target_serial'] = ore_bulk_serial
        action['amount'] = 8

        picked_item = uo_service.world_item_dict[ore_bulk_serial]
        uo_service.picked_up_item = picked_item

        drop_ore_flag = True
        pick_up_ore_flag = False
      elif drop_ore_flag == True:
        print("Drop the item into the backpack")

        action['action_type'] = 4
        action['target_serial'] = backpack_serial
        action['index'] = 1

        drop_ore_flag = False
        double_click_ore_flag = True
      elif double_click_ore_flag == True and ore_serial != None:
        print("Double click the ore item")

        action['action_type'] = 2
        action['target_serial'] = ore_serial

        forging_flag = True
        double_click_ore_flag = False
      elif forging_flag == True and forge_serial != None:
        action['action_type'] = 5
        action['target_serial'] = forge_serial
        #action['target_serial'] = bag_serial
        #action['index'] = 0

        forging_flag = False

    action['action_type'] = 0
    obs = uo_service.step(action)

    step += 1


## Declare the main function
def main():
  ## Declare the UoService using the parsed argument
  uo_service = UoService(grpc_port, window_width, window_height)

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