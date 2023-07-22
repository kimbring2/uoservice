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
  step = 0
  open_pop_up_flag = True
  select_pop_up_flag = False
  training_price = None
  pick_up_gold_flag = False
  giving_gold_flag = False

  one_trial_check_flag = True

  while True:
    miner_teacher_serial = None
    miner_teacher = None

    if len(uo_service.world_mobile_dict) != 0:
      for k_world, v_world in uo_service.world_mobile_dict.items():
        #print("name: {0}, title: {1}, distance: {2}".format(v_world['name'], v_world['title'], v_world['distance']))
        # name:  Jacob Waltzt The Miner Instructor, title:  Jacob Waltzt The Miner Instructor
        # name:  Gervis The Blacksmith Trainer, title:  Gervis the blacksmith trainer
        # name:  Mugg The Miner, title:  Mugg the miner
        # name:  Orane The Miner, title:  Orane the miner
        # name:  Grizzled Mare , title:  Grizzled Mare
        if "Orane" in v_world["name"] and "miner" in v_world["title"]:
          miner_teacher_serial = k_world
          miner_teacher = uo_service.world_mobile_dict[miner_teacher_serial]

      #print("")

    ## Player status
    hold_item_serial = uo_service.hold_item_serial
    cliloc_dict = uo_service.cliloc_dict
    backpack_serial = uo_service.backpack_serial
    cliloc_dict = uo_service.cliloc_dict
    popup_menu_list = uo_service.popup_menu_list
    player_skills_dict = uo_service.player_skills_dict

    if "Mining" in player_skills_dict:
      mining_skill_level = player_skills_dict["Mining"]["value"]
      #print("mining_skill_level: ", mining_skill_level)

    backpack_item_data = uo_service.backpack_item_dict
    gold_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')

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

      print("cliloc_dict: ", cliloc_dict)
      print("popup_menu_list: ", popup_menu_list)

      if miner_teacher_serial != None:
        if miner_teacher_serial in cliloc_dict:
          #[{'text': ' Orane the miner', 'affix': '', 'name': 'Orane'}, 
          # {'text': ' Orane the miner', 'affix': '', 'name': 'Orane'}, 
          # {'text': 'I will teach thee all I know, if paid the amount in full.  The price is: 225', 'affix': ' 225', 'name': 'Orane'}, 
          # {'text': 'For less I shall teach thee less.', 'affix': '', 'name': 'Orane'}]
          for cliloc_data in cliloc_dict[miner_teacher_serial]:
            if cliloc_data["affix"] != '':
              training_price = int(cliloc_data["affix"])
              if one_trial_check_flag == True:
                pick_up_gold_flag = True
                one_trial_check_flag = False

      if open_pop_up_flag == True and miner_teacher_serial != None and mining_skill_level < 20:
        print("open the pop up menu of NPC")

        action['action_type'] = 10
        action['target_serial'] = miner_teacher_serial

        open_pop_up_flag = False
        select_pop_up_flag = True
      elif select_pop_up_flag == True and len(popup_menu_list) != 0:
        print("select the pop up menu")

        action['action_type'] = 11
        action['target_serial'] = miner_teacher_serial

        menu_index = 0
        for i in range(0, len(popup_menu_list)):
          if popup_menu_list[i].text == "Train Mining" and popup_menu_list[i].active == True:
            action['index'] = i

        uo_service.popup_menu_list = []
        select_pop_up_flag = False
      elif training_price != None and pick_up_gold_flag == True and backpack_serial != None and gold_serial != None:
        print("pick up gold to before giving it to NPC")

        action['action_type'] = 3
        action['target_serial'] = gold_serial
        action['amount'] = training_price

        pick_up_gold_flag = False
        giving_gold_flag = True
      elif giving_gold_flag == True:
        print("giving the gold to NPC")

        action['action_type'] = 4
        action['target_serial'] = miner_teacher_serial

        giving_gold_flag = False

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
  thread_1 = threading.Thread(target=uo_service.parse_land_static, daemon=True, args=())

  thread_2.start()
  thread_1.start()

  thread_2.join()
  thread_1.join()


## Start the main function
if __name__ == '__main__':
  main()