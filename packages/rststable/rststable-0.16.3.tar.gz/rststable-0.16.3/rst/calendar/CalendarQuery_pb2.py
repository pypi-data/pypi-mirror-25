# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/calendar/CalendarQuery.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.calendar import DateTime_pb2 as rst_dot_calendar_dot_DateTime__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/calendar/CalendarQuery.proto',
  package='rst.calendar',
  syntax='proto2',
  serialized_pb=_b('\n rst/calendar/CalendarQuery.proto\x12\x0crst.calendar\x1a\x1brst/calendar/DateTime.proto\"\xc5\x01\n\rCalendarQuery\x12*\n\nstart_time\x18\x01 \x01(\x0b\x32\x16.rst.calendar.DateTime\x12(\n\x08\x65nd_time\x18\x02 \x01(\x0b\x32\x16.rst.calendar.DateTime\x12\x1a\n\x0csearch_todos\x18\x03 \x01(\x08:\x04true\x12\x1b\n\rsearch_events\x18\x04 \x01(\x08:\x04true\x12%\n\x16\x63\x61lculate_time_periods\x18\x05 \x01(\x08:\x05\x66\x61lseB\x13\x42\x11\x43\x61lendarQueryType')
  ,
  dependencies=[rst_dot_calendar_dot_DateTime__pb2.DESCRIPTOR,])




_CALENDARQUERY = _descriptor.Descriptor(
  name='CalendarQuery',
  full_name='rst.calendar.CalendarQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_time', full_name='rst.calendar.CalendarQuery.start_time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_time', full_name='rst.calendar.CalendarQuery.end_time', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='search_todos', full_name='rst.calendar.CalendarQuery.search_todos', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='search_events', full_name='rst.calendar.CalendarQuery.search_events', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='calculate_time_periods', full_name='rst.calendar.CalendarQuery.calculate_time_periods', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=80,
  serialized_end=277,
)

_CALENDARQUERY.fields_by_name['start_time'].message_type = rst_dot_calendar_dot_DateTime__pb2._DATETIME
_CALENDARQUERY.fields_by_name['end_time'].message_type = rst_dot_calendar_dot_DateTime__pb2._DATETIME
DESCRIPTOR.message_types_by_name['CalendarQuery'] = _CALENDARQUERY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CalendarQuery = _reflection.GeneratedProtocolMessageType('CalendarQuery', (_message.Message,), dict(
  DESCRIPTOR = _CALENDARQUERY,
  __module__ = 'rst.calendar.CalendarQuery_pb2'
  # @@protoc_insertion_point(class_scope:rst.calendar.CalendarQuery)
  ))
_sym_db.RegisterMessage(CalendarQuery)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\021CalendarQueryType'))
# @@protoc_insertion_point(module_scope)
