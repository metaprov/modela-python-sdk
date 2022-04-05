from abc import ABC
import modela.data.common as data_common
from modela.data.common import *
from modela.infra.Account import Account
from modela.infra.UserRoleClass import UserRoleClass
from modela.infra.models import Workload, NotificationSetting, OutputLogs, GitSettings, ImageLocation
from modela.training.common import *
from modela.common import *
from modela.Configuration import *
from dataclasses import field
from typing import List, Union
from github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 import CompilerSpec, Stakeholder, \
    PermissionsSpec
import github.com.metaprov.modelaapi.pkg.apis.catalog.v1alpha1.generated_pb2 as catalog_pb
import github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 as data_pb
import github.com.metaprov.modelaapi.services.common.v1.common_pb2 as common_pb
from modela.common import Plot
from modela.util import TrackedList

@datamodel(proto=data_pb.DataLocation)
class DataLocation(Configuration):
    Type: DataLocationType = DataLocationType.ObjectStorage
    ConnectionName: str = ""
    BucketName: str = ""
    Path: str = ""
    Table: str = ""
    Database: str = ""
    Sql: str = ""
    Topic: str = ""


@datamodel(proto=data_pb.SampleSpec)
class SampleSettings(Configuration):
    Enabled: bool = False
    Type: SamplingType = SamplingType.Random
    Rows: int = 500
    Percent: int = 100
    Filter: str = ""
    Column: str = ""

@datamodel(proto=data_pb.GovernanceSpec)
class GovernanceSpec(Configuration):
    Enabled: bool = False
    Country: str = ""
    ItReviewer: str = ""
    ComplianceReviewer: str = ""
    BusinessReviewer: str = ""


@datamodel(proto=catalog_pb.CompilerSpec)
class CompilerSettings(Configuration):
    Enable: bool = False
    Compiler: CompilerType = CompilerType.Nothing
    Targets: List[HardwareTarget] = field(default_factory=lambda: [])

# Typename collision workaround
ColorType = Color
ImageLocationType = ImageLocation
DataLocationType = DataLocation


@datamodel(proto=catalog_pb.Stakeholder)
class Stakeholder(Configuration):
    Account: str
    Roles: List[ObjectReference] = field(default_factory=lambda: [])


@datamodel(proto=catalog_pb.PermissionsSpec)
class PermissionsSpec(Configuration):
    Stakeholders: List[Stakeholder] = field(default_factory=lambda: [])

    @classmethod
    def create(cls, accounts: dict[Union[Account, str], Union[UserRoleClass, str]]) -> PermissionsSpec:
        """ Generate a permission specification based on a dictionary of Accounts and their User Role Classes """
        stakeholders = []
        for account, role in accounts.items():
            if type(account) == Account:
                account = account.name

            if type(role) == UserRoleClass:
                role = role.name

            stakeholders.append(Stakeholder(Account=account, Roles=role))

        return cls(Stakeholders=stakeholders)


@datamodel(proto=data_pb.DataProductSpec)
class DataProductSpec(Configuration):
    Owner: str = "no-one"
    TenantRef: ObjectReference = ObjectReference(Namespace="modela-system", Name="default-tenant")
    GitLocation: GitSettings = GitSettings()
    ImageLocation: ImageLocationType = ImageLocation()
    LabName: str = "default-lab"
    ServingSiteName: str = "default-serving-site"
    Task: TaskType = TaskType.BinaryClassification
    Description: str = ""
    DataLocation: DataLocationType = DataLocationType()
    Notification: NotificationSetting = NotificationSetting()
    TrainingResources: Workload = Workload("general-large")
    ServingResources: Workload = Workload("general-large")
    RetriesOnFailure: int = 3
    OnCallAccountName: str = ""
    Compilation: CompilerSettings = CompilerSettings()
    ClearanceLevel: SecurityClearanceLevel = SecurityClearanceLevel.Unclassified
    Priority: PriorityLevel = PriorityLevel.Medium
    Color: ColorType = ColorType.NoColor
    Governance: GovernanceSpec = GovernanceSpec()
    Public: bool = False
    Permissions: PermissionsSpec = PermissionsSpec()



@datamodel(proto=data_pb.DataProductVersionSpec)
class DataProductVersionSpec(Configuration):
    ProductRef: ObjectReference = ObjectReference(Namespace="default-tenant", Name="iris-product")
    Description: str = ""
    PrevVersionName: str = ""
    Baseline: bool = False
    Owner: str = "no-one"


@datamodel(proto=data_pb.CsvFileSpec)
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


@datamodel(proto=data_pb.ExcelSheetArea)
class ExcelSheetArea(Configuration):
    EntireSheet: bool = True
    FromColumn: int = 1
    ToColumn: int = 1
    FromRow: int = 1
    ToRow: int = 1


@datamodel(proto=data_pb.ExcelNotebookSpec)
class ExcelNotebookFormat(Configuration):
    FirstSheetWithData: bool = False
    SheetName: str = ""
    SheetIndex: int = 0
    ColumnNameRow: int = 1
    Data: ExcelSheetArea = ExcelSheetArea()


@datamodel(proto=data_pb.Column)
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


@datamodel(proto=data_pb.TimeSeriesSchema)
class TimeSeriesSchema(Configuration):
    Freq: Frequency = None
    Country: HolidayCountry = None


@datamodel(proto=data_pb.RecommendationSchema)
class RecommendationSchema(Configuration):
    UserIDColumn: str = "user_id"
    ItemIDColumn: str = "item_id"
    RatingColumn: str = "rating"


@datamodel(proto=data_pb.MultiDatasetValidation)
class MultiDatasetValidation(Configuration):
    Type: MultiDatasetValidationRule = None
    Datasets: List[str] = field(default_factory=lambda: [])
    Generated: bool = False


@datamodel(proto=data_pb.DatasetValidation)
class DatasetValidation(Configuration):
    Type: DatasetValidationRule = None
    Value: float = 0
    Min: float = 0
    Max: float = 0
    ValueSet: List[str] = field(default_factory=lambda: [])
    StrictMin: bool = False
    StrictMax: bool = False
    Generated: bool = False


@datamodel(proto=data_pb.MultiColumnValidation)
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


@datamodel(proto=data_pb.ColumnValidation)
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


@datamodel(proto=data_pb.FileValidation)
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


@datamodel(proto=data_pb.ValidationSpec)
class ValidationRules(Configuration):
    MultiDatasetValidations: List[MultiDatasetValidation] = field(default_factory=lambda: [])
    DatasetValidations: List[DatasetValidation] = field(default_factory=lambda: [])
    MultiColumnValidations: List[MultiColumnValidation] = field(default_factory=lambda: [])
    ColumnValidations: List[ColumnValidation] = field(default_factory=lambda: [])
    FileValidations: List[FileValidation] = field(default_factory=lambda: [])


MDTimeSeriesSchema = TimeSeriesSchema
MDRecommendationSchema = RecommendationSchema

@datamodel(proto=data_pb.Schema)
class Schema(Configuration):
    Columns: List[Column] = field(default_factory=lambda: [])
    TimeSeriesSchema: MDTimeSeriesSchema = None
    RecommendationSchema: MDRecommendationSchema = None
    Validation: ValidationRules = ValidationRules()


@datamodel(proto=data_pb.RelationshipSpec)
class ColumnRelationship(Configuration):
    Type: str = None
    Column: str = None
    Arity: RelationshipArity = None
    RelatesTo: str = None


@datamodel(proto=data_pb.CorrelationSpec)
class CorrelationSetting(Configuration):
    Cutoff: float = 50
    Method: str = "pearson"
    Top: int = 10

DataSourceSchema = Schema  # workaround for type annotation bug


@datamodel(proto=data_pb.DataSourceSpec)
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


@datamodel(proto=data_pb.DatasetSpec)
class DatasetSpec(Configuration):
    Origin: DataLocation = DataLocation()
    Location: DataLocation = DataLocation()
    Owner: str = "no-one"
    VersionName: str = "v0.0.1"
    DatasourceName: str = ""
    Description: str = ""
    DisplayName: str = ""
    Reported: bool = True
    Snapshotted: bool = False
    Validate: bool = True
    Labeled: bool = True
    Synthetic: bool = False
    SyntheticRows: int = 0
    Resources: Workload = None
    ActiveDeadlineSeconds: int = 600
    Type: DatasetType = DatasetType.Tabular
    Sample: SampleSettings = None
    Task: TaskType = None
    Notification: NotificationSetting = None
    Correlation: CorrelationSetting = None
    Fast: bool = False


@datamodel(proto=data_pb.ColumnStatistics)
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


@datamodel(proto=common_pb.ColumnProfile)
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


@datamodel(proto=common_pb.DatasetProfile)
class DatasetProfile(Configuration):
    Cols: int = 0
    Rows: int = 0
    Filesize: int = 0
    Imbalance: bool = False
    Plots: List[Plot] = field(default_factory=lambda: [])
    Columns: List[ColumnProfile] = field(default_factory=lambda: [])
    Hash: str = ""


@datamodel(proto=data_pb.Correlation)
class Correlation(Configuration):
    Feature1: str = ""
    Feature2: str = ""
    Value: float = 0
    Method: str = ""


@datamodel(proto=data_pb.DatasetStatistics)
class DatasetStatistics(Configuration):
    Columns: List[ColumnStatistics] = field(default_factory=lambda: [])
    Rows: int = 0
    Cols: int = 0
    FileSize: int = 0
    CorrelationsWithTarget: List[Correlation] = field(default_factory=lambda: [])
    TopCorrelations: List[Correlation] = field(default_factory=lambda: [])


@datamodel(proto=data_pb.DatasetCondition)
class DatasetCondition(Configuration):
    Type: data_common.DatasetCondition = data_common.DatasetCondition.Ready
    Status: ConditionStatus = ConditionStatus.ConditionUnknown
    LastTransitionTime: Time = None
    Reason: str = ""
    Message: str = ""


@datamodel(proto=data_pb.DataValidationResult)
class DataValidationResult(Configuration):
    Type: str = ""
    Column: str = ""
    Error: str = ""
    Passed: bool = False


@datamodel(proto=data_pb.DatasetStatus)
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
    FailureReason: StatusError = None
    FailureMessage: str = ""
    Progress: int = 0
    Hash: str = ""
    Logs: OutputLogs = OutputLogs()
    DerivedFromDataset: str = ""
    LastUpdated: Time = None
    StartTime: Time = None
    EndTime: Time = None
    Conditions: List[DatasetCondition] = field(default_factory=lambda: [])
