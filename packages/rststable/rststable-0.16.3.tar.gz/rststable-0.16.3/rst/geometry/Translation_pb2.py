# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/geometry/Translation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/geometry/Translation.proto',
  package='rst.geometry',
  syntax='proto2',
  serialized_pb=_b('\n\x1erst/geometry/Translation.proto\x12\x0crst.geometry\"@\n\x0bTranslation\x12\t\n\x01x\x18\x01 \x02(\x01\x12\t\n\x01y\x18\x02 \x02(\x01\x12\t\n\x01z\x18\x03 \x02(\x01\x12\x10\n\x08\x66rame_id\x18\x08 \x01(\tB\x11\x42\x0fTranslationType')
)




_TRANSLATION = _descriptor.Descriptor(
  name='Translation',
  full_name='rst.geometry.Translation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='rst.geometry.Translation.x', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='rst.geometry.Translation.y', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='rst.geometry.Translation.z', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame_id', full_name='rst.geometry.Translation.frame_id', index=3,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=112,
)

DESCRIPTOR.message_types_by_name['Translation'] = _TRANSLATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Translation = _reflection.GeneratedProtocolMessageType('Translation', (_message.Message,), dict(
  DESCRIPTOR = _TRANSLATION,
  __module__ = 'rst.geometry.Translation_pb2'
  # @@protoc_insertion_point(class_scope:rst.geometry.Translation)
  ))
_sym_db.RegisterMessage(Translation)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\017TranslationType'))
# @@protoc_insertion_point(module_scope)
