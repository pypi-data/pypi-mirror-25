# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/geometry/PointCloudSet3DFloat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.geometry import PointCloud3DFloat_pb2 as rst_dot_geometry_dot_PointCloud3DFloat__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/geometry/PointCloudSet3DFloat.proto',
  package='rst.geometry',
  syntax='proto2',
  serialized_pb=_b('\n\'rst/geometry/PointCloudSet3DFloat.proto\x12\x0crst.geometry\x1a$rst/geometry/PointCloud3DFloat.proto\"G\n\x14PointCloudSet3DFloat\x12/\n\x06\x63louds\x18\x01 \x03(\x0b\x32\x1f.rst.geometry.PointCloud3DFloatB\x1a\x42\x18PointCloudSet3DFloatType')
  ,
  dependencies=[rst_dot_geometry_dot_PointCloud3DFloat__pb2.DESCRIPTOR,])




_POINTCLOUDSET3DFLOAT = _descriptor.Descriptor(
  name='PointCloudSet3DFloat',
  full_name='rst.geometry.PointCloudSet3DFloat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clouds', full_name='rst.geometry.PointCloudSet3DFloat.clouds', index=0,
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
  serialized_start=95,
  serialized_end=166,
)

_POINTCLOUDSET3DFLOAT.fields_by_name['clouds'].message_type = rst_dot_geometry_dot_PointCloud3DFloat__pb2._POINTCLOUD3DFLOAT
DESCRIPTOR.message_types_by_name['PointCloudSet3DFloat'] = _POINTCLOUDSET3DFLOAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PointCloudSet3DFloat = _reflection.GeneratedProtocolMessageType('PointCloudSet3DFloat', (_message.Message,), dict(
  DESCRIPTOR = _POINTCLOUDSET3DFLOAT,
  __module__ = 'rst.geometry.PointCloudSet3DFloat_pb2'
  # @@protoc_insertion_point(class_scope:rst.geometry.PointCloudSet3DFloat)
  ))
_sym_db.RegisterMessage(PointCloudSet3DFloat)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\030PointCloudSet3DFloatType'))
# @@protoc_insertion_point(module_scope)
