# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/classification/ClassifiedRegions3D.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.classification import ClassifiedRegion3D_pb2 as rst_dot_classification_dot_ClassifiedRegion3D__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/classification/ClassifiedRegions3D.proto',
  package='rst.classification',
  syntax='proto2',
  serialized_pb=_b('\n,rst/classification/ClassifiedRegions3D.proto\x12\x12rst.classification\x1a+rst/classification/ClassifiedRegion3D.proto\"N\n\x13\x43lassifiedRegions3D\x12\x37\n\x07regions\x18\x01 \x03(\x0b\x32&.rst.classification.ClassifiedRegion3DB\x19\x42\x17\x43lassifiedRegions3DType')
  ,
  dependencies=[rst_dot_classification_dot_ClassifiedRegion3D__pb2.DESCRIPTOR,])




_CLASSIFIEDREGIONS3D = _descriptor.Descriptor(
  name='ClassifiedRegions3D',
  full_name='rst.classification.ClassifiedRegions3D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='regions', full_name='rst.classification.ClassifiedRegions3D.regions', index=0,
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
  serialized_start=113,
  serialized_end=191,
)

_CLASSIFIEDREGIONS3D.fields_by_name['regions'].message_type = rst_dot_classification_dot_ClassifiedRegion3D__pb2._CLASSIFIEDREGION3D
DESCRIPTOR.message_types_by_name['ClassifiedRegions3D'] = _CLASSIFIEDREGIONS3D
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ClassifiedRegions3D = _reflection.GeneratedProtocolMessageType('ClassifiedRegions3D', (_message.Message,), dict(
  DESCRIPTOR = _CLASSIFIEDREGIONS3D,
  __module__ = 'rst.classification.ClassifiedRegions3D_pb2'
  # @@protoc_insertion_point(class_scope:rst.classification.ClassifiedRegions3D)
  ))
_sym_db.RegisterMessage(ClassifiedRegions3D)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\027ClassifiedRegions3DType'))
# @@protoc_insertion_point(module_scope)
