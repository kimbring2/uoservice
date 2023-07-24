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
  open_pop_up_flag = True
  select_pop_up_flag = False

  one_trial_check_flag = True

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

    healer_vendor_serial = None
    healer_vendor = None

    world_item_data = uo_service.world_item_dict
    world_mobile_data = uo_service.world_mobile_dict
    backpack_item_data = uo_service.backpack_item_dict
    equipped_item_data = uo_service.equipped_item_dict
    popup_menu_list = uo_service.popup_menu_list
    ground_item_data = uo_service.ground_item_dict
    
    targeting_state = uo_service.targeting_state
    hold_item_serial = uo_service.hold_item_serial
    equipped_item_data = uo_service.equipped_item_dict
    player_status_dict = uo_service.player_status_dict

    if len(world_mobile_data) != 0:
      for k_world, v_world in world_mobile_data.items():
        #print("mobile v_world: ", v_world)
        #print("name: {0}, title: {1}, distance: {2}".format(v_world['name'], v_world['title'], v_world['distance']))
        if "Lowell" in v_world["name"] and "healer" in v_world["title"]:
          #print("name: {0}, title: {1}, serial: {2}".format(v_world['name'], v_world['title'], v_world['serial']))
          healer_vendor_serial = k_world
          healer_vendor = world_mobile_data[healer_vendor_serial]
      #print("")

    if len(world_item_data) != 0:
        for k_world, v_world in world_item_data.items():
          #print("name: {0}, container: {1}, amount: {2}".format(v_world['name'], v_world['container'], v_world['amount']))

          #if v_world["container"] == healer_vendor_serial:
          if v_world["amount"] == 250:
            #print("item v_world: ", v_world)
            #print("healer_vendor_serial: ", healer_vendor_serial)
            print("item / name: {0}, layer: {1}, amount: {2}".format(v_world["name"], 
                                                                     v_world["layer"],
                                                                     v_world["amount"]))
            pass
            #print("")
        #print("")

    gold_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')

    if gold_serial in backpack_item_data:
      gold_info = backpack_item_data[gold_serial]
    else:
      pass

    if len(uo_service.player_status_dict) != 0:
      player_gold = uo_service.player_status_dict['gold']
      #print("player_gold: ", player_gold)

    ## Declare the empty action
    if step % 100 == 0:
      if len(backpack_item_data) != 0:
        for k_backpack, v_backpack in backpack_item_data.items():
          #print("backpack {0}: {1}".format(k_backpack, v_backpack["name"]))
          pass
        #print("")

      #print("step: ", step)
      #print("healer_vendor_serial: ", healer_vendor_serial)
      #print("select_pop_up_flag: ", select_pop_up_flag)
      #print("popup_menu_list: ", popup_menu_list)
      #print("")

      if open_pop_up_flag == True and healer_vendor_serial != None:
        print("open the pop up menu of NPC")

        action['action_type'] = 10
        action['target_serial'] = healer_vendor_serial

        open_pop_up_flag = False
        select_pop_up_flag = True
      elif select_pop_up_flag == True and len(popup_menu_list) != 0:
        print("select the pop up menu")

        action['action_type'] = 11
        action['target_serial'] = healer_vendor_serial

        menu_index = 0
        for i in range(0, len(popup_menu_list)):
          if popup_menu_list[i].text == "Buy" and popup_menu_list[i].active == True:
            action['index'] = i

        uo_service.popup_menu_list = []
        select_pop_up_flag = False

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
  thread_1 = threading.Thread(target=uo_service.parse_land_static, daemon=True, args=( ))

  thread_2.start()
  thread_1.start()

  thread_2.join()
  thread_1.join()


## Start the main function
if __name__ == '__main__':
  main()