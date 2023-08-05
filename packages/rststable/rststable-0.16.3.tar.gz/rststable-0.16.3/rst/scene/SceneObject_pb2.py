# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/scene/SceneObject.proto

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
from rst.geometry import Shape3DFloat_pb2 as rst_dot_geometry_dot_Shape3DFloat__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/scene/SceneObject.proto',
  package='rst.scene',
  syntax='proto2',
  serialized_pb=_b('\n\x1brst/scene/SceneObject.proto\x12\trst.scene\x1a\x17rst/geometry/Pose.proto\x1a\x1frst/geometry/Shape3DFloat.proto\"x\n\x0bSceneObject\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12\"\n\x06\x63\x65nter\x18\x03 \x02(\x0b\x32\x12.rst.geometry.Pose\x12)\n\x05shape\x18\x04 \x01(\x0b\x32\x1a.rst.geometry.Shape3DFloatB\x11\x42\x0fSceneObjectType')
  ,
  dependencies=[rst_dot_geometry_dot_Pose__pb2.DESCRIPTOR,rst_dot_geometry_dot_Shape3DFloat__pb2.DESCRIPTOR,])




_SCENEOBJECT = _descriptor.Descriptor(
  name='SceneObject',
  full_name='rst.scene.SceneObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='rst.scene.SceneObject.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='kind', full_name='rst.scene.SceneObject.kind', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='center', full_name='rst.scene.SceneObject.center', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shape', full_name='rst.scene.SceneObject.shape', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=100,
  serialized_end=220,
)

_SCENEOBJECT.fields_by_name['center'].message_type = rst_dot_geometry_dot_Pose__pb2._POSE
_SCENEOBJECT.fields_by_name['shape'].message_type = rst_dot_geometry_dot_Shape3DFloat__pb2._SHAPE3DFLOAT
DESCRIPTOR.message_types_by_name['SceneObject'] = _SCENEOBJECT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SceneObject = _reflection.GeneratedProtocolMessageType('SceneObject', (_message.Message,), dict(
  DESCRIPTOR = _SCENEOBJECT,
  __module__ = 'rst.scene.SceneObject_pb2'
  # @@protoc_insertion_point(class_scope:rst.scene.SceneObject)
  ))
_sym_db.RegisterMessage(SceneObject)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\017SceneObjectType'))
# @@protoc_insertion_point(module_scope)
