# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/audition/InterauralTimeDifference.proto

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
  name='rst/audition/InterauralTimeDifference.proto',
  package='rst.audition',
  syntax='proto2',
  serialized_pb=_b('\n+rst/audition/InterauralTimeDifference.proto\x12\x0crst.audition\"c\n\x18InterauralTimeDifference\x12\r\n\x05value\x18\x01 \x03(\x02\x12\x0e\n\x06weight\x18\x02 \x03(\x02\x12\x13\n\x0b\x66rame_shift\x18\x03 \x02(\x02\x12\x13\n\x0btime_window\x18\x04 \x02(\x02\x42\x1e\x42\x1cInterauralTimeDifferenceType')
)




_INTERAURALTIMEDIFFERENCE = _descriptor.Descriptor(
  name='InterauralTimeDifference',
  full_name='rst.audition.InterauralTimeDifference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='rst.audition.InterauralTimeDifference.value', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weight', full_name='rst.audition.InterauralTimeDifference.weight', index=1,
      number=2, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame_shift', full_name='rst.audition.InterauralTimeDifference.frame_shift', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_window', full_name='rst.audition.InterauralTimeDifference.time_window', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=61,
  serialized_end=160,
)

DESCRIPTOR.message_types_by_name['InterauralTimeDifference'] = _INTERAURALTIMEDIFFERENCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InterauralTimeDifference = _reflection.GeneratedProtocolMessageType('InterauralTimeDifference', (_message.Message,), dict(
  DESCRIPTOR = _INTERAURALTIMEDIFFERENCE,
  __module__ = 'rst.audition.InterauralTimeDifference_pb2'
  # @@protoc_insertion_point(class_scope:rst.audition.InterauralTimeDifference)
  ))
_sym_db.RegisterMessage(InterauralTimeDifference)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\034InterauralTimeDifferenceType'))
# @@protoc_insertion_point(module_scope)
