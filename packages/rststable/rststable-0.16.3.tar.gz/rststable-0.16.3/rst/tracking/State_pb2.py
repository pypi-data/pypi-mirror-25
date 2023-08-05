# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/tracking/State.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.tracking import TrackingInfo_pb2 as rst_dot_tracking_dot_TrackingInfo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/tracking/State.proto',
  package='rst.tracking',
  syntax='proto2',
  serialized_pb=_b('\n\x18rst/tracking/State.proto\x12\x0crst.tracking\x1a\x1frst/tracking/TrackingInfo.proto\"\xe8\x02\n\x05State\x12(\n\x04info\x18\x01 \x02(\x0b\x32\x1a.rst.tracking.TrackingInfo\x12.\n\x06\x61spect\x18\x02 \x03(\x0e\x32\x1a.rst.tracking.State.AspectB\x02\x10\x01\"\x84\x02\n\x06\x41spect\x12\x16\n\x12\x41SPECT_POSITION_2D\x10\x00\x12\x16\n\x12\x41SPECT_POSITION_3D\x10\x01\x12\'\n#ASPECT_AXIS_ALIGNED_BOUNDING_BOX_2D\x10\x02\x12\'\n#ASPECT_AXIS_ALIGNED_BOUNDING_BOX_3D\x10\x03\x12\x1a\n\x16\x41SPECT_BOUNDING_BOX_2D\x10\x04\x12\x1a\n\x16\x41SPECT_BOUNDING_BOX_3D\x10\x05\x12\x12\n\x0e\x41SPECT_CONTOUR\x10\x06\x12\x15\n\x11\x41SPECT_POSTURE_2D\x10\x07\x12\x15\n\x11\x41SPECT_POSTURE_3D\x10\x08\x42\x0b\x42\tStateType')
  ,
  dependencies=[rst_dot_tracking_dot_TrackingInfo__pb2.DESCRIPTOR,])



_STATE_ASPECT = _descriptor.EnumDescriptor(
  name='Aspect',
  full_name='rst.tracking.State.Aspect',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ASPECT_POSITION_2D', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_POSITION_3D', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_AXIS_ALIGNED_BOUNDING_BOX_2D', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_AXIS_ALIGNED_BOUNDING_BOX_3D', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_BOUNDING_BOX_2D', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_BOUNDING_BOX_3D', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_CONTOUR', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_POSTURE_2D', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASPECT_POSTURE_3D', index=8, number=8,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=176,
  serialized_end=436,
)
_sym_db.RegisterEnumDescriptor(_STATE_ASPECT)


_STATE = _descriptor.Descriptor(
  name='State',
  full_name='rst.tracking.State',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='rst.tracking.State.info', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aspect', full_name='rst.tracking.State.aspect', index=1,
      number=2, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STATE_ASPECT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=436,
)

_STATE.fields_by_name['info'].message_type = rst_dot_tracking_dot_TrackingInfo__pb2._TRACKINGINFO
_STATE.fields_by_name['aspect'].enum_type = _STATE_ASPECT
_STATE_ASPECT.containing_type = _STATE
DESCRIPTOR.message_types_by_name['State'] = _STATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

State = _reflection.GeneratedProtocolMessageType('State', (_message.Message,), dict(
  DESCRIPTOR = _STATE,
  __module__ = 'rst.tracking.State_pb2'
  # @@protoc_insertion_point(class_scope:rst.tracking.State)
  ))
_sym_db.RegisterMessage(State)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\tStateType'))
_STATE.fields_by_name['aspect'].has_options = True
_STATE.fields_by_name['aspect']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
