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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fUoService.proto\x12\tuoservice\"\x07\n\x05\x45mpty\"K\n\x0cGrpcItemData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05layer\x18\x02 \x01(\r\x12\x0e\n\x06serial\x18\x03 \x01(\r\x12\x0e\n\x06\x61mount\x18\x04 \x01(\r\"K\n\x0eGrpcClilocData\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\r\n\x05\x61\x66\x66ix\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"\xe1\x01\n\x12GrpcGameObjectData\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07screenX\x18\x02 \x01(\r\x12\x0f\n\x07screenY\x18\x03 \x01(\r\x12\x10\n\x08\x64istance\x18\x04 \x01(\r\x12\r\n\x05gameX\x18\x05 \x01(\r\x12\r\n\x05gameY\x18\x06 \x01(\r\x12\x0e\n\x06serial\x18\x07 \x01(\r\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x10\n\x08isCorpse\x18\t \x01(\x08\x12\r\n\x05title\x18\n \x01(\t\x12\x0e\n\x06\x61mount\x18\x0b \x01(\r\x12\r\n\x05price\x18\x0c \x01(\r\x12\r\n\x05layer\x18\r \x01(\r\"u\n\tGrpcSkill\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\r\x12\x13\n\x0bisClickable\x18\x03 \x01(\x08\x12\r\n\x05value\x18\x04 \x01(\r\x12\x0c\n\x04\x62\x61se\x18\x05 \x01(\r\x12\x0b\n\x03\x63\x61p\x18\x06 \x01(\r\x12\x0c\n\x04lock\x18\x07 \x01(\r\"\xec\x01\n\x10GrpcPlayerStatus\x12\x0b\n\x03str\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x65x\x18\x02 \x01(\r\x12\x0e\n\x06intell\x18\x03 \x01(\r\x12\x0c\n\x04hits\x18\x04 \x01(\r\x12\x0f\n\x07hitsMax\x18\x05 \x01(\r\x12\x0f\n\x07stamina\x18\x06 \x01(\r\x12\x12\n\nstaminaMax\x18\x07 \x01(\r\x12\x0c\n\x04mana\x18\x08 \x01(\r\x12\x0f\n\x07manaMax\x18\t \x01(\r\x12\x0c\n\x04gold\x18\n \x01(\r\x12\x1a\n\x12physicalResistance\x18\x0b \x01(\r\x12\x0e\n\x06weight\x18\x0c \x01(\r\x12\x11\n\tweightMax\x18\r \x01(\r\">\n\x13GrpcPlayerStatusEtc\x12\x16\n\x0eholdItemSerial\x18\x01 \x01(\r\x12\x0f\n\x07warMode\x18\x02 \x01(\x08\"8\n\x18GrpcGameObjectSimpleData\x12\r\n\x05gameX\x18\x01 \x01(\r\x12\r\n\x05gameY\x18\x02 \x01(\r\"<\n\x16GrpcGameObjectInfoList\x12\x10\n\x08screenXs\x18\x01 \x03(\r\x12\x10\n\x08screenYs\x18\x02 \x03(\r\"\"\n\x11GrpcPopupMenuList\x12\r\n\x05menus\x18\x01 \x03(\t\"D\n\x12GrpcClilocDataList\x12.\n\x0b\x63lilocDatas\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcClilocData\"H\n\x12GrpcGameObjectList\x12\x32\n\x0bgameObjects\x18\x01 \x03(\x0b\x32\x1d.uoservice.GrpcGameObjectData\"Z\n\x18GrpcGameObjectSimpleList\x12>\n\x11gameSimpleObjects\x18\x01 \x03(\x0b\x32#.uoservice.GrpcGameObjectSimpleData\"\x1f\n\x0fSemaphoreAction\x12\x0c\n\x04mode\x18\x01 \x01(\t\"6\n\x0cGrpcItemList\x12&\n\x05items\x18\x01 \x03(\x0b\x32\x17.uoservice.GrpcItemData\"\x16\n\x06\x43onfig\x12\x0c\n\x04init\x18\x01 \x01(\x08\"5\n\rGrpcSkillList\x12$\n\x06skills\x18\x01 \x03(\x0b\x32\x14.uoservice.GrpcSkill\"h\n\x11GrpcContainerData\x12\x17\n\x0f\x63ontainerSerial\x18\x01 \x01(\r\x12:\n\x17\x63ontainerItemSerialList\x18\x02 \x01(\x0b\x32\x19.uoservice.GrpcSerialList\"I\n\x15GrpcContainerDataList\x12\x30\n\ncontainers\x18\x01 \x03(\x0b\x32\x1c.uoservice.GrpcContainerData\"!\n\x0eGrpcSerialList\x12\x0f\n\x07serials\x18\x01 \x03(\r\"\xb0\x07\n\x06States\x12\x37\n\x10playerGameObject\x18\x01 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectData\x12\x34\n\rWorldItemList\x18\x02 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12\x36\n\x0fWorldMobileList\x18\x03 \x01(\x0b\x32\x1d.uoservice.GrpcGameObjectList\x12\x39\n\x16\x65quippedItemSerialList\x18\x04 \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12\x39\n\x16\x62\x61\x63kpackItemSerialList\x18\x05 \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12\x35\n\x12\x62\x61nkItemSerialList\x18\x06 \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12\x37\n\x14vendorItemSerialList\x18\x07 \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12:\n\x10openedCorpseList\x18\x08 \x01(\x0b\x32 .uoservice.GrpcContainerDataList\x12\x31\n\x0cplayerStatus\x18\t \x01(\x0b\x32\x1b.uoservice.GrpcPlayerStatus\x12\x33\n\x10mobileObjectList\x18\n \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12\x31\n\x0eitemObjectList\x18\x0b \x01(\x0b\x32\x19.uoservice.GrpcSerialList\x12\x33\n\rpopupMenuList\x18\x0c \x01(\x0b\x32\x1c.uoservice.GrpcPopupMenuList\x12\x35\n\x0e\x63lilocDataList\x18\r \x01(\x0b\x32\x1d.uoservice.GrpcClilocDataList\x12)\n\rreplayActions\x18\x0e \x01(\x0b\x32\x12.uoservice.Actions\x12?\n\x14staticObjectInfoList\x18\x0f \x01(\x0b\x32!.uoservice.GrpcGameObjectInfoList\x12\x31\n\x0fplayerSkillList\x18\x10 \x01(\x0b\x32\x18.uoservice.GrpcSkillList\x12\x37\n\x0fplayerStatusEtc\x18\x11 \x01(\x0b\x32\x1e.uoservice.GrpcPlayerStatusEtc\"\x8a\x01\n\x07\x41\x63tions\x12\x12\n\nactionType\x18\x01 \x01(\r\x12\x12\n\nitemSerial\x18\x02 \x01(\r\x12\x14\n\x0cmobileSerial\x18\x03 \x01(\r\x12\x15\n\rwalkDirection\x18\x04 \x01(\r\x12\r\n\x05index\x18\x05 \x01(\r\x12\x0e\n\x06\x61mount\x18\x06 \x01(\r\x12\x0b\n\x03run\x18\x07 \x01(\x08\x32\x8f\x03\n\tUoService\x12-\n\x05Reset\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12/\n\x07ReadObs\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x30\n\x08WriteAct\x12\x12.uoservice.Actions\x1a\x10.uoservice.Empty\x12\x43\n\x13\x41\x63tSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x43\n\x13ObsSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x32\n\nReadReplay\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x32\n\x0bReadMPQFile\x12\x11.uoservice.Config\x1a\x10.uoservice.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_GRPCITEMDATA = DESCRIPTOR.message_types_by_name['GrpcItemData']
_GRPCCLILOCDATA = DESCRIPTOR.message_types_by_name['GrpcClilocData']
_GRPCGAMEOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcGameObjectData']
_GRPCSKILL = DESCRIPTOR.message_types_by_name['GrpcSkill']
_GRPCPLAYERSTATUS = DESCRIPTOR.message_types_by_name['GrpcPlayerStatus']
_GRPCPLAYERSTATUSETC = DESCRIPTOR.message_types_by_name['GrpcPlayerStatusEtc']
_GRPCGAMEOBJECTSIMPLEDATA = DESCRIPTOR.message_types_by_name['GrpcGameObjectSimpleData']
_GRPCGAMEOBJECTINFOLIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectInfoList']
_GRPCPOPUPMENULIST = DESCRIPTOR.message_types_by_name['GrpcPopupMenuList']
_GRPCCLILOCDATALIST = DESCRIPTOR.message_types_by_name['GrpcClilocDataList']
_GRPCGAMEOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectList']
_GRPCGAMEOBJECTSIMPLELIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectSimpleList']
_SEMAPHOREACTION = DESCRIPTOR.message_types_by_name['SemaphoreAction']
_GRPCITEMLIST = DESCRIPTOR.message_types_by_name['GrpcItemList']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']
_GRPCSKILLLIST = DESCRIPTOR.message_types_by_name['GrpcSkillList']
_GRPCCONTAINERDATA = DESCRIPTOR.message_types_by_name['GrpcContainerData']
_GRPCCONTAINERDATALIST = DESCRIPTOR.message_types_by_name['GrpcContainerDataList']
_GRPCSERIALLIST = DESCRIPTOR.message_types_by_name['GrpcSerialList']
_STATES = DESCRIPTOR.message_types_by_name['States']
_ACTIONS = DESCRIPTOR.message_types_by_name['Actions']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Empty)
  })
_sym_db.RegisterMessage(Empty)

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

GrpcGameObjectData = _reflection.GeneratedProtocolMessageType('GrpcGameObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectData)
  })
_sym_db.RegisterMessage(GrpcGameObjectData)

GrpcSkill = _reflection.GeneratedProtocolMessageType('GrpcSkill', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSKILL,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSkill)
  })
_sym_db.RegisterMessage(GrpcSkill)

GrpcPlayerStatus = _reflection.GeneratedProtocolMessageType('GrpcPlayerStatus', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYERSTATUS,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerStatus)
  })
_sym_db.RegisterMessage(GrpcPlayerStatus)

GrpcPlayerStatusEtc = _reflection.GeneratedProtocolMessageType('GrpcPlayerStatusEtc', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYERSTATUSETC,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerStatusEtc)
  })
_sym_db.RegisterMessage(GrpcPlayerStatusEtc)

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

GrpcPopupMenuList = _reflection.GeneratedProtocolMessageType('GrpcPopupMenuList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPOPUPMENULIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPopupMenuList)
  })
_sym_db.RegisterMessage(GrpcPopupMenuList)

GrpcClilocDataList = _reflection.GeneratedProtocolMessageType('GrpcClilocDataList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCLILOCDATALIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcClilocDataList)
  })
_sym_db.RegisterMessage(GrpcClilocDataList)

GrpcGameObjectList = _reflection.GeneratedProtocolMessageType('GrpcGameObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCGAMEOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcGameObjectList)
  })
_sym_db.RegisterMessage(GrpcGameObjectList)

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

GrpcItemList = _reflection.GeneratedProtocolMessageType('GrpcItemList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCITEMLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcItemList)
  })
_sym_db.RegisterMessage(GrpcItemList)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Config)
  })
_sym_db.RegisterMessage(Config)

GrpcSkillList = _reflection.GeneratedProtocolMessageType('GrpcSkillList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSKILLLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSkillList)
  })
_sym_db.RegisterMessage(GrpcSkillList)

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

GrpcSerialList = _reflection.GeneratedProtocolMessageType('GrpcSerialList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSERIALLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSerialList)
  })
_sym_db.RegisterMessage(GrpcSerialList)

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
  _GRPCITEMDATA._serialized_start=39
  _GRPCITEMDATA._serialized_end=114
  _GRPCCLILOCDATA._serialized_start=116
  _GRPCCLILOCDATA._serialized_end=191
  _GRPCGAMEOBJECTDATA._serialized_start=194
  _GRPCGAMEOBJECTDATA._serialized_end=419
  _GRPCSKILL._serialized_start=421
  _GRPCSKILL._serialized_end=538
  _GRPCPLAYERSTATUS._serialized_start=541
  _GRPCPLAYERSTATUS._serialized_end=777
  _GRPCPLAYERSTATUSETC._serialized_start=779
  _GRPCPLAYERSTATUSETC._serialized_end=841
  _GRPCGAMEOBJECTSIMPLEDATA._serialized_start=843
  _GRPCGAMEOBJECTSIMPLEDATA._serialized_end=899
  _GRPCGAMEOBJECTINFOLIST._serialized_start=901
  _GRPCGAMEOBJECTINFOLIST._serialized_end=961
  _GRPCPOPUPMENULIST._serialized_start=963
  _GRPCPOPUPMENULIST._serialized_end=997
  _GRPCCLILOCDATALIST._serialized_start=999
  _GRPCCLILOCDATALIST._serialized_end=1067
  _GRPCGAMEOBJECTLIST._serialized_start=1069
  _GRPCGAMEOBJECTLIST._serialized_end=1141
  _GRPCGAMEOBJECTSIMPLELIST._serialized_start=1143
  _GRPCGAMEOBJECTSIMPLELIST._serialized_end=1233
  _SEMAPHOREACTION._serialized_start=1235
  _SEMAPHOREACTION._serialized_end=1266
  _GRPCITEMLIST._serialized_start=1268
  _GRPCITEMLIST._serialized_end=1322
  _CONFIG._serialized_start=1324
  _CONFIG._serialized_end=1346
  _GRPCSKILLLIST._serialized_start=1348
  _GRPCSKILLLIST._serialized_end=1401
  _GRPCCONTAINERDATA._serialized_start=1403
  _GRPCCONTAINERDATA._serialized_end=1507
  _GRPCCONTAINERDATALIST._serialized_start=1509
  _GRPCCONTAINERDATALIST._serialized_end=1582
  _GRPCSERIALLIST._serialized_start=1584
  _GRPCSERIALLIST._serialized_end=1617
  _STATES._serialized_start=1620
  _STATES._serialized_end=2564
  _ACTIONS._serialized_start=2567
  _ACTIONS._serialized_end=2705
  _UOSERVICE._serialized_start=2708
  _UOSERVICE._serialized_end=3107
# @@protoc_insertion_point(module_scope)
