# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: UoService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fUoService.proto\x12\tuoservice\"\x07\n\x05\x45mpty\"R\n\x0eGrpcMobileData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\x12\x0c\n\x04race\x18\x04 \x01(\r\x12\x0e\n\x06serial\x18\x05 \x01(\r\"K\n\x0cGrpcItemData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05layer\x18\x02 \x01(\r\x12\x0e\n\x06serial\x18\x03 \x01(\r\x12\x0e\n\x06\x61mount\x18\x04 \x01(\r\"K\n\x0eGrpcClilocData\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\r\n\x05\x61\x66\x66ix\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"C\n\x12GrpcClilocDataList\x12-\n\nclilocData\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcClilocData\"\xd2\x01\n\x12GrpcGameObjectData\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07screenX\x18\x02 \x01(\r\x12\x0f\n\x07screenY\x18\x03 \x01(\r\x12\x10\n\x08\x64istance\x18\x04 \x01(\r\x12\r\n\x05gameX\x18\x05 \x01(\r\x12\r\n\x05gameY\x18\x06 \x01(\r\x12\x0e\n\x06serial\x18\x07 \x01(\r\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x10\n\x08isCorpse\x18\t \x01(\x08\x12\r\n\x05title\x18\n \x01(\t\x12\x0e\n\x06\x61mount\x18\x0b \x01(\r\x12\r\n\x05price\x18\x0c \x01(\r\"G\n\x12GrpcGameObjectList\x12\x31\n\ngameObject\x18\x01 \x03(\x0b\x32\x1d.uoservice.GrpcGameObjectData\"8\n\x18GrpcGameObjectSimpleData\x12\r\n\x05gameX\x18\x01 \x01(\r\x12\r\n\x05gameY\x18\x02 \x01(\r\"<\n\x16GrpcGameObjectInfoList\x12\x10\n\x08screenXs\x18\x01 \x03(\r\x12\x10\n\x08screenYs\x18\x02 \x03(\r\"Y\n\x18GrpcGameObjectSimpleList\x12=\n\x10gameSimpleObject\x18\x01 \x03(\x0b\x32#.uoservice.GrpcGameObjectSimpleData\"\x1f\n\x0fSemaphoreAction\x12\x0c\n\x04mode\x18\x01 \x01(\t\";\n\x0eGrpcMobileList\x12)\n\x06mobile\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcMobileData\"5\n\x0cGrpcItemList\x12%\n\x04item\x18\x01 \x03(\x0b\x32\x17.uoservice.GrpcItemData\"!\n\x11GrpcPopupMenuList\x12\x0c\n\x04menu\x18\x01 \x03(\t\"*\n\x06\x43onfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nreplayName\x18\x02 \x01(\t\"u\n\tGrpcSkill\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\r\x12\x13\n\x0bisClickable\x18\x03 \x01(\x08\x12\r\n\x05value\x18\x04 \x01(\r\x12\x0c\n\x04\x62\x61se\x18\x05 \x01(\r\x12\x0b\n\x03\x63\x61p\x18\x06 \x01(\r\x12\x0c\n\x04lock\x18\x07 \x01(\r\"5\n\rGrpcSkillList\x12$\n\x06skills\x18\x01 \x03(\x0b\x32\x14.uoservice.GrpcSkill\"\xec\x01\n\x10GrpcPlayerStatus\x12\x0b\n\x03str\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x65x\x18\x02 \x01(\r\x12\x0e\n\x06intell\x18\x03 \x01(\r\x12\x0c\n\x04hits\x18\x04 \x01(\r\x12\x0f\n\x07hitsMax\x18\x05 \x01(\r\x12\x0f\n\x07stamina\x18\x06 \x01(\r\x12\x12\n\nstaminaMax\x18\x07 \x01(\r\x12\x0c\n\x04mana\x18\x08 \x01(\r\x12\x0f\n\x07manaMax\x18\t \x01(\r\x12\x0c\n\x04gold\x18\n \x01(\r\x12\x1a\n\x12physicalResistance\x18\x0b \x01(\r\x12\x0e\n\x06weight\x18\x0c \x01(\r\x12\x11\n\tweightMax\x18\r \x01(\r\"y\n\x11GrpcContainerData\x12\x30\n\tcontainer\x18\x01 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectData\x12\x32\n\x11\x63ontainerItemList\x18\x02 \x01(\x0b\x32\x17.uoservice.GrpcItemList\"I\n\x15GrpcContainerDataList\x12\x30\n\ncontainers\x18\x01 \x03(\x0b\x32\x1c.uoservice.GrpcContainerData\"\xa5\x07\n\x06States\x12-\n\nmobileList\x18\x01 \x01(\x0b\x32\x19.uoservice.GrpcMobileList\x12.\n\rworldItemList\x18\x02 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12\x31\n\x10\x65quippedItemList\x18\x03 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12\x31\n\x10\x62\x61\x63kpackItemList\x18\x04 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12:\n\x10openedCorpseList\x18\x05 \x01(\x0b\x32 .uoservice.GrpcContainerDataList\x12\x31\n\x0cplayerStatus\x18\x06 \x01(\x0b\x32\x1b.uoservice.GrpcPlayerStatus\x12\x37\n\x10mobileObjectList\x18\x07 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12=\n\x16playerMobileObjectList\x18\x08 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12\x35\n\x0eitemObjectList\x18\t \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12\x41\n\x14itemDropableLandList\x18\x0b \x01(\x0b\x32#.uoservice.GrpcGameObjectSimpleList\x12;\n\x14vendorItemObjectList\x18\x0c \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12\x33\n\rpopupMenuList\x18\r \x01(\x0b\x32\x1c.uoservice.GrpcPopupMenuList\x12\x35\n\x0e\x63lilocDataList\x18\x0e \x01(\x0b\x32\x1d.uoservice.GrpcClilocDataList\x12)\n\rreplayActions\x18\x0f \x01(\x0b\x32\x12.uoservice.Actions\x12?\n\x14staticObjectInfoList\x18\x10 \x01(\x0b\x32!.uoservice.GrpcGameObjectInfoList\x12\x31\n\x0fplayerSkillList\x18\x11 \x01(\x0b\x32\x18.uoservice.GrpcSkillList\x12-\n\x0c\x62\x61nkItemList\x18\x12 \x01(\x0b\x32\x17.uoservice.GrpcItemList\"\x8e\x01\n\x07\x41\x63tions\x12\x12\n\nactionType\x18\x01 \x01(\r\x12\x16\n\x0eselectedSerial\x18\x02 \x01(\r\x12\x14\n\x0ctargetSerial\x18\x03 \x01(\r\x12\x15\n\rwalkDirection\x18\x04 \x01(\r\x12\r\n\x05index\x18\x05 \x01(\r\x12\x0e\n\x06\x61mount\x18\x06 \x01(\r\x12\x0b\n\x03run\x18\x07 \x01(\r2\x8f\x03\n\tUoService\x12-\n\x05Reset\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12/\n\x07ReadObs\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x30\n\x08WriteAct\x12\x12.uoservice.Actions\x1a\x10.uoservice.Empty\x12\x43\n\x13\x41\x63tSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x43\n\x13ObsSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x32\n\nReadReplay\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x32\n\x0bReadMPQFile\x12\x11.uoservice.Config\x1a\x10.uoservice.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_GRPCMOBILEDATA = DESCRIPTOR.message_types_by_name['GrpcMobileData']
_GRPCITEMDATA = DESCRIPTOR.message_types_by_name['GrpcItemData']
_GRPCCLILOCDATA = DESCRIPTOR.message_types_by_name['GrpcClilocData']
_GRPCCLILOCDATALIST = DESCRIPTOR.message_types_by_name['GrpcClilocDataList']
_GRPCGAMEOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcGameObjectData']
_GRPCGAMEOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectList']
_GRPCGAMEOBJECTSIMPLEDATA = DESCRIPTOR.message_types_by_name['GrpcGameObjectSimpleData']
_GRPCGAMEOBJECTINFOLIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectInfoList']
_GRPCGAMEOBJECTSIMPLELIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectSimpleList']
_SEMAPHOREACTION = DESCRIPTOR.message_types_by_name['SemaphoreAction']
_GRPCMOBILELIST = DESCRIPTOR.message_types_by_name['GrpcMobileList']
_GRPCITEMLIST = DESCRIPTOR.message_types_by_name['GrpcItemList']
_GRPCPOPUPMENULIST = DESCRIPTOR.message_types_by_name['GrpcPopupMenuList']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']
_GRPCSKILL = DESCRIPTOR.message_types_by_name['GrpcSkill']
_GRPCSKILLLIST = DESCRIPTOR.message_types_by_name['GrpcSkillList']
_GRPCPLAYERSTATUS = DESCRIPTOR.message_types_by_name['GrpcPlayerStatus']
_GRPCCONTAINERDATA = DESCRIPTOR.message_types_by_name['GrpcContainerData']
_GRPCCONTAINERDATALIST = DESCRIPTOR.message_types_by_name['GrpcContainerDataList']
_STATES = DESCRIPTOR.message_types_by_name['States']
_ACTIONS = DESCRIPTOR.message_types_by_name['Actions']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Empty)
  })
_sym_db.RegisterMessage(Empty)

GrpcMobileData = _reflection.GeneratedProtocolMessageType('GrpcMobileData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCMOBILEDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcMobileData)
  })
_sym_db.RegisterMessage(GrpcMobileData)

GrpcItemData = _reflection.GeneratedProtocolMessageType('GrpcItemData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCITEMDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcItemData)
  })
_sym_db.RegisterMessage(GrpcItemData)

GrpcClilocData = _reflection.GeneratedProtocolMessageType('GrpcClilocData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCLILOCDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcClilocData)
  })
_sym_db.RegisterMessage(GrpcClilocData)

GrpcClilocDataList = _reflection.GeneratedProtocolMessageType('GrpcClilocDataList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCLILOCDATALIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcClilocDataList)
  })
_sym_db.RegisterMessage(GrpcClilocDataList)

GrpcGameObjectData = _reflection.GeneratedProtocolMessageType('GrpcGameObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectData)
  })
_sym_db.RegisterMessage(GrpcGameObjectData)

GrpcGameObjectList = _reflection.GeneratedProtocolMessageType('GrpcGameObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectList)
  })
_sym_db.RegisterMessage(GrpcGameObjectList)

GrpcGameObjectSimpleData = _reflection.GeneratedProtocolMessageType('GrpcGameObjectSimpleData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTSIMPLEDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectSimpleData)
  })
_sym_db.RegisterMessage(GrpcGameObjectSimpleData)

GrpcGameObjectInfoList = _reflection.GeneratedProtocolMessageType('GrpcGameObjectInfoList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTINFOLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectInfoList)
  })
_sym_db.RegisterMessage(GrpcGameObjectInfoList)

GrpcGameObjectSimpleList = _reflection.GeneratedProtocolMessageType('GrpcGameObjectSimpleList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTSIMPLELIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectSimpleList)
  })
_sym_db.RegisterMessage(GrpcGameObjectSimpleList)

SemaphoreAction = _reflection.GeneratedProtocolMessageType('SemaphoreAction', (_message.Message,), {
  'DESCRIPTOR' : _SEMAPHOREACTION,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.SemaphoreAction)
  })
_sym_db.RegisterMessage(SemaphoreAction)

GrpcMobileList = _reflection.GeneratedProtocolMessageType('GrpcMobileList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCMOBILELIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcMobileList)
  })
_sym_db.RegisterMessage(GrpcMobileList)

GrpcItemList = _reflection.GeneratedProtocolMessageType('GrpcItemList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCITEMLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcItemList)
  })
_sym_db.RegisterMessage(GrpcItemList)

GrpcPopupMenuList = _reflection.GeneratedProtocolMessageType('GrpcPopupMenuList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPOPUPMENULIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPopupMenuList)
  })
_sym_db.RegisterMessage(GrpcPopupMenuList)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Config)
  })
_sym_db.RegisterMessage(Config)

GrpcSkill = _reflection.GeneratedProtocolMessageType('GrpcSkill', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSKILL,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSkill)
  })
_sym_db.RegisterMessage(GrpcSkill)

GrpcSkillList = _reflection.GeneratedProtocolMessageType('GrpcSkillList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSKILLLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSkillList)
  })
_sym_db.RegisterMessage(GrpcSkillList)

GrpcPlayerStatus = _reflection.GeneratedProtocolMessageType('GrpcPlayerStatus', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYERSTATUS,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerStatus)
  })
_sym_db.RegisterMessage(GrpcPlayerStatus)

GrpcContainerData = _reflection.GeneratedProtocolMessageType('GrpcContainerData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCONTAINERDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcContainerData)
  })
_sym_db.RegisterMessage(GrpcContainerData)

GrpcContainerDataList = _reflection.GeneratedProtocolMessageType('GrpcContainerDataList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCONTAINERDATALIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcContainerDataList)
  })
_sym_db.RegisterMessage(GrpcContainerDataList)

States = _reflection.GeneratedProtocolMessageType('States', (_message.Message,), {
  'DESCRIPTOR' : _STATES,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.States)
  })
_sym_db.RegisterMessage(States)

Actions = _reflection.GeneratedProtocolMessageType('Actions', (_message.Message,), {
  'DESCRIPTOR' : _ACTIONS,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Actions)
  })
_sym_db.RegisterMessage(Actions)

_UOSERVICE = DESCRIPTOR.services_by_name['UoService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=30
  _EMPTY._serialized_end=37
  _GRPCMOBILEDATA._serialized_start=39
  _GRPCMOBILEDATA._serialized_end=121
  _GRPCITEMDATA._serialized_start=123
  _GRPCITEMDATA._serialized_end=198
  _GRPCCLILOCDATA._serialized_start=200
  _GRPCCLILOCDATA._serialized_end=275
  _GRPCCLILOCDATALIST._serialized_start=277
  _GRPCCLILOCDATALIST._serialized_end=344
  _GRPCGAMEOBJECTDATA._serialized_start=347
  _GRPCGAMEOBJECTDATA._serialized_end=557
  _GRPCGAMEOBJECTLIST._serialized_start=559
  _GRPCGAMEOBJECTLIST._serialized_end=630
  _GRPCGAMEOBJECTSIMPLEDATA._serialized_start=632
  _GRPCGAMEOBJECTSIMPLEDATA._serialized_end=688
  _GRPCGAMEOBJECTINFOLIST._serialized_start=690
  _GRPCGAMEOBJECTINFOLIST._serialized_end=750
  _GRPCGAMEOBJECTSIMPLELIST._serialized_start=752
  _GRPCGAMEOBJECTSIMPLELIST._serialized_end=841
  _SEMAPHOREACTION._serialized_start=843
  _SEMAPHOREACTION._serialized_end=874
  _GRPCMOBILELIST._serialized_start=876
  _GRPCMOBILELIST._serialized_end=935
  _GRPCITEMLIST._serialized_start=937
  _GRPCITEMLIST._serialized_end=990
  _GRPCPOPUPMENULIST._serialized_start=992
  _GRPCPOPUPMENULIST._serialized_end=1025
  _CONFIG._serialized_start=1027
  _CONFIG._serialized_end=1069
  _GRPCSKILL._serialized_start=1071
  _GRPCSKILL._serialized_end=1188
  _GRPCSKILLLIST._serialized_start=1190
  _GRPCSKILLLIST._serialized_end=1243
  _GRPCPLAYERSTATUS._serialized_start=1246
  _GRPCPLAYERSTATUS._serialized_end=1482
  _GRPCCONTAINERDATA._serialized_start=1484
  _GRPCCONTAINERDATA._serialized_end=1605
  _GRPCCONTAINERDATALIST._serialized_start=1607
  _GRPCCONTAINERDATALIST._serialized_end=1680
  _STATES._serialized_start=1683
  _STATES._serialized_end=2616
  _ACTIONS._serialized_start=2619
  _ACTIONS._serialized_end=2761
  _UOSERVICE._serialized_start=2764
  _UOSERVICE._serialized_end=3163
# @@protoc_insertion_point(module_scope)
