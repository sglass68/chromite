# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/branch.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/branch.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=b'Z4go.chromium.org/chromiumos/infra/proto/go/chromiumos',
  serialized_pb=b'\n\x17\x63hromiumos/branch.proto\x12\nchromiumos\"\xb9\x01\n\x06\x42ranch\x12+\n\x04type\x18\x01 \x01(\x0e\x32\x1d.chromiumos.Branch.BranchType\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\ndescriptor\x18\x03 \x01(\t\"`\n\nBranchType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07RELEASE\x10\x01\x12\x0b\n\x07\x46\x41\x43TORY\x10\x02\x12\x0c\n\x08\x46IRMWARE\x10\x03\x12\r\n\tSTABILIZE\x10\x04\x12\n\n\x06\x43USTOM\x10\x05\x42\x36Z4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3'
)



_BRANCH_BRANCHTYPE = _descriptor.EnumDescriptor(
  name='BranchType',
  full_name='chromiumos.Branch.BranchType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RELEASE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FACTORY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIRMWARE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STABILIZE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=129,
  serialized_end=225,
)
_sym_db.RegisterEnumDescriptor(_BRANCH_BRANCHTYPE)


_BRANCH = _descriptor.Descriptor(
  name='Branch',
  full_name='chromiumos.Branch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='chromiumos.Branch.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.Branch.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='descriptor', full_name='chromiumos.Branch.descriptor', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BRANCH_BRANCHTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=225,
)

_BRANCH.fields_by_name['type'].enum_type = _BRANCH_BRANCHTYPE
_BRANCH_BRANCHTYPE.containing_type = _BRANCH
DESCRIPTOR.message_types_by_name['Branch'] = _BRANCH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Branch = _reflection.GeneratedProtocolMessageType('Branch', (_message.Message,), {
  'DESCRIPTOR' : _BRANCH,
  '__module__' : 'chromiumos.branch_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Branch)
  })
_sym_db.RegisterMessage(Branch)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
