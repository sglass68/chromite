# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/skylab_local_state/common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/skylab_local_state/common.proto',
  package='test_platform.skylab_local_state',
  syntax='proto3',
  serialized_options=b'ZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_local_state',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-test_platform/skylab_local_state/common.proto\x12 test_platform.skylab_local_state\"o\n\x06\x43onfig\x12\x15\n\radmin_service\x18\x01 \x01(\t\x12\x14\n\x0c\x61utotest_dir\x18\x02 \x01(\t\x12\x1e\n\x16\x63ros_inventory_service\x18\x03 \x01(\t\x12\x18\n\x10\x63ros_ufs_service\x18\x04 \x01(\tBLZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_local_stateb\x06proto3'
)




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='test_platform.skylab_local_state.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='admin_service', full_name='test_platform.skylab_local_state.Config.admin_service', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='autotest_dir', full_name='test_platform.skylab_local_state.Config.autotest_dir', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cros_inventory_service', full_name='test_platform.skylab_local_state.Config.cros_inventory_service', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cros_ufs_service', full_name='test_platform.skylab_local_state.Config.cros_ufs_service', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=83,
  serialized_end=194,
)

DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'test_platform.skylab_local_state.common_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.skylab_local_state.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
