# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: autotest.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import build_api_pb2 as build__api__pb2
import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='autotest.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0e\x61utotest.proto\x12\x0c\x63hromite.api\x1a\x0f\x62uild_api.proto\x1a\x0c\x63ommon.proto\"[\n\x1b\x43reateHwTestArchivesRequest\x12\"\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x0c.BuildTarget\x12\x18\n\x10output_directory\x18\x02 \x01(\t\"\x1b\n\x0b\x41rchiveFile\x12\x0c\n\x04path\x18\x01 \x01(\t\"H\n\x1c\x43reateHwTestArchivesResponse\x12(\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x19.chromite.api.ArchiveFile2\x97\x01\n\x0e\x41rchiveService\x12m\n\x14\x43reateHwTestArchives\x12).chromite.api.CreateHwTestArchivesRequest\x1a*.chromite.api.CreateHwTestArchivesResponse\x1a\x16\xc2\xed\x1a\x12\n\x10\x61utotest_archiveb\x06proto3')
  ,
  dependencies=[build__api__pb2.DESCRIPTOR,common__pb2.DESCRIPTOR,])




_CREATEHWTESTARCHIVESREQUEST = _descriptor.Descriptor(
  name='CreateHwTestArchivesRequest',
  full_name='chromite.api.CreateHwTestArchivesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.CreateHwTestArchivesRequest.build_target', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_directory', full_name='chromite.api.CreateHwTestArchivesRequest.output_directory', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=154,
)


_ARCHIVEFILE = _descriptor.Descriptor(
  name='ArchiveFile',
  full_name='chromite.api.ArchiveFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.ArchiveFile.path', index=0,
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
  serialized_start=156,
  serialized_end=183,
)


_CREATEHWTESTARCHIVESRESPONSE = _descriptor.Descriptor(
  name='CreateHwTestArchivesResponse',
  full_name='chromite.api.CreateHwTestArchivesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='files', full_name='chromite.api.CreateHwTestArchivesResponse.files', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=185,
  serialized_end=257,
)

_CREATEHWTESTARCHIVESREQUEST.fields_by_name['build_target'].message_type = common__pb2._BUILDTARGET
_CREATEHWTESTARCHIVESRESPONSE.fields_by_name['files'].message_type = _ARCHIVEFILE
DESCRIPTOR.message_types_by_name['CreateHwTestArchivesRequest'] = _CREATEHWTESTARCHIVESREQUEST
DESCRIPTOR.message_types_by_name['ArchiveFile'] = _ARCHIVEFILE
DESCRIPTOR.message_types_by_name['CreateHwTestArchivesResponse'] = _CREATEHWTESTARCHIVESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateHwTestArchivesRequest = _reflection.GeneratedProtocolMessageType('CreateHwTestArchivesRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEHWTESTARCHIVESREQUEST,
  __module__ = 'autotest_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateHwTestArchivesRequest)
  ))
_sym_db.RegisterMessage(CreateHwTestArchivesRequest)

ArchiveFile = _reflection.GeneratedProtocolMessageType('ArchiveFile', (_message.Message,), dict(
  DESCRIPTOR = _ARCHIVEFILE,
  __module__ = 'autotest_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.ArchiveFile)
  ))
_sym_db.RegisterMessage(ArchiveFile)

CreateHwTestArchivesResponse = _reflection.GeneratedProtocolMessageType('CreateHwTestArchivesResponse', (_message.Message,), dict(
  DESCRIPTOR = _CREATEHWTESTARCHIVESRESPONSE,
  __module__ = 'autotest_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateHwTestArchivesResponse)
  ))
_sym_db.RegisterMessage(CreateHwTestArchivesResponse)



_ARCHIVESERVICE = _descriptor.ServiceDescriptor(
  name='ArchiveService',
  full_name='chromite.api.ArchiveService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\302\355\032\022\n\020autotest_archive'),
  serialized_start=260,
  serialized_end=411,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateHwTestArchives',
    full_name='chromite.api.ArchiveService.CreateHwTestArchives',
    index=0,
    containing_service=None,
    input_type=_CREATEHWTESTARCHIVESREQUEST,
    output_type=_CREATEHWTESTARCHIVESRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ARCHIVESERVICE)

DESCRIPTOR.services_by_name['ArchiveService'] = _ARCHIVESERVICE

# @@protoc_insertion_point(module_scope)
