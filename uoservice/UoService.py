import numpy as np
import grpc
import subprocess

import UoService_pb2
import UoService_pb2_grpc


class UoService:
	def __init__(self, game_path, username, password, grpc_port, window_width, window_height, human_play=None, replay=None):
			self.game_path = game_path
			self.grpc_port = grpc_port
			self.username = username
			self.password = password
			self.human_play = human_play
			self.window_width = window_width
			self.window_height = window_height
			self.replay = replay

	def _run_uo(self):
			#argument = '-username kimbring2 -password kimbring2 -grpc_port 60051 -human_play -window_width 1370 -window_height 1280'.split()

			argument = ''
			argument += ' '
			argument += '-username ' + self.username + ' '
			argument += '-password ' + self.password + ' '
			argument += '-grpc_port ' + str(self.grpc_port) + ' '

			if self.human_play:
				argument += '-human_play ' + ' '

			argument += '-window_width ' + str(self.window_width) + ' '
			argument += '-window_height ' + str(self.window_height) + ' '

			if self.replay:
				argument += '-replay '

			print("argument: ", argument)

			subprocess.call([str(self.game_path)] + argument.split(), shell=False)