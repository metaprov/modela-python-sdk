import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataPipelineRun as MDDataPipelineRun
from github.com.metaprov.modelaapi.services.datapipelinerun.v1.datapipelinerun_pb2_grpc import DataPipelineRunServiceStub
from github.com.metaprov.modelaapi.services.datapipelinerun.v1.datapipelinerun_pb2 import CreateDataPipelineRunRequest, \
    UpdateDataPipelineRunRequest, \
    DeleteDataPipelineRunRequest, GetDataPipelineRunRequest, ListDataPipelineRunRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class DataPipelineRun(Resource):
    def __init__(self, item: MDDataPipelineRun = MDDataPipelineRun(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class DataPipelineRunClient:
    def __init__(self, stub):
        self.__stub: DataPipelineRunServiceStub = stub

    def create(self, datapipelinerun: DataPipelineRun) -> bool:
        request = CreateDataPipelineRunRequest()
        request.item.CopyFrom(datapipelinerun.raw_message)
        try:
            response = self.__stub.CreateDataPipelineRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, datapipelinerun: DataPipelineRun) -> bool:
        request = UpdateDataPipelineRunRequest()
        request.item.CopyFrom(datapipelinerun.raw_message)
        try:
            self.__stub.UpdateDataPipelineRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[DataPipelineRun, bool]:
        request = GetDataPipelineRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataPipelineRun(request)
            return DataPipelineRun(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteDataPipelineRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataPipelineRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[DataPipelineRun], bool]:
        request = ListDataPipelineRunRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataPipelineRuns(request)
            return [DataPipelineRun(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


