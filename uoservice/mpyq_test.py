import struct
import numpy as np
import grpc

from mpyq import MPQArchive
import UoService_pb2
import UoService_pb2_grpc

archive = MPQArchive('/home/kimbring2/ClassicUO/bin/dist/Replay/kimbring2-2023-6-6-01-56-41.uoreplay')

files = archive.extract()


def ConvertByteArrayToIntList(byteArray):
	intList = []

	for i in range(0, len(byteArray), np.dtype(np.uint32).itemsize):
		intValue = struct.unpack('I', byteArray[i:i + 4])[0]
		intList.append(intValue)
	
	return intList


## Read the length byte array for data array
mobileDataArrayLengthArrRead = archive.read_file("replay.metadata.mobileDataLen");
equippedItemArrayLengthArrRead = archive.read_file("replay.metadata.equippedItemLen");
backpackItemArrayLengthArrRead = archive.read_file("replay.metadata.backpackitemLen");
corpseItemArrayLengthArrRead = archive.read_file("replay.metadata.corpseItemLen");
popupMenuArrayLengthArrRead = archive.read_file("replay.metadata.popupMenuLen");
clilocDataArrayLengthArrRead = archive.read_file("replay.metadata.clilocDataLen");

playerMobileObjectArrayLengthArrRead = archive.read_file("replay.metadata.playerMobileObjectLen");
mobileObjectArrayLengthArrRead = archive.read_file("replay.metadata.mobileObjectLen");
itemObjectArrayLengthArrRead = archive.read_file("replay.metadata.itemObjectLen");
itemDropableLandArrayLengthArrRead = archive.read_file("replay.metadata.itemDropableLandSimpleLen");
vendorItemObjectArrayLengthArrRead = archive.read_file("replay.metadata.vendorItemObjectLen");

playerStatusZeroLenStepArrRead = archive.read_file("replay.metadata.playerStatusZeroLenStep");
playerSkillListArrayLengthArrRead = archive.read_file("replay.metadata.playerSkillListLen");

staticObjectInfoListLengthArrRead = archive.read_file("replay.metadata.staticObjectInfoListArraysLen");

## Convert the byte array to int array
mobileDataArrayLengthListRead = ConvertByteArrayToIntList(mobileDataArrayLengthArrRead);
equippedItemArrayLengthListRead = ConvertByteArrayToIntList(equippedItemArrayLengthArrRead);
backpackItemArrayLengthListRead = ConvertByteArrayToIntList(backpackItemArrayLengthArrRead);
corpseItemArrayLengthListRead = ConvertByteArrayToIntList(corpseItemArrayLengthArrRead);
popupMenuArrayLengthListRead = ConvertByteArrayToIntList(popupMenuArrayLengthArrRead);
clilocDataArrayLengthListRead = ConvertByteArrayToIntList(clilocDataArrayLengthArrRead);
playerMobileObjectArrayLengthListRead = ConvertByteArrayToIntList(playerMobileObjectArrayLengthArrRead);
mobileObjectArrayLengthListRead = ConvertByteArrayToIntList(mobileObjectArrayLengthArrRead);
itemObjectArrayLengthListRead = ConvertByteArrayToIntList(itemObjectArrayLengthArrRead);
itemDropableLandArrayLengthListRead = ConvertByteArrayToIntList(itemDropableLandArrayLengthArrRead);
vendorItemObjectArrayLengthListRead = ConvertByteArrayToIntList(vendorItemObjectArrayLengthArrRead);
playerStatusZeroLenStepListRead = ConvertByteArrayToIntList(playerStatusZeroLenStepArrRead);
playerSkillListArrayLengthListRead = ConvertByteArrayToIntList(playerSkillListArrayLengthArrRead);
staticObjectInfoListLengthListRead = ConvertByteArrayToIntList(staticObjectInfoListLengthArrRead);

## Read the actual for data array
mobileDataArrRead = archive.read_file("replay.data.mobileData");
equippedItemArrRead = archive.read_file("replay.data.equippedItem");
backpackItemArrRead = archive.read_file("replay.data.backpackItem");
corpseItemArrRead = archive.read_file("replay.data.corpseItem");
popupMenuArrRead = archive.read_file("replay.data.popupMenu");
clilocDataArrRead = archive.read_file("replay.data.clilocData");

playerMobileObjectArrRead = archive.read_file("replay.data.playerMobileObject");
mobileObjectArrRead = archive.read_file("replay.data.mobileObject");
itemObjectArrRead = archive.read_file("replay.data.itemObject");
itemDropableLandArrRead = archive.read_file("replay.data.itemDropableLandSimple");
vendorItemObjectArrRead = archive.read_file("replay.data.vendorItemObject");

playerStatusArrRead = archive.read_file("replay.data.playerStatus");
playerSkillListArrRead = archive.read_file("replay.data.playerSkillList");

staticObjectInfoListArrRead = archive.read_file("replay.data.staticObjectInfoList");

## Check the data array is existed
if mobileDataArrRead:
	print("len(mobileDataArrRead): ", len(mobileDataArrRead))
else:
	print("mobileDataArrRead is None")

if equippedItemArrRead:
	print("len(equippedItemArrRead): ", len(equippedItemArrRead))
else:
	print("equippedItemArrRead is None")

if backpackItemArrRead:
	print("len(backpackItemArrRead): ", len(backpackItemArrRead))
else:
	print("backpackItemArrRead is None")

if corpseItemArrRead:
	print("len(corpseItemArrRead): ", len(corpseItemArrRead))
else:
	print("corpseItemArrRead is None")

if popupMenuArrRead:
	print("len(popupMenuArrRead): ", len(popupMenuArrRead))
else:
	print("popupMenuArrRead is None")

if clilocDataArrRead:
	print("len(clilocDataArrRead): ", len(clilocDataArrRead))
else:
	print("clilocDataArrRead is None")

if playerMobileObjectArrRead:
	print("len(playerMobileObjectArrRead): ", len(playerMobileObjectArrRead))
else:
	print("playerMobileObjectArrRead is None")

if mobileObjectArrRead:
	print("len(mobileObjectArrRead): ", len(mobileObjectArrRead))
else:
	print("mobileObjectArrRead is None")

if itemObjectArrRead:
	print("len(itemObjectArrRead): ", len(itemObjectArrRead))
else:
	print("itemObjectArrRead is None")

if itemDropableLandArrRead:
	print("len(itemDropableLandArrRead): ", len(itemDropableLandArrRead))
else:
	print("itemDropableLandArrRead is None")

if vendorItemObjectArrRead:
	print("len(vendorItemObjectArrRead): ", len(vendorItemObjectArrRead))
else:
	print("vendorItemObjectArrRead is None")

if playerStatusArrRead:
	print("len(playerStatusArrRead): ", len(playerStatusArrRead))
else:
	print("playerStatusArrRead is None")

if playerSkillListArrRead:
	print("len(playerSkillListArrRead): ", len(playerSkillListArrRead))
else:
	print("playerSkillListArrRead is None")

if staticObjectInfoListArrRead:
	print("len(staticObjectInfoListArrRead): ", len(staticObjectInfoListArrRead))
else:
	print("staticObjectInfoListArrRead is None")


## Initialize the length related variable
_replayStep = len(mobileDataArrayLengthListRead)

_mobileDataArrayOffset = 0
_equippedItemArrayOffset = 0
_backpackItemArrayOffset = 0
_corpseItemArrayOffset = 0
_popupMenuArrayOffset = 0
_clilocDataArrayOffset = 0

_playerMobileObjectArrayOffset = 0
_mobileObjectArrayOffset = 0
_itemObjectArrayOffset = 0
_itemDropableLandArrayOffset = 0
_vendorItemObjectArrayOffset = 0

_playerStatusArrayOffset = 0
_playerSkillListArrayOffset = 0

_staticObjectInfoListArrayOffset = 0


def GetSubsetArray(index, lengthListRead, offset, arrRead):
	item = lengthListRead[index]
	startIndex = offset
	subsetArray = arrRead[startIndex:startIndex + item]
	offset += item

	return subsetArray, offset


def GetSubsetArrayFix(index, lengthRead, offset, arrRead):
	item = lengthRead
	startIndex = offset
	subsetArray = arrRead[startIndex:startIndex + item]
	offset += item

	return subsetArray, offset


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