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


grpc_port = 50051
channel = grpc.insecure_channel('localhost:' + str(grpc_port))
stub = UoService_pb2_grpc.UoServiceStub(channel)


def parse_response(response):
  #print("response: ", response)
  '''
  screen_data = response.data
  screen_data = io.BytesIO(screen_data).read()

  screen_image = np.ndarray(shape=(80,100,4), dtype=np.uint8, buffer=screen_data)
  screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
  dim = (1600, 1280)
  screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)

  cv2.imshow('screen_image', screen_image)
  cv2.waitKey(1)
  #cv2.destroyAllWindows()
  '''
  screen_image = None

  return screen_image


def main():
  for ep in range(0, 10000):
    print("ep: ", ep)
    res = stub.reset(UoService_pb2.ImageRequest(name='you'))
    obs = parse_response(res)

    for step in range(0, 100000):
      print("step: ", step)

      res_next = stub.step(UoService_pb2.ImageRequest(name='you'))
      obs_next = parse_response(res_next)

      stub.act(UoService_pb2.Actions(action=1))

      time.sleep(1)

    cv2.destroyAllWindows()

if __name__ == '__main__':
  main()