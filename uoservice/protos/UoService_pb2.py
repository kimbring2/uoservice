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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fUoService.proto\x12\tuoservice\"\x07\n\x05\x45mpty\"\x9e\x01\n\x10GrpcPlayerObject\x12\r\n\x05gameX\x18\x01 \x01(\r\x12\r\n\x05gameY\x18\x02 \x01(\r\x12\x0e\n\x06serial\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\r\n\x05title\x18\x05 \x01(\t\x12\x16\n\x0eholdItemSerial\x18\x06 \x01(\r\x12\x0f\n\x07warMode\x18\x07 \x01(\x08\x12\x16\n\x0etargetingState\x18\x08 \x01(\r\"\xb7\x01\n\x14GrpcMobileObjectData\x12\x0c\n\x04hits\x18\x01 \x01(\r\x12\x0f\n\x07hitsMax\x18\x02 \x01(\r\x12\x0c\n\x04race\x18\x03 \x01(\r\x12\x10\n\x08\x64istance\x18\x04 \x01(\r\x12\r\n\x05gameX\x18\x05 \x01(\r\x12\r\n\x05gameY\x18\x06 \x01(\r\x12\x0e\n\x06serial\x18\x07 \x01(\r\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\r\n\x05title\x18\t \x01(\t\x12\x15\n\rnotorietyFlag\x18\n \x01(\r\"\xb5\x01\n\x12GrpcItemObjectData\x12\x10\n\x08\x64istance\x18\x01 \x01(\r\x12\r\n\x05gameX\x18\x02 \x01(\r\x12\r\n\x05gameY\x18\x03 \x01(\r\x12\x0e\n\x06serial\x18\x04 \x01(\r\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x10\n\x08isCorpse\x18\x06 \x01(\x08\x12\x0e\n\x06\x61mount\x18\x07 \x01(\r\x12\r\n\x05price\x18\x08 \x01(\r\x12\r\n\x05layer\x18\t \x01(\r\x12\x11\n\tcontainer\x18\n \x01(\r\"a\n\x12GrpcLandObjectData\x12\r\n\x05index\x18\x01 \x01(\r\x12\r\n\x05gameX\x18\x02 \x01(\r\x12\r\n\x05gameY\x18\x03 \x01(\r\x12\x10\n\x08\x64istance\x18\x04 \x01(\r\x12\x0c\n\x04name\x18\x05 \x01(\t\"c\n\x14GrpcStaticObjectData\x12\r\n\x05index\x18\x01 \x01(\r\x12\r\n\x05gameX\x18\x02 \x01(\r\x12\r\n\x05gameY\x18\x03 \x01(\r\x12\x10\n\x08\x64istance\x18\x04 \x01(\r\x12\x0c\n\x04name\x18\x05 \x01(\t\"\xec\x01\n\x10GrpcPlayerStatus\x12\x0b\n\x03str\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x65x\x18\x02 \x01(\r\x12\x0e\n\x06intell\x18\x03 \x01(\r\x12\x0c\n\x04hits\x18\x04 \x01(\r\x12\x0f\n\x07hitsMax\x18\x05 \x01(\r\x12\x0f\n\x07stamina\x18\x06 \x01(\r\x12\x12\n\nstaminaMax\x18\x07 \x01(\r\x12\x0c\n\x04mana\x18\x08 \x01(\r\x12\x0f\n\x07manaMax\x18\t \x01(\r\x12\x0c\n\x04gold\x18\n \x01(\r\x12\x1a\n\x12physicalResistance\x18\x0b \x01(\r\x12\x0e\n\x06weight\x18\x0c \x01(\r\x12\x11\n\tweightMax\x18\r \x01(\r\"u\n\tGrpcSkill\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\r\x12\x13\n\x0bisClickable\x18\x03 \x01(\x08\x12\r\n\x05value\x18\x04 \x01(\r\x12\x0c\n\x04\x62\x61se\x18\x05 \x01(\r\x12\x0b\n\x03\x63\x61p\x18\x06 \x01(\r\x12\x0c\n\x04lock\x18\x07 \x01(\r\"6\n\x14GrpcObstacleInfoList\x12\x0e\n\x06gameXs\x18\x01 \x03(\r\x12\x0e\n\x06gameYs\x18\x02 \x03(\r\"-\n\rGrpcPopupMenu\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x02 \x01(\x08\"K\n\x0eGrpcClilocData\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\r\n\x05\x61\x66\x66ix\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"<\n\x11GrpcPopupMenuList\x12\'\n\x05menus\x18\x01 \x03(\x0b\x32\x18.uoservice.GrpcPopupMenu\"D\n\x12GrpcClilocDataList\x12.\n\x0b\x63lilocDatas\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcClilocData\"N\n\x14GrpcMobileObjectList\x12\x36\n\rmobileObjects\x18\x01 \x03(\x0b\x32\x1f.uoservice.GrpcMobileObjectData\"H\n\x12GrpcItemObjectList\x12\x32\n\x0bitemObjects\x18\x01 \x03(\x0b\x32\x1d.uoservice.GrpcItemObjectData\"H\n\x12GrpcLandObjectList\x12\x32\n\x0blandObjects\x18\x01 \x03(\x0b\x32\x1d.uoservice.GrpcLandObjectData\"N\n\x14GrpcStaticObjectList\x12\x36\n\rstaticObjects\x18\x01 \x03(\x0b\x32\x1f.uoservice.GrpcStaticObjectData\"\x1f\n\x0fSemaphoreAction\x12\x0c\n\x04mode\x18\x01 \x01(\t\"\x16\n\x06\x43onfig\x12\x0c\n\x04init\x18\x01 \x01(\x08\"5\n\rGrpcSkillList\x12$\n\x06skills\x18\x01 \x03(\x0b\x32\x14.uoservice.GrpcSkill\"\xae\x04\n\nGrpcStates\x12\x31\n\x0cplayerObject\x18\x01 \x01(\x0b\x32\x1b.uoservice.GrpcPlayerObject\x12\x34\n\rWorldItemList\x18\x02 \x01(\x0b\x32\x1d.uoservice.GrpcItemObjectList\x12\x38\n\x0fWorldMobileList\x18\x03 \x01(\x0b\x32\x1f.uoservice.GrpcMobileObjectList\x12\x33\n\rpopupMenuList\x18\x04 \x01(\x0b\x32\x1c.uoservice.GrpcPopupMenuList\x12\x35\n\x0e\x63lilocDataList\x18\x05 \x01(\x0b\x32\x1d.uoservice.GrpcClilocDataList\x12\x31\n\x0cplayerStatus\x18\x06 \x01(\x0b\x32\x1b.uoservice.GrpcPlayerStatus\x12\x31\n\x0fplayerSkillList\x18\x07 \x01(\x0b\x32\x18.uoservice.GrpcSkillList\x12\x35\n\x0elandObjectList\x18\x08 \x01(\x0b\x32\x1d.uoservice.GrpcLandObjectList\x12\x39\n\x10staticObjectList\x18\t \x01(\x0b\x32\x1f.uoservice.GrpcStaticObjectList\x12\x39\n\x10obstacleInfoList\x18\n \x01(\x0b\x32\x1f.uoservice.GrpcObstacleInfoList\"\x8f\x01\n\nGrpcAction\x12\x12\n\nactionType\x18\x01 \x01(\r\x12\x14\n\x0csourceSerial\x18\x02 \x01(\r\x12\x14\n\x0ctargetSerial\x18\x03 \x01(\r\x12\x15\n\rwalkDirection\x18\x04 \x01(\r\x12\r\n\x05index\x18\x05 \x01(\r\x12\x0e\n\x06\x61mount\x18\x06 \x01(\r\x12\x0b\n\x03run\x18\x07 \x01(\x08\x32\x9e\x03\n\tUoService\x12\x31\n\x05Reset\x12\x11.uoservice.Config\x1a\x15.uoservice.GrpcStates\x12\x33\n\x07ReadObs\x12\x11.uoservice.Config\x1a\x15.uoservice.GrpcStates\x12\x33\n\x08WriteAct\x12\x15.uoservice.GrpcAction\x1a\x10.uoservice.Empty\x12\x43\n\x13\x41\x63tSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x43\n\x13ObsSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x36\n\nReadReplay\x12\x11.uoservice.Config\x1a\x15.uoservice.GrpcStates\x12\x32\n\x0bReadMPQFile\x12\x11.uoservice.Config\x1a\x10.uoservice.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_GRPCPLAYEROBJECT = DESCRIPTOR.message_types_by_name['GrpcPlayerObject']
_GRPCMOBILEOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcMobileObjectData']
_GRPCITEMOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcItemObjectData']
_GRPCLANDOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcLandObjectData']
_GRPCSTATICOBJECTDATA = DESCRIPTOR.message_types_by_name['GrpcStaticObjectData']
_GRPCPLAYERSTATUS = DESCRIPTOR.message_types_by_name['GrpcPlayerStatus']
_GRPCSKILL = DESCRIPTOR.message_types_by_name['GrpcSkill']
_GRPCOBSTACLEINFOLIST = DESCRIPTOR.message_types_by_name['GrpcObstacleInfoList']
_GRPCPOPUPMENU = DESCRIPTOR.message_types_by_name['GrpcPopupMenu']
_GRPCCLILOCDATA = DESCRIPTOR.message_types_by_name['GrpcClilocData']
_GRPCPOPUPMENULIST = DESCRIPTOR.message_types_by_name['GrpcPopupMenuList']
_GRPCCLILOCDATALIST = DESCRIPTOR.message_types_by_name['GrpcClilocDataList']
_GRPCMOBILEOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcMobileObjectList']
_GRPCITEMOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcItemObjectList']
_GRPCLANDOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcLandObjectList']
_GRPCSTATICOBJECTLIST = DESCRIPTOR.message_types_by_name['GrpcStaticObjectList']
_SEMAPHOREACTION = DESCRIPTOR.message_types_by_name['SemaphoreAction']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']
_GRPCSKILLLIST = DESCRIPTOR.message_types_by_name['GrpcSkillList']
_GRPCSTATES = DESCRIPTOR.message_types_by_name['GrpcStates']
_GRPCACTION = DESCRIPTOR.message_types_by_name['GrpcAction']
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Empty)
  })
_sym_db.RegisterMessage(Empty)

GrpcPlayerObject = _reflection.GeneratedProtocolMessageType('GrpcPlayerObject', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYEROBJECT,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerObject)
  })
_sym_db.RegisterMessage(GrpcPlayerObject)

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

GrpcLandObjectData = _reflection.GeneratedProtocolMessageType('GrpcLandObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCLANDOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcLandObjectData)
  })
_sym_db.RegisterMessage(GrpcLandObjectData)

GrpcStaticObjectData = _reflection.GeneratedProtocolMessageType('GrpcStaticObjectData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSTATICOBJECTDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcStaticObjectData)
  })
_sym_db.RegisterMessage(GrpcStaticObjectData)

GrpcPlayerStatus = _reflection.GeneratedProtocolMessageType('GrpcPlayerStatus', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPLAYERSTATUS,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPlayerStatus)
  })
_sym_db.RegisterMessage(GrpcPlayerStatus)

GrpcSkill = _reflection.GeneratedProtocolMessageType('GrpcSkill', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSKILL,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcSkill)
  })
_sym_db.RegisterMessage(GrpcSkill)

GrpcObstacleInfoList = _reflection.GeneratedProtocolMessageType('GrpcObstacleInfoList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCOBSTACLEINFOLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcObstacleInfoList)
  })
_sym_db.RegisterMessage(GrpcObstacleInfoList)

GrpcPopupMenu = _reflection.GeneratedProtocolMessageType('GrpcPopupMenu', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPOPUPMENU,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcPopupMenu)
  })
_sym_db.RegisterMessage(GrpcPopupMenu)

GrpcClilocData = _reflection.GeneratedProtocolMessageType('GrpcClilocData', (_message.Message,), {
  'DESCRIPTOR' : _GRPCCLILOCDATA,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcClilocData)
  })
_sym_db.RegisterMessage(GrpcClilocData)

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

GrpcLandObjectList = _reflection.GeneratedProtocolMessageType('GrpcLandObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCLANDOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcLandObjectList)
  })
_sym_db.RegisterMessage(GrpcLandObjectList)

GrpcStaticObjectList = _reflection.GeneratedProtocolMessageType('GrpcStaticObjectList', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSTATICOBJECTLIST,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcStaticObjectList)
  })
_sym_db.RegisterMessage(GrpcStaticObjectList)

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

GrpcStates = _reflection.GeneratedProtocolMessageType('GrpcStates', (_message.Message,), {
  'DESCRIPTOR' : _GRPCSTATES,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcStates)
  })
_sym_db.RegisterMessage(GrpcStates)

GrpcAction = _reflection.GeneratedProtocolMessageType('GrpcAction', (_message.Message,), {
  'DESCRIPTOR' : _GRPCACTION,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.GrpcAction)
  })
_sym_db.RegisterMessage(GrpcAction)

_UOSERVICE = DESCRIPTOR.services_by_name['UoService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=30
  _EMPTY._serialized_end=37
  _GRPCPLAYEROBJECT._serialized_start=40
  _GRPCPLAYEROBJECT._serialized_end=198
  _GRPCMOBILEOBJECTDATA._serialized_start=201
  _GRPCMOBILEOBJECTDATA._serialized_end=384
  _GRPCITEMOBJECTDATA._serialized_start=387
  _GRPCITEMOBJECTDATA._serialized_end=568
  _GRPCLANDOBJECTDATA._serialized_start=570
  _GRPCLANDOBJECTDATA._serialized_end=667
  _GRPCSTATICOBJECTDATA._serialized_start=669
  _GRPCSTATICOBJECTDATA._serialized_end=768
  _GRPCPLAYERSTATUS._serialized_start=771
  _GRPCPLAYERSTATUS._serialized_end=1007
  _GRPCSKILL._serialized_start=1009
  _GRPCSKILL._serialized_end=1126
  _GRPCOBSTACLEINFOLIST._serialized_start=1128
  _GRPCOBSTACLEINFOLIST._serialized_end=1182
  _GRPCPOPUPMENU._serialized_start=1184
  _GRPCPOPUPMENU._serialized_end=1229
  _GRPCCLILOCDATA._serialized_start=1231
  _GRPCCLILOCDATA._serialized_end=1306
  _GRPCPOPUPMENULIST._serialized_start=1308
  _GRPCPOPUPMENULIST._serialized_end=1368
  _GRPCCLILOCDATALIST._serialized_start=1370
  _GRPCCLILOCDATALIST._serialized_end=1438
  _GRPCMOBILEOBJECTLIST._serialized_start=1440
  _GRPCMOBILEOBJECTLIST._serialized_end=1518
  _GRPCITEMOBJECTLIST._serialized_start=1520
  _GRPCITEMOBJECTLIST._serialized_end=1592
  _GRPCLANDOBJECTLIST._serialized_start=1594
  _GRPCLANDOBJECTLIST._serialized_end=1666
  _GRPCSTATICOBJECTLIST._serialized_start=1668
  _GRPCSTATICOBJECTLIST._serialized_end=1746
  _SEMAPHOREACTION._serialized_start=1748
  _SEMAPHOREACTION._serialized_end=1779
  _CONFIG._serialized_start=1781
  _CONFIG._serialized_end=1803
  _GRPCSKILLLIST._serialized_start=1805
  _GRPCSKILLLIST._serialized_end=1858
  _GRPCSTATES._serialized_start=1861
  _GRPCSTATES._serialized_end=2419
  _GRPCACTION._serialized_start=2422
  _GRPCACTION._serialized_end=2565
  _UOSERVICE._serialized_start=2568
  _UOSERVICE._serialized_end=2982
# @@protoc_insertion_point(module_scope)
