import struct
import numpy as np
import grpc

from mpyq import MPQArchive
import UoService_pb2
import UoService_pb2_grpc


import io
from PIL import Image
import time
import numpy as np
import cv2
import random
import pygame
import sys
from enum import Enum
 
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")


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
	def __init__(self, rootPath, screenWidth, screenHeight):
		self._rootPath = rootPath
		self._archive = None

    	## Initialize the length related variable
		self._replayLength = 0

		self._mobileDataArrayOffset = 0
		self._equippedItemArrayOffset = 0
		self._backpackItemArrayOffset = 0
		self._corpseItemArrayOffset = 0
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

		self._playerMobileObjectDataList = []
		self._mobileObjectDataList = []
		self._itemObjectDataList = []
		self._staticObjectScreenXsList = []
		self._staticObjectScreenYsList = []
		self._itemDropableLandObjectList = []
		self._mobileDataList = []
		self._equippedItemList = []
		self._backpackItemList = []
		self._popupMenuDataList = []
		self._corpseItemList = []
		self._vendorItemDataList = []
		self._clilocDataList = []
		self._playerStatusList = []
		self._playerSkillListList = []

		self._screenWidth = screenWidth
		self._screenHeight = screenHeight

		self._mainSurface = pygame.display.set_mode([self._screenWidth + 500, self._screenHeight + 350])
		self._screenSurface = pygame.Surface((self._screenWidth, self._screenHeight))
		self._equipItemSurface = pygame.Surface((600, self._screenHeight))
		self._statusSurface = pygame.Surface((self._screenWidth, 350))
		self._clock = pygame.time.Clock()

	def ConvertByteArrayToIntList(self, byteArray):
		intList = []
		for i in range(0, len(byteArray), np.dtype(np.uint32).itemsize):
			intValue = struct.unpack('I', byteArray[i:i + 4])[0]
			intList.append(intValue)
		
		return intList

	def GetSubsetArray(self, index, lengthListRead, offset, arrRead):
		item = lengthListRead[index]
		startIndex = offset
		subsetArray = arrRead[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def GetSubsetArrayFix(self, index, lengthRead, offset, arrRead):
		item = lengthRead
		startIndex = offset
		subsetArray = arrRead[startIndex:startIndex + item]
		offset += item

		return subsetArray, offset

	def parseItem(self, itemGrpc):
		itemDict = {}
		for item in itemGrpc :
			itemDict[item.serial] = [item.name, item.amount]

		return itemDict

	def parsePlayerStatus(self, playerStatusGrpc):
		playerStatusDict = {}

		playerStatusDict['str'] = playerStatusGrpc.str
		playerStatusDict['dex'] = playerStatusGrpc.dex
		playerStatusDict['intell'] = playerStatusGrpc.intell
		playerStatusDict['hits'] = playerStatusGrpc.hits
		playerStatusDict['hitsMax'] = playerStatusGrpc.hitsMax
		playerStatusDict['stamina'] = playerStatusGrpc.stamina
		playerStatusDict['staminaMax'] = playerStatusGrpc.staminaMax
		playerStatusDict['mana'] = playerStatusGrpc.mana
		playerStatusDict['gold'] = playerStatusGrpc.gold
		playerStatusDict['physicalResistance'] = playerStatusGrpc.physicalResistance
		playerStatusDict['weight'] = playerStatusGrpc.weight
		playerStatusDict['weightMax'] = playerStatusGrpc.weightMax

		return playerStatusDict

	def visObject(self, screenImage, ObjectData, color):
		for obj in ObjectData:
			screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 0] = color[0]
			screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 1] = color[1]
			screenImage[int(obj.screenX / 10.0), int(obj.screenY / 10.0), 2] = color[2]

		return screenImage

	def ReadReplay(self, fileName):
		self._archive = MPQArchive(self._rootPath + '/' + fileName + ".uoreplay")

		## Read the length byte array for data array
		self.mobileDataArrayLengthArrRead = self._archive.read_file("replay.metadata.mobileDataLen");
		self.equippedItemArrayLengthArrRead = self._archive.read_file("replay.metadata.equippedItemLen");
		self.backpackItemArrayLengthArrRead = self._archive.read_file("replay.metadata.backpackitemLen");
		self.corpseItemArrayLengthArrRead = self._archive.read_file("replay.metadata.corpseItemLen");
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
		self.mobileDataArrayLengthListRead = self.ConvertByteArrayToIntList(self.mobileDataArrayLengthArrRead);
		self.equippedItemArrayLengthListRead = self.ConvertByteArrayToIntList(self.equippedItemArrayLengthArrRead);
		self.backpackItemArrayLengthListRead = self.ConvertByteArrayToIntList(self.backpackItemArrayLengthArrRead);
		self.corpseItemArrayLengthListRead = self.ConvertByteArrayToIntList(self.corpseItemArrayLengthArrRead);
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

		self._replayLength = len(self.mobileDataArrayLengthListRead)

		## Read the actual data as byte array
		self.mobileDataArrRead = self._archive.read_file("replay.data.mobileData");
		self.equippedItemArrRead = self._archive.read_file("replay.data.equippedItem");
		self.backpackItemArrRead = self._archive.read_file("replay.data.backpackItem");
		self.corpseItemArrRead = self._archive.read_file("replay.data.corpseItem");
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
		self.actionTypeArrRead = self._archive.read_file("replay.data.type");
		self.walkDirectionArrRead = self._archive.read_file("replay.data.walkDirection");
		self.mobileSerialArrRead = self._archive.read_file("replay.data.mobileSerial");
		self.itemSerialArrRead = self._archive.read_file("replay.data.itemSerial");
		self.indexArrRead = self._archive.read_file("replay.data.index");
		self.amountArrRead = self._archive.read_file("replay.data.amount");

		## Convert the byte array to int array
		self.actionTypeListRead = self.ConvertByteArrayToIntList(self.actionTypeArrRead);
		self.walkDirectionListRead = self.ConvertByteArrayToIntList(self.walkDirectionArrRead);
		self.mobileSerialListRead = self.ConvertByteArrayToIntList(self.mobileSerialArrRead);
		self.itemSerialListRead = self.ConvertByteArrayToIntList(self.itemSerialArrRead);
		self.indexListRead = self.ConvertByteArrayToIntList(self.indexArrRead);
		self.amountListRead = self.ConvertByteArrayToIntList(self.amountArrRead);

		## Check the data array is existed
		if self.mobileDataArrRead:
			print("len(self.mobileDataArrRead): ", len(self.mobileDataArrRead))
		else:
			print("self.mobileDataArrRead is None")

		if self.equippedItemArrRead:
			print("len(self.equippedItemArrRead): ", len(self.equippedItemArrRead))
		else:
			print("self.equippedItemArrRead is None")

		if self.backpackItemArrRead:
			print("len(backpackItemArrRead): ", len(self.backpackItemArrRead))
		else:
			print("backpackItemArrRead is None")

		if self.corpseItemArrRead:
			print("len(corpseItemArrRead): ", len(self.corpseItemArrRead))
		else:
			print("corpseItemArrRead is None")

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
		for step in range(0, self._replayLength):
			print("step: ", step)

			self._actionTypeList.append(self.actionTypeListRead[step])
			self._walkDirectionList.append(self.walkDirectionListRead[step])
			self._mobileSerialList.append(self.mobileSerialListRead[step])
			self._itemSerialList.append(self.itemSerialListRead[step])
			self._indexList.append(self.indexListRead[step])
			self._amountList.append(self.amountListRead[step])

			if self.mobileDataArrRead:
				mobileDataSubsetArray, self._mobileDataArrayOffset = self.GetSubsetArray(step, self.mobileDataArrayLengthListRead, 
																			   self._mobileDataArrayOffset, self.mobileDataArrRead)
				grpcMobileDataReplay = UoService_pb2.GrpcMobileList().FromString(mobileDataSubsetArray)
				#print("grpcMobileDataReplay: ", grpcMobileDataReplay)
				self._mobileDataList.append(grpcMobileDataReplay.mobile)
			else:
				print("mobileDataArrRead is None")

			if self.equippedItemArrRead:
				equippedItemSubsetArray, self._equippedItemArrayOffset = self.GetSubsetArray(step, self.equippedItemArrayLengthListRead, 
																				   self._equippedItemArrayOffset, self.equippedItemArrRead)
				grpcEquippedItemReplay = UoService_pb2.GrpcItemList().FromString(equippedItemSubsetArray)
				#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
				self._equippedItemList.append(grpcEquippedItemReplay.item)
			else:
				print("equippedItemArrRead is None")

			if self.backpackItemArrRead:
				backpackItemSubsetArray, self._backpackItemArrayOffset = self.GetSubsetArray(step, self.backpackItemArrayLengthListRead, 
																				  self._backpackItemArrayOffset, self.backpackItemArrRead)
				grpcBackpackItemReplay = UoService_pb2.GrpcItemList().FromString(backpackItemSubsetArray)
				#print("grpcBackpackItemReplay: ", grpcBackpackItemReplay)
				self._backpackItemList.append(grpcBackpackItemReplay.item)
			else:
				print("backpackItemArrRead is None")

			if self.playerMobileObjectArrRead:
				playerMobileObjectSubsetArray, self._playerMobileObjectArrayOffset = self.GetSubsetArray(step, self.playerMobileObjectArrayLengthListRead, 
																				  			   self._playerMobileObjectArrayOffset, self.playerMobileObjectArrRead)
				grpcPlayerMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(playerMobileObjectSubsetArray)
				#print("grpcPlayerMobileObjectReplay: ", grpcPlayerMobileObjectReplay)
				self._playerMobileObjectDataList.append(grpcPlayerMobileObjectReplay.gameObject)
			else:
				print("playerMobileObjectArrRead is None")

			if self.mobileObjectArrRead:
				mobileObjectSubsetArray, self._mobileObjectArrayOffset = self.GetSubsetArray(step, self.mobileObjectArrayLengthListRead, 
																				   self._mobileObjectArrayOffset, self.mobileObjectArrRead)
				grpcMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(mobileObjectSubsetArray)
				#print("grpcMobileObjectReplay: ", grpcMobileObjectReplay)
				self._mobileObjectDataList.append(grpcMobileObjectReplay.gameObject)
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

			if self.corpseItemArrRead:
				corpseItemSubsetArray, self._corpseItemArrayOffset = self.GetSubsetArray(step, self.corpseItemArrayLengthListRead, 
																			   			 self._corpseItemArrayOffset, self.corpseItemArrRead)
				grpcCorpseItemReplay = UoService_pb2.GrpcItemList().FromString(corpseItemSubsetArray)
				#print("grpcCorpseItemReplay: ", grpcCorpseItemReplay)
				self._corpseItemList.append(grpcCorpseItemReplay.item)
			else:
				print("corpseItemArrRead is None")

			if self.itemObjectArrRead:
				itemObjectSubsetArray, self._itemObjectArrayOffset = self.GetSubsetArray(step, self.itemObjectArrayLengthListRead, 
																			   			 self._itemObjectArrayOffset, self.itemObjectArrRead)
				grpcItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(itemObjectSubsetArray)
				#print("grpcItemObjectReplay: ", grpcItemObjectReplay)
				self._itemObjectDataList.append(grpcItemObjectReplay.gameObject)
			else:
				print("itemObjectArrRead is None")

			if self.itemDropableLandArrRead:
				itemDropableLandSubsetArray, self._itemDropableLandArrayOffset = self.GetSubsetArray(step, self.itemDropableLandArrayLengthListRead, 
																			   			   			 self._itemDropableLandArrayOffset, self.itemDropableLandArrRead)
				grpcItemDropableLandReplay = UoService_pb2.GrpcGameObjectSimpleList().FromString(itemDropableLandSubsetArray)
				#print("grpcItemDropableLandReplay: ", grpcItemDropableLandReplay)
				self._itemDropableLandObjectList.append(grpcItemDropableLandReplay.gameSimpleObject)
			else:
				print("itemDropableLandArrRead is None")

			if self.popupMenuArrRead:
				popupMenuSubsetArray, self._popupMenuArrayOffset = self.GetSubsetArray(step, self.popupMenuArrayLengthListRead, 
																			 		   self._popupMenuArrayOffset, self.popupMenuArrRead)
				grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray)
				#print("grpcPopupMenuReplay: ", grpcPopupMenuReplay)
				self._popupMenuDataList.append(grpcPopupMenuReplay.menu)
			else:
				print("popupMenuArrRead is None")

			if self.vendorItemObjectArrRead:
				vendorItemObjectSubsetArray, self._vendorItemObjectArrayOffset = self.GetSubsetArray(step, self.vendorItemObjectArrayLengthListRead, 
																			 			   			 self._vendorItemObjectArrayOffset, self.vendorItemObjectArrRead)
				grpcVendorItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(vendorItemObjectSubsetArray)
				#print("grpcVendorItemObjectReplay: ", grpcVendorItemObjectReplay)
				self._vendorItemDataList.append(grpcVendorItemObjectReplay.gameObject)
			else:
				print("vendorItemObjectArrRead is None")

			if self.clilocDataArrRead:
				clilocDataSubsetArray, self._clilocDataArrayOffset = self.GetSubsetArray(step, self.clilocDataArrayLengthListRead, 
																			   			 self._clilocDataArrayOffset, self.clilocDataArrRead)
				grpcClilocDataReplay = UoService_pb2.GrpcClilocDataList().FromString(clilocDataSubsetArray)
				#print("grpcClilocDataReplay: ", grpcClilocDataReplay)
				self._clilocDataList.append(grpcClilocDataReplay.clilocData)
			else:
				print("clilocDataArrRead is None")

	def InteractWithReplay(self):
		replay_step = 0

		while True:
		    for event in pygame.event.get():
		         if event.type == pygame.QUIT:
		             running = False

		    keys = pygame.key.get_pressed()
		    if keys[pygame.K_LEFT]:
		      if replay_step >= 1:
		        replay_step -= 1
		        #print("replay_step: ", replay_step)
		      else:
		        print("This is start of replay")

		    if keys[pygame.K_RIGHT]:
		      if replay_step < self._replayLength - 1:
		        replay_step += 1
		        #print("replay_step: ", replay_step)
		      else:
		        print("This is end of replay")

		    # Create the downscaled array for bigger mobile object drawing
		    #screen_image = np.zeros((172,137,3), dtype=np.uint8)
		    screen_image = np.zeros((int((self._screenWidth + 100) / 10), int((self._screenHeight + 100) / 10), 3), dtype=np.uint8)

		    # Draw the player mobile object
		    screen_image = self.visObject(screen_image, self._playerMobileObjectDataList[replay_step], (0, 255, 0))

		    # Draw the mobile object
		    screen_image = self.visObject(screen_image, self._mobileObjectDataList[replay_step], (255, 0, 0))

		    # Draw the item object
		    screen_image = self.visObject(screen_image, self._itemObjectDataList[replay_step], (0, 0, 255))

		    # Resize the screen size to fit real screen
		    screen_image = cv2.resize(screen_image, (self._screenWidth, self._screenHeight), interpolation=cv2.INTER_AREA)
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

		    # Draw the action info on the Pygame screen
		    action_type_surface = font.render("action type: " + str(self._actionTypeList[replay_step]), True, (255, 255, 255))
		    self._screenSurface.blit(action_type_surface, (0, 30))
		    action_type_surface = font.render("walk direction: " + str(self._walkDirectionList[replay_step]), True, (255, 255, 255))
		    self._screenSurface.blit(action_type_surface, (0, 60))

		    # Draw the boundary line
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
		    backpack_item_dict = self.parseItem(backpack_item_grpc)
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
			    vendor_item_dict = self.parseItem(vendor_item_grpc)
			    for i, k in enumerate(vendor_item_dict):
			      font = pygame.font.Font('freesansbold.ttf', 16)
			      item = vendor_item_dict[k]
			      text_surface = font.render(str(k) + ": " + str(item[0]) + ", " + str(item[1]), True, (255, 255, 255))
			      self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 920))

		    # Player status draw
		    player_status_grpc = self._playerStatusList[replay_step]
		    player_status_dict = self.parsePlayerStatus(player_status_grpc)
		    self._statusSurface.fill(((0, 0, 0)))
		    font = pygame.font.Font('freesansbold.ttf', 32)
		    text_surface = font.render("Player Status", True, (255, 0, 255))
		    self._statusSurface.blit(text_surface, (0, 0))
		    for i, k in enumerate(player_status_dict):
		      font = pygame.font.Font('freesansbold.ttf', 16)
		      text_surface = font.render(str(k) + ": " + str(player_status_dict[k]), True, (255, 255, 255))
		      self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

		    # Pop up menu draw
		    font = pygame.font.Font('freesansbold.ttf', 32)
		    text_surface = font.render("Pop Up Menu", True, (255, 0, 255))
		    self._statusSurface.blit(text_surface, (300, 0))
		    if len(self._popupMenuDataList) > 0:
			    for i, menu in enumerate(self._popupMenuDataList[replay_step]):
			      font = pygame.font.Font('freesansbold.ttf', 16)
			      text_surface = font.render(str(i) + ": " + str(menu), True, (255, 255, 255))
			      self._statusSurface.blit(text_surface, (300, 20 * (i + 1) + 20))

		    # Draw each surface on root surface
		    self._mainSurface.blit(self._screenSurface, (0, 0))
		    self._mainSurface.blit(self._equipItemSurface, (self._screenWidth, 0))
		    self._mainSurface.blit(self._statusSurface, (0, self._screenHeight))
		    pygame.display.update()

		    # Wait little bit
		    self._clock.tick(100)

'''
for step in range(0, _replayStep):
	print("step: ", step)

	if mobileDataArrRead:
		mobileDataSubsetArray, _mobileDataArrayOffset = GetSubsetArray(step, mobileDataArrayLengthListRead, 
																	   _mobileDataArrayOffset, mobileDataArrRead)
		grpcMobileDataReplay = UoService_pb2.GrpcMobileList().FromString(mobileDataSubsetArray);
		#print("grpcMobileDataReplay: ", grpcMobileDataReplay)
	else:
		print("mobileDataArrRead is None")

	if equippedItemArrRead:
		equippedItemSubsetArray, _equippedItemArrayOffset = GetSubsetArray(step, equippedItemArrayLengthListRead, 
																		   _equippedItemArrayOffset, equippedItemArrRead)
		grpcEquippedItemReplay = UoService_pb2.GrpcItemList().FromString(equippedItemSubsetArray);
		#print("grpcEquippedItemReplay: ", grpcEquippedItemReplay)
	else:
		print("equippedItemArrRead is None")

	if backpackItemArrRead:
		backpackItemSubsetArray, _backpackItemArrayOffset = GetSubsetArray(step, backpackItemArrayLengthListRead, 
																		  _backpackItemArrayOffset, backpackItemArrRead)
		grpcBackpackItemReplay = UoService_pb2.GrpcItemList().FromString(backpackItemSubsetArray);
		#print("grpcBackpackItemReplay: ", grpcBackpackItemReplay)
	else:
		print("backpackItemArrRead is None")

	if playerMobileObjectArrRead:
		playerMobileObjectSubsetArray, _playerMobileObjectArrayOffset = GetSubsetArray(step, playerMobileObjectArrayLengthListRead, 
																		  			   _playerMobileObjectArrayOffset, playerMobileObjectArrRead)
		grpcPlayerMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(playerMobileObjectSubsetArray);
		#print("grpcPlayerMobileObjectReplay: ", grpcPlayerMobileObjectReplay)
	else:
		print("playerMobileObjectArrRead is None")

	if mobileObjectArrRead:
		mobileObjectSubsetArray, _mobileObjectArrayOffset = GetSubsetArray(step, mobileObjectArrayLengthListRead, 
																		   _mobileObjectArrayOffset, mobileObjectArrRead)
		grpcMobileObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(mobileObjectSubsetArray);
		#print("grpcMobileObjectReplay: ", grpcMobileObjectReplay)
		for obj in grpcMobileObjectReplay.gameObject:
			print("obj: ", obj)

		print("")
	else:
		print("mobileObjectArrRead is None")

	if staticObjectInfoListArrRead:
		staticObjectInfoListSubsetArrays, _staticObjectInfoListArrayOffset = GetSubsetArray(step, staticObjectInfoListLengthListRead, 
																		   		   			_staticObjectInfoListArrayOffset, staticObjectInfoListArrRead)
		grpcStaticObjectInfoListReplay = UoService_pb2.GrpcGameObjectInfoList().FromString(staticObjectInfoListSubsetArrays);
		#print("grpcStaticObjectInfoListReplay: ", grpcStaticObjectInfoListReplay)
	else:
		print("staticObjectInfoListArrRead is None")

	if step not in playerStatusZeroLenStepListRead:
		if playerStatusArrRead:
			playerStatusSubsetArray, _playerStatusArrayOffset = GetSubsetArrayFix(step, 30, _playerStatusArrayOffset, playerStatusArrRead);
			grpcPlayerStatusReplay = UoService_pb2.GrpcPlayerStatus().FromString(playerStatusSubsetArray);
			#print("grpcPlayerStatusReplay: ", grpcPlayerStatusReplay)
		else:
			print("playerStatusArrRead is None")

	if playerSkillListArrRead:
		playerSkillListSubsetArray, _playerSkillListArrayOffset = GetSubsetArray(step, playerSkillListArrayLengthListRead, 
																		   		 _playerSkillListArrayOffset, playerSkillListArrRead)
		grpcPlayerSkillListReplay = UoService_pb2.GrpcSkillList().FromString(playerSkillListSubsetArray);
		#print("grpcPlayerSkillListReplay: ", grpcPlayerSkillListReplay)
	else:
		print("playerSkillListArrRead is None")

	if corpseItemArrRead:
		corpseItemSubsetArray, _corpseItemArrayOffset = GetSubsetArray(step, corpseItemArrayLengthListRead, 
																	   _corpseItemArrayOffset, corpseItemArrRead)
		grpcCorpseItemReplay = UoService_pb2.GrpcItemList().FromString(corpseItemSubsetArray);
		#print("grpcCorpseItemReplay: ", grpcCorpseItemReplay)
	else:
		print("corpseItemArrRead is None")

	if itemObjectArrRead:
		itemObjectSubsetArray, _itemObjectArrayOffset = GetSubsetArray(step, itemObjectArrayLengthListRead, 
																	   _itemObjectArrayOffset, itemObjectArrRead)
		grpcItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(itemObjectSubsetArray);
		#print("grpcItemObjectReplay: ", grpcItemObjectReplay)
	else:
		print("itemObjectArrRead is None")

	if itemObjectArrRead:
		itemDropableLandSubsetArray, _itemDropableLandArrayOffset = GetSubsetArray(step, itemDropableLandArrayLengthListRead, 
																	   			   _itemDropableLandArrayOffset, itemDropableLandArrRead)
		grpcItemDropableLandReplay = UoService_pb2.GrpcGameObjectSimpleList().FromString(itemDropableLandSubsetArray);
		#print("grpcItemDropableLandReplay: ", grpcItemDropableLandReplay)
	else:
		print("itemObjectArrRead is None")

	if popupMenuArrRead:
		popupMenuSubsetArray, _popupMenuArrayOffset = GetSubsetArray(step, popupMenuArrayLengthListRead, 
																	 _popupMenuArrayOffset, popupMenuArrRead)
		grpcPopupMenuReplay = UoService_pb2.GrpcPopupMenuList().FromString(popupMenuSubsetArray);
		#print("grpcPopupMenuReplay: ", grpcPopupMenuReplay)
	else:
		print("popupMenuArrRead is None")

	if vendorItemObjectArrRead:
		vendorItemObjectSubsetArray, _vendorItemObjectArrayOffset = GetSubsetArray(step, vendorItemObjectArrayLengthListRead, 
																	 			   _vendorItemObjectArrayOffset, vendorItemObjectArrRead)
		grpcVendorItemObjectReplay = UoService_pb2.GrpcGameObjectList().FromString(vendorItemObjectSubsetArray);
		#print("grpcVendorItemObjectReplay: ", grpcVendorItemObjectReplay)
	else:
		print("vendorItemObjectArrRead is None")


	if clilocDataArrRead:
		clilocDataSubsetArray, _clilocDataArrayOffset = GetSubsetArray(step, clilocDataArrayLengthListRead, 
																	   _clilocDataArrayOffset, clilocDataArrRead)
		grpcClilocDataReplay = UoService_pb2.GrpcClilocDataList().FromString(clilocDataSubsetArray);
		#print("grpcClilocDataReplay: ", grpcClilocDataReplay)
	else:
		print("clilocDataArrRead is None")
'''