# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/navigation/CommandResult.proto

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
  name='rst/navigation/CommandResult.proto',
  package='rst.navigation',
  syntax='proto2',
  serialized_pb=_b('\n\"rst/navigation/CommandResult.proto\x12\x0erst.navigation\"\xf8\x01\n\rCommandResult\x12\x32\n\x04type\x18\x01 \x02(\x0e\x32$.rst.navigation.CommandResult.Result\x12\x0c\n\x04\x63ode\x18\x02 \x01(\r\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"\x8f\x01\n\x06Result\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0e\n\nSUPERSEDED\x10\x01\x12\r\n\tCANCELLED\x10\x02\x12\x15\n\x11\x45MERGENCY_STOPPED\x10\x03\x12\x10\n\x0cPATH_BLOCKED\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x10\n\x0c\x43USTOM_ERROR\x10\x64\x12\x11\n\rUNKNOWN_ERROR\x10\x65\x42\x13\x42\x11\x43ommandResultType')
)



_COMMANDRESULT_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='rst.navigation.CommandResult.Result',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUPERSEDED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANCELLED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EMERGENCY_STOPPED', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATH_BLOCKED', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TIMEOUT', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_ERROR', index=6, number=100,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_ERROR', index=7, number=101,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=160,
  serialized_end=303,
)
_sym_db.RegisterEnumDescriptor(_COMMANDRESULT_RESULT)


_COMMANDRESULT = _descriptor.Descriptor(
  name='CommandResult',
  full_name='rst.navigation.CommandResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rst.navigation.CommandResult.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='rst.navigation.CommandResult.code', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='rst.navigation.CommandResult.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMMANDRESULT_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=55,
  serialized_end=303,
)

_COMMANDRESULT.fields_by_name['type'].enum_type = _COMMANDRESULT_RESULT
_COMMANDRESULT_RESULT.containing_type = _COMMANDRESULT
DESCRIPTOR.message_types_by_name['CommandResult'] = _COMMANDRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CommandResult = _reflection.GeneratedProtocolMessageType('CommandResult', (_message.Message,), dict(
  DESCRIPTOR = _COMMANDRESULT,
  __module__ = 'rst.navigation.CommandResult_pb2'
  # @@protoc_insertion_point(class_scope:rst.navigation.CommandResult)
  ))
_sym_db.RegisterMessage(CommandResult)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\021CommandResultType'))
# @@protoc_insertion_point(module_scope)
