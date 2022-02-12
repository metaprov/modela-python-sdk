from dataclasses import dataclass, field
from modela.Configuration import *
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import ResourceSpec as MDResourceSpec
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import NotificationSpec as MDNotificationSpec
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import Logs as MDLogs


@dataclass
class NotificationSetting(Configuration):
    OnError: bool = True
    ErrorTTL: int = 3600
    OnSuccess: bool = False
    SuccessTTL: int = 3600
    NotifierName: str = ""

    def to_message(self) -> MDNotificationSpec:
        return self.set_parent(MDNotificationSpec()).parent


@dataclass
class Workload(Configuration):
    WorkloadClassName: str = ""
    Enable: bool = False

    def to_message(self) -> MDResourceSpec:
        return self.set_parent(MDResourceSpec()).parent


@dataclass
class OutputLogs(Configuration):
    BucketName: str = ""
    Paths: List[str] = field(default_factory=lambda: [])

    def to_message(self) -> MDLogs:
        return self.set_parent(MDLogs()).parent

    def __post_init__(self):
        self.Paths = TrackedList(self.Paths, self, "Paths")


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
