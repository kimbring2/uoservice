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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fUoService.proto\x12\tuoservice\"\x07\n\x05\x45mpty\"K\n\x0eGrpcClilocData\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\r\n\x05\x61\x66\x66ix\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"s\n\x14GrpcMobileObjectData\x12\x10\n\x08\x64istance\x18\x01 \x01(\r\x12\r\n\x05gameX\x18\x02 \x01(\r\x12\r\n\x05gameY\x18\x03 \x01(\r\x12\x0e\n\x06serial\x18\x04 \x01(\r\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\r\n\x05title\x18\x06 \x01(\t\"\xb5\x01\n\x12GrpcItemObjectData\x12\x10\n\x08\x64istance\x18\x01 \x01(\r\x12\r\n\x05gameX\x18\x02 \x01(\r\x12\r\n\x05gameY\x18\x03 \x01(\r\x12\x0e\n\x06serial\x18\x04 \x01(\r\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x10\n\x08isCorpse\x18\x06 \x01(\x08\x12\x0e\n\x06\x61mount\x18\x07 \x01(\r\x12\r\n\x05price\x18\x08 \x01(\r\x12\r\n\x05layer\x18\t \x01(\r\x12\x11\n\tcontainer\x18\n \x01(\r\"u\n\tGrpcSkill\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\r\x12\x13\n\x0bisClickable\x18\x03 \x01(\x08\x12\r\n\x05value\x18\x04 \x01(\r\x12\x0c\n\x04\x62\x61se\x18\x05 \x01(\r\x12\x0b\n\x03\x63\x61p\x18\x06 \x01(\r\x12\x0c\n\x04lock\x18\x07 \x01(\r\"\xec\x01\n\x10GrpcPlayerStatus\x12\x0b\n\x03str\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x65x\x18\x02 \x01(\r\x12\x0e\n\x06intell\x18\x03 \x01(\r\x12\x0c\n\x04hits\x18\x04 \x01(\r\x12\x0f\n\x07hitsMax\x18\x05 \x01(\r\x12\x0f\n\x07stamina\x18\x06 \x01(\r\x12\x12\n\nstaminaMax\x18\x07 \x01(\r\x12\x0c\n\x04mana\x18\x08 \x01(\r\x12\x0f\n\x07manaMax\x18\t \x01(\r\x12\x0c\n\x04gold\x18\n \x01(\r\x12\x1a\n\x12physicalResistance\x18\x0b \x01(\r\x12\x0e\n\x06weight\x18\x0c \x01(\r\x12\x11\n\tweightMax\x18\r \x01(\r\"\x86\x01\n\x10GrpcPlayerObject\x12\r\n\x05gameX\x18\x01 \x01(\r\x12\r\n\x05gameY\x18\x02 \x01(\r\x12\x0e\n\x06serial\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\r\n\x05title\x18\x05 \x01(\t\x12\x16\n\x0eholdItemSerial\x18\x06 \x01(\r\x12\x0f\n\x07warMode\x18\x07 \x01(\x08\"8\n\x16GrpcGameObjectInfoList\x12\x0e\n\x06gameXs\x18\x01 \x03(\r\x12\x0e\n\x06gameYs\x18\x02 \x03(\r\"\"\n\x11GrpcPopupMenuList\x12\r\n\x05menus\x18\x01 \x03(\t\"D\n\x12GrpcClilocDataList\x12.\n\x0b\x63lilocDatas\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcClilocData\"N\n\x14GrpcMobileObjectList\x12\x36\n\rmobileObjects\x18\x01 \x03(\x0b\x32\x1f.uoservice.GrpcMobileObjectData\"H\n\x12GrpcItemObjectList\x12\x32\n\x0bitemObjects\x18\x01 \x03(\x0b\x32\x1d.uoservice.GrpcItemObjectData\"\x1f\n\x0fSemaphoreAction\x12\x0c\n\x04mode\x18\x01 \x01(\t\"\x16\n\x06\x43onfig\x12\x0c\n\x04init\x18\x01 \x01(\x08\"5\n\rGrpcSkillList\x12$\n\x06skills\x18\x01 \x03(\x0b\x32\x14.uoservice.GrpcSkill\"\xe9\x03\n\x06States\x12\x31\n\x0cplayerObject\x18\x01 \x01(\x0b\x32\x1b.uoservice.GrpcPlayerObject\x12\x34\n\rWorldItemList\x18\x02 \x01(\x0b\x32\x1d.uoservice.GrpcItemObjectList\x12\x38\n\x0fWorldMobileList\x18\x03 \x01(\x0b\x32\x1f.uoservice.GrpcMobileObjectList\x12\x33\n\rpopupMenuList\x18\x04 \x01(\x0b\x32\x1c.uoservice.GrpcPopupMenuList\x12\x35\n\x0e\x63lilocDataList\x18\x05 \x01(\x0b\x32\x1d.uoservice.GrpcClilocDataList\x12\x31\n\x0cplayerStatus\x18\x06 \x01(\x0b\x32\x1b.uoservice.GrpcPlayerStatus\x12\x31\n\x0fplayerSkillList\x18\x07 \x01(\x0b\x32\x18.uoservice.GrpcSkillList\x12?\n\x14staticObjectInfoList\x18\x08 \x01(\x0b\x32!.uoservice.GrpcGameObjectInfoList\x12)\n\rreplayActions\x18\t \x01(\x0b\x32\x12.uoservice.Actions\"\x8a\x01\n\x07\x41\x63tions\x12\x12\n\nactionType\x18\x01 \x01(\r\x12\x12\n\nitemSerial\x18\x02 \x01(\r\x12\x14\n\x0cmobileSerial\x18\x03 \x01(\r\x12\x15\n\rwalkDirection\x18\x04 \x01(\r\x12\r\n\x05index\x18\x05 \x01(\r\x12\x0e\n\x06\x61mount\x18\x06 \x01(\r\x12\x0b\n\x03run\x18\x07 \x01(\x08\x32\x8f\x03\n\tUoService\x12-\n\x05Reset\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12/\n\x07ReadObs\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x30\n\x08WriteAct\x12\x12.uoservice.Actions\x1a\x10.uoservice.Empty\x12\x43\n\x13\x41\x63tSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x43\n\x13ObsSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x32\n\nReadReplay\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x32\n\x0bReadMPQFile\x12\x11.uoservice.Config\x1a\x10.uoservice.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_GRPCCLILOCDATA = DESCRIPTOR.message_types_by_name['GrpcClilocData']
_GRPCMOBILEOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcMobileObjectData']
_GRPCITEMOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcItemObjectData']
_GRPCSKILL = DESCRIPTOR.message_types_by_name['GrpcSkill']
_GRPCPLAYERSTATUS = DESCRIPTOR.message_types_by_name['GrpcPlayerStatus']
_GRPCPLAYEROBJECT = DESCRIPTOR.message_types_by_name['GrpcPlayerObject']
_GRPCGAMEOBJECTINFOLIST = DESCRIPTOR.message_types_by_name['GrpcGameObjectInfoList']
_GRPCPOPUPMENULIST = DESCRIPTOR.message_types_by_name['GrpcPopupMenuList']
_GRPCCLILOCDATALIST = DESCRIPTOR.message_types_by_name['GrpcClilocDataList']
_GRPCMOBILEOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcMobileObjectList']
_GRPCITEMOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcItemObjectList']
_SEMAPHOREACTION = DESCRIPTOR.message_types_by_name['SemaphoreAction']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']
_GRPCSKILLLIST = DESCRIPTOR.message_types_by_name['GrpcSkillList']
_STATES = DESCRIPTOR.message_types_by_name['States']
_ACTIONS = DESCRIPTOR.message_types_by_name['Actions']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Empty)
  })
_sym_db.RegisterMessage(Empty)

GrpcClilocData = _reflection.GeneratedProtocolMessageType('GrpcClilocData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCLILOCDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcClilocData)
  })
_sym_db.RegisterMessage(GrpcClilocData)

GrpcMobileObjectData = _reflection.GeneratedProtocolMessageType('GrpcMobileObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCMOBILEOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcMobileObjectData)
  })
_sym_db.RegisterMessage(GrpcMobileObjectData)

GrpcItemObjectData = _reflection.GeneratedProtocolMessageType('GrpcItemObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCITEMOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcItemObjectData)
  })
_sym_db.RegisterMessage(GrpcItemObjectData)

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

GrpcPlayerObject = _reflection.GeneratedProtocolMessageType('GrpcPlayerObject', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYEROBJECT,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerObject)
  })
_sym_db.RegisterMessage(GrpcPlayerObject)

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

GrpcMobileObjectList = _reflection.GeneratedProtocolMessageType('GrpcMobileObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCMOBILEOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcMobileObjectList)
  })
_sym_db.RegisterMessage(GrpcMobileObjectList)

GrpcItemObjectList = _reflection.GeneratedProtocolMessageType('GrpcItemObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCITEMOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcItemObjectList)
  })
_sym_db.RegisterMessage(GrpcItemObjectList)

SemaphoreAction = _reflection.GeneratedProtocolMessageType('SemaphoreAction', (_message.Message,), {
  'DESCRIPTOR' : _SEMAPHOREACTION,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.SemaphoreAction)
  })
_sym_db.RegisterMessage(SemaphoreAction)

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
  _GRPCCLILOCDATA._serialized_start=39
  _GRPCCLILOCDATA._serialized_end=114
  _GRPCMOBILEOBJECTDATA._serialized_start=116
  _GRPCMOBILEOBJECTDATA._serialized_end=231
  _GRPCITEMOBJECTDATA._serialized_start=234
  _GRPCITEMOBJECTDATA._serialized_end=415
  _GRPCSKILL._serialized_start=417
  _GRPCSKILL._serialized_end=534
  _GRPCPLAYERSTATUS._serialized_start=537
  _GRPCPLAYERSTATUS._serialized_end=773
  _GRPCPLAYEROBJECT._serialized_start=776
  _GRPCPLAYEROBJECT._serialized_end=910
  _GRPCGAMEOBJECTINFOLIST._serialized_start=912
  _GRPCGAMEOBJECTINFOLIST._serialized_end=968
  _GRPCPOPUPMENULIST._serialized_start=970
  _GRPCPOPUPMENULIST._serialized_end=1004
  _GRPCCLILOCDATALIST._serialized_start=1006
  _GRPCCLILOCDATALIST._serialized_end=1074
  _GRPCMOBILEOBJECTLIST._serialized_start=1076
  _GRPCMOBILEOBJECTLIST._serialized_end=1154
  _GRPCITEMOBJECTLIST._serialized_start=1156
  _GRPCITEMOBJECTLIST._serialized_end=1228
  _SEMAPHOREACTION._serialized_start=1230
  _SEMAPHOREACTION._serialized_end=1261
  _CONFIG._serialized_start=1263
  _CONFIG._serialized_end=1285
  _GRPCSKILLLIST._serialized_start=1287
  _GRPCSKILLLIST._serialized_end=1340
  _STATES._serialized_start=1343
  _STATES._serialized_end=1832
  _ACTIONS._serialized_start=1835
  _ACTIONS._serialized_end=1973
  _UOSERVICE._serialized_start=1976
  _UOSERVICE._serialized_end=2375
# @@protoc_insertion_point(module_scope)
