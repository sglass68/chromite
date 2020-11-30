# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/phosphorus/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/phosphorus/common.proto',
  package='test_platform.phosphorus',
  syntax='proto3',
  serialized_options=_b('ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorus'),
  serialized_pb=_b('\n%test_platform/phosphorus/common.proto\x12\x18test_platform.phosphorus\"&\n\x0e\x42otEnvironment\x12\x14\n\x0c\x61utotest_dir\x18\x01 \x01(\t\"|\n\x0fTaskEnvironment\x12\x13\n\x0bresults_dir\x18\x02 \x01(\t\x12\x18\n\x10test_results_dir\x18\x03 \x01(\t\x12\x1b\n\x13ssp_base_image_name\x18\x04 \x01(\tJ\x04\x08\x01\x10\x02R\x17synchronous_offload_dir\"3\n\x11LogDataUploadStep\x12\x1e\n\x16max_concurrent_uploads\x18\x01 \x01(\x05\"\xc3\x01\n\x06\x43onfig\x12\x35\n\x03\x62ot\x18\x01 \x01(\x0b\x32(.test_platform.phosphorus.BotEnvironment\x12\x37\n\x04task\x18\x02 \x01(\x0b\x32).test_platform.phosphorus.TaskEnvironment\x12I\n\x14log_data_upload_step\x18\x03 \x01(\x0b\x32+.test_platform.phosphorus.LogDataUploadStepBDZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorusb\x06proto3')
)




_BOTENVIRONMENT = _descriptor.Descriptor(
  name='BotEnvironment',
  full_name='test_platform.phosphorus.BotEnvironment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='autotest_dir', full_name='test_platform.phosphorus.BotEnvironment.autotest_dir', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=67,
  serialized_end=105,
)


_TASKENVIRONMENT = _descriptor.Descriptor(
  name='TaskEnvironment',
  full_name='test_platform.phosphorus.TaskEnvironment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='results_dir', full_name='test_platform.phosphorus.TaskEnvironment.results_dir', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_results_dir', full_name='test_platform.phosphorus.TaskEnvironment.test_results_dir', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssp_base_image_name', full_name='test_platform.phosphorus.TaskEnvironment.ssp_base_image_name', index=2,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=107,
  serialized_end=231,
)


_LOGDATAUPLOADSTEP = _descriptor.Descriptor(
  name='LogDataUploadStep',
  full_name='test_platform.phosphorus.LogDataUploadStep',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_concurrent_uploads', full_name='test_platform.phosphorus.LogDataUploadStep.max_concurrent_uploads', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=233,
  serialized_end=284,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='test_platform.phosphorus.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bot', full_name='test_platform.phosphorus.Config.bot', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task', full_name='test_platform.phosphorus.Config.task', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='log_data_upload_step', full_name='test_platform.phosphorus.Config.log_data_upload_step', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=287,
  serialized_end=482,
)

_CONFIG.fields_by_name['bot'].message_type = _BOTENVIRONMENT
_CONFIG.fields_by_name['task'].message_type = _TASKENVIRONMENT
_CONFIG.fields_by_name['log_data_upload_step'].message_type = _LOGDATAUPLOADSTEP
DESCRIPTOR.message_types_by_name['BotEnvironment'] = _BOTENVIRONMENT
DESCRIPTOR.message_types_by_name['TaskEnvironment'] = _TASKENVIRONMENT
DESCRIPTOR.message_types_by_name['LogDataUploadStep'] = _LOGDATAUPLOADSTEP
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BotEnvironment = _reflection.GeneratedProtocolMessageType('BotEnvironment', (_message.Message,), dict(
  DESCRIPTOR = _BOTENVIRONMENT,
  __module__ = 'test_platform.phosphorus.common_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.BotEnvironment)
  ))
_sym_db.RegisterMessage(BotEnvironment)

TaskEnvironment = _reflection.GeneratedProtocolMessageType('TaskEnvironment', (_message.Message,), dict(
  DESCRIPTOR = _TASKENVIRONMENT,
  __module__ = 'test_platform.phosphorus.common_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.TaskEnvironment)
  ))
_sym_db.RegisterMessage(TaskEnvironment)

LogDataUploadStep = _reflection.GeneratedProtocolMessageType('LogDataUploadStep', (_message.Message,), dict(
  DESCRIPTOR = _LOGDATAUPLOADSTEP,
  __module__ = 'test_platform.phosphorus.common_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.LogDataUploadStep)
  ))
_sym_db.RegisterMessage(LogDataUploadStep)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), dict(
  DESCRIPTOR = _CONFIG,
  __module__ = 'test_platform.phosphorus.common_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.Config)
  ))
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
