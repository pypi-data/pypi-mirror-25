# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/vision/AugmentedPointCloudSet3DFloat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.vision import AugmentedPointCloud3DFloat_pb2 as rst_dot_vision_dot_AugmentedPointCloud3DFloat__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/vision/AugmentedPointCloudSet3DFloat.proto',
  package='rst.vision',
  syntax='proto2',
  serialized_pb=_b('\n.rst/vision/AugmentedPointCloudSet3DFloat.proto\x12\nrst.vision\x1a+rst/vision/AugmentedPointCloud3DFloat.proto\"W\n\x1d\x41ugmentedPointCloudSet3DFloat\x12\x36\n\x06\x63louds\x18\x01 \x03(\x0b\x32&.rst.vision.AugmentedPointCloud3DFloatB#B!AugmentedPointCloudSet3DFloatType')
  ,
  dependencies=[rst_dot_vision_dot_AugmentedPointCloud3DFloat__pb2.DESCRIPTOR,])




_AUGMENTEDPOINTCLOUDSET3DFLOAT = _descriptor.Descriptor(
  name='AugmentedPointCloudSet3DFloat',
  full_name='rst.vision.AugmentedPointCloudSet3DFloat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clouds', full_name='rst.vision.AugmentedPointCloudSet3DFloat.clouds', index=0,
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
  serialized_start=107,
  serialized_end=194,
)

_AUGMENTEDPOINTCLOUDSET3DFLOAT.fields_by_name['clouds'].message_type = rst_dot_vision_dot_AugmentedPointCloud3DFloat__pb2._AUGMENTEDPOINTCLOUD3DFLOAT
DESCRIPTOR.message_types_by_name['AugmentedPointCloudSet3DFloat'] = _AUGMENTEDPOINTCLOUDSET3DFLOAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AugmentedPointCloudSet3DFloat = _reflection.GeneratedProtocolMessageType('AugmentedPointCloudSet3DFloat', (_message.Message,), dict(
  DESCRIPTOR = _AUGMENTEDPOINTCLOUDSET3DFLOAT,
  __module__ = 'rst.vision.AugmentedPointCloudSet3DFloat_pb2'
  # @@protoc_insertion_point(class_scope:rst.vision.AugmentedPointCloudSet3DFloat)
  ))
_sym_db.RegisterMessage(AugmentedPointCloudSet3DFloat)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B!AugmentedPointCloudSet3DFloatType'))
# @@protoc_insertion_point(module_scope)
