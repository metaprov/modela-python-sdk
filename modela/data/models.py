from modela.data.common import *
from modela.training.common import *
from modela.common import *
from modela.Resource import *
from dataclasses import dataclass, field
from typing import List
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Column as MDColumn

from modela.util import TrackedList


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
        self._parent = MDColumn()
        return self.apply_config(self._parent)

    def __post_init__(self):
        self.Enum = TrackedList(self.Enum, self, "Enum")


@dataclass
class Schema(Configuration):
    Columns: List[Column]

    def __post_init__(self):
        self.Columns = TrackedList(self.Columns, self, "Columns")
