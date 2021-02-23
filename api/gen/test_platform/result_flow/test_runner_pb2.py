# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/result_flow/test_runner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.test_platform.result_flow import common_pb2 as test__platform_dot_result__flow_dot_common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/result_flow/test_runner.proto',
  package='test_platform.result_flow',
  syntax='proto3',
  serialized_options=b'ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flow',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+test_platform/result_flow/test_runner.proto\x12\x19test_platform.result_flow\x1a&test_platform/result_flow/common.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe4\x01\n\x11TestRunnerRequest\x12\x36\n\x0btest_runner\x18\x01 \x01(\x0b\x32!.test_platform.result_flow.Source\x12\x33\n\x08test_run\x18\x02 \x01(\x0b\x32!.test_platform.result_flow.Target\x12\x34\n\ttest_case\x18\x03 \x01(\x0b\x32!.test_platform.result_flow.Target\x12,\n\x08\x64\x65\x61\x64line\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"E\n\x12TestRunnerResponse\x12/\n\x05state\x18\x01 \x01(\x0e\x32 .test_platform.result_flow.StateBEZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flowb\x06proto3'
  ,
  dependencies=[test__platform_dot_result__flow_dot_common__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_TESTRUNNERREQUEST = _descriptor.Descriptor(
  name='TestRunnerRequest',
  full_name='test_platform.result_flow.TestRunnerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_runner', full_name='test_platform.result_flow.TestRunnerRequest.test_runner', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_run', full_name='test_platform.result_flow.TestRunnerRequest.test_run', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_case', full_name='test_platform.result_flow.TestRunnerRequest.test_case', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deadline', full_name='test_platform.result_flow.TestRunnerRequest.deadline', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=148,
  serialized_end=376,
)


_TESTRUNNERRESPONSE = _descriptor.Descriptor(
  name='TestRunnerResponse',
  full_name='test_platform.result_flow.TestRunnerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='test_platform.result_flow.TestRunnerResponse.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=378,
  serialized_end=447,
)

_TESTRUNNERREQUEST.fields_by_name['test_runner'].message_type = test__platform_dot_result__flow_dot_common__pb2._SOURCE
_TESTRUNNERREQUEST.fields_by_name['test_run'].message_type = test__platform_dot_result__flow_dot_common__pb2._TARGET
_TESTRUNNERREQUEST.fields_by_name['test_case'].message_type = test__platform_dot_result__flow_dot_common__pb2._TARGET
_TESTRUNNERREQUEST.fields_by_name['deadline'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TESTRUNNERRESPONSE.fields_by_name['state'].enum_type = test__platform_dot_result__flow_dot_common__pb2._STATE
DESCRIPTOR.message_types_by_name['TestRunnerRequest'] = _TESTRUNNERREQUEST
DESCRIPTOR.message_types_by_name['TestRunnerResponse'] = _TESTRUNNERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestRunnerRequest = _reflection.GeneratedProtocolMessageType('TestRunnerRequest', (_message.Message,), {
  'DESCRIPTOR' : _TESTRUNNERREQUEST,
  '__module__' : 'test_platform.result_flow.test_runner_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.result_flow.TestRunnerRequest)
  })
_sym_db.RegisterMessage(TestRunnerRequest)

TestRunnerResponse = _reflection.GeneratedProtocolMessageType('TestRunnerResponse', (_message.Message,), {
  'DESCRIPTOR' : _TESTRUNNERRESPONSE,
  '__module__' : 'test_platform.result_flow.test_runner_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.result_flow.TestRunnerResponse)
  })
_sym_db.RegisterMessage(TestRunnerResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
