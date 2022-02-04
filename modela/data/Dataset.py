import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Dataset as MDDataset
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2_grpc import DatasetServiceStub
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2 import CreateDatasetRequest, \
    UpdateDatasetRequest, \
    DeleteDatasetRequest, GetDatasetRequest, ListDatasetsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Dataset(Resource):
    def __init__(self, item: MDDataset = MDDataset(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class DatasetClient:
    def __init__(self, stub):
        self.__stub: DatasetServiceStub = stub

    def create(self, dataset: Dataset) -> bool:
        request = CreateDatasetRequest()
        request.item.CopyFrom(Dataset.raw_message)
        try:
            response = self.__stub.CreateDataset(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataset: Dataset) -> bool:
        request = UpdateDatasetRequest()
        request.item = Dataset.raw_message
        try:
            self.__stub.UpdateDataset(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Dataset, bool]:
        request = GetDatasetRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataset(request)
            return Dataset(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteDatasetRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataset(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Dataset], bool]:
        request = ListDatasetsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDatasets(request)
            return [Dataset(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


