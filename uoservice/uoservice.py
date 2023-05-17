# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` helloworld.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. helloworld.proto --proto_path /home/kimbring2/grpc/examples/protos/

from __future__ import print_function
from concurrent import futures

import grpc
import UoService_pb2
import UoService_pb2_grpc

import io
from PIL import Image
import time
import numpy as np
import cv2
import random


grpc_port = 50051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)

selected_target_serial = None
player_serial = None

def parse_response(response):
  global selected_target_serial
  global player_serial

  #print("response: ", response)
  
  mobile_data = response.mobileList.mobile
  print("len(mobile_data): ", len(mobile_data))

  if len(mobile_data) == 0:
    return None

  #print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile_data[0].name, 
  #                                                      mobile_data[0].x, mobile_data[0].y, 
  #                                                      mobile_data[0].race,
  #                                                      mobile_data[0].serial))  

  #player_mobile = mobile_data[0]
  #player = [player_mobile.name, int(player_mobile.x), int(player_mobile.y), player_mobile.race, player_mobile.serial]
  #print('name: {0}, x: {1}, y: {2}'.format(player.name, player.x, player.y))

  screen_data = response.screenImage.image
  screen_data = io.BytesIO(screen_data).read()

  screen_image = np.ndarray(shape=(80,100,4), dtype=np.uint8, buffer=screen_data)
  screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
  dim = (1600, 1280)
  screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)

  mobile_dict = {}
  for mobile in mobile_data:
    #print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, 
    #                                                                   mobile.x, mobile.y, 
    #                                                                   mobile.race,
    #                                                                   mobile.serial))

    if mobile.race != 1:
      #enemy_list.append([mobile.name, int(mobile.x), int(mobile.y), mobile.race, mobile.serial])
      mobile_dict[mobile.serial] = [mobile.name, int(mobile.x), int(mobile.y), mobile.race]

    if mobile.x >= 1600 or mobile.y >= 1280:
      #print("mobile.x: ", mobile.x)
      #print("mobile.y: ", mobile.y)
      continue

    center_coordinates = (int(mobile.x), int(mobile.y))
    start_point = (int(mobile.x - 40), int(mobile.y - 40))
    end_point = (int(mobile.x + 40), int(mobile.y + 40))
    #screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    #screen_image = cv2.circle(screen_image, center_coordinates, 20, color, thickness)

    if mobile.race == 1:
      color = (0, 255, 0)
    elif mobile.race == 0:
      color = (0, 0, 255)
    else:
      color = (255, 0, 0)

    screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    cv2.putText(screen_image,
                text=mobile.name,
                org=center_coordinates,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=color,
                thickness=2,
                lineType=cv2.LINE_4)
  
  if (selected_target_serial not in mobile_dict) and selected_target_serial != None:
    print("(selected_target not in enemy_list) and selected_target != None")
    selected_target_serial = None

    print("len(mobile_dict): ", len(mobile_dict))

  if selected_target_serial == None and len(mobile_dict) != 0:
    print("selected_target_serial == None and len(mobile_dict) != 0")
    selected_target_serial = random.choice(list(mobile_dict.keys()))
    print("selected_target_serial: ", selected_target_serial)
    selected_target = mobile_dict[selected_target_serial]

  if selected_target_serial != None:
    #print("selected_target: ", selected_target)
    selected_target = mobile_dict[selected_target_serial]

    try:
      color = (255, 0, 0)
      start_point = (selected_target[1] - 40, selected_target[2] - 40)
      end_point = (selected_target[1] + 40, selected_target[2] + 40)
      screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    except:
      print("selected_target drawing error")
      print("selected_target: ", selected_target)

  cv2.imshow('screen_image', screen_image)
  cv2.waitKey(1)

  return mobile_dict


def main():
  for ep in range(0, 10000):
    print("ep: ", ep)

    #try:
    stub.WriteAct(UoService_pb2.Actions(action=1, 
                                        mousePoint=UoService_pb2.MousePoint(x=500, y=500),
                                        serial=123))
    #except:
    # continue
    
    # self.sem_act.post()
    stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

    # self.sem_obs.wait()
    stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

    try:
      res = stub.ReadObs(UoService_pb2.ImageRequest(name='you'))
    except:
      print("The 'try except' is finished")
      continue

    mobile_dict = parse_response(res)

    for step in range(0, 100000):
      print("step: ", step)

      print("mobile_dict: ", mobile_dict)
      print("selected_target_serial: ", selected_target_serial)

      if selected_target_serial != None and selected_target_serial in mobile_dict:
        selected_target = mobile_dict[selected_target_serial]
        target_x = selected_target[1]
        target_y = selected_target[2]
        target_serial = selected_target_serial
      elif player_serial != None:
        player = mobile_dict[player_serial]
        target_x = player[1]
        target_y = player[2]
        target_serial = player_serial
      else:
        target_x = 500
        target_y = 500
        target_serial = 1

      print("target_x: ", target_x)
      print("target_y: ", target_y)
      print("")

      stub.WriteAct(UoService_pb2.Actions(action=1, 
                                          mousePoint=UoService_pb2.MousePoint(x=target_x, y=target_y),
                                          serial=target_serial))
      
      # self.sem_act.post()
      stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

      # self.sem_obs.wait()
      stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

      try:
        res_next = stub.ReadObs(UoService_pb2.ImageRequest(name='you'))
      except:
        print("The 'try except' is finished")
        continue

      mobile_dict = parse_response(res_next)

      #time.sleep(0.5)

    cv2.destroyAllWindows()

if __name__ == '__main__':
  main()