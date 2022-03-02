from abc import ABC

from github.com.metaprov.modelaapi.services.common.v1.common_pb2 import ColumnProfile as MDColumnProfile
from modela.data.common import *
from modela.infra.models import Workload, NotificationSetting, OutputLogs, GitSettings, ImageLocation
from modela.training.common import *
from modela.common import *
from modela.Configuration import *
from dataclasses import dataclass, field
from typing import List
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Column as MDColumn
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import \
    MultiDatasetValidation as MDMultiDatasetValidation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DatasetValidation as MDDatasetValidation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import \
    MultiColumnValidation as MDMultiColumnValidation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import ColumnValidation as MDColumnValidation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import FileValidation as MDFileValidation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataSourceSpec as MDDataSourceSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RelationshipSpec as MDRelationshipSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Recipe as MDRecipe
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RecipeSpec as MDRecipeSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RecipeStep as MDRecipeStep
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RecipeStepParam as MDRecipeStepParam
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import SampleSpec as MDSampleSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RecipeInputSpec as MDRecipeInputSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import RecipeOutputSpec as MDRecipeOutputSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Dataset as MDDataset
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DatasetSpec as MDDatasetSpec
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DatasetStatistics as MDDatasetStatistics
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DatasetCondition as MDDatasetCondition
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import ColumnStatistics as MDColumnStatistics
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DatasetTemplate as MDDatasetTemplate
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataLocation as MDDataLocation

from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import \
    DataValidationResult as MDDataValidationResult
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Correlation as MDCorrelation
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import CorrelationSpec as MDCorrelationSpec

from modela.util import TrackedList


@dataclass
class DataLocation(Configuration):
    Type: DataLocationType = DataLocationType.ObjectStorage
    ConnectionName: str = ""
    BucketName: str = ""
    Path: str = ""
    Table: str = ""
    Database: str = ""
    Sql: str = ""
    Topic: str = ""

    def to_message(self) -> MDDataLocation:
        return self.set_parent(MDDataLocation()).parent


@dataclass
class SampleSettings(Configuration):
    Enabled: bool = False
    Type: SamplingType = SamplingType.Random
    Rows: int = 500
    Percent: int = 100
    Filter: str = ""
    Column: str = ""

    def to_message(self) -> MDSampleSpec:
        return self.set_parent(MDSampleSpec()).parent


@dataclass
class GovernanceSpec(Configuration):
    Enabled: bool = False
    Country: str = ""
    ItReviewer: str = ""
    ComplianceReviewer: str = ""
    BusinessReviewer: str = ""


@dataclass
class CompilerSettings(Configuration):
    Enable: bool = False
    Compiler: CompilerType = CompilerType.Nothing
    Targets: List[HardwareTarget] = field(default_factory=lambda: [])


# Typename collision workaround
ColorType = Color
ImageLocationType = ImageLocation
DataLocationType = DataLocation


@dataclass
class DataProductSpec(Configuration):
    Owner: str = "no-one"
    TenantRef: ObjectReference = ObjectReference(Namespace="modela-system", Name="default-tenant")
    GitLocation: GitSettings = GitSettings()
    ImageLocation: ImageLocationType = ImageLocation()
    LabName: str = "default-lab"
    ServingSiteName: str = "default-servingsite"
    Task: TaskType = TaskType.BinaryClassification
    Description: str = ""
    DataLocation: DataLocationType = DataLocationType()
    Notification: NotificationSetting = NotificationSetting()
    Resources: Workload = Workload("general-large")
    RetriesOnFailure: int = 3
    OnCallAccountName: str = ""
    Compilation: CompilerSettings = CompilerSettings()
    ClearanceLevel: SecurityClearanceLevel = SecurityClearanceLevel.Unclassified
    Priority: PriorityLevel = PriorityLevel.Medium
    Color: ColorType = ColorType.NoColor
    Governance: GovernanceSpec = GovernanceSpec()


@dataclass
class DataProductVersionSpec(Configuration):
    ProductRef: ObjectReference = ObjectReference(Namespace="default-tenant", Name="iris-product")
    Description: str = ""
    PrevVersionName: str = ""
    Baseline: bool = False
    Owner: str = "no-one"


@dataclass
class CsvFileFormat(Configuration):
    """
    CsvFileFormat defines the file format of a raw CSV file.
    """
    ColumnDelimiter: Delimiter = Delimiter.Comma
    EscapeChar: EscapeCharacter = EscapeCharacter.DoubleQuote
    Quote: QuoteCharacter = QuoteCharacter.DoubleQuote
    CommentChars: str = "#"
    Header: bool = True
    SkipRows: int = 0
    NullValues: str = ""
    Encoding: FileEncoding = FileEncoding.Utf8
    MaxRows: int = 0
    Strict: bool = True
    Compression: CompressionType = CompressionType.Uncompressed
    HasIndexColumn: bool = False
    IndexColumn: int = 0


@dataclass
class ExcelSheetArea(Configuration):
    EntireSheet: bool = True
    FromColumn: int = 1
    ToColumn: int = 1
    FromRow: int = 1
    ToRow: int = 1


@dataclass
class ExcelNotebookFormat(Configuration):
    FirstSheetWithData: bool = False
    SheetName: str = ""
    SheetIndex: int = 0
    ColumnNameRow: int = 1
    Data: ExcelSheetArea = ExcelSheetArea()


@dataclass
class Column(Configuration):
    Name: str = ""
    Datatype: DataType = DataType.Categorical
    Format: DataDomain = DataDomain.Unknown
    DisplayName: str = ""
    Description: str = ""
    Ignore: bool = False
    Target: bool = False
    Nullable: bool = False
    Pk: bool = False
    Fk: bool = False
    MultipleOf: int = 0
    Maximum: int = 0
    ExclusiveMinimum: bool = False
    MaxLength: int = 0
    MinLength: int = 0
    Pattern: str = ""
    Required: bool = False
    Example: str = ""
    ExternalDocs: str = ""
    Enum: List[str] = field(default_factory=lambda: [])
    Ordinal: bool = False
    MaxItems: int = 0
    MinItems: int = 0
    UniqueItems: bool = False
    TimeColumn: bool = False
    Pii: bool = False
    Phi: bool = False
    PersonalData: bool = False
    Protected: bool = False
    DefaultValueNum: float = 0
    Log: bool = False
    Mu: float = 0
    Sigma: float = 0
    SkewThreshold: float = None
    DriftThreshold: float = None
    Index: bool = True
    Fold: bool = False
    Weight: bool = False
    Reserved: bool = False
    Imputation: Imputation = Imputation.AutoImputer
    Scaling: Scaling = Scaling.Auto
    Generated: bool = False
    Formula: str = ""
    Id: bool = False
    Step: float = 1

    def to_message(self) -> MDColumn:
        return self.set_parent(MDColumn()).parent


@dataclass
class TimeSeriesSchema(Configuration):
    Freq: Frequency = None
    Country: HolidayCountry = None


@dataclass
class RecommendationSchema(Configuration):
    UserIDColumn: str = "user_id"
    ItemIDColumn: str = "item_id"
    RatingColumn: str = "rating"


@dataclass
class MultiDatasetValidation(Configuration):
    Type: MultiDatasetValidationRule = None
    Datasets: List[str] = field(default_factory=lambda: [])
    Generated: bool = False

    def to_message(self) -> MDMultiDatasetValidation:
        return self.set_parent(MDMultiDatasetValidation()).parent


@dataclass
class DatasetValidation(Configuration):
    Type: DatasetValidationRule = None
    Value: float = 0
    Min: float = 0
    Max: float = 0
    ValueSet: List[str] = field(default_factory=lambda: [])
    StrictMin: bool = False
    StrictMax: bool = False
    Generated: bool = False

    def to_message(self) -> MDDatasetValidation:
        return self.set_parent(MDDatasetValidation()).parent


@dataclass
class MultiColumnValidation(Configuration):
    Type: MultiColumnValidationRule = None
    Columns: List[str] = field(default_factory=lambda: [])
    Value: float = 0
    Min: float = 0
    Max: float = 0
    ValueSet: List[str] = field(default_factory=lambda: [])
    StrictMin: bool = False
    StrictMax: bool = False
    Generated: bool = False

    def to_message(self) -> MDMultiColumnValidation:
        return self.set_parent(MDMultiColumnValidation()).parent


@dataclass
class ColumnValidation(Configuration):
    Type: ColumnValidationRule = None
    Column: str = ""
    Value: float = 0
    Min: float = 0
    Max: float = 0
    ValueSet: List[str] = field(default_factory=lambda: [])
    StrictMin: bool = False
    StrictMax: bool = False
    Generated: bool = False

    def to_message(self) -> MDColumnValidation:
        return self.set_parent(MDColumnValidation()).parent


@dataclass
class FileValidation(Configuration):
    Type: FileValidationRule = None
    BucketName: str = ""
    Column: str = ""
    Value: float = 0
    Min: float = 0
    Max: float = 0
    ValueSet: List[str] = field(default_factory=lambda: [])
    StrictMin: bool = False
    StrictMax: bool = False
    Generated: bool = False

    def to_message(self) -> MDFileValidation:
        return self.set_parent(MDFileValidation()).parent


@dataclass
class ValidationRules(Configuration):
    MultiDatasetValidations: List[MultiDatasetValidation] = field(default_factory=lambda: [])
    DatasetValidations: List[DatasetValidation] = field(default_factory=lambda: [])
    MultiColumnValidations: List[MultiColumnValidation] = field(default_factory=lambda: [])
    ColumnValidations: List[ColumnValidation] = field(default_factory=lambda: [])
    FileValidations: List[FileValidation] = field(default_factory=lambda: [])


MDTimeSeriesSchema = TimeSeriesSchema
MDRecommendationSchema = RecommendationSchema


@dataclass
class Schema(Configuration):
    Columns: List[Column] = field(default_factory=lambda: [])
    TimeSeriesSchema: MDTimeSeriesSchema = None
    RecommendationSchema: MDRecommendationSchema = None
    Validation: ValidationRules = ValidationRules()


@dataclass
class ColumnRelationship(Configuration):
    Type: str = None
    Column: str = None
    Arity: RelationshipArity = None
    RelatesTo: str = None

    def to_message(self) -> MDRelationshipSpec:
        return self.set_parent(MDRelationshipSpec()).parent


@dataclass
class CorrelationSetting(Configuration):
    Cutoff: float = 50
    Method: str = "pearson"
    Top: int = 10

    def to_message(self) -> MDCorrelationSpec:
        return self.set_parent(MDCorrelationSpec()).parent


DataSourceSchema = Schema  # workaround for type annotation bug


@dataclass
class DataSourceSpec(Configuration):
    Schema: DataSourceSchema = DataSourceSchema()
    Sample: SampleSettings = SampleSettings()
    Relationships: List[ColumnRelationship] = field(default_factory=lambda: [])
    Owner: str = "no-one"
    VersionName: str = "v0.0.1"
    Description: str = ""
    FileType: FlatFileType = FlatFileType.Csv
    Task: TaskType = TaskType.BinaryClassification
    Csvfile: CsvFileFormat = CsvFileFormat()
    ExcelNotebook: ExcelNotebookFormat = None
    DatasetType: DatasetType = DatasetType.Tabular


@dataclass
class DatasetSpec(Configuration):
    Origin: DataLocation = DataLocation()
    Location: DataLocation = DataLocation()
    Owner: str = "no-one"
    VersionName: str = "v0.0.1"
    DatasourceName: str = ""
    Description: str = ""
    DisplayName: str = ""
    Reported: bool = False
    Snapshotted: bool = False
    Validate: bool = True
    Labeled: bool = True
    Syntactic: bool = False
    SyntacticRows: int = 0
    Resources: Workload = None
    ActiveDeadlineSeconds: int = 600
    Type: DatasetType = DatasetType.Tabular
    Sample: SampleSettings = None
    Task: TaskType = None
    Notification: NotificationSetting = None
    Correlation: CorrelationSetting = None


@dataclass
class ColumnStatistics(Configuration):
    Name: str = ""
    Datatype: DataType = None
    Count: float = 0
    Distinct: int = 0
    Missing: int = 0
    PercentMissing: float = 0
    Mean: float = 0
    Stddev: float = 0
    Variance: float = 0
    Min: float = 0
    Max: float = 0
    Kurtosis: float = 0
    Skewness: float = 0
    Sum: float = 0
    Mad: float = 0
    P25: float = 0
    P50: float = 0
    P75: float = 0
    Iqr: float = 0
    Mode: str = ""
    Zeros: float = 0
    Invalid: int = 0
    Importance: float = 0
    Target: bool = False
    Ignore: bool = False
    Nullable: bool = False
    HighCardinality: bool = False
    HighCorrWithOtherFeatures: bool = False
    LowCorrWithTarget: bool = False
    HighMissingPct: bool = False
    Skewed: bool = False
    Id: bool = False
    Constant: bool = False
    Duplicate: bool = False
    Reserved: bool = False
    Outliers: int = 0
    Completeness: float = 0
    DistinctValueCount: float = 0
    MostFreqValuesRatio: float = 0
    IndexOfPeculiarity: float = 0
    CorrToTarget: float = 0

    def to_message(self) -> MDColumnStatistics:
        return self.set_parent(MDColumnStatistics()).parent


@dataclass
class ColumnProfile(Configuration):
    Name: str = ""
    Count: int = 0
    Type: str = 0
    Missing: int = 0
    PercentMissing: float = 0
    Distinct: int = 0
    Mean: float = 0
    Mode: str = ""
    Stddev: float = 0
    Variance: float = 0
    Min: float = 0
    Max: float = 0
    Kurtosis: float = 0
    Skewness: float = 0
    Sum: float = 0
    Mad: float = 0
    Zeros: float = 0
    P25: float = 0
    P50: float = 0
    P75: float = 0
    P100: float = 0
    Iqr: float = 0
    Cv: float = 0
    Top: int = 0
    Freq: int = 0
    Ignore: bool = False
    Target: bool = False
    Invalid: int = 0
    Importance: float = 0
    Nullable: bool = False
    HighCardinality: bool = False
    HighCorrWithOtherFeatures: bool = False
    LowCorrWithTarget: bool = False
    HighMissingPct: bool = False
    Skewed: bool = False
    Id: bool = False
    Constant: bool = False
    Duplicate: bool = False
    Reserved: bool = False
    Outliers: int = 0
    Completeness: float = 0
    DistinctValueCount: float = 0
    MostFreqValuesRatio: float = 0
    IndexOfPeculiarity: float = 0
    Values: List[str] = field(default_factory=lambda: [])
    CorrToTarget: float = 0



@dataclass
class Correlation(Configuration):
    Feature1: str = ""
    Feature2: str = ""
    Value: float = 0
    Method: str = ""

    def to_message(self) -> MDCorrelation:
        return self.set_parent(MDCorrelation()).parent


@dataclass
class DatasetStatistics(Configuration):
    Columns: List[ColumnStatistics] = field(default_factory=lambda: [])
    Rows: int = 0
    Cols: int = 0
    FileSize: int = 0
    CorrelationsWithTarget: List[Correlation] = field(default_factory=lambda: [])
    TopCorrelations: List[Correlation] = field(default_factory=lambda: [])

    def to_message(self) -> MDDatasetStatistics:
        return self.set_parent(MDDatasetStatistics()).parent


@dataclass
class DatasetCondition(Configuration):
    Type: DatasetCondition = DatasetCondition.Ready
    Status: ConditionStatus = ConditionStatus.ConditionUnknown
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""

    def to_message(self) -> MDDatasetCondition:
        return self.set_parent(MDDatasetCondition()).parent


@dataclass
class DataValidationResult(Configuration):
    Type: str = ""
    Column: str = ""
    Error: str = ""
    Passed: bool = False

    def to_message(self) -> MDDataValidationResult:
        return self.set_parent(MDDataValidationResult()).parent


@dataclass
class DatasetStatus(ImmutableConfiguration):
    Statistics: DatasetStatistics = None
    Phase: DatasetPhase = DatasetPhase.Pending
    ReportName: str = ""
    ReportUri: str = ""
    ProfileUri: str = ""
    Imbalanced: bool = False
    ObservedGeneration: int = 0
    ValidationResults: List[DataValidationResult] = field(default_factory=lambda: [])
    LastStudyTime: Time = None
    LastNotificationTime: Time = None
    FailureReason: StatusError = None
    FailureMessage: str = ""
    Progress: int = 0
    Hash: str = ""
    Logs: OutputLogs = OutputLogs()
    DerivedFromDataset: str = ""
    LastUpdated: Time = None
    Conditions: List[DatasetCondition] = field(default_factory=lambda: [])
