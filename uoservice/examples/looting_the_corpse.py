# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Game scenario 3: Kill the monster and loot the gold from it
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

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoService import UoService
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
  ## Event flags to test the scenario manually
  target_skeleton_serial = None
  corpse_dict = {}
  corpse_serial = None
  hold_item_serial = 0
  corpse_item_dict = {}

  ## Event flags to test the scenario manually
  step = 0
  while True:
    ## Parse the x and y position of player 
    player_game_x = uo_service.player_game_x
    player_game_y = uo_service.player_game_y

    if len(uo_service.world_mobile_dict) != 0 and target_skeleton_serial == None:
      ## Obtain the serial number list of skeleton around the player
      skeleton_serial_list = [k for k, v in uo_service.world_mobile_dict.items() \
                        if v['name'] == ' A Skeleton ' and v['distance'] <= 10 and v['distance'] > 1]

      ## Select of skeleton
      if len(skeleton_serial_list) != 0:
        target_skeleton_serial = random.choice(skeleton_serial_list)

    corpse_dict = {}
    for k, v in uo_service.world_item_dict.items():
      if v["isCorpse"] == True:
        corpse_dict[k] = v

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    ## Declare the empty action
    if step % 100 == 0:
      #print("step: ", step)
      if len(uo_service.player_status_dict) != 0:
        player_gold = uo_service.player_status_dict['gold']
        print("player_gold: ", player_gold)

      if target_skeleton_serial != None and player_game_x != None:
        ## finally, we can acquire the target mobile data
        if target_skeleton_serial in uo_service.world_mobile_dict:
          target_skeleton = uo_service.world_mobile_dict[target_skeleton_serial]
        else:
          target_skeleton_serial = None
          continue

        ## Parse x and y position of target mobile
        target_skeleton_game_x = target_skeleton["gameX"]
        target_skeleton_game_y = target_skeleton["gameY"]

        ## Calculate the directons to move toward the target mobile
        direction = utils.get_walk_direction_to_target([player_game_x, player_game_y], 
                                                       [target_skeleton_game_x, target_skeleton_game_y])

        ## Distance between the player and target mobile
        distance = target_skeleton['distance']

        ## Player war mode
        war_mode = uo_service.war_mode

        ## Player holded item
        hold_item_serial = uo_service.hold_item_serial
        print("hold_item_serial: ", hold_item_serial)

        backpack_serial = uo_service.backpack_serial
        #print("backpack_serial: ", backpack_serial)

        for k_corpse, v_corpse in corpse_dict.items():
          for k_world, v_world in uo_service.world_item_dict.items():
            if k_corpse == v_world["container"]:
              if k_world not in corpse_item_dict:
                corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]
              else:
                corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]

        if len(corpse_dict) == 0:
          if distance >= 2:
            ## Target mobile is far away from the player
            if direction == -1:
              # Can not find the walk direction
              action['action_type'] = 0
            else:
              ## Walk toward target mobile
              action['action_type'] = 1
              action['walk_direction'] = direction
              action['run'] = True
          else:
            ## Player is near the target
              if war_mode == False:
                ## Change the war mode to combat to attack
                action['action_type'] = 19
                action['index'] = 1
              else:
                ## Attack the target mobile
                action['action_type'] = 2
                action['target_serial'] = target_skeleton_serial
        else:
          if len(corpse_item_dict) == 0:
            ## Open the corpse container
            corpse_serial_list = list(corpse_dict.keys())
            corpse_serial_data = random.choice(corpse_serial_list)
            if corpse_serial == None:
              corpse_serial = corpse_serial_data

            action['action_type'] = 2
            action['target_serial'] = corpse_serial
          else:
            if hold_item_serial == 0:
              ## Pick up the gold from corpse
              gold_item_serial, gold_item_max = \
                utils.get_serial_amount_from_corpse_item_list(corpse_item_dict, 'Gold')

              action['action_type'] = 3
              action['target_serial'] = gold_item_serial
              action['amount'] = gold_item_max
            else:
              ## Drop item into backpack
              action['action_type'] = 4
              action['target_serial'] = backpack_serial

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


'''
## Declare the main function
def main():
  ## Declare the UoService using the parsed argument
  uo_service = UoService(grpc_port, window_width, window_height)

  ## Open the gRPC client to connect with gRPC server of CSharp part
  uo_service._open_grpc()

  ## Send the reset signal to gRPC server
  obs = uo_service.reset()

  ## Event flags to test the scenario manually
  target_skeleton_serial = None
  corpse_dict = {}
  corpse_serial = None
  hold_item_serial = 0
  corpse_item_dict = {}

  ## Event flags to test the scenario manually
  for step in range(100000):
    ## Parse the x and y position of player 
    player_game_x = uo_service.player_game_x
    player_game_y = uo_service.player_game_y

    if len(uo_service.world_mobile_dict) != 0 and target_skeleton_serial == None:
      ## Obtain the serial number list of skeleton around the player
      skeleton_serial_list = [k for k, v in uo_service.world_mobile_dict.items() \
                        if v['name'] == ' A Skeleton ' and v['distance'] <= 10 and v['distance'] > 1]

      ## Select of skeleton
      if len(skeleton_serial_list) != 0:
        target_skeleton_serial = random.choice(skeleton_serial_list)

    corpse_dict = {}
    for k, v in uo_service.world_item_dict.items():
      if v["isCorpse"] == True:
        corpse_dict[k] = v

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    ## Declare the empty action
    if step % 150 == 0:
      #print("step: ", step)
      if len(uo_service.player_status_dict) != 0:
        player_gold = uo_service.player_status_dict['gold']
        print("player_gold: ", player_gold)

      if target_skeleton_serial != None and player_game_x != None:
        ## finally, we can acquire the target mobile data
        if target_skeleton_serial in uo_service.world_mobile_dict:
          target_skeleton = uo_service.world_mobile_dict[target_skeleton_serial]
        else:
          target_skeleton_serial = None
          continue

        ## Parse x and y position of target mobile
        target_skeleton_game_x = target_skeleton["gameX"]
        target_skeleton_game_y = target_skeleton["gameY"]

        ## Calculate the directons to move toward the target mobile
        direction = utils.get_walk_direction_to_target([player_game_x, player_game_y], 
                                                       [target_skeleton_game_x, target_skeleton_game_y])

        ## Distance between the player and target mobile
        distance = target_skeleton['distance']

        ## Player war mode
        war_mode = uo_service.war_mode

        ## Player holded item
        hold_item_serial = uo_service.hold_item_serial

        backpack_serial = uo_service.backpack_serial
        #print("backpack_serial: ", backpack_serial)

        for k_corpse, v_corpse in corpse_dict.items():
          for k_world, v_world in uo_service.world_item_dict.items():
            if k_corpse == v_world["container"]:
              if k_world not in corpse_item_dict:
                corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]
              else:
                corpse_item_dict[k_world] = uo_service.world_item_dict[k_world]

        if len(corpse_dict) == 0:
          if distance >= 2:
            ## Target mobile is far away from the player
            if direction == -1:
              # Can not find the walk direction
              action['action_type'] = 0
            else:
              ## Walk toward target mobile
              action['action_type'] = 1
              action['walk_direction'] = direction
              action['run'] = True
          else:
            ## Player is near the target
              if war_mode == False:
                ## Change the war mode to combat to attack
                action['action_type'] = 19
                action['index'] = 1
              else:
                ## Attack the target mobile
                action['action_type'] = 2
                action['target_serial'] = target_skeleton_serial
        else:
          if len(corpse_item_dict) == 0:
            ## Open the corpse container
            corpse_serial_list = list(corpse_dict.keys())
            corpse_serial_data = random.choice(corpse_serial_list)
            if corpse_serial == None:
              corpse_serial = corpse_serial_data

            action['action_type'] = 7
            action['target_serial'] = corpse_serial
          else:
            if hold_item_serial == 0:
              ## Pick up the gold from corpse
              gold_item_serial, gold_item_max = \
                utils.get_serial_amount_from_corpse_item_list(corpse_item_dict, 'Gold')

              action['action_type'] = 3
              action['target_serial'] = gold_item_serial
              action['amount'] = gold_item_max
            else:
              ## Drop item into backpack
              action['action_type'] = 4
              action['target_serial'] = backpack_serial

        #print("action_type: ", action['action_type'])
        obs = uo_service.step(action)
    else:
      obs = uo_service.step(action)


## Start the main function
if __name__ == '__main__':
  main()
'''