from dataclasses import dataclass, field
from modela.Configuration import *
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import ResourceSpec as MDResourceSpec
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import NotificationSpec as MDNotificationSpec
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import Logs as MDLogs
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import ContainerLog as MDContainerLog


@dataclass
class NotificationSetting(Configuration):
    OnError: bool = True
    ErrorTTL: int = 3600
    OnSuccess: bool = False
    SuccessTTL: int = 3600
    NotifierName: str = ""


@dataclass
class Workload(Configuration):
    WorkloadClassName: str = ""
    Enable: bool = False


@dataclass
class ContainerLog(Configuration):
    Job: str = ""
    Container: str = ""
    Key: str = ""

    def to_message(self) -> MDContainerLog:
        return self.set_parent(MDContainerLog()).parent

@dataclass
class OutputLogs(Configuration):
    BucketName: str = ""
    Containers: List[ContainerLog] = field(default_factory=lambda: [])

    def to_message(self) -> MDLogs:
        return self.set_parent(MDLogs()).parent


@dataclass
class GitSettings(Configuration):
    GitConnectionName: str = ""
    Url: str = ""
    Branch: str = ""
    Private: bool = False


@dataclass
class ImageLocation(Configuration):
    Name: str = ""
    RegistryConnectionName: str = ""
