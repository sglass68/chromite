# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/steps/compute_backfill.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.test_platform import request_pb2 as test__platform_dot_request__pb2
from chromite.api.gen.test_platform.steps import enumeration_pb2 as test__platform_dot_steps_dot_enumeration__pb2
from chromite.api.gen.test_platform.steps import execution_pb2 as test__platform_dot_steps_dot_execution__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/steps/compute_backfill.proto',
  package='test_platform.steps',
  syntax='proto3',
  serialized_options=b'Z=go.chromium.org/chromiumos/infra/proto/go/test_platform/steps',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*test_platform/steps/compute_backfill.proto\x12\x13test_platform.steps\x1a\x1btest_platform/request.proto\x1a%test_platform/steps/enumeration.proto\x1a#test_platform/steps/execution.proto\"\x97\x02\n\x17\x43omputeBackfillRequests\x12=\n\x08requests\x18\x01 \x03(\x0b\x32+.test_platform.steps.ComputeBackfillRequest\x12Y\n\x0ftagged_requests\x18\x02 \x03(\x0b\x32@.test_platform.steps.ComputeBackfillRequests.TaggedRequestsEntry\x1a\x62\n\x13TaggedRequestsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12:\n\x05value\x18\x02 \x01(\x0b\x32+.test_platform.steps.ComputeBackfillRequest:\x02\x38\x01\"\x9f\x02\n\x18\x43omputeBackfillResponses\x12?\n\tresponses\x18\x01 \x03(\x0b\x32,.test_platform.steps.ComputeBackfillResponse\x12\\\n\x10tagged_responses\x18\x02 \x03(\x0b\x32\x42.test_platform.steps.ComputeBackfillResponses.TaggedResponsesEntry\x1a\x64\n\x14TaggedResponsesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12;\n\x05value\x18\x02 \x01(\x0b\x32,.test_platform.steps.ComputeBackfillResponse:\x02\x38\x01\"\xb9\x01\n\x16\x43omputeBackfillRequest\x12\'\n\x07request\x18\x01 \x01(\x0b\x32\x16.test_platform.Request\x12=\n\x0b\x65numeration\x18\x02 \x01(\x0b\x32(.test_platform.steps.EnumerationResponse\x12\x37\n\texecution\x18\x03 \x01(\x0b\x32$.test_platform.steps.ExecuteResponse\"B\n\x17\x43omputeBackfillResponse\x12\'\n\x07request\x18\x01 \x01(\x0b\x32\x16.test_platform.RequestB?Z=go.chromium.org/chromiumos/infra/proto/go/test_platform/stepsb\x06proto3'
  ,
  dependencies=[test__platform_dot_request__pb2.DESCRIPTOR,test__platform_dot_steps_dot_enumeration__pb2.DESCRIPTOR,test__platform_dot_steps_dot_execution__pb2.DESCRIPTOR,])




_COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY = _descriptor.Descriptor(
  name='TaggedRequestsEntry',
  full_name='test_platform.steps.ComputeBackfillRequests.TaggedRequestsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.steps.ComputeBackfillRequests.TaggedRequestsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.steps.ComputeBackfillRequests.TaggedRequestsEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=354,
  serialized_end=452,
)

_COMPUTEBACKFILLREQUESTS = _descriptor.Descriptor(
  name='ComputeBackfillRequests',
  full_name='test_platform.steps.ComputeBackfillRequests',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='requests', full_name='test_platform.steps.ComputeBackfillRequests.requests', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tagged_requests', full_name='test_platform.steps.ComputeBackfillRequests.tagged_requests', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=173,
  serialized_end=452,
)


_COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY = _descriptor.Descriptor(
  name='TaggedResponsesEntry',
  full_name='test_platform.steps.ComputeBackfillResponses.TaggedResponsesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.steps.ComputeBackfillResponses.TaggedResponsesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.steps.ComputeBackfillResponses.TaggedResponsesEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=642,
  serialized_end=742,
)

_COMPUTEBACKFILLRESPONSES = _descriptor.Descriptor(
  name='ComputeBackfillResponses',
  full_name='test_platform.steps.ComputeBackfillResponses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='responses', full_name='test_platform.steps.ComputeBackfillResponses.responses', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tagged_responses', full_name='test_platform.steps.ComputeBackfillResponses.tagged_responses', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=742,
)


_COMPUTEBACKFILLREQUEST = _descriptor.Descriptor(
  name='ComputeBackfillRequest',
  full_name='test_platform.steps.ComputeBackfillRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='test_platform.steps.ComputeBackfillRequest.request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enumeration', full_name='test_platform.steps.ComputeBackfillRequest.enumeration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='execution', full_name='test_platform.steps.ComputeBackfillRequest.execution', index=2,
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
  serialized_start=745,
  serialized_end=930,
)


_COMPUTEBACKFILLRESPONSE = _descriptor.Descriptor(
  name='ComputeBackfillResponse',
  full_name='test_platform.steps.ComputeBackfillResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='test_platform.steps.ComputeBackfillResponse.request', index=0,
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
  serialized_start=932,
  serialized_end=998,
)

_COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY.fields_by_name['value'].message_type = _COMPUTEBACKFILLREQUEST
_COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY.containing_type = _COMPUTEBACKFILLREQUESTS
_COMPUTEBACKFILLREQUESTS.fields_by_name['requests'].message_type = _COMPUTEBACKFILLREQUEST
_COMPUTEBACKFILLREQUESTS.fields_by_name['tagged_requests'].message_type = _COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY
_COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY.fields_by_name['value'].message_type = _COMPUTEBACKFILLRESPONSE
_COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY.containing_type = _COMPUTEBACKFILLRESPONSES
_COMPUTEBACKFILLRESPONSES.fields_by_name['responses'].message_type = _COMPUTEBACKFILLRESPONSE
_COMPUTEBACKFILLRESPONSES.fields_by_name['tagged_responses'].message_type = _COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY
_COMPUTEBACKFILLREQUEST.fields_by_name['request'].message_type = test__platform_dot_request__pb2._REQUEST
_COMPUTEBACKFILLREQUEST.fields_by_name['enumeration'].message_type = test__platform_dot_steps_dot_enumeration__pb2._ENUMERATIONRESPONSE
_COMPUTEBACKFILLREQUEST.fields_by_name['execution'].message_type = test__platform_dot_steps_dot_execution__pb2._EXECUTERESPONSE
_COMPUTEBACKFILLRESPONSE.fields_by_name['request'].message_type = test__platform_dot_request__pb2._REQUEST
DESCRIPTOR.message_types_by_name['ComputeBackfillRequests'] = _COMPUTEBACKFILLREQUESTS
DESCRIPTOR.message_types_by_name['ComputeBackfillResponses'] = _COMPUTEBACKFILLRESPONSES
DESCRIPTOR.message_types_by_name['ComputeBackfillRequest'] = _COMPUTEBACKFILLREQUEST
DESCRIPTOR.message_types_by_name['ComputeBackfillResponse'] = _COMPUTEBACKFILLRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ComputeBackfillRequests = _reflection.GeneratedProtocolMessageType('ComputeBackfillRequests', (_message.Message,), {

  'TaggedRequestsEntry' : _reflection.GeneratedProtocolMessageType('TaggedRequestsEntry', (_message.Message,), {
    'DESCRIPTOR' : _COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY,
    '__module__' : 'test_platform.steps.compute_backfill_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillRequests.TaggedRequestsEntry)
    })
  ,
  'DESCRIPTOR' : _COMPUTEBACKFILLREQUESTS,
  '__module__' : 'test_platform.steps.compute_backfill_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillRequests)
  })
_sym_db.RegisterMessage(ComputeBackfillRequests)
_sym_db.RegisterMessage(ComputeBackfillRequests.TaggedRequestsEntry)

ComputeBackfillResponses = _reflection.GeneratedProtocolMessageType('ComputeBackfillResponses', (_message.Message,), {

  'TaggedResponsesEntry' : _reflection.GeneratedProtocolMessageType('TaggedResponsesEntry', (_message.Message,), {
    'DESCRIPTOR' : _COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY,
    '__module__' : 'test_platform.steps.compute_backfill_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillResponses.TaggedResponsesEntry)
    })
  ,
  'DESCRIPTOR' : _COMPUTEBACKFILLRESPONSES,
  '__module__' : 'test_platform.steps.compute_backfill_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillResponses)
  })
_sym_db.RegisterMessage(ComputeBackfillResponses)
_sym_db.RegisterMessage(ComputeBackfillResponses.TaggedResponsesEntry)

ComputeBackfillRequest = _reflection.GeneratedProtocolMessageType('ComputeBackfillRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPUTEBACKFILLREQUEST,
  '__module__' : 'test_platform.steps.compute_backfill_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillRequest)
  })
_sym_db.RegisterMessage(ComputeBackfillRequest)

ComputeBackfillResponse = _reflection.GeneratedProtocolMessageType('ComputeBackfillResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMPUTEBACKFILLRESPONSE,
  '__module__' : 'test_platform.steps.compute_backfill_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.ComputeBackfillResponse)
  })
_sym_db.RegisterMessage(ComputeBackfillResponse)


DESCRIPTOR._options = None
_COMPUTEBACKFILLREQUESTS_TAGGEDREQUESTSENTRY._options = None
_COMPUTEBACKFILLRESPONSES_TAGGEDRESPONSESENTRY._options = None
# @@protoc_insertion_point(module_scope)
