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
  target_mobile_serial = None

  ## Event flags to test the scenario manually
  for step in tqdm(range(100000)):
    ## Obtain the serial of random mobile around the player
    #print("player_game_x: {0}, player_game_y: {1}".format(uo_service.player_game_x, uo_service.player_game_y))
    #for k_mobile, v_mobile in uo_service.world_mobile_dict.items():
    #  print("mobile item {0}: {1}".format(k_mobile, uo_service.world_mobile_dict[k_mobile]))

    #print("len(uo_service.world_mobile_dict): ", len(uo_service.world_mobile_dict))

    ## Parse the x and y position of player 
    player_game_x = uo_service.player_game_x
    player_game_y = uo_service.player_game_y

    if len(uo_service.world_mobile_dict) != 0 and target_mobile_serial == None:
      ## Obtain the serial list of mobiles in current game screen 
      mobile_serial_list = list(uo_service.world_mobile_dict.keys())

      ## Obtain the serial list of mobiles in current game screen
      target_mobile_serial = random.choice(mobile_serial_list)

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['item_serial'] = 0
    action['mobile_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    ## Declare the empty action
    if step % 50 == 0:
      print("step: ", step)
      #print("target_mobile_serial: ", target_mobile_serial)

      if target_mobile_serial != None and player_game_x != None:
        ## finally, we can acquire the target mobile data
        if target_mobile_serial in uo_service.world_mobile_dict:
          target_mobile = uo_service.world_mobile_dict[target_mobile_serial]
        else:
          target_mobile_serial = None
          continue

        print("target_mobile: ", target_mobile)

        ## Parse x and y position of target mobile
        target_mobile_game_x = target_mobile["gameX"]
        target_mobile_game_y = target_mobile["gameY"]

        ## Calculate the directons to move toward the target mobile
        direction = utils.get_walk_direction_to_target([player_game_x, player_game_y], 
                                                       [target_mobile_game_x, target_mobile_game_y])

        #print("direction: ", direction)
        if direction != -1:
          # Walk action
          action['action_type'] = 1
          action['walk_direction'] = direction
          action['run'] = True

    uo_service.step(action)


## Start the main function
if __name__ == '__main__':
  main()