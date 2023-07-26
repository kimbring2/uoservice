# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Parsing the MPQ replay file of human player
#
# Please reference me when you are going to use this code as reference :)

## general package imports
import struct
import numpy as np
import grpc
import io
from PIL import Image
import time
import numpy as np
import cv2
import random
import pygame
import sys
from enum import Enum

## package for replay
from mpyq import MPQArchive

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice.UoServiceGameFileParser import UoServiceGameFileParser
from uoservice import utils


## Initialize the PyGame
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")


## layers of Equipped item
class Layers(Enum):
  Invalid = 0
  OneHanded = 1
  TwoHanded = 2
  Shoes = 3
  Pants = 4
  Shirt = 5
  Helmet = 6
  Gloves = 7
  Ring = 8
  Talisman = 9
  Necklace = 10
  Hair = 11
  Waist = 12
  Torso = 13
  Bracelet = 14
  Face = 15
  Beard = 16
  Tunic = 17
  Earrings = 18
  Arms = 19
  Cloak = 20
  Backpack = 21
  Robe = 22
  Skirt = 23
  Legs = 24
  Mount = 25
  ShopBuyRestock = 26
  ShopBuy = 27
  ShopSell = 28
  Bank = 29


class UoServiceReplay:
	'''UoServiceReplay class including MPQ loader'''
	def __init__(self, rootPath, screenWidth, screenHeight, uo_installed_path):
		self._rootPath = rootPath
		self._archive = None

		## Initialize the length related variable
		self._replayLength = 0
		self._tickScale = 10
		self._previousControl = 0

		## Initialize the offset for the start position of byte array read
		self._playerObjectArrayOffset = 0
		self._worldItemArrayOffset = 0
		self._worldMobileArrayOffset = 0
		self._popupMenuArrayOffset = 0
		self._clilocArrayOffset = 0
		self._vendorListArrayOffset = 0
		self._playerStatusArrayOffset = 0
		self._playerSkillListArrayOffset = 0
		self._playerBuffListArrayOffset = 0
		self._actionArrayOffset = 0

		## Initialize the list to save the replay state data
		self._playerObjectList = []
		self._worldItemList = []
		self._worldMobileList = []
		self._popupMenuList = []
		self._clilocList = []
		self._vendorListList = []
		self._playerStatusList = []
		self._playerSkillListList = []
		self._playerBuffListList = []
		self._actionList = []

		## Initialize the witdh, height of replay file
		self._screenWidth = screenWidth
		self._screenHeight = screenHeight

		## PyGame related variables
		self._mainSurface = pygame.display.set_mode([500 + self._screenWidth + 500, self._screenHeight + 350])
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight))
		self._equipItemSurface = pygame.Surface((500, self._screenHeight))
		self._npcSurface = pygame.Surface((self._screenWidth, 350))
		self._statusSurface = pygame.Surface((500, self._screenHeight))
		self._clock = pygame.time.Clock()

		## Dict to keep the replay data
		self.world_item_dict = {}
		self.world_mobile_dict = {}
		self.player_skills_dict = {}
		self.player_status_dict = {}

		self.player_game_name = None
		self.player_hit = self.player_hit_max = None
		self.player_game_x = self.player_game_y = None
		self.player_serial = None
		self.war_mode = False
		self.hold_item_serial = 0
		self.player_gold = None
		self.targeting_state = None

		self.backpack_serial = None

		self.backpack_item_dict = {}
		self.equipped_item_dict = {}
		self.corpse_dict = {}

		self.min_tile_x = self.min_tile_y = self.max_tile_x = self.max_tile_y = None

		self.uo_installed_path = uo_installed_path
		self.uoservice_game_file_parser = UoServiceGameFileParser(self.uo_installed_path)
		self.uoservice_game_file_parser.load()

	def ConvertByteArrayToIntList(self, byteArray):
		# Convert byte array of MQP file to int list
		intList = []
		for i in range(0, len(byteArray), np.dtype(np.uint32).itemsize):
			intValue = struct.unpack('I', byteArray[i:i + 4])[0]
			intList.append(intValue)
		
		return intList

	def ConvertByteArrayToBoolList(self, byteArray):
		# Convert byte array of MQP file to bool list
		boolList = []
		for byte in byteArray:
			for i in range(8):
				bit = (byte >> i) & 1
				boolList.append(bool(bit))
		
		return boolList

	def GetSubsetArray(self, index, lengthList, offset, arr):
		# Crop the part of array when the length is variable. Return the modifed offset value for next cropping.
		item = lengthList[index]
		startIndex = offset
		subsetArray = arr[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def GetSubsetArrayFix(self, index, length, offset, arr):
		# Crop the part of array when the length is fixed. Return the modifed offset value for next cropping.
		item = length
		startIndex = offset
		subsetArray = arr[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def ReadReplay(self, fileName):
		#  the original data files and length metadata files for them from MPQ file
		self._archive = MPQArchive(self._rootPath + '/' + fileName + ".uoreplay")

		## The length byte array for data array
		self.playerObjectArrayLengthArr = self._archive.read_file("replay.meta.playerObjectLen");
		self.worldItemArrayLengthArr = self._archive.read_file("replay.meta.worldItemLen");
		self.worldMobileArrayLengthArr = self._archive.read_file("replay.meta.worldMobileLen");
		self.popupMenuArrayLengthArr = self._archive.read_file("replay.meta.popupMenuLen");
		self.clilocArrayLengthArr = self._archive.read_file("replay.meta.clilocLen");
		self.vendorListArrayLengthArr = self._archive.read_file("replay.meta.vendorListLen");
		self.playerStatusArrayLengthArr = self._archive.read_file("replay.meta.playerStatusLen");
		self.playerSkillListArrayLengthArr = self._archive.read_file("replay.meta.playerSkillListLen");
		self.playerBuffListArrayLengthArr = self._archive.read_file("replay.meta.playerBuffListLen");
		self.actionArrayLengthArr = self._archive.read_file("replay.meta.actionArraysLen");

		## Convert the byte array to int array
		self.playerObjectArrayLengthList = self.ConvertByteArrayToIntList(self.playerObjectArrayLengthArr);
		self.worldItemArrayLengthList = self.ConvertByteArrayToIntList(self.worldItemArrayLengthArr);
		self.worldMobileArrayLengthList = self.ConvertByteArrayToIntList(self.worldMobileArrayLengthArr);
		self.popupMenuArrayLengthList = self.ConvertByteArrayToIntList(self.popupMenuArrayLengthArr);
		self.clilocArrayLengthList = self.ConvertByteArrayToIntList(self.clilocArrayLengthArr);
		self.vendorListArrayLengthList = self.ConvertByteArrayToIntList(self.vendorListArrayLengthArr);
		self.playerStatusArrayLengthList = self.ConvertByteArrayToIntList(self.playerStatusArrayLengthArr);
		self.playerSkillListArrayLengthList = self.ConvertByteArrayToIntList(self.playerSkillListArrayLengthArr);
		self.playerBuffListArrayLengthList = self.ConvertByteArrayToIntList(self.playerBuffListArrayLengthArr);
		self.actionArrayLengthList = self.ConvertByteArrayToIntList(self.actionArrayLengthArr);

		## Find the total length of replay
		self._replayLength = len(self.playerObjectArrayLengthList)

		## The actual data as byte array
		self.playerObjectArr = self._archive.read_file("replay.playerObject");
		self.worldItemArr = self._archive.read_file("replay.worldItems");
		self.worldMobileArr = self._archive.read_file("replay.worldMobiles");
		self.popupMenuArr = self._archive.read_file("replay.popupMenu");
		self.clilocArr = self._archive.read_file("replay.cliloc");
		self.vendorListArr = self._archive.read_file("replay.vendorList");
		self.playerStatusArr = self._archive.read_file("replay.playerStatus");
		self.playerSkillListArr = self._archive.read_file("replay.playerSkillList");
		self.playerBuffListArr = self._archive.read_file("replay.playerBuffList");
		self.actionArr = self._archive.read_file("replay.actionArrays");

		## Check the data array is existed
		if self.playerObjectArr:
			print("len(self.playerObjectArr): ", len(self.playerObjectArr))
		else:
			print("self.playerObjectArr is None")

		if self.worldItemArr:
			print("len(self.worldItemArr): ", len(self.worldItemArr))
		else:
			print("self.worldItemArr is None")

		if self.worldMobileArr:
			print("len(self.worldMobileArr): ", len(self.worldMobileArr))
		else:
			print("self.worldMobileArr is None")

		if self.popupMenuArr:
			print("len(popupMenuArr): ", len(self.popupMenuArr))
		else:
			print("popupMenuArr is None")

		if self.clilocArr:
			print("len(self.clilocArr): ", len(self.clilocArr))
		else:
			print("self.clilocArr is None")

		if self.vendorListArr:
			print("len(self.vendorListArr): ", len(self.vendorListArr))
		else:
			print("self.vendorListArr is None")

		if self.playerStatusArr:
			print("len(self.playerStatusArr): ", len(self.playerStatusArr))
		else:
			print("self.playerStatusArr is None")

		if self.playerSkillListArr:
			print("len(self.playerSkillListArr): ", len(self.playerSkillListArr))
		else:
			print("self.playerSkillListArr is None")

		if self.playerBuffListArr:
			print("len(self.playerBuffListArr): ", len(self.playerBuffListArr))
		else:
			print("self.playerBuffListArr is None")

		if self.actionArr:
			print("len(self.actionArr): ", len(self.actionArr))
		else:
			print("self.actionArr is None")

	def ParseReplay(self):
		# Saves the loaded replay data into Python list to visualize them one by one
		player_game_x = None
		player_game_y = None
		min_tile_x = None
		min_tile_y = None
		max_tile_x = None
		max_tile_y = None

		mydict = {}

		for step in range(0, self._replayLength):
			#print("step: ", step)

			if self.playerObjectArr:
				playerObjectSubsetArray, self._playerObjectArrayOffset = self.GetSubsetArray(step, self.playerObjectArrayLengthList, 
																				             self._playerObjectArrayOffset, 
																				             self.playerObjectArr)
				grpcPlayerObjectReplay = UoService_pb2.GrpcPlayerObject().FromString(playerObjectSubsetArray)

				if grpcPlayerObjectReplay.gameX != 0:
					player_game_x = grpcPlayerObjectReplay.gameX
					player_game_y = grpcPlayerObjectReplay.gameY
					min_tile_x = grpcPlayerObjectReplay.minTileX
					min_tile_y = grpcPlayerObjectReplay.minTileY
					max_tile_x = grpcPlayerObjectReplay.maxTileX
					max_tile_y = grpcPlayerObjectReplay.maxTileY
					#print("grpcPlayerObjectReplay: ", grpcPlayerObjectReplay)

				self._playerObjectList.append(grpcPlayerObjectReplay)
			else:
				#print("playerObjectArr is None")
				pass

			if self.worldItemArr:
				worldItemSubsetArray, self._worldItemArrayOffset = self.GetSubsetArray(step, self.worldItemArrayLengthList, 
																				       self._worldItemArrayOffset, self.worldItemArr)
				grpcWorldItemReplay = UoService_pb2.GrpcItemObjectList().FromString(worldItemSubsetArray)
				self._worldItemList.append(grpcWorldItemReplay.itemObjects)
			else:
				#print("worldItemArr is None")
				pass

			if self.worldMobileArr:
				worldMobileSubsetArray, self._worldMobileArrayOffset = self.GetSubsetArray(step, self.worldMobileArrayLengthList, 
																				           self._worldMobileArrayOffset, self.worldMobileArr)
				grpcWorldMobileReplay = UoService_pb2.GrpcMobileObjectList().FromString(worldMobileSubsetArray)
				#print("grpcWorldMobileReplay: ", grpcWorldMobileReplay)
				self._worldMobileList.append(grpcWorldMobileReplay.mobileObjects)
			else:
				#print("worldMobileArr is None")
				pass

			if self.popupMenuArr:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthList, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArr)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				self._popupMenuList.append(grpcPopupMenuReplay.menus)
			else:
				#print("popupMenuArr is None")
				pass

			if self.clilocArr:
				clilocSubsetArray, self._clilocArrayOffset = self.GetSubsetArray(step, self.clilocArrayLengthList, 
																			   			 self._clilocArrayOffset, self.clilocArr)
				grpcClilocReplay = UoService_pb2.GrpcClilocList().FromString(clilocSubsetArray)
				self._clilocList.append(grpcClilocReplay.clilocs)
			else:
				pass
				#print("clilocArr is None")

			if self.vendorListArr:
				vendorListSubsetArray, self._vendorListArrayOffset = self.GetSubsetArray(step, self.vendorListArrayLengthList, 
																			   			 self._vendorListArrayOffset, self.vendorListArr)
				grpcVendorListReplay = UoService_pb2.GrpcVendorList().FromString(vendorListSubsetArray)
				self._vendorListList.append(grpcVendorListReplay.vendors)
			else:
				pass
				#print("clilocArr is None")

			if self.playerStatusArr:
				playerStatusSubsetArray, self._playerStatusArrayOffset = self.GetSubsetArray(step, self.playerStatusArrayLengthList, 
																							 self._playerStatusArrayOffset, 
																							 self.playerStatusArr)
				grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
				self._playerStatusList.append(grpcPlayerStatusReplay)
			else:
				pass
				#print("playerStatusArr is None")

			if self.playerSkillListArr:
				playerSkillListSubsetArray, self._playerSkillListArrayOffset = self.GetSubsetArray(step, self.playerSkillListArrayLengthList, 
																				   		 		   self._playerSkillListArrayOffset, 
																				   		 		   self.playerSkillListArr)
				grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray)
				self._playerSkillListList.append(grpcPlayerSkillListReplay.skills)
			else:
				pass
				#print("playerSkillListArr is None")

			if self.playerBuffListArr:
				playerBuffListSubsetArray, self._playerBuffListArrayOffset = self.GetSubsetArray(step, self.playerBuffListArrayLengthList, 
																				   		 		   self._playerBuffListArrayOffset, 
																				   		 		   self.playerBuffListArr)
				grpcPlayerBuffListReplay = UoService_pb2.GrpcBuffList().FromString(playerBuffListSubsetArray)
				self._playerBuffListList.append(grpcPlayerBuffListReplay.buffs)
			else:
				pass
				#print("playerBuffListArr is None")

			#print("self.actionArrayLengthList[step]: ", self.actionArrayLengthList[step])
			if self.actionArr:
				actionSubsetArrays, self._actionArrayOffset = self.GetSubsetArray(step, self.actionArrayLengthList, self._actionArrayOffset, 
																				  self.actionArr)
				actionReplay = UoService_pb2.GrpcAction().FromString(actionSubsetArrays)
				#print("actionReplay: ", actionReplay)
				self._actionList.append(actionReplay)
			else:
				pass
				#print("actionArr is None")

			print("step: {0}, player_game_x: {1}, player_game_y: {2}", step, player_game_x, player_game_y)

			if min_tile_x != None:
				cell_x_list = []
				cell_y_list = []
				tile_data_list = []
				for x in range(min_tile_x, max_tile_x):
					cell_x = x >> 3
					if cell_x not in cell_x_list:
						cell_x_list.append(cell_x)

				for y in range(min_tile_y, max_tile_y):
					cell_y = y >> 3
					if cell_y not in cell_y_list:
						cell_y_list.append(cell_y)

				cell_zip = zip(cell_x_list, cell_y_list)
				for cell_x in cell_x_list:
					for cell_y in cell_y_list:
						if (cell_x, cell_y) not in mydict:
							land_data_list, static_data_list = self.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)
							mydict[(cell_x, cell_y)] = [land_data_list, static_data_list]
						else:
							land_data_list, static_data_list = mydict[(cell_x, cell_y)]


		if len(self._playerObjectList) == 0:
			print("No playerObjectList")

		if len(self._worldItemList) == 0:
			print("No worldItemList")

		if len(self._worldMobileList) == 0:
			print("No worldMobileList")

		if len(self._popupMenuList) == 0:
			print("No popupMenuList")

		if len(self._clilocList) == 0:
			print("No _clilocList")

		if len(self._vendorListList) == 0:
			print("No vendorListList")

		if len(self._playerStatusList) == 0:
			print("No playerStatusList")

		if len(self._playerSkillListList) == 0:
			print("No playerSkillListList")

		if len(self._playerBuffListList) == 0:
			print("No playerBuffListList")

		if len(self._actionList) == 0:
			print("No _actionList")

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
		if self.max_tile_x != None:
			screen_length = 1000

			screen_image = np.zeros((screen_length, screen_length, 3), dtype=np.uint8)
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

			return screen_image
			#cv2.imshow('screen_image_' + str(self.grpc_port), screen_image)
			#cv2.waitKey(1)

	def InteractWithReplay(self):
		# Viewers can Forward and rewind the saved replay data by left and right arrow key
		replay_step = 0

		while True:
			for event in pygame.event.get():
				 if event.type == pygame.QUIT:
					 running = False

			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				if self._previousControl == pygame.K_LEFT:
					if self._tickScale < 300:
				  		self._tickScale += 1

				if replay_step >= 1:
					replay_step -= 1
					self._previousControl = pygame.K_LEFT
					print("replay_step: ", replay_step)
				else:
					print("This is start of replay")
			elif keys[pygame.K_RIGHT]:
				if self._previousControl == pygame.K_RIGHT:
					if self._tickScale < 300:
				  		self._tickScale += 1

				if replay_step < self._replayLength - 1:
					replay_step += 1
					self._previousControl = pygame.K_RIGHT
					print("replay_step: ", replay_step)
				else:
					print("This is end of replay")
			else:
				self._previousControl = 0
				self._tickScale = 10

			# Create the downscaled array for bigger mobile object drawing
			screen_image = np.zeros((int((self._screenWidth + 100)), int((self._screenHeight + 100)), 3), dtype=np.uint8)
			#screen_image = np.zeros((int((5000)), int((5000)), 3), dtype=np.uint8)
			if self._playerObjectList[replay_step].name != '':
				self.player_game_name = self._playerObjectList[replay_step].name
				self.player_serial = self._playerObjectList[replay_step].serial
				self.player_game_x = self._playerObjectList[replay_step].gameX
				self.player_game_y = self._playerObjectList[replay_step].gameY
				self.war_mode = self._playerObjectList[replay_step].warMode
				self.hold_item_serial = self._playerObjectList[replay_step].holdItemSerial
				self.targeting_state = self._playerObjectList[replay_step].targetingState
				self.min_tile_x = self._playerObjectList[replay_step].minTileX
				self.min_tile_y = self._playerObjectList[replay_step].minTileY
				self.max_tile_x = self._playerObjectList[replay_step].maxTileX
				self.max_tile_y = self._playerObjectList[replay_step].maxTileY

				print("player_game_x: {0}, player_game_y: {1}: ", self.player_game_x, self.player_game_y)

			#print("replay_step: ", replay_step)
			#print("self.player_game_name: ", self.player_game_name)
			#screen_image = self.parse_land_static()

			if self.player_game_name == None:
				#print("self.player_game_name: ", self.player_game_name)
				replay_step += 1
				continue

			if len(self._worldMobileList[replay_step]) != 0:
				self.world_mobile_dict = {}
				for obj in self._worldMobileList[replay_step]:
					self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
														   "distance": obj.distance, "title": obj.title, "hits": obj.hits,
														   "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
														   "race": obj.race }

			if len(self._worldItemList[replay_step]) != 0:
				self.world_item_dict = {}
				for obj in self._worldItemList[replay_step]:
					self.world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
														 "distance": obj.distance, "layer":obj.layer, "container": obj.container, 
														 "isCorpse": obj.isCorpse, "amount": obj.amount }

					if obj.layer == 21:
						self.backpack_serial = obj.serial

			if self._playerStatusList[replay_step].str != 0:
				self.player_status_dict = utils.parsePlayerStatus(self._playerStatusList[replay_step])
				#print("self.player_status_dict: ", self.player_status_dict)

			player_skills_data = self._playerSkillListList[replay_step]
			#print("player_skills_data: ", player_skills_data)

			if len(player_skills_data) != 0:
				for skill in player_skills_data:
					#player_skills_dict[skill.name] = [skill.index, skill.isClickable, skill.value, skill.base, skill.cap, skill.lock]
					self.player_skills_dict[skill.name] = {"index": skill.index, "isClickable": skill.isClickable, "value": skill.value, 
														   "base: ": skill.base, "cap": skill.cap, "lock": skill.lock}

			if len(self.world_item_dict) != 0 and self.backpack_serial != None:
				self.backpack_item_dict = {}
				self.equipped_item_dict = {}
				self.corpse_dict = {}
				for k, v in self.world_item_dict.items():
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

			if self.backpack_item_dict != 0:
				#print("self.backpack_item_dict: ", self.backpack_item_dict)
				for k, v in self.backpack_item_dict.items():
					#print("backpack item {0}: {1}".format(k, self.backpack_item_dict[k]))
					pass
				#print("")

			'''
			radius = 2
			color = (120, 120, 120)
			thickness = 2
			if self.static_object_game_x_data != None:
				for i in range(0, len(self.static_object_game_x_data)):
					if self.static_object_game_x_data[i] >= 1400 or self.static_object_game_y_data[i] >= 1280:
						continue

					image = cv2.circle(screen_image, (self.static_object_game_x_data[i], self.static_object_game_y_data[i]), 
									   radius, color, thickness)
			

			radius = 10
			thickness = 2
			for k, v in self.world_mobile_dict.items():
				#if v["gameX"] < self._screenWidth and v["gameY"] < self._screenHeight:
				screen_image = cv2.circle(screen_image, (v["gameX"], v["gameY"]), radius, (0, 0, 255), thickness)

			if self.player_game_x != None:
				screen_image = cv2.circle(screen_image, (self.player_game_x, self.player_game_y), radius, (0, 255, 0), thickness)
				screen_image = screen_image[self.player_game_y - 600:self.player_game_y + 600, self.player_game_x - 600:self.player_game_x + 600, :]

			# Draw the screen image on the Pygame screen
			screen_image = cv2.resize(screen_image, (1200, 1200), interpolation=cv2.INTER_AREA)
			screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
			screen_image = cv2.flip(screen_image, 1)

			'''
			surf = pygame.surfarray.make_surface(screen_image)
			self._screenSurface.blit(surf, (0, 0))

			#print("self._actionList[replay_step]: ", self._actionList[replay_step])

			# Draw the action info on the Pygame screen
			font = pygame.font.Font('freesansbold.ttf', 16)
			text_surface = font.render("action type: " + str(self._actionList[replay_step].actionType), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 40))
			text_surface = font.render("item serial: " + str(self._actionList[replay_step].sourceSerial), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 60))
			text_surface = font.render("mobile serial: " + str(self._actionList[replay_step].targetSerial), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 80))
			text_surface = font.render("walk direction: " + str(self._actionList[replay_step].walkDirection), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 100))
			text_surface = font.render("index: " + str(self._actionList[replay_step].index), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 120))
			text_surface = font.render("amount: " + str(self._actionList[replay_step].amount), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 140))
			text_surface = font.render("run: " + str(self._actionList[replay_step].run), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 160))

			# Draw the boundary line
			pygame.draw.line(self._screenSurface, (255, 255, 255), (1, 0), (1, self._screenHeight))
			pygame.draw.line(self._screenSurface, (255, 255, 255), (self._screenWidth - 1, 0), (self._screenWidth - 1, self._screenHeight))
			pygame.draw.line(self._screenSurface, (255, 255, 255), (0, self._screenHeight - 1), (self._screenWidth, self._screenHeight - 1))

			# Player status draw
			self._statusSurface.fill(((0, 0, 0)))
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Player Status", True, (255, 0, 255))
			self._statusSurface.blit(text_surface, (0, 0))
			for i, k in enumerate(self.player_status_dict):
				font = pygame.font.Font('freesansbold.ttf', 16)
				text_surface = font.render(str(k) + ": " + str(self.player_status_dict[k]), True, (255, 255, 255))
				self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

			# Player skill draw
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Player Skills", True, (255, 0, 255))
			self._statusSurface.blit(text_surface, (0, 500))
			for i, k in enumerate(self.player_skills_dict):
				font = pygame.font.Font('freesansbold.ttf', 16)
				skill = self.player_skills_dict[k]
				#print("k: {0}, skill: {1}".format(k, skill))
				text_surface = font.render(str(skill["index"]) + '. ' + str(k) + ": " + str(skill["value"]), 
										   True, (255, 255, 255))
				self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 520))

			# Equipped item draw
			self._equipItemSurface.fill(((0, 0, 0)))
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Equip Items", True, (255, 0, 255))
			self._equipItemSurface.blit(text_surface, (0, 0))
			for i, k in enumerate(self.equipped_item_dict):
				font = pygame.font.Font('freesansbold.ttf', 20)
				item = self.equipped_item_dict[k]
				text_surface = font.render(str(Layers(int(item["layer"])).name) + ": " + str(item["name"]), True, 
										   (255, 255, 255))
				self._equipItemSurface.blit(text_surface, (0, 25 * (i + 1) + 20))

			# Backpack item draw
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Backpack Item", True, (255, 0, 255))
			self._equipItemSurface.blit(text_surface, (0, 400))
			for i, k in enumerate(self.backpack_item_dict):
				font = pygame.font.Font('freesansbold.ttf', 16)
				item = self.backpack_item_dict[k]
				text_surface = font.render(str(k) + ": " + str(item["name"]) + ", " + str(item["amount"]), True, (255, 255, 255))
				self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 420))

			# Draw each surface on root surface
			self._mainSurface.blit(self._screenSurface, (500, 0))
			self._mainSurface.blit(self._equipItemSurface, (500 + self._screenWidth, 0))
			#self._mainSurface.blit(self._npcSurface, (500, self._screenHeight))
			self._mainSurface.blit(self._statusSurface, (0, 0))
			
			pygame.display.update()

			# Wait little bit
			#print("self._tickScale: ", self._tickScale)
			self._clock.tick(self._tickScale)