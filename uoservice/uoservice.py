# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` helloworld.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. helloworld.proto --proto_path /home/kimbring2/grpc/examples/protos/

from __future__ import print_function
from concurrent import futures

import grpc

#import test_pb2
#import test_pb2_grpc

import UoService_pb2
import UoService_pb2_grpc

import io

from PIL import Image
import time
import numpy as np
import cv2


def run():
  channel = grpc.insecure_channel('localhost:50052')
  stub = UoService_pb2_grpc.UoServiceStub(channel)

  for i in range(0, 10000):
    print("i: ", i)

    response = stub.Step(UoService_pb2.ImageRequest(name='you'))
    image_data = response.data
    image_data = io.BytesIO(image_data).read()
    image = Image.frombuffer("RGBA", (960,760), image_data, "raw", "BGRA", 0, 1)
    obs = np.ndarray(shape=(760,960,4), dtype=np.uint8, buffer=image_data)
    obs = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)

    cv2.imshow('obs', obs)
    cv2.waitKey(1)

if __name__ == '__main__':
  run()
