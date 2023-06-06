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
print("len(mobileDataArrayLengthListRead): ", len(mobileDataArrayLengthListRead))

equippedItemArrayLengthListRead = ConvertByteArrayToIntList(equippedItemArrayLengthArrRead);
print("len(equippedItemArrayLengthListRead): ", len(equippedItemArrayLengthListRead))

backpackItemArrayLengthListRead = ConvertByteArrayToIntList(backpackItemArrayLengthArrRead);
print("len(backpackItemArrayLengthListRead): ", len(backpackItemArrayLengthListRead))

corpseItemArrayLengthListRead = ConvertByteArrayToIntList(corpseItemArrayLengthArrRead);
print("len(corpseItemArrayLengthListRead): ", len(corpseItemArrayLengthListRead))

popupMenuArrayLengthListRead = ConvertByteArrayToIntList(popupMenuArrayLengthArrRead);
print("len(popupMenuArrayLengthListRead): ", len(popupMenuArrayLengthListRead))

clilocDataArrayLengthListRead = ConvertByteArrayToIntList(clilocDataArrayLengthArrRead);
print("len(clilocDataArrayLengthListRead): ", len(clilocDataArrayLengthListRead))

playerMobileObjectArrayLengthListRead = ConvertByteArrayToIntList(playerMobileObjectArrayLengthArrRead);
print("len(playerMobileObjectArrayLengthListRead): ", len(playerMobileObjectArrayLengthListRead))

mobileObjectArrayLengthListRead = ConvertByteArrayToIntList(mobileObjectArrayLengthArrRead);
print("len(mobileDataArrayLengthListRead): ", len(mobileDataArrayLengthListRead))

itemObjectArrayLengthListRead = ConvertByteArrayToIntList(itemObjectArrayLengthArrRead);
print("len(itemObjectArrayLengthListRead): ", len(itemObjectArrayLengthListRead))

itemDropableLandArrayLengthListRead = ConvertByteArrayToIntList(itemDropableLandArrayLengthArrRead);
print("len(itemDropableLandArrayLengthListRead): ", len(itemDropableLandArrayLengthListRead))

vendorItemObjectArrayLengthListRead = ConvertByteArrayToIntList(vendorItemObjectArrayLengthArrRead);
print("len(vendorItemObjectArrayLengthListRead): ", len(vendorItemObjectArrayLengthListRead))

playerStatusZeroLenStepListRead = ConvertByteArrayToIntList(playerStatusZeroLenStepArrRead);
print("len(playerStatusZeroLenStepListRead): ", len(playerStatusZeroLenStepListRead))

playerSkillListArrayLengthListRead = ConvertByteArrayToIntList(playerSkillListArrayLengthArrRead);
print("len(playerSkillListArrayLengthListRead): ", len(playerSkillListArrayLengthListRead))

staticObjectInfoListLengthListRead = ConvertByteArrayToIntList(staticObjectInfoListLengthArrRead);
print("len(staticObjectInfoListLengthListRead): ", len(staticObjectInfoListLengthListRead))


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
	item = lengthListRead[index];
	#print("item: ", item)

	startIndex = offset; 
	#Array.Copy(arrRead, startIndex, subsetArray, 0, item);
	subsetArray = arrRead[startIndex:startIndex + item]
	#print("subsetArray: ", subsetArray)

	offset += item;

	return subsetArray, offset;


for step in range(0, _replayStep):
	mobileDataSubsetArray, _mobileDataArrayOffset = GetSubsetArray(step, mobileDataArrayLengthListRead, _mobileDataArrayOffset, mobileDataArrRead)

	#print("mobileDataSubsetArray: ", mobileDataSubsetArray)

	message = UoService_pb2.GrpcMobileList()
	grpcMobileDataReplay = message.FromString(mobileDataSubsetArray);
	print("grpcMobileDataReplay: ", grpcMobileDataReplay)
	#print("")

	#states.MobileList = grpcMobileDataReplay;