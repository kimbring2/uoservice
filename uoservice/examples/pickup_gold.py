# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Short game scenario: Pick up item from backpack and drop on near ground
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
  target_item_serial = None

  ## Event flags to test the scenario manually
  pick_up_flag = False
  drop_flag = False

  ## Event flags to test the scenario manually
  for step in tqdm(range(100000)):
    #print("ground_item_dict: ", obs["ground_item_dict"])

    ## Obtain the serial of random mobile around the player
    if len(obs["ground_item_dict"]) != 0 and target_item_serial == None:
      print("ground_item_dict: ", obs["ground_item_dict"])
      
      ## Format of item data
      ## 1074150311: ['46 Gold Coin', 'Item', 866, 574, 3, 'None']

      target_item_serial = utils.get_serial_by_name(obs["ground_item_dict"], 'Gold')
      print("target_item_serial: ", target_item_serial)

    item_serial = 0

    ## Obtain the serial of Gold from players' backpack information
    if len(obs["backpack_item_data"]) != 0:
      item_serial, index = utils.get_serial_by_name(obs["backpack_item_data"], "Gold")

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
    if step % 200 == 0:
      print("step: ", step)

      if pick_up_flag == True and item_serial != 0:
        # Pick up the item
        action['action_type'] = 3
        action['item_serial'] = item_serial
        action['amount'] = 100
        pick_up_flag = False
        drop_flag = True
        print("action: ", action)
      elif drop_flag == True:
        # Drop the item
        action['action_type'] = 5
        print("action: ", action)
        drop_flag = False

    obs = uo_service.step(action)


## Start the main function
if __name__ == '__main__':
  main()