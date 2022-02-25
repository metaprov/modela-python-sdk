import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ModelAutobuilder as MDModelAutobuilder
from github.com.metaprov.modelaapi.services.modelautobuilder.v1.modelautobuilder_pb2_grpc import ModelAutobuilderServiceStub
from github.com.metaprov.modelaapi.services.modelautobuilder.v1.modelautobuilder_pb2 import CreateModelAutobuilderRequest, \
    UpdateModelAutobuilderRequest, \
    DeleteModelAutobuilderRequest, GetModelAutobuilderRequest, ListModelAutobuildersRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class ModelAutobuilder(Resource):
    def __init__(self, item: MDModelAutobuilder = MDModelAutobuilder(), client=None, namespace="", name="", version=Resource.DefaultVersion):
        super().__init__(item, client, namespace=namespace, name=name, version=version)


class ModelAutobuilderClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: ModelAutobuilderServiceStub = stub

    def create(self, modelautobuilder: ModelAutobuilder) -> bool:
        request = CreateModelAutobuilderRequest()
        request.modelautobuilder.CopyFrom(modelautobuilder.raw_message)
        try:
            response = self.__stub.CreateModelAutobuilder(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, modelautobuilder: ModelAutobuilder) -> bool:
        request = UpdateModelAutobuilderRequest()
        request.modelautobuilder.CopyFrom(modelautobuilder.raw_message)
        try:
            self.__stub.UpdateModelAutobuilder(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[ModelAutobuilder, bool]:
        request = GetModelAutobuilderRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetModelAutobuilder(request)
            return ModelAutobuilder(response.modelautobuilder, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteModelAutobuilderRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteModelAutobuilder(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str, labels: dict = None) -> Union[List[ModelAutobuilder], bool]:
        request = ListModelAutobuildersRequest()
        request.namespace = namespace
        if labels is not None:
            request.labels.update(labels)

        try:
            response = self.__stub.ListModelAutobuilders(request)
            return [ModelAutobuilder(item, self) for item in response.modelautobuilders.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


