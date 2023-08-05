# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/cbse/ComponentInfo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rst.cbse import ComponentState_pb2 as rst_dot_cbse_dot_ComponentState__pb2
from rst.cbse import InputPort_pb2 as rst_dot_cbse_dot_InputPort__pb2
from rst.cbse import OutputPort_pb2 as rst_dot_cbse_dot_OutputPort__pb2
from rst.timing import Duration_pb2 as rst_dot_timing_dot_Duration__pb2
from rst.timing import Frequency_pb2 as rst_dot_timing_dot_Frequency__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rst/cbse/ComponentInfo.proto',
  package='rst.cbse',
  syntax='proto2',
  serialized_pb=_b('\n\x1crst/cbse/ComponentInfo.proto\x12\x08rst.cbse\x1a\x1drst/cbse/ComponentState.proto\x1a\x18rst/cbse/InputPort.proto\x1a\x19rst/cbse/OutputPort.proto\x1a\x19rst/timing/Duration.proto\x1a\x1arst/timing/Frequency.proto\"\xe3\x01\n\rComponentInfo\x12\n\n\x02id\x18\x01 \x02(\t\x12+\n\tlifecycle\x18\x02 \x02(\x0b\x32\x18.rst.cbse.ComponentState\x12#\n\x06inputs\x18\x03 \x02(\x0b\x32\x13.rst.cbse.InputPort\x12%\n\x07outputs\x18\x04 \x02(\x0b\x32\x14.rst.cbse.OutputPort\x12$\n\x06uptime\x18\x05 \x01(\x0b\x32\x14.rst.timing.Duration\x12\'\n\x08\x66reqency\x18\x06 \x01(\x0b\x32\x15.rst.timing.FrequencyB\x13\x42\x11\x43omponentInfoType')
  ,
  dependencies=[rst_dot_cbse_dot_ComponentState__pb2.DESCRIPTOR,rst_dot_cbse_dot_InputPort__pb2.DESCRIPTOR,rst_dot_cbse_dot_OutputPort__pb2.DESCRIPTOR,rst_dot_timing_dot_Duration__pb2.DESCRIPTOR,rst_dot_timing_dot_Frequency__pb2.DESCRIPTOR,])




_COMPONENTINFO = _descriptor.Descriptor(
  name='ComponentInfo',
  full_name='rst.cbse.ComponentInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='rst.cbse.ComponentInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lifecycle', full_name='rst.cbse.ComponentInfo.lifecycle', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inputs', full_name='rst.cbse.ComponentInfo.inputs', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='rst.cbse.ComponentInfo.outputs', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uptime', full_name='rst.cbse.ComponentInfo.uptime', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='freqency', full_name='rst.cbse.ComponentInfo.freqency', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=182,
  serialized_end=409,
)

_COMPONENTINFO.fields_by_name['lifecycle'].message_type = rst_dot_cbse_dot_ComponentState__pb2._COMPONENTSTATE
_COMPONENTINFO.fields_by_name['inputs'].message_type = rst_dot_cbse_dot_InputPort__pb2._INPUTPORT
_COMPONENTINFO.fields_by_name['outputs'].message_type = rst_dot_cbse_dot_OutputPort__pb2._OUTPUTPORT
_COMPONENTINFO.fields_by_name['uptime'].message_type = rst_dot_timing_dot_Duration__pb2._DURATION
_COMPONENTINFO.fields_by_name['freqency'].message_type = rst_dot_timing_dot_Frequency__pb2._FREQUENCY
DESCRIPTOR.message_types_by_name['ComponentInfo'] = _COMPONENTINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ComponentInfo = _reflection.GeneratedProtocolMessageType('ComponentInfo', (_message.Message,), dict(
  DESCRIPTOR = _COMPONENTINFO,
  __module__ = 'rst.cbse.ComponentInfo_pb2'
  # @@protoc_insertion_point(class_scope:rst.cbse.ComponentInfo)
  ))
_sym_db.RegisterMessage(ComponentInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\021ComponentInfoType'))
# @@protoc_insertion_point(module_scope)
