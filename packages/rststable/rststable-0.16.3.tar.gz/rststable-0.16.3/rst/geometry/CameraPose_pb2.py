# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/geometry/CameraPose.proto

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
  name='rst/geometry/CameraPose.proto',
  package='rst.geometry',
  syntax='proto2',
  serialized_pb=_b('\n\x1drst/geometry/CameraPose.proto\x12\x0crst.geometry\x1a\x17rst/geometry/Pose.proto\"\x82\x02\n\nCameraPose\x12V\n\x10\x63oordinate_frame\x18\x01 \x01(\x0e\x32(.rst.geometry.CameraPose.CoordinateFrame:\x12\x43\x41MERA_IMAGE_FRAME\x12 \n\x04pose\x18\x02 \x02(\x0b\x32\x12.rst.geometry.Pose\"z\n\x0f\x43oordinateFrame\x12\x16\n\x12\x43\x41MERA_IMAGE_FRAME\x10\x00\x12\x15\n\x11\x43\x41MERA_X_UP_FRAME\x10\x01\x12\x15\n\x11\x43\x41MERA_Y_UP_FRAME\x10\x02\x12\x0f\n\x0bLASER_FRAME\x10\x03\x12\x10\n\x0cSCREEN_FRAME\x10\x04\x42\x10\x42\x0e\x43\x61meraPoseType')
  ,
  dependencies=[rst_dot_geometry_dot_Pose__pb2.DESCRIPTOR,])



_CAMERAPOSE_COORDINATEFRAME = _descriptor.EnumDescriptor(
  name='CoordinateFrame',
  full_name='rst.geometry.CameraPose.CoordinateFrame',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CAMERA_IMAGE_FRAME', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAMERA_X_UP_FRAME', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAMERA_Y_UP_FRAME', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LASER_FRAME', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SCREEN_FRAME', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=209,
  serialized_end=331,
)
_sym_db.RegisterEnumDescriptor(_CAMERAPOSE_COORDINATEFRAME)


_CAMERAPOSE = _descriptor.Descriptor(
  name='CameraPose',
  full_name='rst.geometry.CameraPose',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='coordinate_frame', full_name='rst.geometry.CameraPose.coordinate_frame', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pose', full_name='rst.geometry.CameraPose.pose', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CAMERAPOSE_COORDINATEFRAME,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=331,
)

_CAMERAPOSE.fields_by_name['coordinate_frame'].enum_type = _CAMERAPOSE_COORDINATEFRAME
_CAMERAPOSE.fields_by_name['pose'].message_type = rst_dot_geometry_dot_Pose__pb2._POSE
_CAMERAPOSE_COORDINATEFRAME.containing_type = _CAMERAPOSE
DESCRIPTOR.message_types_by_name['CameraPose'] = _CAMERAPOSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CameraPose = _reflection.GeneratedProtocolMessageType('CameraPose', (_message.Message,), dict(
  DESCRIPTOR = _CAMERAPOSE,
  __module__ = 'rst.geometry.CameraPose_pb2'
  # @@protoc_insertion_point(class_scope:rst.geometry.CameraPose)
  ))
_sym_db.RegisterMessage(CameraPose)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\016CameraPoseType'))
# @@protoc_insertion_point(module_scope)
