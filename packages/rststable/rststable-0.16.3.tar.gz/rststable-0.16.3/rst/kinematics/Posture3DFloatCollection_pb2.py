# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/kinematics/Posture3DFloatCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.kinematics import Posture3DFloat_pb2 as rst_dot_kinematics_dot_Posture3DFloat__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/kinematics/Posture3DFloatCollection.proto',
  package='rst.kinematics',
  syntax='proto2',
  serialized_pb=_b('\n-rst/kinematics/Posture3DFloatCollection.proto\x12\x0erst.kinematics\x1a#rst/kinematics/Posture3DFloat.proto\"K\n\x18Posture3DFloatCollection\x12/\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x1e.rst.kinematics.Posture3DFloatB\x1e\x42\x1cPosture3DFloatCollectionType')
  ,
  dependencies=[rst_dot_kinematics_dot_Posture3DFloat__pb2.DESCRIPTOR,])




_POSTURE3DFLOATCOLLECTION = _descriptor.Descriptor(
  name='Posture3DFloatCollection',
  full_name='rst.kinematics.Posture3DFloatCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.kinematics.Posture3DFloatCollection.element', index=0,
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
  serialized_start=102,
  serialized_end=177,
)

_POSTURE3DFLOATCOLLECTION.fields_by_name['element'].message_type = rst_dot_kinematics_dot_Posture3DFloat__pb2._POSTURE3DFLOAT
DESCRIPTOR.message_types_by_name['Posture3DFloatCollection'] = _POSTURE3DFLOATCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Posture3DFloatCollection = _reflection.GeneratedProtocolMessageType('Posture3DFloatCollection', (_message.Message,), dict(
  DESCRIPTOR = _POSTURE3DFLOATCOLLECTION,
  __module__ = 'rst.kinematics.Posture3DFloatCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.kinematics.Posture3DFloatCollection)
  ))
_sym_db.RegisterMessage(Posture3DFloatCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\034Posture3DFloatCollectionType'))
# @@protoc_insertion_point(module_scope)
