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


grpc_port = 50052
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)

def parse_response(response):
  #print("response: ", response)
  
  mobile_data = response.mobileList.mobile
  #print("mobile_data: ", mobile_data)

  if len(mobile_data) == 0:
    return None

  player = mobile_data[0]
  #print('name: {0}, x: {1}, y: {2}'.format(player.name, player.x, player.y))

  screen_data = response.screenImage.image
  screen_data = io.BytesIO(screen_data).read()

  screen_image = np.ndarray(shape=(80,100,4), dtype=np.uint8, buffer=screen_data)
  screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
  dim = (1600, 1280)
  screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)

  for mobile in mobile_data:
    print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, 
                                                          mobile.x, mobile.y, 
                                                          mobile.race,
                                                          mobile.serial))

    if mobile.x >= 1600 or mobile.y >= 1280:
      continue

    center_coordinates = (mobile.x, mobile.y)
    start_point = (mobile.x - 40, mobile.y - 40)
    end_point = (mobile.x + 40, mobile.y + 40)
    #screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    #screen_image = cv2.circle(screen_image, center_coordinates, 20, color, thickness)

    if mobile.race == 1:
      color = (0, 255, 0)
    elif mobile.race == 0:
      color = (0, 0, 255)
    else:
      color = (0, 255, 0)

    screen_image = cv2.rectangle(screen_image, start_point, end_point, color, 2)
    cv2.putText(screen_image,
                text=mobile.name,
                org=center_coordinates,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=color,
                thickness=2,
                lineType=cv2.LINE_4)

  cv2.imshow('screen_image', screen_image)
  cv2.waitKey(1)
  #cv2.destroyAllWindows()
  
  screen_image = None

  return screen_image


def main():
  for ep in range(0, 10000):
    print("ep: ", ep)

    stub.WriteAct(UoService_pb2.Actions(action=1, mousePoint=UoService_pb2.MousePoint(x=500, y=500)))
    
    # self.sem_act.post()
    stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

    # self.sem_obs.wait()
    stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

    res = stub.ReadObs(UoService_pb2.ImageRequest(name='you'))

    obs = parse_response(res)

    for step in range(0, 100000):
      print("step: ", step)

      stub.WriteAct(UoService_pb2.Actions(action=1, mousePoint=UoService_pb2.MousePoint(x=500, y=500)))
      
      # self.sem_act.post()
      stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

      # self.sem_obs.wait()
      stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

      try:
        res_next = stub.ReadObs(UoService_pb2.ImageRequest(name='you'))
      except:
        print("The 'try except' is finished")
        continue

      obs_next = parse_response(res_next)

      #time.sleep(0.5)

    cv2.destroyAllWindows()

if __name__ == '__main__':
  main()