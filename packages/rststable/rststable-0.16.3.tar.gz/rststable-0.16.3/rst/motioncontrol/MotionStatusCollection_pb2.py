# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/motioncontrol/MotionStatusCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.motioncontrol import MotionStatus_pb2 as rst_dot_motioncontrol_dot_MotionStatus__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/motioncontrol/MotionStatusCollection.proto',
  package='rst.motioncontrol',
  syntax='proto2',
  serialized_pb=_b('\n.rst/motioncontrol/MotionStatusCollection.proto\x12\x11rst.motioncontrol\x1a$rst/motioncontrol/MotionStatus.proto\"J\n\x16MotionStatusCollection\x12\x30\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x1f.rst.motioncontrol.MotionStatusB\x1c\x42\x1aMotionStatusCollectionType')
  ,
  dependencies=[rst_dot_motioncontrol_dot_MotionStatus__pb2.DESCRIPTOR,])




_MOTIONSTATUSCOLLECTION = _descriptor.Descriptor(
  name='MotionStatusCollection',
  full_name='rst.motioncontrol.MotionStatusCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.motioncontrol.MotionStatusCollection.element', index=0,
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
  serialized_end=181,
)

_MOTIONSTATUSCOLLECTION.fields_by_name['element'].message_type = rst_dot_motioncontrol_dot_MotionStatus__pb2._MOTIONSTATUS
DESCRIPTOR.message_types_by_name['MotionStatusCollection'] = _MOTIONSTATUSCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MotionStatusCollection = _reflection.GeneratedProtocolMessageType('MotionStatusCollection', (_message.Message,), dict(
  DESCRIPTOR = _MOTIONSTATUSCOLLECTION,
  __module__ = 'rst.motioncontrol.MotionStatusCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.motioncontrol.MotionStatusCollection)
  ))
_sym_db.RegisterMessage(MotionStatusCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\032MotionStatusCollectionType'))
# @@protoc_insertion_point(module_scope)
