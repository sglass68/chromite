# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client/request_id.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.client import client_id_pb2 as client_dot_client__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='client/request_id.proto',
  package='client',
  syntax='proto3',
  serialized_options=_b('Z0go.chromium.org/chromiumos/infra/proto/go/client'),
  serialized_pb=_b('\n\x17\x63lient/request_id.proto\x12\x06\x63lient\x1a\x16\x63lient/client_id.proto\"<\n\tRequestId\x12\n\n\x02id\x18\x01 \x01(\t\x12#\n\tclient_id\x18\x02 \x01(\x0b\x32\x10.client.ClientIdB2Z0go.chromium.org/chromiumos/infra/proto/go/clientb\x06proto3')
  ,
  dependencies=[client_dot_client__id__pb2.DESCRIPTOR,])




_REQUESTID = _descriptor.Descriptor(
  name='RequestId',
  full_name='client.RequestId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='client.RequestId.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='client.RequestId.client_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=59,
  serialized_end=119,
)

_REQUESTID.fields_by_name['client_id'].message_type = client_dot_client__id__pb2._CLIENTID
DESCRIPTOR.message_types_by_name['RequestId'] = _REQUESTID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestId = _reflection.GeneratedProtocolMessageType('RequestId', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTID,
  __module__ = 'client.request_id_pb2'
  # @@protoc_insertion_point(class_scope:client.RequestId)
  ))
_sym_db.RegisterMessage(RequestId)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
