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

import UoService_pb2
import UoService_pb2_grpc
from UoService import UoService

#replay_path = '/home/kimbring2/ClassicUO/bin/dist/Replay'
#file_name = 'kimbring2-2023-6-6-01-56-41'

parser = argparse.ArgumentParser(description='Ultima Online Replay Parser')
parser.add_argument('--game_path', type=str, help='root directory of UO execution')

arguments = parser.parse_args()

game_path = arguments.game_path
username = 'kimbring2'
password = 'kimbring2'
grpc_port = 60051
window_width = 1370
window_height = 1280
human_play = True
replay = None

def main():
  # username, password, grpc_port, window_width, window_height, replay=None, human_play=None
  uo_service = UoService(game_path, username, password, grpc_port, window_width, window_height, human_play, replay)
  uo_service._run_uo()


if __name__ == '__main__':
  main()