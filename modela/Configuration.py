from abc import ABCMeta, ABC
from typing import List, get_type_hints, get_args
import typing_utils
from google.protobuf.message import Message
from enum import Enum
from modela.util import TrackedList


def isPrimitive(obj):
    return not hasattr(obj, '__dict__')


def convert_case(attr):
    return attr[0].lower() + attr[1:]


class Configuration(object):
    """
    Configuration is a base class for all dataclasses that represent Protobuf Messages for specification subclasses.
    They serve to provide Python developers with fully typed (and tracked) interactions with Modela API objects. This class
    provides methods for interacting with raw Protobuf Message types and automatically reading and propagating changes
    from a Python dataclass to a Message, and vice-versa.
    """

    def __post_init__(self):  # Apply tracking to all list attributes post-initialization
        for attribute, value in self.__dict__.items():
            annotation_type = get_type_hints(self)[attribute]
            if typing_utils.issubtype(annotation_type, List):
                setattr(self, attribute, TrackedList(value, self, attribute))

    def apply_field(self, attribute, value, message):
        """ Apply a single attribute to a related Protobuf Message """
        if value is None:
            return
        real_field = convert_case(attribute)
        annotation_type = get_type_hints(self)[attribute]
        if typing_utils.issubtype(annotation_type, List):
            del getattr(message, real_field)[:]
            if issubclass(get_args(annotation_type)[0], Enum) or isPrimitive(get_args(annotation_type)[0]()):
                getattr(message, real_field).extend(value)
            else:
                getattr(message, real_field).extend([model.to_message() for model in value])
                for ind, model in enumerate(
                        value):  # Fix _parent references, protobuf containers like to make copies of objects
                    model._parent = getattr(message, real_field)[ind]

        elif isinstance(getattr(message, real_field), Message):
            value.set_parent(getattr(message, real_field))
        else:
            setattr(message, real_field, value.value if isinstance(value, Enum) else (value or annotation_type()))

    def apply_config(self, message):
        """ Apply all attributes of a class to a Protobuf Message """
        for attribute, value in self.__dict__.items():
            if attribute == "_parent":
                continue
            self.apply_field(attribute, value, message)

        return message

    def copy_from(self, message):
        """ Copy the contents of a Protobuf Message to a related dataclass """
        for attribute, value in self.__dict__.items():
            if attribute == "_parent":
                continue
            annotation_type = get_type_hints(self)[attribute]
            message_attr = getattr(message, convert_case(attribute))
            if typing_utils.issubtype(annotation_type, List):
                annotation_type = get_args(annotation_type)[0]
                if issubclass(annotation_type, Enum) or isPrimitive(annotation_type()):
                    setattr(self, attribute, TrackedList([annotation_type(message) for message in message_attr],
                                                         self, attribute))
                else:
                    setattr(self, attribute, TrackedList(
                        [annotation_type().copy_from(message).set_parent(message) for message in message_attr],
                        self, attribute))
            elif isinstance(message_attr, Message):
                if message_attr.ByteSize() <= 0:
                    continue
                setattr(self, attribute, annotation_type().copy_from(message_attr))
            else:
                try:
                    setattr(self, attribute,
                            (type(annotation_type) if not callable(annotation_type) else annotation_type)(
                                message_attr))
                except ValueError:
                    pass

        self._parent = message
        return self

    def set_parent(self, model):
        self._parent = model
        self.apply_config(model)
        return self

    def propagate_to_parent(self, attribute, value):
        if hasattr(self, "_parent"):
            self.apply_field(attribute, value, self._parent)

    def to_message(self):
        raise NotImplementedError()

    @property
    def parent(self):
        return self._parent

    def __setattr__(self, attribute, value):
        if hasattr(self, "_parent") and attribute != "_parent":
            self.apply_field(attribute, value, self._parent)

        if type(value) == list:
            value = TrackedList(value, self, attribute)

        super().__setattr__(attribute, value)


class ImmutableConfiguration(Configuration):
    def apply_field(self, attribute, value, message):
        raise TypeError("This configuration is immutable.")

    def apply_config(self, message):
        raise TypeError("This configuration is immutable.")

    def set_parent(self, model):
        raise TypeError("This configuration is immutable.")

    def __setattr__(self, attribute, value):
        object.__setattr__(attribute, value)
