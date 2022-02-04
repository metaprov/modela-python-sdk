import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Model as MDModel
from github.com.metaprov.modelaapi.services.model.v1.model_pb2_grpc import ModelServiceStub
from github.com.metaprov.modelaapi.services.model.v1.model_pb2 import CreateModelRequest, \
    UpdateModelRequest, \
    DeleteModelRequest, GetModelRequest, ListModelsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Model(Resource):
    def __init__(self, item: MDModel = MDModel(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class ModelClient:
    def __init__(self, stub):
        self.__stub: ModelServiceStub = stub

    def create(self, model: Model) -> bool:
        request = CreateModelRequest()
        request.item.CopyFrom(Model.raw_message)
        try:
            response = self.__stub.CreateModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, model: Model) -> bool:
        request = UpdateModelRequest()
        request.item = Model.raw_message
        try:
            self.__stub.UpdateModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Model, bool]:
        request = GetModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetModel(request)
            return Model(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Model], bool]:
        request = ListModelsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListModels(request)
            return [Model(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


