# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/kinematics/JointAccelerations.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/kinematics/JointAccelerations.proto',
  package='rst.kinematics',
  syntax='proto2',
  serialized_pb=_b('\n\'rst/kinematics/JointAccelerations.proto\x12\x0erst.kinematics\"/\n\x12JointAccelerations\x12\x19\n\raccelerations\x18\x01 \x03(\x02\x42\x02\x10\x01\x42\x18\x42\x16JointAccelerationsType')
)




_JOINTACCELERATIONS = _descriptor.Descriptor(
  name='JointAccelerations',
  full_name='rst.kinematics.JointAccelerations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='accelerations', full_name='rst.kinematics.JointAccelerations.accelerations', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
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
  serialized_start=59,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['JointAccelerations'] = _JOINTACCELERATIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JointAccelerations = _reflection.GeneratedProtocolMessageType('JointAccelerations', (_message.Message,), dict(
  DESCRIPTOR = _JOINTACCELERATIONS,
  __module__ = 'rst.kinematics.JointAccelerations_pb2'
  # @@protoc_insertion_point(class_scope:rst.kinematics.JointAccelerations)
  ))
_sym_db.RegisterMessage(JointAccelerations)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\026JointAccelerationsType'))
_JOINTACCELERATIONS.fields_by_name['accelerations'].has_options = True
_JOINTACCELERATIONS.fields_by_name['accelerations']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
