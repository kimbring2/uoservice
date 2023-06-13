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
import UoService_pb2
import UoService_pb2_grpc
import utils
 

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

		self._equippedItemArrayOffset = 0
		self._backpackItemArrayOffset = 0
		self._openedCorpseArrayOffset = 0
		self._popupMenuArrayOffset = 0
		self._clilocDataArrayOffset = 0

		self._playerMobileObjectArrayOffset = 0
		self._mobileObjectArrayOffset = 0
		self._itemObjectArrayOffset = 0
		self._itemDropableLandArrayOffset = 0
		self._vendorItemObjectArrayOffset = 0

		self._playerStatusArrayOffset = 0
		self._playerSkillListArrayOffset = 0

		self._staticObjectInfoListArrayOffset = 0

		self._actionTypeList = []
		self._walkDirectionList = []
		self._mobileSerialList = []
		self._itemSerialList = []
		self._indexList = []
		self._amountList = []
		self._runList = []

		self._playerMobileObjectDataList = []
		self._mobileObjectDataList = []
		self._itemObjectDataList = []
		self._staticObjectScreenXsList = []
		self._staticObjectScreenYsList = []
		self._itemDropableLandObjectList = []
		self._equippedItemList = []
		self._backpackItemList = []
		self._popupMenuDataList = []
		self._openedCorpseList = []
		self._vendorItemDataList = []
		self._clilocDataList = []
		self._playerStatusList = []
		self._playerSkillListList = []

		self._screenWidth = screenWidth
		self._screenHeight = screenHeight

		self._mainSurface = pygame.display.set_mode([500 + self._screenWidth + 500, self._screenHeight + 350])
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight))
		self._equipItemSurface = pygame.Surface((500, self._screenHeight))
		self._npcSurface = pygame.Surface((self._screenWidth, 350))
		self._statusSurface = pygame.Surface((500, self._screenHeight))

		self._clock = pygame.time.Clock()

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

	def GetSubsetArray(self, index, lengthListRead, offset, arrRead):
		# Crop the part of array when the length is variable. Return the modifed offset value for next cropping.
		item = lengthListRead[index]
		startIndex = offset
		subsetArray = arrRead[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def GetSubsetArrayFix(self, index, lengthRead, offset, arrRead):
		# Crop the part of array when the length is fixed. Return the modifed offset value for next cropping.
		item = lengthRead
		startIndex = offset
		subsetArray = arrRead[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def ReadReplay(self, fileName):
		# Read the original data files and length metadata files for them from MPQ file
		self._archive = MPQArchive(self._rootPath + '/' + fileName + ".uoreplay")

		## Read the length byte array for data array
		self.equippedItemArrayLengthArrRead = self._archive.read_file("replay.metadata.equippedItemLen");
		self.backpackItemArrayLengthArrRead = self._archive.read_file("replay.metadata.backpackitemLen");
		self.openedCorpseArrayLengthArrRead = self._archive.read_file("replay.metadata.openedCorpseLen");
		self.popupMenuArrayLengthArrRead = self._archive.read_file("replay.metadata.popupMenuLen");
		self.clilocDataArrayLengthArrRead = self._archive.read_file("replay.metadata.clilocDataLen");
		self.playerMobileObjectArrayLengthArrRead = self._archive.read_file("replay.metadata.playerMobileObjectLen");
		self.mobileObjectArrayLengthArrRead = self._archive.read_file("replay.metadata.mobileObjectLen");
		self.itemObjectArrayLengthArrRead = self._archive.read_file("replay.metadata.itemObjectLen");
		self.itemDropableLandArrayLengthArrRead = self._archive.read_file("replay.metadata.itemDropableLandSimpleLen");
		self.vendorItemObjectArrayLengthArrRead = self._archive.read_file("replay.metadata.vendorItemObjectLen");
		self.playerStatusZeroLenStepArrRead = self._archive.read_file("replay.metadata.playerStatusZeroLenStep");
		self.playerSkillListArrayLengthArrRead = self._archive.read_file("replay.metadata.playerSkillListLen");
		self.staticObjectInfoListLengthArrRead = self._archive.read_file("replay.metadata.staticObjectInfoListArraysLen");

		## Convert the byte array to int array
		self.equippedItemArrayLengthListRead = self.ConvertByteArrayToIntList(self.equippedItemArrayLengthArrRead);
		self.backpackItemArrayLengthListRead = self.ConvertByteArrayToIntList(self.backpackItemArrayLengthArrRead);
		self.openedCorpseArrayLengthListRead = self.ConvertByteArrayToIntList(self.openedCorpseArrayLengthArrRead);
		self.popupMenuArrayLengthListRead = self.ConvertByteArrayToIntList(self.popupMenuArrayLengthArrRead);
		self.clilocDataArrayLengthListRead = self.ConvertByteArrayToIntList(self.clilocDataArrayLengthArrRead);
		self.playerMobileObjectArrayLengthListRead = self.ConvertByteArrayToIntList(self.playerMobileObjectArrayLengthArrRead);
		self.mobileObjectArrayLengthListRead = self.ConvertByteArrayToIntList(self.mobileObjectArrayLengthArrRead);
		self.itemObjectArrayLengthListRead = self.ConvertByteArrayToIntList(self.itemObjectArrayLengthArrRead);
		self.itemDropableLandArrayLengthListRead = self.ConvertByteArrayToIntList(self.itemDropableLandArrayLengthArrRead);
		self.vendorItemObjectArrayLengthListRead = self.ConvertByteArrayToIntList(self.vendorItemObjectArrayLengthArrRead);
		self.playerStatusZeroLenStepListRead = self.ConvertByteArrayToIntList(self.playerStatusZeroLenStepArrRead);
		self.playerSkillListArrayLengthListRead = self.ConvertByteArrayToIntList(self.playerSkillListArrayLengthArrRead);
		self.staticObjectInfoListLengthListRead = self.ConvertByteArrayToIntList(self.staticObjectInfoListLengthArrRead);

		self._replayLength = len(self.equippedItemArrayLengthListRead)

		## Read the actual data as byte array
		self.equippedItemArrRead = self._archive.read_file("replay.data.equippedItem");
		self.backpackItemArrRead = self._archive.read_file("replay.data.backpackItem");
		self.openedCorpseArrRead = self._archive.read_file("replay.data.openedCorpse");
		self.popupMenuArrRead = self._archive.read_file("replay.data.popupMenu");
		self.clilocDataArrRead = self._archive.read_file("replay.data.clilocData");
		self.playerMobileObjectArrRead = self._archive.read_file("replay.data.playerMobileObject");
		self.mobileObjectArrRead = self._archive.read_file("replay.data.mobileObject");
		self.itemObjectArrRead = self._archive.read_file("replay.data.itemObject");
		self.itemDropableLandArrRead = self._archive.read_file("replay.data.itemDropableLandSimple");
		self.vendorItemObjectArrRead = self._archive.read_file("replay.data.vendorItemObject");
		self.playerStatusArrRead = self._archive.read_file("replay.data.playerStatus");
		self.playerSkillListArrRead = self._archive.read_file("replay.data.playerSkillList");
		self.staticObjectInfoListArrRead = self._archive.read_file("replay.data.staticObjectInfoList");

		## Read the action data as byte array
		self.actionTypeArrRead = self._archive.read_file("replay.action.type");
		self.walkDirectionArrRead = self._archive.read_file("replay.action.walkDirection");
		self.mobileSerialArrRead = self._archive.read_file("replay.action.mobileSerial");
		self.itemSerialArrRead = self._archive.read_file("replay.action.itemSerial");
		self.indexArrRead = self._archive.read_file("replay.action.index");
		self.amountArrRead = self._archive.read_file("replay.action.amount");
		self.runArrRead = self._archive.read_file("replay.action.run");

		## Convert the byte array to int array
		self.actionTypeListRead = self.ConvertByteArrayToIntList(self.actionTypeArrRead);
		self.walkDirectionListRead = self.ConvertByteArrayToIntList(self.walkDirectionArrRead);
		self.mobileSerialListRead = self.ConvertByteArrayToIntList(self.mobileSerialArrRead);
		self.itemSerialListRead = self.ConvertByteArrayToIntList(self.itemSerialArrRead);
		self.indexListRead = self.ConvertByteArrayToIntList(self.indexArrRead);
		self.amountListRead = self.ConvertByteArrayToIntList(self.amountArrRead);
		self.runListRead = self.ConvertByteArrayToBoolList(self.runArrRead);

		## Check the data array is existed
		if self.equippedItemArrRead:
			print("len(self.equippedItemArrRead): ", len(self.equippedItemArrRead))
		else:
			print("self.equippedItemArrRead is None")

		if self.backpackItemArrRead:
			print("len(backpackItemArrRead): ", len(self.backpackItemArrRead))
		else:
			print("backpackItemArrRead is None")

		if self.openedCorpseArrRead:
			print("len(openedCorpseArrRead): ", len(self.openedCorpseArrRead))
		else:
			print("openedCorpseArrRead is None")

		if self.popupMenuArrRead:
			print("len(popupMenuArrRead): ", len(self.popupMenuArrRead))
		else:
			print("popupMenuArrRead is None")

		if self.clilocDataArrRead:
			print("len(self.clilocDataArrRead): ", len(self.clilocDataArrRead))
		else:
			print("self.clilocDataArrRead is None")

		if self.playerMobileObjectArrRead:
			print("len(self.playerMobileObjectArrRead): ", len(self.playerMobileObjectArrRead))
		else:
			print("self.playerMobileObjectArrRead is None")

		if self.mobileObjectArrRead:
			print("len(self.mobileObjectArrRead): ", len(self.mobileObjectArrRead))
		else:
			print("self.mobileObjectArrRead is None")

		if self.itemObjectArrRead:
			print("len(self.itemObjectArrRead): ", len(self.itemObjectArrRead))
		else:
			print("self.itemObjectArrRead is None")

		if self.itemDropableLandArrRead:
			print("len(self.itemDropableLandArrRead): ", len(self.itemDropableLandArrRead))
		else:
			print("self.itemDropableLandArrRead is None")

		if self.vendorItemObjectArrRead:
			print("len(self.vendorItemObjectArrRead): ", len(self.vendorItemObjectArrRead))
		else:
			print("self.vendorItemObjectArrRead is None")

		if self.playerStatusArrRead:
			print("len(self.playerStatusArrRead): ", len(self.playerStatusArrRead))
		else:
			print("self.playerStatusArrRead is None")

		if self.playerSkillListArrRead:
			print("len(self.playerSkillListArrRead): ", len(self.playerSkillListArrRead))
		else:
			print("self.playerSkillListArrRead is None")

		if self.staticObjectInfoListArrRead:
			print("len(self.staticObjectInfoListArrRead): ", len(self.staticObjectInfoListArrRead))
		else:
			print("self.staticObjectInfoListArrRead is None")

	def ParseReplay(self):
		# Saves the loaded replay data into Python list to visualize them one by one
		for step in range(0, self._replayLength):
			print("step: ", step)

			self._actionTypeList.append(self.actionTypeListRead[step])
			self._walkDirectionList.append(self.walkDirectionListRead[step])
			self._mobileSerialList.append(self.mobileSerialListRead[step])
			self._itemSerialList.append(self.itemSerialListRead[step])
			self._indexList.append(self.indexListRead[step])
			self._amountList.append(self.amountListRead[step])
			self._runList.append(self.runListRead[step])

			if self.equippedItemArrRead:
				equippedItemSubsetArray, self._equippedItemArrayOffset = self.GetSubsetArray(step, self.equippedItemArrayLengthListRead, 
																				   self._equippedItemArrayOffset, self.equippedItemArrRead)
				grpcEquippedItemReplay = UoService_pb2.GrpcItemList().FromString(equippedItemSubsetArray)
				#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
				self._equippedItemList.append(grpcEquippedItemReplay.items)
			else:
				print("equippedItemArrRead is None")

			if self.backpackItemArrRead:
				backpackItemSubsetArray, self._backpackItemArrayOffset = self.GetSubsetArray(step, self.backpackItemArrayLengthListRead, 
																				  self._backpackItemArrayOffset, self.backpackItemArrRead)
				grpcBackpackItemReplay = UoService_pb2.GrpcItemList().FromString(backpackItemSubsetArray)
				#print("grpcBackpackItemReplay: ", grpcBackpackItemReplay)
				self._backpackItemList.append(grpcBackpackItemReplay.items)
			else:
				print("backpackItemArrRead is None")

			if self.playerMobileObjectArrRead:
				playerMobileObjectSubsetArray, self._playerMobileObjectArrayOffset = self.GetSubsetArray(step, self.playerMobileObjectArrayLengthListRead, 
																				  			   self._playerMobileObjectArrayOffset, self.playerMobileObjectArrRead)
				grpcPlayerMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(playerMobileObjectSubsetArray)
				#print("grpcPlayerMobileObjectReplay: ", grpcPlayerMobileObjectReplay)
				self._playerMobileObjectDataList.append(grpcPlayerMobileObjectReplay.gameObjects)
			else:
				print("playerMobileObjectArrRead is None")

			if self.mobileObjectArrRead:
				mobileObjectSubsetArray, self._mobileObjectArrayOffset = self.GetSubsetArray(step, self.mobileObjectArrayLengthListRead, 
																				   self._mobileObjectArrayOffset, self.mobileObjectArrRead)
				grpcMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(mobileObjectSubsetArray)
				#print("grpcMobileObjectReplay: ", grpcMobileObjectReplay)
				self._mobileObjectDataList.append(grpcMobileObjectReplay.gameObjects)
			else:
				print("mobileObjectArrRead is None")

			if self.staticObjectInfoListArrRead:
				staticObjectInfoListSubsetArrays, self._staticObjectInfoListArrayOffset = self.GetSubsetArray(step, self.staticObjectInfoListLengthListRead, 
																				   		   			self._staticObjectInfoListArrayOffset, self.staticObjectInfoListArrRead)
				grpcStaticObjectInfoListReplay = UoService_pb2.GrpcGameObjectInfoList().FromString(staticObjectInfoListSubsetArrays)
				#print("grpcStaticObjectInfoListReplay.screenXs: ", grpcStaticObjectInfoListReplay.screenXs)
				#print("grpcStaticObjectInfoListReplay.screenYs: ", grpcStaticObjectInfoListReplay.screenYs)
				self._staticObjectScreenXsList.append(grpcStaticObjectInfoListReplay.screenXs)
				self._staticObjectScreenYsList.append(grpcStaticObjectInfoListReplay.screenYs)

			else:
				print("staticObjectInfoListArrRead is None")
			
			if step not in self.playerStatusZeroLenStepListRead:
				if self.playerStatusArrRead:
					playerStatusSubsetArray, self._playerStatusArrayOffset = self.GetSubsetArrayFix(step, 30, self._playerStatusArrayOffset, 
																									self.playerStatusArrRead)
					grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
					#print("grpcPlayerStatusReplay: ", grpcPlayerStatusReplay)
					self._playerStatusList.append(grpcPlayerStatusReplay)
				else:
					print("playerStatusArrRead is None")

			if self.playerSkillListArrRead:
				playerSkillListSubsetArray, self._playerSkillListArrayOffset = self.GetSubsetArray(step, self.playerSkillListArrayLengthListRead, 
																				   		 		   self._playerSkillListArrayOffset, self.playerSkillListArrRead)
				grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray)
				#print("grpcPlayerSkillListReplay: ", grpcPlayerSkillListReplay)
				self._playerSkillListList.append(grpcPlayerSkillListReplay.skills)
			else:
				print("playerSkillListArrRead is None")

			if self.openedCorpseArrRead:
				openedCorpseSubsetArray, self._openedCorpseArrayOffset = self.GetSubsetArray(step, self.openedCorpseArrayLengthListRead, 
																			   				 self._openedCorpseArrayOffset, self.openedCorpseArrRead)
				grpcOpenedCorpseReplay = UoService_pb2.GrpcContainerDataList().FromString(openedCorpseSubsetArray)
				#print("grpcOpenedCorpseReplay: ", grpcOpenedCorpseReplay)
				self._openedCorpseList.append(grpcOpenedCorpseReplay.containers)
			else:
				print("openedCorpseArrRead is None")

			if self.itemObjectArrRead:
				itemObjectSubsetArray, self._itemObjectArrayOffset = self.GetSubsetArray(step, self.itemObjectArrayLengthListRead, 
																			   			 self._itemObjectArrayOffset, self.itemObjectArrRead)
				grpcItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(itemObjectSubsetArray)
				#print("grpcItemObjectReplay: ", grpcItemObjectReplay)
				self._itemObjectDataList.append(grpcItemObjectReplay.gameObjects)
			else:
				print("itemObjectArrRead is None")

			if self.itemDropableLandArrRead:
				itemDropableLandSubsetArray, self._itemDropableLandArrayOffset = self.GetSubsetArray(step, self.itemDropableLandArrayLengthListRead, 
																			   			   			 self._itemDropableLandArrayOffset, self.itemDropableLandArrRead)
				grpcItemDropableLandReplay = UoService_pb2.GrpcGameObjectSimpleList().FromString(itemDropableLandSubsetArray)
				#print("grpcItemDropableLandReplay: ", grpcItemDropableLandReplay)
				self._itemDropableLandObjectList.append(grpcItemDropableLandReplay.gameSimpleObjects)
			else:
				print("itemDropableLandArrRead is None")

			if self.popupMenuArrRead:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthListRead, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArrRead)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				#print("grpcPopupMenuReplay: ", grpcPopupMenuReplay)
				self._popupMenuDataList.append(grpcPopupMenuReplay.menus)
			else:
				print("popupMenuArrRead is None")

			if self.vendorItemObjectArrRead:
				vendorItemObjectSubsetArray, self._vendorItemObjectArrayOffset = self.GetSubsetArray(step, self.vendorItemObjectArrayLengthListRead, 
																			 			   			 self._vendorItemObjectArrayOffset, self.vendorItemObjectArrRead)
				grpcVendorItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(vendorItemObjectSubsetArray)
				#print("grpcVendorItemObjectReplay: ", grpcVendorItemObjectReplay)
				self._vendorItemDataList.append(grpcVendorItemObjectReplay.gameObjects)
			else:
				print("vendorItemObjectArrRead is None")

			if self.clilocDataArrRead:
				clilocDataSubsetArray, self._clilocDataArrayOffset = self.GetSubsetArray(step, self.clilocDataArrayLengthListRead, 
																			   			 self._clilocDataArrayOffset, self.clilocDataArrRead)
				grpcClilocDataReplay = UoService_pb2.GrpcClilocDataList().FromString(clilocDataSubsetArray)
				#print("grpcClilocDataReplay: ", grpcClilocDataReplay)
				self._clilocDataList.append(grpcClilocDataReplay.clilocDatas)
			else:
				print("clilocDataArrRead is None")

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
					if self._tickScale < 60:
				  		self._tickScale += 1

				if replay_step >= 1:
					replay_step -= 1
					self._previousControl = pygame.K_LEFT
					#print("replay_step: ", replay_step)
				else:
					print("This is start of replay")
			elif keys[pygame.K_RIGHT]:
				if self._previousControl == pygame.K_RIGHT:
					if self._tickScale < 60:
				  		self._tickScale += 1

				if replay_step < self._replayLength - 1:
					replay_step += 1
					self._previousControl = pygame.K_RIGHT
					#print("replay_step: ", replay_step)
				else:
					print("This is end of replay")
			else:
				self._previousControl = 0
				self._tickScale = 10

			# Create the downscaled array for bigger mobile object drawing
			screen_image = np.zeros((int((self._screenWidth + 100)), int((self._screenHeight + 100)), 3), dtype=np.uint8)

			# Draw the static object
			static_object_screen_x_data = self._staticObjectScreenXsList[replay_step]
			static_object_screen_y_data = self._staticObjectScreenYsList[replay_step]

			radius = 1
			color = (120, 120, 120)
			thickness = 2
			for i in range(0, len(static_object_screen_x_data)):
				if static_object_screen_x_data[i] >= 1400 or static_object_screen_y_data[i] >= 1280:
					continue

				image = cv2.circle(screen_image, (static_object_screen_x_data[i], static_object_screen_y_data[i]), 
								   radius, color, thickness)

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
			#screen_image = utils.visObject(screen_image, self._itemObjectDataList[replay_step], (0, 0, 255))

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

			#self._actionTypeList.append(self.actionTypeListRead[step])
			#self._walkDirectionList.append(self.walkDirectionListRead[step])
			#self._mobileSerialList.append(self.mobileSerialListRead[step])
			#self._itemSerialList.append(self.itemSerialListRead[step])
			#self._indexList.append(self.indexListRead[step])
			#self._amountList.append(self.amountListRead[step])

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
			for i, equipped_item in enumerate(self._equippedItemList[replay_step]):
			  font = pygame.font.Font('freesansbold.ttf', 20)
			  text_surface = font.render(str(Layers(int(equipped_item.layer)).name) + ": " + str(equipped_item.name), True, (255, 255, 255))
			  self._equipItemSurface.blit(text_surface, (0, 25 * (i + 1) + 20))

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

			# Draw each surface on root surface
			self._mainSurface.blit(self._screenSurface, (500, 0))
			self._mainSurface.blit(self._equipItemSurface, (500 + self._screenWidth, 0))
			self._mainSurface.blit(self._npcSurface, (500, self._screenHeight))
			self._mainSurface.blit(self._statusSurface, (0, 0))
			pygame.display.update()

			# Wait little bit
			#print("self._tickScale: ", self._tickScale)
			self._clock.tick(self._tickScale)