from dataclasses import field
from typing import List
import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
import github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 as inference_pb
import github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 as data_pb
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1.grpcinferenceservice_pb2 import *
from modela.Configuration import datamodel
from modela.common import Configuration, ConditionStatus, Time, ObjectReference, StatusError, TriggerScheduleEventType, TestSuite, TestSuiteResult, Measurement
from modela.inference.common import *
from modela.infra.models import Workload
from modela.data.models import DataLocation
from modela.training.common import TaskType
from modela.common import Metric


@datamodel(proto=inference_pb.KubernetesObjectStatus)
class KubernetesObjectStatus(Configuration):
    """ KubernetesObjectStatus describes the location and status of a Kubernetes-native resource """
    Ref: ObjectReference = None
    """ The object reference """
    Status: K8sObjectStatusState = K8sObjectStatusState.Unknown
    """ The status of the object """


ValidationMetric = Metric


@datamodel(proto=inference_pb.ValidationError)
class ValidationError(Configuration):
    Column: str = ''
    Metric: ValidationMetric = None
    """ The metric from the rule """
    Min: float = 0
    """ Expected min """
    Max: float = 0
    """ Expected max """
    Actual: float = 0
    """ Actual value """


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
    ObjectStatuses: KubernetesObjectStatus = KubernetesObjectStatus()
    Errors: List[ValidationError] = field(default_factory=lambda : [])
    """ the set of validation errors """
    LastFeedbackDatasetRef: ObjectReference = None
    """ Ref to the last ground true dataset that this model was tested against. """
    LastFeedbackTest: Time = None
    """ Last time that a ground true test was done. """
    LastFeedbackTestResults: List[Measurement] = field(default_factory=lambda : [])
    """ Last results of the ground truth tests. """


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
    P95: float = 0
    """ 95% latency for predictions served by the Predictorlet """
    P99: float = 0
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
    ObjectStatuses: K8sObjectStatusState = None


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
    Role: ModelRole = ModelRole.Live
    """ Role denotes the role of this model """
    MountTar: bool = False
    """ MountTar means that we would mount the model tar file. Else we would use baked image. """
    TrafficSelector: str = ''
    """ TrafficSelector is a filter on the traffic to this model """
    ApprovedBy: ObjectReference = None
    """ The approver account name """
    ApprovedAt: Time = None
    """ The time of approval """
    Port: int = 8080
    """ the port of the model service. """


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
    ConnectionRef: ObjectReference = None
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


@datamodel(proto=inference_pb.PredictionCacheStatus)
class PredictionCacheStatus(Configuration):
    LastAccessed: Time = None


@datamodel(proto=inference_pb.OnlineStoreStatus)
class OnlineStoreStatus(Configuration):
    LastAccessed: Time = None


PredictorletStatus_ = PredictorletStatus
OnlineStoreStatus_ = OnlineStoreStatus


@datamodel(proto=inference_pb.PredictorStatus)
class PredictorStatus(Configuration):
    """ PredictorStatus contain the current state of the Predictor resource """
    ObservedGeneration: int = 0
    """ ObservedGeneration is the last generation that was acted on """
    History: List[ModelRecord] = field(default_factory=lambda : [])
    """ The collection of historical records of models deployed to the Predictor, used internally to roll-back models """
    ModelsStatus: List[ModelDeploymentStatus] = field(default_factory=lambda : [])
    """ The status of the shadow models """
    PredictorletStatus: PredictorletStatus_ = None
    """
    The status of the Predictorlet associated with the Predictor. The Predictorlet is a service which handles prediction traffic
    and routes predictions to individual models based on the specification of the Predictor
    """
    CacheStatus: PredictionCacheStatus = None
    """ The status of the prediction cache managed by the Predictor """
    OnlineStoreStatus: OnlineStoreStatus_ = OnlineStoreStatus_()
    """ The status of the online store managed by the Predictor """
    LastPredictionDataset: Time = None
    """ The last time that a prediction dataset was created """
    LastUpdated: Time = None
    """ The last time the object was updated """
    EndPoint: str = ''
    """ The end-point URL of the Predictor """
    FailureReason: StatusError = None
    """ In the case of failure, the Predictor resource controller will set this field with a failure reason """
    FailureMessage: str = ''
    """ In the case of failure, the Predictor resource controller will set this field with a failure reason """
    Conditions: List[PredictorCondition] = field(default_factory=lambda : [])


@datamodel(proto=inference_pb.FeedbackTestSpec)
class FeedbackTestSpec(Configuration):
    Enabled: bool = False
    Schedule: RunSchedule = None
    """ The schedule on which model monitoring computations will be performed """
    Tests: TestSuite = TestSuite()
    """ Define the tests to run against the predictor. """


DriftMetric = Metric


@datamodel(proto=data_pb.DriftThreshold)
class DriftThreshold(Configuration):
    """ Define a threshold """
    Metric: DriftMetric = DriftMetric.Accuracy
    """ The metric type name (e.g. F1 / Accuracy) """
    Value: float = 0
    """ The value of the metric for quantitive observations """


@datamodel(proto=inference_pb.DriftDetectionSpec)
class DriftDetectionSpec(Configuration):
    """
    ==============================================================================
    Monitoring spec
    ==============================================================================
    """
    Enabled: bool = False
    """ Indicates if model monitoring is enabled for the model """
    UnitTestsTemplate: TestSuite = TestSuite()
    """ Define the tests to run against the predictor. """
    Schedule: RunSchedule = None
    """ The schedule on which model monitoring computations will be performed """
    OutlierDetectionModelRef: ObjectReference = None
    """
    Reference to a model that will be used for outlier detection. If empty, an outlier detection model.
    Currently not in use.
    """
    GenDriftTests: bool = False
    """ If true, automatically generate drift test to all the columns based on the column type """
    MinPredictions: int = 1000
    """ If true, automatically generate drift test to all the columns based on the column type """
    Columns: List[str] = field(default_factory=lambda : [])
    """ Set the list of columns for drift detection, if empty, watch all the columns. """
    DriftThresholds: List[DriftThreshold] = field(default_factory=lambda : [])
    """
    The drift threshold for drift metrics.
    If empty will be set the modela
    """
    MaxHistograms: int = 5
    """ how many feature histograms to keep in memory (as kubernetes objects). Histograms are garbage collected. """
    PeriodSeconds: int = 3600
    """
    The duration in seconds that an histogram is updated before computing drift
    the default is one hour
    """


@datamodel(proto=inference_pb.PredictionLoggingSpec)
class PredictionLoggingSpec(Configuration):
    """ PredictionLoggingSpec specifies the configuration to log incoming and outgoing prediction requests """
    Enabled: bool = False
    """ Indicates if prediction logging is enabled """
    SamplePercent: int = 0
    """ The number percentage (0 through 100) of prediction requests to log """
    Rows: int = 0
    """ Number of rows in the serving dataset """
    BackupFreqSeconds: int = 0
    """ Backup Frequency seconds. """
    BackupConnectionRef: ObjectReference = None
    """ Reference to backup location. """
    Location: DataLocation = None
    """ Target location of the serving dataset """


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
    ServingTests: TestSuite = TestSuite()
    """ Serving tests """


@datamodel(proto=inference_pb.ForwardCurtainSpec)
class ForwardCurtainSpec(Configuration):
    Enabled: bool = False
    CurtainRef: ObjectReference = None
    """ The forward curtain receives prediction requests before the prediction (currently unimplemented) """
    Percent: int = 0
    """ Percent of request that are sent to the foreward curtain. """


@datamodel(proto=inference_pb.BackwardCurtainSpec)
class BackwardCurtainSpec(Configuration):
    Enabled: bool = False
    CurtainRef: ObjectReference = None
    """ The forward curtain receives prediction requests before the prediction (currently unimplemented) """
    ConfidenceLow: float = 0
    """ For backward curtain is the confidence low """
    ConfidenceHigh: float = 0
    """ For backward curtain is the confidence high """


@datamodel(proto=inference_pb.OnlineFeatureStoreSpec)
class OnlineFeatureStoreSpec(Configuration):
    """
    /////////////////////////////////////////////////////////
    Online feature store spec
    /////////////////////////////////////////////////////////
    OnlineFeaturestoreSpec specifies the connection information for an online feature store
    """
    Enabled: bool = False
    Hostname: str = ''
    """ The host name of the feature store micro service. """


@datamodel(proto=inference_pb.FastSlowModelSpec)
class FastSlowModelSpec(Configuration):
    """
    Fast slow model mode, use two models as the live.
    All request are send first to the fast model.
    """
    Enabled: bool = False
    """ Indicates if model monitoring is enabled for the model """
    FastModelRef: ObjectReference = None
    """ Reference to the fast model """
    SlowModelRef: ObjectReference = None
    """ Reference to the slow model """
    ProbaLowPct: int = 40
    """ The low range of confidence. """
    ProbaHighPct: int = 60
    """ The high range of confidence , Must be higher than probalow """


AccessType_ = AccessType


@datamodel(proto=catalog_pb.AccessSpec)
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
    AuthMethod: str = 'none'
    """ Indicates """


@datamodel(proto=inference_pb.PredictorSpec)
class PredictorSpec(Configuration):
    """ PredictorSpec defines the desired state of a Predictor """
    VersionName: str = ''
    """
    If specified, the name of the DataProductVersion which describes the version of the resource
    that exists in the same DataProduct namespace as the resource
    """
    Description: str = ''
    """ If specified, the user-provided description of the Predictor """
    ProductRef: ObjectReference = None
    """ The reference to the DataProduct that the resource exists under """
    ServingsiteRef: ObjectReference = ObjectReference('modela', 'modela-lab')
    """
    If specified, the reference to the ServingSite resource that hosts the Predictor
    If not specified, the predictor will be hosted on the default serving site.
    """
    Models: List[ModelDeploymentSpec] = field(default_factory=lambda : [])
    """
    If specified, the collection of shadow models. A shadow model receives prediction request, but does
    not serve the reply.
    """
    Progressive: ProgressiveSpec = None
    """
    The specification to progressively deploy a new live model. ModelDeploymentSpec specifications within Models that have the
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
    """ Store specifies the configuration of the online data store """
    ForwardCurtain: ForwardCurtainSpec = ForwardCurtainSpec()
    """ Forward curtain """
    BackwardCurtain: BackwardCurtainSpec = BackwardCurtainSpec()
    """ Backward curtain """
    Task: TaskType = None
    """ The task type of the Predictor, which should match the task type of the models being served """
    PredictionThreshold: float = 0
    """ The prediction threshold """
    Drift: DriftDetectionSpec = DriftDetectionSpec()
    """ Spec for the drift detection process """
    Feedback: FeedbackTestSpec = FeedbackTestSpec()
    """ Spec for the ground truth process. """
    FastSlow: FastSlowModelSpec = FastSlowModelSpec()
    """ Fast slow is the specification of deployment of a fast - slow models. """
    NotifierRef: ObjectReference = None
    """ NotifierRef references a Notifier resource that will be triggered in the case that a concept or data drift is detected """


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
