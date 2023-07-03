# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Communicating with Ultima Online game client through GRPC
#
# Please reference me when you are going to use this code as reference :)

## general package imports
import numpy as np
import math
import grpc
import subprocess
import time
import numpy as np
import cv2
import random

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice import utils


class UoService:
	'''UoService class including gRPC client'''
	def __init__(self, grpc_port, window_width, window_height):
		self.grpc_port = grpc_port
		self.window_width = window_width
		self.window_height = window_height
		self.stub = None

		self.total_step = 0

		self.world_item_dict = {}
		self.world_mobile_dict = {}
		self.player_skills_dict = {}
		self.player_status_dict = {}

		self.backpack_item_dict = {}
		self.equipped_item_dict = {}
		self.corpse_dict = {}
		self.corpse_item_dict = {}
		self.cliloc_dict = {}
		self.popup_menu_list = []

		self.player_game_x = None
		self.player_game_y = None
		self.war_mode = False
		self.hold_item_serial = None
		self.player_gold = None

		self.backpack_serial = None

		self.static_object_game_x_data = None
		self.static_object_game_y_data = None

		self.rock_object_game_x_data = None
		self.rock_object_game_y_data = None

		self.static_object_list = []

	def _open_grpc(self):
		# Open the gRPC channel using the port that is same of game client 
		channel = grpc.insecure_channel('localhost:' + str(self.grpc_port))
		self.stub = UoService_pb2_grpc.UoServiceStub(channel)

	def reset(self):
		print("UoService reset()")

		self.stub.Reset(UoService_pb2.Config(init=False))

		# Reset the gRPC server before communcation with it.
		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=0, mobileSerial=0, walkDirection=0, index=0, amount=0))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(init=False))

		self.parse_response(response)

	def parse_response(self, response):
		# Preprocess the gRPC response format to Python friendly type
		player_object = response.playerObject

		world_item_data = response.WorldItemList.itemObjects
		world_mobile_data = response.WorldMobileList.mobileObjects

		popup_menu_data = response.popupMenuList.menus
		cliloc_data = response.clilocDataList.clilocDatas

		player_status_data = response.playerStatus
		player_skills_data = response.playerSkillList.skills

		static_object_game_x_data = response.staticObjectInfoList.gameXs
		static_object_game_y_data = response.staticObjectInfoList.gameYs

		rock_object_game_x_data = response.landRockObjectInfoList.gameXs
		rock_object_game_y_data = response.landRockObjectInfoList.gameYs

		if len(popup_menu_data):
			for popup_menu in popup_menu_data:
				#print("popup_menu / text: {0}, active: {1}".format(popup_menu.text, popup_menu.active))
				pass
			#print("")

		if player_object.gameX != 0:
			#print("player_object: ", player_object)
			self.player_game_x = player_object.gameX
			self.player_game_y = player_object.gameY

		self.war_mode = player_object.warMode
		self.hold_item_serial = player_object.holdItemSerial

		#print("len(world_item_data): ", len(world_item_data))
		if len(world_item_data) != 0:
			self.world_item_dict = {}
			for obj in world_item_data:
				#print("obj.name: ", obj.name)
				self.world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, "serial": obj.serial,
																						 "distance": obj.distance, "layer":obj.layer, "container": obj.container, 
																						 "isCorpse": obj.isCorpse, "amount": obj.amount }
				if obj.layer == 21:
					self.backpack_serial = obj.serial

				#print("")

		#print("len(world_mobile_data): ", len(world_mobile_data))
		if len(world_mobile_data) != 0:
			self.world_mobile_dict = {}
			for obj in world_mobile_data:
				self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
																							 "distance": obj.distance, "title": obj.title, "hits": obj.hits,
																							 "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
																							 "race": obj.race}


		if len(static_object_game_x_data) != 0:
			self.static_object_game_x_data = static_object_game_x_data
			self.static_object_game_y_data = static_object_game_y_data

		if len(rock_object_game_x_data) != 0:
			self.rock_object_game_x_data = rock_object_game_x_data
			self.rock_object_game_y_data = rock_object_game_y_data

		if len(self.world_item_dict) != 0 and self.backpack_serial != None:
			self.backpack_item_dict = {}
			self.equipped_item_dict = {}
			self.corpse_dict = {}
			for k, v in self.world_item_dict.items():
				#print("world item {0}: {1}".format(k, self.world_item_dict[k]))

				if v["isCorpse"] == True:
					self.corpse_dict[k] = v

				if v["container"] == self.backpack_serial:
					if 'Gold' in v["name"]:
						#print("world item {0}: {1}".format(k, self.world_item_dict[k]))
						pass

					self.backpack_item_dict[k] = v

				if v["layer"] == 1:
					self.equipped_item_dict['OneHanded'] = v
				elif v["layer"] == 2:
					self.equipped_item_dict['TwoHanded'] = v
				elif v["layer"] == 3:
					self.equipped_item_dict['Shoes'] = v
				elif v["layer"] == 4:
					self.equipped_item_dict['Pants'] = v
				elif v["layer"] == 5:
					self.equipped_item_dict['Shirt'] = v
				elif v["layer"] == 6:
					self.equipped_item_dict['Helmet'] = v
				elif v["layer"] == 7:
					self.equipped_item_dict['Gloves'] = v
				elif v["layer"] == 8:
					self.equipped_item_dict['Ring'] = v
				elif v["layer"] == 9:
					self.equipped_item_dict['Talisman'] = v
				elif v["layer"] == 10:
					self.equipped_item_dict['Necklace'] = v
				elif v["layer"] == 11:
					self.equipped_item_dict['Hair'] = v
				elif v["layer"] == 12:
					self.equipped_item_dict['Waist'] = v
				elif v["layer"] == 13:
					self.equipped_item_dict['Torso'] = v
				elif v["layer"] == 14:
					self.equipped_item_dict['Bracelet'] = v
				elif v["layer"] == 15:
					self.equipped_item_dict['Face'] = v
				elif v["layer"] == 16:
					self.equipped_item_dict['Beard'] = v
				elif v["layer"] == 17:
					self.equipped_item_dict['Tunic'] = v
				elif v["layer"] == 18:
					self.equipped_item_dict['Earrings'] = v
				elif v["layer"] == 19:
					self.equipped_item_dict['Arms'] = v
				elif v["layer"] == 20:
					self.equipped_item_dict['Cloak'] = v
				elif v["layer"] == 22:
					self.equipped_item_dict['Robe'] = v
				elif v["layer"] == 23:
					self.equipped_item_dict['Skirt'] = v
				elif v["layer"] == 24:
					self.equipped_item_dict['Legs'] = v

		#print("self.corpse_dict: ", self.corpse_dict)
		#print("self.equipped_item_dict: ", self.equipped_item_dict)
		#print("")

		self.corpse_item_dict = {}
		for k_corpse, v_corpse in self.corpse_dict.items():
			for k_world, v_world in self.world_item_dict.items():
				if k_corpse == v_world["container"]:
					#print("corpse item {0}: {1}".format(k, self.world_item_dict[k_world]))

					if k_corpse not in self.corpse_item_dict:
						self.corpse_item_dict[k_corpse] = {}
						self.corpse_item_dict[k_corpse][k_world] = self.world_item_dict[k_world]
					else:
						self.corpse_item_dict[k_corpse][k_world] = self.world_item_dict[k_world]

					pass

		if self.backpack_item_dict != 0:
			#print("self.backpack_item_dict: ", self.backpack_item_dict)
			for k, v in self.backpack_item_dict.items():
				#print("backpack item {0}: {1}".format(k, self.backpack_item_dict[k]))
				pass
			#print("")

		if player_status_data.str != 0:
			#print("player_status_data.str: ", player_status_data.str)
			self.player_status_dict = utils.parsePlayerStatus(player_status_data)

		for skill in player_skills_data:
			self.player_skills_dict[skill.name] = {"index": skill.index, "isClickable": skill.isClickable, "value": skill.value, 
														   							 "base: ": skill.base, "cap": skill.cap, "lock": skill.lock}

		for data in cliloc_data:
			#print("data: ", data)
			if data.serial not in self.cliloc_dict:
				self.cliloc_dict[data.serial] = [{"text": data.text, "affix": data.affix, "name": data.name}]
			else:
				self.cliloc_dict[data.serial].append({"text": data.text, "affix": data.affix, "name": data.name})

		player_status_dict = utils.parsePlayerStatus(player_status_data)

		for menu_data in popup_menu_data:
			self.popup_menu_list.append(menu_data)

		screen_image = np.zeros((5000,5000,4), dtype=np.uint8)

		radius = 5
		thickness = 2
		screen_width = 5000
		screen_height = 5000
		for k, v in self.world_mobile_dict.items():
			if self.player_game_x != None:
				if v["gameX"] < screen_width and v["gameY"] < screen_height:
						screen_image = cv2.circle(screen_image, (v["gameX"], v["gameY"]), radius, (0, 0, 255), thickness)

		if self.static_object_game_x_data != None:
			#print("len(self.static_object_game_x_data): ", len(self.static_object_game_x_data))
			for i in range(0, len(self.static_object_game_x_data)):
					#if self.static_object_game_x_data[i] >= 1400 or self.static_object_game_y_data[i] >= 1280:
					#	continue
					#print("self.static_object_game_x_data[{0}]: {1}".format(i, self.static_object_game_x_data[i]))
					#print("self.static_object_game_y_data[{0}]: {1}".format(i, self.static_object_game_y_data[i]))
					screen_image = cv2.circle(screen_image, (self.static_object_game_x_data[i], self.static_object_game_y_data[i]), 
									   				 		    1, (120, 120, 120), 1)

		if self.rock_object_game_x_data != None:
			#print("len(self.rock_object_game_x_data): ", len(self.rock_object_game_x_data))
			for i in range(0, len(self.rock_object_game_x_data)):
					#if self.static_object_game_x_data[i] >= 1400 or self.static_object_game_y_data[i] >= 1280:
					#	continue
					#print("self.static_object_game_x_data[{0}]: {1}".format(i, self.static_object_game_x_data[i]))
					#print("self.static_object_game_y_data[{0}]: {1}".format(i, self.static_object_game_y_data[i]))
					screen_image = cv2.circle(screen_image, (self.rock_object_game_x_data[i], self.rock_object_game_y_data[i]), 
									   				 		    1, (0, 0, 255), 1)
		#print("")

		if self.player_game_x != None:
			#print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))

			radius = 5
			screen_image = cv2.circle(screen_image, (self.player_game_x, self.player_game_y), radius, (0, 255, 0), thickness)
			if self.player_game_y > 600 and self.player_game_x > 600:
				screen_image = screen_image[self.player_game_y - 600:self.player_game_y + 600, 
																	  self.player_game_x - 600:self.player_game_x + 600, :]
			elif self.player_game_y < 600 and self.player_game_x > 600:
				#print("self.player_game_y < 600 and self.player_game_x > 600")
				screen_image = screen_image[0:self.player_game_y + 600, 
																		self.player_game_x - 600:self.player_game_x + 600, :]
			elif self.player_game_y > 600 and self.player_game_x < 600:
				#print("self.player_game_y > 600 and self.player_game_x < 600")
				screen_image = screen_image[self.player_game_y - 600:self.player_game_y + 600, 
																		0:self.player_game_x + 600, :]
			else:
				#print("else")
				screen_image = screen_image[0:self.player_game_y + 600, 
																		0:self.player_game_x + 600, :]

		vis = True
		if vis:
			#dim = (1720, 1370)

			try:
				screen_image = cv2.resize(screen_image, (1200, 1200), interpolation=cv2.INTER_AREA)
				screen_image = utils.rotate_image(screen_image, -45)
				#screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
				#screen_image = cv2.flip(screen_image, 1)
				cv2.imshow('screen_image_' + str(self.grpc_port), screen_image)
				cv2.waitKey(1)
			except Exception as e:
				print("e: ", e)
				print("screen_image.shape: \n", screen_image.shape)

		self.static_object_game_x_list = []
		self.static_object_game_y_list = []
		for i in range(0, len(static_object_game_x_data)):
			self.static_object_game_x_list.append(static_object_game_x_data[i])
			self.static_object_game_y_list.append(static_object_game_y_data[i])

	def step(self, action):
		# Send the action data to game client and receive the state of that action
		action_type = action['action_type']
		item_serial = action['item_serial']
		mobile_serial = action['mobile_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']
		run = action['run']

		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=action_type, 
																						    itemSerial=item_serial,
																						    mobileSerial=mobile_serial,
																						    walkDirection=walk_direction,
																						    index=index, 
																						    amount=amount,
																						    run=run))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

		if self.total_step == 100:
			response = self.stub.ReadObs(UoService_pb2.Config(init=True))
		else:
			response = self.stub.ReadObs(UoService_pb2.Config(init=False))

		self.parse_response(response)

		self.total_step += 1