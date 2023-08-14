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
  smith_hammer_serial = None
  onehanded_item_serial = None
  gump_local_serial = None

  open_blacksmith_gump_flag = False
  crafting_ready_flag = False

  select_gump_button_flag = False

  gump_local_serial = None
  gump_server_serial = None

  targeting_type = None
  one_time_trial = True

  step = 0
  while True:
    menu_gump_control = uo_service.menu_gump_control
    backpack_item_data = uo_service.backpack_item_dict
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state

    if len(backpack_item_data) > 0:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
        pass
      #print("")

    equipped_item_dict = uo_service.equipped_item_dict
    #print("equipped_item_dict: ", equipped_item_dict)
    for k_equip, v_equip in equipped_item_dict.items():
      #print("equipped item {0}: {1}".format(k_equip, v_equip))
      pass

    if len(menu_gump_control) != 0:
      for k_gump, v_gump in menu_gump_control.items():
        #print("k_gump: ", k_gump)
        #print("v_gump['server_serial']: ", v_gump['server_serial'])

        gump_local_serial = k_gump
        gump_server_serial = v_gump['server_serial']

        for i, control in enumerate(v_gump["control_list"]):
          #print("control: ", control)
          pass

      #print("")

    if "OneHanded" in equipped_item_dict:
      #print("OneHanded equip item {0}", equipped_item_dict["OneHanded"])

      if equipped_item_dict['OneHanded']['name'] == "Smith's Hammer":
        #print("equipped_item_dict['OneHanded']['name']: {0}", 
        #        equipped_item_dict['OneHanded']['name'])

        onehanded_item_serial = equipped_item_dict["OneHanded"]["serial"]
        smith_hammer_serial = onehanded_item_serial

        if open_blacksmith_gump_flag == False and one_time_trial == True:
          open_blacksmith_gump_flag = True
          one_time_trial = False

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    cliloc_dict = uo_service.cliloc_dict
    #print("cliloc_dict: ", cliloc_dict)

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
      #print("targeting_state: ", targeting_state)

      if open_blacksmith_gump_flag == True:
        print("Double click the Smith Hammer item")

        action['action_type'] = 2
        action['target_serial'] = smith_hammer_serial

        open_blacksmith_gump_flag = False
        select_gump_button_flag = True
      elif select_gump_button_flag == True:
        print("Select sword craft category button")
        action['action_type'] = 9
        action['target_serial'] = gump_server_serial
        action['source_serial'] = gump_local_serial
        action['index'] = 9

        select_gump_button_flag = False

    #action['action_type'] = 0  
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
  thread_1 = threading.Thread(target=uo_service.parse_land_static, daemon=True, args=())

  thread_2.start()
  thread_1.start()

  thread_2.join()
  thread_1.join()


## Start the main function
if __name__ == '__main__':
  main()