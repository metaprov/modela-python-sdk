from dataclasses import field
from typing import List

from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import Measurement
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import *
from github.com.metaprov.modelaapi.services.common.v1.common_pb2 import ModelProfile

from modela.Configuration import Configuration, ImmutableConfiguration, datamodel
from modela.common import PriorityLevel, Time, StatusError, ConditionStatus, ObjectReference, Freq, Plot
from modela.data.common import DataType
from modela.data.models import DataLocation, GovernanceSpec, CompilerSettings, Correlation, DataSourceSpec
from modela.inference.common import AccessType
from modela.infra.models import Workload, OutputLogs, NotificationSetting
from modela.training.common import *


@datamodel(proto=ModelValidation)
class ModelValidation(Configuration):
    Type: ModelValidationType = None
    PrevModel: str = ""
    DatasetName: str = ""
    DriftFreq: Freq = None
    DriftInterval: int = 0
    Column: str = ""
    Metric: Metric = None
    Min: float = 0
    Max: float = 0
    MinPercent: float = 0
    MaxPercent: float = 0
    Agg: Aggregate = None


@datamodel(proto=ModelValidationResult)
class ModelValidationResult(Configuration):
    Type: str = ""
    DatasetName: str = ""
    ModelName: str = ""
    Column: str = ""
    Error: str = ""
    Metric: Metric = None
    ActualValue: float = 0
    Passed: bool = False
    At: Time = None
    DurationInSec: int = 0


@datamodel(proto=Measurement)
class Measurement(ImmutableConfiguration):
    Metric: Metric = Metric.Null
    Value: float = 0


@datamodel(proto=SegmentSpec)
class Segment(Configuration):
    ColumnName: str = ""
    Op: Operation = Operation.EQ
    Value: str = ""


@datamodel(proto=HyperParameterValue)
class HyperParameterValue(ImmutableConfiguration):
    Name: str = ""
    Value: str = ""


@datamodel(proto=ClassicalEstimatorSpec)
class ClassicalEstimatorSpec(ImmutableConfiguration):
    AlgorithmName: str = ""
    Parameters: List[HyperParameterValue] = field(default_factory=lambda: [])


@datamodel(proto=ChatbotEstimatorSpec)
class ChatbotEstimatorSpec(ImmutableConfiguration):  # Not Implemented
    Base: str = ""


@datamodel(proto=NLPEstimatorSpec)
class NLPEstimatorSpec(ImmutableConfiguration):  # Not Implemented
    Base: str = ""


@datamodel(proto=FeatureImportance)
class FeatureImportance(ImmutableConfiguration):
    Feature: str = ""
    Importance: float = 0


@datamodel(proto=SuccessiveHalvingSpec)
class SuccessiveHalving(ImmutableConfiguration):
    Budget: int = 0
    Bracket: int = 0
    Rung: int = 0
    ConfID: int = 0
    Modality: ModalityType = None


@datamodel(proto=DataSplitSpec)
class DataSplit(Configuration):
    Method: DataSplitMethod = DataSplitMethod.Auto
    Train: int = 80
    Validation: int = 0
    Test: int = 20
    SplitColumn: str = ""
    Segments: List[Segment] = field(default_factory=lambda: [])
    TrainDataset: str = ""
    TestDataset: str = ""


@datamodel(proto=TrainingSpec)
class Training(Configuration):
    Priority: PriorityLevel = PriorityLevel.Medium
    Cvtype: CvType = CvType.CVTypeKFold
    CV: bool = True
    Folds: int = 5
    Split: DataSplit = DataSplit()
    EvalMetrics: List[Metric] = field(default_factory=lambda: [])
    EarlyStop: bool = False
    CheckpointInterval: int = 10
    Sh: SuccessiveHalving = None
    Seed: float = 42
    Resources: Workload = Workload("general-large")
    Gpu: bool = False
    Distributed: bool = False
    NodeCount: int = 1
    SamplePct: int = 100
    LabRef: ObjectReference = ObjectReference("default-tenant", "default-lab")


@datamodel(proto=ServingSpec)
class ServingSpec(ImmutableConfiguration):
    Resources: Workload = None


@datamodel(proto=TextPipelineSpec)
class TextPipelineSpec(ImmutableConfiguration):
    Encoder: TextEncoding = TextEncoding.Auto
    Tokenizer: str = ""
    Stopwords: bool = True
    Pos: bool = True
    Lemma: bool = True
    Stem: bool = True
    Embedding: str = ""
    Svd: bool = True
    MaxSvdComponents: int = 0


@datamodel(proto=ImagePipelineSpec)
class ImagePipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@datamodel(proto=VideoPipelineSpec)
class VideoPipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@datamodel(proto=AudioPipelineSpec)
class AudioPipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@datamodel(proto=ResourceConsumption)
class ResourceConsumption(ImmutableConfiguration):
    Cpu: float = 0
    Mem: float = 0
    Gpu: float = 0


@datamodel(proto=DataHashes)
class DataHashes(ImmutableConfiguration):
    TrainHash: str = ""
    TestingHash: str = ""
    ValidationHash: str = ""


@datamodel(proto=GeneratedColumnSpec)
class GeneratedColumnSpec(ImmutableConfiguration):
    Name: str = ""
    Datatype: DataType = DataType.Text
    First: str = ""
    Second: str = ""
    Original: str = ""


@datamodel(proto=FeatureSelectionSpec)
class FeatureSelection(Configuration):
    Enabled: bool = False
    SamplePct: int = 100
    Embedding: bool = False
    Filter: bool = False
    Wrapper: bool = False
    Pipeline: List[FeatureSelectionType] = field(default_factory=lambda: [])
    VarianceThresholdPct: int = 5
    CorrThreshold: int = 95
    TopN: int = 0
    CumulativeImportancePercent: int = 95
    Reserved: List[str] = field(default_factory=lambda: [])


@datamodel(proto=FeaturePair)
class FeaturePair(ImmutableConfiguration):
    X: str = ""
    Y: str = ""


@datamodel(proto=InterpretabilitySpec)
class Interpretability(Configuration):
    Ice: bool = True
    Icepairs: List[FeaturePair] = field(default_factory=lambda: [])
    Lime: bool = False
    Shap: ShapType = ShapType.Auto
    Shappairs: List[FeaturePair] = field(default_factory=lambda: [])
    Counterfactual: bool = False
    Anchor: bool = False


# Name collision workaround
ImputationType = Imputation
DiscretisationType = Discretisation
OutlierHandlingType = OutlierHandling
VariableTransformationType = VariableTransformation
DatetimeTransformationType = DatetimeTransformation
ScalingType = Scaling


@datamodel(proto=FeatureEngineeringPipeline)
class FeatureEngineeringPipeline(ImmutableConfiguration):
    Name: str = ""
    Datatype: DataType = DataType.Text
    Columns: List[str] = field(default_factory=lambda: [])
    Imputation: ImputationType = ImputationType.AutoImputer
    Encoding: CategoricalEncoding = CategoricalEncoding.NoneEncoding
    Scaling: ScalingType = ScalingType.NoScaling
    Discretisation: DiscretisationType = DiscretisationType.NoDiscretisation
    VariableTransformation: VariableTransformationType = VariableTransformationType.NoneTransform
    OutlierHandling: OutlierHandlingType = OutlierHandlingType.AutoOutlier
    DatetimeTransformation: DatetimeTransformationType = DatetimeTransformationType.NoneDatetime
    Text: TextPipelineSpec = None
    Image: ImagePipelineSpec = None
    Audio: AudioPipelineSpec = None
    Video: VideoPipelineSpec = None
    Generated: List[GeneratedColumnSpec] = field(default_factory=lambda: [])
    Custom: List[GeneratedColumnSpec] = field(default_factory=lambda: [])
    Drop: bool = False
    Passthrough: bool = False


@datamodel(proto=FeatureEngineeringSpec)
class FeatureEngineeringSpec(ImmutableConfiguration):
    Pipelines: List[FeatureEngineeringPipeline] = field(default_factory=lambda: [])
    Imbalance: ImbalanceHandling = ImbalanceHandling.ImbalanceAuto
    Selection: FeatureSelection = FeatureSelection()


@datamodel(proto=EnsembleSpec)
class EnsembleSpec(ImmutableConfiguration):
    Models: List[str] = field(default_factory=lambda: [])
    Estimators: List[ClassicalEstimatorSpec] = field(default_factory=lambda: [])
    Base: ClassicalEstimatorSpec = None
    Type: EnsembleType = None


TrainingSpec = Training
InterpretabilitySpec = Interpretability


@datamodel(proto=ModelSpec)
class ModelSpec(ImmutableConfiguration):
    Owner: str = "no-one"
    VersionName: str = "v0.0.1"
    ModelVersion: str = ""
    StudyName: str = ""
    DatasetName: str = ""
    Task: TaskType = None
    Objective: Metric = None
    FeatureEngineering: FeatureEngineeringSpec = None
    Estimator: ClassicalEstimatorSpec = None
    NlpEstimator: NLPEstimatorSpec = None
    Ensemble: EnsembleSpec = None
    Training: TrainingSpec = None
    Serving: ServingSpec = None
    Tested: bool = False
    Aborted: bool = False
    Packaged: bool = False
    Published: bool = False
    Pushed: bool = False
    Reported: bool = False
    Paused: bool = False
    Profiled: bool = False
    Archived: bool = False
    Forecasted: bool = False
    Released: bool = False
    Benchmarked: bool = False
    Explained: bool = False
    Baseline: bool = False
    Flagged: bool = False
    Location: DataLocation = None
    # Forecast: ForecastSpec = None
    Compilation: CompilerSettings = None
    ActiveDeadlineSeconds: int = 600
    EstimatorType: ModelType = ModelType.Classical
    ModelClass: ModelClassType = None
    TrialID: int = 0
    Governance: GovernanceSpec = None
    Interpretability: InterpretabilitySpec = None


@datamodel(proto=InterpretabilityStatus)
class InterpretabilityStatus(ImmutableConfiguration):
    TrainingStartTime: Time = None
    TrainingEndTime: Time = None
    ExplainerURI: str = ""
    TrainShapValuesURI: str = ""
    TestShapValuesURI: str = ""
    Importance: List[FeatureImportance] = field(default_factory=lambda: [])


@datamodel(proto=ModelCondition)
class ModelCondition(ImmutableConfiguration):
    Type: ModelConditionType = ModelConditionType.ModelReady
    Status: ConditionStatus = ConditionStatus.ConditionUnknown
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""


@datamodel(proto=ModelStatus)
class ModelStatus(ImmutableConfiguration):
    StartTime: Time = None
    TrainingStartTime: Time = None
    TrainingEndTime: Time = None
    TestingStartTime: Time = None
    TestingEndTime: Time = None
    EndTime: Time = None
    CvScore: float = 0
    TrainingScore: float = 0
    TestScore: float = 0
    Cost: float = 0
    Best: bool = False
    Cv: List[Measurement] = field(default_factory=lambda: [])
    Train: List[Measurement] = field(default_factory=lambda: [])
    Test: List[Measurement] = field(default_factory=lambda: [])
    Phase: ModelPhase = ModelPhase.Pending
    ReportName: str = ""
    ReportUri: str = ""
    ManifestUri: str = ""
    WeightsUri: str = ""
    LabelEncoderUri: str = ""
    LogsUri: str = ""
    ProfileUri: str = ""
    MisclassUri: str = ""
    TarUri: str = ""
    AppUri: str = ""
    ImageName: str = ""
    Importance: List[FeatureImportance] = field(default_factory=lambda: [])
    ForecastUri: str = ""
    PythonVersion: str = ""
    TrainDataset: DataLocation = None
    TestDataset: DataLocation = None
    ValidationDataset: DataLocation = None
    ObservedGeneration: int = 0
    TrainingRows: int = 0
    TestingRows: int = 0
    ValidationRows: int = 0
    FailureReason: StatusError = None
    FailureMessage: str = ""
    Progress: int = 0
    SizeInBytes: int = 0
    Latency: float = 0
    Url: str = ""
    PredictorName: str = ""
    ReleasedAt: Time = None
    TarfileHash: str = ""
    ImageHash: str = ""
    TrainingDataHash: DataHashes = None
    TrainingResources: ResourceConsumption = None
    TestingResources: ResourceConsumption = None
    TrainedBy: str = ""
    Team: str = ""
    Endpoint: str = ""
    Logs: OutputLogs = None
    CorrelationsWithTarget: List[Correlation] = field(default_factory=lambda: [])
    TopCorrelations: List[Correlation] = field(default_factory=lambda: [])
    LastUpdated: Time = None
    # GovernanceStatus: GovernanceStatus = None
    Interpretability: InterpretabilityStatus = None
    Conditions: List[ModelCondition] = field(default_factory=lambda: [])


@datamodel(proto=ModelProfile)
class ModelProfile(ImmutableConfiguration):
    Name: str = ""
    Importance: List[float] = field(default_factory=lambda: [])
    Plots: List[Plot] = field(default_factory=lambda: [])


@datamodel(proto=AlgorithmSearchSpaceSpec)
class AlgorithmSearchSpace(Configuration):
    Allowlist: List[ClassicEstimator] = field(default_factory=lambda: [])
    Filter: AlgorithmFilter = AlgorithmFilter.NoFilter


@datamodel(proto=SuccessiveHalvingOptions)
class SuccessiveHalvingOptions(Configuration):
    MaxBudget: int = 81
    EliminationRate: int = 3
    Modality: ModalityType = ModalityType.Epochs


@datamodel(proto=PrunerSpec)
class PrunerSettings(Configuration):
    Type: Pruner = Pruner.MedianPruner
    StartupTrials: int = 5
    WarmupTrials: int = 0
    MinTrials: int = 1
    IntervalTrials: int = 1
    Percentile: int = 25
    Lower: int = 0
    Upper: int = 0
    ShOptions: SuccessiveHalvingOptions = SuccessiveHalvingOptions()


SamplerType = Sampler


@datamodel(proto=SearchSpec)
class ModelSearch(Configuration):
    Sampler: SamplerType = SamplerType.TPESearch
    Pruner: PrunerSettings = None
    MaxCost: int = 100  # Not Implemented
    MaxTime: int = 30
    MaxModels: int = 10
    MinScore: float = 0
    Trainers: int = 1
    Test: int = 1
    RetainTop: int = 10
    RetainedFor: int = 60
    SearchSpace: AlgorithmSearchSpace = AlgorithmSearchSpace()
    EarlyStopAfter: int = 0
    KeepOnlyTopModel: bool = True
    Objective: Metric = None
    Objective2: Metric = None


@datamodel(proto=BaselineSpec)
class BaselineSettings(Configuration):
    Enabled: bool = False
    Baselines: List[ClassicEstimator] = field(default_factory=lambda: [])
    All: bool = False


@datamodel(proto=FeatureEngineeringSearchSpec)
class FeatureEngineeringSearch(Configuration):
    Enabled: bool = True
    ImbalancedHandler: ImbalanceHandling = ImbalanceHandling.ImbalanceAuto
    Estimator: ClassicEstimator = ClassicEstimator.DecisionTreeClassifier  # FIXME: Should auto detect
    MaxModels: int = 2
    MaxTime: int = 3600
    MaxTrainers: int = 1
    SamplePct: int = 100
    AutoRemove: bool = True
    Reuse: bool = False
    FeatureSelectionTemplate: FeatureSelection = FeatureSelection()


@datamodel(proto=StudyScheduleSpec)
class StudySchedule(Configuration):
    Enabled: bool = False
    StartAt: Time = None


@datamodel(proto=ModelResult)
class ModelResult(Configuration):
    Name: str = ""
    Alg: str = ""
    Score: float = 0
    Error: bool = False
    TrialID: int = 0


@datamodel(proto=GarbageCollectionSpec)
class GarbageCollection(Configuration):
    CollectAtStudyEnd: bool = True
    KeepOnlyBestModelPerAlgorithm: bool = True


@datamodel(proto=EnsemblesSpec)
class Ensemble(Configuration):
    Enabled: bool = False
    VotingEnsemble: bool = False
    StackingEnsemble: bool = True
    Top: int = 3


@datamodel(proto=StudySpec)
class StudySpec(Configuration):
    VersionName: str = "v0.0.1"
    Description: str = ""
    LabRef: ObjectReference = ObjectReference("default-tenant", "default-lab")
    DatasetName: str = ""
    Task: TaskType = TaskType.AutoDetectTask
    FeSearch: FeatureEngineeringSearch = FeatureEngineeringSearch()
    Baseline: BaselineSettings = BaselineSettings()
    Search: ModelSearch = ModelSearch()
    Ensembles: Ensemble = Ensemble()
    TrainingTemplate: Training = Training()
    Schedule: StudySchedule = StudySchedule()
    Interpretability: InterpretabilitySpec = InterpretabilitySpec()
    Aborted: bool = False
    Reported: bool = True
    Paused: bool = False
    Profiled: bool = True
    ModelPublished: bool = False
    ModelImagePushed: bool = False
    ModelBenchmarked: bool = True
    ModelExplained: bool = True
    Fast: bool = False
    Location: DataLocation = DataLocation(BucketName="default-minio-bucket")
    Owner: str = "no-one"
    ActiveDeadlineSeconds: int = 600
    Compilation: CompilerSettings = None
    Template: bool = False
    Flagged: bool = False
    Notification: NotificationSetting = NotificationSetting()
    # ModelImage: ImageLocation = ImageLocation()
    Gc: GarbageCollection = GarbageCollection()
    Ttl: int = 0


@datamodel(proto=StudyCondition)
class StudyCondition(Configuration):
    Type: StudyConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""


@datamodel(proto=GarbageCollectionStatus)
class GarbageCollectionStatus(Configuration):
    Collected: int = 0
    Models: List[ModelResult] = field(default_factory=lambda: [])

@datamodel(proto=StudyPhaseStatus)
class StudyPhaseStatus(Configuration):
    StartTime: Time = None
    EndTime: Time = None
    Waiting: int = 0
    Running: int = 0
    Failed: int = 0
    Completed: int = 0


@datamodel(proto=StudyStatus)
class StudyStatus(ImmutableConfiguration):
    Models: int = 0
    StartTime: Time = None
    EndTime: Time = None
    BestModel: str = ""
    BestModelScore: float = 0
    ProfileUri: str = ""
    ReportName: str = ""
    Phase: StudyPhase = StudyPhase.ModelPending
    ObservedGeneration: int = 0
    TrainDataset: DataLocation = None
    TestDataset: DataLocation = None
    ValidationDataset: DataLocation = None
    LastModelID: int = 0
    FailureReason: StatusError = None
    FailureMessage: str = ""
    TrainingRows: int = 0
    TestingRows: int = 0
    ValidationRows: int = 0
    Progress: int = 0
    BaselineModel: ClassicEstimator = None
    TrainingDataHash: DataHashes = None
    TriggeredBy: TriggerType = None
    Logs: OutputLogs = None
    FeatureEngineering: StudyPhaseStatus = None
    Baseline: StudyPhaseStatus = None
    Search: StudyPhaseStatus = None
    Ensemble: StudyPhaseStatus = None
    Test: StudyPhaseStatus = None
    Explain: StudyPhaseStatus = None
    LastUpdated: Time = None
    BestFE: FeatureEngineeringSpec = None
    Gc: GarbageCollectionStatus = None
    Conditions: List[StudyCondition] = field(default_factory=lambda: [])


@datamodel(proto=ReportCondition)
class ReportCondition(Configuration):
    Type: ReportConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""

ReportType_ = ReportType


@datamodel(proto=ReportSpec)
class ReportSpec(Configuration):
    VersionName: str = "v0.0.1"
    EntityRef: ObjectReference = None
    Location: DataLocation = DataLocation(BucketName="modela")
    ReportType: ReportType_ = None
    Format: ReportFormat = ReportFormat.Pdf
    NotifierName: str = ""
    Owner: str = "no-one"
    Resources: Workload = Workload("memory-large")
    ActiveDeadlineSeconds: int = 600


@datamodel(proto=ReportStatus)
class ReportStatus(Configuration):
    StartTime: Time = None
    EndTime: Time = None
    Phase: ReportPhase = ReportPhase.Pending
    Uri: str = ""
    ObservedGeneration: int = 0
    FailureReason: StatusError = None
    FailureMessage: str = ""
    Logs: OutputLogs = None
    LastUpdated: Time = None
    Conditions: List[ReportCondition] = field(default_factory=lambda: [])


@datamodel(proto=ModelAutobuilderCondition)
class ModelAutobuilderCondition(Configuration):
    Type: ModelAutobuilderConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""


DataSourceTemplate = DataSourceSpec
DatasetType_ = DatasetType

@datamodel(proto=ModelAutobuilderSpec)
class ModelAutobuilderSpec(Configuration):
    DataProductName: str = ""
    DataProductVersionName: str = ""
    DatasourceName: str = ""
    DatasetName: str = ""
    Location: DataLocation = None
    Task: TaskType = None
    Objective: Metric = None
    TargetColumn: str = ""
    MaxTime: int = 60
    MaxModels: int = 10
    AccessMethod: AccessType = AccessType.ClusterIP
    AutoScale: bool = False
    Dataapp: bool = False
    DataSourceSpec: DataSourceSpec = None
    Trainers: int = 1
    Sampler: SamplerType = None
    Aborted: bool = False
    Owner: str = "no-one"
    Resources: Workload = None
    FeatureEngineering: bool = False
    FeatureSelection: bool = False
    ServingSiteRef: ObjectReference = ObjectReference(Namespace="default-tenant", Name="default-serving-site")
    LabRef: ObjectReference = ObjectReference(Namespace="default-tenant", Name="default-lab")
    DatasetType: DatasetType_ = DatasetType_.Tabular


@datamodel(proto=ModelAutobuilderStatus)
class ModelAutobuilderStatus(Configuration):
    FlatFileName: str = ""
    DataSourceName: str = ""
    DatasetName: str = ""
    StudyName: str = ""
    BestModelName: str = ""
    PredictorName: str = ""
    ImageRepoName: str = ""
    Phase: ModelAutobuilderPhase = ModelAutobuilderPhase.Pending
    Rows: int = 0
    Cols: int = 0
    FileSize: int = 0
    Models: int = 0
    TrainedModels: int = 0
    BestModelScore: float = 0
    Estimator: ClassicalEstimatorSpec = None
    StartTime: Time = None
    EndTime: Time = None
    ObservedGeneration: int = 0
    FailureReason: StatusError = None
    FailureMessage: str = ""
    LastUpdated: Time = None
    Conditions: List[ModelAutobuilderCondition] = field(default_factory=lambda: [])
