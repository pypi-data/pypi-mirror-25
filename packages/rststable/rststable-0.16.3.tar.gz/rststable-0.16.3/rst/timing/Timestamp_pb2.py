# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/timing/Timestamp.proto

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
  name='rst/timing/Timestamp.proto',
  package='rst.timing',
  syntax='proto2',
  serialized_pb=_b('\n\x1arst/timing/Timestamp.proto\x12\nrst.timing\"\x19\n\tTimestamp\x12\x0c\n\x04time\x18\x01 \x02(\x04\x42\x0f\x42\rTimestampType')
)




_TIMESTAMP = _descriptor.Descriptor(
  name='Timestamp',
  full_name='rst.timing.Timestamp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='rst.timing.Timestamp.time', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=42,
  serialized_end=67,
)

DESCRIPTOR.message_types_by_name['Timestamp'] = _TIMESTAMP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Timestamp = _reflection.GeneratedProtocolMessageType('Timestamp', (_message.Message,), dict(
  DESCRIPTOR = _TIMESTAMP,
  __module__ = 'rst.timing.Timestamp_pb2'
  # @@protoc_insertion_point(class_scope:rst.timing.Timestamp)
  ))
_sym_db.RegisterMessage(Timestamp)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\rTimestampType'))
# @@protoc_insertion_point(module_scope)
