# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rst/cbse/OutputPort.proto

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
  name='rst/cbse/OutputPort.proto',
  package='rst.cbse',
  syntax='proto2',
  serialized_pb=_b('\n\x19rst/cbse/OutputPort.proto\x12\x08rst.cbse\"@\n\nOutputPort\x12\r\n\x05scope\x18\x01 \x02(\t\x12\x12\n\nbuffersize\x18\x02 \x01(\x04\x12\x0f\n\x07\x66illing\x18\x03 \x01(\x04\x42\x10\x42\x0eOutputPortType')
)




_OUTPUTPORT = _descriptor.Descriptor(
  name='OutputPort',
  full_name='rst.cbse.OutputPort',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scope', full_name='rst.cbse.OutputPort.scope', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buffersize', full_name='rst.cbse.OutputPort.buffersize', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='filling', full_name='rst.cbse.OutputPort.filling', index=2,
      number=3, type=4, cpp_type=4, label=1,
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
  serialized_start=39,
  serialized_end=103,
)

DESCRIPTOR.message_types_by_name['OutputPort'] = _OUTPUTPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OutputPort = _reflection.GeneratedProtocolMessageType('OutputPort', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUTPORT,
  __module__ = 'rst.cbse.OutputPort_pb2'
  # @@protoc_insertion_point(class_scope:rst.cbse.OutputPort)
  ))
_sym_db.RegisterMessage(OutputPort)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\016OutputPortType'))
# @@protoc_insertion_point(module_scope)
