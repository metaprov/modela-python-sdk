import grpc
from github.com.metaprov.modelaapi.pkg.apis.inference.v1alpha1.generated_pb2 import Predictor as MDPredictor
from github.com.metaprov.modelaapi.services.predictor.v1.predictor_pb2_grpc import PredictorServiceStub
from github.com.metaprov.modelaapi.services.predictor.v1.predictor_pb2 import CreatePredictorRequest, \
    UpdatePredictorRequest, \
    DeletePredictorRequest, GetPredictorRequest, ListPredictorsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Predictor(Resource):
    def __init__(self, item: MDPredictor = MDPredictor(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class PredictorClient:
    def __init__(self, stub):
        self.__stub: PredictorServiceStub = stub

    def create(self, predictor: Predictor) -> bool:
        request = CreatePredictorRequest()
        request.item.CopyFrom(Predictor.raw_message)
        try:
            response = self.__stub.CreatePredictor(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, predictor: Predictor) -> bool:
        request = UpdatePredictorRequest()
        request.item = Predictor.raw_message
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
            return Predictor(response.item, self)
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

    def list(self, namespace: str) -> Union[List[Predictor], bool]:
        request = ListPredictorsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListPredictors(request)
            return [Predictor(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


