# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/execution/param.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/execution/param.proto',
  package='test_platform.execution',
  syntax='proto3',
  serialized_options=b'ZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/execution',
  serialized_pb=b'\n#test_platform/execution/param.proto\x12\x17test_platform.execution\"\x1f\n\x05Param\x12\x16\n\x0eupload_crashes\x18\x01 \x01(\x08\x42\x43ZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/executionb\x06proto3'
)




_PARAM = _descriptor.Descriptor(
  name='Param',
  full_name='test_platform.execution.Param',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='upload_crashes', full_name='test_platform.execution.Param.upload_crashes', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=64,
  serialized_end=95,
)

DESCRIPTOR.message_types_by_name['Param'] = _PARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Param = _reflection.GeneratedProtocolMessageType('Param', (_message.Message,), {
  'DESCRIPTOR' : _PARAM,
  '__module__' : 'test_platform.execution.param_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.execution.Param)
  })
_sym_db.RegisterMessage(Param)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
