# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/vision/LocatedFaceCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.vision import LocatedFace_pb2 as rst_dot_vision_dot_LocatedFace__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/vision/LocatedFaceCollection.proto',
  package='rst.vision',
  syntax='proto2',
  serialized_pb=_b('\n&rst/vision/LocatedFaceCollection.proto\x12\nrst.vision\x1a\x1crst/vision/LocatedFace.proto\"A\n\x15LocatedFaceCollection\x12(\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x17.rst.vision.LocatedFaceB\x1b\x42\x19LocatedFaceCollectionType')
  ,
  dependencies=[rst_dot_vision_dot_LocatedFace__pb2.DESCRIPTOR,])




_LOCATEDFACECOLLECTION = _descriptor.Descriptor(
  name='LocatedFaceCollection',
  full_name='rst.vision.LocatedFaceCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.vision.LocatedFaceCollection.element', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=84,
  serialized_end=149,
)

_LOCATEDFACECOLLECTION.fields_by_name['element'].message_type = rst_dot_vision_dot_LocatedFace__pb2._LOCATEDFACE
DESCRIPTOR.message_types_by_name['LocatedFaceCollection'] = _LOCATEDFACECOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LocatedFaceCollection = _reflection.GeneratedProtocolMessageType('LocatedFaceCollection', (_message.Message,), dict(
  DESCRIPTOR = _LOCATEDFACECOLLECTION,
  __module__ = 'rst.vision.LocatedFaceCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.vision.LocatedFaceCollection)
  ))
_sym_db.RegisterMessage(LocatedFaceCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\031LocatedFaceCollectionType'))
# @@protoc_insertion_point(module_scope)
