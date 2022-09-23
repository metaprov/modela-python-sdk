from enum import Enum


class CompilerType(Enum):
    TVM = "tvm"
    Onyx = "onyx"
    Xla = "xla"
    Nothing = "none"


class FileEncoding(Enum):
    Utf8 = "utf-8"
    Lating1 = "latin-1"
    Utf16 = "utf-16"


class Delimiter(Enum):
    CRLF = "crlf"
    CR = "cr"
    LF = "lf"
    Semicolon = "semicolon"
    Colon = "colon"
    Comma = "comma"
    Tab = "tab"
    Space = "space"
    Pipe = "pipe"


class EscapeCharacter(Enum):
    SingleQuote = "single-quote"
    DoubleQuote = "double-quote"
    Tilda = "tilda"
    NoneChar = "none"


class QuoteCharacter(Enum):
    SingleQuote = "single-quote"
    DoubleQuote = "double-quote"


class CompressionType(Enum):
    Tar = "tar"
    Gzip = "gzip"
    Zip = "zip"
    Uncompressed = "none"


class FlatFileType(Enum):
    Csv = "csv"
    Table = "tsv"
    Excel = "excel"
    Fwf = "fwf"
    Hdf5 = "hdf"
    Html = "html"
    Json = "json"
    Pickle = "pickle"
    Sas = "sas"
    Stata = "stata"
    Feather = "feather"
    Parquet = "parquet"


class DataType(Enum):
    Boolean = "boolean"
    DateTime = "datetime"
    Number = "number"
    Categorical = "categorical"
    Ordinal = "ordinal"
    Text = "text"
    Json = "json"
    NumberList = "number-list"
    CategoricalList = "categorical-list"
    TextList = "text-list"


class DataDomain(Enum):
    Url = "url"
    Path = "path"
    Password = "password"
    Time = "time"
    Count = "count"
    Interval = "interval"
    Nominal = "nominal"
    Email = "email"
    CreditCard = "creditCard"
    Uuid3 = "uuid"
    Uuid5 = "uuid5"
    Uuid = "uuid"
    Base64 = "base64"
    Latitude = "latitude"
    Longtitude = "longtitude"
    DnsName = "dns"
    Ip4 = "ip4"
    Ip6 = "ip6"
    Ssn = "ssn"
    Alpha = "alpha"
    AlphaNumeric = "alphanumeric"
    Unknown = "unknown"
    Color = "color"
    Currency = "currency"
    Date = "date"
    Guid = "guid"
    Hyperlink = "hyperlink"
    Image = "image"
    Media = "media"
    File = "file"
    Embedding = "embedding"
    Record = "record"
    Useless = "useless"
    Nothing = "none"


class SamplingType(Enum):
    Header = "header"
    Random = "random"
    Filter = "filter"
    Anomaly = "anomaly"
    Stratified = "stratified"


class DataLocationType(Enum):
    ObjectStorage = "object"
    SQLTable = "table"
    SQLView = "view"
    Stream = "stream"
    WebApi = "web"
    PublicDataset = "public-dataset"
    Dataset = "dataset"


class DatasetCondition(Enum):
    Reported = "Reported"
    Validated = "Validated"
    Snapshotted = "Snapshotted"
    Profiled = "Profiled"
    Ingested = "Ingested"
    Generated = "Generated"
    Saved = "Saved"
    Archived = "Archived"
    Ready = "Ready"


class DatasetPhase(Enum):
    Pending = "Pending"
    Generating = "Generating"
    GenSuccess = "GenSuccess"
    IngestRunning = "Ingesting"
    IngestSuccess = "Ingested"
    ReportRunning = "Reporting"
    ReportSuccess = "Reported"
    ProfileRunning = "Profiling"
    ProfileSuccess = "Profiled"
    ValidationRunning = "Validating"
    ValidationSuccess = "Validated"
    SnapshotRunning = "TakingSnapshot"
    SnapshotSuccess = "Snapshotted"
    Failed = "Failed"
    Aborted = "Aborted"
    Ready = "Ready"


class Color(Enum):
    Aliceblue = "aliceblue"
    Antiquewhite = "antiquewhite"
    Aqua = "aqua"
    Aquamarine = "aquamarine"
    Azure = "azure"
    Beige = "beige"
    Bisque = "bisque"
    Black = "black"
    Blanchedalmond = "blanchedalmond"
    Blue = "blue"
    Blueviolet = "blueviolet"
    Brown = "brown"
    Burlywood = "burlywood"
    Cadetblue = "cadetblue"
    Chartreuse = "chartreuse"
    Chocolate = "chocolate"
    Coral = "coral"
    Cornflowerblue = "cornflowerblue"
    Cornsilk = "cornsilk"
    NoColor = "none"


class SecurityClearanceLevel(Enum):
    Unclassified = "unclassified"
    Confidential = "confidential"
    Secret = "secret"
    TopSecret = "top-secret"


class DatasetRole(Enum):
    Unlabeled = "unlabeled"
    Serving = "serving"
    Feedback = "feedback"
    Training = "training"
    Prediction = "prediction"


class TimeSeriesType(Enum):
    Series = "series"
    Panel = "panel"
    Hierarchical = "hierarchical"
