# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/vision/Images.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.vision import Image_pb2 as rst_dot_vision_dot_Image__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/vision/Images.proto',
  package='rst.vision',
  syntax='proto2',
  serialized_pb=_b('\n\x17rst/vision/Images.proto\x12\nrst.vision\x1a\x16rst/vision/Image.proto\"+\n\x06Images\x12!\n\x06images\x18\x01 \x03(\x0b\x32\x11.rst.vision.ImageB\x0c\x42\nImagesType')
  ,
  dependencies=[rst_dot_vision_dot_Image__pb2.DESCRIPTOR,])




_IMAGES = _descriptor.Descriptor(
  name='Images',
  full_name='rst.vision.Images',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='images', full_name='rst.vision.Images.images', index=0,
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
  serialized_start=63,
  serialized_end=106,
)

_IMAGES.fields_by_name['images'].message_type = rst_dot_vision_dot_Image__pb2._IMAGE
DESCRIPTOR.message_types_by_name['Images'] = _IMAGES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Images = _reflection.GeneratedProtocolMessageType('Images', (_message.Message,), dict(
  DESCRIPTOR = _IMAGES,
  __module__ = 'rst.vision.Images_pb2'
  # @@protoc_insertion_point(class_scope:rst.vision.Images)
  ))
_sym_db.RegisterMessage(Images)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\nImagesType'))
# @@protoc_insertion_point(module_scope)
