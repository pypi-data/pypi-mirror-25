# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/kinematics/JointPositionState.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.kinematics import JointState_pb2 as rst_dot_kinematics_dot_JointState__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/kinematics/JointPositionState.proto',
  package='rst.kinematics',
  syntax='proto2',
  serialized_pb=_b('\n\'rst/kinematics/JointPositionState.proto\x12\x0erst.kinematics\x1a\x1frst/kinematics/JointState.proto\"@\n\x12JointPositionState\x12*\n\x06joints\x18\x01 \x03(\x0b\x32\x1a.rst.kinematics.JointStateB\x18\x42\x16JointPositionStateType')
  ,
  dependencies=[rst_dot_kinematics_dot_JointState__pb2.DESCRIPTOR,])




_JOINTPOSITIONSTATE = _descriptor.Descriptor(
  name='JointPositionState',
  full_name='rst.kinematics.JointPositionState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='joints', full_name='rst.kinematics.JointPositionState.joints', index=0,
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
  serialized_start=92,
  serialized_end=156,
)

_JOINTPOSITIONSTATE.fields_by_name['joints'].message_type = rst_dot_kinematics_dot_JointState__pb2._JOINTSTATE
DESCRIPTOR.message_types_by_name['JointPositionState'] = _JOINTPOSITIONSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JointPositionState = _reflection.GeneratedProtocolMessageType('JointPositionState', (_message.Message,), dict(
  DESCRIPTOR = _JOINTPOSITIONSTATE,
  __module__ = 'rst.kinematics.JointPositionState_pb2'
  # @@protoc_insertion_point(class_scope:rst.kinematics.JointPositionState)
  ))
_sym_db.RegisterMessage(JointPositionState)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\026JointPositionStateType'))
# @@protoc_insertion_point(module_scope)
