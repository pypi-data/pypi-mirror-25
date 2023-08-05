# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/tts/Prosody.proto

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
  name='rst/tts/Prosody.proto',
  package='rst.tts',
  syntax='proto2',
  serialized_pb=_b('\n\x15rst/tts/Prosody.proto\x12\x07rst.tts\"\xe6\x01\n\x07Prosody\x12%\n\x05pitch\x18\x01 \x01(\x0b\x32\x16.rst.tts.Prosody.Value\x12%\n\x05range\x18\x02 \x01(\x0b\x32\x16.rst.tts.Prosody.Value\x12&\n\x06volume\x18\x03 \x01(\x0b\x32\x16.rst.tts.Prosody.Value\x12\x10\n\x08\x64uration\x18\x04 \x01(\x02\x12\x0f\n\x04rate\x18\x05 \x01(\x02:\x01\x31\x1a\x42\n\x05Value\x12\x10\n\x08\x61\x62solute\x18\x01 \x01(\x02\x12\x10\n\x08relative\x18\x02 \x01(\x02\x12\x15\n\npercentage\x18\x03 \x01(\x02:\x01\x31\x42\rB\x0bProsodyType')
)




_PROSODY_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='rst.tts.Prosody.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='absolute', full_name='rst.tts.Prosody.Value.absolute', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='relative', full_name='rst.tts.Prosody.Value.relative', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='percentage', full_name='rst.tts.Prosody.Value.percentage', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
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
  serialized_start=199,
  serialized_end=265,
)

_PROSODY = _descriptor.Descriptor(
  name='Prosody',
  full_name='rst.tts.Prosody',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pitch', full_name='rst.tts.Prosody.pitch', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='range', full_name='rst.tts.Prosody.range', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='volume', full_name='rst.tts.Prosody.volume', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='duration', full_name='rst.tts.Prosody.duration', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rate', full_name='rst.tts.Prosody.rate', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PROSODY_VALUE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=265,
)

_PROSODY_VALUE.containing_type = _PROSODY
_PROSODY.fields_by_name['pitch'].message_type = _PROSODY_VALUE
_PROSODY.fields_by_name['range'].message_type = _PROSODY_VALUE
_PROSODY.fields_by_name['volume'].message_type = _PROSODY_VALUE
DESCRIPTOR.message_types_by_name['Prosody'] = _PROSODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Prosody = _reflection.GeneratedProtocolMessageType('Prosody', (_message.Message,), dict(

  Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), dict(
    DESCRIPTOR = _PROSODY_VALUE,
    __module__ = 'rst.tts.Prosody_pb2'
    # @@protoc_insertion_point(class_scope:rst.tts.Prosody.Value)
    ))
  ,
  DESCRIPTOR = _PROSODY,
  __module__ = 'rst.tts.Prosody_pb2'
  # @@protoc_insertion_point(class_scope:rst.tts.Prosody)
  ))
_sym_db.RegisterMessage(Prosody)
_sym_db.RegisterMessage(Prosody.Value)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\013ProsodyType'))
# @@protoc_insertion_point(module_scope)
