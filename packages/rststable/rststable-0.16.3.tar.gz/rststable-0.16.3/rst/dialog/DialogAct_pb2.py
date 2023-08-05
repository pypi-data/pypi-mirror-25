# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/dialog/DialogAct.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.dialog import IncrementalUnit_pb2 as rst_dot_dialog_dot_IncrementalUnit__pb2
from rst.dialog import SpeechHypotheses_pb2 as rst_dot_dialog_dot_SpeechHypotheses__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/dialog/DialogAct.proto',
  package='rst.dialog',
  syntax='proto2',
  serialized_pb=_b('\n\x1arst/dialog/DialogAct.proto\x12\nrst.dialog\x1a rst/dialog/IncrementalUnit.proto\x1a!rst/dialog/SpeechHypotheses.proto\"\xc3\x02\n\tDialogAct\x12(\n\x04type\x18\x01 \x02(\x0e\x32\x1a.rst.dialog.DialogAct.Type\x12\x35\n\x10incremental_unit\x18\x02 \x02(\x0b\x32\x1b.rst.dialog.IncrementalUnit\x12\x37\n\x11speech_hypotheses\x18\x03 \x01(\x0b\x32\x1c.rst.dialog.SpeechHypotheses\"\x9b\x01\n\x04Type\x12\t\n\x05GREET\x10\x00\x12\n\n\x06\x41\x43\x43\x45PT\x10\x01\x12\n\n\x06REJECT\x10\x02\x12\x0b\n\x07\x43ONFIRM\x10\x03\x12\n\n\x06NEGATE\x10\x04\x12\x10\n\x0cINFO_REQUEST\x10\x05\x12\x12\n\x0e\x41\x43TION_REQUEST\x10\x06\x12\r\n\tSTATEMENT\x10\x07\x12\n\n\x06\x41NSWER\x10\x08\x12\x0b\n\x07GOODBYE\x10\t\x12\t\n\x05OTHER\x10\x64\x42\x0f\x42\rDialogActType')
  ,
  dependencies=[rst_dot_dialog_dot_IncrementalUnit__pb2.DESCRIPTOR,rst_dot_dialog_dot_SpeechHypotheses__pb2.DESCRIPTOR,])



_DIALOGACT_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='rst.dialog.DialogAct.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GREET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCEPT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REJECT', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONFIRM', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEGATE', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO_REQUEST', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACTION_REQUEST', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATEMENT', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANSWER', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOODBYE', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OTHER', index=10, number=100,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=280,
  serialized_end=435,
)
_sym_db.RegisterEnumDescriptor(_DIALOGACT_TYPE)


_DIALOGACT = _descriptor.Descriptor(
  name='DialogAct',
  full_name='rst.dialog.DialogAct',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rst.dialog.DialogAct.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='incremental_unit', full_name='rst.dialog.DialogAct.incremental_unit', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speech_hypotheses', full_name='rst.dialog.DialogAct.speech_hypotheses', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DIALOGACT_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=112,
  serialized_end=435,
)

_DIALOGACT.fields_by_name['type'].enum_type = _DIALOGACT_TYPE
_DIALOGACT.fields_by_name['incremental_unit'].message_type = rst_dot_dialog_dot_IncrementalUnit__pb2._INCREMENTALUNIT
_DIALOGACT.fields_by_name['speech_hypotheses'].message_type = rst_dot_dialog_dot_SpeechHypotheses__pb2._SPEECHHYPOTHESES
_DIALOGACT_TYPE.containing_type = _DIALOGACT
DESCRIPTOR.message_types_by_name['DialogAct'] = _DIALOGACT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DialogAct = _reflection.GeneratedProtocolMessageType('DialogAct', (_message.Message,), dict(
  DESCRIPTOR = _DIALOGACT,
  __module__ = 'rst.dialog.DialogAct_pb2'
  # @@protoc_insertion_point(class_scope:rst.dialog.DialogAct)
  ))
_sym_db.RegisterMessage(DialogAct)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\rDialogActType'))
# @@protoc_insertion_point(module_scope)
