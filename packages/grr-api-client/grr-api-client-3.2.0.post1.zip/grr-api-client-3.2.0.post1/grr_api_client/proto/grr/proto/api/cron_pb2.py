# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr/proto/api/cron.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from grr.proto import flows_pb2 as grr_dot_proto_dot_flows__pb2
from grr.proto import semantic_pb2 as grr_dot_proto_dot_semantic__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr/proto/api/cron.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x18grr/proto/api/cron.proto\x1a\x19google/protobuf/any.proto\x1a\x15grr/proto/flows.proto\x1a\x18grr/proto/semantic.proto\"\xe8\x07\n\nApiCronJob\x12*\n\x03urn\x18\x01 \x01(\tB\x1d\xe2\xfc\xe3\xc4\x01\x17\n\x06RDFURN\x12\rCron job URN.\x12\x32\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x1d\xe2\xfc\xe3\xc4\x01\x17\x12\x15\x43ron job description.\x12*\n\tflow_name\x18\x03 \x01(\tB\x17\xe2\xfc\xe3\xc4\x01\x11\x12\x0f\x43ron flow name.\x12S\n\tflow_args\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyB*\xe2\xfc\xe3\xc4\x01$\x12\x14\x43ron flow arguments.*\x0cGetArgsClass\x12I\n\x10\x66low_runner_args\x18\x05 \x01(\x0b\x32\x0f.FlowRunnerArgsB\x1e\xe2\xfc\xe3\xc4\x01\x18\x12\x16\x46low runner arguments.\x12\x42\n\x0bperiodicity\x18\x06 \x01(\x04\x42-\xe2\xfc\xe3\xc4\x01\'\n\x08\x44uration\x12\x1bInterval between cron runs.\x12\x9a\x02\n\x08lifetime\x18\x07 \x01(\x04\x42\x87\x02\xe2\xfc\xe3\xc4\x01\x80\x02\n\x08\x44uration\x12\xf3\x01How long each run of the cron should be allowed to run. Runs that exceed lifetime will be killed. This is complimentary but different to periodicity e.g. it allows us to run jobs weekly that should be killed if they take more than a few hours.\x12Y\n\x0e\x61llow_overruns\x18\x08 \x01(\x08\x42\x41\xe2\xfc\xe3\xc4\x01;\x12\x37If true, don\'t kill the previous run if new one starts.\x18\x01\x12=\n\x05state\x18\t \x01(\x0e\x32\x11.ApiCronJob.StateB\x1b\xe2\xfc\xe3\xc4\x01\x15\x12\x13\x43urrent flow state.\x12M\n\rlast_run_time\x18\n \x01(\x04\x42\x36\xe2\xfc\xe3\xc4\x01\x30\n\x0bRDFDatetime\x12!Last time when this cron job ran.\x12@\n\nis_failing\x18\x0b \x01(\x08\x42,\xe2\xfc\xe3\xc4\x01&\x12$Is this cron job constantly failing?\"\"\n\x05State\x12\x0b\n\x07\x45NABLED\x10\x00\x12\x0c\n\x08\x44ISABLED\x10\x01\"y\n\x13\x41piListCronJobsArgs\x12(\n\x06offset\x18\x01 \x01(\x03\x42\x18\xe2\xfc\xe3\xc4\x01\x12\x12\x10Starting offset.\x12\x38\n\x05\x63ount\x18\x02 \x01(\x03\x42)\xe2\xfc\xe3\xc4\x01#\x12!Max number of cron jobs to fetch.\"{\n\x15\x41piListCronJobsResult\x12.\n\x05items\x18\x01 \x03(\x0b\x32\x0b.ApiCronJobB\x12\xe2\xfc\xe3\xc4\x01\x0c\x12\nCron jobs.\x12\x32\n\x0btotal_count\x18\x02 \x01(\x03\x42\x1d\xe2\xfc\xe3\xc4\x01\x17\x12\x15Total count of items.\">\n\x11\x41piGetCronJobArgs\x12)\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x14\xe2\xfc\xe3\xc4\x01\x0e\x12\x0c\x43ron job id.\"C\n\x16\x41piForceRunCronJobArgs\x12)\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x14\xe2\xfc\xe3\xc4\x01\x0e\x12\x0c\x43ron job id.\"\x86\x01\n\x14\x41piModifyCronJobArgs\x12)\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x14\xe2\xfc\xe3\xc4\x01\x0e\x12\x0c\x43ron job id.\x12\x43\n\x05state\x18\x02 \x01(\x0e\x32\x11.ApiCronJob.StateB!\xe2\xfc\xe3\xc4\x01\x1b\x12\x19New cron job state value.\"\xa4\x01\n\x17\x41piListCronJobFlowsArgs\x12)\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x14\xe2\xfc\xe3\xc4\x01\x0e\x12\x0c\x43ron job id.\x12(\n\x06offset\x18\x02 \x01(\x03\x42\x18\xe2\xfc\xe3\xc4\x01\x12\x12\x10Starting offset.\x12\x34\n\x05\x63ount\x18\x03 \x01(\x03\x42%\xe2\xfc\xe3\xc4\x01\x1f\x12\x1dMax number of flows to fetch.\"p\n\x15\x41piGetCronJobFlowArgs\x12)\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x14\xe2\xfc\xe3\xc4\x01\x0e\x12\x0c\x43ron job id.\x12,\n\x07\x66low_id\x18\x02 \x01(\tB\x1b\xe2\xfc\xe3\xc4\x01\x15\n\tApiFlowId\x12\x08\x46low id.\"L\n\x14\x41piDeleteCronJobArgs\x12\x34\n\x0b\x63ron_job_id\x18\x01 \x01(\tB\x1f\xe2\xfc\xe3\xc4\x01\x19\x12\x17The id of the cron job.')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,grr_dot_proto_dot_flows__pb2.DESCRIPTOR,grr_dot_proto_dot_semantic__pb2.DESCRIPTOR,])



_APICRONJOB_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='ApiCronJob.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ENABLED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1071,
  serialized_end=1105,
)
_sym_db.RegisterEnumDescriptor(_APICRONJOB_STATE)


_APICRONJOB = _descriptor.Descriptor(
  name='ApiCronJob',
  full_name='ApiCronJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='urn', full_name='ApiCronJob.urn', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\n\006RDFURN\022\rCron job URN.'))),
    _descriptor.FieldDescriptor(
      name='description', full_name='ApiCronJob.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\022\025Cron job description.'))),
    _descriptor.FieldDescriptor(
      name='flow_name', full_name='ApiCronJob.flow_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\021\022\017Cron flow name.'))),
    _descriptor.FieldDescriptor(
      name='flow_args', full_name='ApiCronJob.flow_args', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001$\022\024Cron flow arguments.*\014GetArgsClass'))),
    _descriptor.FieldDescriptor(
      name='flow_runner_args', full_name='ApiCronJob.flow_runner_args', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\030\022\026Flow runner arguments.'))),
    _descriptor.FieldDescriptor(
      name='periodicity', full_name='ApiCronJob.periodicity', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\'\n\010Duration\022\033Interval between cron runs.'))),
    _descriptor.FieldDescriptor(
      name='lifetime', full_name='ApiCronJob.lifetime', index=6,
      number=7, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\200\002\n\010Duration\022\363\001How long each run of the cron should be allowed to run. Runs that exceed lifetime will be killed. This is complimentary but different to periodicity e.g. it allows us to run jobs weekly that should be killed if they take more than a few hours.'))),
    _descriptor.FieldDescriptor(
      name='allow_overruns', full_name='ApiCronJob.allow_overruns', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001;\0227If true, don\'t kill the previous run if new one starts.\030\001'))),
    _descriptor.FieldDescriptor(
      name='state', full_name='ApiCronJob.state', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\025\022\023Current flow state.'))),
    _descriptor.FieldDescriptor(
      name='last_run_time', full_name='ApiCronJob.last_run_time', index=9,
      number=10, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\0010\n\013RDFDatetime\022!Last time when this cron job ran.'))),
    _descriptor.FieldDescriptor(
      name='is_failing', full_name='ApiCronJob.is_failing', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001&\022$Is this cron job constantly failing?'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _APICRONJOB_STATE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=105,
  serialized_end=1105,
)


_APILISTCRONJOBSARGS = _descriptor.Descriptor(
  name='ApiListCronJobsArgs',
  full_name='ApiListCronJobsArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='offset', full_name='ApiListCronJobsArgs.offset', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\022\022\020Starting offset.'))),
    _descriptor.FieldDescriptor(
      name='count', full_name='ApiListCronJobsArgs.count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001#\022!Max number of cron jobs to fetch.'))),
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
  serialized_start=1107,
  serialized_end=1228,
)


_APILISTCRONJOBSRESULT = _descriptor.Descriptor(
  name='ApiListCronJobsResult',
  full_name='ApiListCronJobsResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='ApiListCronJobsResult.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\014\022\nCron jobs.'))),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='ApiListCronJobsResult.total_count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\022\025Total count of items.'))),
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
  serialized_start=1230,
  serialized_end=1353,
)


_APIGETCRONJOBARGS = _descriptor.Descriptor(
  name='ApiGetCronJobArgs',
  full_name='ApiGetCronJobArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiGetCronJobArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))),
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
  serialized_start=1355,
  serialized_end=1417,
)


_APIFORCERUNCRONJOBARGS = _descriptor.Descriptor(
  name='ApiForceRunCronJobArgs',
  full_name='ApiForceRunCronJobArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiForceRunCronJobArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))),
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
  serialized_start=1419,
  serialized_end=1486,
)


_APIMODIFYCRONJOBARGS = _descriptor.Descriptor(
  name='ApiModifyCronJobArgs',
  full_name='ApiModifyCronJobArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiModifyCronJobArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))),
    _descriptor.FieldDescriptor(
      name='state', full_name='ApiModifyCronJobArgs.state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\033\022\031New cron job state value.'))),
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
  serialized_start=1489,
  serialized_end=1623,
)


_APILISTCRONJOBFLOWSARGS = _descriptor.Descriptor(
  name='ApiListCronJobFlowsArgs',
  full_name='ApiListCronJobFlowsArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiListCronJobFlowsArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))),
    _descriptor.FieldDescriptor(
      name='offset', full_name='ApiListCronJobFlowsArgs.offset', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\022\022\020Starting offset.'))),
    _descriptor.FieldDescriptor(
      name='count', full_name='ApiListCronJobFlowsArgs.count', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\037\022\035Max number of flows to fetch.'))),
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
  serialized_start=1626,
  serialized_end=1790,
)


_APIGETCRONJOBFLOWARGS = _descriptor.Descriptor(
  name='ApiGetCronJobFlowArgs',
  full_name='ApiGetCronJobFlowArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiGetCronJobFlowArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))),
    _descriptor.FieldDescriptor(
      name='flow_id', full_name='ApiGetCronJobFlowArgs.flow_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\025\n\tApiFlowId\022\010Flow id.'))),
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
  serialized_start=1792,
  serialized_end=1904,
)


_APIDELETECRONJOBARGS = _descriptor.Descriptor(
  name='ApiDeleteCronJobArgs',
  full_name='ApiDeleteCronJobArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cron_job_id', full_name='ApiDeleteCronJobArgs.cron_job_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\031\022\027The id of the cron job.'))),
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
  serialized_start=1906,
  serialized_end=1982,
)

_APICRONJOB.fields_by_name['flow_args'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_APICRONJOB.fields_by_name['flow_runner_args'].message_type = grr_dot_proto_dot_flows__pb2._FLOWRUNNERARGS
_APICRONJOB.fields_by_name['state'].enum_type = _APICRONJOB_STATE
_APICRONJOB_STATE.containing_type = _APICRONJOB
_APILISTCRONJOBSRESULT.fields_by_name['items'].message_type = _APICRONJOB
_APIMODIFYCRONJOBARGS.fields_by_name['state'].enum_type = _APICRONJOB_STATE
DESCRIPTOR.message_types_by_name['ApiCronJob'] = _APICRONJOB
DESCRIPTOR.message_types_by_name['ApiListCronJobsArgs'] = _APILISTCRONJOBSARGS
DESCRIPTOR.message_types_by_name['ApiListCronJobsResult'] = _APILISTCRONJOBSRESULT
DESCRIPTOR.message_types_by_name['ApiGetCronJobArgs'] = _APIGETCRONJOBARGS
DESCRIPTOR.message_types_by_name['ApiForceRunCronJobArgs'] = _APIFORCERUNCRONJOBARGS
DESCRIPTOR.message_types_by_name['ApiModifyCronJobArgs'] = _APIMODIFYCRONJOBARGS
DESCRIPTOR.message_types_by_name['ApiListCronJobFlowsArgs'] = _APILISTCRONJOBFLOWSARGS
DESCRIPTOR.message_types_by_name['ApiGetCronJobFlowArgs'] = _APIGETCRONJOBFLOWARGS
DESCRIPTOR.message_types_by_name['ApiDeleteCronJobArgs'] = _APIDELETECRONJOBARGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ApiCronJob = _reflection.GeneratedProtocolMessageType('ApiCronJob', (_message.Message,), dict(
  DESCRIPTOR = _APICRONJOB,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiCronJob)
  ))
_sym_db.RegisterMessage(ApiCronJob)

ApiListCronJobsArgs = _reflection.GeneratedProtocolMessageType('ApiListCronJobsArgs', (_message.Message,), dict(
  DESCRIPTOR = _APILISTCRONJOBSARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiListCronJobsArgs)
  ))
_sym_db.RegisterMessage(ApiListCronJobsArgs)

ApiListCronJobsResult = _reflection.GeneratedProtocolMessageType('ApiListCronJobsResult', (_message.Message,), dict(
  DESCRIPTOR = _APILISTCRONJOBSRESULT,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiListCronJobsResult)
  ))
_sym_db.RegisterMessage(ApiListCronJobsResult)

ApiGetCronJobArgs = _reflection.GeneratedProtocolMessageType('ApiGetCronJobArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIGETCRONJOBARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiGetCronJobArgs)
  ))
_sym_db.RegisterMessage(ApiGetCronJobArgs)

ApiForceRunCronJobArgs = _reflection.GeneratedProtocolMessageType('ApiForceRunCronJobArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIFORCERUNCRONJOBARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiForceRunCronJobArgs)
  ))
_sym_db.RegisterMessage(ApiForceRunCronJobArgs)

ApiModifyCronJobArgs = _reflection.GeneratedProtocolMessageType('ApiModifyCronJobArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIMODIFYCRONJOBARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiModifyCronJobArgs)
  ))
_sym_db.RegisterMessage(ApiModifyCronJobArgs)

ApiListCronJobFlowsArgs = _reflection.GeneratedProtocolMessageType('ApiListCronJobFlowsArgs', (_message.Message,), dict(
  DESCRIPTOR = _APILISTCRONJOBFLOWSARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiListCronJobFlowsArgs)
  ))
_sym_db.RegisterMessage(ApiListCronJobFlowsArgs)

ApiGetCronJobFlowArgs = _reflection.GeneratedProtocolMessageType('ApiGetCronJobFlowArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIGETCRONJOBFLOWARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiGetCronJobFlowArgs)
  ))
_sym_db.RegisterMessage(ApiGetCronJobFlowArgs)

ApiDeleteCronJobArgs = _reflection.GeneratedProtocolMessageType('ApiDeleteCronJobArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIDELETECRONJOBARGS,
  __module__ = 'grr.proto.api.cron_pb2'
  # @@protoc_insertion_point(class_scope:ApiDeleteCronJobArgs)
  ))
_sym_db.RegisterMessage(ApiDeleteCronJobArgs)


_APICRONJOB.fields_by_name['urn'].has_options = True
_APICRONJOB.fields_by_name['urn']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\n\006RDFURN\022\rCron job URN.'))
_APICRONJOB.fields_by_name['description'].has_options = True
_APICRONJOB.fields_by_name['description']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\022\025Cron job description.'))
_APICRONJOB.fields_by_name['flow_name'].has_options = True
_APICRONJOB.fields_by_name['flow_name']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\021\022\017Cron flow name.'))
_APICRONJOB.fields_by_name['flow_args'].has_options = True
_APICRONJOB.fields_by_name['flow_args']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001$\022\024Cron flow arguments.*\014GetArgsClass'))
_APICRONJOB.fields_by_name['flow_runner_args'].has_options = True
_APICRONJOB.fields_by_name['flow_runner_args']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\030\022\026Flow runner arguments.'))
_APICRONJOB.fields_by_name['periodicity'].has_options = True
_APICRONJOB.fields_by_name['periodicity']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\'\n\010Duration\022\033Interval between cron runs.'))
_APICRONJOB.fields_by_name['lifetime'].has_options = True
_APICRONJOB.fields_by_name['lifetime']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\200\002\n\010Duration\022\363\001How long each run of the cron should be allowed to run. Runs that exceed lifetime will be killed. This is complimentary but different to periodicity e.g. it allows us to run jobs weekly that should be killed if they take more than a few hours.'))
_APICRONJOB.fields_by_name['allow_overruns'].has_options = True
_APICRONJOB.fields_by_name['allow_overruns']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001;\0227If true, don\'t kill the previous run if new one starts.\030\001'))
_APICRONJOB.fields_by_name['state'].has_options = True
_APICRONJOB.fields_by_name['state']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\025\022\023Current flow state.'))
_APICRONJOB.fields_by_name['last_run_time'].has_options = True
_APICRONJOB.fields_by_name['last_run_time']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\0010\n\013RDFDatetime\022!Last time when this cron job ran.'))
_APICRONJOB.fields_by_name['is_failing'].has_options = True
_APICRONJOB.fields_by_name['is_failing']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001&\022$Is this cron job constantly failing?'))
_APILISTCRONJOBSARGS.fields_by_name['offset'].has_options = True
_APILISTCRONJOBSARGS.fields_by_name['offset']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\022\022\020Starting offset.'))
_APILISTCRONJOBSARGS.fields_by_name['count'].has_options = True
_APILISTCRONJOBSARGS.fields_by_name['count']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001#\022!Max number of cron jobs to fetch.'))
_APILISTCRONJOBSRESULT.fields_by_name['items'].has_options = True
_APILISTCRONJOBSRESULT.fields_by_name['items']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\014\022\nCron jobs.'))
_APILISTCRONJOBSRESULT.fields_by_name['total_count'].has_options = True
_APILISTCRONJOBSRESULT.fields_by_name['total_count']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\027\022\025Total count of items.'))
_APIGETCRONJOBARGS.fields_by_name['cron_job_id'].has_options = True
_APIGETCRONJOBARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))
_APIFORCERUNCRONJOBARGS.fields_by_name['cron_job_id'].has_options = True
_APIFORCERUNCRONJOBARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))
_APIMODIFYCRONJOBARGS.fields_by_name['cron_job_id'].has_options = True
_APIMODIFYCRONJOBARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))
_APIMODIFYCRONJOBARGS.fields_by_name['state'].has_options = True
_APIMODIFYCRONJOBARGS.fields_by_name['state']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\033\022\031New cron job state value.'))
_APILISTCRONJOBFLOWSARGS.fields_by_name['cron_job_id'].has_options = True
_APILISTCRONJOBFLOWSARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))
_APILISTCRONJOBFLOWSARGS.fields_by_name['offset'].has_options = True
_APILISTCRONJOBFLOWSARGS.fields_by_name['offset']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\022\022\020Starting offset.'))
_APILISTCRONJOBFLOWSARGS.fields_by_name['count'].has_options = True
_APILISTCRONJOBFLOWSARGS.fields_by_name['count']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\037\022\035Max number of flows to fetch.'))
_APIGETCRONJOBFLOWARGS.fields_by_name['cron_job_id'].has_options = True
_APIGETCRONJOBFLOWARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\016\022\014Cron job id.'))
_APIGETCRONJOBFLOWARGS.fields_by_name['flow_id'].has_options = True
_APIGETCRONJOBFLOWARGS.fields_by_name['flow_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\025\n\tApiFlowId\022\010Flow id.'))
_APIDELETECRONJOBARGS.fields_by_name['cron_job_id'].has_options = True
_APIDELETECRONJOBARGS.fields_by_name['cron_job_id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\342\374\343\304\001\031\022\027The id of the cron job.'))
# @@protoc_insertion_point(module_scope)
