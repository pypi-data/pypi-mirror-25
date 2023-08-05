# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/calendar/CalendarComponents.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.calendar import TimeZone_pb2 as rst_dot_calendar_dot_TimeZone__pb2
from rst.calendar import Event_pb2 as rst_dot_calendar_dot_Event__pb2
from rst.calendar import Todo_pb2 as rst_dot_calendar_dot_Todo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/calendar/CalendarComponents.proto',
  package='rst.calendar',
  syntax='proto2',
  serialized_pb=_b('\n%rst/calendar/CalendarComponents.proto\x12\x0crst.calendar\x1a\x1brst/calendar/TimeZone.proto\x1a\x18rst/calendar/Event.proto\x1a\x17rst/calendar/Todo.proto\"\x87\x01\n\x12\x43\x61lendarComponents\x12)\n\ttimezones\x18\x01 \x03(\x0b\x32\x16.rst.calendar.TimeZone\x12#\n\x06\x65vents\x18\x02 \x03(\x0b\x32\x13.rst.calendar.Event\x12!\n\x05todos\x18\x03 \x03(\x0b\x32\x12.rst.calendar.TodoB\x18\x42\x16\x43\x61lendarComponentsType')
  ,
  dependencies=[rst_dot_calendar_dot_TimeZone__pb2.DESCRIPTOR,rst_dot_calendar_dot_Event__pb2.DESCRIPTOR,rst_dot_calendar_dot_Todo__pb2.DESCRIPTOR,])




_CALENDARCOMPONENTS = _descriptor.Descriptor(
  name='CalendarComponents',
  full_name='rst.calendar.CalendarComponents',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timezones', full_name='rst.calendar.CalendarComponents.timezones', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='events', full_name='rst.calendar.CalendarComponents.events', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='todos', full_name='rst.calendar.CalendarComponents.todos', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=136,
  serialized_end=271,
)

_CALENDARCOMPONENTS.fields_by_name['timezones'].message_type = rst_dot_calendar_dot_TimeZone__pb2._TIMEZONE
_CALENDARCOMPONENTS.fields_by_name['events'].message_type = rst_dot_calendar_dot_Event__pb2._EVENT
_CALENDARCOMPONENTS.fields_by_name['todos'].message_type = rst_dot_calendar_dot_Todo__pb2._TODO
DESCRIPTOR.message_types_by_name['CalendarComponents'] = _CALENDARCOMPONENTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CalendarComponents = _reflection.GeneratedProtocolMessageType('CalendarComponents', (_message.Message,), dict(
  DESCRIPTOR = _CALENDARCOMPONENTS,
  __module__ = 'rst.calendar.CalendarComponents_pb2'
  # @@protoc_insertion_point(class_scope:rst.calendar.CalendarComponents)
  ))
_sym_db.RegisterMessage(CalendarComponents)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\026CalendarComponentsType'))
# @@protoc_insertion_point(module_scope)
