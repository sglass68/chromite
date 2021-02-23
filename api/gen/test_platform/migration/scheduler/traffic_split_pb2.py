# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/migration/scheduler/traffic_split.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen.test_platform import request_pb2 as test__platform_dot_request__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/migration/scheduler/traffic_split.proto',
  package='test_platform.migration.scheduler',
  syntax='proto3',
  serialized_options=b'ZKgo.chromium.org/chromiumos/infra/proto/go/test_platform/migration/scheduler',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n5test_platform/migration/scheduler/traffic_split.proto\x12!test_platform.migration.scheduler\x1a\x17\x63hromiumos/common.proto\x1a\x1btest_platform/request.proto\"\x91\x01\n\x0cTrafficSplit\x12\x36\n\x05rules\x18\x01 \x03(\x0b\x32\'.test_platform.migration.scheduler.Rule\x12I\n\x0fsuite_overrides\x18\x02 \x03(\x0b\x32\x30.test_platform.migration.scheduler.SuiteOverride\"\xc4\x01\n\x04Rule\x12;\n\x07request\x18\x01 \x01(\x0b\x32*.test_platform.migration.scheduler.Request\x12;\n\x07\x62\x61\x63kend\x18\x02 \x01(\x0e\x32*.test_platform.migration.scheduler.Backend\x12\x42\n\x0brequest_mod\x18\x03 \x01(\x0b\x32-.test_platform.migration.scheduler.RequestMod\"\x85\x01\n\x07Request\x12<\n\nscheduling\x18\x01 \x01(\x0b\x32(.test_platform.Request.Params.Scheduling\x12\r\n\x05model\x18\x02 \x01(\t\x12-\n\x0c\x62uild_target\x18\x03 \x01(\x0b\x32\x17.chromiumos.BuildTarget\"J\n\nRequestMod\x12<\n\nscheduling\x18\x01 \x01(\x0b\x32(.test_platform.Request.Params.Scheduling\"s\n\rSuiteOverride\x12+\n\x05suite\x18\x01 \x01(\x0b\x32\x1c.test_platform.Request.Suite\x12\x35\n\x04rule\x18\x02 \x01(\x0b\x32\'.test_platform.migration.scheduler.Rule*L\n\x07\x42\x61\x63kend\x12\x17\n\x13\x42\x41\x43KEND_UNSPECIFIED\x10\x00\x12\x14\n\x10\x42\x41\x43KEND_AUTOTEST\x10\x01\x12\x12\n\x0e\x42\x41\x43KEND_SKYLAB\x10\x02\x42MZKgo.chromium.org/chromiumos/infra/proto/go/test_platform/migration/schedulerb\x06proto3'
  ,
  dependencies=[chromiumos_dot_common__pb2.DESCRIPTOR,test__platform_dot_request__pb2.DESCRIPTOR,])

_BACKEND = _descriptor.EnumDescriptor(
  name='Backend',
  full_name='test_platform.migration.scheduler.Backend',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BACKEND_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BACKEND_AUTOTEST', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BACKEND_SKYLAB', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=822,
  serialized_end=898,
)
_sym_db.RegisterEnumDescriptor(_BACKEND)

Backend = enum_type_wrapper.EnumTypeWrapper(_BACKEND)
BACKEND_UNSPECIFIED = 0
BACKEND_AUTOTEST = 1
BACKEND_SKYLAB = 2



_TRAFFICSPLIT = _descriptor.Descriptor(
  name='TrafficSplit',
  full_name='test_platform.migration.scheduler.TrafficSplit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rules', full_name='test_platform.migration.scheduler.TrafficSplit.rules', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='suite_overrides', full_name='test_platform.migration.scheduler.TrafficSplit.suite_overrides', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=147,
  serialized_end=292,
)


_RULE = _descriptor.Descriptor(
  name='Rule',
  full_name='test_platform.migration.scheduler.Rule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='test_platform.migration.scheduler.Rule.request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='backend', full_name='test_platform.migration.scheduler.Rule.backend', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_mod', full_name='test_platform.migration.scheduler.Rule.request_mod', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=295,
  serialized_end=491,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='test_platform.migration.scheduler.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduling', full_name='test_platform.migration.scheduler.Request.scheduling', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model', full_name='test_platform.migration.scheduler.Request.model', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='test_platform.migration.scheduler.Request.build_target', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=494,
  serialized_end=627,
)


_REQUESTMOD = _descriptor.Descriptor(
  name='RequestMod',
  full_name='test_platform.migration.scheduler.RequestMod',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scheduling', full_name='test_platform.migration.scheduler.RequestMod.scheduling', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=629,
  serialized_end=703,
)


_SUITEOVERRIDE = _descriptor.Descriptor(
  name='SuiteOverride',
  full_name='test_platform.migration.scheduler.SuiteOverride',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='suite', full_name='test_platform.migration.scheduler.SuiteOverride.suite', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rule', full_name='test_platform.migration.scheduler.SuiteOverride.rule', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=705,
  serialized_end=820,
)

_TRAFFICSPLIT.fields_by_name['rules'].message_type = _RULE
_TRAFFICSPLIT.fields_by_name['suite_overrides'].message_type = _SUITEOVERRIDE
_RULE.fields_by_name['request'].message_type = _REQUEST
_RULE.fields_by_name['backend'].enum_type = _BACKEND
_RULE.fields_by_name['request_mod'].message_type = _REQUESTMOD
_REQUEST.fields_by_name['scheduling'].message_type = test__platform_dot_request__pb2._REQUEST_PARAMS_SCHEDULING
_REQUEST.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_REQUESTMOD.fields_by_name['scheduling'].message_type = test__platform_dot_request__pb2._REQUEST_PARAMS_SCHEDULING
_SUITEOVERRIDE.fields_by_name['suite'].message_type = test__platform_dot_request__pb2._REQUEST_SUITE
_SUITEOVERRIDE.fields_by_name['rule'].message_type = _RULE
DESCRIPTOR.message_types_by_name['TrafficSplit'] = _TRAFFICSPLIT
DESCRIPTOR.message_types_by_name['Rule'] = _RULE
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['RequestMod'] = _REQUESTMOD
DESCRIPTOR.message_types_by_name['SuiteOverride'] = _SUITEOVERRIDE
DESCRIPTOR.enum_types_by_name['Backend'] = _BACKEND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrafficSplit = _reflection.GeneratedProtocolMessageType('TrafficSplit', (_message.Message,), {
  'DESCRIPTOR' : _TRAFFICSPLIT,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.TrafficSplit)
  })
_sym_db.RegisterMessage(TrafficSplit)

Rule = _reflection.GeneratedProtocolMessageType('Rule', (_message.Message,), {
  'DESCRIPTOR' : _RULE,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.Rule)
  })
_sym_db.RegisterMessage(Rule)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.Request)
  })
_sym_db.RegisterMessage(Request)

RequestMod = _reflection.GeneratedProtocolMessageType('RequestMod', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTMOD,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.RequestMod)
  })
_sym_db.RegisterMessage(RequestMod)

SuiteOverride = _reflection.GeneratedProtocolMessageType('SuiteOverride', (_message.Message,), {
  'DESCRIPTOR' : _SUITEOVERRIDE,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.SuiteOverride)
  })
_sym_db.RegisterMessage(SuiteOverride)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
