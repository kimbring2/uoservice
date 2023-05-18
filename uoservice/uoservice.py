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

  mobile_data = response.mobileList.mobile
  if len(mobile_data) == 0:
    return None

  item_data = response.itemList.item
  print("item_data: ", item_data)
  if len(item_data) == 0:
    return None

  #screen_data = response.screenImage.image
  #screen_data = io.BytesIO(screen_data).read()

  #screen_image = np.ndarray(shape=(80,100,4), dtype=np.uint8, buffer=screen_data)
  #screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
  #dim = (1600, 1280)
  #screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)

  mobile_dict = {}
  for mobile in mobile_data:
    #print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, 
    #                                                                   mobile.x, mobile.y, 
    #                                                                   mobile.race,
    #                                                                   mobile.serial))

    if mobile.race != 1:
      mobile_dict[mobile.serial] = [mobile.name, int(mobile.x), int(mobile.y), mobile.race]

    if mobile.x >= 1600 or mobile.y >= 1280:
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
    '''
    screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    cv2.putText(screen_image,
                text=mobile.name,
                org=center_coordinates,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=color,
                thickness=2,
                lineType=cv2.LINE_4)
    '''

  item_dict = {}
  for item in item_data:
    '''
    message GrpcItemData {
      string name = 1;
      uint32 layer = 2;
      uint32 serial = 3;
      uint32 amount = 4;
    }
    '''

    print('name: {0}, layer: {1}, serial: {2}, amount: {3}\n'.format(item.name, item.layer, 
                                                                     item.serial, item.amount))
    
  if (selected_target_serial not in mobile_dict) and selected_target_serial != None:
    selected_target_serial = None

  if selected_target_serial == None and len(mobile_dict) != 0:
    selected_target_serial = random.choice(list(mobile_dict.keys()))
    selected_target = mobile_dict[selected_target_serial]

  if selected_target_serial != None:
    selected_target = mobile_dict[selected_target_serial]

    color = (255, 0, 0)
    start_point = (selected_target[1] - 40, selected_target[2] - 40)
    end_point = (selected_target[1] + 40, selected_target[2] + 40)
    #screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)

  #cv2.imshow('screen_image', screen_image)
  #cv2.waitKey(1)

  return mobile_dict


def main():
  for ep in range(0, 10000):
    print("ep: ", ep)

    stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                        mobileSerial=1,
                                        walkDirection=UoService_pb2.WalkDirection(direction=1)))
    
    stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
    stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

    res = stub.ReadObs(UoService_pb2.Config(name='you'))

    mobile_dict = parse_response(res)

    for step in range(0, 100000):
      print("step: ", step)

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

      stub.WriteAct(UoService_pb2.Actions(actionType=0, 
                                          mobileSerial=target_serial,
                                          walkDirection=UoService_pb2.WalkDirection(direction=2)))
      
      stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

      stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

      res_next = stub.ReadObs(UoService_pb2.Config(name='you'))

      mobile_dict = parse_response(res_next)

      #time.sleep(0.5)

    cv2.destroyAllWindows()

if __name__ == '__main__':
  main()