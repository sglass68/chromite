# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/phosphorus/runtest.proto

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
  name='test_platform/phosphorus/runtest.proto',
  package='test_platform.phosphorus',
  syntax='proto3',
  serialized_options=_b('ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorus'),
  serialized_pb=_b('\n&test_platform/phosphorus/runtest.proto\x12\x18test_platform.phosphorus\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%test_platform/phosphorus/common.proto\"\xae\x04\n\x0eRunTestRequest\x12\x30\n\x06\x63onfig\x18\x01 \x01(\x0b\x32 .test_platform.phosphorus.Config\x12\x15\n\rdut_hostnames\x18\x02 \x03(\t\x12\x45\n\x08\x61utotest\x18\x03 \x01(\x0b\x32\x31.test_platform.phosphorus.RunTestRequest.AutotestH\x00\x12I\n\x0b\x65nvironment\x18\x04 \x01(\x0b\x32\x34.test_platform.phosphorus.RunTestRequest.Environment\x12,\n\x08\x64\x65\x61\x64line\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\xda\x01\n\x08\x41utotest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\ttest_args\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\t\x12\x16\n\x0eis_client_test\x18\x04 \x01(\x08\x12O\n\x07keyvals\x18\x05 \x03(\x0b\x32>.test_platform.phosphorus.RunTestRequest.Autotest.KeyvalsEntry\x1a.\n\x0cKeyvalsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a.\n\x0b\x45nvironment\x12\x1f\n\x13isolated_output_dir\x18\x01 \x01(\tB\x02\x18\x01\x42\x06\n\x04testBDZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorusb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,test__platform_dot_phosphorus_dot_common__pb2.DESCRIPTOR,])




_RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY = _descriptor.Descriptor(
  name='KeyvalsEntry',
  full_name='test_platform.phosphorus.RunTestRequest.Autotest.KeyvalsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.phosphorus.RunTestRequest.Autotest.KeyvalsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.phosphorus.RunTestRequest.Autotest.KeyvalsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=597,
  serialized_end=643,
)

_RUNTESTREQUEST_AUTOTEST = _descriptor.Descriptor(
  name='Autotest',
  full_name='test_platform.phosphorus.RunTestRequest.Autotest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test_platform.phosphorus.RunTestRequest.Autotest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_args', full_name='test_platform.phosphorus.RunTestRequest.Autotest.test_args', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='test_platform.phosphorus.RunTestRequest.Autotest.display_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_client_test', full_name='test_platform.phosphorus.RunTestRequest.Autotest.is_client_test', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keyvals', full_name='test_platform.phosphorus.RunTestRequest.Autotest.keyvals', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=425,
  serialized_end=643,
)

_RUNTESTREQUEST_ENVIRONMENT = _descriptor.Descriptor(
  name='Environment',
  full_name='test_platform.phosphorus.RunTestRequest.Environment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isolated_output_dir', full_name='test_platform.phosphorus.RunTestRequest.Environment.isolated_output_dir', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\030\001'), file=DESCRIPTOR),
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
  serialized_start=645,
  serialized_end=691,
)

_RUNTESTREQUEST = _descriptor.Descriptor(
  name='RunTestRequest',
  full_name='test_platform.phosphorus.RunTestRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='test_platform.phosphorus.RunTestRequest.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dut_hostnames', full_name='test_platform.phosphorus.RunTestRequest.dut_hostnames', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='autotest', full_name='test_platform.phosphorus.RunTestRequest.autotest', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='environment', full_name='test_platform.phosphorus.RunTestRequest.environment', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deadline', full_name='test_platform.phosphorus.RunTestRequest.deadline', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RUNTESTREQUEST_AUTOTEST, _RUNTESTREQUEST_ENVIRONMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='test', full_name='test_platform.phosphorus.RunTestRequest.test',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=141,
  serialized_end=699,
)

_RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY.containing_type = _RUNTESTREQUEST_AUTOTEST
_RUNTESTREQUEST_AUTOTEST.fields_by_name['keyvals'].message_type = _RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY
_RUNTESTREQUEST_AUTOTEST.containing_type = _RUNTESTREQUEST
_RUNTESTREQUEST_ENVIRONMENT.containing_type = _RUNTESTREQUEST
_RUNTESTREQUEST.fields_by_name['config'].message_type = test__platform_dot_phosphorus_dot_common__pb2._CONFIG
_RUNTESTREQUEST.fields_by_name['autotest'].message_type = _RUNTESTREQUEST_AUTOTEST
_RUNTESTREQUEST.fields_by_name['environment'].message_type = _RUNTESTREQUEST_ENVIRONMENT
_RUNTESTREQUEST.fields_by_name['deadline'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RUNTESTREQUEST.oneofs_by_name['test'].fields.append(
  _RUNTESTREQUEST.fields_by_name['autotest'])
_RUNTESTREQUEST.fields_by_name['autotest'].containing_oneof = _RUNTESTREQUEST.oneofs_by_name['test']
DESCRIPTOR.message_types_by_name['RunTestRequest'] = _RUNTESTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RunTestRequest = _reflection.GeneratedProtocolMessageType('RunTestRequest', (_message.Message,), dict(

  Autotest = _reflection.GeneratedProtocolMessageType('Autotest', (_message.Message,), dict(

    KeyvalsEntry = _reflection.GeneratedProtocolMessageType('KeyvalsEntry', (_message.Message,), dict(
      DESCRIPTOR = _RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY,
      __module__ = 'test_platform.phosphorus.runtest_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.phosphorus.RunTestRequest.Autotest.KeyvalsEntry)
      ))
    ,
    DESCRIPTOR = _RUNTESTREQUEST_AUTOTEST,
    __module__ = 'test_platform.phosphorus.runtest_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.phosphorus.RunTestRequest.Autotest)
    ))
  ,

  Environment = _reflection.GeneratedProtocolMessageType('Environment', (_message.Message,), dict(
    DESCRIPTOR = _RUNTESTREQUEST_ENVIRONMENT,
    __module__ = 'test_platform.phosphorus.runtest_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.phosphorus.RunTestRequest.Environment)
    ))
  ,
  DESCRIPTOR = _RUNTESTREQUEST,
  __module__ = 'test_platform.phosphorus.runtest_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.RunTestRequest)
  ))
_sym_db.RegisterMessage(RunTestRequest)
_sym_db.RegisterMessage(RunTestRequest.Autotest)
_sym_db.RegisterMessage(RunTestRequest.Autotest.KeyvalsEntry)
_sym_db.RegisterMessage(RunTestRequest.Environment)


DESCRIPTOR._options = None
_RUNTESTREQUEST_AUTOTEST_KEYVALSENTRY._options = None
_RUNTESTREQUEST_ENVIRONMENT.fields_by_name['isolated_output_dir']._options = None
# @@protoc_insertion_point(module_scope)
