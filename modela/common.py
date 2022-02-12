from enum import Enum

from modela.Configuration import Configuration


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


class Time(Configuration):
    Seconds: int = 0
    Nanos: int = 0
