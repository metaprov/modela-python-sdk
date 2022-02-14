from dataclasses import dataclass, field
from typing import List

from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ModelValidation as MDModelValidation
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Model as MDModel
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ModelSpec as MDModelSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import EnsembleSpec as MDEnsembleSpec

from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import Measurement as MDMeasurement
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ModelCondition as MDModelCondition
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    HyperParameterValue as MDHyperParameterValue
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    ClassicalEstimatorSpec as MDClassicalEstimatorSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    ChatbotEstimatorSpec as MDChatbotEstimatorSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    NLPEstimatorSpec as MDNLPEstimatorSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    FeatureEngineeringSpec as MDFeatureEngineeringSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    FeatureEngineeringPipeline as MDFeatureEngineeringPipeline
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    FeatureImportance as MDFeatureImportance
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    SuccessiveHalvingSpec as MDSuccessiveHalvingSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import DataSplitSpec as MDDataSplitSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import TrainingSpec as MDTrainingSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ServingSpec as MDServingSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import StudyCondition as MDStudyCondition
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    TextPipelineSpec as MDTextPipelineSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    ImagePipelineSpec as MDImagePipelineSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    VideoPipelineSpec as MDVideoPipelineSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    AudioPipelineSpec as MDAudioPipelineSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    ResourceConsumption as MDResourceConsumption
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import DataHashes as MDDataHashes
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    GeneratedColumnSpec as MDGeneratedColumnSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    FeatureSelectionSpec as MDFeatureSelectionSpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import \
    InterpretabilitySpec as MDInterpretabilitySpec
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import FeaturePair as MDFeaturePair
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import SegmentSpec as MDSegmentSpec

from modela.Configuration import Configuration, ImmutableConfiguration
from modela.common import PriorityLevel, Time, StatusError, ConditionStatus, ObjectReference
from modela.data.common import DataType
from modela.data.models import DataLocation, GovernanceSpec, CompilerSettings, Correlation, ImageLocation
from modela.infra.models import Workload, OutputLogs, NotificationSetting
from modela.training.common import *


@dataclass
class Measurement(ImmutableConfiguration):
    Metric: Metric = Metric.Null
    Value: float = 0

    def to_message(self) -> MDMeasurement:
        return self.set_parent(MDMeasurement()).parent


@dataclass
class Segment(Configuration):
    ColumnName: str = ""
    Op: Operation = Operation.EQ
    Value: str = ""

    def to_message(self) -> MDSegmentSpec:
        return self.set_parent(MDSegmentSpec()).parent


@dataclass
class HyperParameterValue(ImmutableConfiguration):
    Name: str = ""
    Value: str = ""

    def to_message(self) -> MDHyperParameterValue:
        return self.set_parent(MDHyperParameterValue()).parent


@dataclass
class ClassicalEstimatorSpec(ImmutableConfiguration):
    AlgorithmName: str = ""
    Parameters: List[HyperParameterValue] = field(default_factory=lambda: [])


@dataclass
class ChatbotEstimatorSpec(ImmutableConfiguration):  # Not Implemented
    Base: str = ""


@dataclass
class NLPEstimatorSpec(ImmutableConfiguration):  # Not Implemented
    Base: str = ""


@dataclass
class FeatureImportance(ImmutableConfiguration):
    Feature: str = ""
    Importance: float = 0

    def to_message(self) -> MDFeatureImportance:
        return self.set_parent(MDFeatureImportance()).parent


@dataclass
class SuccessiveHalving(ImmutableConfiguration):
    Budget: int = 0
    Bracket: int = 0
    Rung: int = 0
    ConfID: int = 0
    Modality: ModalityType = None


@dataclass
class DataSplit(Configuration):
    Method: DataSplitMethod = DataSplitMethod.Random
    Train: int = 80
    Validation: int = 0
    Test: int = 20
    SplitColumn: str = ""
    Segments: List[Segment] = field(default_factory=lambda: [])


@dataclass
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
    Resources: Workload = None
    Gpu: bool = False
    Distributed: bool = False
    NodeCount: int = 1
    SamplePct: int = 100


@dataclass
class ServingSpec(ImmutableConfiguration):
    Resources: Workload = None


@dataclass
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

    def to_message(self) -> MDTextPipelineSpec:
        return self.set_parent(MDTextPipelineSpec()).parent


@dataclass
class ImagePipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@dataclass
class VideoPipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@dataclass
class AudioPipelineSpec(ImmutableConfiguration):  # Not Implemented
    Featurizer: str = None


@dataclass
class ResourceConsumption(ImmutableConfiguration):
    Cpu: float = 0
    Mem: float = 0
    Gpu: float = 0

    def to_message(self) -> MDResourceConsumption:
        return self.set_parent(MDResourceConsumption()).parent


@dataclass
class DataHashes(ImmutableConfiguration):
    TrainHash: str = ""
    TestingHash: str = ""
    ValidationHash: str = ""

    def to_message(self) -> MDDataHashes:
        return self.set_parent(MDDataHashes()).parent


@dataclass
class GeneratedColumnSpec(ImmutableConfiguration):
    Name: str = ""
    Datatype: DataType = DataType.Text
    First: str = ""
    Second: str = ""
    Original: str = ""

    def to_message(self) -> MDGeneratedColumnSpec:
        return self.set_parent(MDGeneratedColumnSpec()).parent


@dataclass
class FeatureSelectionSpec(ImmutableConfiguration):
    Enabled: bool = True
    SamplePct: int = 100
    Embedding: bool = True
    Filter: bool = True
    Wrapper: bool = True
    Pipeline: List[FeatureSelection] = field(default_factory=lambda: [])
    VarianceThresholdPct: int = 5
    CorrThreshold: int = 95
    TopN: int = 0
    CumulativeImportancePercent: int = 95
    Reserved: List[str] = field(default_factory=lambda: [])


@dataclass
class FeaturePair(ImmutableConfiguration):
    X: str = ""
    Y: str = ""

    def to_message(self) -> MDFeaturePair:
        return self.set_parent(MDFeaturePair()).parent


@dataclass
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


@dataclass
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

    def to_message(self) -> MDFeatureEngineeringPipeline:
        return self.set_parent(MDFeatureEngineeringPipeline()).parent


@dataclass
class FeatureEngineeringSpec(ImmutableConfiguration):
    Pipelines: List[FeatureEngineeringPipeline] = field(default_factory=lambda: [])
    Imbalance: ImbalanceHandling = ImbalanceHandling.ImbalanceAuto
    Selection: FeatureSelectionSpec = None


@dataclass
class EnsembleSpec(ImmutableConfiguration):
    Models: List[str] = field(default_factory=lambda: [])
    Estimators: List[ClassicalEstimatorSpec] = field(default_factory=lambda: [])
    Base: ClassicalEstimatorSpec = None
    Type: EnsembleType = None


@dataclass
class ModelSpec(ImmutableConfiguration):
    """
    Docstring
    """
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
    Training: Training = None
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
    Interpretability: Interpretability = None


@dataclass
class InterpretabilityStatus(ImmutableConfiguration):
    TrainingStartTime: Time = None
    TrainingEndTime: Time = None
    ExplainerURI: str = ""
    TrainShapValuesURI: str = ""
    TestShapValuesURI: str = ""
    Importance: List[FeatureImportance] = field(default_factory=lambda: [])


@dataclass
class ModelCondition(ImmutableConfiguration):
    Type: ModelConditionType = ModelConditionType.ModelReady
    Status: ConditionStatus = ConditionStatus.ConditionUnknown
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""

    def to_message(self) -> MDModelCondition:
        return self.set_parent(MDModelCondition()).parent


InterpretabilitySpec = Interpretability


@dataclass
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
    TrainerImage: str = ""
    Endpoint: str = ""
    Logs: OutputLogs = None
    CorrelationsWithTarget: List[Correlation] = field(default_factory=lambda: [])
    TopCorrelations: List[Correlation] = field(default_factory=lambda: [])
    LastUpdated: Time = None
    # GovernanceStatus: GovernanceStatus = None
    # Interpretability: InterpretabilityStatus = None
    Conditions: List[ModelCondition] = field(default_factory=lambda: [])


@dataclass
class AlgorithmSearchSpace(Configuration):
    Allowlist: List[ClassicEstimator] = field(default_factory=lambda: [])
    Filter: AlgorithmFilter = AlgorithmFilter.NoFilter


@dataclass
class SuccessiveHalvingOptions(Configuration):
    MaxBudget: int = 81
    EliminationRate: int = 3
    Modality: ModalityType = ModalityType.Epochs


@dataclass
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


@dataclass
class ModelSearch(Configuration):
    Sampler: SamplerType = SamplerType.BayesianSearch
    Pruner: PrunerSettings = None
    MaxCost: int = 100
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
    Objective: Metric = Metric.Null
    Objective2: Metric = None


@dataclass
class BaselineSettings(Configuration):
    Enabled: bool = False
    Baselines: List[ClassicEstimator] = field(default_factory=lambda: [])
    All: bool = False


@dataclass
class FeatureEngineeringSearch(Configuration):
    Enabled: bool = True
    ImbalancedHandler: ImbalanceHandling = ImbalanceHandling.ImbalanceAuto
    Estimator: ClassicEstimator = None
    MaxModels: int = 10
    MaxTime: int = 3600
    MaxTrainers: int = 1
    SamplePct: int = 100
    AutoRemove: bool = True
    Reuse: bool = False
    FeatureSelectionTemplate: FeatureSelectionSpec = None


@dataclass
class StudySchedule(Configuration):
    Enabled: bool = False
    StartAt: Time = None


@dataclass
class GarbageCollection(Configuration):
    CollectAtStudyEnd: bool = True
    KeepOnlyBestModelPerAlgorithm: bool = True


@dataclass
class Ensemble(Configuration):
    Enabled: bool = False
    VotingEnsemble: bool = False
    StackingEnsemble: bool = True
    Top: int = 3


@dataclass
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
    Location: DataLocation = None
    Owner: str = "no-one"
    ActiveDeadlineSeconds: int = 600
    Compilation: CompilerSettings = None
    Template: bool = False
    Flagged: bool = False
    Notification: NotificationSetting = NotificationSetting()
    ModelImage: ImageLocation = ImageLocation()
    Gc: GarbageCollection = GarbageCollection()
    Ttl: int = 0


@dataclass
class StudyCondition(Configuration):
    Type: StudyConditionType = None
    Status: ConditionStatus = None
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""

    def to_message(self) -> MDStudyCondition:
        return self.set_parent(MDStudyCondition()).parent


@dataclass
class GarbageCollectionStatus(Configuration):
    Collected: int = 0


@dataclass
class StudyPhaseStatus(Configuration):
    StartTime: Time = None
    EndTime: Time = None
    Waiting: int = 0
    Running: int = 0
    Failed: int = 0
    Completed: int = 0


@dataclass
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
