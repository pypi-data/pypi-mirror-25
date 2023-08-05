# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/generic/Value.proto

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
  name='rst/generic/Value.proto',
  package='rst.generic',
  syntax='proto2',
  serialized_pb=_b('\n\x17rst/generic/Value.proto\x12\x0brst.generic\"\xf0\x01\n\x05Value\x12%\n\x04type\x18\x01 \x02(\x0e\x32\x17.rst.generic.Value.Type\x12\x0b\n\x03int\x18\x02 \x01(\x03\x12\x0e\n\x06\x64ouble\x18\x03 \x01(\x01\x12\x0e\n\x06string\x18\x04 \x01(\t\x12\x0c\n\x04\x62ool\x18\x05 \x01(\x08\x12\x0e\n\x06\x62inary\x18\x06 \x01(\x0c\x12!\n\x05\x61rray\x18\x07 \x03(\x0b\x32\x12.rst.generic.Value\"R\n\x04Type\x12\x08\n\x04VOID\x10\x01\x12\x07\n\x03INT\x10\x02\x12\n\n\x06\x44OUBLE\x10\x03\x12\n\n\x06STRING\x10\x04\x12\x08\n\x04\x42OOL\x10\x05\x12\n\n\x06\x42INARY\x10\x06\x12\t\n\x05\x41RRAY\x10\x07\x42\x0b\x42\tValueType')
)



_VALUE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='rst.generic.Value.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VOID', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INT', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLE', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRING', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOOL', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BINARY', index=5, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARRAY', index=6, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=199,
  serialized_end=281,
)
_sym_db.RegisterEnumDescriptor(_VALUE_TYPE)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='rst.generic.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rst.generic.Value.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int', full_name='rst.generic.Value.int', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='double', full_name='rst.generic.Value.double', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='string', full_name='rst.generic.Value.string', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bool', full_name='rst.generic.Value.bool', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='binary', full_name='rst.generic.Value.binary', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='array', full_name='rst.generic.Value.array', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _VALUE_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=281,
)

_VALUE.fields_by_name['type'].enum_type = _VALUE_TYPE
_VALUE.fields_by_name['array'].message_type = _VALUE
_VALUE_TYPE.containing_type = _VALUE
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), dict(
  DESCRIPTOR = _VALUE,
  __module__ = 'rst.generic.Value_pb2'
  # @@protoc_insertion_point(class_scope:rst.generic.Value)
  ))
_sym_db.RegisterMessage(Value)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\tValueType'))
# @@protoc_insertion_point(module_scope)
