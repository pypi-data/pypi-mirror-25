# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/dialog/SpeechHypotheses.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.dialog import SpeechHypothesis_pb2 as rst_dot_dialog_dot_SpeechHypothesis__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/dialog/SpeechHypotheses.proto',
  package='rst.dialog',
  syntax='proto2',
  serialized_pb=_b('\n!rst/dialog/SpeechHypotheses.proto\x12\nrst.dialog\x1a!rst/dialog/SpeechHypothesis.proto\"\x8b\x01\n\x10SpeechHypotheses\x12\x31\n\x0b\x62\x65st_result\x18\x01 \x02(\x0b\x32\x1c.rst.dialog.SpeechHypothesis\x12\x35\n\x0f\x66urther_results\x18\x02 \x03(\x0b\x32\x1c.rst.dialog.SpeechHypothesis\x12\r\n\x05\x66inal\x18\x03 \x02(\x08\x42\x16\x42\x14SpeechHypothesesType')
  ,
  dependencies=[rst_dot_dialog_dot_SpeechHypothesis__pb2.DESCRIPTOR,])




_SPEECHHYPOTHESES = _descriptor.Descriptor(
  name='SpeechHypotheses',
  full_name='rst.dialog.SpeechHypotheses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='best_result', full_name='rst.dialog.SpeechHypotheses.best_result', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='further_results', full_name='rst.dialog.SpeechHypotheses.further_results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='final', full_name='rst.dialog.SpeechHypotheses.final', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=85,
  serialized_end=224,
)

_SPEECHHYPOTHESES.fields_by_name['best_result'].message_type = rst_dot_dialog_dot_SpeechHypothesis__pb2._SPEECHHYPOTHESIS
_SPEECHHYPOTHESES.fields_by_name['further_results'].message_type = rst_dot_dialog_dot_SpeechHypothesis__pb2._SPEECHHYPOTHESIS
DESCRIPTOR.message_types_by_name['SpeechHypotheses'] = _SPEECHHYPOTHESES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SpeechHypotheses = _reflection.GeneratedProtocolMessageType('SpeechHypotheses', (_message.Message,), dict(
  DESCRIPTOR = _SPEECHHYPOTHESES,
  __module__ = 'rst.dialog.SpeechHypotheses_pb2'
  # @@protoc_insertion_point(class_scope:rst.dialog.SpeechHypotheses)
  ))
_sym_db.RegisterMessage(SpeechHypotheses)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\024SpeechHypothesesType'))
# @@protoc_insertion_point(module_scope)
