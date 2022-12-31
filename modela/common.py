from enum import Enum
from typing import List
from dataclasses import field

from github.com.metaprov.modelaapi.services.common.v1.common_pb2 import Plot, Histogram
from k8s.io.api.core.v1.generated_pb2 import ObjectReference, SecretReference
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import Time

from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import TestSuite, DataTestCase, \
    TestSuiteResult, \
    DataTestCaseResult

from modela.Configuration import Configuration, ImmutableConfiguration, datamodel
import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
from dataclasses import field
from enum import Enum
from typing import List

import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import TestSuite, DataTestCase, \
    TestSuiteResult, \
    DataTestCaseResult, \
    HistogramData
from github.com.metaprov.modelaapi.services.common.v1.common_pb2 import Plot
from k8s.io.api.core.v1.generated_pb2 import ObjectReference, SecretReference
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import Time

from modela.Configuration import Configuration, ImmutableConfiguration, datamodel


class ConditionStatus(Enum):
    ConditionTrue = "True"
    ConditionFalse = "False"
    ConditionUnknown = "Unknown"


class TaskName(Enum):
    BatchPredictTask = "batch-predict"
    ForecastTask = "forecast"
    ProfileDatasetTask = "profile-dataset"
    SnapshotDatasetTask = "snapshot-dataset"
    ProfileStudyTask = "profile-study"
    ProfileModelTask = "profile-model"
    PublishModelTask = "publish-model"
    BakeModelTask = "bake-model"
    RunRecipeTask = "run-recipe"
    ReportDatasetTask = "report-dataset"
    ReportModelTask = "report-model"
    ReportStudyTask = "report-study"
    ReportPeriodTask = "report-period"
    ReportSummaryTask = "report-summary"
    SplitDatasetTask = "split-dataset"
    TestEnsembleTask = "test-ensemble"
    TestModelTask = "test-model"
    TrainEnsembleTask = "train-ensemble"
    TrainModelTask = "train-model"
    ValidateDatasetTask = "validate-dataset"
    MergeForecastTask = "merge-forecast"
    PartitionForecastTask = "partition-forecast"
    SplitDatasetToRungs = "split-dataset-to-rungs"
    PackageModelTask = "package-model"
    FeatureGenTask = "feature-gen"
    FeatureSelectTask = "feature-select"
    GenerateDataset = "generate-dataset"
    ValidateModel = "validate-model"


class StatusError(Enum):
    InvalidConfiguration = "InvalidConfiguration"
    InsufficientResources = "InsufficientResources"
    CreateError = "CreateError"
    UpdateError = "UpdateError"
    DeleteError = "DeleteError"


class AssertionType(Enum):
    MultiDatasetSameNumberOfRows = "multi-dataset-same-number-of-rows"
    MultiDatasetOuterJoinEmpty = "multi-dataset-outer-join-empty"
    MultiDatasetOuterJoinNotEmpty = "multi-dataset-outer-join-not-empty"
    MultiDatasetInnerJoinEmpty = "multi-dataset-inner-join-empty"
    MultiDatasetInnerJoinNotEmpty = "multi-dataset-inner-join-not-empty"
    MultiDatasetLeftJoinEmpty = "multi-dataset-left-join-empty"
    MultiDatasetLeftJoinNotEmpty = "multi-dataset-left-join-not-empty"
    MultiDatasetRightJoinEmpty = "multi-dataset-right-join-empty"
    MultiDatasetRightJoinNotEmpty = "multi-dataset-right-join-not-empty"
    DatasetColumnsCountEqual = "dataset-columns-count-equal"
    DatasetColumnsNameInSet = "dataset-columns-in-set"
    DatasetColumnsInOrderedList = "dataset-columns-in-ordered-list"
    DatasetRowCountBetween = "dataset-row-count-between"
    DatasetNotEmpty = "dataset-dataset-not-empty"
    DatasetTestNameNameEmpty = "dataset-empty"
    MultiColumnCorr = "multi-column-corr"
    ColumnTestNameColumnExist = "column-exist"
    ColumnHaveValues = "column-have-values"
    ColumnHasNoValue = "column-has-no-values"
    ColumnHaveNulls = "column-value-have-nulls"
    ColumnHasNoNull = "column-value-has-no-nulls"
    ColumnOfType = "column-of-type"
    ColumnValuesInSet = "column-values-in-set"
    ColumnValuesIncreasing = "column-values-increasing"
    ColumnsValuesDecreasing = "column-values-decreasing"
    ColumnValueLengthBetween = "column-value-length-between"
    ColumnValueNameMatchRegex = "column-value-match-regex"
    ColumnValueIsDate = "column-value-is-date"
    ColumnValueIsJson = "column-value-is-json"
    ColumnValueInDomain = "column-value-in-domain"
    ColumnUniqueValueCountBetween = "column-unique-value-count-between"
    ColumnOutlierValueUniqueBetween = "column-outlier-value-count-between"
    ColumnValidValueUniqueBetween = "column-valid-values-count-between"
    ColumnMismatchValueBetween = "column-mismatch-values-between"
    ColumnValueMinBetween = "column-value-min-between"
    ColumnValueLowerQuartileBetween = "column-value-lower-quartile-between"
    ColumnValueMedianBetween = "column-value-median-between"
    ColumnValueAvgBetween = "column-value-average-between"
    ColumnValueUpperQuartileBetween = "column-value-upper-quartile-between"
    ColumnValueMaxBetween = "column-value-max-between"
    ColumnValueStddevBetween = "column-value-stddev-between"
    ColumnValueChiSquarePValueBetween = "column-value-chi-square-p-value-between"
    ColumnValuePairCramersBetween = "column-value-pair-cramers-between"
    FileSizeBetween = "file-size-between"
    FileExist = "file-exist"
    FileRegexMatchCountBetween = "file-regex-match-count-between"
    FileValidJson = "file-valid-json"
    FileValidCsv = "file-valid-csv"

    # Model Tests
    ModelAccuracy = "model-accuracy-greater-than"
    ModelRocAuc = "model-roc-auc-greater-than"
    ModelF1 = "model-f1-greater-than"
    ModelPrecision = "model-precision-greater-than"
    ModelRecall = "model-recall-less-than"
    ModelMSE = "model-mse-less-than"
    ModelRMSE = "model-rmse-less-than"
    ModelMAPE = "model-mape-less-than"

    ModelAccuracyGreaterThanBaseline = "model-accuracy-greater-than-baseline"
    ModelRocAucGreaterThanBaseline = "model-roc-auc-greater-than-baseline"
    ModelF1GreaterThanBaseline = "model-f1-greater-than-baseline"
    ModelPrecisionGreaterThanBaseline = "model-precision-greater-than-baseline"
    ModelRecallGreaterThanBaseline = "model-recall-less-than-baseline"
    ModelMSELessThanBaseline = "model-mse-less-than-baseline"
    ModelRMSELessThanBaseline = "model-rmse-less-than-baseline"
    ModelMAPELessThanBaseline = "model-mape-less-than-baseline"

    NoneAssertion = "none"


class DataTestType(Enum):
    MultiDataset = "multi-dataset"
    Dataset = "dataset"
    MultiColumn = "multi-column"
    Column = "column"
    Model = "model"
    DataDrift = "data-drift"


class FeatureFilterType(Enum):
    AllFeatures = "all-features"
    ImportantFeatures = "important-features"
    FeatureList = "features-list"
    NumericFeatures = "numeric-features"
    CatFeatures = "categorical-features"
    TextFeatures = "text-features"


class ReferenceDataType(Enum):
    TrainingData = "train-data"
    TestingData = "test-data"
    DataRange = "range"
    DataMovingAvg = "moving-avg"


class PriorityLevel(Enum):
    Low = "low"
    Medium = "medium"
    High = "high"
    Urgent = "urgent"


class HardwareTarget(Enum):
    AMDEPYC2 = "amd-epyc-2"
    ARMA53 = "arma-53"
    ARMA72 = "arma-72"
    IntelCascadeLake = "intel-cascade-lake"
    IntelBroadwell = "intel-broadwell"
    IntelSkylake = "intel-skylake"
    TeslaV100 = "tesla-v100"
    TeslaK80 = "tesla-k80"
    T4 = "t4"
    RaspberryPi8MODELB = "raspberry-pi8-modela-b"


class TriggerScheduleEventType(Enum):
    Now = "now"
    Once = "once"
    Hourly = "hourly"
    Daily = "daily"
    Weekly = "weekly"
    Monthly = "monthly"
    Yearly = "yearly"
    Cron = "cron"


class Freq(Enum):
    Seconds = "second"
    Minutes = "minute"
    Hours = "hour"
    Days = "day"
    Weeks = "week"
    Months = "month"
    Qtrs = "quarter"
    Years = "year"


@datamodel(proto=Time)
class Time(Configuration):
    Seconds: int = 0
    Nanos: int = 0


class Metric(Enum):
    Accuracy = "accuracy"
    AveragePrecision = "average-precision"
    BalancedAccuracy = "balanced-accuracy"
    F1Binary = "f1"
    F1Micro = "f1-micro"
    F1Macro = "f1-macro"
    F1Weighted = "f1-weighted"
    F1Samples = "f1-samples"
    PrecisionBinary = "precision"
    PrecisionMicro = "precision-micro"
    PrecisionMacro = "precision-macro"
    PrecisionWeighted = "precision-weighted"
    PrecisionSamples = "precision-samples"
    RecallBinary = "recall"
    RecallMacro = "recall-macro"
    RecallMicro = "recall-micro"
    RecallWeighted = "recall-weighted"
    RecallSamples = "recall-samples"
    LogLoss = "log-loss"
    RocAuc = "auc"
    RocAucMicro = "auc-micro"
    RocAucMacro = "auc-macro"
    RocAucWeighted = "auc-weighted"
    PRRocAuc = "pr-auc"
    PRRocAucMicro = "pr-auc-micro"
    PRRocAucMacro = "pr-auc-macro"
    PRRocAucWeighted = "pr-auc-weighted"
    ZeroOne = "zero-one"
    HammingLoss = "hamming-loss"
    HingeLoss = "hinge-loss"
    JacquardScore = "jacquard-loss"
    MatthewsCorrCoef = "mcc"
    Fp = "fp"
    Fn = "fn"
    Tn = "tn"
    Tp = "tp"
    Tpr = "tpr"
    Fpr = "fpr"
    Tnr = "tnr"
    MCC = "matthews-corr-coef"
    ExplainedVariance = "explained-variance"
    MaxError = "max-error"
    MAE = "mae"
    MSE = "mse"
    MSLE = "msle"
    RMSE = "rmse"
    RMSLE = "rmsle"
    MedianAbsoluteError = "median-absolute-error"
    R2 = "r2"
    AdjR2 = "adj-r2"
    MeanPoissonDeviance = "mean_poisson_deviance"
    MeanGammaDeviance = "mean-gamma-deviance"
    MeanTweedieDeviance = "mean-tweedie-deviance"
    MAPE = "mape"
    MAZE = "maze"
    MDAPE = "mdape"
    SMAPE = "smape"
    AdjustedMutualInfoScore = "adjusted-mutual-info-score"
    AdjustedRandScore = "adjusted-rand-score"
    CompletenessScore = "completeness-score"
    FowlkesMallowsScore = "fowlkes-mallows-score"
    HomogeneityScore = "homogeneity-score"
    MutualInfoScore = "mutual-info-score"
    NormalizedMutualInfoScore = "normalized-mutual-info-score"
    VMeasureScore = "v-measure-score"
    P50Latency = "p50-latency"
    P95Latency = "p95-latency"
    P99Latency = "p99-latency"
    Cpu = "cpu"
    Gpu = "gpu"
    Mem = "mem"
    GpuMem = "gpu-mem"
    ReqSec = "req-per-sec"
    UncrainPredictionPercent = "uncertain-prediction-percent"
    Null = "none"


@datamodel(proto=ObjectReference)
class ObjectReference(Configuration):
    """
    An Object Reference defines the location of a resource on the current operational cluster, denoted by the namespace
    of the resource and the name of the resource which exists on that namespace.
    """

    Namespace: str = ""
    Name: str = ""


@datamodel(proto=SecretReference)
class SecretReference(Configuration):
    Name: str = ""
    Namespace: str = ""


@datamodel(proto=Plot)
class Plot(ImmutableConfiguration):
    Fname: str = ""
    Img: bytes = ""
    Name: str = ""
    Title: str = ""
    Url: str = ""


@datamodel(proto=catalog_pb.Measurement)
class Measurement(ImmutableConfiguration):
    """ Measurement is a value for a specific metric """
    Entity: ObjectReference = None
    Column: str = ''
    Metric: Metric = Metric.Null
    """ The metric type name (e.g. F1 / Accuracy) """
    Value: float = 0
    """ The value of the metric """
    Stddev: float = 0
    BoolQty: bool = False
    Category: str = ''
    ValueSet: List[str] = field(default_factory=lambda: [])
    TimePoint: Time = None


##########################################
# Test classes
##########################################

@datamodel(proto=TestSuite)
class TestSuite(Configuration):
    Enabled: bool = False
    Tests: List[DataTestCase] = field(default_factory=lambda: [])


TestMetric = Metric


@datamodel(proto=DataTestCase)
class DataTestCase(Configuration):
    Enabled: bool = True
    AssertThat: AssertionType = AssertionType.NoneAssertion
    Metric: TestMetric = TestMetric.Null
    ExpectedSet: List[str] = field(default_factory=lambda: [])
    Generated: bool = False
    Tags: List[str] = field(default_factory=lambda: [])
    Name: str = ''
    EntityRef: ObjectReference = None
    CompareToRef: ObjectReference = None
    Column: str = ''
    Type: DataTestType = DataTestType.Column
    ExpectedValue: float = 0
    ExpectedCategory: str = ''
    Lower: float = 0
    Upper: float = 0
    LowerInclusive: bool = False
    UpperInclusive: bool = False
    Column2: str = ''
    EntityRef2: ObjectReference = None
    Columns: List[str] = ''
    FeatureFilter: FeatureFilterType = FeatureFilterType.AllFeatures
    ReferenceType: ReferenceDataType = ReferenceDataType.TrainingData
    Periods: int = 0


@datamodel(proto=TestSuiteResult)
class TestSuiteResult(Configuration):
    Failures: int = 0
    Errors: int = 0
    StartTime: Time = None
    StopTime: Time = None
    Tests: List[DataTestCaseResult] = field(default_factory=lambda: [])


@datamodel(proto=DataTestCaseResult)
class TestCaseResult(Configuration):
    Name: str = ''
    Actual: Measurement = Measurement()
    Failure: bool = False
    Error: bool = False
    FailureMsg: str = ""


@datamodel(proto=HistogramData)
class HistogramData(Configuration):
    Bins: List[float] = field(default_factory=lambda: [])
    Categories: List[str] = field(default_factory=lambda: [])
    Counts: List[float] = field(default_factory=lambda: [])
    Missing: int = 0
    Invalid: int = 0


@datamodel(proto=Histogram)
class Histogram(Configuration):
    Values: List[float] = field(default_factory=lambda: [])
    Categories: List[str] = field(default_factory=lambda: [])
    Bins: List[float] = field(default_factory=lambda: [])

