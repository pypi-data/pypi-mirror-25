# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/scene/SceneObjects.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.scene import SceneObject_pb2 as rst_dot_scene_dot_SceneObject__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/scene/SceneObjects.proto',
  package='rst.scene',
  syntax='proto2',
  serialized_pb=_b('\n\x1crst/scene/SceneObjects.proto\x12\trst.scene\x1a\x1brst/scene/SceneObject.proto\"<\n\x0cSceneObjects\x12,\n\x0cscene_object\x18\x01 \x03(\x0b\x32\x16.rst.scene.SceneObjectB\x12\x42\x10SceneObjectsType')
  ,
  dependencies=[rst_dot_scene_dot_SceneObject__pb2.DESCRIPTOR,])




_SCENEOBJECTS = _descriptor.Descriptor(
  name='SceneObjects',
  full_name='rst.scene.SceneObjects',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scene_object', full_name='rst.scene.SceneObjects.scene_object', index=0,
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
  serialized_start=72,
  serialized_end=132,
)

_SCENEOBJECTS.fields_by_name['scene_object'].message_type = rst_dot_scene_dot_SceneObject__pb2._SCENEOBJECT
DESCRIPTOR.message_types_by_name['SceneObjects'] = _SCENEOBJECTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SceneObjects = _reflection.GeneratedProtocolMessageType('SceneObjects', (_message.Message,), dict(
  DESCRIPTOR = _SCENEOBJECTS,
  __module__ = 'rst.scene.SceneObjects_pb2'
  # @@protoc_insertion_point(class_scope:rst.scene.SceneObjects)
  ))
_sym_db.RegisterMessage(SceneObjects)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\020SceneObjectsType'))
# @@protoc_insertion_point(module_scope)
