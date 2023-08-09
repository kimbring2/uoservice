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
import copy

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoServiceGameFileParser import UoServiceGameFileParser
from uoservice import utils


class UoService:
	'''UoService class including gRPC client'''
	def __init__(self, grpc_port, window_width, window_height, uo_installed_path):
		## Variable for gRPC part
		self.grpc_port = grpc_port
		self.stub = None

		## Variables for rendering the replay data
		self.window_width = window_width
		self.window_height = window_height

		## Variables to keep the replay data
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
		self.vendor_item_dict = {}
		self.popup_menu_list = []
		self.ground_item_dict = {}
		self.player_hit = None
		self.player_hit_max = None
		self.player_game_x = self.player_game_y = None
		self.player_serial = None
		self.war_mode = False
		self.hold_item_serial = 0
		self.player_gold = None
		self.player_serial = None
		self.targeting_state = None
		self.backpack_serial = None
		self.bank_serial = None
		self.picked_up_item = {}
		self.menu_gump_serial = 0
		self.menu_gump_control = {}
		self.active_gump_list = []

		## Variables to load the binary file for land, static data
		self.min_tile_x = self.min_tile_y = self.max_tile_x = self.max_tile_y = None
		self.uo_installed_path = uo_installed_path
		self.uoservice_game_file_parser = UoServiceGameFileParser(self.uo_installed_path)
		self.uoservice_game_file_parser.load()
		self.tile_data_list = []

		## Etc
		self.total_step = 0

	def _open_grpc(self):
		## Open the gRPC channel using the port that is same of game client 
		channel = grpc.insecure_channel('localhost:' + str(self.grpc_port))
		self.stub = UoService_pb2_grpc.UoServiceStub(channel)

	def reset(self):
		# Reset the gRPC server before communcation with it.

		## Send a Reset signal to C# application
		self.stub.Reset(UoService_pb2.Config(init=False))

		## Send a dummy action data to C# application
		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=0, sourceSerial=0, targetSerial=0, 
													walkDirection=0, index=0, amount=0, run=False))

		## Notify to C# application that action data is sent
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		## Notify to C# application that Python application is ready to receive the observation data
		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

		## Receive the observation data from C# application
		response = self.stub.ReadObs(UoService_pb2.Config(init=False))

		## Parse the observation gRPC data from the C# application
		self.parse_response(response)

	def get_distance(self, target_game_x, target_game_y):
		## Distance between the player and target
		if self.player_game_x != None:
			return max(abs(self.player_game_x - target_game_x), abs(self.player_game_y - target_game_y))
		else:
			return -1

	def get_land_index(self, game_x, game_y):
		## Land index of x, y position
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
		## Reverse function of the get_land_index function
		game_x = index / (self.max_tile_x - self.min_tile_x);
		game_y = index % (self.max_tile_x - self.min_tile_x);

		x = game_x + self.min_tile_x;
		y = game_y + self.min_tile_y;

		return x, y

	def parse_land_static(self):
		## Start to parse the binary file
		while True:
			## Only parsing when player is in the world
			if self.max_tile_x != None:
				## Main game screen array
				screen_length = 1000
				screen_image = np.zeros((screen_length, screen_length, 4), dtype=np.uint8)

				## Load and draw the land, static data
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

				## Check the player game position
				player_game_x = self.player_game_x
				player_game_y = self.player_game_y

				scale = 40 ## Scale factor to make the space between the box line
				radius = int(scale / 2)
				cell_zip = zip(cell_x_list, cell_y_list)
				for cell_x in cell_x_list:
					for cell_y in cell_y_list:
						## Get the land and static data of cell position
						land_data_list, static_data_list = self.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)

						for land_data in land_data_list:
							#print("land / name: {0}, game_x: {1}, game_y: {2}".format(land_data["name"], land_data["game_x"], land_data["game_y"]))

							## Box start and end position
							start_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											(land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
							end_point = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
										  (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

							## Get the unique index of land at this screen view
							index = self.get_land_index(land_data["game_x"], land_data["game_y"])

							## Middle point of land box
							org = ( (land_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
									    (land_data["game_y"] - player_game_y) * scale + int(screen_length / 2) )

							## Text for land index
							screen_image = cv2.putText(screen_image, str(index), org, cv2.FONT_HERSHEY_SIMPLEX, 0.4, utils.color_dict["Blue"], 1, cv2.LINE_4)

							## Draw the different color box for land
							if land_data["name"] == "forest":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Lime"], 1)
							elif land_data["name"] == "rock":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Yellow"], 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Gray"], 1)

						for static_data in static_data_list:
							#print("static / name: {0}, game_x: {1}, game_y: {2}".format(static_data["name"], static_data["game_x"], static_data["game_y"]))

							## Box start and end position
							start_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
							end_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

							## Draw the different color box for static object
							if "grasses" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Green"], 1)
							elif "wall" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["White"], -1)
							elif "water" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Cadetblue"], 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, utils.color_dict["Lavenderblush2"], 1)

				## Rendering the replay data as real screen scale 
				screen_width = 4000
				screen_height = 4000
				world_mobile_dict = copy.deepcopy(self.world_mobile_dict)
				for k, v in world_mobile_dict.items():
					if self.player_game_x != None and v["isDead"] == False and k != self.player_serial:
						#print("world mobile {0}: {1}".format(k, v["isDead"]))
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											  radius, utils.color_dict["Red"], -1)

							screen_image = cv2.putText(screen_image, "  " + v["name"], 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											cv2.FONT_HERSHEY_SIMPLEX, 0.5, utils.color_dict["Red"], 1, cv2.LINE_4)

				world_item_dict = copy.deepcopy(self.world_item_dict)
				for k, v in world_item_dict.items():
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

				## Cropping the real screen around player position to zoom in
				boundary = 500
				if self.player_game_x != None:
					#print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))
					screen_image = cv2.putText(screen_image, str("player"), (int(screen_length / 2), int(screen_length / 2) - int(scale / 2)), 
											  cv2.FONT_HERSHEY_SIMPLEX, 1.0, utils.color_dict["Green"], 4, cv2.LINE_4)

					radius = int(scale / 2)
					screen_image = cv2.circle(screen_image, (int(screen_length / 2), int(screen_length / 2)), radius, utils.color_dict["Lime"], -1)
					screen_image = screen_image[int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, 
												int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, :]
		        
		        ## Resize the cropped screen larger
				screen_image = cv2.resize(screen_image, (screen_length, screen_length), interpolation=cv2.INTER_AREA)

				## Rotate image to show like a real game angle
				screen_image = utils.rotate_image(screen_image, -45)

				cv2.imshow('screen_image_' + str(self.grpc_port), screen_image)

				## Draw action related gump
				for k_gump, v_gump in self.menu_gump_control.items():
					gump_width = 500
					gump_height = 1000
					gump_image = np.zeros((gump_width, gump_height, 4), dtype=np.uint8)
					print("k_gump: ", k_gump)
					for i, control in enumerate(v_gump):
						#print("control: ", control)
						if control.name == "xmfhtmlgumpcolor" or control.name == "xmfhtmlgump":
							gump_image = cv2.putText(gump_image, control.text, (control.x, control.y), 
								cv2.FONT_HERSHEY_SIMPLEX, 1.0, utils.color_dict["White"], 1, cv2.LINE_4)
						elif control.name == "button":
							start_point = (control.x, control.y)
							end_point = (control.x + 10, control.y + 10)
							gump_image = cv2.rectangle(gump_image, start_point, end_point, utils.color_dict["Green"], 1)

					print("")
					cv2.imshow('gump_image_' + str(k_gump), gump_image)

				cv2.waitKey(1)

	def parse_response(self, response):
		## Load the each gRPC message from response data 
		player_object = response.playerObject
		world_item_data = response.WorldItemList.itemObjects
		world_mobile_data = response.WorldMobileList.mobileObjects
		popup_menu_data = response.popupMenuList.menus
		cliloc_data = response.clilocList.clilocs
		vendor_data = response.vendorList.vendors
		player_status_data = response.playerStatus
		player_skills_data = response.playerSkillList.skills
		player_buffs_data = response.playerBuffList.buffs
		delete_item_serial_list = response.deleteItemSerialList.serials
		delete_mobile_serial_list = response.deleteMobileSerialList.serials
		menu_gump_serial = response.menuControlList.localSerial
		menu_gump_control_list = response.menuControlList.menuControls

		## Save the player buff data into global variable
		if len(player_buffs_data) != 0:
			self.player_buff_dict = {}
			for buff in player_buffs_data:
				self.player_buff_dict[buff.type] = {"text": buff.text, "delta": buff.delta}

		## Save the player object data into global variable
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
			self.active_gump_list = player_object.activeGumps

		#print("self.active_gump_list: ", self.active_gump_list)

		## Save the hold item data into global variable
		if player_object.holdItemSerial != 0:
			self.hold_item_serial = player_object.holdItemSerial

		## Save the world item object into global Dict	
		if len(world_item_data) != 0:
			self.bank_item_dict = {}
			self.bank_serial = None

			for obj in world_item_data:
				#print("name: {0}, layer: {1}".format(obj.name, obj.layer))
				self.world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, "serial": obj.serial,
													 "distance": obj.distance, "layer":obj.layer, "container": obj.container, 
													 "isCorpse": obj.isCorpse, "amount": obj.amount, "data": obj.data }
				## Check the serial number of backpack container
				if obj.layer == 21:
					self.backpack_serial = obj.serial

				## Check the serial number of bank container
				if obj.layer == 29:
					self.bank_serial = obj.serial

			#print("")


		## Save the world mobile object into global Dict
		if len(world_mobile_data) != 0:
			for obj in world_mobile_data:
				#print("serial: {0}, name: {1}, gameX: {2}, gameY: {3}".format(obj.serial, obj.name, obj.gameX, obj.gameY))
				self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY": obj.gameY, 
													   "distance": obj.distance, "title": obj.title, "hits": obj.hits,
													   "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
													   "race": obj.race, "serial": obj.serial, "isDead": obj.isDead}

		if self.bank_serial != None:
			bank_box = self.world_item_dict[self.bank_serial]

		## Parse the backpack, equipped, corpse item from world item
		if len(self.world_item_dict) != 0 and self.backpack_serial != None:
			self.backpack_item_dict = {}
			self.equipped_item_dict = {}
			self.corpse_dict = {}
			self.ground_item_dict = {}

			for k, v in self.world_item_dict.items():
				#print("world item / name: {0}, layer: {1}".format(v["name"], v["layer"]))

				if v["isCorpse"] == True:
					## Corpse item
					self.corpse_dict[k] = v
				elif v["container"] == self.backpack_serial:
					## Backpack item
					self.backpack_item_dict[k] = v
				elif v["container"] == self.bank_serial:
					## Bank item
					self.bank_item_dict[k] = v
				elif v["layer"] != 0:
					## Equipped item
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
					## Item on ground
					self.ground_item_dict[k] = v

		## Parse and save the vendor data 
		if len(vendor_data) != 0:
			self.vendor_item_dict = {}
			for obj in vendor_data:
				self.vendor_item_dict[obj.itemSerial] = { "vendor_serial": obj.vendorSerial, "item_serial": obj.itemSerial, 
													      "item_graphic": obj.itemGraphic, "item_hue": obj.itemHue,
													      "item_amount": obj.itemAmount, "item_price":obj.itemPrice, 
													      "item_name": obj.itemName}

		## Parse and save the player status data 
		if player_status_data.str != 0:
			self.player_status_dict = utils.parsePlayerStatus(player_status_data)

		## Parse and save the player skill data
		for skill in player_skills_data:
			self.player_skills_dict[skill.name] = {"index": skill.index, "isClickable": skill.isClickable, "value": skill.value, 
												   "base: ": skill.base, "cap": skill.cap, "lock": skill.lock}

		## Parse and save the clilo data 
		for data in cliloc_data:
			if data.serial not in self.cliloc_dict:
				self.cliloc_dict[data.serial] = [{"text": data.text, "affix": data.affix, "name": data.name}]
			else:
				self.cliloc_dict[data.serial].append({"text": data.text, "affix": data.affix, "name": data.name})

		## Parse and save the popup menu data
		for menu_data in popup_menu_data:
			self.popup_menu_list.append(menu_data)

		if len(menu_gump_control_list) != 0:
			#print("menu_gump_serial: ", menu_gump_serial)
			self.menu_gump_control[menu_gump_serial] = []
			#print("len(menu_gump_control_list): ", len(menu_gump_control_list))
			for menu_gump_control in menu_gump_control_list:
				# print("menu_gump_control: ", menu_gump_control)
				self.menu_gump_control[menu_gump_serial].append(menu_gump_control)
			#print("")

		delete_gump_serial = []
		for serial in self.menu_gump_control:
			if serial not in self.active_gump_list:
				#del self.menu_gump_control[serial]
				delete_gump_serial.append(serial)

		for serial in delete_gump_serial:
			del self.menu_gump_control[serial]

		## Delete the item from world item Dict using the gRPC data
		if len(delete_item_serial_list) != 0:
			for serial in delete_item_serial_list:
				if serial in self.world_item_dict:
					del self.world_item_dict[serial]

		## Delete the mobile from world mobile Dict using the gRPC data
		if len(delete_mobile_serial_list) != 0:
			#print("delete_mobile_serial_list: ", delete_mobile_serial_list)
			for serial in delete_mobile_serial_list:
				if serial in self.world_mobile_dict:
					del self.world_mobile_dict[serial]

	def step(self, action):
		# Send the action data to game client and receive the state of that action
		## Parse the action Dict
		action_type = action['action_type']
		source_serial = action['source_serial']
		target_serial = action['target_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']
		run = action['run']

		## Send a action data to C# application
		self.stub.WriteAct(UoService_pb2.GrpcAction(actionType=action_type, 
												    sourceSerial=source_serial,
												    targetSerial=target_serial,
												    walkDirection=walk_direction,
												    index=index, 
												    amount=amount,
												    run=run))

		## Notify to C# application that action data is sent
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		## Notify to C# application that Python application is ready to receive the observation data
		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

		## Hard reset at the first time of eposide
		if self.total_step == 100:
			## Receive the observation data from C# application
			response = self.stub.ReadObs(UoService_pb2.Config(init=True))
		else:
			response = self.stub.ReadObs(UoService_pb2.Config(init=False))

		## Parse the observation gRPC data from the C# application
		self.parse_response(response)

		## Increase the eposide step
		self.total_step += 1