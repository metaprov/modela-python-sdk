import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Dataset as MDDataset, DataSource
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2_grpc import DatasetServiceStub
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2 import CreateDatasetRequest, \
    UpdateDatasetRequest, \
    DeleteDatasetRequest, GetDatasetRequest, ListDatasetsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union
import pandas
from modela.data.models import SampleSettings, DatasetSpec
from modela.infra.models import Workload
from modela.training.common import TaskType


class Dataset(Resource):
    def __init__(self, item: MDDataset = MDDataset(), client=None, namespace="", name="", datasource: Union[DataSource, str] = "",
                 dataframe: pandas.DataFrame = None, data_file: str = None, workload: Workload = Workload(WorkloadClassName="general-large"),
                 sample=SampleSettings(), task_type: TaskType = TaskType.BinaryClassification):
        """

        :param client: The Dataset client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The desired name of the resource.
        :param datasource: If specified as a string, the SDK will attempt to find a Data Source resource with the given name.
            If specified as a Data Source, or if one was found with the given name, it will be applied to the Dataset.
        :param dataframe: If specified, the Pandas Dataframe will be serialized and uploaded for ingestion with the Dataset resource.
        :param data_file: If specified, the SDK will attempt read a file with the given path and will upload the
            contents of the file for ingestion with the Dataset resource.
        :param workload: The resource requirements which will be allocated for Dataset ingestion.
        :param sample: The sample settings of the dataset, which if enabled will ingest a Dataset with a portion of the uploaded data.
        :param task_type: The target task type in relation to the data being used.
        """
        super().__init__(item, client, namespace=namespace, name=name)

    @property
    def spec(self) -> DatasetSpec:
        return DatasetSpec().copy_from(self._object.spec).set_parent(self._object.spec)

    def default(self):
        DatasetSpec().apply_config(self._object.spec)




class DatasetClient:
    def __init__(self, stub):
        self.__stub: DatasetServiceStub = stub

    def create(self, dataset: Dataset) -> bool:
        request = CreateDatasetRequest()
        request.item.CopyFrom(dataset.raw_message)
        try:
            response = self.__stub.CreateDataset(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataset: Dataset) -> bool:
        request = UpdateDatasetRequest()
        request.item.CopyFrom(dataset.raw_message)
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


