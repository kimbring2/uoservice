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

  ## Event flags to test the scenario manually
  target_skeleton_serial = None

  ## Event flags to test the scenario manually
  for step in tqdm(range(100000)):
    ## Parse the x and y position of player 
    player_game_x = uo_service.player_game_x
    player_game_y = uo_service.player_game_y

    if len(uo_service.world_mobile_dict) != 0 and target_skeleton_serial == None:
      ## Obtain the serial number list of skeleton around the player
      skeleton_serial_list = [k for k, v in uo_service.world_mobile_dict.items() \
                        if v['name'] == ' A Skeleton ' and v['distance'] <= 15 and v['distance'] > 5]

      ## Select of skeleton
      target_skeleton_serial = random.choice(skeleton_serial_list)

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
    if step % 50 == 0:
      print("step: ", step)
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

        if direction != -1:
          # Walk action
          action['action_type'] = 1
          action['walk_direction'] = direction
          action['run'] = True

    uo_service.step(action)


## Start the main function
if __name__ == '__main__':
  main()