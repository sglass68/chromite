# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/phosphorus/fetchcrashes.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from chromite.api.gen.test_platform.phosphorus import common_pb2 as test__platform_dot_phosphorus_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/phosphorus/fetchcrashes.proto',
  package='test_platform.phosphorus',
  syntax='proto3',
  serialized_options=_b('ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorus'),
  serialized_pb=_b('\n+test_platform/phosphorus/fetchcrashes.proto\x12\x18test_platform.phosphorus\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%test_platform/phosphorus/common.proto\"\xb8\x01\n\x13\x46\x65tchCrashesRequest\x12\x30\n\x06\x63onfig\x18\x01 \x01(\x0b\x32 .test_platform.phosphorus.Config\x12\x14\n\x0c\x64ut_hostname\x18\x02 \x01(\t\x12,\n\x08\x64\x65\x61\x64line\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0eupload_crashes\x18\x04 \x01(\x08\x12\x13\n\x0buse_staging\x18\x05 \x01(\x08\"\x7f\n\x0c\x43rashSummary\x12\x11\n\texec_name\x18\x01 \x01(\t\x12\x12\n\nupload_url\x18\x02 \x01(\t\x12$\n\x1cin_progress_integration_test\x18\x03 \x01(\t\x12\x0b\n\x03sig\x18\x04 \x01(\t\x12\x15\n\rfilename_base\x18\x05 \x01(\t\"\x9f\x02\n\x14\x46\x65tchCrashesResponse\x12\x43\n\x05state\x18\x01 \x01(\x0e\x32\x34.test_platform.phosphorus.FetchCrashesResponse.State\x12\x37\n\x07\x63rashes\x18\x02 \x03(\x0b\x32&.test_platform.phosphorus.CrashSummary\x12\x18\n\x10\x63rashes_rtd_only\x18\x04 \x03(\t\x12\x18\n\x10\x63rashes_tls_only\x18\x05 \x03(\t\"U\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\r\n\tSUCCEEDED\x10\x01\x12\n\n\x06\x46\x41ILED\x10\x02\x12\r\n\tTIMED_OUT\x10\x03\x12\x0b\n\x07\x41\x42ORTED\x10\x04\x42\x44ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorusb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,test__platform_dot_phosphorus_dot_common__pb2.DESCRIPTOR,])



_FETCHCRASHESRESPONSE_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='test_platform.phosphorus.FetchCrashesResponse.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCEEDED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TIMED_OUT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABORTED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=664,
  serialized_end=749,
)
_sym_db.RegisterEnumDescriptor(_FETCHCRASHESRESPONSE_STATE)


_FETCHCRASHESREQUEST = _descriptor.Descriptor(
  name='FetchCrashesRequest',
  full_name='test_platform.phosphorus.FetchCrashesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='test_platform.phosphorus.FetchCrashesRequest.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dut_hostname', full_name='test_platform.phosphorus.FetchCrashesRequest.dut_hostname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deadline', full_name='test_platform.phosphorus.FetchCrashesRequest.deadline', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upload_crashes', full_name='test_platform.phosphorus.FetchCrashesRequest.upload_crashes', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='use_staging', full_name='test_platform.phosphorus.FetchCrashesRequest.use_staging', index=4,
      number=5, type=8, cpp_type=7, label=1,
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
  serialized_start=146,
  serialized_end=330,
)


_CRASHSUMMARY = _descriptor.Descriptor(
  name='CrashSummary',
  full_name='test_platform.phosphorus.CrashSummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='exec_name', full_name='test_platform.phosphorus.CrashSummary.exec_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upload_url', full_name='test_platform.phosphorus.CrashSummary.upload_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='in_progress_integration_test', full_name='test_platform.phosphorus.CrashSummary.in_progress_integration_test', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sig', full_name='test_platform.phosphorus.CrashSummary.sig', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filename_base', full_name='test_platform.phosphorus.CrashSummary.filename_base', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=332,
  serialized_end=459,
)


_FETCHCRASHESRESPONSE = _descriptor.Descriptor(
  name='FetchCrashesResponse',
  full_name='test_platform.phosphorus.FetchCrashesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='test_platform.phosphorus.FetchCrashesResponse.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crashes', full_name='test_platform.phosphorus.FetchCrashesResponse.crashes', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crashes_rtd_only', full_name='test_platform.phosphorus.FetchCrashesResponse.crashes_rtd_only', index=2,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crashes_tls_only', full_name='test_platform.phosphorus.FetchCrashesResponse.crashes_tls_only', index=3,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FETCHCRASHESRESPONSE_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=462,
  serialized_end=749,
)

_FETCHCRASHESREQUEST.fields_by_name['config'].message_type = test__platform_dot_phosphorus_dot_common__pb2._CONFIG
_FETCHCRASHESREQUEST.fields_by_name['deadline'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_FETCHCRASHESRESPONSE.fields_by_name['state'].enum_type = _FETCHCRASHESRESPONSE_STATE
_FETCHCRASHESRESPONSE.fields_by_name['crashes'].message_type = _CRASHSUMMARY
_FETCHCRASHESRESPONSE_STATE.containing_type = _FETCHCRASHESRESPONSE
DESCRIPTOR.message_types_by_name['FetchCrashesRequest'] = _FETCHCRASHESREQUEST
DESCRIPTOR.message_types_by_name['CrashSummary'] = _CRASHSUMMARY
DESCRIPTOR.message_types_by_name['FetchCrashesResponse'] = _FETCHCRASHESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FetchCrashesRequest = _reflection.GeneratedProtocolMessageType('FetchCrashesRequest', (_message.Message,), dict(
  DESCRIPTOR = _FETCHCRASHESREQUEST,
  __module__ = 'test_platform.phosphorus.fetchcrashes_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.FetchCrashesRequest)
  ))
_sym_db.RegisterMessage(FetchCrashesRequest)

CrashSummary = _reflection.GeneratedProtocolMessageType('CrashSummary', (_message.Message,), dict(
  DESCRIPTOR = _CRASHSUMMARY,
  __module__ = 'test_platform.phosphorus.fetchcrashes_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.CrashSummary)
  ))
_sym_db.RegisterMessage(CrashSummary)

FetchCrashesResponse = _reflection.GeneratedProtocolMessageType('FetchCrashesResponse', (_message.Message,), dict(
  DESCRIPTOR = _FETCHCRASHESRESPONSE,
  __module__ = 'test_platform.phosphorus.fetchcrashes_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.FetchCrashesResponse)
  ))
_sym_db.RegisterMessage(FetchCrashesResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
