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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fUoService.proto\x12\tuoservice\"\x07\n\x05\x45mpty\"R\n\x0eGrpcMobileData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\x12\x0c\n\x04race\x18\x04 \x01(\r\x12\x0e\n\x06serial\x18\x05 \x01(\r\"K\n\x0cGrpcItemData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05layer\x18\x02 \x01(\r\x12\x0e\n\x06serial\x18\x03 \x01(\r\x12\x0e\n\x06\x61mount\x18\x04 \x01(\r\"\x1f\n\x0fSemaphoreAction\x12\x0c\n\x04mode\x18\x01 \x01(\t\";\n\x0eGrpcMobileList\x12)\n\x06mobile\x18\x01 \x03(\x0b\x32\x19.uoservice.GrpcMobileData\"5\n\x0cGrpcItemList\x12%\n\x04item\x18\x01 \x03(\x0b\x32\x17.uoservice.GrpcItemData\"\x16\n\x06\x43onfig\x12\x0c\n\x04name\x18\x01 \x01(\t\"8\n\x0cPlayerStatus\x12\x0b\n\x03str\x18\x01 \x01(\r\x12\x0b\n\x03\x64\x65x\x18\x02 \x01(\r\x12\x0e\n\x06intell\x18\x03 \x01(\r\"\xfc\x01\n\x06States\x12-\n\nmobileList\x18\x01 \x01(\x0b\x32\x19.uoservice.GrpcMobileList\x12.\n\rworldItemList\x18\x02 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12\x31\n\x10\x65quippedItemList\x18\x03 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12\x31\n\x10\x62\x61\x63kpackItemList\x18\x04 \x01(\x0b\x32\x17.uoservice.GrpcItemList\x12-\n\x0cplayerStatus\x18\x05 \x01(\x0b\x32\x17.uoservice.PlayerStatus\"\"\n\rWalkDirection\x12\x11\n\tdirection\x18\x01 \x01(\r\"x\n\x07\x41\x63tions\x12\x12\n\nactionType\x18\x01 \x01(\r\x12\x14\n\x0cmobileSerial\x18\x02 \x01(\r\x12\x12\n\nitemSerial\x18\x03 \x01(\r\x12/\n\rwalkDirection\x18\x04 \x01(\x0b\x32\x18.uoservice.WalkDirection2\xa7\x02\n\tUoService\x12-\n\x05Reset\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12/\n\x07ReadObs\x12\x11.uoservice.Config\x1a\x11.uoservice.States\x12\x30\n\x08WriteAct\x12\x12.uoservice.Actions\x1a\x10.uoservice.Empty\x12\x43\n\x13\x41\x63tSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Empty\x12\x43\n\x13ObsSemaphoreControl\x12\x1a.uoservice.SemaphoreAction\x1a\x10.uoservice.Emptyb\x06proto3')



_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_GRPCMOBILEDATA = DESCRIPTOR.message_types_by_name['GrpcMobileData']
_GRPCITEMDATA = DESCRIPTOR.message_types_by_name['GrpcItemData']
_SEMAPHOREACTION = DESCRIPTOR.message_types_by_name['SemaphoreAction']
_GRPCMOBILELIST = DESCRIPTOR.message_types_by_name['GrpcMobileList']
_GRPCITEMLIST = DESCRIPTOR.message_types_by_name['GrpcItemList']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']
_PLAYERSTATUS = DESCRIPTOR.message_types_by_name['PlayerStatus']
_STATES = DESCRIPTOR.message_types_by_name['States']
_WALKDIRECTION = DESCRIPTOR.message_types_by_name['WalkDirection']
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

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.Config)
  })
_sym_db.RegisterMessage(Config)

PlayerStatus = _reflection.GeneratedProtocolMessageType('PlayerStatus', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERSTATUS,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.PlayerStatus)
  })
_sym_db.RegisterMessage(PlayerStatus)

States = _reflection.GeneratedProtocolMessageType('States', (_message.Message,), {
  'DESCRIPTOR' : _STATES,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.States)
  })
_sym_db.RegisterMessage(States)

WalkDirection = _reflection.GeneratedProtocolMessageType('WalkDirection', (_message.Message,), {
  'DESCRIPTOR' : _WALKDIRECTION,
  '__module__' : 'UoService_pb2'
  # @@protoc_insertion_point(class_scope:uoservice.WalkDirection)
  })
_sym_db.RegisterMessage(WalkDirection)

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
  _SEMAPHOREACTION._serialized_start=200
  _SEMAPHOREACTION._serialized_end=231
  _GRPCMOBILELIST._serialized_start=233
  _GRPCMOBILELIST._serialized_end=292
  _GRPCITEMLIST._serialized_start=294
  _GRPCITEMLIST._serialized_end=347
  _CONFIG._serialized_start=349
  _CONFIG._serialized_end=371
  _PLAYERSTATUS._serialized_start=373
  _PLAYERSTATUS._serialized_end=429
  _STATES._serialized_start=432
  _STATES._serialized_end=684
  _WALKDIRECTION._serialized_start=686
  _WALKDIRECTION._serialized_end=720
  _ACTIONS._serialized_start=722
  _ACTIONS._serialized_end=842
  _UOSERVICE._serialized_start=845
  _UOSERVICE._serialized_end=1140
# @@protoc_insertion_point(module_scope)
