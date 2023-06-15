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
  corpse_serial = None
  hold_item_serial = 0

  ## Event flags to test the scenario manually
  for step in tqdm(range(100000)):
    ## Obtain the serial of random mobile around the player
    if len(obs["mobile_data"]) != 0 and target_mobile_serial == None:
      ## Format of mobile data
      ## [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
      ## 16852: ['a zombie', 'Mobile', 646, 22, 16, ' a zombie ']

      ## Obtain the serial list of mobiles in current game screen 
      mobile_serial_list = list(obs["mobile_data"].keys())

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
    if step % 150 == 0:
      print("step: ", step)

      ## [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
      ## {1074164822: ['A Skeletal Corpse', 'Item', 734, 662, 2, 'None']}
      
      if len(obs['corpse_data']) != 0:
        corpse_serial_list = list(obs['corpse_data'].keys())
        corpse_serial_data = random.choice(corpse_serial_list)
        if corpse_serial == None:
          corpse_serial = corpse_serial_data
      
      if target_mobile_serial != None:
        ## format of player mobile data 
        ## [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
        ## 120: ['masterkim', 'PlayerMobile', 778, 618, 0, 'None']
        player_mobile_serial = list(obs['player_mobile_data'].keys())[0]
        player_mobile = obs['player_mobile_data'][player_mobile_serial]

        ## finally, we can acquire the target mobile data
        if target_mobile_serial in obs["mobile_data"]:
          target_mobile = obs["mobile_data"][target_mobile_serial]
        else:
          target_mobile_serial = None
          continue

        ## Parse the x and y position of player 
        player_screen_x = player_mobile[2]
        player_screen_y = player_mobile[3]

        ## Parse x and y position of target mobile
        target_mobile_screen_x = target_mobile[2]
        target_mobile_screen_y = target_mobile[3]

        ## Calculate the directons to move toward the target mobile
        direction = utils.get_walk_direction_to_target([player_screen_x, player_screen_y], 
                                                       [target_mobile_screen_x, target_mobile_screen_y])

        ## Distance between the player and target mobile
        distance = target_mobile[4]

        ## Format of player status
        '''player_status_dict:  {'str': 100, 'dex': 62, 'intell': 133, 'hits': 121, 'hitsMax': 121, 
                                 'stamina': 70, 'staminaMax': 70, 'mana': 148, 'gold': 46739, 
                                 'physicalResistance': 88, 'weight': 654, 'weightMax': 450, 
                                 'HoldItemSerial': 0, 'warMode': True}'''
        if 'player_status_data' in obs:
          war_mode = obs['player_status_data']['warMode']
          hold_item_serial = obs['player_status_data']['HoldItemSerial']

        #print("obs['corpse_data']: ", obs['corpse_data'])
        #print("opened_corpse_data: ", obs['opened_corpse_data'])

        if len(obs['corpse_data']) == 0:
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
                action['mobile_serial'] = target_mobile_serial
        else:
          if len(obs['opened_corpse_data']) == 0:
            ## Open the corpse container
            corpse_serial_list = list(obs['corpse_data'].keys())
            corpse_serial_data = random.choice(corpse_serial_list)
            if corpse_serial == None:
              corpse_serial = corpse_serial_data

            action['action_type'] = 7
            action['item_serial'] = corpse_serial
          else:
            if hold_item_serial == 0:
              print("action['action_type'] = 3")

              opened_corpse_serial_list = list(obs['opened_corpse_data'].keys())
              opened_corpse_serial = random.choice(opened_corpse_serial_list)
              opened_corpse_item_list = obs['opened_corpse_data'][opened_corpse_serial]
              gold_item_serial, gold_item_max = \
                utils.get_serial_amount_from_corpse_item_list(opened_corpse_item_list, 'Gold')

              action['action_type'] = 3
              action['item_serial'] = gold_item_serial
              action['amount'] = gold_item_max
            else:
              print("action['action_type'] = 4")
              print("distance: ", distance)

              ## Item loot action
              action['action_type'] = 4

        print("action_type: ", action['action_type'])
        obs = uo_service.step(action)
        #break

        print("")
    else:
      obs = uo_service.step(action)


## Start the main function
if __name__ == '__main__':
  main()