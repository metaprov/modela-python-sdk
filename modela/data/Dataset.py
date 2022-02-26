import io
import os.path

import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Dataset as MDDataset
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2_grpc import DatasetServiceStub
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2 import CreateDatasetRequest, \
    UpdateDatasetRequest, \
    DeleteDatasetRequest, GetDatasetRequest, ListDatasetsRequest

from modela import DatasetPhase, FlatFileType
from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union
import pandas

from modela.data.DataSource import DataSource
from modela.data.models import SampleSettings, DatasetSpec, DatasetStatus
from modela.infra.models import Workload, NotificationSetting
from modela.training.Report import Report
from modela.training.common import TaskType


class Dataset(Resource):
    def __init__(self, item: MDDataset = MDDataset(), client=None, namespace="", name="",
                 version=Resource.DefaultVersion,
                 gen_datasource: bool = False,
                 target_column: str = None,
                 datasource: Union[DataSource, str] = None,
                 bucket: str = "default-minio-bucket",
                 dataframe: pandas.DataFrame = None,
                 data_file: str = None,
                 raw_data: bytes = None,
                 workload: Workload = Workload("general-large"),
                 sample=SampleSettings(),
                 task_type: TaskType = TaskType.BinaryClassification,
                 notification: NotificationSetting = None):
        """
        :param client: The Dataset client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        :param gen_datasource: If true, a Datasource resource will be created from the uploaded dataset and applied to
            the Dataset resource.
        :param target_column: If gen_datasource is enabled, then the target column of the data source must be specified.
        :param datasource: If specified as a string, the SDK will attempt to find a Data Source resource with the given name.
            If specified as a Data Source, or if one was found with the given name, it will be applied to the Dataset.
        :param bucket: The bucket which the raw dataset data will be uploaded to.
        :param dataframe: If specified, the Pandas Dataframe will be serialized and uploaded for ingestion with the Dataset resource.
        :param data_file: If specified, the SDK will attempt read a file with the given path and will upload the
            contents of the file for ingestion with the Dataset resource.
        :param raw_data: If specified, the SDK will upload the given raw data for ingestion with the Dataset resource.
        :param workload: The resource requirements which will be allocated for Dataset ingestion.
        :param sample: The sample settings of the dataset, which if enabled will ingest a Dataset with a portion of the uploaded data.
        :param task_type: The target task type in relation to the data being used.
        :param notification: The notification settings, which if enabled will forward events about this resource to a notifier.
        """
        self.default_resource = False
        super().__init__(item, client, namespace=namespace, name=name, version=version)
        if not self.default_resource:  # Ignore the rest of the constructor; datasets are immutable
            return

        if not gen_datasource:
            if type(datasource) != DataSource:  # Fetch the data source in case we need to read the file type
                datasource = client.modela.DataSource(namespace=namespace, name=datasource)

        if data_file is not None:
            with open(data_file, 'r') as f:
                raw_data = f.read()
            data_file = os.path.basename(data_file)
        elif dataframe is not None:
            writer = io.BytesIO()
            if datasource.spec.FileType == FlatFileType.Csv:
                df_encoded = dataframe.to_csv()
            if datasource.spec.FileType == FlatFileType.Parquet:
                df_encoded = dataframe.to_parquet()
            elif datasource.spec.FileType == FlatFileType.Excel:
                dataframe.to_excel(writer)
                df_encoded = writer.getvalue()
            elif datasource.spec.FileType == FlatFileType.Json:
                df_encoded = dataframe.to_json()
            elif datasource.spec.FileType == FlatFileType.Feather:
                dataframe.to_feather(writer)
                df_encoded = writer.getvalue()
            else:
                raise TypeError(
                    "Pandas cannot deserialize a dataframe to the file type {0}. Consider changing your data source file format."
                        .format(datasource.spec.FileType))
            raw_data = bytes(df_encoded, encoding='utf-8')

        self.spec.Location = client.modela.FileService.upload_file(data_file or name, raw_data, client.modela.tenant,
                                                                   namespace, version, bucket, "datasets", name)

        if gen_datasource:
            datasource = client.modela.DataSource(namespace=namespace, name=name + "_source", version=version,
                                                  infer_bytes=raw_data, target_column=target_column)
            datasource.submit()

        self.spec.DatasourceName = datasource.name
        self.spec.Resources = workload
        self.spec.Task = task_type
        if sample is not None:
            self.spec.Sample = sample

        if notification is not None:
            self.spec.Notification = notification

    @property
    def spec(self) -> DatasetSpec:
        return DatasetSpec().copy_from(self._object.spec).set_parent(self._object.spec)

    @property
    def status(self) -> DatasetStatus:
        return DatasetStatus().copy_from(self._object.spec)

    def default(self):
        self.default_resource = True
        DatasetSpec().apply_config(self._object.spec)

    @property
    def report(self) -> Report:
        if hasattr(self, "_client"):
            if self._object.status.reportName != "":
                return self._client.modela.Report(namespace=self.namespace, name=self._object.status.reportName)
            else:
                print("Dataset {0} has no report.".format(self.name))
        else:
            raise AttributeError("Object has no client repository")

    @property
    def phase(self) -> DatasetPhase:
        return self.status.Phase

    @property
    def datasource(self) -> DataSource:
        if hasattr(self, "_client"):
            return self._client.modela.DataSource(self.namespace, self.spec.DatasourceName)
        else:
            raise AttributeError("Object has no client repository")


class DatasetClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: DatasetServiceStub = stub

    def create(self, dataset: Dataset) -> bool:
        request = CreateDatasetRequest()
        request.dataset.CopyFrom(dataset.raw_message)
        try:
            response = self.__stub.CreateDataset(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataset: Dataset) -> bool:
        request = UpdateDatasetRequest()
        request.dataset.CopyFrom(dataset.raw_message)
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
            return Dataset(response.dataset, self)
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
            return [Dataset(item, self) for item in response.datasets.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False
