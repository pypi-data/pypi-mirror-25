# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/geometry/PointCloud2DIntCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.geometry import PointCloud2DInt_pb2 as rst_dot_geometry_dot_PointCloud2DInt__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/geometry/PointCloud2DIntCollection.proto',
  package='rst.geometry',
  syntax='proto2',
  serialized_pb=_b('\n,rst/geometry/PointCloud2DIntCollection.proto\x12\x0crst.geometry\x1a\"rst/geometry/PointCloud2DInt.proto\"K\n\x19PointCloud2DIntCollection\x12.\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x1d.rst.geometry.PointCloud2DIntB\x1f\x42\x1dPointCloud2DIntCollectionType')
  ,
  dependencies=[rst_dot_geometry_dot_PointCloud2DInt__pb2.DESCRIPTOR,])




_POINTCLOUD2DINTCOLLECTION = _descriptor.Descriptor(
  name='PointCloud2DIntCollection',
  full_name='rst.geometry.PointCloud2DIntCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.geometry.PointCloud2DIntCollection.element', index=0,
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
  serialized_start=98,
  serialized_end=173,
)

_POINTCLOUD2DINTCOLLECTION.fields_by_name['element'].message_type = rst_dot_geometry_dot_PointCloud2DInt__pb2._POINTCLOUD2DINT
DESCRIPTOR.message_types_by_name['PointCloud2DIntCollection'] = _POINTCLOUD2DINTCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PointCloud2DIntCollection = _reflection.GeneratedProtocolMessageType('PointCloud2DIntCollection', (_message.Message,), dict(
  DESCRIPTOR = _POINTCLOUD2DINTCOLLECTION,
  __module__ = 'rst.geometry.PointCloud2DIntCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.geometry.PointCloud2DIntCollection)
  ))
_sym_db.RegisterMessage(PointCloud2DIntCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\035PointCloud2DIntCollectionType'))
# @@protoc_insertion_point(module_scope)
