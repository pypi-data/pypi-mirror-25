# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/dialog/SpeechHypothesis.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.timing import Interval_pb2 as rst_dot_timing_dot_Interval__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/dialog/SpeechHypothesis.proto',
  package='rst.dialog',
  syntax='proto2',
  serialized_pb=_b('\n!rst/dialog/SpeechHypothesis.proto\x12\nrst.dialog\x1a\x19rst/timing/Interval.proto\"\xd7\x01\n\x10SpeechHypothesis\x12\x30\n\x05words\x18\x01 \x03(\x0b\x32!.rst.dialog.SpeechHypothesis.Word\x12\x12\n\nconfidence\x18\x02 \x01(\x02\x12\'\n\ttimestamp\x18\x03 \x01(\x0b\x32\x14.rst.timing.Interval\x12\x14\n\x0cgrammar_tree\x18\x04 \x01(\t\x1a>\n\x04Word\x12\x0c\n\x04word\x18\x01 \x02(\t\x12(\n\ntimestamps\x18\x02 \x01(\x0b\x32\x14.rst.timing.IntervalB\x16\x42\x14SpeechHypothesisType')
  ,
  dependencies=[rst_dot_timing_dot_Interval__pb2.DESCRIPTOR,])




_SPEECHHYPOTHESIS_WORD = _descriptor.Descriptor(
  name='Word',
  full_name='rst.dialog.SpeechHypothesis.Word',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='word', full_name='rst.dialog.SpeechHypothesis.Word.word', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamps', full_name='rst.dialog.SpeechHypothesis.Word.timestamps', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=230,
  serialized_end=292,
)

_SPEECHHYPOTHESIS = _descriptor.Descriptor(
  name='SpeechHypothesis',
  full_name='rst.dialog.SpeechHypothesis',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='words', full_name='rst.dialog.SpeechHypothesis.words', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='confidence', full_name='rst.dialog.SpeechHypothesis.confidence', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='rst.dialog.SpeechHypothesis.timestamp', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='grammar_tree', full_name='rst.dialog.SpeechHypothesis.grammar_tree', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_SPEECHHYPOTHESIS_WORD, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=292,
)

_SPEECHHYPOTHESIS_WORD.fields_by_name['timestamps'].message_type = rst_dot_timing_dot_Interval__pb2._INTERVAL
_SPEECHHYPOTHESIS_WORD.containing_type = _SPEECHHYPOTHESIS
_SPEECHHYPOTHESIS.fields_by_name['words'].message_type = _SPEECHHYPOTHESIS_WORD
_SPEECHHYPOTHESIS.fields_by_name['timestamp'].message_type = rst_dot_timing_dot_Interval__pb2._INTERVAL
DESCRIPTOR.message_types_by_name['SpeechHypothesis'] = _SPEECHHYPOTHESIS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SpeechHypothesis = _reflection.GeneratedProtocolMessageType('SpeechHypothesis', (_message.Message,), dict(

  Word = _reflection.GeneratedProtocolMessageType('Word', (_message.Message,), dict(
    DESCRIPTOR = _SPEECHHYPOTHESIS_WORD,
    __module__ = 'rst.dialog.SpeechHypothesis_pb2'
    # @@protoc_insertion_point(class_scope:rst.dialog.SpeechHypothesis.Word)
    ))
  ,
  DESCRIPTOR = _SPEECHHYPOTHESIS,
  __module__ = 'rst.dialog.SpeechHypothesis_pb2'
  # @@protoc_insertion_point(class_scope:rst.dialog.SpeechHypothesis)
  ))
_sym_db.RegisterMessage(SpeechHypothesis)
_sym_db.RegisterMessage(SpeechHypothesis.Word)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\024SpeechHypothesisType'))
# @@protoc_insertion_point(module_scope)
