import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import NotebookRun as MDNotebookRun
from github.com.metaprov.modelaapi.services.notebookrun.v1.notebookrun_pb2_grpc import NotebookRunServiceStub
from github.com.metaprov.modelaapi.services.notebookrun.v1.notebookrun_pb2 import CreateNotebookRunRequest, \
    UpdateNotebookRunRequest, \
    DeleteNotebookRunRequest, GetNotebookRunRequest, ListNotebookRunsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class NotebookRun(Resource):
    def __init__(self, item: MDNotebookRun = MDNotebookRun(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class NotebookRunClient:
    def __init__(self, stub):
        self.__stub: NotebookRunServiceStub = stub

    def create(self, notebookrun: NotebookRun) -> bool:
        request = CreateNotebookRunRequest()
        request.item.CopyFrom(NotebookRun.raw_message)
        try:
            response = self.__stub.CreateNotebookRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, notebookrun: NotebookRun) -> bool:
        request = UpdateNotebookRunRequest()
        request.item = NotebookRun.raw_message
        try:
            self.__stub.UpdateNotebookRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[NotebookRun, bool]:
        request = GetNotebookRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetNotebookRun(request)
            return NotebookRun(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteNotebookRunRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteNotebookRun(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[NotebookRun], bool]:
        request = ListNotebookRunsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListNotebookRuns(request)
            return [NotebookRun(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


