# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/navigation/OccupancyGrid2DInt.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.geometry import Pose_pb2 as rst_dot_geometry_dot_Pose__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/navigation/OccupancyGrid2DInt.proto',
  package='rst.navigation',
  syntax='proto2',
  serialized_pb=_b('\n\'rst/navigation/OccupancyGrid2DInt.proto\x12\x0erst.navigation\x1a\x17rst/geometry/Pose.proto\"x\n\x12OccupancyGrid2DInt\x12\x12\n\nresolution\x18\x01 \x02(\x02\x12\r\n\x05width\x18\x02 \x02(\r\x12\x0e\n\x06height\x18\x03 \x02(\r\x12\"\n\x06origin\x18\x04 \x02(\x0b\x32\x12.rst.geometry.Pose\x12\x0b\n\x03map\x18\x05 \x02(\x0c\x42\x18\x42\x16OccupancyGrid2DIntType')
  ,
  dependencies=[rst_dot_geometry_dot_Pose__pb2.DESCRIPTOR,])




_OCCUPANCYGRID2DINT = _descriptor.Descriptor(
  name='OccupancyGrid2DInt',
  full_name='rst.navigation.OccupancyGrid2DInt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resolution', full_name='rst.navigation.OccupancyGrid2DInt.resolution', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width', full_name='rst.navigation.OccupancyGrid2DInt.width', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height', full_name='rst.navigation.OccupancyGrid2DInt.height', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='origin', full_name='rst.navigation.OccupancyGrid2DInt.origin', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='map', full_name='rst.navigation.OccupancyGrid2DInt.map', index=4,
      number=5, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
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
  serialized_end=204,
)

_OCCUPANCYGRID2DINT.fields_by_name['origin'].message_type = rst_dot_geometry_dot_Pose__pb2._POSE
DESCRIPTOR.message_types_by_name['OccupancyGrid2DInt'] = _OCCUPANCYGRID2DINT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OccupancyGrid2DInt = _reflection.GeneratedProtocolMessageType('OccupancyGrid2DInt', (_message.Message,), dict(
  DESCRIPTOR = _OCCUPANCYGRID2DINT,
  __module__ = 'rst.navigation.OccupancyGrid2DInt_pb2'
  # @@protoc_insertion_point(class_scope:rst.navigation.OccupancyGrid2DInt)
  ))
_sym_db.RegisterMessage(OccupancyGrid2DInt)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\026OccupancyGrid2DIntType'))
# @@protoc_insertion_point(module_scope)
