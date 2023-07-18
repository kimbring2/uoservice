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


color_dict = {"Black": (0, 0, 0),
              "Red": (0, 0, 255),
              "Blue": (255, 0, 0),
              "Lime": (0, 255, 0),
              "Green": (0, 128, 0),
              "Yellow": (0, 255, 255),
              "Purple": (128, 255, 128),
              "Gray": (128, 128, 128),
              "Brown": (42, 42, 165),
             }


def parse_land_static(uo_service):
  while True:
    #print("parse_land_static(): {0}".format(uo_service.total_step))

    if uo_service.max_tile_x != None:
      #print("parse_land_static(): {0}".format(uo_service.total_step))

      screen_image = np.zeros((1000,1000,4), dtype=np.uint8)
      radius = 5
      thickness = 2
      screen_width = 1000
      screen_height = 1000

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

      player_game_x = uo_service.player_game_x
      player_game_y = uo_service.player_game_y

      scale = 40

      cell_zip = zip(cell_x_list, cell_y_list)
      for cell_x in cell_x_list:
        for cell_y in cell_y_list:
          land_data_list, static_data_list = uo_service.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)

          for land_data in land_data_list:
            #print("land / name: {0}, game_x: {1}, game_y: {2}".format(land_data["name"], land_data["game_x"], land_data["game_y"]))
            start_point = ( (land_data["game_x"] - player_game_x) * scale + 500 - int(scale / 2), 
                            (land_data["game_y"] - player_game_y) * scale + 500 - int(scale / 2) )
            end_point = ( (land_data["game_x"] - player_game_x) * scale + 500 + int(scale / 2), 
                          (land_data["game_y"] - player_game_y) * scale + 500 + int(scale / 2) )

            index = uo_service.get_land_index(land_data["game_x"], land_data["game_y"])

            radius = 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = ( (land_data["game_x"] - player_game_x) * scale + 500 - int(scale / 2), 
                    (land_data["game_y"] - player_game_y) * scale + 500 )
            fontScale = 0.4
            color = (255, 0, 0)
            thickness = 1
            screen_image = cv2.putText(screen_image, str(index), org, font, fontScale, color, thickness, cv2.LINE_4)

            if land_data["name"] == "forest":
              #screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Lime"], 1)
              pass
            else:
              screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Gray"], 1)

          for static_data in static_data_list:
            #if "water" not in static_data["name"]:
              #print("static / name: {0}, game_x: {1}, game_y: {2}".format(static_data["name"], static_data["game_x"], static_data["game_y"]))
            
            start_point = ( (static_data["game_x"] - player_game_x) * scale + 500 - int(scale / 2), 
                            (static_data["game_y"] - player_game_y) * scale + 500 - int(scale / 2) )
            end_point = ( (static_data["game_x"] - player_game_x) * scale + 500 + int(scale / 2), 
                          (static_data["game_y"] - player_game_y) * scale + 500 + int(scale / 2) )

            if "wood" in static_data["name"]:
              screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Brown"], 1)
            elif "grasses" in static_data["name"]:
              screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Green"], 1)
            #elif "water" in static_data["name"]:
            #  screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Blue"], 1)

      boundary = 500

      radius = 1
      thickness = 1
      screen_width = 4000
      screen_height = 4000
      for k, v in uo_service.world_mobile_dict.items():
        if uo_service.player_game_x != None:
          if v["gameX"] < screen_width and v["gameY"] < screen_height:
            #screen_image = cv2.circle(screen_image, (v["gameX"], v["gameY"]), radius, (0, 0, 255), thickness)
            pass

      for k, v in uo_service.world_item_dict.items():
        if uo_service.player_game_x != None:
          #print("world item {0}: {1}".format(k, uo_service.world_item_dict[k]))
          if v["gameX"] < screen_width and v["gameY"] < screen_height:
            screen_image = cv2.circle(screen_image, 
                                      ( 
                                          (v["gameX"] - player_game_x) * scale + 500, 
                                          (v["gameY"] - player_game_y) * scale + 500
                                      ),
                                      radius, (0, 0, 255), thickness)
            #pass
      #print("")

      if uo_service.player_game_x != None:
        #print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))

        radius = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (500 - 16, 500)
        fontScale = 0.5
        color = (255, 0, 0)
        thickness = 1
        #screen_image = cv2.putText(screen_image, str("player"), org, font, fontScale, color, thickness, cv2.LINE_4)

        screen_image = cv2.circle(screen_image, (500, 500), radius, (0, 255, 0), thickness)
        
        screen_image = screen_image[500 - boundary:500 + boundary, 500 - boundary:500 + boundary, :]
        
        '''
        if uo_service.player_game_y > boundary and uo_service.player_game_x > boundary:
          screen_image = screen_image[500 - boundary:500 + boundary, 
                                      500 - boundary:500 + boundary, :]
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
        '''
        
      
      screen_image = cv2.resize(screen_image, (1000, 1000), interpolation=cv2.INTER_AREA)
      screen_image = utils.rotate_image(screen_image, -45)
      cv2.imshow('screen_image_' + str(uo_service.grpc_port), screen_image)
      cv2.waitKey(1)

      time.sleep(1.0)
      

def step(uo_service):
  target_skeleton_serial = None

  step = 0
  while True:
    #print("step()")

    ## Declare the empty action
    action = {}
    action['action_type'] = 0
    action['source_serial'] = 0
    action['target_serial'] = 0
    action['walk_direction'] = 0
    action['index'] = 0
    action['amount'] = 0
    action['run'] = False

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
    if step % 150 == 0:
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

    obs = uo_service.step(action)
    step += 1


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