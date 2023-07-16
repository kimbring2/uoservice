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
parser.add_argument('--window_width', type=int, default=1370, help='screen width of game')
parser.add_argument('--window_height', type=int, default=1280, help='screen height of game')
parser.add_argument('--grpc_port', type=int, default=60051, help='port of grpc')

## Parse the command argument
arguments = parser.parse_args()
grpc_port = arguments.grpc_port
window_width = arguments.window_width
window_height = arguments.window_height

#uoservice_game_file_parser = UoServiceGameFileParser("/home/kimbring2/.wine/drive_c/Program Files (x86)/Electronic Arts/Ultima Online Classic")
#uoservice_game_file_parser.load()
#uoservice_game_file_parser.get_tile_data(438, 313)


def parse_land_static(uo_service):
  while True:
    print("parse_land_static(): {0}".format(uo_service.total_step))
    if uo_service.max_tile_x != None:

      screen_image = np.zeros((4000,4000,4), dtype=np.uint8)
      radius = 5
      thickness = 2
      screen_width = 4000
      screen_height = 4000

      cell_x_list = []
      cell_y_list = []
      tile_data_list = []

      for x in range(uo_service.min_tile_x, uo_service.max_tile_x):
        cell_x = x >> 3
        if cell_x not in cell_x_list:
          cell_x_list.append(cell_x)

      for y in range(uo_service.min_tile_y, uo_service.max_tile_y):
        cell_y = y >> 3
        if cell_y not in cell_y_list:
          cell_y_list.append(cell_y)

      #print("cell_x_list: {0}, cell_y_list: {1}: ".format(cell_x_list, cell_y_list))
      cell_zip = zip(cell_x_list, cell_y_list)
      for cell_x in cell_x_list:
        for cell_y in cell_y_list:
          #print("cell: ({0}, {1})".format(cell_x, cell_y))
          tile_data = uo_service.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)

          for tile in tile_data:
            #print("name: {0}, game_x: {1}, game_y: {2}".format(tile["name"], tile["game_x"], tile["game_y"]))
            if tile["name"] == "forest":
              #print("name: {0}, game_x: {1}, game_y: {2}".format(tile["name"], tile["game_x"], tile["game_y"]))
              screen_image = cv2.circle(screen_image, (tile["game_x"], tile["game_y"]), 1, (128, 0, 128), 1)
              pass
          
          tile_data_list.append(tile_data)

      boundary = 50

      '''
      radius = 1
      thickness = 2
      screen_width = 4000
      screen_height = 4000
      for k, v in self.world_mobile_dict.items():
        if self.player_game_x != None:
          if v["gameX"] < screen_width and v["gameY"] < screen_height:
            screen_image = cv2.circle(screen_image, (v["gameX"], v["gameY"]), radius, (0, 0, 255), thickness)
            pass

      '''
      if uo_service.player_game_x != None:
        #print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))

        radius = 1
        screen_image = cv2.circle(screen_image, (uo_service.player_game_x, uo_service.player_game_y), radius, (0, 255, 0), thickness)
        if uo_service.player_game_y > boundary and uo_service.player_game_x > boundary:
          screen_image = screen_image[uo_service.player_game_y - boundary:uo_service.player_game_y + boundary, 
                                      uo_service.player_game_x - boundary:uo_service.player_game_x + boundary, :]
        elif uo_service.player_game_y < boundary and uo_service.player_game_x > boundary:
          #print("self.player_game_y < 600 and self.player_game_x > 600")
          screen_image = screen_image[0:uo_service.player_game_y + boundary, 
                                      uo_service.player_game_x - boundary:uo_service.player_game_x + boundary, :]
        elif uo_service.player_game_y > boundary and uo_service.player_game_x < boundary:
          #print("self.player_game_y > 600 and self.player_game_x < 600")
          screen_image = screen_image[uo_service.player_game_y - boundary:uo_service.player_game_y + boundary, 
                                      0:uo_service.player_game_x + boundary, :]
        else:
          #print("else")
          screen_image = screen_image[0:uo_service.player_game_y + boundary, 0:uo_service.player_game_x + boundary, :]
      
      screen_image = cv2.resize(screen_image, (boundary * 4, boundary * 4), interpolation=cv2.INTER_AREA)
      screen_image = utils.rotate_image(screen_image, -45)
      cv2.imshow('screen_image_' + str(uo_service.grpc_port), screen_image)
      cv2.waitKey(1)
      
      #time.sleep(1.0)

      #return tile_data_list
    #else:
      #return None


def step(uo_service):
  player_gold = None
  pick_up_flag = True
  drop_flag = False

  step = 0
  while True:
    print("step()")

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

    backpack_item_data = uo_service.backpack_item_dict
    #print("backpack_item_data: ", backpack_item_data)
    for k_backpack, v_backpack in backpack_item_data.items():
      #print("backpack {0}: {1}".format(k_backpack, v_backpack))
      pass

    #for k_mobile, v_mobile in uo_service.world_mobile_dict.items():
    #  print("world_mobile {0}: {1}".format(k_mobile, v_mobile))

    equipped_item_data = uo_service.equipped_item_dict
    #print("equipped_item_data: ", equipped_item_data)

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    gold_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if gold_serial in backpack_item_data:
      gold_info = backpack_item_data[gold_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

    if len(uo_service.player_status_dict) != 0:
      player_gold = uo_service.player_status_dict['gold']
      #print("player_gold: ", player_gold)

    ## Declare the empty action
    if step % 150 == 0:
      print("step: ", step)
      #print("gold_serial: ", gold_serial)
      if gold_serial != None and pick_up_flag == True:
        action['action_type'] = 0
        action['target_serial'] = gold_serial
        action['amount'] = 100
        pick_up_flag = False
        drop_flag = True
      elif drop_flag == True:
        #if len(uo_service.near_land_object_dict) != 0:
        if True:
          action['action_type'] = 4

          #drop_index = random.randint(0, len(near_land_object_dict))
          action['index'] = 0
          drop_flag = False

      obs = uo_service.step(action)
    else:
      obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Declare the main function
def main():
  ## Declare the UoService using the parsed argument
  uo_service = UoService(grpc_port, window_width, window_height)

  ## Open the gRPC client to connect with gRPC server of CSharp part
  uo_service._open_grpc()

  ## Send the reset signal to gRPC server
  obs = uo_service.reset()

  thread_2 = threading.Thread(target=step, daemon=True, args=(uo_service,))
  thread_1 = threading.Thread(target=parse_land_static, daemon=True, args=(uo_service,))

  thread_2.start()
  thread_1.start()

  thread_2.join()
  thread_1.join()


## Start the main function
if __name__ == '__main__':
  main()