import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataSource as MDDataSource
from github.com.metaprov.modelaapi.services.datasource.v1.datasource_pb2_grpc import DataSourceServiceStub
from github.com.metaprov.modelaapi.services.datasource.v1.datasource_pb2 import CreateDataSourceRequest, \
    UpdateDataSourceRequest, \
    DeleteDataSourceRequest, GetDataSourceRequest, ListDataSourceRequest
from modela.Resource import *
from modela.ModelaException import ModelaException
from typing import List, Union
import pandas
from modela.data.models import *
from modela.training.common import *


class DataSource(Resource):
    def __init__(self, item: MDDataSource = MDDataSource(), client=None, namespace="", name="", version=Resource.DefaultVersion,
                 infer_file: str = None,
                 infer_dataframe: pandas.DataFrame = None,
                 target_column: str = "",
                 file_type: FlatFileType = FlatFileType.Csv,
                 task_type: TaskType = TaskType.BinaryClassification,
                 csv_config: CsvFileFormat = None,
                 excel_config: ExcelNotebookFormat = None):
        """
        :param client: The Data Source client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        :param infer_file: If specified, the SDK will attempt read a file with the given path and will upload the
            contents of the file to the Modela API for analysis. The analysed columns will be applied to the Data Source.
        :param infer_dataframe: If specified, the  Pandas DataFrame will be serialized and uploaded to the Modela
            API for analysis. The analysed columns will be applied to the Data Source.
        :param target_column: The name of the target column used when training a model. This parameter only has effect
            when `infer_file` or `infer_dataframe` is specified.
        :param file_type: The file type of raw data, used when ingesting a Dataset. Only applicable for flat files.
        :param task_type: The target task type in relation to the data being used.
        :param csv_config: The CSV file format of the raw data.
        :param excel_config: The Excel file format of the raw data.
        """

        super().__init__(item, client, namespace=namespace, name=name, version=version)

    @property
    def spec(self) -> DataSourceSpec:
        return DataSourceSpec().copy_from(self._object.spec).set_parent(self._object.spec)

    @property
    def schema(self):
        return self.spec.Schema

    def default(self):
        DataSourceSpec().apply_config(self._object.spec)


class DataSourceClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: DataSourceServiceStub = stub

    def create(self, datasource: DataSource) -> bool:
        request = CreateDataSourceRequest()
        request.datasource.CopyFrom(datasource.raw_message)
        try:
            response = self.__stub.CreateDataSource(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, datasource: DataSource) -> bool:
        request = UpdateDataSourceRequest()
        request.datasource.CopyFrom(datasource.raw_message)
        try:
            self.__stub.UpdateDataSource(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[DataSource, bool]:
        request = GetDataSourceRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataSource(request)
            return DataSource(response.datasource, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteDataSourceRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataSource(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[DataSource], bool]:
        request = ListDataSourceRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataSources(request)
            return [DataSource(item, self) for item in response.datasources.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False
