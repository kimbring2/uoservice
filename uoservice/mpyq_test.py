import struct
from mpyq import MPQArchive
import numpy as np

archive = MPQArchive('/home/kimbring2/ClassicUO/bin/dist/Replay/kimbring2-2023-6-6-01-56-41.uoreplay')

files = archive.extract()

'''
mobileDataArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.mobileDataLen");
equippedItemArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.equippedItemLen");
backpackItemArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.backpackitemLen");
corpseItemArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.corpseItemLen");
popupMenuArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.popupMenuLen");
clilocDataArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.clilocDataLen");

playerMobileObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.playerMobileObjectLen");
mobileObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.mobileObjectLen");
itemObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.itemObjectLen");
itemDropableLandArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.itemDropableLandSimpleLen");
vendorItemObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.vendorItemObjectLen");

playerStatusZeroLenStepArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.playerStatusZeroLenStep");
playerSkillListArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.playerSkillListLen");

staticObjectInfoListLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.staticObjectInfoListArraysLen");
'''

test_byte_array = archive.read_file('replay.metadata.mobileDataLen')

mobileDataArrayLengthArrRead = archive.read_file("replay.metadata.mobileDataLen");
equippedItemArrayLengthArrRead = archive.read_file("replay.metadata.equippedItemLen");
backpackItemArrayLengthArrRead = archive.read_file("replay.metadata.backpackitemLen");
corpseItemArrayLengthArrRead = archive.read_file("replay.metadata.corpseItemLen");
popupMenuArrayLengthArrRead = archive.read_file("replay.metadata.popupMenuLen");
clilocDataArrayLengthArrRead = archive.read_file("replay.metadata.clilocDataLen");

playerMobileObjectArrayLengthArrRead = archive.read_file("replay.metadata.playerMobileObjectLen");
mobileObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.mobileObjectLen");
itemObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.itemObjectLen");
itemDropableLandArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.itemDropableLandSimpleLen");
vendorItemObjectArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.vendorItemObjectLen");

playerStatusZeroLenStepArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.playerStatusZeroLenStep");
playerSkillListArrayLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.playerSkillListLen");

staticObjectInfoListLengthArrRead = ReadFromMpqArchive(_replayName, "replay.metadata.staticObjectInfoListArraysLen");

def ConvertByteArrayToIntList(byte_array):
	uint32_list = []

	#for (i = 0; i < len(byte_array); i += sizeof(int))
	for i in range(0, len(byte_array), np.dtype(np.uint32).itemsize):
		#byte_array = byte_array[i:i + 4]
		#print("byte_array: ", byte_array)

		uint32_value = struct.unpack('I', byte_array[i:i + 4])[0]
		uint32_list.append(uint32_value)
	
	return uint32_list


#test_int_list = ConvertByteArrayToIntList(test_byte_array)
