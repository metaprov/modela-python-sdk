from dataclasses import dataclass, field
from typing import List

from github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 import \
    PredictorCondition as MDPredictorCondition
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import \
    ModelDeploymentSpec as MDModelDeploymentSpec
from github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 import ModelRecord as MDModelRecord
from github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 import MonitorStatus as MDMonitorStatus
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import \
    ModelDeploymentStatus as MDModelDeploymentStatus
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import RunSchedule as MDRunSchedule
from modela import Configuration, ConditionStatus, Time, ObjectReference, StatusError, TriggerScheduleEventType
from modela.inference.common import PredictorConditionType, CanaryMetric, AccessType, PredictorType, \
    ModelDeploymentPhase
from modela.infra.models import Workload
from modela.training.common import TaskType
from modela.training.models import ModelValidation, ModelValidationResult


@dataclass
class RunSchedule(Configuration):
    Enabled: bool = False
    StartTime: Time = None
    EndTime: Time = None
    Cron: str = ""
    Type: TriggerScheduleEventType = None

    def to_message(self) -> MDRunSchedule:
        return self.set_parent(MDRunSchedule()).parent


@dataclass
class ModelDeploymentStatus(Configuration):
    ImageName: str = ""
    DeploymentRef: ObjectReference = None
    ServiceRef: ObjectReference = None
    HpaName: str = ""
    Current95: float = 0
    Current99: float = 0
    LastPredictionTime: Time = None
    DailyPredictionAvg: int = 0
    LastFailure: str = ""
    Phase: ModelDeploymentPhase = None
    DeployedAt: Time = None
    ReleasedAt: Time = None
    TrainingDatasetName: str = ""
    ApprovedBy: str = ""
    ApprovedAt: Time = None

    def to_message(self) -> MDModelDeploymentStatus:
        return self.set_parent(MDModelDeploymentStatus()).parent


@dataclass
class ModelRecord(Configuration):
    ModelName: str = ""
    ModelVersion: str = ""
    LiveAt: Time = None
    RetiredAt: Time = None
    AvgDailyPrediction: int = 0
    AvgLatency: float = 0

    def to_message(self) -> MDModelRecord:
        return self.set_parent(MDModelRecord()).parent


@dataclass
class ModelDeploymentSpec(Configuration):
    ModelName: str = ""
    ModelVersion: str = ""
    MaxTraffic: int = 0
    Traffic: int = 0
    Canary: bool = False
    Shadow: bool = False
    Released: bool = False
    Deployed: bool = False
    MountTar: bool = False
    TrafficSelector: str = ""
    CanaryMetrics: List[CanaryMetric] = field(default_factory=lambda: [])

    def to_message(self) -> MDModelDeploymentSpec:
        return self.set_parent(MDModelDeploymentSpec()).parent


@dataclass
class PredictorCondition(Configuration):
    Type: PredictorConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""

    def to_message(self) -> MDPredictorCondition:
        return self.set_parent(MDPredictorCondition()).parent


@dataclass
class ProgressiveSpec(Configuration):
    Warmup: int = 0
    TrafficIncrement: int = 0
    CanaryMetrics: List[CanaryMetric] = field(default_factory=lambda: [])


@dataclass
class PredictionCacheSpec(Configuration):
    Active: bool = False
    ServiceName: str = ""


@dataclass
class AutoScaling(Configuration):
    Enabled: bool = False
    MinReplicas: int = 1
    MaxReplicas: int = 1
    CpuAvgUtilization: int = 80
    MemAvgUtilization: int = 80


@dataclass
class PredictorHealth(Configuration):
    Service: bool = False
    DataDrift: bool = False
    ConceptDrift: bool = False
    TotalPredictions: int = 0
    Avg: int = 0
    TotalP95Requests: int = 0
    MedianResponseTime: int = 0
    LastDailyPredictions: List[int] = field(default_factory=lambda: [])


@dataclass
class PredictorStatus(Configuration):
    ModelStatus: List[ModelDeploymentStatus] = field(default_factory=lambda: [])
    MonitorLastAttemptAt: Time = None
    MonitorLastScore: float = 0
    MonitorLastLatency: float = 0
    Health: PredictorHealth = None
    ObservedGeneration: int = 0
    History: List[ModelRecord] = field(default_factory=lambda: [])
    MonitorStatus: MonitorStatus = None
    LastUpdated: Time = None
    TargetColumn: str = ""
    PositiveLabel: str = ""
    NegativeLabel: str = ""
    EndPoint: str = ""
    ProxyDeploymentRef: ObjectReference = None
    ProxyServiceRef: ObjectReference = None
    FailureReason: StatusError = None
    FailureMessage: str = ""
    Conditions: List[PredictorCondition] = field(default_factory=lambda: [])


@dataclass
class MonitorSpec(Configuration):
    Enabled: bool = False
    SamplePercent: int = 0
    Schedule: RunSchedule = None
    NotifierName: str = ""
    Validations: List[ModelValidation] = field(default_factory=lambda: [])
    LogRequests: bool = False
    LogResponses: bool = False


@dataclass
class MonitorStatus(Configuration):
    LastPrediction: Time = None
    ValidationResults: List[ModelValidationResult] = field(default_factory=lambda: [])

    def to_message(self) -> MDMonitorStatus:
        return self.set_parent(MDMonitorStatus()).parent


@dataclass
class PredictorAuthSpec(Configuration):
    Enabled: bool = False


PredictorAccessType = AccessType
PredictorAutoScaling = AutoScaling


@dataclass
class PredictorSpec(Configuration):
    VersionName: str = ""
    Description: str = ""
    ProductRef: ObjectReference = None
    ServingsiteRef: ObjectReference = ObjectReference("default-tenant", "default-lab")
    # Template: PodTemplate = None
    Models: List[ModelDeploymentSpec] = field(default_factory=lambda: [])
    Progressive: ProgressiveSpec = None
    ArtifactsFolder: str = ""
    Port: int = 8080
    Path: str = ""
    AccessType: PredictorAccessType = None
    Replicas: int = 1
    AutoScaling: PredictorAutoScaling = None
    Owner: str = "no-one"
    Resources: Workload = None
    Cache: PredictionCacheSpec = None
    # Store: OnlineFeaturestoreSpec = None
    ForewardCurtain: str = ""
    BackwardCurtain: str = ""
    Type: PredictorType = PredictorType.Online
    Task: TaskType = None
    PredictionThreshold: float = 0
    Monitor: MonitorSpec = None
    Auth: PredictorAuthSpec = None
