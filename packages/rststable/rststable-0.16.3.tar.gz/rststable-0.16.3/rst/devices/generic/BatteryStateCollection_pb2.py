# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/devices/generic/BatteryStateCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.devices.generic import BatteryState_pb2 as rst_dot_devices_dot_generic_dot_BatteryState__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/devices/generic/BatteryStateCollection.proto',
  package='rst.devices.generic',
  syntax='proto2',
  serialized_pb=_b('\n0rst/devices/generic/BatteryStateCollection.proto\x12\x13rst.devices.generic\x1a&rst/devices/generic/BatteryState.proto\"L\n\x16\x42\x61tteryStateCollection\x12\x32\n\x07\x65lement\x18\x01 \x03(\x0b\x32!.rst.devices.generic.BatteryStateB\x1c\x42\x1a\x42\x61tteryStateCollectionType')
  ,
  dependencies=[rst_dot_devices_dot_generic_dot_BatteryState__pb2.DESCRIPTOR,])




_BATTERYSTATECOLLECTION = _descriptor.Descriptor(
  name='BatteryStateCollection',
  full_name='rst.devices.generic.BatteryStateCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='rst.devices.generic.BatteryStateCollection.element', index=0,
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
  serialized_end=189,
)

_BATTERYSTATECOLLECTION.fields_by_name['element'].message_type = rst_dot_devices_dot_generic_dot_BatteryState__pb2._BATTERYSTATE
DESCRIPTOR.message_types_by_name['BatteryStateCollection'] = _BATTERYSTATECOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BatteryStateCollection = _reflection.GeneratedProtocolMessageType('BatteryStateCollection', (_message.Message,), dict(
  DESCRIPTOR = _BATTERYSTATECOLLECTION,
  __module__ = 'rst.devices.generic.BatteryStateCollection_pb2'
  # @@protoc_insertion_point(class_scope:rst.devices.generic.BatteryStateCollection)
  ))
_sym_db.RegisterMessage(BatteryStateCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\032BatteryStateCollectionType'))
# @@protoc_insertion_point(module_scope)
