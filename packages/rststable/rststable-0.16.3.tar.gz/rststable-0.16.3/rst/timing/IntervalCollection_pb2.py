# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/timing/IntervalCollection.proto

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
  name='rst/timing/IntervalCollection.proto',
  package='rst.timing',
  syntax='proto2',
  serialized_pb=_b('\n#rst/timing/IntervalCollection.proto\x12\nrst.timing\x1a\x19rst/timing/Interval.proto\";\n\x12IntervalCollection\x12%\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x14.rst.timing.IntervalB\x18\x42\x16IntervalCollectionType')
  ,
  dependencies=[rst_dot_timing_dot_Interval__pb2.DESCRIPTOR,])




_INTERVALCOLLECTION = _descriptor.Descriptor(
  name='IntervalCollection',
  full_name='rst.timing.IntervalCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.timing.IntervalCollection.element', index=0,
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
  serialized_start=78,
  serialized_end=137,
)

_INTERVALCOLLECTION.fields_by_name['element'].message_type = rst_dot_timing_dot_Interval__pb2._INTERVAL
DESCRIPTOR.message_types_by_name['IntervalCollection'] = _INTERVALCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IntervalCollection = _reflection.GeneratedProtocolMessageType('IntervalCollection', (_message.Message,), dict(
  DESCRIPTOR = _INTERVALCOLLECTION,
  __module__ = 'rst.timing.IntervalCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.timing.IntervalCollection)
  ))
_sym_db.RegisterMessage(IntervalCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\026IntervalCollectionType'))
# @@protoc_insertion_point(module_scope)
