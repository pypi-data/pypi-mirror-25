# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/vision/FaceLandmarksCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.vision import FaceLandmarks_pb2 as rst_dot_vision_dot_FaceLandmarks__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/vision/FaceLandmarksCollection.proto',
  package='rst.vision',
  syntax='proto2',
  serialized_pb=_b('\n(rst/vision/FaceLandmarksCollection.proto\x12\nrst.vision\x1a\x1erst/vision/FaceLandmarks.proto\"E\n\x17\x46\x61\x63\x65LandmarksCollection\x12*\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x19.rst.vision.FaceLandmarksB\x1d\x42\x1b\x46\x61\x63\x65LandmarksCollectionType')
  ,
  dependencies=[rst_dot_vision_dot_FaceLandmarks__pb2.DESCRIPTOR,])




_FACELANDMARKSCOLLECTION = _descriptor.Descriptor(
  name='FaceLandmarksCollection',
  full_name='rst.vision.FaceLandmarksCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.vision.FaceLandmarksCollection.element', index=0,
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
  serialized_start=88,
  serialized_end=157,
)

_FACELANDMARKSCOLLECTION.fields_by_name['element'].message_type = rst_dot_vision_dot_FaceLandmarks__pb2._FACELANDMARKS
DESCRIPTOR.message_types_by_name['FaceLandmarksCollection'] = _FACELANDMARKSCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FaceLandmarksCollection = _reflection.GeneratedProtocolMessageType('FaceLandmarksCollection', (_message.Message,), dict(
  DESCRIPTOR = _FACELANDMARKSCOLLECTION,
  __module__ = 'rst.vision.FaceLandmarksCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.vision.FaceLandmarksCollection)
  ))
_sym_db.RegisterMessage(FaceLandmarksCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\033FaceLandmarksCollectionType'))
# @@protoc_insertion_point(module_scope)
