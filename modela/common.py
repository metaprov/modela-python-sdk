from dataclasses import dataclass
from enum import Enum

from modela.Configuration import Configuration, ImmutableConfiguration


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


@dataclass
class Time(Configuration):
    Seconds: int = 0
    Nanos: int = 0


@dataclass
class ObjectReference(Configuration):
    """
    An Object Reference defines the location of a resource on the current operational cluster, denoted by the namespace
    of the resource and the name of the resource which exists on that namespace.
    """

    Namespace: str = ""
    Name: str = ""


@dataclass
class SecretReference(Configuration):
    Name: str = ""
    Namespace: str = ""

@dataclass
class Plot(ImmutableConfiguration):
    Fname: str = ""
    Img: bytes = ""
    Name: str = ""
    Title: str = ""
    Url: str = ""

