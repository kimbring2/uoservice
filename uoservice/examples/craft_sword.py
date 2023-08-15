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
  pick_up_item_flag = False
  equip_item_flag = False

  drop_item_serial = None
  onehanded_item_serial = None
  smith_hammer_serial = None

  open_blacksmith_gump_flag = False
  crafting_ready_flag = False

  select_gump_button_flag_1 = False
  select_gump_button_flag_2 = False
  select_gump_button_flag_3 = False

  gump_local_serial = None
  gump_server_serial = None

  targeting_type = None
  one_time_trial = True

  iron_ingot_amount = 0
  anvil_distance = 100

  step = 0
  while True:
    world_item_data = uo_service.world_item_dict
    menu_gump_control = uo_service.menu_gump_control
    backpack_item_data = uo_service.backpack_item_dict
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state
    world_static_data = uo_service.world_static_dict

    if len(backpack_item_data) > 0:
      for k_backpack, v_backpack in backpack_item_data.items():
        if "Ingot" in v_backpack["name"]:
          iron_ingot = True
          for ingot_category in utils.ingot_category_list:
            if ingot_category in v_backpack["data"]:
              iron_ingot = False

          if iron_ingot == True:
            #print("name: {0}, amount: {1}".format(v_backpack["name"], v_backpack["amount"]))
            iron_ingot_amount = v_backpack["amount"]
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

    if len(world_static_data) > 0:
      for k_static, v_static in world_static_data.items():
        #print("k_static: {0}, v_static: {1}".format(k_static, v_static))
        if "anvil" in v_static["name"]:
          #print("name: {0}, game_x: {1}, game_y: {2}".format(v_static["name"], v_static["game_x"],
          #                                                   v_static["game_y"]))
          anvil_distance = uo_service.get_distance(v_static['game_x'], v_static['game_y'])
          #print("anvil_distance: ", anvil_distance)
          pass
      #print("")

    unequip_item_serial = None
    if "OneHanded" in equipped_item_dict:
      if equipped_item_dict["OneHanded"]["name"] != "Smith's Hammer":
        unequip_item_serial = equipped_item_dict["OneHanded"]["serial"]
      elif equipped_item_dict['OneHanded']['name'] == "Smith's Hammer":
        onehanded_item_serial = equipped_item_dict["OneHanded"]["serial"]
        smith_hammer_serial = onehanded_item_serial

        if open_blacksmith_gump_flag == False and one_time_trial == True:
          open_blacksmith_gump_flag = True
          one_time_trial = False
    else:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
        if v_backpack["name"] == "Smith's Hammer":
          smith_hammer_serial = k_backpack

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

    if step % 200 == 0:
      #print("step: ", step)
      print("gump_local_serial: ", gump_local_serial)
      print("gump_server_serial: ", gump_server_serial)

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
        pick_up_item_flag = True
      elif pick_up_item_flag == True:
        print("Pick up the Smith's Hammer from backpack")

        action['action_type'] = 3
        action['target_serial'] = smith_hammer_serial

        pick_up_item_flag = False
        equip_item_flag = True
      elif equip_item_flag == True:
        print("Equip the holded item")

        action['action_type'] = 6
        equip_item_flag = False
      elif open_blacksmith_gump_flag == True:
        print("Double click the Smith Hammer item")

        action['action_type'] = 2
        action['target_serial'] = smith_hammer_serial

        open_blacksmith_gump_flag = False
        select_gump_button_flag_1 = True
      elif select_gump_button_flag_1 == True:
        print("Select sword craft category button")

        action['action_type'] = 9
        action['target_serial'] = gump_server_serial
        action['source_serial'] = gump_local_serial
        action['index'] = 22

        select_gump_button_flag_1 = False
        select_gump_button_flag_2 = True
      elif select_gump_button_flag_2 == True:
        print("Select broadsword detail button")

        action['action_type'] = 9
        action['target_serial'] = gump_server_serial
        action['source_serial'] = gump_local_serial
        action['index'] = 10

        select_gump_button_flag_2 = False
        select_gump_button_flag_3 = True
      elif select_gump_button_flag_3 == True:
        print("Select make now button")

        if anvil_distance <= 2 and iron_ingot_amount >= 10:
          action['action_type'] = 9
          action['target_serial'] = gump_server_serial
          action['source_serial'] = gump_local_serial
          action['index'] = 1
        else:
          print("can not craft the broadsword")

        select_gump_button_flag_3 = False

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