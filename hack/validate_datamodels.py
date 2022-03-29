""" Script to check all datamodels against their respective Protobuf messages for inconsistencies """
import inspect
import sys
from modela import *
from modela.Configuration import convert_case

types = {
    "TYPE_DOUBLE": 1,
    "TYPE_FLOAT": 2,
    "TYPE_INT64": 3,
    "TYPE_UINT64": 4,
    "TYPE_INT32": 5,
    "TYPE_FIXED64": 6,
    "TYPE_FIXED32": 7,
    "TYPE_BOOL": 8,
    "TYPE_STRING": 9,
    "TYPE_GROUP": 10,
    "TYPE_MESSAGE": 11,
    "TYPE_BYTES": 12,
    "TYPE_UINT32": 13,
    "TYPE_ENUM": 14,
    "TYPE_SFIXED32": 15,
    "TYPE_SFIXED64": 16,
    "TYPE_SINT32": 17,
    "TYPE_SINT64": 18,
}
types = {v: k for k, v in types.items()}


def convert_proto_case(attr):
    return attr[0].upper() + attr[1:]


def validate_configuration(config):
    if hasattr(config, "proto_type"):
        found_errors = False
        fields = config.proto_type.DESCRIPTOR.fields_by_name.keys()
        cls_fields = config.__dict__["__annotations__"]
        for field in fields:
            if not convert_proto_case(field) in cls_fields:
                if not found_errors: print(config); found_errors = True
                print("Field not found: %s (type %s)" %
                      (convert_proto_case(field), types[config.proto_type.DESCRIPTOR.fields_by_name[field].type]))

        for field in cls_fields.keys():
            if not convert_case(field) in fields:
                if not found_errors: print(config); found_errors = True
                print("Nonexistent field found: %s" % field)

        if found_errors: print("")


def check_all():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if issubclass(obj, Configuration):
                validate_configuration(obj)

if __name__ == "__main__":
   check_all()