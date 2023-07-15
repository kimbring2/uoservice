# protoc --csharp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` UoService.proto
# python3.7 -m grpc_tools.protoc -I ../ --python_out=. --grpc_python_out=. UoService.proto --proto_path /home/kimbring2/uoservice/uoservice/protos/

from __future__ import print_function
from concurrent import futures
import io
from PIL import Image
import time
import numpy as np
import cv2
import random
import pygame
import argparse
import sys
import grpc
from enum import Enum

from uoservice.protos  import UoService_pb2
from uoservice.protos  import UoService_pb2_grpc
from uoservice.UoServiceReplay import UoServiceReplay

#replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
#file_name = 'kimbring2-2023-6-6-01-56-41'

parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--replay_path', type=str, help='root directory of replay')
parser.add_argument('--file_name', type=str, help='replay file name')
parser.add_argument('--screen_width', type=int, default=1370, help='screen width of game')
parser.add_argument('--screen_height', type=int, default=1280, help='screen height of game')

arguments = parser.parse_args()

replay_path = arguments.replay_path
file_name = arguments.file_name
screen_width = arguments.screen_width
screen_height = arguments.screen_height

print("screen_width: ", screen_width)
print("screen_height: ", screen_height)

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")


def parse_item(item_grpc):
  item_dict = {}

  for item in item_grpc :
    item_dict[item.serial] = [item.name, item.amount]

  return item_dict


def main():
  #replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
  #file_name = 'kimbring2-2023-6-6-01-56-41'

  uo_service_replay = UoServiceReplay(replay_path, screen_width, screen_height)
  uo_service_replay.ReadReplay(file_name)
  uo_service_replay.ParseReplay()

  uo_service_replay.InteractWithReplay()


if __name__ == '__main__':
  main()