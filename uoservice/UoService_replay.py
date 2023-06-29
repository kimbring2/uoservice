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
	def __init__(self, rootPath, screenWidth, screenHeight):
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
		self._clilocDataArrayOffset = 0

		self._playerStatusArrayOffset = 0
		self._playerSkillListArrayOffset = 0

		self._staticObjectInfoListArrayOffset = 0

		## Initialize the list to save the replay action data
		self._actionTypeList = []
		self._walkDirectionList = []
		self._mobileSerialList = []
		self._itemSerialList = []
		self._indexList = []
		self._amountList = []
		self._runList = []

		## Initialize the list to save the replay state data
		self._playerObjectList = []

		self._worldItemList = []
		self._worldMobileList = []

		self._popupMenuDataList = []
		self._clilocDataList = []

		self._playerStatusList = []
		self._playerSkillListList = []

		self._staticObjectScreenXsList = []
		self._staticObjectScreenYsList = []

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

		self.player_game_x = None
		self.player_game_y = None

		self.backpack_serial = None

		self.static_object_game_x_data = None
		self.static_object_game_y_data = None

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

		##  the length byte array for data array
		self.playerObjectArrayLengthArr = self._archive.read_file("replay.metadata.playerObjectLen");

		self.worldItemArrayLengthArr = self._archive.read_file("replay.metadata.worldItemLen");
		self.worldMobileArrayLengthArr = self._archive.read_file("replay.metadata.worldMobileLen");

		self.popupMenuArrayLengthArr = self._archive.read_file("replay.metadata.popupMenuLen");
		self.clilocDataArrayLengthArr = self._archive.read_file("replay.metadata.clilocDataLen");

		self.playerStatusArrayLengthArr = self._archive.read_file("replay.metadata.playerStatusLen");
		self.playerSkillListArrayLengthArr = self._archive.read_file("replay.metadata.playerSkillListLen");

		self.staticObjectInfoListLengthArr = self._archive.read_file("replay.metadata.staticObjectInfoListArraysLen");

		## Convert the byte array to int array
		self.playerObjectArrayLengthList = self.ConvertByteArrayToIntList(self.playerObjectArrayLengthArr);

		self.worldItemArrayLengthList = self.ConvertByteArrayToIntList(self.worldItemArrayLengthArr);
		self.worldMobileArrayLengthList = self.ConvertByteArrayToIntList(self.worldMobileArrayLengthArr);

		self.popupMenuArrayLengthList = self.ConvertByteArrayToIntList(self.popupMenuArrayLengthArr);
		self.clilocDataArrayLengthList = self.ConvertByteArrayToIntList(self.clilocDataArrayLengthArr);

		self.playerStatusArrayLengthList = self.ConvertByteArrayToIntList(self.playerStatusArrayLengthArr);
		self.playerSkillListArrayLengthList = self.ConvertByteArrayToIntList(self.playerSkillListArrayLengthArr);

		self.staticObjectInfoListLengthList = self.ConvertByteArrayToIntList(self.staticObjectInfoListLengthArr);

		## Find the total length of replay
		self._replayLength = len(self.playerObjectArrayLengthList)

		##  the actual data as byte array
		self.playerObjectArr = self._archive.read_file("replay.data.playerObject");

		self.worldItemArr = self._archive.read_file("replay.data.worldItems");
		self.worldMobileArr = self._archive.read_file("replay.data.worldMobiles");

		self.popupMenuArr = self._archive.read_file("replay.data.popupMenu");
		self.clilocDataArr = self._archive.read_file("replay.data.clilocData");

		self.playerStatusArr = self._archive.read_file("replay.data.playerStatus");
		self.playerSkillListArr = self._archive.read_file("replay.data.playerSkillList");

		self.staticObjectInfoListArr = self._archive.read_file("replay.data.staticObjectInfoList");

		##  the action data as byte array
		self.actionTypeArr = self._archive.read_file("replay.action.type");
		self.walkDirectionArr = self._archive.read_file("replay.action.walkDirection");
		self.mobileSerialArr = self._archive.read_file("replay.action.mobileSerial");
		self.itemSerialArr = self._archive.read_file("replay.action.itemSerial");
		self.indexArr = self._archive.read_file("replay.action.index");
		self.amountArr = self._archive.read_file("replay.action.amount");
		self.runArr = self._archive.read_file("replay.action.run");

		## Convert the byte array to int array
		self.actionTypeList = self.ConvertByteArrayToIntList(self.actionTypeArr);
		self.walkDirectionList = self.ConvertByteArrayToIntList(self.walkDirectionArr);
		self.mobileSerialList = self.ConvertByteArrayToIntList(self.mobileSerialArr);
		self.itemSerialList = self.ConvertByteArrayToIntList(self.itemSerialArr);
		self.indexList = self.ConvertByteArrayToIntList(self.indexArr);
		self.amountList = self.ConvertByteArrayToIntList(self.amountArr);
		self.runList = self.ConvertByteArrayToBoolList(self.runArr);

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

		if self.clilocDataArr:
			print("len(self.clilocDataArr): ", len(self.clilocDataArr))
		else:
			print("self.clilocDataArr is None")

		if self.playerStatusArr:
			print("len(self.playerStatusArr): ", len(self.playerStatusArr))
		else:
			print("self.playerStatusArr is None")

		if self.playerSkillListArr:
			print("len(self.playerSkillListArr): ", len(self.playerSkillListArr))
		else:
			print("self.playerSkillListArr is None")

		if self.staticObjectInfoListArr:
			print("len(self.staticObjectInfoListArr): ", len(self.staticObjectInfoListArr))
		else:
			print("self.staticObjectInfoListArr is None")

	def ParseReplay(self):
		# Saves the loaded replay data into Python list to visualize them one by one
		for step in range(0, self._replayLength):
			#print("step: ", step)

			self._actionTypeList.append(self.actionTypeList[step])
			self._walkDirectionList.append(self.walkDirectionList[step])
			self._mobileSerialList.append(self.mobileSerialList[step])
			self._itemSerialList.append(self.itemSerialList[step])
			self._indexList.append(self.indexList[step])
			self._amountList.append(self.amountList[step])
			self._runList.append(self.runList[step])

			if self.playerObjectArr:
				playerObjectSubsetArray, self._playerObjectArrayOffset = self.GetSubsetArray(step, self.playerObjectArrayLengthList, 
																				             self._playerObjectArrayOffset, 
																				             self.playerObjectArr)
				grpcPlayerObjectReplay = UoService_pb2.GrpcPlayerObject().FromString(playerObjectSubsetArray)
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
				self._worldMobileList.append(grpcWorldMobileReplay.mobileObjects)
			else:
				#print("worldMobileArr is None")
				pass

			if self.popupMenuArr:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthList, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArr)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				self._popupMenuDataList.append(grpcPopupMenuReplay.menus)
			else:
				#print("popupMenuArr is None")
				pass

			if self.clilocDataArr:
				clilocDataSubsetArray, self._clilocDataArrayOffset = self.GetSubsetArray(step, self.clilocDataArrayLengthList, 
																			   			 self._clilocDataArrayOffset, self.clilocDataArr)
				grpcClilocDataReplay = UoService_pb2.GrpcClilocDataList().FromString(clilocDataSubsetArray)
				self._clilocDataList.append(grpcClilocDataReplay.clilocDatas)
			else:
				pass
				#print("clilocDataArr is None")

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

			if self.staticObjectInfoListArr:
				staticObjectInfoListSubsetArrays, self._staticObjectInfoListArrayOffset = self.GetSubsetArray(step, self.staticObjectInfoListLengthList, 
																				   		   					  self._staticObjectInfoListArrayOffset, 
																				   		   					  self.staticObjectInfoListArr)
				grpcStaticObjectInfoListReplay = UoService_pb2.GrpcGameObjectInfoList().FromString(staticObjectInfoListSubsetArrays)
				self._staticObjectScreenXsList.append(grpcStaticObjectInfoListReplay.gameXs)
				self._staticObjectScreenYsList.append(grpcStaticObjectInfoListReplay.gameYs)
			else:
				pass
				#print("staticObjectInfoListArr is None")

		if len(self._playerObjectList) == 0:
			print("No playerObjectList")

		if len(self._worldItemList) == 0:
			print("No worldItemList")

		if len(self._worldMobileList) == 0:
			print("No worldMobileList")

		if len(self._popupMenuDataList) == 0:
			print("No popupMenuDataList")

		if len(self._clilocDataList) == 0:
			print("No clilocDataList")

		if len(self._playerStatusList) == 0:
			print("No playerStatusList")

		if len(self._playerSkillListList) == 0:
			print("No playerSkillListList")

		if len(self._staticObjectScreenXsList) == 0:
			print("No staticObjectScreenXsList")

		if len(self._staticObjectScreenYsList) == 0:
			print("No staticObjectScreenYsList")


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
			#screen_image = np.zeros((int((self._screenWidth + 100)), int((self._screenHeight + 100)), 3), dtype=np.uint8)
			screen_image = np.zeros((int((5000)), int((5000)), 3), dtype=np.uint8)

			if self._playerObjectList[replay_step].gameX != 0:
				#print("player_object: ", player_object)
				self.player_game_x = self._playerObjectList[replay_step].gameX
				self.player_game_y = self._playerObjectList[replay_step].gameY

			if len(self._worldMobileList[replay_step]) != 0:
				self.world_mobile_dict = {}
				for obj in self._worldMobileList[replay_step]:
					self.world_mobile_dict[obj.serial] = { "name": obj.name, "gameX": obj.gameX, "gameY":obj.gameY, 
														   "distance": obj.distance, "title": obj.title, "hits": obj.hits,
														   "notorietyFlag": obj.notorietyFlag, "hitsMax": obj.hitsMax,
														   "race": obj.race }

			# Draw the static object
			if len(self._staticObjectScreenXsList[replay_step]) != 0:
				self.static_object_game_x_data = self._staticObjectScreenXsList[replay_step]
				self.static_object_game_y_data = self._staticObjectScreenYsList[replay_step]

			radius = 2
			color = (120, 120, 120)
			thickness = 2
			if self.static_object_game_x_data != None:
				for i in range(0, len(self.static_object_game_x_data)):
					if self.static_object_game_x_data[i] >= 1400 or self.static_object_game_y_data[i] >= 1280:
						continue

					image = cv2.circle(screen_image, (self.static_object_game_x_data[i], self.static_object_game_y_data[i]), 
									   radius, color, thickness)
			
			print("self.player_game_x: {0}, self.player_game_y: {1}".format(self.player_game_x, self.player_game_y))
			#print("")

			radius = 20
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

			surf = pygame.surfarray.make_surface(screen_image)
			self._screenSurface.blit(surf, (0, 0))

			'''
			# Draw the player mobile object
			playerMobileObjectData = self._playerMobileObjectDataList[replay_step]
			#for obj in playerMobileObjectData:
			#	print("screenX: {0}, screenY: {1}".format(obj.screenX, obj.screenY))

			screen_image = utils.visObject(screen_image, self._playerMobileObjectDataList[replay_step], (0, 255, 0))
			for obj in self._playerMobileObjectDataList[replay_step]:
				#print("vendor_title: {0}, obj: {1}".format(vendor_title, obj))
				cv2.putText(screen_image, text=obj.name, org=(obj.screenX, obj.screenY),
			            	fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
			            	color=(200, 200, 0), thickness=2, lineType=cv2.LINE_4)

			# Draw the mobile object
			screen_image = utils.visObject(screen_image, self._mobileObjectDataList[replay_step], (0, 0, 255))

			# Draw the item object
			#screen_image = utils.visObject(screen_image, self._itemObjectDataList[replay_step], (255, 0, 0))

			for obj in self._mobileObjectDataList[replay_step]:
				vendor_title = utils.isVendor(obj.title)
				if vendor_title != None:
					#print("vendor_title: {0}, obj: {1}".format(vendor_title, obj))
					cv2.putText(screen_image, text=vendor_title, org=(obj.screenX, obj.screenY),
				            	fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
				            	color=(0, 200, 200), thickness=2, lineType=cv2.LINE_4)

			screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
			screen_image = cv2.flip(screen_image, 1)

			# Draw the screen image on the Pygame screen
			surf = pygame.surfarray.make_surface(screen_image)
			self._screenSurface.blit(surf, (0, 0))

			# Draw the replay step on the Pygame screen
			font = pygame.font.Font('freesansbold.ttf', 32)
			replay_step_surface = font.render("step: " + str(replay_step), True, (255, 255, 255))
			self._screenSurface.blit(replay_step_surface, (0, 0))

			#self._actionTypeList.append(self.actionTypeList[step])
			#self._walkDirectionList.append(self.walkDirectionList[step])
			#self._mobileSerialList.append(self.mobileSerialList[step])
			#self._itemSerialList.append(self.itemSerialList[step])
			#self._indexList.append(self.indexList[step])
			#self._amountList.append(self.amountList[step])

			# Player status draw
			self._statusSurface.fill(((0, 0, 0)))
			player_status_grpc = self._playerStatusList[replay_step]
			player_status_dict = utils.parsePlayerStatus(player_status_grpc)
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Player Status", True, (255, 0, 255))
			self._statusSurface.blit(text_surface, (0, 0))
			for i, k in enumerate(player_status_dict):
			  font = pygame.font.Font('freesansbold.ttf', 16)
			  text_surface = font.render(str(k) + ": " + str(player_status_dict[k]), True, (255, 255, 255))
			  self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Player Skills", True, (255, 0, 255))
			self._statusSurface.blit(text_surface, (0, 500))
			if len(self._playerSkillListList) > 0:
				playerSkillList = self._playerSkillListList[replay_step]
				for i, playerSkill in enumerate(playerSkillList):
					font = pygame.font.Font('freesansbold.ttf', 16)
					text_surface = font.render(str(playerSkill.index) + '. ' + str(playerSkill.name) + ": " + str(playerSkill.value), 
											   True, (255, 255, 255))
					self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 520))
					if playerSkill.index == 40:
						pass

			if len(self._openedCorpseList) > 0:
				openedCorpseList = self._openedCorpseList[replay_step]
				for openedCorpse in openedCorpseList:
					pass

			# Draw the action info on the Pygame screen
			font = pygame.font.Font('freesansbold.ttf', 16)
			text_surface = font.render("action type: " + str(self._actionTypeList[replay_step]), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 40))
			text_surface = font.render("walk direction: " + str(self._walkDirectionList[replay_step]), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 60))
			text_surface = font.render("run: " + str(self._runList[replay_step]), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 80))
			text_surface = font.render("index: " + str(self._indexList[replay_step]), True, (255, 255, 255))
			self._screenSurface.blit(text_surface, (5, 100))

			# Draw the boundary line
			pygame.draw.line(self._screenSurface, (255, 255, 255), (1, 0), (1, self._screenHeight))
			pygame.draw.line(self._screenSurface, (255, 255, 255), (self._screenWidth - 1, 0), (self._screenWidth - 1, self._screenHeight))
			pygame.draw.line(self._screenSurface, (255, 255, 255), (0, self._screenHeight - 1), (self._screenWidth, self._screenHeight - 1))

			# Equip item draw
			self._equipItemSurface.fill(((0, 0, 0)))
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Equip Items", True, (255, 0, 255))
			self._equipItemSurface.blit(text_surface, (0, 0))

			equippedItemList = self._equippedItemList[replay_step]
			print("equippedItemList: ", equippedItemList)

			# Backpack item draw
			backpack_item_grpc = self._backpackItemList[replay_step]
			backpack_item_dict = utils.parseItem(backpack_item_grpc)
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Backpack Item", True, (255, 0, 255))
			self._equipItemSurface.blit(text_surface, (0, 400))
			for i, k in enumerate(backpack_item_dict):
			  font = pygame.font.Font('freesansbold.ttf', 16)
			  item = backpack_item_dict[k]
			  text_surface = font.render(str(k) + ": " + str(item[0]) + ", " + str(item[1]), True, (255, 255, 255))
			  self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 420))

			# Vendor item draw
			#print("len(self._vendorItemDataList): ", len(self._vendorItemDataList))
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Vendor Item", True, (255, 0, 255))
			self._equipItemSurface.blit(text_surface, (0, 900))
			if len(self._vendorItemDataList) > 0:
				vendor_item_grpc = self._vendorItemDataList[replay_step]
				vendor_item_dict = utils.parseItem(vendor_item_grpc)
				for i, k in enumerate(vendor_item_dict):
				  font = pygame.font.Font('freesansbold.ttf', 16)
				  item = vendor_item_dict[k]
				  text_surface = font.render(str(k) + ": " + str(item[0]) + ", " + str(item[1]), True, (255, 255, 255))
				  self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 920))

			# Pop up menu draw
			self._npcSurface.fill(((0, 0, 0)))
			font = pygame.font.Font('freesansbold.ttf', 32)
			text_surface = font.render("Pop Up Menu", True, (255, 0, 255))
			self._npcSurface.blit(text_surface, (0, 0))
			if len(self._popupMenuDataList) > 0:
				for i, menu in enumerate(self._popupMenuDataList[replay_step]):
				  font = pygame.font.Font('freesansbold.ttf', 16)
				  text_surface = font.render(str(i) + ": " + str(menu), True, (255, 255, 255))
				  self._npcSurface.blit(text_surface, (0, 20 * (i + 1) + 20))
			'''

			# Draw each surface on root surface
			self._mainSurface.blit(self._screenSurface, (500, 0))

			#self._mainSurface.blit(self._equipItemSurface, (500 + self._screenWidth, 0))
			#self._mainSurface.blit(self._npcSurface, (500, self._screenHeight))
			#self._mainSurface.blit(self._statusSurface, (0, 0))
			
			pygame.display.update()

			# Wait little bit
			#print("self._tickScale: ", self._tickScale)
			self._clock.tick(self._tickScale)