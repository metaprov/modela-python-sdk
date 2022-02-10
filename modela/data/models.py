from abc import ABC

from modela.data.common import *
from modela.training.common import *
from modela.common import *
from modela.Resource import *
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

from modela.util import TrackedList


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
    Datatype: DataType = DataType.Categorical
    Format: DataDomain = DataDomain.Unknown
    Name: str = ""
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

    def __post_init__(self):
        self.Enum = TrackedList(self.Enum, self, "Enum")


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

    def __post_init__(self):
        self.Datasets = TrackedList(self.Datasets, self, "Datasets")


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

    def __post_init__(self):
        self.ValueSet = TrackedList(self.ValueSet, self, "ValueSet")


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

    def __post_init__(self):
        self.Columns = TrackedList(self.Columns, self, "Columns")
        self.ValueSet = TrackedList(self.ValueSet, self, "ValueSet")


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

    def __post_init__(self):
        self.ValueSet = TrackedList(self.ValueSet, self, "ValueSet")


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

    def __post_init__(self):
        self.ValueSet = TrackedList(self.ValueSet, self, "ValueSet")


@dataclass
class ValidationRules(Configuration):
    MultiDatasetValidations: List[MultiDatasetValidation] = field(default_factory=lambda: [])
    DatasetValidations: List[DatasetValidation] = field(default_factory=lambda: [])
    MultiColumnValidations: List[MultiColumnValidation] = field(default_factory=lambda: [])
    ColumnValidations: List[ColumnValidation] = field(default_factory=lambda: [])
    FileValidations: List[FileValidation] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.MultiDatasetValidations = TrackedList(self.MultiDatasetValidations, self, "MultiDatasetValidations")
        self.DatasetValidations = TrackedList(self.DatasetValidations, self, "DatasetValidations")
        self.MultiColumnValidations = TrackedList(self.MultiColumnValidations, self, "MultiColumnValidations")
        self.ColumnValidations = TrackedList(self.ColumnValidation, self, "ColumnValidations")
        self.FileValidations = TrackedList(self.FileValidation, self, "FileValidations")


MDTimeSeriesSchema = TimeSeriesSchema
MDRecommendationSchema = RecommendationSchema


@dataclass
class Schema(Configuration):
    Columns: List[Column] = field(default_factory=lambda: [])
    TimeSeriesSchema: MDTimeSeriesSchema = None
    RecommendationSchema: MDRecommendationSchema = None
    Validation: ValidationRules = None

    def __post_init__(self):
        self.Columns = TrackedList(self.Columns, self, "Columns")


@dataclass
class ColumnRelationship(Configuration):
    Type: str = None
    Column: str = None
    Arity: RelationshipArity = None
    RelatesTo: str = None

    def to_message(self) -> MDRelationshipSpec:
        return self.set_parent(MDRelationshipSpec()).parent


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
    Csvfile: CsvFileFormat = CsvFileFormat()
    ExcelNotebook: ExcelNotebookFormat = None
    DatasetType: DatasetType = DatasetType.Tabular

    def __post_init__(self):
        self.Relationships = TrackedList(self.Relationships, self, "Relationships")
