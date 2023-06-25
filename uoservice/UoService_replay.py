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

		## 
		self._worldItemArrayOffset = 0
		self._worldMobileArrayOffset = 0

		self._equippedItemSerialArrayOffset = 0
		self._backpackItemSerialArrayOffset = 0
		self._bankItemSerialArrayOffset = 0
		self._vendorItemSerialArrayOffset = 0

		self._openedCorpseArrayOffset = 0
		self._popupMenuArrayOffset = 0
		self._clilocDataArrayOffset = 0

		self._sceneMobileObjectSerialArrayOffset = 0
		self._sceneItemObjectSerialArrayOffset = 0

		self._playerStatusArrayOffset = 0
		self._playerStatusEtcArrayOffset = 0
		self._playerSkillListArrayOffset = 0

		self._staticObjectInfoListArrayOffset = 0

		## 
		self._actionTypeList = []
		self._walkDirectionList = []
		self._mobileSerialList = []
		self._itemSerialList = []
		self._indexList = []
		self._amountList = []
		self._runList = []

		## 
		self._worldItemList = []
		self._worldMobileList = []

		self._equippedItemSerialList = []
		self._backpackItemSerialList = []
		self._bankItemSerialList = []
		self._vendorItemSerialList = []

		self._popupMenuDataList = []
		self._openedCorpseList = []
		self._clilocDataList = []

		self._sceneMobileObjectSerialList = []
		self._sceneItemObjectSerialList = []

		self._playerStatusList = []
		self._playerStatusEtcList = []
		self._playerSkillListList = []

		self._staticObjectScreenXsList = []
		self._staticObjectScreenYsList = []

		## 
		self._screenWidth = screenWidth
		self._screenHeight = screenHeight

		self._mainSurface = pygame.display.set_mode([500 + self._screenWidth + 500, self._screenHeight + 350])
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight))
		self._equipItemSurface = pygame.Surface((500, self._screenHeight))
		self._npcSurface = pygame.Surface((self._screenWidth, 350))
		self._statusSurface = pygame.Surface((500, self._screenHeight))

		self._clock = pygame.time.Clock()

		## Global replay data
		self.world_item_dict = {}
		self.world_mobile_dict = {}
		self.player_skills_dict = {}
		self.player_status_dict = {}

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
		self.worldItemArrayLengthArr = self._archive.read_file("replay.metadata.worldItemLen");
		self.worldMobileArrayLengthArr = self._archive.read_file("replay.metadata.worldMobileLen");

		self.equippedItemSerialArrayLengthArr = self._archive.read_file("replay.metadata.equippedItemSerialLen");
		self.backpackItemSerialArrayLengthArr = self._archive.read_file("replay.metadata.backpackitemSerialLen");
		self.bankItemSerialArrayLengthArr = self._archive.read_file("replay.metadata.bankitemSerialLen");
		self.vendorItemSerialArrayLengthArr = self._archive.read_file("replay.metadata.vendorItemSerialLen");

		self.openedCorpseArrayLengthArr = self._archive.read_file("replay.metadata.openedCorpseLen");
		self.popupMenuArrayLengthArr = self._archive.read_file("replay.metadata.popupMenuLen");
		self.clilocDataArrayLengthArr = self._archive.read_file("replay.metadata.clilocDataLen");

		self.sceneMobileObjectSerialArrayLengthArr = self._archive.read_file("replay.metadata.sceneMobileSerialLen");
		self.sceneItemObjectSerialArrayLengthArr = self._archive.read_file("replay.metadata.sceneItemSerialLen");

		self.playerStatusArrayLengthArr = self._archive.read_file("replay.metadata.playerStatusLen");
		self.playerStatusEtcArrayLengthArr = self._archive.read_file("replay.metadata.playerStatusEtcLen");
		self.playerSkillListArrayLengthArr = self._archive.read_file("replay.metadata.playerSkillListLen");

		self.staticObjectInfoListLengthArr = self._archive.read_file("replay.metadata.staticObjectInfoListArraysLen");

		## Convert the byte array to int array
		self.worldItemArrayLengthList = self.ConvertByteArrayToIntList(self.worldItemArrayLengthArr);
		self.worldMobileArrayLengthList = self.ConvertByteArrayToIntList(self.worldMobileArrayLengthArr);

		self.equippedItemSerialArrayLengthList = self.ConvertByteArrayToIntList(self.equippedItemSerialArrayLengthArr);
		self.backpackItemSerialArrayLengthList = self.ConvertByteArrayToIntList(self.backpackItemSerialArrayLengthArr);
		self.bankItemSerialArrayLengthList = self.ConvertByteArrayToIntList(self.bankItemSerialArrayLengthArr);
		self.vendorItemSerialArrayLengthList = self.ConvertByteArrayToIntList(self.vendorItemSerialArrayLengthArr);

		self.openedCorpseArrayLengthList = self.ConvertByteArrayToIntList(self.openedCorpseArrayLengthArr);
		self.popupMenuArrayLengthList = self.ConvertByteArrayToIntList(self.popupMenuArrayLengthArr);
		self.clilocDataArrayLengthList = self.ConvertByteArrayToIntList(self.clilocDataArrayLengthArr);

		self.sceneMobileObjectSerialArrayLengthList = self.ConvertByteArrayToIntList(self.sceneMobileObjectSerialArrayLengthArr);
		self.sceneItemObjectSerialArrayLengthList = self.ConvertByteArrayToIntList(self.sceneItemObjectSerialArrayLengthArr);

		self.playerStatusArrayLengthList = self.ConvertByteArrayToIntList(self.playerStatusArrayLengthArr);
		self.playerStatusEtcArrayLengthList = self.ConvertByteArrayToIntList(self.playerStatusEtcArrayLengthArr);
		self.playerSkillListArrayLengthList = self.ConvertByteArrayToIntList(self.playerSkillListArrayLengthArr);

		self.staticObjectInfoListLengthList = self.ConvertByteArrayToIntList(self.staticObjectInfoListLengthArr);

		## Find the total length of replay
		self._replayLength = len(self.equippedItemSerialArrayLengthList)

		##  the actual data as byte array
		self.worldItemArr = self._archive.read_file("replay.data.worldItems");
		self.worldMobileArr = self._archive.read_file("replay.data.worldMobiles");

		self.equippedItemSerialArr = self._archive.read_file("replay.data.equippedItemSerials");
		self.backpackItemSerialArr = self._archive.read_file("replay.data.backpackItemSerials");
		self.bankItemSerialArr = self._archive.read_file("replay.data.bankItemSerials");
		self.vendorItemSerialArr = self._archive.read_file("replay.data.vendorItemSerials");

		self.openedCorpseArr = self._archive.read_file("replay.data.openedCorpse");
		self.popupMenuArr = self._archive.read_file("replay.data.popupMenu");
		self.clilocDataArr = self._archive.read_file("replay.data.clilocData");

		self.sceneMobileObjectSerialArr = self._archive.read_file("replay.data.sceneMobileObjectSerials");
		self.sceneItemObjectSerialArr = self._archive.read_file("replay.data.sceneItemObjectSerials");

		self.playerStatusArr = self._archive.read_file("replay.data.playerStatus");
		self.playerStatusEtcArr = self._archive.read_file("replay.data.playerStatusEtc");
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
		if self.worldItemArr:
			print("len(self.worldItemArr): ", len(self.worldItemArr))
		else:
			print("self.worldItemArr is None")

		if self.worldMobileArr:
			print("len(self.worldMobileArr): ", len(self.worldMobileArr))
		else:
			print("self.worldMobileArr is None")

		if self.equippedItemSerialArr:
			print("len(self.equippedItemSerialArr): ", len(self.equippedItemSerialArr))
		else:
			print("self.equippedItemSerialArr is None")

		if self.backpackItemSerialArr:
			print("len(backpackItemSerialArr): ", len(self.backpackItemSerialArr))
		else:
			print("backpackItemSerialArr is None")

		if self.bankItemSerialArr:
			print("len(bankItemSerialArr): ", len(self.bankItemSerialArr))
		else:
			print("bankItemSerialArr is None")

		if self.vendorItemSerialArr:
			print("len(self.vendorItemSerialArr): ", len(self.vendorItemSerialArr))
		else:
			print("self.vendorItemSerialArr is None")

		if self.openedCorpseArr:
			print("len(openedCorpseArr): ", len(self.openedCorpseArr))
		else:
			print("openedCorpseArr is None")

		if self.popupMenuArr:
			print("len(popupMenuArr): ", len(self.popupMenuArr))
		else:
			print("popupMenuArr is None")

		if self.clilocDataArr:
			print("len(self.clilocDataArr): ", len(self.clilocDataArr))
		else:
			print("self.clilocDataArr is None")

		if self.sceneMobileObjectSerialArr:
			print("len(self.sceneMobileObjectSerialArr): ", len(self.sceneMobileObjectSerialArr))
		else:
			print("self.sceneMobileSerialArr is None")

		if self.sceneItemObjectSerialArr:
			print("len(self.sceneItemObjectSerialArr): ", len(self.sceneItemObjectSerialArr))
		else:
			print("self.sceneItemObjectSerialArr is None")

		if self.playerStatusArr:
			print("len(self.playerStatusArr): ", len(self.playerStatusArr))
		else:
			print("self.playerStatusArr is None")

		if self.playerStatusEtcArr:
			print("len(self.playerStatusEtcArr): ", len(self.playerStatusEtcArr))
		else:
			print("self.playerStatusEtcArr is None")

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
			print("step: ", step)

			self._actionTypeList.append(self.actionTypeList[step])
			self._walkDirectionList.append(self.walkDirectionList[step])
			self._mobileSerialList.append(self.mobileSerialList[step])
			self._itemSerialList.append(self.itemSerialList[step])
			self._indexList.append(self.indexList[step])
			self._amountList.append(self.amountList[step])
			self._runList.append(self.runList[step])

			if self.worldItemArr:
				worldItemSubsetArray, self._worldItemArrayOffset = self.GetSubsetArray(step, self.worldItemArrayLengthList, 
																				       self._worldItemArrayOffset, self.worldItemArr)
				grpcWorldItemReplay = UoService_pb2.GrpcGameObjectList().FromString(worldItemSubsetArray)
				#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
				self._worldItemList.append(grpcWorldItemReplay.gameObjects)
			else:
				print("worldItemArr is None")

			if self.worldMobileArr:
				worldMobileSubsetArray, self._worldMobileArrayOffset = self.GetSubsetArray(step, self.worldMobileArrayLengthList, 
																				           self._worldMobileArrayOffset, self.worldMobileArr)
				grpcWorldMobileReplay = UoService_pb2.GrpcGameObjectList().FromString(worldMobileSubsetArray)
				#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
				self._worldMobileList.append(grpcWorldMobileReplay.gameObjects)
			else:
				print("worldMobileArr is None")

			if self.equippedItemSerialArr:
				equippedItemSerialSubsetArray, self._equippedItemSerialArrayOffset = self.GetSubsetArray(step, self.equippedItemSerialArrayLengthList, 
																				   self._equippedItemSerialArrayOffset, self.equippedItemSerialArr)
				grpcEquippedItemSerialReplay = UoService_pb2.GrpcSerialList().FromString(equippedItemSerialSubsetArray)
				#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
				self._equippedItemSerialList.append(grpcEquippedItemSerialReplay.serials)
			else:
				print("equippedItemSerialArr is None")

			if self.backpackItemSerialArr:
				backpackItemSerialSubsetArray, self._backpackItemSerialArrayOffset = self.GetSubsetArray(step, self.backpackItemSerialArrayLengthList, 
																				  self._backpackItemSerialArrayOffset, self.backpackItemSerialArr)
				grpcBackpackItemSerialReplay = UoService_pb2.GrpcSerialList().FromString(backpackItemSerialSubsetArray)
				#print("grpcBackpackItemReplay: ", grpcBackpackItemReplay)
				self._backpackItemSerialList.append(grpcBackpackItemSerialReplay.serials)
			else:
				print("backpackItemSerialArr is None")

			if self.bankItemSerialArr:
				bankItemSerialSubsetArray, self._bankItemSerialArrayOffset = self.GetSubsetArray(step, self.bankItemSerialArrayLengthList, 
																				  self._bankItemSerialArrayOffset, self.bankItemSerialArr)
				grpcBankItemSerialReplay = UoService_pb2.GrpcSerialList().FromString(bankItemSerialSubsetArray)
				#print("grpcBackpackItemReplay: ", grpcBackpackItemReplay)
				self._bankItemSerialList.append(grpcBankItemSerialReplay.serials)
			else:
				print("bankItemSerialArr is None")

			if self.vendorItemSerialArr:
				vendorItemSerialSubsetArray, self._vendorItemSerialArrayOffset = self.GetSubsetArray(step, self.vendorItemSerialArrayLengthList, 
																			 			   			 self._vendorItemSerialArrayOffset, 
																			 			   			 self.vendorItemSerialArr)
				grpcVendorItemSerialReplay = UoService_pb2.GrpcSerialList().FromString(vendorItemSerialSubsetArray)
				#print("grpcVendorItemObjectReplay: ", grpcVendorItemObjectReplay)
				self._vendorItemSerialsList.append(grpcVendorItemSerialReplay.serials)
			else:
				print("vendorItemSerialsArr is None")

			if self.openedCorpseArr:
				openedCorpseSubsetArray, self._openedCorpseArrayOffset = self.GetSubsetArray(step, self.openedCorpseArrayLengthList, 
																			   				 self._openedCorpseArrayOffset, self.openedCorpseArr)
				grpcOpenedCorpseReplay = UoService_pb2.GrpcContainerDataList().FromString(openedCorpseSubsetArray)
				#print("grpcOpenedCorpseReplay: ", grpcOpenedCorpseReplay)
				self._openedCorpseList.append(grpcOpenedCorpseReplay.containers)
			else:
				print("openedCorpseArr is None")

			if self.popupMenuArr:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthList, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArr)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				#print("grpcPopupMenuReplay: ", grpcPopupMenuReplay)
				self._popupMenuDataList.append(grpcPopupMenuReplay.menus)
			else:
				print("popupMenuArr is None")

			if self.clilocDataArr:
				clilocDataSubsetArray, self._clilocDataArrayOffset = self.GetSubsetArray(step, self.clilocDataArrayLengthList, 
																			   			 self._clilocDataArrayOffset, self.clilocDataArr)
				grpcClilocDataReplay = UoService_pb2.GrpcClilocDataList().FromString(clilocDataSubsetArray)
				#print("grpcClilocDataReplay: ", grpcClilocDataReplay)
				self._clilocDataList.append(grpcClilocDataReplay.clilocDatas)
			else:
				print("clilocDataArr is None")

			if self.sceneMobileObjectSerialArr:
				sceneMobileObjectSerialSubsetArray, self._sceneMobileObjectSerialArrayOffset = self.GetSubsetArray(step, 
																				   self.sceneMobileObjectSerialArrayLengthList, 
																				   self._sceneMobileObjectSerialArrayOffset, self.sceneMobileObjectSerialArr)
				grpcSceneMobileObjectSerialReplay = UoService_pb2.GrpcSerialList().FromString(sceneMobileObjectSerialSubsetArray)
				#print("grpcMobileObjectReplay: ", grpcMobileObjectReplay)
				self._sceneMobileObjectSerialList.append(grpcSceneMobileObjectSerialReplay.serials)
			else:
				print("sceneMobileObjectSerialArr is None")

			if self.sceneItemObjectSerialArr:
				sceneItemObjectSerialSubsetArray, self._sceneItemObjectSerialArrayOffset = self.GetSubsetArray(step, 
																				   self.sceneItemObjectSerialArrayLengthList, 
																				   self._sceneItemObjectSerialArrayOffset, self.sceneItemObjectSerialArr)
				grpcSceneItemObjectSerialReplay = UoService_pb2.GrpcSerialList().FromString(sceneItemObjectSerialSubsetArray)
				#print("grpcMobileObjectReplay: ", grpcMobileObjectReplay)
				self._sceneItemObjectSerialList.append(grpcSceneItemObjectSerialReplay.serials)
			else:
				print("sceneItemObjectSerialArr is None")

			if self.playerStatusArr:
				playerStatusSubsetArray, self._playerStatusArrayOffset = self.GetSubsetArray(step, self.playerStatusArrayLengthList, 
																							 self._playerStatusArrayOffset, 
																							 self.playerStatusArr)
				grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
				#print("grpcPlayerStatusReplay: ", grpcPlayerStatusReplay)
				self._playerStatusList.append(grpcPlayerStatusReplay)
			else:
				print("playerStatusArr is None")

			if self.playerStatusEtcArr:
				playerStatusEtcSubsetArray, self._playerStatusEtcArrayOffset = self.GetSubsetArray(step, self.playerStatusArrayLengthList, 
																								   self._playerStatusArrayOffset, 
																							 	   self.playerStatusEtcArr)
				grpcPlayerStatusEtcReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray)
				#print("grpcPlayerStatusReplay: ", grpcPlayerStatusReplay)
				self._playerStatusList.append(grpcPlayerStatusReplay)
			else:
				print("playerStatusEtcArr is None")

			if self.playerSkillListArr:
				playerSkillListSubsetArray, self._playerSkillListArrayOffset = self.GetSubsetArray(step, self.playerSkillListArrayLengthList, 
																				   		 		   self._playerSkillListArrayOffset, 
																				   		 		   self.playerSkillListArr)
				grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray)
				#print("grpcPlayerSkillListReplay: ", grpcPlayerSkillListReplay)
				self._playerSkillListList.append(grpcPlayerSkillListReplay.skills)
			else:
				print("playerSkillListArr is None")

			if self.staticObjectInfoListArr:
				staticObjectInfoListSubsetArrays, self._staticObjectInfoListArrayOffset = self.GetSubsetArray(step, self.staticObjectInfoListLengthList, 
																				   		   					  self._staticObjectInfoListArrayOffset, 
																				   		   					  self.staticObjectInfoListArr)
				grpcStaticObjectInfoListReplay = UoService_pb2.GrpcGameObjectInfoList().FromString(staticObjectInfoListSubsetArrays)
				#print("grpcStaticObjectInfoListReplay.screenXs: ", grpcStaticObjectInfoListReplay.screenXs)
				#print("grpcStaticObjectInfoListReplay.screenYs: ", grpcStaticObjectInfoListReplay.screenYs)
				self._staticObjectScreenXsList.append(grpcStaticObjectInfoListReplay.screenXs)
				self._staticObjectScreenYsList.append(grpcStaticObjectInfoListReplay.screenYs)

			else:
				print("staticObjectInfoListArr is None")


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

			if len(self._worldMobileList[replay_step]) != 0:
				for obj in self._worldMobileList[replay_step]:

					self.world_mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title, obj.layer]

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
			
			print("self.world_mobile_dict: ", self.world_mobile_dict)
			print("")

			radius = 20
			thickness = 2
			for k, v in self.world_mobile_dict.items():
				#print("v: ", v)
				if v[2] < self._screenWidth and v[3] < self._screenHeight:
					if v[1] == 'Player':
						screen_image = cv2.circle(screen_image, (v[2], v[3]), radius, (0, 255, 0), thickness)
					elif v[1] == 'Mobile':
						screen_image = cv2.circle(screen_image, (v[2], v[3]), radius, (0, 0, 255), thickness)


			mobile_serial_list = self._sceneMobileObjectSerialList[replay_step]
			#print("mobile_serial_list: ", mobile_serial_list)

			'''
			for serial in mobile_serial_list:
				if serial in self.world_mobile_dict:
					#print("serial: ", serial)
					mobile = self.world_mobile_dict[serial]
					#print("mobile: ", mobile)

					#mobile_dict[serial] = [mobile[0], mobile[1], mobile[2], mobile[3], mobile[4], mobile[5]]
					radius = 20
					thickness = 2
					color = (0, 0, 255)
					screen_image = cv2.circle(screen_image, (mobile[2], mobile[3]), radius, color, thickness)
			'''
			#print("")

			# Draw the screen image on the Pygame screen
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