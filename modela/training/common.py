from enum import Enum


class TaskType(Enum):
    BinaryClassification = "binary-classification"
    MultiClassification = "multi-classification"
    MultiLabelClassification = "multi-label-classification"
    Forecasting = "forecasting"
    Regression = "regression"
    Clustering = "clustering"
    Recommendation = "recommendation"
    OutlierDetection = "outlier-detection"
    NoveltyDetection = "novelty-detection"
    TopicModeling = "topic-modeling"
    VideoActionRecognition = "video-action-recognition"
    VideoClassification = "video-classification"
    VideoObjectTracking = "video-object-tracking"
    ImageClassification = "image-classification"
    ImageMultiLabelClassification = "image-multi-classification"
    ImageObjectDetection = "image-object-detection"
    ImageSegmentation = "image-segmentation"
    AutoDetectTask = "auto"


class Imputation(Enum):
    RemoveRowsWithMissingValues = "remove-rows-with-missing-values"
    ReplaceWithMean = "replace-with-mean"
    ReplaceWithMedian = "replace-with-median"
    ReplaceWithArbitraryValue = "replace-with-arbitrary-value"
    ReplaceWithEndOfTail = "replace-with-end-of-tail"
    ReplaceWithRandomSample = "replace-with-random-sample"
    FreqCategory = "freq-category-imputation"
    AddMissingValueIndicator = "add-missing-value-indicator"
    Knn = "knn"
    Iterative = "iterative"
    MICE = "mice"
    No = "no-imputation"
    AutoImputer = "auto"


class Scaling(Enum):
    Standard = "standard-scaling"
    MaxAbs = "max-abs-scaling"
    MinMax = "min-max-scaling"
    Normalization = "normalizion-scaling"
    Robust = "robust-scaling"
    ScaleToUnitNorm = "scale-to-unit-norm"
    NoScaling = "none"
    Auto = "auto"
