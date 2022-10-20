from enum import Enum


class AccessType(Enum):
    ClusterIP = "cluster-ip"
    NodePort = "node-port"
    LoadBalancer = "load-balancer"
    Ingress = "ingress"
    Mesh = "mesh"
    Nothing = "none"


class PredictorConditionType(Enum):
    PredictorReady = "Ready"
    PredictorSaved = "Saved"


class ModelRole(Enum):
    Live = "live"
    Shadow = "shadow"


class ModelDeploymentPhase(Enum):
    Deploying = "Deploying"
    Deployed = "Deployed"
    Shadowing = "Shadowing"
    Releasing = "Releasing"
    Released = "Released"
    Failed = "Failed"


class PredictorType(Enum):
    Online = "online"
    Batch = "batch"
    Streaming = "streaming"


class K8sObjectStatusState(Enum):
    Healthy = "healthy"
    Warning = "warning"
    Error = "error"
    Unknown = "unknown"