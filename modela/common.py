from dataclasses import dataclass
from enum import Enum
from typing import List
from dataclasses import dataclass, field

from github.com.metaprov.modelaapi.services.common.v1.common_pb2 import Plot
from k8s.io.api.core.v1.generated_pb2 import ObjectReference, SecretReference
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import Time

from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import TestSuite, TestCase, TestSuiteResult, \
    TestCaseResult

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
    CompileTask = "compile-model"
    PackageModelTask = "package-model"
    FeatureGenTask = "feature-gen"
    FeatureSelectTask = "feature-select"
    RunSqlQueryTask = "run-sql-query"
    RunWebRequestTask = "run-web-request"
    GenerateDataset = "generate-dataset"
    ValidateModel = "validate-model"


class StatusError(Enum):
    InvalidConfiguration = "InvalidConfiguration"
    InsufficientResources = "InsufficientResources"
    CreateError = "CreateError"
    UpdateError = "UpdateError"
    DeleteError = "DeleteError"


class TestCaseName(Enum):
    MultiDatasetSameNumberOfRows = "MultiDatasetSameNumberOfRows"
    MultiDatasetOuterJoinEmpty = "MultiDatasetOuterJoinEmpty"
    MultiDatasetOuterJoinNotEmpty = "MultiDatasetOuterJoinNotEmpty"
    MultiDatasetInnerJoinEmpty = "MultiDatasetInnerJoinEmpty"
    MultiDatasetInnerJoinNotEmpty = "MultiDatasetInnerJoinNotEmpty"
    MultiDatasetLeftJoinEmpty = "MultiDatasetLeftJoinEmpty"
    MultiDatasetLeftJoinNotEmpty = "MultiDatasetLeftJoinNotEmpty"
    MultiDatasetRightJoinEmpty = "MultiDatasetRightJoinEmpty"
    MultiDatasetRightJoinNotEmpty = "MultiDatasetRightJoinNotEmpty"
    DatasetColumnsCountEqual = "DatasetColumnsCountEqual"
    DatasetColumnsNameInSet = "DatasetColumnsNameInSet"
    DatasetColumnsInOrderedList = "DatasetColumnsInOrderedList"
    DatasetRowCountBetween = "DatasetRowCountBetween"
    DatasetNotEmpty = "DatasetNotEmpty"
    DatasetTestNameNameEmpty = "DatasetTestNameNameEmpty"
    MultiColumnCorr = "MultiColumnCorr"
    ColumnTestNameColumnExist = "ColumnTestNameColumnExist"
    ColumnHaveValues = "ColumnHaveValues"
    ColumnHasNoValue = "ColumnHasNoValue"
    ColumnHaveNulls = "ColumnHaveNulls"
    ColumnHasNoNull = "ColumnHasNoNull"
    ColumnOfType = "ColumnOfType"
    ColumnValuesInSet = "ColumnValuesInSet"
    ColumnValuesIncreasing = "ColumnValuesIncreasing"
    ColumnsValuesDecreasing = "ColumnsValuesDecreasing"
    ColumnValueLengthBetween = "ColumnValueLengthBetween"
    ColumnValueNameMatchRegex = "ColumnValueNameMatchRegex"
    ColumnValueIsDate = "ColumnValueIsDate"
    ColumnValueIsJson = "ColumnValueIsJson"
    ColumnValueInDomain = "ColumnValueInDomain"
    ColumnUniqueValueCountBetween = "ColumnUniqueValueCountBetween"
    ColumnOutlierValueUniqueBetween = "ColumnOutlierValueUniqueBetween"
    ColumnValidValueUniqueBetween = "ColumnValidValueUniqueBetween"
    ColumnMismatchValueBetween = "ColumnMismatchValueBetween"
    ColumnValueMinBetween = "ColumnValueMinBetween"
    ColumnValueLowerQuartileBetween = "ColumnValueLowerQuartileBetween"
    ColumnValueMedianBetween = "ColumnValueMedianBetween"
    ColumnValueAvgBetween = "ColumnValueAvgBetween"
    ColumnValueUpperQuartileBetween = "ColumnValueUpperQuartileBetween"
    ColumnValueMaxBetween = "ColumnValueMaxBetween"
    ColumnValueStddevBetween = "ColumnValueStddevBetween"
    ColumnValueChiSquarePValueBetween = "ColumnValueChiSquarePValueBetween"
    ColumnValuePairCramersBetween = "ColumnValuePairCramersBetween"
    FileSizeBetween = "FileSizeBetween"
    FileExist = "FileExist"
    FileRegexMatchCountBetween = "FileRegexMatchCountBetween"
    FileValidJson = "FileValidJson"
    FileValidCsv = "FileValidCsv"

    # Model Tests
    ModelAccuracy = "ModelAccuracy"
    ModelRocAuc = "ModelRocAuc"
    ModelF1 = "ModelF1"
    ModelPrecision = "ModelPrecision"
    ModelRecall = "ModelRecall"
    ModelMSE = "ModelMSE"
    ModelRMSE = "ModelRMSE"
    ModelMAPE = "ModelMAPE"


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


@datamodel(proto=TestSuite)
class TestSuite(Configuration):
    Tests: List[TestCase] = field(default_factory=lambda: [])


@datamodel(proto=TestCase)
class TestCase(Configuration):
    Name: TestCaseName
    Metric: Metric
    Column: str
    Value: float
    Min: float
    Max: float
    StrictMin: bool
    StrictMax: bool
    Generated: bool
    BucketName: str
    Path: str


@datamodel(proto=TestSuiteResult)
class TestSuiteResult(Configuration):
    Failures: int
    Success: int
    Started: Time
    Ended: Time
    Tests: List[TestCaseResult]


@datamodel(proto=TestCaseResult)
class TestSuiteResult(Configuration):
    Name: TestCaseName
    Metric: Metric
    Column: str
    Failed: bool
    TotalValues: int
    FailedValues: int
    SampleFailedValues: str
