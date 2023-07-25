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
import threading

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoServiceGameFileParser import UoServiceGameFileParser
from uoservice import utils


class UoService:
	'''UoService class including gRPC client'''
	def __init__(self, grpc_port, window_width, window_height, uo_installed_path):
		self.grpc_port = grpc_port
		self.window_width = window_width
		self.window_height = window_height
		self.stub = None

		self.total_step = 0

		self.world_item_dict = {}
		self.world_mobile_dict = {}
		self.player_skills_dict = {}
		self.player_status_dict = {}
		self.player_buff_dict = {}

		self.backpack_item_dict = {}
		self.bank_item_dict = {}
		self.equipped_item_dict = {}
		self.corpse_dict = {}
		self.corpse_item_dict = {}
		self.cliloc_dict = {}
		self.popup_menu_list = []
		self.ground_item_dict = {}
		self.vendor_item_list = []

		self.player_hit = None
		self.player_hit_max = None
		self.player_game_x = self.player_game_y = None
		self.player_serial = None
		self.war_mode = False
		self.hold_item_serial = 0
		self.player_gold = None
		self.targeting_state = None

		self.min_tile_x = self.min_tile_y = self.max_tile_x = self.max_tile_y = None

		self.backpack_serial = None
		self.bank_serial = None
		self.picked_up_item = {}

		#self.uo_installed_path = "/home/kimbring2/.wine/drive_c/Program Files (x86)/Electronic Arts/Ultima Online Classic"
		self.uo_installed_path = uo_installed_path
		self.uoservice_game_file_parser = UoServiceGameFileParser(self.uo_installed_path)
		self.uoservice_game_file_parser.load()

		self.tile_data_list = []

	def _open_grpc(self):
		# Open the gRPC channel using the port that is same of game client 
		channel = grpc.insecure_channel('localhost:' + str(self.grpc_port))
		self.stub = UoService_pb2_grpc.UoServiceStub(channel)

	def reset(self):
		print("UoService reset()")

		self.stub.Reset(UoService_pb2.Config(init=False))

		# Reset the gRPC server before communcation with it.
		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=0, sourceSerial=0, targetSerial=0, 
													walkDirection=0, index=0, amount=0, run=False))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(init=False))

		self.parse_response(response)

	def get_distance(self, target_game_x, target_game_y):
		if self.player_game_x != None:
			return max(abs(self.player_game_x - target_game_x), abs(self.player_game_y - target_game_y))
		else:
			return -1

	def get_land_index(self, game_x, game_y):
		x_relative = 0
		for i in range(self.min_tile_x, self.max_tile_x):
			if game_x == i:
				x_relative = i - self.min_tile_x

		y_relative = 0
		for i in range(self.min_tile_y, self.max_tile_y):
			if game_y == i:
				y_relative = i - self.min_tile_y

		index = x_relative * (self.max_tile_x - self.min_tile_x) + y_relative

		return index

	def get_land_position(self, index):
		game_x = index / (self.max_tile_x - self.min_tile_x);
		game_y = index % (self.max_tile_x - self.min_tile_x);

		x = game_x + self.min_tile_x;
		y = game_y + self.min_tile_y;

		return x, y

	def parse_land_static(self):
		while True:
			if self.max_tile_x != None:
				screen_length = 1000

				screen_image = np.zeros((screen_length,screen_length,4), dtype=np.uint8)
				radius = 5
				thickness = 2
				screen_width = screen_length
				screen_height = screen_length

				cell_x_list = []
				cell_y_list = []
				tile_data_list = []

				for x in range(self.min_tile_x, self.max_tile_x):
					cell_x = x >> 3
					if cell_x not in cell_x_list:
						cell_x_list.append(cell_x)

				for y in range(self.min_tile_y, self.max_tile_y):
					cell_y = y >> 3
					if cell_y not in cell_y_list:
						cell_y_list.append(cell_y)

				player_game_x = self.player_game_x
				player_game_y = self.player_game_y

				scale = 40

				cell_zip = zip(cell_x_list, cell_y_list)
				for cell_x in cell_x_list:
					for cell_y in cell_y_list:
						land_data_list, static_data_list = self.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)

						for land_data in land_data_list:
							#print("land / name: {0}, game_x: {1}, game_y: {2}".format(land_data["name"], land_data["game_x"], land_data["game_y"]))
							start_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											(land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
							end_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
										  (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

							index = self.get_land_index(land_data["game_x"], land_data["game_y"])

							radius = 1
							font = cv2.FONT_HERSHEY_SIMPLEX
							org = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
									(land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) )
							fontScale = 0.4
							color = (255, 0, 0)
							thickness = 1
							screen_image = cv2.putText(screen_image, str(index), org, font, fontScale, color, thickness, cv2.LINE_4)

							if land_data["name"] == "forest":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Lime"], 1)
							elif land_data["name"] == "rock":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Yellow"], 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Gray"], 1)

						for static_data in static_data_list:
							#if "water" not in static_data["name"]:
							#print("static / name: {0}, game_x: {1}, game_y: {2}".format(static_data["name"], static_data["game_x"], static_data["game_y"]))
			            
							start_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
							end_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

							if "grasses" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Green"], 1)
							elif "wall" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["White"], -1)
							elif "water" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Cadetblue"], 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Lavenderblush2"], 1)

				boundary = 500

				radius = int(scale / 2)
				screen_width = 4000
				screen_height = 4000
				for k, v in self.world_mobile_dict.items():
					if self.player_game_x != None:
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											  radius, utils.color_dict["Red"], -1)

							screen_image = cv2.putText(screen_image, "  " + v["name"], 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											cv2.FONT_HERSHEY_SIMPLEX, 0.5, utils.color_dict["Red"], 1, cv2.LINE_4)

				for k, v in self.world_item_dict.items():
					if self.player_game_x != None:
						#print("world item {0}: {1}".format(k, self.world_item_dict[k]))
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2)
											),
											radius, utils.color_dict["Purple"], -1)
		           
							item_name_list = v["name"].split(" ")
							screen_image = cv2.putText(screen_image, "     " + item_name_list[-1], 
												( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
												  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
												cv2.FONT_HERSHEY_SIMPLEX, 0.5, utils.color_dict["Purple"], 1, cv2.LINE_4)

				if self.player_game_x != None:
					#print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))

					screen_image = cv2.putText(screen_image, str("player"), (int(screen_length / 2), int(screen_length / 2) - int(scale / 2)), 
											  cv2.FONT_HERSHEY_SIMPLEX, 1.0, utils.color_dict["Green"], 4, cv2.LINE_4)

					radius = int(scale / 2)
					screen_image = cv2.circle(screen_image, (int(screen_length / 2), int(screen_length / 2)), radius, utils.color_dict["Lime"], -1)
					screen_image = screen_image[int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, 
												int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, :]
		        
				screen_image = cv2.resize(screen_image, (screen_length, screen_length), interpolation=cv2.INTER_AREA)
				screen_image = utils.rotate_image(screen_image, -45)
				cv2.imshow('screen_image_' + str(self.grpc_port), screen_image)
				cv2.waitKey(1)

	def parse_response(self, response):
		# Preprocess the gRPC response format to Python friendly type
		player_object = response.playerObject

		world_item_data = response.WorldItemList.itemObjects
		world_mobile_data = response.WorldMobileList.mobileObjects

		popup_menu_data = response.popupMenuList.menus
		cliloc_data = response.clilocList.clilocs

		player_status_data = response.playerStatus
		player_skills_data = response.playerSkillList.skills
		player_buffs_data = response.playerBuffList.buffs

		vendor_data = response.vendorList.vendors

		if len(popup_menu_data):
			for popup_menu in popup_menu_data:
				#print("popup_menu / text: {0}, active: {1}".format(popup_menu.text, popup_menu.active))
				pass
			#print("")

		if len(player_buffs_data) != 0:
			#print("len(player_buffs_data): ", len(player_buffs_data))
			self.player_buff_dict = {}
			for buff in player_buffs_data:
				#print("buff: ", buff)
				self.player_buff_dict[buff.type] = {"text": buff.text, "delta": buff.delta}
				pass
			#print("")

		if player_object.gameX != 0:
			#print("gameX: {0}, gameY: {1}", player_object.gameX, player_object.gameY)
			self.player_serial = player_object.serial
			self.player_game_x = player_object.gameX
			self.player_game_y = player_object.gameY
			self.war_mode = player_object.warMode
			self.hold_item_serial = player_object.holdItemSerial
			self.targeting_state = player_object.targetingState
			self.min_tile_x = player_object.minTileX
			self.min_tile_y = player_object.minTileY
			self.max_tile_x = player_object.maxTileX
			self.max_tile_y = player_object.maxTileY

		#if player_object.holdItemSerial != 0:
		#	self.hold_item_serial = player_object.holdItemSerial

		if len(world_item_data) != 0:
			#print("len(world_item_data): ", len(world_item_data))
			pass

		if len(world_item_data) != 0:
			self.world_item_dict = {}
			self.bank_item_dict = {}
			self.bank_serial = None

			for obj in world_item_data:
				#print("name: {0}, layer: {1}".format(obj.name, obj.layer))
				self.world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, "serial": obj.serial,
													 "distance": obj.distance, "layer":obj.layer, "container": obj.container, 
													 "isCorpse": obj.isCorpse, "amount": obj.amount, "data": obj.data }
				if obj.layer == 21:
					self.backpack_serial = obj.serial

				if obj.layer == 29:
					#print("bank item distance: ", obj.distance)
					self.bank_serial = obj.serial

		#print("len(world_mobile_data): ", len(world_mobile_data))
		if len(world_mobile_data) != 0:
			self.world_mobile_dict = {}
			for obj in world_mobile_data:
				self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
													   "distance": obj.distance, "title": obj.title, "hits": obj.hits,
													   "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
													   "race": obj.race, "serial": obj.serial}

		#print("self.bank_serial: ", self.bank_serial)
		if self.bank_serial != None:
			bank_box = self.world_item_dict[self.bank_serial]

		if len(self.world_item_dict) != 0 and self.backpack_serial != None:
			self.backpack_item_dict = {}
			self.equipped_item_dict = {}
			self.corpse_dict = {}
			self.ground_item_dict = {}

			for k, v in self.world_item_dict.items():
				#print("name: {0}, layer: {1}".format(v['name'], v['layer']))

				if v["isCorpse"] == True:
					self.corpse_dict[k] = v
				elif v["container"] == self.backpack_serial:
					self.backpack_item_dict[k] = v
				elif v["container"] == self.bank_serial:
					self.bank_item_dict[k] = v
				elif v["layer"] != 0:
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
				else:
					self.ground_item_dict[k] = v

		if len(vendor_data) != 0:
			self.vendor_item_list = []
			for data in vendor_data:
				self.vendor_item_list.append({"vendor_serial": data.vendorSerial, 
											  "item_serial": data.itemSerial})

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

	def step(self, action):
		#print("action: ", action)

		# Send the action data to game client and receive the state of that action
		action_type = action['action_type']
		source_serial = action['source_serial']
		target_serial = action['target_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']
		run = action['run']

		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=action_type, 
												    sourceSerial=source_serial,
												    targetSerial=target_serial,
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