import _collections_abc
import warnings
from types import GenericAlias
from typing import List, get_type_hints, get_args
import typing_utils
from google.protobuf.message import Message
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import ObjectMeta
from enum import Enum

from modela.ModelaException import ResourceNotFoundException
from modela.util import TrackedList


def isPrimitive(obj):
    return not hasattr(obj, '__dict__')


def convert_case(attr):
    return attr[0].lower() + attr[1:]


class Configuration:
    """
    Configuration is a base class for all dataclasses that represent Protobuf Messages for specification subclasses.
    They serve to provide Python developers with fully typed (and tracked) interactions with Modela API objects. This class
    provides methods for interacting with raw Protobuf Message types and automatically reading and propagating changes
    from a Python dataclass to a Message, and vice-versa.
    """

    def apply_field(self, attribute, value, message):
        """ Apply a single attribute to a related Protobuf Message """
        if not value:
            return
        real_field = convert_case(attribute)
        annotation_type = get_type_hints(self)[attribute]
        if typing_utils.issubtype(annotation_type, List):
            del getattr(message, real_field)[:]
            if isPrimitive(get_args(annotation_type)[0]()):
                getattr(message, real_field).extend(value)
            else:
                getattr(message, real_field).extend([model.to_message() for model in value])
                for ind, model in enumerate(value): # Fix _parent references, protobuf containers like to make copies of objects
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
                if isPrimitive(annotation_type()):
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
                    setattr(self, attribute, (type(annotation_type) if not callable(annotation_type) else annotation_type)(
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


class Resource:
    """
    Base class for all classes representing Modela custom resources
    """
    DefaultVersion = 'v0.0.1'

    def __init__(self, resource: Message, client=None, name="", namespace=""):
        self._object: Message = resource
        self._client = client
        if name != "" and namespace != "":
            if hasattr(self._client, "get"):
                try:
                    self._object = self._client.get(namespace, name).raw_message
                except ResourceNotFoundException:
                    self._object.metadata.CopyFrom(ObjectMeta())
                    self._object.metadata.name = name
                    self._object.metadata.namespace = namespace
                    self.default()
                    if hasattr(self._object.spec, 'versionName'):
                        self._object.spec.versionName = Resource.DefaultVersion

            else:
                print("Unable to lookup resource: object has no client repository")

    @property
    def spec(self):
        return self._object.spec

    @property
    def metadata(self) -> ObjectMeta:
        return self._object.metadata

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def namespace(self) -> str:
        return self.metadata.namespace

    def has_label(self, label: str) -> bool:
        return label in self.metadata.labels

    def set_label(self, label: str, value: str):
        self.metadata.labels[label] = value

    def label(self, label: str) -> str:
        return self.metadata.labels[label]

    @property
    def raw_message(self) -> Message:
        return self._object

    def submit(self, **kwargs):
        """
        Submit will create the resource on the cluster if it does not exist.
        """
        if hasattr(self._client, "create"):
            self._client.create(self, **kwargs)
        else:
            raise AttributeError("Object has no client repository")

    def update(self):
        if hasattr(self._client, "update"):
            self._client.update(self)
        else:
            raise AttributeError("Object has no client repository")

    def delete(self):
        if hasattr(self._client, "delete"):
            self._client.delete(self.namespace, self.name)
        else:
            raise AttributeError("Object has no client repository")

    def sync(self):
        if hasattr(self._client, "get"):
            self._object = self._client.get(self.namespace, self.name).raw_message
        else:
            raise AttributeError("Object has no client repository")

    def default(self):
        warnings.warn("default resource constructor is missing. resource may encounter errors.")