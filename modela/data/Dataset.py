import io
import os.path
import random
import time

import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import Dataset as MDDataset
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2_grpc import DatasetServiceStub
from github.com.metaprov.modelaapi.services.dataset.v1.dataset_pb2 import CreateDatasetRequest, \
    UpdateDatasetRequest, \
    DeleteDatasetRequest, GetDatasetRequest, ListDatasetsRequest, GetDatasetProfileRequest
from tabulate import tabulate
from tqdm import tqdm, trange

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union
import pandas

from modela.data.common import *
from modela.data.DataSource import DataSource
from modela.data.models import SampleSettings, DatasetSpec, DatasetStatus, DatasetProfile
from modela.infra.models import Workload, NotificationSetting
from modela.training.Report import Report
from modela.training.common import TaskType
from modela.util import convert_size


class Dataset(Resource):
    """
    Testing dataset resource
    """
    def __init__(self, item: MDDataset = MDDataset(), client=None, namespace="", name="",
                 version=Resource.DefaultVersion,
                 gen_datasource: bool = False,
                 target_column: str = None,
                 datasource: Union[DataSource, str] = "",
                 bucket: str = "default-minio-bucket",
                 dataframe: pandas.DataFrame = None,
                 data_file: str = None,
                 data_bytes: bytes = None,
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
        :param data_bytes: If specified, the SDK will upload the given raw data for ingestion with the Dataset resource.
        :param workload: The resource requirements which will be allocated for Dataset ingestion.
        :param sample: The sample settings of the dataset, which if enabled will ingest a Dataset with a portion of the uploaded data.
        :param task_type: The target task type in relation to the data being used.
        :param notification: The notification settings, which if enabled will forward events about this resource to a notifier.
        """
        self.default_resource = False
        self._profile = None
        super().__init__(item, client, namespace=namespace, name=name, version=version)
        if not self.default_resource:  # Ignore the rest of the constructor; datasets are immutable
            return

        if not gen_datasource:
            if type(datasource) != DataSource:  # Fetch the data source in case we need to read the file type
                datasource = client.modela.DataSource(namespace=namespace, name=datasource)

        if data_file is not None:
            with open(data_file, 'r') as f:
                data_bytes = f.read()
            data_file = os.path.basename(data_file)
        elif dataframe is not None:
            writer = io.BytesIO()
            if datasource.spec.FileType == FlatFileType.Csv:
                df_encoded = dataframe.to_csv(index=False)
            if datasource.spec.FileType == FlatFileType.Parquet:
                df_encoded = dataframe.to_parquet(index=False)
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
            data_bytes = bytes(df_encoded, encoding='utf-8')

        if data_bytes is not None:
            self.spec.Origin = client.modela.FileService.upload_file(data_file or name, data_bytes,
                                                                     client.modela.tenant,
                                                                     namespace, version, bucket, "datasets", name)

        if gen_datasource:
            datasource = client.modela.DataSource(namespace=namespace, name=name + "_source", version=version,
                                                  infer_bytes=data_bytes, target_column=target_column)
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
        return DatasetStatus().copy_from(self._object.status)

    def default(self):
        self.default_resource = True
        DatasetSpec().apply_config(self._object.spec)

    @property
    def report(self) -> Report:
        """ Fetch the report associated with the Dataset """
        if hasattr(self, "_client"):
            if self._object.status.reportName != "":
                return self._client.modela.Report(namespace=self.namespace, name=self._object.status.reportName)
            else:
                print("Dataset {0} has no report.".format(self.name))
        else:
            raise AttributeError("Object has no client repository")

    @property
    def phase(self) -> DatasetPhase:
        """ The phase specified by the status of the Dataset """
        return self.status.Phase

    @property
    def datasource(self) -> DataSource:
        """ Fetch the DataSource object associated with the Dataset """
        if hasattr(self, "_client"):
            return self._client.modela.DataSource(self.namespace, self.spec.DatasourceName)
        else:
            raise AttributeError("Object has no client repository")

    def submit_and_visualize(self, replace: bool = False):
        """
        Submit the resource and call visualize().

        :param replace: Replace the resource if it already exists on the cluster.
        """
        self.submit(replace)
        self.visualize()

    def visualize(self):
        """
        Display a real-time visualization of the Dataset's progress
        """
        desc = tqdm(total=0, position=0, bar_format='{desc}Time Elapsed: {elapsed}')
        progress = tqdm(total=100, position=1, bar_format='{l_bar}{bar}',
                        desc=self.name, ncols=80, initial=0)

        current_status = self.status
        try:
            while True:
                self.sync()
                if current_status == self.status:
                    time.sleep(0.1)
                    continue

                current_status = self.status
                desc.set_description_str('Phase: %s | File Size: %s | Rows: %s | Columns: %s' %
                                     (self.phase.name, convert_size(self.status.Statistics.FileSize),
                                      "[Processing]" if self.status.Statistics.Rows == 0 else self.status.Statistics.Rows,
                                      "[Processing]" if len(self.status.Statistics.Columns) == 0 else len(self.status.Statistics.Columns)))
                progress.n = self.status.Progress
                progress.last_print_n = self.status.Progress
                progress.refresh()
                if self.phase in (DatasetPhase.Ready, DatasetPhase.Aborted, DatasetPhase.Failed):
                    if self.phase == DatasetPhase.Ready:
                        print("\n\n" + self.profile)
                    else:
                        progress.colour = "red"
                        progress.refresh()
                        print("\nDataset was failed or aborted: %s" % current_status.FailureMessage)

                    break

        except KeyboardInterrupt:
            pass

        desc.close()
        progress.close()

    @property
    def profile(self) -> str:
        """
        Returns an ASCII-rendered table of the Dataset's profile
        """
        profile = self.get_profile()

        table = []
        for col in profile.Columns:
            table.append([col.Name, col.Type, col.Distinct, col.Missing,
                           '{0:.3g}'.format(col.Mean), '{0:.3g}'.format(col.Stddev), col.P50, col.Min, col.Max,
                           '{0:.3g}'.format(col.CorrToTarget), '{0:.3g}'.format(col.Variance),
                           '{0:.3g}'.format(col.Skewness), '{0:.3g}'.format(col.Kurtosis)])

        table = tabulate(table, tablefmt='pretty', headers=['Column', 'Data Type', 'Distinct', 'Missing', 'Mean',
                          'Stddev', 'Median', 'Min', 'Max', 'Corr. To Target', 'Variance', 'Skewness', 'Kurtosis'])
        return table + "\n"
        # TODO: jupyter support, print all viz plots in jupyter

    @property
    def details(self) -> str:
        """
        Returns an ASCII-rendered table of the Dataset's statistics
        """
        table = []
        for col in self.status.Statistics.Columns:
            table.append([col.Name, col.Datatype.name, col.Distinct, col.Missing,
                           '{0:.3g}'.format(col.Mean), '{0:.3g}'.format(col.Stddev), col.P50, col.Min, col.Max,
                           '{0:.3g}'.format(col.Skewness), '{0:.3g}'.format(col.Kurtosis)])

        table = tabulate(table, tablefmt='pretty', headers=['Column', 'Data Type', 'Distinct', 'Missing', 'Mean',
                                                            'Stddev', 'Median', 'Min', 'Max', 'Skewness', 'Kurtosis'])
        return table + "\n"

    def get_profile(self) -> DatasetProfile:
        if self._profile:
            return self._profile
        if hasattr(self, "_client"):
            self._profile = self._client.profile(self.namespace, self.name)
            return self._profile
        else:
            raise AttributeError("Object has no client repository")


    def __repr__(self):
        out = super().__repr__()
        if len(self.status.Statistics.Columns) > 0:
            out += "\n" + self.details

        return out




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

    def profile(self, namespace: str, name: str) -> DatasetProfile:
        request = GetDatasetProfileRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDatasetProfile(request)
            return DatasetProfile().copy_from(response.profile)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False