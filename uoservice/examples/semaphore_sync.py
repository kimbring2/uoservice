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
  #for step in tqdm(range(100000)):

  corpse_gold_serial = None

  step = 0
  while True:
    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['item_serial'] = 0
    action['mobile_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    backpack_item_data = uo_service.backpack_item_dict
    #print("backpack_item_data: ", backpack_item_data)

    equipped_item_data = uo_service.equipped_item_dict
    #print("equipped_item_data: ", equipped_item_data)

    corpse_dict = uo_service.corpse_dict
    #print("corpse_dict: ", corpse_dict)

    corpse_item_dict = uo_service.corpse_item_dict
    #print("corpse_item_dict: ", corpse_item_dict)

    for k_corpse, v_corpse in corpse_item_dict.items():
      #print("corpse {0}: {1}".format(k_corpse, v_corpse))
      for k_item, v_item in v_corpse.items():
        #print("corpse item {0}: {1}".format(k_item, v_item))

        if 'Gold' in v_item[0]:
          #print("corpse gold item {0}: {1}".format(k_item, v_item))
          corpse_gold_serial = k_item

        if corpse_gold_serial != None:
          #print("corpse_gold_serial: ", corpse_gold_serial)
          #action['action_type'] = 3
          #action['item_serial'] = corpse_gold_serial
          #print("v_corpse[corpse_gold_serial][-1]: ", v_corpse[corpse_gold_serial][-1])
          #action['amount'] = corpse_item_dict[corpse_gold_serial][-1]
          pass

    #print("player_skills_dict: ", uo_service.player_skills_dict)
    if 'Swordsmanship' in uo_service.player_skills_dict:
      swordsmanship_skill = uo_service.player_skills_dict['Swordsmanship']
      #print("swordsmanship_skill: ", swordsmanship_skill)

    gold_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if gold_serial in backpack_item_data:
      gold_info = backpack_item_data[gold_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

    ## Declare the empty action
    if step % 500 == 0:
      print("step: ", step)
      print("action: ", action)

      obs = uo_service.step(action)
    else:
      obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Start the main function
if __name__ == '__main__':
  main()