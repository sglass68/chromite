# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/analytics/result.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/analytics/result.proto',
  package='test_platform.analytics',
  syntax='proto3',
  serialized_options=_b('ZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/analytics'),
  serialized_pb=_b('\n$test_platform/analytics/result.proto\x12\x17test_platform.analytics\x1a\x1fgoogle/protobuf/timestamp.proto\"\xf8\x01\n\x0bTestPlanRun\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x10\n\x08\x62uild_id\x18\x02 \x01(\x03\x12\r\n\x05suite\x18\x03 \x01(\t\x12\x15\n\rexecution_url\x18\x04 \x01(\t\x12\x10\n\x08\x64ut_pool\x18\x05 \x01(\t\x12\x14\n\x0c\x62uild_target\x18\x06 \x01(\t\x12\x16\n\x0e\x63hromeos_build\x18\x07 \x01(\t\x12/\n\x06status\x18\x08 \x01(\x0b\x32\x1f.test_platform.analytics.Status\x12\x33\n\x08timeline\x18\t \x01(\x0b\x32!.test_platform.analytics.Timeline\"\x90\x03\n\x07TestRun\x12\x10\n\x08\x62uild_id\x18\x01 \x01(\x03\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x15\n\rexecution_url\x18\x03 \x01(\t\x12\x12\n\nparent_uid\x18\x04 \x01(\t\x12\r\n\x05model\x18\x05 \x01(\t\x12\x33\n\x08timeline\x18\x06 \x01(\x0b\x32!.test_platform.analytics.Timeline\x12/\n\x06status\x18\x07 \x01(\x0b\x32\x1f.test_platform.analytics.Status\x12\x31\n\x07verdict\x18\x08 \x01(\x0b\x32 .test_platform.analytics.Verdict\x12\x14\n\x0c\x66ull_log_url\x18\t \x01(\t\x12\x37\n\x06prejob\x18\n \x01(\x0b\x32\'.test_platform.analytics.TestRun.Prejob\x1a;\n\x06Prejob\x12\x31\n\x07verdict\x18\x01 \x01(\x0b\x32 .test_platform.analytics.Verdict\"\x9f\x01\n\x0eTestCaseResult\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x17\n\x0fparent_build_id\x18\x03 \x01(\x03\x12\x31\n\x07verdict\x18\x04 \x01(\x0b\x32 .test_platform.analytics.Verdict\x12\x1e\n\x16human_readable_summary\x18\x05 \x01(\t\"\xcb\x01\n\x08Timeline\x12/\n\x0b\x63reate_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstart_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x61\x62\x61ndon_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x17\n\x06Status\x12\r\n\x05value\x18\x01 \x01(\t\"\x18\n\x07Verdict\x12\r\n\x05value\x18\x01 \x01(\tBCZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/analyticsb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_TESTPLANRUN = _descriptor.Descriptor(
  name='TestPlanRun',
  full_name='test_platform.analytics.TestPlanRun',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='test_platform.analytics.TestPlanRun.uid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_id', full_name='test_platform.analytics.TestPlanRun.build_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='suite', full_name='test_platform.analytics.TestPlanRun.suite', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execution_url', full_name='test_platform.analytics.TestPlanRun.execution_url', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dut_pool', full_name='test_platform.analytics.TestPlanRun.dut_pool', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='test_platform.analytics.TestPlanRun.build_target', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chromeos_build', full_name='test_platform.analytics.TestPlanRun.chromeos_build', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='test_platform.analytics.TestPlanRun.status', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeline', full_name='test_platform.analytics.TestPlanRun.timeline', index=8,
      number=9, type=11, cpp_type=10, label=1,
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
  serialized_start=99,
  serialized_end=347,
)


_TESTRUN_PREJOB = _descriptor.Descriptor(
  name='Prejob',
  full_name='test_platform.analytics.TestRun.Prejob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='verdict', full_name='test_platform.analytics.TestRun.Prejob.verdict', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=691,
  serialized_end=750,
)

_TESTRUN = _descriptor.Descriptor(
  name='TestRun',
  full_name='test_platform.analytics.TestRun',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_id', full_name='test_platform.analytics.TestRun.build_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='test_platform.analytics.TestRun.display_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execution_url', full_name='test_platform.analytics.TestRun.execution_url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_uid', full_name='test_platform.analytics.TestRun.parent_uid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model', full_name='test_platform.analytics.TestRun.model', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeline', full_name='test_platform.analytics.TestRun.timeline', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='test_platform.analytics.TestRun.status', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verdict', full_name='test_platform.analytics.TestRun.verdict', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full_log_url', full_name='test_platform.analytics.TestRun.full_log_url', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='prejob', full_name='test_platform.analytics.TestRun.prejob', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TESTRUN_PREJOB, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=350,
  serialized_end=750,
)


_TESTCASERESULT = _descriptor.Descriptor(
  name='TestCaseResult',
  full_name='test_platform.analytics.TestCaseResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='test_platform.analytics.TestCaseResult.uid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='test_platform.analytics.TestCaseResult.display_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_build_id', full_name='test_platform.analytics.TestCaseResult.parent_build_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verdict', full_name='test_platform.analytics.TestCaseResult.verdict', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='human_readable_summary', full_name='test_platform.analytics.TestCaseResult.human_readable_summary', index=4,
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
  serialized_start=753,
  serialized_end=912,
)


_TIMELINE = _descriptor.Descriptor(
  name='Timeline',
  full_name='test_platform.analytics.Timeline',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='create_time', full_name='test_platform.analytics.Timeline.create_time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_time', full_name='test_platform.analytics.Timeline.start_time', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_time', full_name='test_platform.analytics.Timeline.end_time', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='abandon_time', full_name='test_platform.analytics.Timeline.abandon_time', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=915,
  serialized_end=1118,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='test_platform.analytics.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.analytics.Status.value', index=0,
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
  serialized_start=1120,
  serialized_end=1143,
)


_VERDICT = _descriptor.Descriptor(
  name='Verdict',
  full_name='test_platform.analytics.Verdict',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.analytics.Verdict.value', index=0,
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
  serialized_start=1145,
  serialized_end=1169,
)

_TESTPLANRUN.fields_by_name['status'].message_type = _STATUS
_TESTPLANRUN.fields_by_name['timeline'].message_type = _TIMELINE
_TESTRUN_PREJOB.fields_by_name['verdict'].message_type = _VERDICT
_TESTRUN_PREJOB.containing_type = _TESTRUN
_TESTRUN.fields_by_name['timeline'].message_type = _TIMELINE
_TESTRUN.fields_by_name['status'].message_type = _STATUS
_TESTRUN.fields_by_name['verdict'].message_type = _VERDICT
_TESTRUN.fields_by_name['prejob'].message_type = _TESTRUN_PREJOB
_TESTCASERESULT.fields_by_name['verdict'].message_type = _VERDICT
_TIMELINE.fields_by_name['create_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TIMELINE.fields_by_name['start_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TIMELINE.fields_by_name['end_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TIMELINE.fields_by_name['abandon_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['TestPlanRun'] = _TESTPLANRUN
DESCRIPTOR.message_types_by_name['TestRun'] = _TESTRUN
DESCRIPTOR.message_types_by_name['TestCaseResult'] = _TESTCASERESULT
DESCRIPTOR.message_types_by_name['Timeline'] = _TIMELINE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['Verdict'] = _VERDICT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestPlanRun = _reflection.GeneratedProtocolMessageType('TestPlanRun', (_message.Message,), dict(
  DESCRIPTOR = _TESTPLANRUN,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestPlanRun)
  ))
_sym_db.RegisterMessage(TestPlanRun)

TestRun = _reflection.GeneratedProtocolMessageType('TestRun', (_message.Message,), dict(

  Prejob = _reflection.GeneratedProtocolMessageType('Prejob', (_message.Message,), dict(
    DESCRIPTOR = _TESTRUN_PREJOB,
    __module__ = 'test_platform.analytics.result_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.analytics.TestRun.Prejob)
    ))
  ,
  DESCRIPTOR = _TESTRUN,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestRun)
  ))
_sym_db.RegisterMessage(TestRun)
_sym_db.RegisterMessage(TestRun.Prejob)

TestCaseResult = _reflection.GeneratedProtocolMessageType('TestCaseResult', (_message.Message,), dict(
  DESCRIPTOR = _TESTCASERESULT,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestCaseResult)
  ))
_sym_db.RegisterMessage(TestCaseResult)

Timeline = _reflection.GeneratedProtocolMessageType('Timeline', (_message.Message,), dict(
  DESCRIPTOR = _TIMELINE,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Timeline)
  ))
_sym_db.RegisterMessage(Timeline)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), dict(
  DESCRIPTOR = _STATUS,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Status)
  ))
_sym_db.RegisterMessage(Status)

Verdict = _reflection.GeneratedProtocolMessageType('Verdict', (_message.Message,), dict(
  DESCRIPTOR = _VERDICT,
  __module__ = 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Verdict)
  ))
_sym_db.RegisterMessage(Verdict)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)