from dataclasses import field

from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import *
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import GitLocation, ImageLocation
from modela.Configuration import *
from modela.common import ObjectReference


@datamodel(proto=NotificationSpec)
class NotificationSetting(Configuration):
    ErrorTTL: int = 3600
    SuccessTTL: int = 3600
    NotifierName: str = ""
    # FIXME: Implement dict types: Selector: dict = field(default_factory=lambda: {})


@datamodel(proto=ResourceSpec)
class Workload(Configuration):
    WorkloadName: str = ""
    CpuImage: ObjectReference = ObjectReference("modela-catalog", "modela-cpu-trainer-latest")
    GpuImage: ObjectReference = ObjectReference("modela-catalog", "modela-gpu-trainer-latest")


@datamodel(proto=ContainerLog)
class ContainerLog(Configuration):
    Job: str = ""
    Container: str = ""
    Key: str = ""


@datamodel(proto=Logs)
class OutputLogs(Configuration):
    BucketName: str = ""
    Containers: List[ContainerLog] = field(default_factory=lambda: [])


@datamodel(proto=GitLocation)
class GitSettings(Configuration):
    GitConnectionName: str = ""
    Url: str = ""
    Branch: str = ""
    Private: bool = False


@datamodel(proto=ImageLocation)
class ImageLocation(Configuration):
    Name: str = ""
    RegistryConnectionName: str = ""
