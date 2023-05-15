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


channel = grpc.insecure_channel('localhost:50052')
stub = UoService_pb2_grpc.UoServiceStub(channel)


def parse_response(response):
  screen_data = response.data
  screen_data = io.BytesIO(screen_data).read()
  #screen_image = Image.frombuffer("RGBA", (960,760), screen_data, "raw", "BGRA", 0, 1)

  screen_image = np.ndarray(shape=(760,960,4), dtype=np.uint8, buffer=screen_data)
  screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)

  cv2.imshow('screen_image', screen_image)
  cv2.waitKey(1)
  #cv2.destroyAllWindows()

  return screen_image


def main():
  for ep in range(0, 10000):
    print("ep: ", ep)
    res = stub.reset(UoService_pb2.ImageRequest(name='you'))
    obs = parse_response(res)

    for step in range(0, 100000):
      res_next = stub.step(UoService_pb2.ImageRequest(name='you'))
      obs_next = parse_response(res_next)

      stub.act(UoService_pb2.Actions(action=1))

    cv2.destroyAllWindows()

if __name__ == '__main__':
  main()