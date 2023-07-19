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
              "White": (255, 255, 255),
             }


def parse_land_static(uo_service):
  while True:
    #print("parse_land_static(): {0}".format(uo_service.total_step))

    if uo_service.max_tile_x != None:
      #print("parse_land_static(): {0}".format(uo_service.total_step))

      screen_length = 1000

      screen_image = np.zeros((screen_length,screen_length,4), dtype=np.uint8)
      radius = 5
      thickness = 2
      screen_width = screen_length
      screen_height = screen_length

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
            start_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
                            (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
            end_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
                          (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

            index = uo_service.get_land_index(land_data["game_x"], land_data["game_y"])

            radius = 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
                    (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) )
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
            
            start_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
                            (static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
            end_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
                          (static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

            #if "grasses" in static_data["name"]:
            #  screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Green"], 1)
            if "wall" in static_data["name"]:
              screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["White"], -1)
            #elif "wood" in static_data["name"]:
            #  screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Brown"], 1)

            #elif "water" in static_data["name"]:
            #  screen_image = cv2.rectangle(screen_image, start_point, end_point, color_dict["Blue"], 1)

      boundary = 500

      radius = int(scale / 2)
      screen_width = 4000
      screen_height = 4000
      for k, v in uo_service.world_mobile_dict.items():
        if uo_service.player_game_x != None:
          if v["gameX"] < screen_width and v["gameY"] < screen_height:
            screen_image = cv2.circle(screen_image, 
                                      ( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
                                        (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
                                      radius, color_dict["Red"], -1)

            screen_image = cv2.putText(screen_image, "  " + v["name"], 
                                       ( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
                                         (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_dict["Red"], 2, cv2.LINE_4)

      for k, v in uo_service.world_item_dict.items():
        if uo_service.player_game_x != None:
          #print("world item {0}: {1}".format(k, uo_service.world_item_dict[k]))
          if v["gameX"] < screen_width and v["gameY"] < screen_height:
            screen_image = cv2.circle(screen_image, 
                                      ( 
                                          (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
                                          (v["gameY"] - player_game_y) * scale + int(screen_length / 2)
                                      ),
                                      radius, color_dict["Purple"], -1)
           
            item_name_list = v["name"].split(" ")
            screen_image = cv2.putText(screen_image, "     " + item_name_list[-1], 
                                       ( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
                                         (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_dict["Purple"], 2, cv2.LINE_4)


      if uo_service.player_game_x != None:
        #print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))

        screen_image = cv2.putText(screen_image, str("player"), (int(screen_length / 2), int(screen_length / 2) - int(scale / 2)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_dict["Green"], 4, cv2.LINE_4)

        radius = int(scale / 2)
        screen_image = cv2.circle(screen_image, (int(screen_length / 2), int(screen_length / 2)), radius, color_dict["Lime"], -1)
        screen_image = screen_image[int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, 
                                    int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, :]
        
      screen_image = cv2.resize(screen_image, (screen_length, screen_length), interpolation=cv2.INTER_AREA)
      screen_image = utils.rotate_image(screen_image, -45)
      cv2.imshow('screen_image_' + str(uo_service.grpc_port), screen_image)
      cv2.waitKey(1)

      #time.sleep(1.0)
      

def step(uo_service):
  pick_up_ingot_flag = False
  ingot_serial = None

  step = 0
  while True:
    backpack_item_data = uo_service.backpack_item_dict

    if len(backpack_item_data) != 0:
      for k_backpack, v_backpack in backpack_item_data.items():
        if "Ingot" in v_backpack["name"]:
          print("{0}: {1}, {2}".format(k_backpack, v_backpack["name"], v_backpack["data"]))

      print("")
      pass

    equipped_item_dict = uo_service.equipped_item_dict
    if len(equipped_item_dict) != 0:
      for k_equip, v_equip in equipped_item_dict.items():
        #print("equipped item {0}: {1}, {2}".format(k_equip, v_equip["name"], v_equip["data"]))
        pass

      #print("")

    ## Player holded item
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state

    #print("targeting_state: ", targeting_state)

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    cliloc_dict = uo_service.cliloc_dict
    #print("cliloc_dict: ", cliloc_dict)

    pickaxe_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if pickaxe_serial in backpack_item_data:
      pickaxe_serial = backpack_item_data[pickaxe_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

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
      #print("step: ", step)
      #print("targeting_state: ", targeting_state)

      if pick_up_ingot_flag == True:
        #print("Pick up the equipped item from player")

        action['action_type'] = 3
        action['target_serial'] = unequip_item_serial

        unequip_item = uo_service.world_item_dict[unequip_item_serial]
        uo_service.picked_up_item = unequip_item

        drop_item_serial = unequip_item_serial
        unequip_item_serial = None


    action['action_type'] = 0
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

'''
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

  pickaxe_serial = None
  equip_item_flag = False
  unequip_item_serial = None
  pickaxe_item_serial = None
  onehanded_item_serial = None
  drop_item_serial = None
  picked_up_item_serial = None

  mining_prepare_flag = False
  mining_ready_flag = False

  targeting_type = None

  one_time_trial = True

  step = 0
  while True:
    backpack_item_data = uo_service.backpack_item_dict
    for k_backpack, v_backpack in backpack_item_data.items():
      #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
      pass

    equipped_item_dict = uo_service.equipped_item_dict
    #print("equipped_item_dict: ", equipped_item_dict)

    #for k_equip, v_equip in equipped_item_dict.items():
    #  print("equipped item {0}: {1}".format(k_equip, v_equip))

    ## Player holded item
    hold_item_serial = uo_service.hold_item_serial
    targeting_state = uo_service.targeting_state

    unequip_item_serial = None
    pickaxe_item_serial = None
    if "OneHanded" in equipped_item_dict:
      #print("OneHanded equip item {0}", equipped_item_dict["OneHanded"])

      if equipped_item_dict["OneHanded"]["name"] != "Pickaxe":
        unequip_item_serial = equipped_item_dict["OneHanded"]["serial"]
      elif equipped_item_dict["OneHanded"]["name"] == "Pickaxe":
        onehanded_item_serial = equipped_item_dict["OneHanded"]["serial"]
        if mining_ready_flag == False:
          mining_prepare_flag = True
    else:
      for k_backpack, v_backpack in backpack_item_data.items():
        #print("{0}: {1}".format(k_backpack, v_backpack["name"]))
        if v_backpack["name"] == "Pickaxe":
          pickaxe_item_serial = k_backpack

    player_status_dict = uo_service.player_status_dict
    #print("player_status_dict: ", player_status_dict)

    cliloc_dict = uo_service.cliloc_dict
    print("cliloc_dict: ", cliloc_dict)

    pickaxe_serial, index = utils.get_serial_by_name(backpack_item_data, 'Gold')
    #print("gold_serial: ", gold_serial)

    if pickaxe_serial in backpack_item_data:
      pickaxe_serial = backpack_item_data[pickaxe_serial]
      #print("gold_info: ", gold_info)
    else:
      #print("gold_serial is not in backpack_item_data")
      pass

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
      #print("step: ", step)
      print("targeting_state: ", targeting_state)

      if unequip_item_serial != None:
        print("Pick up the equipped item from player")

        action['action_type'] = 3
        action['target_serial'] = unequip_item_serial

        unequip_item = uo_service.world_item_dict[unequip_item_serial]
        uo_service.picked_up_item = unequip_item

        drop_item_serial = unequip_item_serial
        unequip_item_serial = None
      elif drop_item_serial != None and uo_service.backpack_serial: 
        print("Drop the holded item into backpack")

        action['action_type'] = 4
        action['target_serial'] = uo_service.backpack_serial
        drop_item_serial = None
      elif pickaxe_item_serial != None:
        print("Pick up the Pickaxe item from backpack")
        action['action_type'] = 3
        action['target_serial'] = pickaxe_item_serial
        equip_item_flag = True
      elif equip_item_flag == True:
        print("Equip the holded item")
        action['action_type'] = 6
        equip_item_flag = False
      elif mining_prepare_flag == True and one_time_trial == True:
        print("Double click the Pickaxe item")
        action['action_type'] = 2
        action['target_serial'] = onehanded_item_serial

        mining_prepare_flag = False
        mining_ready_flag = True
        one_time_trial = False
      elif mining_ready_flag == True:
        print("Mining the land target")

        # GameX: 3527, GameY: 2753, index:8
        if len(uo_service.near_land_object_dict) != 0:
          #print("len(uo_service.near_land_object_dict): ", len(uo_service.near_land_object_dict))
          for k, v in uo_service.near_land_object_dict.items():
            #print("Near land {0}: {1}".format(k, uo_service.near_land_object_dict[k]))
            if v['gameX'] == 3527 and v['gameY'] == 2753:
              print("Near land {0}: {1}".format(k, uo_service.near_land_object_dict[k]))
              action['action_type'] = 5
              action['index'] = k
              mining_ready_flag = False

      obs = uo_service.step(action)

    #obs = uo_service.step(action)
    obs = uo_service.step(utils.noop_action)

    step += 1
    #print("")


## Start the main function
if __name__ == '__main__':
  main()
'''