# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/android.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromite/api/android.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=_b('Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'),
  serialized_pb=_b('\n\x1a\x63hromite/api/android.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x17\x63hromiumos/common.proto\"\xef\x01\n\x11MarkStableRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12\x17\n\x0ftracking_branch\x18\x02 \x01(\t\x12\x14\n\x0cpackage_name\x18\x03 \x01(\t\x12\x1c\n\x14\x61ndroid_build_branch\x18\x04 \x01(\t\x12\x17\n\x0f\x61ndroid_version\x18\x05 \x01(\t\x12 \n\x18\x61ndroid_gts_build_branch\x18\x06 \x01(\t\x12.\n\rbuild_targets\x18\x07 \x03(\x0b\x32\x17.chromiumos.BuildTarget\"w\n\x12MarkStableResponse\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".chromite.api.MarkStableStatusType\x12-\n\x0c\x61ndroid_atom\x18\x02 \x01(\x0b\x32\x17.chromiumos.PackageInfo\"9\n\x13UnpinVersionRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x16\n\x14UnpinVersionResponse*\x9c\x01\n\x14MarkStableStatusType\x12\"\n\x1eMARK_STABLE_STATUS_UNSPECIFIED\x10\x00\x12\x1e\n\x1aMARK_STABLE_STATUS_SUCCESS\x10\x01\x12\x1d\n\x19MARK_STABLE_STATUS_PINNED\x10\x02\x12!\n\x1dMARK_STABLE_STATUS_EARLY_EXIT\x10\x03\x32\xd9\x01\n\x0e\x41ndroidService\x12W\n\nMarkStable\x12\x1f.chromite.api.MarkStableRequest\x1a .chromite.api.MarkStableResponse\"\x06\xc2\xed\x1a\x02\x10\x02\x12]\n\x0cUnpinVersion\x12!.chromite.api.UnpinVersionRequest\x1a\".chromite.api.UnpinVersionResponse\"\x06\xc2\xed\x1a\x02\x10\x01\x1a\x0f\xc2\xed\x1a\x0b\n\x07\x61ndroid\x10\x01\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')
  ,
  dependencies=[chromite_dot_api_dot_build__api__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,])

_MARKSTABLESTATUSTYPE = _descriptor.EnumDescriptor(
  name='MarkStableStatusType',
  full_name='chromite.api.MarkStableStatusType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MARK_STABLE_STATUS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MARK_STABLE_STATUS_SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MARK_STABLE_STATUS_PINNED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MARK_STABLE_STATUS_EARLY_EXIT', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=546,
  serialized_end=702,
)
_sym_db.RegisterEnumDescriptor(_MARKSTABLESTATUSTYPE)

MarkStableStatusType = enum_type_wrapper.EnumTypeWrapper(_MARKSTABLESTATUSTYPE)
MARK_STABLE_STATUS_UNSPECIFIED = 0
MARK_STABLE_STATUS_SUCCESS = 1
MARK_STABLE_STATUS_PINNED = 2
MARK_STABLE_STATUS_EARLY_EXIT = 3



_MARKSTABLEREQUEST = _descriptor.Descriptor(
  name='MarkStableRequest',
  full_name='chromite.api.MarkStableRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.MarkStableRequest.chroot', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tracking_branch', full_name='chromite.api.MarkStableRequest.tracking_branch', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='package_name', full_name='chromite.api.MarkStableRequest.package_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='android_build_branch', full_name='chromite.api.MarkStableRequest.android_build_branch', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='android_version', full_name='chromite.api.MarkStableRequest.android_version', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='android_gts_build_branch', full_name='chromite.api.MarkStableRequest.android_gts_build_branch', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_targets', full_name='chromite.api.MarkStableRequest.build_targets', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=100,
  serialized_end=339,
)


_MARKSTABLERESPONSE = _descriptor.Descriptor(
  name='MarkStableResponse',
  full_name='chromite.api.MarkStableResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='chromite.api.MarkStableResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='android_atom', full_name='chromite.api.MarkStableResponse.android_atom', index=1,
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
  serialized_start=341,
  serialized_end=460,
)


_UNPINVERSIONREQUEST = _descriptor.Descriptor(
  name='UnpinVersionRequest',
  full_name='chromite.api.UnpinVersionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.UnpinVersionRequest.chroot', index=0,
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
  serialized_start=462,
  serialized_end=519,
)


_UNPINVERSIONRESPONSE = _descriptor.Descriptor(
  name='UnpinVersionResponse',
  full_name='chromite.api.UnpinVersionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=521,
  serialized_end=543,
)

_MARKSTABLEREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
_MARKSTABLEREQUEST.fields_by_name['build_targets'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_MARKSTABLERESPONSE.fields_by_name['status'].enum_type = _MARKSTABLESTATUSTYPE
_MARKSTABLERESPONSE.fields_by_name['android_atom'].message_type = chromiumos_dot_common__pb2._PACKAGEINFO
_UNPINVERSIONREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
DESCRIPTOR.message_types_by_name['MarkStableRequest'] = _MARKSTABLEREQUEST
DESCRIPTOR.message_types_by_name['MarkStableResponse'] = _MARKSTABLERESPONSE
DESCRIPTOR.message_types_by_name['UnpinVersionRequest'] = _UNPINVERSIONREQUEST
DESCRIPTOR.message_types_by_name['UnpinVersionResponse'] = _UNPINVERSIONRESPONSE
DESCRIPTOR.enum_types_by_name['MarkStableStatusType'] = _MARKSTABLESTATUSTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MarkStableRequest = _reflection.GeneratedProtocolMessageType('MarkStableRequest', (_message.Message,), dict(
  DESCRIPTOR = _MARKSTABLEREQUEST,
  __module__ = 'chromite.api.android_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.MarkStableRequest)
  ))
_sym_db.RegisterMessage(MarkStableRequest)

MarkStableResponse = _reflection.GeneratedProtocolMessageType('MarkStableResponse', (_message.Message,), dict(
  DESCRIPTOR = _MARKSTABLERESPONSE,
  __module__ = 'chromite.api.android_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.MarkStableResponse)
  ))
_sym_db.RegisterMessage(MarkStableResponse)

UnpinVersionRequest = _reflection.GeneratedProtocolMessageType('UnpinVersionRequest', (_message.Message,), dict(
  DESCRIPTOR = _UNPINVERSIONREQUEST,
  __module__ = 'chromite.api.android_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.UnpinVersionRequest)
  ))
_sym_db.RegisterMessage(UnpinVersionRequest)

UnpinVersionResponse = _reflection.GeneratedProtocolMessageType('UnpinVersionResponse', (_message.Message,), dict(
  DESCRIPTOR = _UNPINVERSIONRESPONSE,
  __module__ = 'chromite.api.android_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.UnpinVersionResponse)
  ))
_sym_db.RegisterMessage(UnpinVersionResponse)


DESCRIPTOR._options = None

_ANDROIDSERVICE = _descriptor.ServiceDescriptor(
  name='AndroidService',
  full_name='chromite.api.AndroidService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\302\355\032\013\n\007android\020\001'),
  serialized_start=705,
  serialized_end=922,
  methods=[
  _descriptor.MethodDescriptor(
    name='MarkStable',
    full_name='chromite.api.AndroidService.MarkStable',
    index=0,
    containing_service=None,
    input_type=_MARKSTABLEREQUEST,
    output_type=_MARKSTABLERESPONSE,
    serialized_options=_b('\302\355\032\002\020\002'),
  ),
  _descriptor.MethodDescriptor(
    name='UnpinVersion',
    full_name='chromite.api.AndroidService.UnpinVersion',
    index=1,
    containing_service=None,
    input_type=_UNPINVERSIONREQUEST,
    output_type=_UNPINVERSIONRESPONSE,
    serialized_options=_b('\302\355\032\002\020\001'),
  ),
])
_sym_db.RegisterServiceDescriptor(_ANDROIDSERVICE)

DESCRIPTOR.services_by_name['AndroidService'] = _ANDROIDSERVICE

# @@protoc_insertion_point(module_scope)
