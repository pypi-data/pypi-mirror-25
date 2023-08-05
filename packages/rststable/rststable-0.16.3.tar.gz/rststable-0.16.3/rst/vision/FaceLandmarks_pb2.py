# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/vision/FaceLandmarks.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.math import Vec2DInt_pb2 as rst_dot_math_dot_Vec2DInt__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/vision/FaceLandmarks.proto',
  package='rst.vision',
  syntax='proto2',
  serialized_pb=_b('\n\x1erst/vision/FaceLandmarks.proto\x12\nrst.vision\x1a\x17rst/math/Vec2DInt.proto\"\xe6\x02\n\rFaceLandmarks\x12\x1f\n\x03jaw\x18\x01 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12 \n\x04nose\x18\x02 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12&\n\nnose_wings\x18\x03 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12&\n\nright_brow\x18\x04 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12%\n\tleft_brow\x18\x05 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12%\n\tright_eye\x18\x06 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12$\n\x08left_eye\x18\x07 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12&\n\nouter_lips\x18\x08 \x03(\x0b\x32\x12.rst.math.Vec2DInt\x12&\n\ninner_lips\x18\t \x03(\x0b\x32\x12.rst.math.Vec2DIntB\x13\x42\x11\x46\x61\x63\x65LandmarksType')
  ,
  dependencies=[rst_dot_math_dot_Vec2DInt__pb2.DESCRIPTOR,])




_FACELANDMARKS = _descriptor.Descriptor(
  name='FaceLandmarks',
  full_name='rst.vision.FaceLandmarks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='jaw', full_name='rst.vision.FaceLandmarks.jaw', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nose', full_name='rst.vision.FaceLandmarks.nose', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nose_wings', full_name='rst.vision.FaceLandmarks.nose_wings', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='right_brow', full_name='rst.vision.FaceLandmarks.right_brow', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='left_brow', full_name='rst.vision.FaceLandmarks.left_brow', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='right_eye', full_name='rst.vision.FaceLandmarks.right_eye', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='left_eye', full_name='rst.vision.FaceLandmarks.left_eye', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='outer_lips', full_name='rst.vision.FaceLandmarks.outer_lips', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inner_lips', full_name='rst.vision.FaceLandmarks.inner_lips', index=8,
      number=9, type=11, cpp_type=10, label=3,
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
  serialized_end=430,
)

_FACELANDMARKS.fields_by_name['jaw'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['nose'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['nose_wings'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['right_brow'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['left_brow'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['right_eye'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['left_eye'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['outer_lips'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
_FACELANDMARKS.fields_by_name['inner_lips'].message_type = rst_dot_math_dot_Vec2DInt__pb2._VEC2DINT
DESCRIPTOR.message_types_by_name['FaceLandmarks'] = _FACELANDMARKS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FaceLandmarks = _reflection.GeneratedProtocolMessageType('FaceLandmarks', (_message.Message,), dict(
  DESCRIPTOR = _FACELANDMARKS,
  __module__ = 'rst.vision.FaceLandmarks_pb2'
  # @@protoc_insertion_point(class_scope:rst.vision.FaceLandmarks)
  ))
_sym_db.RegisterMessage(FaceLandmarks)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\021FaceLandmarksType'))
# @@protoc_insertion_point(module_scope)
