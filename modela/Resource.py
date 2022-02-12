import _collections_abc
import warnings
from types import GenericAlias
from typing import List, get_type_hints, get_args
import typing_utils
from google.protobuf.message import Message
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import ObjectMeta
from modela.ModelaException import ResourceNotFoundException


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
        warnings.warn("default resource constructor is missing. resource may encounter errors on creation.")

    @staticmethod
    def set_default_version(version):
        Resource.DefaultVersion = version
