from dataclasses import field
from typing import List
import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
import github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 as inference_pb
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1.grpcinferenceservice_pb2 import *
from modela.Configuration import datamodel
from modela.common import Configuration, ConditionStatus, Time, ObjectReference, StatusError, TriggerScheduleEventType,TestSuite
from modela.inference.common import PredictorConditionType, AccessType, PredictorType, ModelDeploymentPhase, ModelRole
from modela.infra.models import Workload
from modela.data.models import DataLocation
from modela.training.common import TaskType
from modela.training.models import ModelTest, ModelTestResult
from modela.common import Metric


@datamodel(proto=catalog_pb.RunSchedule)
class RunSchedule(Configuration):
    """ RunSchedule specifies the schedule for a Job to be executed """
    Enabled: bool = False
    """ Indicates if the schedule is enabled and the Jobs associated it will be created at the specified time """
    StartTime: Time = None
    """ The time of the day when the schedule will be executed """
    EndTime: Time = None
    """ The time of the day when the schedule is expected to conclude """
    Cron: str = ''
    """ The cron string of the schedule. See https://docs.oracle.com/cd/E12058_01/doc/doc.1014/e12030/cron_expressions.htm for more information """
    Type: TriggerScheduleEventType = None
    """ The type of schedule, which can be a frequency interval or a cron expression """


@datamodel(proto=inference_pb.ModelDeploymentStatus)
class ModelDeploymentStatus(Configuration):
    ImageName: str = ''
    ModelName: str = ''
    """ The name of the Model resource associated with the deployment """
    ModelVersion: str = ''
    """ The version of the Model resource """
    HpaRef: ObjectReference = None
    """ the name of the horizonal pod autoscaler, if autoscaling is true """
    DeploymentRef: ObjectReference = None
    """ The name of the Kubernetes Deployment that manages the pods of the Model """
    ServiceRef: ObjectReference = None
    """ The name of the Kubernetes Service which exposes the Model externally """
    P50: float = 0
    """ 50% latency (median) for predictions served by the model """
    P95: float = 0
    """ 95% latency for predictions served by the model """
    P99: float = 0
    """ 99% latency for predictions served by the model """
    LastPredictionTime: Time = None
    """ The last time a prediction was served by the Predictorlet """
    DailyPredictionAvg: int = 0
    LastFailure: str = ''
    """ LastFailure is the last failure that occured with the model """
    Phase: ModelDeploymentPhase = None
    """ Phase is the current phase of the model deployment """
    DeployedAt: Time = None
    """ DeployedAt is the last time that the model was deployed """
    ReleasedAt: Time = None
    """ ReleasedAt is the time that the model was released """
    DataDrift: bool = False
    """ Indicates if a data drift has been detected based on incoming prediction data """
    ConceptDrift: bool = False
    """ Indicates if a concept drift has been detected based on incoming prediction data """
    LastDailyPredictions: List[int] = field(default_factory=lambda : [])
    """ The predictions from the last 7 days """


@datamodel(proto=inference_pb.PredictorletStatus)
class PredictorletStatus(Configuration):
    """ PredictorletStatus describes the current state of a prediction proxy service associated with a Predictor """
    ImageName: str = ''
    """ The image name that the Predictorlet is currently running """
    DeploymentRef: ObjectReference = None
    """ The name of the Kubernetes Deployment that manages the pods of the Predictorlet """
    ServiceRef: ObjectReference = None
    """ The name of the Kubernetes Service which exposes the Predictorlet externally """
    P50: float = 0
    """ 50% latency (median) for predictions served by the Predictorlet """
    Current95: float = 0
    """ 95% latency for predictions served by the Predictorlet """
    Current99: float = 0
    """ 99% latency for predictions served by the Predictorlet """
    LastPredictionTime: Time = None
    """ The last time a prediction was served by the Predictorlet """
    DailyPredictionAvg: int = 0
    TotalPredictions: int = 0
    """ The total number of predictions served by the Predictorlet """
    LastFailure: str = ''
    """ LastFailure contains the last failure that occured with a model served by the Predictorlet """
    LastDailyPredictions: List[int] = field(default_factory=lambda : [])
    """ The predictions from the last 7 days """


@datamodel(proto=inference_pb.ModelRecord)
class ModelRecord(Configuration):
    """ ModelRecord hold the state of a model that was in production """
    ModelName: str = ''
    """ Model Name is the name of the model """
    ModelVersion: str = ''
    """ Model version is the version of the model """
    LiveAt: Time = None
    """ Live at is the time that the model were placed in production """
    RetiredAt: Time = None
    """ Retried at is the time that the model was retired from production. """
    AvgDailyPrediction: int = 0
    """ Retried at is the time that the model was retired from production. """
    AvgLatency: float = 0
    """ Retried at is the time that the model was retired from production. """


@datamodel(proto=catalog_pb.ModelDeploymentSpec)
class ModelDeploymentSpec(Configuration):
    """
    ModelDeploymentSpec describes how a single model should be deployed with a Predictor, and
    how prediction traffic will be routed to the model
    """
    ModelRef: ObjectReference = None
    """
    The reference to a Model resource which has been packaged and exists in the same Data Product
    as the Predictor which specifies the ModelDeploymentSpec
    """
    ModelVersion: str = ''
    """ The version of the model, derived from the Study which created it """
    Traffic: int = 0
    """ The minimum percentage (0 through 100) of traffic that will be served by the model """
    Role: ModelRole = ModelRole.Champion
    """ Role denotes the role of this model """
    Released: bool = False
    """ A released model is a model that should serve production traffic """
    Deployed: bool = False
    """ A deployed model is a model whose containers are up, but does not serve production traffic """
    MountTar: bool = False
    """ MountTar means that we would mount the model tar file. Else we would use baked image. """
    TrafficSelector: str = ''
    """ TrafficSelector is a filter on the traffic to this model """
    CanaryMetrics: List[Metric] = field(default_factory=lambda : [])
    """ If the deployment is canary, the metric define how to evaluate the canary """
    ApprovedBy: str = ''
    """ The account name of the approver """
    ApprovedAt: Time = None
    """ The time of approval """


@datamodel(proto=inference_pb.PredictorCondition)
class PredictorCondition(Configuration):
    """ PredictorCondition describes the state of a Predictor at a certain point """
    Type: PredictorConditionType = None
    """ Type of Predictor condition """
    Status: ConditionStatus = None
    """ Status of the condition, one of True, False, Unknown """
    LastTransitionTime: Time = None
    """ Last time the condition transitioned from one status to another """
    Reason: str = ''
    """ The reason for the condition's last transition """
    Message: str = ''
    """ A human-readable message indicating details about the transition """


@datamodel(proto=inference_pb.ProgressiveSpec)
class ProgressiveSpec(Configuration):
    """ ProgressiveSpec defines the specification to progressively deploy a model to production """
    Warmup: int = 0
    """ The time, in seconds, for the warm-up period """
    TrafficIncrement: int = 0
    """ The percentage of traffic to increment """
    CanaryMetrics: List[Metric] = field(default_factory=lambda : [])
    """ What metric to use when comparing the candidate model to the current model """


@datamodel(proto=inference_pb.PredictionCacheSpec)
class PredictionCacheSpec(Configuration):
    """
    ///////////////////////////////////////////////////
    Prediction Cache Spec
    ///////////////////////////////////////////////////
    PredictionCacheSpec specifies the connection information of a key-value cache to store predictions
    """
    Enabled: bool = False
    """ Enabled indicates if predictions will be cached """
    InMemory: bool = False
    """ InMemory indicates if predictions will be cached in the available memory of the Pod serving the model """
    Redis: bool = False
    """ Redis indicates if predictions will be cached in an external Redis deployment """
    Hostname: ObjectReference = None
    """ The reference to a Connection resource to an external Redis deployment """


@datamodel(proto=inference_pb.AutoScalingSpec)
class AutoScalingSpec(Configuration):
    """
    ///////////////////////////////////////////////////
    Auto Scaling Spec
    ///////////////////////////////////////////////////
    AutoScaling defines the configuration for the automatic scaling of a service
    """
    Enabled: bool = False
    """ Indicates if automatic scaling is enabled """
    MinReplicas: int = 1
    """ The minimum number of replicas running the service """
    MaxReplicas: int = 1
    """ The maximum number of replicas running the service """
    CpuAvgUtilization: int = 80
    """
    The target average CPU utilization across all replicas. The HorizontalPodAutoscaler associated with the
    service will change the number of replicas to maintain this metric
    """
    MemAvgUtilization: int = 80
    """
    The target average memory utilization across all replicas. The HorizontalPodAutoscaler associated with the
    service will change the number of replicas to maintain this metric
    """


@datamodel(proto=inference_pb.PredictorStatus)
class PredictorStatus(Configuration):
    """ PredictorStatus contain the current state of the Predictor resource """
    ObservedGeneration: int = 0
    """ ObservedGeneration is the last generation that was acted on """
    History: List[ModelRecord] = field(default_factory=lambda : [])
    """ The collection of historical records of models deployed to the Predictor, used internally to roll-back models """
    Models: List[ModelDeploymentStatus] = field(default_factory=lambda : [])
    """ The collection of statuses for each model deployed with the Predictor """
    Predictorlet: PredictorletStatus = None
    """
    The status of the Predictorlet associated with the Predictor. The Predictorlet is a service which handles prediction traffic
    and routes predictions to individual models based on the specification of the Predictor
    """
    LastUpdated: Time = None
    """ The last time the object was updated """
    EndPoint: str = ''
    """ The end-point URL of the Predictor """
    FailureReason: StatusError = None
    """ In the case of failure, the Predictor resource controller will set this field with a failure reason """
    FailureMessage: str = ''
    """ In the case of failure, the Predictor resource controller will set this field with a failure reason """
    Conditions: List[PredictorCondition] = field(default_factory=lambda : [])


@datamodel(proto=inference_pb.PredictorMonitorSpec)
class PredictorMonitorSpec(Configuration):
    """
    MonitorSpec defines the specification to monitor a model in production
    """
    Enabled: bool = False
    """
    Indicates if model monitoring is enabled for the model
    """
    Tests:TestSuite = TestSuite()
    """
    tests contains the collection of model tests that will be 
    performed based on incoming prediction traffic
    """
    Schedule: RunSchedule = None
    """ The schedule on which model monitoring computations will be performed """
    NotifierRef: ObjectReference = None
    """ NotifierRef references a Notifier resource that will be triggered in the case that a concept or data drift is detected """
    OutlierDetectionModelRef: ObjectReference = None
    """ Reference to a model that will be used for outlier detection. If empty, an outlier detection model. """


@datamodel(proto=inference_pb.PredictionLoggingSpec)
class PredictionLoggingSpec(Configuration):
    """ PredictionLoggingSpec specifies the configuration to log incoming and outgoing prediction requests """
    Enabled: bool = False
    """ Indicates if prediction logging is enabled """
    SamplePercent: int = 0
    """ The number percentage (0 through 100) of prediction requests to log """
    LogRequests: bool = True
    """ Indicates if incoming requests will be logged """
    LogResponses: bool = True
    """ Indicates if outgoing predictions will be logged """


@datamodel(proto=inference_pb.ModelServingSpec)
class ModelServingSpec(Configuration):
    """ ModelServingSpec specifies the configuration for models to be served by a Predictor """
    Type: PredictorType = PredictorType.Online
    """ The type of predictor (online, batch, or streaming). Online is the only supported type as of the current release """
    Serverless: bool = False
    """
    If Serverless is true, the Kubernetes Deployment which serves the model will not be created 
    until it starts to receive prediction traffic, and will be destroyed once the model becomes dormant
    """


@datamodel(proto=inference_pb.ForwardCurtainSpec)
class ForwardCurtainSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Enabled: bool = False
    """
    Is Forward curtain spec enabled
    """
    CurtainRef:ObjectReference = None
    """
    The forward curtain receives prediction requests before the prediction (currently unimplemented)
    """
    Percent: int = 0
    """
    Percent of request that are sent to the foreward curtain.
    """

@datamodel(proto=inference_pb.ForwardCurtainSpec)
class BackwardCurtainSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Enabled: bool = False
    """
    Is Forward curtain spec enabled
    """
    CurtainRef:ObjectReference = None
    """
    The forward curtain receives prediction requests before the prediction (currently unimplemented)
    """
    ConfidenceLow: float = 0.4
    """
    For backward curtain is the confidence low
    """
    ConfidenceHigh: float = 0.6
    """
    For backward curtain is the confidence high
    """

@datamodel(proto=inference_pb.OnlineFeatureStoreSpec)
class OnlineFeatureStoreSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Enabled: bool = False
    """
    Is online feature store enabled
    """
    HostName:str = ""
    """
    The forward curtain receives prediction requests before the prediction (currently unimplemented)
    """

@datamodel(proto=inference_pb.FastSlowModelSpec)
class FastSlowModelSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Enabled: bool = False
    """
    Is fast slow enabled
    """
    FastModelRef: ObjectReference = None
    """
    Reference to the fast model
    """
    SlowModelRef:ObjectReference = None
    """
    Reference to the slow model
    """
    ProbaLowPct:int = 40
    """
    The low range of confidence.
    """
    ProbaHighPct:int = 60
    """
    The high range of confidence , Must be higher than probalow
    """


AccessType_ = AccessType


@datamodel(proto=inference_pb.AccessSpec)
class AccessSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Port: int = 0
    """
    The port number that will be exposed on the Predictor's Pods to serve prediction traffic through the GRPCInferenceService API.
    The Kubernetes Service created by the Predictor will expose the port and forward GRPC traffic to the backend pods
    """
    NodePort: int = 0
    """
    The port number that will be exposed on the external address of every node on the cluster, in the case of the
    Predictor's access type being NodePort. Traffic from the port will be forwarded to the Predictor's backend service
    """
    Path: str = 0
    """
    The auto-generated DNS path where the Predictor service can be accessed. If the access type is ClusterIP, it will
    be a cluster-internal DNS name (i.e. predictor.default-serving-site.svc.cluster.local). In the case of the Ingress
    access type, it will be determined by the FQDN of the host ServingSite (i.e. predictor.default-serving-site.your-domain.ai).
    """
    AccessType: AccessType_ = AccessType_.ClusterIP
    """
    The Kubernetes-native access method which specifies how the Kubernetes Service created by the Predictor will be exposed.
    See https://modela.ai/docs/docs/serving/production/#access-method for a detailed description of each access type
    (defaults to cluster-ip)
    """
    Rest: bool = False
    """
    Indicates if the prediction service should expose an additional port to serve the GRPCInferenceService API through REST.
    The port one digit above the number specified by the Port field will be exposed to accept HTTP/1.1 traffic
    """
    ApikeySecretRef: ObjectReference = None
    """ ApiKeySecretRef references a Kubernetes Secret containing an API key that must be passed in prediction requests to the Predictor """


@datamodel(proto=inference_pb.PredictorSpec)
class PredictorSpec(Configuration):
    """ PredictorSpec defines the desired state of a Predictor """
    VersionName: str = ''
    """
    The name of the DataProductVersion which describes the version of the resource
    that exists in the same DataProduct namespace as the resource
    """
    Description: str = ''
    """ The user-provided description of the Predictor """
    ProductRef: ObjectReference = None
    """ The reference to the DataProduct that the resource exists under """
    ServingsiteRef: ObjectReference = ObjectReference('default-tenant', 'default-lab')
    """ The reference to the ServingSite resource that hosts the Predictor """
    Models: List[ModelDeploymentSpec] = field(default_factory=lambda : [])
    """
    The collection of model deployment specifications that define which Model resources will be deployed to the
    Predictor service and how they will be deployed. Each model should be trained with the same type of
    dataset and possess a unique version
    """
    Progressive: ProgressiveSpec = None
    """
    The specification to progressively deploy models. ModelDeploymentSpec specifications within Models that have the
    `Canary` field enabled will be progressively deployed according to the specification when they are applied to the Predictor
    """
    ArtifactsFolder: DataLocation = DataLocation()
    """ The data location where artifacts generated by the Predictor will be stored """
    Access: AccessSpec = AccessSpec()
    """ Access specifies the configuration for the Predictor service to be exposed externally """
    Serving: ModelServingSpec = ModelServingSpec()
    """ Serving specifies the configuration for individual models to handle prediction traffic """
    PredictionLogging: PredictionLoggingSpec = PredictionLoggingSpec()
    """ Monitor spec specify the monitor for this predictor. """
    Replicas: int = 1
    """
    The number of replicas for the Kubernetes Deployment associated with the Predictor, which will instantiate multiple
    copies of the service in the case that automatic scaling is disabled
    """
    AutoScaling: AutoScalingSpec = None
    """ AutoScaling specifies the auto-scaling policy """
    Owner: str = 'no-one'
    """ The name of the Account which created the object, which exists in the same tenant as the object """
    Resources: Workload = Workload('general-nano')
    """ Resources specifies the resource requirements allocated to the prediction service """
    Cache: PredictionCacheSpec = PredictionCacheSpec()
    """ Cache specifies the configuration of the prediction cache """
    Store: OnlineFeatureStoreSpec = OnlineFeatureStoreSpec()

    ForwardCurtain: ForwardCurtainSpec = ForwardCurtainSpec()

    BackwardCurtain: BackwardCurtainSpec = BackwardCurtainSpec()

    Task: TaskType = None
    """ The task type of the Predictor, which should match the task type of the models being served """
    PredictionThreshold: float = 0
    """ The prediction threshold """
    Monitor: PredictorMonitorSpec = None
    """ Monitor spec specify the monitor for this predictor. """
    FastSlow: FastSlowModelSpec = FastSlowModelSpec()


@datamodel(proto=ProbabilityValue)
class ProbabilityValue(Configuration):
    Label: str = ''
    Probability: float = 0


@datamodel(proto=ShapValue)
class ShapValue(Configuration):
    Feature: str = ''
    Value: float = 0


@datamodel(proto=PredictResultLineItem)
class PredictionResult(Configuration):
    Success: bool = False
    Score: float = 0
    Label: str = ''
    Probabilities: List[ProbabilityValue] = field(default_factory=lambda : [])
    ShapValues: List[ShapValue] = field(default_factory=lambda : [])
    MissingColumns: List[str] = field(default_factory=lambda : [])
    OutOfBound: List[str] = field(default_factory=lambda : [])
    BaseShapValue: float = 0




@datamodel(proto=inference_pb.BackwardCurtainSpec)
class BackwardCurtainSpec(Configuration):
    """ AccessSpec specifies the configuration to expose a Predictor service externally """
    Port: int = 0
    """
    The port number that will be exposed on the Predictor's Pods to serve prediction traffic through the GRPCInferenceService API.
    The Kubernetes Service created by the Predictor will expose the port and forward GRPC traffic to the backend pods
    """
    NodePort: int = 0
    """
    The port number that will be exposed on the external address of every node on the cluster, in the case of the
    Predictor's access type being NodePort. Traffic from the port will be forwarded to the Predictor's backend service
    """
    Path: str = 0
    """
    The auto-generated DNS path where the Predictor service can be accessed. If the access type is ClusterIP, it will
    be a cluster-internal DNS name (i.e. predictor.default-serving-site.svc.cluster.local). In the case of the Ingress
    access type, it will be determined by the FQDN of the host ServingSite (i.e. predictor.default-serving-site.your-domain.ai).
    """
    AccessType: AccessType_ = AccessType_.ClusterIP
    """
    The Kubernetes-native access method which specifies how the Kubernetes Service created by the Predictor will be exposed.
    See https://modela.ai/docs/docs/serving/production/#access-method for a detailed description of each access type
    (defaults to cluster-ip)
    """
    Rest: bool = False
    """
    Indicates if the prediction service should expose an additional port to serve the GRPCInferenceService API through REST.
    The port one digit above the number specified by the Port field will be exposed to accept HTTP/1.1 traffic
    """
    ApikeySecretRef: ObjectReference = None
    """ ApiKeySecretRef references a Kubernetes Secret containing an API key that must be passed in prediction requests to the Predictor """
