from dataclasses import field

import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
import github.com.metaprov.modelaapi.pkg.apis.infra.v1alpha1.generated_pb2 as infra_pb
import github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 as data_pb


from modela.infra.common import *
from modela.Configuration import *
from modela.common import ObjectReference


@datamodel(proto=catalog_pb.NotificationSpec)
class NotificationSetting(Configuration):
    ErrorTTL: int = 3600
    SuccessTTL: int = 3600
    NotifierName: str = ""
    # FIXME: Implement dict types: Selector: dict = field(default_factory=lambda: {})


@datamodel(proto=catalog_pb.ResourceSpec)
class Workload(Configuration):
    WorkloadName: str = ""
    CpuImage: ObjectReference = ObjectReference("modela-catalog", "modela-cpu-trainer-latest")
    GpuImage: ObjectReference = ObjectReference("modela-catalog", "modela-gpu-trainer-latest")


@datamodel(proto=catalog_pb.ContainerLog)
class ContainerLog(Configuration):
    Job: str = ""
    Container: str = ""
    Key: str = ""


@datamodel(proto=catalog_pb.Logs)
class OutputLogs(Configuration):
    BucketName: str = ""
    Containers: List[ContainerLog] = field(default_factory=lambda: [])


@datamodel(proto=data_pb.GitLocation)
class GitSettings(Configuration):
    GitConnectionName: str = ""
    Url: str = ""
    Branch: str = ""
    Private: bool = False


@datamodel(proto=data_pb.ImageLocation)
class ImageLocation(Configuration):
    Name: str = ""
    RegistryConnectionName: str = ""


@datamodel(proto=infra_pb.RuleSpec)
class Rule(Configuration):
    Resource: ResourceKind = None
    Verbs: List[Verb] = field(default_factory=lambda: [])


@datamodel(proto=infra_pb.UserRoleClassSpec)
class UserRoleClassSpec(Configuration):
    TenantRef: ObjectReference = None
    Description: str = ""
    Owner: str = ""
    Rules: List[Rule] = field(default_factory=lambda: [])
