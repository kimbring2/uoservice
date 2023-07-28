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
import copy
from enum import Enum
import threading
import logging

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


## Contol box to move to the specific replay point
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.main_surface = pygame.Surface((300, 50))
        self.main_surface.fill((pygame.Color('green')))

        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

        return self.text

    def draw(self, screen):
        # Blit the text.
        self.main_surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        screen.blit(self.main_surface, (900, 900))

        # Blit the rect.
        #pygame.draw.rect(screen, self.color, self.rect, 2)
        pygame.draw.rect(self.main_surface, self.color, self.rect, 2)


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
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight))
		self._equipItemSurface = pygame.Surface((500, self._screenHeight))
		self._npcSurface = pygame.Surface((self._screenWidth, 350))
		self._statusSurface = pygame.Surface((500, self._screenHeight))
		self._clock = pygame.time.Clock()
		self._replay_step = 0
		self._step_box = InputBox(900, 900, 140, 32)

		## Variables to keep the replay data
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
		self.deleteItemSerialsArrayLengthArr = self._archive.read_file("replay.meta.deleteItemSerialsLen");
		self.deleteMobileSerialsArrayLengthArr = self._archive.read_file("replay.meta.deleteMobileSerialsLen");
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
		self.deleteItemSerialsArrayLengthList = self.ConvertByteArrayToIntList(self.deleteItemSerialsArrayLengthArr);
		self.deleteMobileSerialsArrayLengthList = self.ConvertByteArrayToIntList(self.deleteMobileSerialsArrayLengthArr);
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

	def ParseReplay(self):
		## Saves the loaded replay data into Python list to visualize them one by one
		player_game_x = None
		player_game_y = None
		min_tile_x = None
		min_tile_y = None
		max_tile_x = None
		max_tile_y = None

		## Start to parse the replay data
		for step in range(0, self._replayLength):
			if self.playerObjectArr:
				playerObjectSubsetArray, self._playerObjectArrayOffset = self.GetSubsetArray(step, self.playerObjectArrayLengthList, 
																				             self._playerObjectArrayOffset, 
																				             self.playerObjectArr)
				grpcPlayerObjectReplay = UoService_pb2.GrpcPlayerObject().FromString(playerObjectSubsetArray)

				## This data is needed to load the land, static data
				if grpcPlayerObjectReplay.gameX != 0:
					player_game_x = grpcPlayerObjectReplay.gameX
					player_game_y = grpcPlayerObjectReplay.gameY
					min_tile_x = grpcPlayerObjectReplay.minTileX
					min_tile_y = grpcPlayerObjectReplay.minTileY
					max_tile_x = grpcPlayerObjectReplay.maxTileX
					max_tile_y = grpcPlayerObjectReplay.maxTileY

				self._playerObjectList.append(grpcPlayerObjectReplay)
			else:
				pass

			if self.worldItemArr:
				## Get the subset array from whole array using the array length data
				worldItemSubsetArray, self._worldItemArrayOffset = self.GetSubsetArray(step, self.worldItemArrayLengthList, 
																				       self._worldItemArrayOffset, self.worldItemArr)

				## Decode the byte array to gRPC protocol
				grpcWorldItemReplay = UoService_pb2.GrpcItemObjectList().FromString(worldItemSubsetArray)

				# Add the gRPC data to list for replay play step by step
				self._worldItemList.append(grpcWorldItemReplay.itemObjects)
			else:
				pass

			if self.worldMobileArr:
				worldMobileSubsetArray, self._worldMobileArrayOffset = self.GetSubsetArray(step, self.worldMobileArrayLengthList, 
																				           self._worldMobileArrayOffset, self.worldMobileArr)
				grpcWorldMobileReplay = UoService_pb2.GrpcMobileObjectList().FromString(worldMobileSubsetArray)
				self._worldMobileList.append(grpcWorldMobileReplay.mobileObjects)
			else:
				pass

			if self.popupMenuArr:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthList, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArr)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				self._popupMenuList.append(grpcPopupMenuReplay.menus)
			else:
				pass

			if self.clilocArr:
				clilocSubsetArray, self._clilocArrayOffset = self.GetSubsetArray(step, self.clilocArrayLengthList, 
																			   			 self._clilocArrayOffset, self.clilocArr)
				grpcClilocReplay = UoService_pb2.GrpcClilocList().FromString(clilocSubsetArray)
				self._clilocList.append(grpcClilocReplay.clilocs)
			else:
				pass

			if self.vendorListArr:
				vendorListSubsetArray, self._vendorListArrayOffset = self.GetSubsetArray(step, self.vendorListArrayLengthList, 
																			   			 self._vendorListArrayOffset, self.vendorListArr)
				grpcVendorListReplay = UoService_pb2.GrpcVendorList().FromString(vendorListSubsetArray)
				self._vendorListList.append(grpcVendorListReplay.vendors)
			else:
				pass

			if self.playerStatusArr:
				playerStatusSubsetArray, self._playerStatusArrayOffset = self.GetSubsetArray(step, self.playerStatusArrayLengthList, 
																							 self._playerStatusArrayOffset, 
																							 self.playerStatusArr)
				grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
				self._playerStatusList.append(grpcPlayerStatusReplay)
			else:
				pass

			if self.playerSkillListArr:
				playerSkillListSubsetArray, self._playerSkillListArrayOffset = self.GetSubsetArray(step, self.playerSkillListArrayLengthList, 
																				   		 		   self._playerSkillListArrayOffset, 
																				   		 		   self.playerSkillListArr)
				grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray)
				self._playerSkillListList.append(grpcPlayerSkillListReplay.skills)
			else:
				pass

			if self.playerBuffListArr:
				playerBuffListSubsetArray, self._playerBuffListArrayOffset = self.GetSubsetArray(step, self.playerBuffListArrayLengthList, 
																				   		 		   self._playerBuffListArrayOffset, 
																				   		 		   self.playerBuffListArr)
				grpcPlayerBuffListReplay = UoService_pb2.GrpcBuffList().FromString(playerBuffListSubsetArray)
				self._playerBuffListList.append(grpcPlayerBuffListReplay.buffs)
			else:
				pass

			if self.deleteItemSerialsArr:
				deleteItemSerialsSubsetArray, self._deleteItemSerialsArrayOffset = self.GetSubsetArray(step, self.deleteItemSerialsArrayLengthList, 
																				   		 		   self._deleteItemSerialsArrayOffset, 
																				   		 		   self.deleteItemSerialsArr)
				grpcDeleteItemSerialsReplay = UoService_pb2.GrpcDeleteItemSerialList().FromString(deleteItemSerialsSubsetArray)
				self._deleteItemSerialsList.append(grpcDeleteItemSerialsReplay.serials)
			else:
				pass

			if self.deleteMobileSerialsArr:
				deleteMobileSerialsSubsetArray, self._deleteMobileSerialsArrayOffset = self.GetSubsetArray(step, self.deleteMobileSerialsArrayLengthList, 
																				   		 		   self._deleteMobileSerialsArrayOffset, 
																				   		 		   self.deleteMobileSerialsArr)
				grpcDeleteMobileSerialsReplay = UoService_pb2.GrpcDeleteMobileSerialList().FromString(deleteMobileSerialsSubsetArray)
				self._deleteMobileSerialsList.append(grpcDeleteMobileSerialsReplay.serials)
			else:
				pass

			if self.actionArr:
				actionSubsetArrays, self._actionArrayOffset = self.GetSubsetArray(step, self.actionArrayLengthList, self._actionArrayOffset, 
																				  self.actionArr)
				actionReplay = UoService_pb2.GrpcAction().FromString(actionSubsetArrays)
				self._actionList.append(actionReplay)
			else:
				pass

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
		while True:
			## Only parsing when player is in the world
			if self.max_tile_x != None:
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
							screen_image = cv2.putText(screen_image, str(index), org, cv2.FONT_HERSHEY_SIMPLEX, 0.4, pygame.Color('blue'), 1, cv2.LINE_4)

							## Draw the different color box for land
							if land_data["name"] == "forest":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('darkgreen'), 1)
							elif land_data["name"] == "rock":
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('yellow'), 1)
							else:
								screen_image = cv2.rectangle(screen_image, start_point, end_point, pygame.Color('gray'), 1)

						for static_data in static_data_list:
							#print("static / name: {0}, game_x: {1}, game_y: {2}".format(static_data["name"], static_data["game_x"], static_data["game_y"]))

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
				world_mobile_dict = copy.deepcopy(self.world_mobile_dict)
				for k, v in world_mobile_dict.items():
					if self.player_game_x != None:
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											  radius, pygame.Color('blue'), -1)

							screen_image = cv2.putText(screen_image, "  " + v["name"], 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
											cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('blue'), 1, cv2.LINE_4)

				## Rendering the item data of replay as real screen scale 
				world_item_dict = copy.deepcopy(self.world_item_dict)
				for k, v in world_item_dict.items():
					if self.player_game_x != None:
						#print("world item {0}: {1}".format(k, self.world_item_dict[k]))
						if v["gameX"] < screen_width and v["gameY"] < screen_height:
							screen_image = cv2.circle(screen_image, 
											( (v["gameX"] - player_game_x) * scale + int(screen_length / 2), 
											  (v["gameY"] - player_game_y) * scale + int(screen_length / 2)
											),
											radius, pygame.Color('purple'), -1)
		          
							item_name_list = v["name"].split(" ")
							screen_image = cv2.putText(screen_image, "     " + item_name_list[-1], 
												( (v["gameX"] - player_game_x) * scale + int(screen_length / 2) - int(scale / 2), 
												  (v["gameY"] - player_game_y) * scale + int(screen_length / 2) ), 
												cv2.FONT_HERSHEY_SIMPLEX, 0.5, pygame.Color('purple'), 1, cv2.LINE_4)

				## Cropping the real screen around player position to zoom in
				boundary = 500
				radius = int(scale / 2)
				if self.player_game_x != None:
					#print("player_game_x: {0}, player_game_y: {1}".format(self.player_game_x, self.player_game_y))
					screen_image = cv2.putText(screen_image, str("player"), (int(screen_length / 2), int(screen_length / 2) - int(scale / 2)), 
											  cv2.FONT_HERSHEY_SIMPLEX, 1.0, pygame.Color('green'), 4, cv2.LINE_4)

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
				text_surface = font.render("item serial: " + str(self._actionList[self._replay_step].sourceSerial), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 60))
				text_surface = font.render("mobile serial: " + str(self._actionList[self._replay_step].targetSerial), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 80))
				text_surface = font.render("walk direction: " + str(self._actionList[self._replay_step].walkDirection), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 100))
				text_surface = font.render("index: " + str(self._actionList[self._replay_step].index), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 120))
				text_surface = font.render("amount: " + str(self._actionList[self._replay_step].amount), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 140))
				text_surface = font.render("run: " + str(self._actionList[self._replay_step].run), True, (255, 255, 255))
				self._screenSurface.blit(text_surface, (5, 160))

				## Draw the boundary line
				pygame.draw.line(self._screenSurface, (255, 255, 255), (1, 0), (1, self._screenHeight))
				pygame.draw.line(self._screenSurface, (255, 255, 255), (self._screenWidth - 1, 0), (self._screenWidth - 1, self._screenHeight))
				pygame.draw.line(self._screenSurface, (255, 255, 255), (0, self._screenHeight - 1), (self._screenWidth, self._screenHeight - 1))

				## Player status draw
				self._statusSurface.fill(((0, 0, 0)))
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Player Status", True, (255, 0, 255))
				self._statusSurface.blit(text_surface, (0, 0))
				for i, k in enumerate(self.player_status_dict):
					font = pygame.font.Font('freesansbold.ttf', 16)
					text_surface = font.render(str(k) + ": " + str(self.player_status_dict[k]), True, (255, 255, 255))
					self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

				## Player skill draw
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

				## Equipped item draw
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

				## Backpack item draw
				font = pygame.font.Font('freesansbold.ttf', 32)
				text_surface = font.render("Backpack Item", True, (255, 0, 255))
				self._equipItemSurface.blit(text_surface, (0, 400))
				for i, k in enumerate(self.backpack_item_dict):
					font = pygame.font.Font('freesansbold.ttf', 16)
					item = self.backpack_item_dict[k]
					text_surface = font.render(str(k) + ": " + str(item["name"]) + ", " + str(item["amount"]), True, (255, 255, 255))
					self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 420))

				## Draw each surface on root surface
				self._mainSurface.blit(self._screenSurface, (500, 0))
				self._mainSurface.blit(self._equipItemSurface, (500 + self._screenWidth, 0))
				#self._mainSurface.blit(self._npcSurface, (500, self._screenHeight))
				self._mainSurface.blit(self._statusSurface, (0, 0))
				
				self._step_box.draw(self._mainSurface)

				pygame.display.update()

	def InteractWithReplay(self):
		## Viewers can Forward and rewind the saved replay data by left and right arrow key
		self._replay_step = 0

		## Seperate thread for rendering data
		threading.Thread(target=self.rendering_data).start()

		## Start PyGame loop to interact with human
		while True:
			## Quit event check
			for event in pygame.event.get():
				 if event.type == pygame.QUIT:
					 running = False

				 self._step_box.handle_event(event)

			replay = self._step_box.update()

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
					self._previousControl = pygame.K_LEFT
				else:
					print("This is start of replay")
			elif keys[pygame.K_RIGHT]:
				## Same as left key part
				if self._previousControl == pygame.K_RIGHT:
					if self._tickScale < 100:
				  		self._tickScale += 1

				if self._replay_step < self._replayLength - 1:
					self._replay_step += 1
					self._previousControl = pygame.K_RIGHT
				else:
					print("This is end of replay")
			else:
				## Switch to slow replay mode when key input is not repeated
				self._previousControl = 0
				self._tickScale = 10

			## Create the downscaled array for bigger mobile object drawing
			screen_image = np.zeros((int((self._screenWidth + 100)), int((self._screenHeight + 100)), 3), dtype=np.uint8)
			if self._playerObjectList[self._replay_step].name != '':
				self.player_game_name = self._playerObjectList[self._replay_step].name
				self.player_serial = self._playerObjectList[self._replay_step].serial
				self.player_game_x = self._playerObjectList[self._replay_step].gameX
				self.player_game_y = self._playerObjectList[self._replay_step].gameY
				self.war_mode = self._playerObjectList[self._replay_step].warMode
				self.hold_item_serial = self._playerObjectList[self._replay_step].holdItemSerial
				self.targeting_state = self._playerObjectList[self._replay_step].targetingState
				self.min_tile_x = self._playerObjectList[self._replay_step].minTileX
				self.min_tile_y = self._playerObjectList[self._replay_step].minTileY
				self.max_tile_x = self._playerObjectList[self._replay_step].maxTileX
				self.max_tile_y = self._playerObjectList[self._replay_step].maxTileY
				#print("player_game_x: {0}, player_game_y: {1}: ", self.player_game_x, self.player_game_y)

			#popup_menu_data = self._popupMenuList[self._replay_step]
			#print("popup_menu_data: ", popup_menu_data)

			## Only increase the replay step when player in the world
			if self.player_game_name == None:
				self._replay_step += 1
				continue

			## Save the world item object into global Dict	
			if len(self._worldItemList[self._replay_step]) != 0:
				for obj in self._worldItemList[self._replay_step]:
					self.world_item_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
														 									 "distance": obj.distance, "layer":obj.layer, "container": obj.container, 
														 									 "isCorpse": obj.isCorpse, "amount": obj.amount }

					## Check the serial number of backpack container
					if obj.layer == 21:
						self.backpack_serial = obj.serial

					## Check the serial number of bank container
					if obj.layer == 29:
						self.bank_serial = obj.serial

			## Save the world mobile object into global Dict
			if len(self._worldMobileList[self._replay_step]) != 0:
				for obj in self._worldMobileList[self._replay_step]:
					self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
														   									 "distance": obj.distance, "title": obj.title, "hits": obj.hits,
														   									 "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
														   									 "race": obj.race }

			## Save the player status informaion into global Dict	
			if self._playerStatusList[self._replay_step].str != 0:
				self.player_status_dict = utils.parsePlayerStatus(self._playerStatusList[self._replay_step])

			## Save the player skills informaion into global Dict
			player_skills_data = self._playerSkillListList[self._replay_step]
			if len(player_skills_data) != 0:
				for skill in player_skills_data:
					self.player_skills_dict[skill.name] = {"index": skill.index, "isClickable": skill.isClickable, "value": skill.value, 
														   "base: ": skill.base, "cap": skill.cap, "lock": skill.lock}

			## Parse the backpack, equipped, corpse item from world item
			if len(self.world_item_dict) != 0 and self.backpack_serial != None:
				self.backpack_item_dict = {}
				self.equipped_item_dict = {}
				self.corpse_dict = {}
				for k, v in self.world_item_dict.items():
					## Corpse item
					if v["isCorpse"] == True:
						self.corpse_dict[k] = v

					## Backpack item
					if v["container"] == self.backpack_serial:
						self.backpack_item_dict[k] = v

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

			## Delete the item from world item Dict using the gRPC data
			if self.deleteItemSerialsArr is not None and len(self._deleteItemSerialsList[self._replay_step]) != 0:
				for serial in self._deleteItemSerialsList[self._replay_step]:
					if serial in self.world_item_dict:
						del self.world_item_dict[serial]

			## Delete the mobile from world mobile Dict using the gRPC data
			if self.deleteMobileSerialsArr is not None and len(self._deleteMobileSerialsList[self._replay_step]) != 0:
				for serial in self._deleteMobileSerialsList[self._replay_step]:
					if serial in self.world_mobile_dict:
						del self.world_mobile_dict[serial]

			# PyGame speed control
			self._clock.tick(self._tickScale)