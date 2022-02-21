import grpc
from github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 import Predictor as MDPredictor
from github.com.metaprov.modelaapi.services.predictor.v1.predictor_pb2_grpc import PredictorServiceStub
from github.com.metaprov.modelaapi.services.predictor.v1.predictor_pb2 import CreatePredictorRequest, \
    UpdatePredictorRequest, \
    DeletePredictorRequest, GetPredictorRequest, ListPredictorsRequest

from modela import ObjectReference
from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union

from modela.inference.common import AccessType
from modela.inference.models import ModelDeploymentSpec, PredictorSpec, PredictorStatus
from modela.infra.ServingSite import ServingSite
from modela.infra.models import Workload
from modela.training.Model import Model


class Predictor(Resource):
    def __init__(self, item: MDPredictor = MDPredictor(), client=None, namespace="", name="",
                 serving_site: Union[ObjectReference, ServingSite, str] = "default-serving-site",
                 model: Union[Model, str] = None,
                 models: List[ModelDeploymentSpec] = [],
                 port: int = 3000,
                 path: str = None,
                 access_type: AccessType = None,
                 replicas: int = 0,
                 autoscale: bool = False,
                 workload: Workload = None):
        """

        :param client: The Predictor client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        :param serving_site: The object reference, Serving Site object, or name under default-tenant for which the
            predictor will be deployed under.
        :param model: The Model object or name that the predictor will serve predictions for. This parameter
            will instantiate the predictor with a singe default deployment specification for the model.
        :param models: The list of model deployment specifications that will be applied to the predictor.
        :param port: The port of the predictor, which if applicable will expose the service internally or externally.
        :param path: The path that the predictor will expose a service on. If this parameter is not specified, then
            a path will be generated based on the access type and predictor name.
        :param access_type: The access type of the predictor. Documentation on how each access type exposes the prediction
            service can be found at the modela.ai Predictor resource documentation.
        :param replicas: The amount of replicas for the predictor, which if greater than zero will serve the prediction
            service on multiple pods.
        :param autoscale: If set to true, the predictor's deployment will scale based on the amount of incoming traffic
            to the service.
        :param workload: The workload specification which determines the resources which will be allocated to the
            prediction service.
        """
        super().__init__(item, client, namespace=namespace, name=name)

        if type(serving_site) == ServingSite:
            serving_site = serving_site.reference
        elif type(serving_site) == str:
            serving_site = ObjectReference(Namespace="default-tenant", Name=serving_site)
        self.spec.ServingsiteRef = serving_site

        if model is not None:
            if type(model) == Model:
                model = model.name
            self.spec.Models = [ModelDeploymentSpec(ModelName=model)]
        else:
            self.spec.Models = models

        if port is not None:
            self._object.spec.port = port

        if path is not None:
            self._object.spec.path = path

        if access_type is not None:
            self._object.spec.accessType = access_type.value

        if replicas > 0:
            self._object.spec.replicas = replicas

        if workload is not None:
            self.spec.Resources = workload

    @property
    def spec(self) -> PredictorSpec:
        return PredictorSpec().copy_from(self._object.spec)

    @property
    def status(self) -> PredictorStatus:
        return PredictorStatus().copy_from(self._object.status)

    def default(self):
        PredictorSpec().apply_config(self._object.spec)

    def connect(self):
        self.name

class PredictorClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: PredictorServiceStub = stub

    def create(self, predictor: Predictor) -> bool:
        request = CreatePredictorRequest()
        request.predictor.CopyFrom(predictor.raw_message)
        try:
            response = self.__stub.CreatePredictor(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, predictor: Predictor) -> bool:
        request = UpdatePredictorRequest()
        request.predictor.CopyFrom(predictor.raw_message)
        try:
            self.__stub.UpdatePredictor(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Predictor, bool]:
        request = GetPredictorRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetPredictor(request)
            return Predictor(response.predictor, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeletePredictorRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeletePredictor(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str, labels: dict[str, str] = None) -> Union[List[Predictor], bool]:
        request = ListPredictorsRequest()
        request.namespace = namespace
        if labels is not None:
            request.labels.update(labels)

        try:
            response = self.__stub.ListPredictors(request)
            return [Predictor(item, self) for item in response.predictors.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False




