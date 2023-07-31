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
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider
import sys
import copy
from enum import Enum
import threading
import logging
from tqdm import tqdm


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

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

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
		## MQP related variable
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
		self._deleteItemSerialsArrayOffset = 0
		self._deleteMobileSerialsArrayOffset = 0
		self._actionArrayOffset = 0

		## Initialize the list to save the replay data
		self._playerObjectList = []
		self._worldItemList = []
		self._worldMobileList = []
		self._popupMenuList = []
		self._clilocList = []
		self._vendorListList = []
		self._playerStatusList = []
		self._playerSkillListList = []
		self._playerBuffListList = []
		self._deleteItemSerialsList = []
		self._deleteMobileSerialsList = []
		self._actionList = []

		## Initialize the witdh, height of replay file
		self._screenWidth = screenWidth
		self._screenHeight = screenHeight

		## PyGame related variables
		self._mainSurface = pygame.display.set_mode([500 + self._screenWidth + 500, self._screenHeight + 350])
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight - 250))
		self._rightSideSurface = pygame.Surface((500, self._screenHeight))
		self._bottomSideSurface = pygame.Surface((self._screenWidth, 350))
		self._leftSideSurface = pygame.Surface((500, self._screenHeight))
		self._clock = pygame.time.Clock()
		self._replay_step = 0

		## PyGame Widget related variables
		self._non_zero_action_step_list = []
		self._non_zero_action_index = 0
		self._pre_non_zero_action_index = self._non_zero_action_index
		
		## Global variables to keep the replay data
		self.player_object_list = []
		self.world_item_list = []
		self.world_mobile_list = []
		self.player_skill_list = []
		self.player_status_list = []
		self.player_buff_list = []
		self.cliloc_list = []
		self.vendor_item_list = []
		self.popup_menu_list = []

		self.player_game_name = None
		self.player_hit = self.player_hit_max = None
		self.player_game_x = self.player_game_y = None
		self.player_serial = None
		self.war_mode = False
		self.hold_item_serial = 0
		self.player_gold = None
		self.targeting_state = None

		self.backpack_serial = None
		self.bank_serial = None
		self.backpack_item_dict = {}
		self.equipped_item_dict = {}
		self.corpse_dict = {}

		## Variables to load the binary file for land, static data
		self.min_tile_x = self.min_tile_y = self.max_tile_x = self.max_tile_y = None
		self.cell_dict = {}
		self.uo_installed_path = uo_installed_path
		self.uoservice_game_file_parser = UoServiceGameFileParser(self.uo_installed_path)
		self.uoservice_game_file_parser.load()

	def left_action_step(self):
		#print("left_action_step()")
		if self._non_zero_action_index > 0:
			self._non_zero_action_index -= 1
		else:
			logging.warning('This is start of non-zero action step list')

		self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]
		self._slider.setValue(self._non_zero_action_index)

	def right_action_step(self):
		#print("right_action_step()")
		if self._non_zero_action_index < len(self._non_zero_action_step_list) - 1:
			self._non_zero_action_index += 1
		else:
			logging.warning('This is end of non-zero action step list')

		self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]
		self._slider.setValue(self._non_zero_action_index)

	def convert_byte_array_to_int_list(self, byteArray):
		# Convert byte array of MQP file to int list
		intList = []
		for i in range(0, len(byteArray), np.dtype(np.uint32).itemsize):
			intValue = struct.unpack('I', byteArray[i:i + 4])[0]
			intList.append(intValue)
		
		return intList

	def convert_byte_array_to_bool_list(self, byteArray):
		# Convert byte array of MQP file to bool list
		boolList = []
		for byte in byteArray:
			for i in range(8):
				bit = (byte >> i) & 1
				boolList.append(bool(bit))
		
		return boolList

	def get_subset_array(self, index, lengthList, offset, arr):
		# Crop the part of array when the length is variable. Return the modifed offset value for next cropping.
		item = lengthList[index]
		startIndex = offset
		subsetArray = arr[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def get_subset_arrayFix(self, index, length, offset, arr):
		# Crop the part of array when the length is fixed. Return the modifed offset value for next cropping.
		item = length
		startIndex = offset
		subsetArray = arr[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def read_replay(self, fileName):
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
		self.deleteItemSerialsArrayLengthArr = self._archive.read_file("replay.meta.deleteItemSerialsLen");
		self.deleteMobileSerialsArrayLengthArr = self._archive.read_file("replay.meta.deleteMobileSerialsLen");
		self.actionArrayLengthArr = self._archive.read_file("replay.meta.actionArraysLen");

		## Convert the byte array to int array
		self.playerObjectArrayLengthList = self.convert_byte_array_to_int_list(self.playerObjectArrayLengthArr);
		self.worldItemArrayLengthList = self.convert_byte_array_to_int_list(self.worldItemArrayLengthArr);
		self.worldMobileArrayLengthList = self.convert_byte_array_to_int_list(self.worldMobileArrayLengthArr);
		self.popupMenuArrayLengthList = self.convert_byte_array_to_int_list(self.popupMenuArrayLengthArr);
		self.clilocArrayLengthList = self.convert_byte_array_to_int_list(self.clilocArrayLengthArr);
		self.vendorListArrayLengthList = self.convert_byte_array_to_int_list(self.vendorListArrayLengthArr);
		self.playerStatusArrayLengthList = self.convert_byte_array_to_int_list(self.playerStatusArrayLengthArr);
		self.playerSkillListArrayLengthList = self.convert_byte_array_to_int_list(self.playerSkillListArrayLengthArr);
		self.playerBuffListArrayLengthList = self.convert_byte_array_to_int_list(self.playerBuffListArrayLengthArr);
		self.deleteItemSerialsArrayLengthList = self.convert_byte_array_to_int_list(self.deleteItemSerialsArrayLengthArr);
		self.deleteMobileSerialsArrayLengthList = self.convert_byte_array_to_int_list(self.deleteMobileSerialsArrayLengthArr);
		self.actionArrayLengthList = self.convert_byte_array_to_int_list(self.actionArrayLengthArr);

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
		self.deleteItemSerialsArr = self._archive.read_file("replay.deleteItemSerials");
		self.deleteMobileSerialsArr = self._archive.read_file("replay.deleteMobileSerials");
		self.actionArr = self._archive.read_file("replay.actionArrays");

		## Check the data array is existed
		if self.playerObjectArr:
			logging.info('Length of the playerObjectArr is %d', len(self.playerObjectArr))
		else:
			logging.warning('playerObjectArr is None')

		if self.worldItemArr:
			logging.info('Length of the worldItemArr is %d', len(self.worldItemArr))
		else:
			logging.warning('worldItemArr is None')

		if self.worldMobileArr:
			logging.info('Length of the worldMobileArr is %d', len(self.worldMobileArr))
		else:
			logging.warning('worldMobileArr is None')

		if self.popupMenuArr:
			logging.info('Length of the popupMenuArr is %d', len(self.popupMenuArr))
		else:
			logging.warning('popupMenuArr is None')

		if self.clilocArr:
			logging.info('Length of the clilocArr is %d', len(self.clilocArr))
		else:
			logging.warning('clilocArr is None')

		if self.vendorListArr:
			logging.info('Length of the vendorListArr is %d', len(self.vendorListArr))
		else:
			logging.warning('vendorListArr is None')

		if self.playerStatusArr:
			logging.info('Length of the playerStatusArr is %d', len(self.playerStatusArr))
		else:
			logging.warning('playerStatusArr is None')

		if self.playerSkillListArr:
			logging.info('Length of the playerSkillListArr is %d', len(self.playerSkillListArr))
		else:
			logging.warning('playerSkillListArr is None')

		if self.playerBuffListArr:
			logging.info('Length of the playerBuffListArr is %d', len(self.playerBuffListArr))
		else:
			logging.warning('playerBuffListArr is None')

		if self.deleteItemSerialsArr:
			logging.info('Length of the deleteItemSerialsArr is %d', len(self.deleteItemSerialsArr))
		else:
			logging.warning('deleteItemSerialsArr is None')

		if self.deleteMobileSerialsArr:
			logging.info('Length of the deleteMobileSerialsArr is %d', len(self.deleteMobileSerialsArr))
		else:
			logging.warning('deleteMobileSerialsArr is None')

		if self.actionArr:
			logging.info('Length of the actionArr is %d', len(self.actionArr))
		else:
			logging.warning('actionArr is None')

	def parse_replay(self):
		## Saves the loaded replay data into Python list to visualize them one by one

		player_game_name = None
		player_serial = None
		war_mode = None
		hold_item_serial = None
		targeting_state = None
		player_game_x = None
		player_game_y = None
		min_tile_x = None
		min_tile_y = None
		max_tile_x = None
		max_tile_y = None

		player_status_dict = {}
		player_skills_dict = {}
		player_buff_dict = {}
		cliloc_dict = {}
		popup_menu_list = []
		vendor_item_dict = {}

		## Start to parse the replay data
		for step in tqdm(range(self._replayLength)):
			if self.playerObjectArr:
				playerObjectSubsetArray, self._playerObjectArrayOffset = self.get_subset_array(step, self.playerObjectArrayLengthList, 
																																											self._playerObjectArrayOffset, 
																																											self.playerObjectArr)
				grpcPlayerObjectReplay = UoService_pb2.GrpcPlayerObject().FromString(playerObjectSubsetArray)

				## This data is needed to load the land, static data
				if grpcPlayerObjectReplay.gameX != 0:
					player_game_name = grpcPlayerObjectReplay.name
					player_serial = grpcPlayerObjectReplay.serial
					player_game_x = grpcPlayerObjectReplay.gameX
					player_game_y = grpcPlayerObjectReplay.gameY
					war_mode = grpcPlayerObjectReplay.warMode
					hold_item_serial = grpcPlayerObjectReplay.holdItemSerial
					targeting_state = grpcPlayerObjectReplay.targetingState
					min_tile_x = grpcPlayerObjectReplay.minTileX
					min_tile_y = grpcPlayerObjectReplay.minTileY
					max_tile_x = grpcPlayerObjectReplay.maxTileX
					max_tile_y = grpcPlayerObjectReplay.maxTileY

				self._playerObjectList.append(grpcPlayerObjectReplay)
			else:
				pass

			if self.worldItemArr:
				## Get the subset array from whole array using the array length data
				worldItemSubsetArray, self._worldItemArrayOffset = self.get_subset_array(step, self.worldItemArrayLengthList, 
																																								self._worldItemArrayOffset, self.worldItemArr)

				## Decode the byte array to gRPC protocol
				grpcWorldItemReplay = UoService_pb2.GrpcItemObjectList().FromString(worldItemSubsetArray)

				# Add the gRPC data to list for replay play step by step
				self._worldItemList.append(grpcWorldItemReplay.itemObjects)
			else:
				pass

			if self.worldMobileArr:
				worldMobileSubsetArray, self._worldMobileArrayOffset = self.get_subset_array(step, self.worldMobileArrayLengthList, 
																																										self._worldMobileArrayOffset, 
																																										self.worldMobileArr)
				grpcWorldMobileReplay = UoService_pb2.GrpcMobileObjectList().FromString(worldMobileSubsetArray)
				self._worldMobileList.append(grpcWorldMobileReplay.mobileObjects)
			else:
				pass

			if self.popupMenuArr:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.get_subset_array(step, self.popupMenuArrayLengthList, 
																																								self._popupMenuArrayOffset, self.popupMenuArr)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)

				if len(grpcPopupMenuReplay.menus) != 0:
					popup_menu_list = []
					for menu_data in grpcPopupMenuReplay.menus:
						popup_menu_list.append(menu_data)

				self._popupMenuList.append(grpcPopupMenuReplay.menus)
			else:
				pass

			if self.clilocArr:
				clilocSubsetArray, self._clilocArrayOffset = self.get_subset_array(step, self.clilocArrayLengthList, 
																																					self._clilocArrayOffset, self.clilocArr)
				grpcClilocReplay = UoService_pb2.GrpcClilocList().FromString(clilocSubsetArray)

				for cliloc_data in grpcClilocReplay.clilocs:
					if cliloc_data.serial not in cliloc_dict:
						cliloc_dict[cliloc_data.serial] = [{"text": cliloc_data.text, "affix": cliloc_data.affix, "name": cliloc_data.name}]
					else:
						cliloc_dict[cliloc_data.serial].append({"text": cliloc_data.text, "affix": cliloc_data.affix, "name": cliloc_data.name})

				self._clilocList.append(grpcClilocReplay.clilocs)
			else:
				pass

			if self.vendorListArr:
				vendorListSubsetArray, self._vendorListArrayOffset = self.get_subset_array(step, self.vendorListArrayLengthList, 
																																									self._vendorListArrayOffset, self.vendorListArr)
				grpcVendorListReplay = UoService_pb2.GrpcVendorList().FromString(vendorListSubsetArray)

				if len(grpcVendorListReplay.vendors) != 0:
					vendor_item_dict = {}
					for data in grpcVendorListReplay.vendors:
						print("vendor item / step: {0}, vendorSerial: {1}, itemSerial: {2}".format(step, data.vendorSerial, data.itemSerial))
						vendor_item_dict[data.itemSerial] = { "vendor_serial": data.vendorSerial, "item_serial": data.itemSerial, 
																								  "item_graphic": data.itemGraphic, "item_hue": data.itemHue,
																								  "item_amount": data.itemAmount, "item_price":data.itemPrice, 
																								  "item_name": data.itemName}

				self._vendorListList.append(grpcVendorListReplay.vendors)
			else:
				pass

			if self.playerStatusArr:
				playerStatusSubsetArray, self._playerStatusArrayOffset = self.get_subset_array(step, self.playerStatusArrayLengthList, 
																																											self._playerStatusArrayOffset, 
																																											self.playerStatusArr)
				grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
				if grpcPlayerStatusReplay.str != 0:
					player_status_dict = utils.parsePlayerStatus(grpcPlayerStatusReplay)

				self._playerStatusList.append(grpcPlayerStatusReplay)
			else:
				pass

			if self.playerSkillListArr:
				playerSkillListSubsetArray, self._playerSkillListArrayOffset = self.get_subset_array(step, self.playerSkillListArrayLengthList, 
																																														self._playerSkillListArrayOffset, 
																																														self.playerSkillListArr)
				grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray)
				if len(grpcPlayerSkillListReplay.skills) != 0:
					for skill in grpcPlayerSkillListReplay.skills:
						if skill.value != 0:
							player_skills_dict[skill.name] = {"index": skill.index, "isClickable": skill.isClickable, "value": skill.value, 
																								"base: ": skill.base, "cap": skill.cap, "lock": skill.lock}

				self._playerSkillListList.append(grpcPlayerSkillListReplay.skills)
			else:
				pass

			if self.playerBuffListArr:
				playerBuffListSubsetArray, self._playerBuffListArrayOffset = self.get_subset_array(step, self.playerBuffListArrayLengthList, 
																																													self._playerBuffListArrayOffset, 
																																													self.playerBuffListArr)
				grpcPlayerBuffListReplay = UoService_pb2.GrpcBuffList().FromString(playerBuffListSubsetArray)
				self._playerBuffListList.append(grpcPlayerBuffListReplay.buffs)

				for buff in grpcPlayerBuffListReplay.buffs:
					player_buff_dict[buff.type] = {"text": buff.text, "delta": buff.delta}
			else:
				pass

			if self.deleteItemSerialsArr:
				deleteItemSerialsSubsetArray, self._deleteItemSerialsArrayOffset = self.get_subset_array(step, self.deleteItemSerialsArrayLengthList, 
																																																self._deleteItemSerialsArrayOffset, 
																																																self.deleteItemSerialsArr)
				grpcDeleteItemSerialsReplay = UoService_pb2.GrpcDeleteItemSerialList().FromString(deleteItemSerialsSubsetArray)
				self._deleteItemSerialsList.append(grpcDeleteItemSerialsReplay.serials)
			else:
				pass

			if self.deleteMobileSerialsArr:
				deleteMobileSerialsSubsetArray, self._deleteMobileSerialsArrayOffset = self.get_subset_array(step, self.deleteMobileSerialsArrayLengthList, 
																																																		self._deleteMobileSerialsArrayOffset, 
																																																		self.deleteMobileSerialsArr)
				grpcDeleteMobileSerialsReplay = UoService_pb2.GrpcDeleteMobileSerialList().FromString(deleteMobileSerialsSubsetArray)
				self._deleteMobileSerialsList.append(grpcDeleteMobileSerialsReplay.serials)
			else:
				pass

			if self.actionArr:
				actionSubsetArrays, self._actionArrayOffset = self.get_subset_array(step, self.actionArrayLengthList, self._actionArrayOffset, 
																																						self.actionArr)
				actionReplay = UoService_pb2.GrpcAction().FromString(actionSubsetArrays)

				if actionReplay.actionType != 0:
					self._non_zero_action_step_list.append(step)

				if actionReplay.actionType == 11:
					popup_menu_list = []

				self._actionList.append(actionReplay)
			else:
				pass

			## Store the every step data of player object into list to move the replay step flexibly
			player_object_dict = {}
			player_object_dict["player_game_name"] = player_game_name
			player_object_dict["player_serial"] = player_serial
			player_object_dict["player_game_x"] = player_game_x
			player_object_dict["player_game_y"] = player_game_y
			player_object_dict["war_mode"] = war_mode
			player_object_dict["hold_item_serial"] = hold_item_serial
			player_object_dict["targeting_state"] = targeting_state
			player_object_dict["min_tile_x"] = min_tile_x
			player_object_dict["min_tile_y"] = min_tile_y
			player_object_dict["max_tile_x"] = max_tile_x
			player_object_dict["max_tile_y"] = max_tile_y
			self.player_object_list.append(copy.deepcopy(player_object_dict))	

			## Store the every step data of player status into list to move the replay step flexibly
			self.player_status_list.append(copy.deepcopy(player_status_dict))	

			## Store the every step data of player skill into list to move the replay step flexibly
			self.player_skill_list.append(copy.deepcopy(player_skills_dict))

			## Store the every step data of cliloc data into list to move the replay step flexibly
			self.cliloc_list.append(copy.deepcopy(cliloc_dict))	

			## Store the every step data of popup menu data into list to move the replay step flexibly
			self.popup_menu_list.append(copy.deepcopy(popup_menu_list))	

			## Store the every step data of player buff into list to move the replay step flexibly
			self.player_buff_list.append(copy.deepcopy(player_buff_dict))

			## Store the every step data of vendor item list into list to move the replay step flexibly
			self.vendor_item_list.append(copy.deepcopy(vendor_item_dict))	

			## Load the cell data for land, static data before replay playing to improve the speed of visualzation
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
						if (cell_x, cell_y) not in self.cell_dict:
							land_data_list, static_data_list = self.uoservice_game_file_parser.get_tile_data(cell_x, cell_y)
							self.cell_dict[(cell_x, cell_y)] = [land_data_list, static_data_list]
						else:
							land_data_list, static_data_list = self.cell_dict[(cell_x, cell_y)]

		# PyGame Widget
		self._slider = Slider(self._mainSurface, 500 + int(self._screenWidth / 2) - 100, self._screenHeight - 250 + 30, 
													700, 40, min=0, max=len(self._non_zero_action_step_list) - 1, step=1)

		self._non_zero_action_index = int(self._slider.getValue())

		self._mainSurface.fill(((131, 139, 139)))

	def parse_world_data(self):
		world_item_dict = {}
		world_mobile_dict = {}

		for step in tqdm(range(self._replayLength)):
			## Save the world item object into global Dict	
			if len(self._worldItemList[step]) != 0:
				for obj in self._worldItemList[step]:
					world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
																					"distance": obj.distance, "layer":obj.layer, "container": obj.container, 
																					"isCorpse": obj.isCorpse, "amount": obj.amount, "price": obj.price }

					## Check the serial number of backpack container
					if obj.layer == 21:
						self.backpack_serial = obj.serial

					## Check the serial number of bank container
					if obj.layer == 29:
						self.bank_serial = obj.serial

			## Save the world mobile object into global Dict
			if len(self._worldMobileList[step]) != 0:
				for obj in self._worldMobileList[step]:
					world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
																						"distance": obj.distance, "title": obj.title, "hits": obj.hits,
																						"notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
																						"race": obj.race }

			## Delete the item from world item Dict using the gRPC data
			if self.deleteItemSerialsArr is not None and len(self._deleteItemSerialsList[step]) != 0:
				for serial in self._deleteItemSerialsList[step]:
					if serial in world_item_dict:
						del world_item_dict[serial]

			## Delete the mobile from world mobile Dict using the gRPC data
			if self.deleteMobileSerialsArr is not None and len(self._deleteMobileSerialsList[step]) != 0:
				for serial in self._deleteMobileSerialsList[step]:
					if serial in world_mobile_dict:
						del world_mobile_dict[serial]

			self.world_item_list.append(copy.deepcopy(world_item_dict))
			self.world_mobile_list.append(copy.deepcopy(world_mobile_dict))

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

	def rendering_data(self):
		## Rendering the replay data obtained from InteractWithReplay function
		if True:
			## Only parse when player is in the world
			if self.max_tile_x != None:
				self._mainSurface.fill(((131, 139, 139)))

				## Main game screen array
				screen_length = 1000
				screen_image = np.zeros((screen_length, screen_length, 3), dtype=np.uint8)

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
				cell_zip = zip(cell_x_list, cell_y_list)
				for cell_x in cell_x_list:
					for cell_y in cell_y_list:
						## Get the land and static data of cell position
						land_data_list, static_data_list = self.cell_dict[(cell_x, cell_y)]

						for land_data in land_data_list:
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
							screen_image = cv2.putText(screen_image, str(index), org, cv2.FONT_HERSHEY_SIMPLEX, 0.4, pygame.Color('blue'), 1, cv2.LINE_4)

							## Draw the different color box for land
							if land_data["name"] == "forest":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('darkgreen'), 1)
							elif land_data["name"] == "rock":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('yellow'), 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('gray'), 1)

						for static_data in static_data_list:
							## Box start and end position
							start_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) - int(scale / 2) )
							end_point = ( (static_data["game_x"] - player_game_x) * scale + int(screen_length / 2) + int(scale / 2), 
											(static_data["game_y"] - player_game_y) * scale + int(screen_length / 2) + int(scale / 2) )

							## Draw the different color box for static object
							if "grasses" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('green'), 1)
							elif "wall" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('white'), -1)
							elif "water" in static_data["name"]:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('cadetblue'), 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('lavenderblush2'), 1)
				
				## Rendering the mobile data of replay as real screen scale 
				screen_width = 4000
				screen_height = 4000
				radius = int(scale / 2)
				world_mobile_dict = self.world_mobile_list[self._replay_step]
				for k, v in world_mobile_dict.items():
					if self.player_game_x != None:
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											  radius, pygame.Color('red'), -1)

							screen_image = cv2.putText(screen_image, "  " + v["name"], 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('red'), 1, cv2.LINE_4)

				## Rendering the item data of replay as real screen scale 
				world_item_dict = self.world_item_list[self._replay_step]
				for k, v in world_item_dict.items():
					if self.player_game_x != None:
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2)
											), radius, pygame.Color('blue'), -1)
		          
							item_name_list = v["name"].split(" ")
							screen_image = cv2.putText(screen_image, "     " + item_name_list[-1], 
												( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
												  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
												cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('blue'), 1, cv2.LINE_4)

				##
				corpse_dict = {}
				for k, v in world_item_dict.items():
					if v["isCorpse"] == True:
						corpse_dict[k] = v

				##
				corpse_item_dict = {}
				for k_corpse, v_corpse in corpse_dict.items():
					for k_world, v_world in world_item_dict.items():
						if k_corpse == v_world["container"]:
							if k_corpse not in corpse_item_dict:
								corpse_item_dict[k_corpse] = [world_item_dict[k_world]]
							else:
								corpse_item_dict[k_corpse].append(world_item_dict[k_world])

				##
				if len(corpse_item_dict) != 0:
					for k_corpse_item, v_corpse_item_list in corpse_item_dict.items():
						#print("v_corpse_item_list: ", v_corpse_item_list)
						for i, corpse_item in enumerate(v_corpse_item_list):
							#print("corpse item: {0}, corpse x: {1}, corpse y: {2}".format(corpse_item["name"], corpse["gameX"]))
							corpse = world_item_dict[k_corpse_item]

							start_point = ( (corpse["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale), 
											(corpse["gameY"] - player_game_y) * scale + int(screen_length / 2) - int(scale) )
							end_point = ( (corpse["gameX"] - player_game_x) * scale + int(screen_length / 2) + int(scale), 
											(corpse["gameY"] - player_game_y) * scale + int(screen_length / 2) + int(scale) )
							screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('yellow'), 1)

							screen_image = cv2.putText(screen_image, corpse_item["name"], 
												( (corpse["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
												  (corpse["gameY"] - player_game_y) * scale + int(screen_length / 2) + i * 20 ), 
													cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('yellow'), 1, cv2.LINE_4)
						pass
					#print("")

				## Cropping the real screen around player position to zoom in
				boundary = 500
				radius = int(scale / 2)
				if self.player_game_x != None:
					screen_image = cv2.putText(screen_image, str(self.player_game_name), (int(screen_length / 2), int(screen_length / 2) + int(scale / 2)), 
											  cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('green'), 1, cv2.LINE_4)

					radius = int(scale / 2)
					screen_image = cv2.circle(screen_image, (int(screen_length / 2), int(screen_length / 2)), radius, utils.color_dict["Lime"], -1)
					screen_image = screen_image[int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, 
												int(screen_length / 2) - boundary:int(screen_length / 2) + boundary, :]
		        
		    ## Resize the cropped screen larger
				screen_image = cv2.resize(screen_image, (screen_length, screen_length), interpolation=cv2.INTER_AREA)

				## Flip and rotate image to show like a real game angle
				screen_image = cv2.flip(screen_image, 0)
				screen_image = utils.rotate_image(screen_image, -45)

				## Draw the main screen image into PyGame screen
				surf = pygame.surfarray.make_surface(screen_image)
				self._screenSurface.blit(surf, (0, 0))

				## Draw the action info on the Pygame screen
				font = pygame.font.Font('freesansbold.ttf', 16)
				text_surface = font.render("action type: " + str(self._actionList[self._replay_step].actionType), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 40))
				text_surface = font.render("source serial: " + str(self._actionList[self._replay_step].sourceSerial), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 60))
				text_surface = font.render("target serial: " + str(self._actionList[self._replay_step].targetSerial), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 80))
				text_surface = font.render("walk direction: " + str(self._actionList[self._replay_step].walkDirection), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 100))
				text_surface = font.render("index: " + str(self._actionList[self._replay_step].index), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 120))
				text_surface = font.render("amount: " + str(self._actionList[self._replay_step].amount), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 140))
				text_surface = font.render("run: " + str(self._actionList[self._replay_step].run), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 160))

				## Replay step draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render(str(self._replay_step) + " / " + str(self._replayLength), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (int(self._screenWidth / 2) - 60, 10))

				## _non_zero_action_index
				font = pygame.font.Font('freesansbold.ttf', 26)
				title = "Non Zero Action Mover: "
				text_surface = font.render(title + str(self._non_zero_action_index) + " / " + str(len(self._non_zero_action_step_list)), 
																	 True, (255, 255, 255))
				self._mainSurface.blit(text_surface, (500 + 50, self._screenHeight - 250 + 35))

				## Draw the boundary line of screenSurface
				pygame.draw.line(self._screenSurface, (255, 255, 255), (1, 0), (1, self._screenHeight))
				pygame.draw.line(self._screenSurface, (255, 255, 255), (self._screenWidth - 1, 0), (self._screenWidth - 1, self._screenHeight))
				pygame.draw.line(self._screenSurface, (255, 255, 255), (0, self._screenHeight - 250 - 1), (self._screenWidth, self._screenHeight - 250 - 1))

				## Draw the boundary line of control widgets
				pygame.draw.line(self._mainSurface, (255, 255, 255), 
												 (500, self._screenHeight - 150 - 1), (self._screenWidth + 500, self._screenHeight - 150 - 1))
				pygame.draw.line(self._mainSurface, (255, 255, 255), (500 + 1, 0), (500 + 1, self._screenHeight - 150))
				pygame.draw.line(self._mainSurface, (255, 255, 255), 
												 (500 + self._screenWidth - 1, 0), (500 + self._screenWidth - 1, self._screenHeight - 150))

				## Player status draw
				self._leftSideSurface.fill(((0, 0, 0)))
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Player Status", True, (255, 0, 255))
				self._leftSideSurface.blit(text_surface, (0, 0))
				player_status_dict = self.player_status_list[self._replay_step]
				for i, k in enumerate(player_status_dict):
					font = pygame.font.Font('freesansbold.ttf', 16)
					text_surface = font.render(str(k) + ": " + str(player_status_dict[k]), True, (255, 255, 255))
					self._leftSideSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

				## Player skill draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Player Skills", True, (255, 0, 255))
				self._leftSideSurface.blit(text_surface, (0, 300))
				player_skills_dict = self.player_skill_list[self._replay_step]
				skill_last_y = 300
				for i, k in enumerate(player_skills_dict):
					font = pygame.font.Font('freesansbold.ttf', 16)
					skill = player_skills_dict[k]
					text_surface = font.render(str(skill["index"]) + '. ' + str(k) + ": " + str(skill["value"]), True, (255, 255, 255))
					self._leftSideSurface.blit(text_surface, (0, 20 * (i + 1) + 320))
					skill_last_y = 20 * (i + 1) + 320

				## Player buff draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Player Buffs", True, (255, 0, 255))
				self._leftSideSurface.blit(text_surface, (0, skill_last_y + 30))
				player_buff_dict = self.player_buff_list[self._replay_step]
				for i, k in enumerate(player_buff_dict):
					font = pygame.font.Font('freesansbold.ttf', 16)
					buff = player_buff_dict[k]
					text = buff["text"].replace('<left>', '').replace('</left>', '').split("\n")[0]
					text_surface = font.render(text + ", " + str(buff["delta"]), True, (255, 255, 255))
					self._leftSideSurface.blit(text_surface, (0, 20 * (i + 1) + skill_last_y + 50))

				## Equipped item draw
				self._rightSideSurface.fill(((0, 0, 0)))
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Equip Items", True, (255, 0, 255))
				self._rightSideSurface.blit(text_surface, (0, 0))
				for i, k in enumerate(self.equipped_item_dict):
					font = pygame.font.Font('freesansbold.ttf', 20)
					item = self.equipped_item_dict[k]
					text_surface = font.render(str(Layers(int(item["layer"])).name) + ": " + str(item["name"]), True, (255, 255, 255))
					self._rightSideSurface.blit(text_surface, (0, 25 * (i + 1) + 20))

				## Backpack item draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Backpack Item", True, (255, 0, 255))
				self._rightSideSurface.blit(text_surface, (0, 400))
				backpack_last_y = 400
				for i, k in enumerate(self.backpack_item_dict):
					font = pygame.font.Font('freesansbold.ttf', 18)
					item = self.backpack_item_dict[k]
					text_surface = font.render(str(k) + ": " + str(item["name"]) + ", " + str(item["amount"]), True, (255, 255, 255))
					self._rightSideSurface.blit(text_surface, (0, 20 * (i + 1) + 420))
					backpack_last_y = 20 * (i + 1) + 420

				## Vendor item draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Vendor Item", True, (255, 0, 255))
				self._rightSideSurface.blit(text_surface, (0, backpack_last_y + 30))
				vendor_item_dict = self.vendor_item_list[self._replay_step]
				font = pygame.font.Font('freesansbold.ttf', 20)
				for i, k in enumerate(vendor_item_dict):
					item = vendor_item_dict[k]
					vendor_serial = item['vendor_serial']
					item_serial = item['item_serial']
					vendor_name = world_mobile_dict[vendor_serial]['name']
					item_name = item['item_name']
					item_price = item['item_price']
					item_amount = item['item_amount']
					text_surface = font.render(vendor_name + ": " + item_name + ", " + str(item_price) + ", " + str(item_amount), 
																		 True, (255, 255, 255))
					self._rightSideSurface.blit(text_surface, (0, 20 * (i + 1) + backpack_last_y + 50))

				## Popup menu draw
				popup_menu_data = self.popup_menu_list[self._replay_step]
				#print("step: {0}, popup_menu_data: {1}".format(self._replay_step, popup_menu_data))

				## Cliloc data draw
				self._bottomSideSurface.fill((pygame.Color('black')))
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Cliloc List", True, (255, 0, 255))
				self._bottomSideSurface.blit(text_surface, (0, 0))
				cliloc_data = self.cliloc_list[self._replay_step]
				if len(cliloc_data) != 0:
					font = pygame.font.Font('freesansbold.ttf', 24)
					for i, k in enumerate(cliloc_data):
						item = cliloc_data[k][-1]
						text_surface = font.render(str(item["name"]) + ": " + str(item["text"]) + ", " + str(item["affix"]) + ", " + str(k), 
																			 True, (255, 255, 255))
						self._bottomSideSurface.blit(text_surface, (0, 25 * (i + 1)))

				## Draw each surface on root surface
				self._mainSurface.blit(self._screenSurface, (500, 0))
				self._mainSurface.blit(self._rightSideSurface, (500 + self._screenWidth, 0))
				self._mainSurface.blit(self._bottomSideSurface, (500, self._screenHeight - 150))
				self._mainSurface.blit(self._leftSideSurface, (0, 0))

				self._slider.draw()

				pygame.display.update()

	def interact_with_replay(self):
		## Viewers can Forward and rewind the saved replay data by left and right arrow key
		self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]

		## Start PyGame loop to interact with human
		while True:
			## Quit event check
			events = pygame.event.get()

			for event in events:
				 if event.type == pygame.QUIT:
					 running = False

			self._non_zero_action_index = self._slider.getValue()
			if self._non_zero_action_index != self._pre_non_zero_action_index:
				self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]

			pygame_widgets.update(events)

			## Check the left, right key input
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				## Check the previous input is repeated
				if self._previousControl == pygame.K_LEFT:
					if self._tickScale < 100:
				  		self._tickScale += 1

				## Decrease the step when there is left arrow input
				if self._replay_step >= 1:
					self._replay_step -= 1

					if self._non_zero_action_index > 0:
						if self._replay_step <= self._non_zero_action_step_list[self._non_zero_action_index - 1]:
							self._non_zero_action_index -= 1
							self._slider.setValue(self._non_zero_action_index)

					self._previousControl = pygame.K_LEFT
				else:
					logging.warning('This is start of replay')
			elif keys[pygame.K_RIGHT]:
				## Same as left key part
				if self._previousControl == pygame.K_RIGHT:
					if self._tickScale < 100:
				  		self._tickScale += 1

				if self._replay_step < self._replayLength - 1:
					self._replay_step += 1
					
					if self._non_zero_action_index < len(self._non_zero_action_step_list) - 1:
						if self._replay_step > self._non_zero_action_step_list[self._non_zero_action_index + 1]:
							self._non_zero_action_index += 1
							self._slider.setValue(self._non_zero_action_index)

					self._previousControl = pygame.K_RIGHT
				else:
					logging.warning('This is end of replay')
			elif keys[pygame.K_a]:
				#print("keys[pygame.K_a]")
				if self._non_zero_action_index > 0:
					self._non_zero_action_index -= 1
					self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]
					self._slider.setValue(self._non_zero_action_index)
				else:
					logging.warning('This is start of non zero action index')
			elif keys[pygame.K_d]:
				#print("keys[pygame.K_d]")
				if self._non_zero_action_index < len(self._non_zero_action_step_list) - 1:
					self._non_zero_action_index += 1
					self._replay_step = self._non_zero_action_step_list[self._non_zero_action_index]
					self._slider.setValue(self._non_zero_action_index)
				else:
					logging.warning('This is end of non zero action index')
			else:
				## Switch to slow replay mode when key input is not repeated
				self._previousControl = 0
				self._tickScale = 10

			## Create the downscaled array for bigger mobile object drawing
			screen_image = np.zeros((int((self._screenWidth + 100)), int((self._screenHeight + 100)), 3), dtype=np.uint8)
			if "player_game_name" in self.player_object_list[self._replay_step]:
				self.player_game_name = self.player_object_list[self._replay_step]["player_game_name"]
				self.player_serial = self.player_object_list[self._replay_step]["player_serial"]
				self.player_game_x = self.player_object_list[self._replay_step]["player_game_x"]
				self.player_game_y = self.player_object_list[self._replay_step]["player_game_y"]
				self.war_mode = self.player_object_list[self._replay_step]["war_mode"]
				self.hold_item_serial = self.player_object_list[self._replay_step]["hold_item_serial"]
				self.targeting_state = self.player_object_list[self._replay_step]["targeting_state"]
				self.min_tile_x = self.player_object_list[self._replay_step]["min_tile_x"]
				self.min_tile_y = self.player_object_list[self._replay_step]["min_tile_y"]
				self.max_tile_x = self.player_object_list[self._replay_step]["max_tile_x"]
				self.max_tile_y = self.player_object_list[self._replay_step]["max_tile_y"]
				#print("player_game_x: {0}, player_game_y: {1}: ", self.player_game_x, self.player_game_y)

			if len(self.world_item_list[self._replay_step]) != 0:
				world_item_dict = self.world_item_list[self._replay_step]
				for k, v in world_item_dict.items():
					## Check the serial number of backpack container
					if v["layer"] == 21:
						self.backpack_serial = k

					## Check the serial number of bank container
					if v["layer"] == 29:
						self.bank_serial = k

			## Parse the backpack, equipped, corpse item from world item
			if len(self.world_item_list[self._replay_step]) != 0 and self.backpack_serial != None:
				world_item_dict = self.world_item_list[self._replay_step]

				self.backpack_item_dict = {}
				self.equipped_item_dict = {}
				self.corpse_dict = {}
				for k, v in world_item_dict.items():
					#print("world item / step: {0}, name: {1}".format(self._replay_step, v['name']))

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

			self.rendering_data()

			self._pre_non_zero_action_index = self._non_zero_action_index

			# PyGame speed control
			self._clock.tick(self._tickScale)