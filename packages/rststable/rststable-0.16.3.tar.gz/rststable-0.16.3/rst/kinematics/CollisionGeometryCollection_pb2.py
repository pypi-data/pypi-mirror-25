# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/kinematics/CollisionGeometryCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.kinematics import CollisionGeometry_pb2 as rst_dot_kinematics_dot_CollisionGeometry__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/kinematics/CollisionGeometryCollection.proto',
  package='rst.kinematics',
  syntax='proto2',
  serialized_pb=_b('\n0rst/kinematics/CollisionGeometryCollection.proto\x12\x0erst.kinematics\x1a&rst/kinematics/CollisionGeometry.proto\"Q\n\x1b\x43ollisionGeometryCollection\x12\x32\n\x07\x65lement\x18\x01 \x03(\x0b\x32!.rst.kinematics.CollisionGeometryB!B\x1f\x43ollisionGeometryCollectionType')
  ,
  dependencies=[rst_dot_kinematics_dot_CollisionGeometry__pb2.DESCRIPTOR,])




_COLLISIONGEOMETRYCOLLECTION = _descriptor.Descriptor(
  name='CollisionGeometryCollection',
  full_name='rst.kinematics.CollisionGeometryCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.kinematics.CollisionGeometryCollection.element', index=0,
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
  serialized_start=108,
  serialized_end=189,
)

_COLLISIONGEOMETRYCOLLECTION.fields_by_name['element'].message_type = rst_dot_kinematics_dot_CollisionGeometry__pb2._COLLISIONGEOMETRY
DESCRIPTOR.message_types_by_name['CollisionGeometryCollection'] = _COLLISIONGEOMETRYCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CollisionGeometryCollection = _reflection.GeneratedProtocolMessageType('CollisionGeometryCollection', (_message.Message,), dict(
  DESCRIPTOR = _COLLISIONGEOMETRYCOLLECTION,
  __module__ = 'rst.kinematics.CollisionGeometryCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.kinematics.CollisionGeometryCollection)
  ))
_sym_db.RegisterMessage(CollisionGeometryCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\037CollisionGeometryCollectionType'))
# @@protoc_insertion_point(module_scope)
