from dataclasses import field
from typing import List

import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
import github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 as inference_pb
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1.grpcinferenceservice_pb2 import *

from modela.Configuration import datamodel
from modela.common import Configuration, ConditionStatus, Time, ObjectReference, StatusError, TriggerScheduleEventType
from modela.inference.common import PredictorConditionType, CanaryMetric, AccessType, PredictorType, \
    ModelDeploymentPhase
from modela.infra.models import Workload
from modela.training.common import TaskType
from modela.training.models import ModelValidation, ModelValidationResult


@datamodel(proto=catalog_pb.RunSchedule)
class RunSchedule(Configuration):
    Enabled: bool = False
    StartTime: Time = None
    EndTime: Time = None
    Cron: str = ""
    Type: TriggerScheduleEventType = None


@datamodel(proto=catalog_pb.ModelDeploymentStatus)
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


@datamodel(proto=inference_pb.ModelRecord)
class ModelRecord(Configuration):
    ModelName: str = ""
    ModelVersion: str = ""
    LiveAt: Time = None
    RetiredAt: Time = None
    AvgDailyPrediction: int = 0
    AvgLatency: float = 0


@datamodel(proto=catalog_pb.ModelDeploymentSpec)
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


@datamodel(proto=inference_pb.PredictorCondition)
class PredictorCondition(Configuration):
    Type: PredictorConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""


@datamodel(proto=inference_pb.ProgressiveSpec)
class ProgressiveSpec(Configuration):
    Warmup: int = 0
    TrafficIncrement: int = 0
    CanaryMetrics: List[CanaryMetric] = field(default_factory=lambda: [])


@datamodel(proto=inference_pb.PredictionCacheSpec)
class PredictionCacheSpec(Configuration):
    Active: bool = False
    ServiceName: str = ""


@datamodel(proto=inference_pb.AutoScaling)
class AutoScaling(Configuration):
    Enabled: bool = False
    MinReplicas: int = 1
    MaxReplicas: int = 1
    CpuAvgUtilization: int = 80
    MemAvgUtilization: int = 80


@datamodel(proto=inference_pb.PredictorHealth)
class PredictorHealth(Configuration):
    Service: bool = False
    DataDrift: bool = False
    ConceptDrift: bool = False
    TotalPredictions: int = 0
    Avg: int = 0
    TotalP95Requests: int = 0
    MedianResponseTime: int = 0
    LastDailyPredictions: List[int] = field(default_factory=lambda: [])


@datamodel(proto=inference_pb.PredictorStatus)
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


@datamodel(proto=inference_pb.MonitorSpec)
class MonitorSpec(Configuration):
    Enabled: bool = False
    SamplePercent: int = 0
    Schedule: RunSchedule = None
    NotifierName: str = ""
    Validations: List[ModelValidation] = field(default_factory=lambda: [])
    LogRequests: bool = False
    LogResponses: bool = False


@datamodel(proto=inference_pb.MonitorStatus)
class MonitorStatus(Configuration):
    LastPrediction: Time = None
    ValidationResults: List[ModelValidationResult] = field(default_factory=lambda: [])


@datamodel(proto=inference_pb.PredictorAuthSpec)
class PredictorAuthSpec(Configuration):
    Enabled: bool = False


AccessType_ = AccessType
AutoScaling_ = AutoScaling


@datamodel(proto=inference_pb.PredictorSpec)
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
    NodePort: int = 30000
    Path: str = ""
    AccessType: AccessType_ = None
    Replicas: int = 1
    AutoScaling: AutoScaling_ = None
    Owner: str = "no-one"
    Resources: Workload = Workload("general-nano")
    Cache: PredictionCacheSpec = None
    # Store: OnlineFeaturestoreSpec = None
    ForwardCurtain: str = ""
    BackwardCurtain: str = ""
    Type: PredictorType = PredictorType.Online
    Task: TaskType = None
    PredictionThreshold: float = 0
    Monitor: MonitorSpec = None
    Auth: PredictorAuthSpec = None


@datamodel(proto=ProbabilityValue)
class ProbabilityValue(Configuration):
    Label: str = ""
    Probability: float = 0


@datamodel(proto=ShapValue)
class ShapValue(Configuration):
    Feature: str = ""
    Value: float = 0


@datamodel(proto=PredictResultLineItem)
class PredictionResult(Configuration):
    Success: bool = False
    Score: float = 0
    Label: str = ""
    Probabilities: List[ProbabilityValue] = field(default_factory=lambda: [])
    ShapValues: List[ShapValue] = field(default_factory=lambda: [])
    MissingColumns: List[str] = field(default_factory=lambda: [])
    OutOfBound: List[str] = field(default_factory=lambda: [])
    BaseShapValue: float = 0



