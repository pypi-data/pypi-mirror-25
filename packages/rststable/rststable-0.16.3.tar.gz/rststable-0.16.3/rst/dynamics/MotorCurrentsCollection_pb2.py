# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/dynamics/MotorCurrentsCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.dynamics import MotorCurrents_pb2 as rst_dot_dynamics_dot_MotorCurrents__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/dynamics/MotorCurrentsCollection.proto',
  package='rst.dynamics',
  syntax='proto2',
  serialized_pb=_b('\n*rst/dynamics/MotorCurrentsCollection.proto\x12\x0crst.dynamics\x1a rst/dynamics/MotorCurrents.proto\"G\n\x17MotorCurrentsCollection\x12,\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x1b.rst.dynamics.MotorCurrentsB\x1d\x42\x1bMotorCurrentsCollectionType')
  ,
  dependencies=[rst_dot_dynamics_dot_MotorCurrents__pb2.DESCRIPTOR,])




_MOTORCURRENTSCOLLECTION = _descriptor.Descriptor(
  name='MotorCurrentsCollection',
  full_name='rst.dynamics.MotorCurrentsCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.dynamics.MotorCurrentsCollection.element', index=0,
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
  serialized_start=94,
  serialized_end=165,
)

_MOTORCURRENTSCOLLECTION.fields_by_name['element'].message_type = rst_dot_dynamics_dot_MotorCurrents__pb2._MOTORCURRENTS
DESCRIPTOR.message_types_by_name['MotorCurrentsCollection'] = _MOTORCURRENTSCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MotorCurrentsCollection = _reflection.GeneratedProtocolMessageType('MotorCurrentsCollection', (_message.Message,), dict(
  DESCRIPTOR = _MOTORCURRENTSCOLLECTION,
  __module__ = 'rst.dynamics.MotorCurrentsCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.dynamics.MotorCurrentsCollection)
  ))
_sym_db.RegisterMessage(MotorCurrentsCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\033MotorCurrentsCollectionType'))
# @@protoc_insertion_point(module_scope)
