import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import ModelCompilerRun as MDModelCompilerRun
from github.com.metaprov.modelaapi.services.modelcompilerrun.v1.modelcompilerrun_pb2_grpc import ModelCompilerRunServiceStub
from github.com.metaprov.modelaapi.services.modelcompilerrun.v1.modelcompilerrun_pb2 import CreateModelCompilerRunRequest, \
    UpdateModelCompilerRunRequest, \
    DeleteModelCompilerRunRequest, GetModelCompilerRunRequest, ListModelCompilerRunsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class ModelCompilerRun(Resource):
    def __init__(self, item: MDModelCompilerRun = MDModelCompilerRun(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class ModelCompilerRunClient:
    def __init__(self, stub):
        self.__stub: ModelCompilerRunServiceStub = stub

    def create(self, modelcompilerrun: ModelCompilerRun) -> bool:
        request = CreateModelCompilerRunRequest()
        request.item.CopyFrom(ModelCompilerRun.raw_message)
        try:
            response = self.__stub.CreateModelCompilerRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, modelcompilerrun: ModelCompilerRun) -> bool:
        request = UpdateModelCompilerRunRequest()
        request.item = ModelCompilerRun.raw_message
        try:
            self.__stub.UpdateModelCompilerRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[ModelCompilerRun, bool]:
        request = GetModelCompilerRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetModelCompilerRun(request)
            return ModelCompilerRun(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteModelCompilerRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteModelCompilerRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[ModelCompilerRun], bool]:
        request = ListModelCompilerRunsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListModelCompilerRuns(request)
            return [ModelCompilerRun(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

