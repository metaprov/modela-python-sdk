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
    def __init__(self, item: MDDataSource = MDDataSource(), client=None, namespace="", name="", infer_file="",
                 infer_dataframe: pandas.DataFrame = None, target_column: str = "", file_type: FlatFileType = FlatFileType.Csv,
                 task_type: TaskType = "", csv_config: CsvFileFormat = None, excel_config: ExcelNotebookFormat = None):
        super().__init__(item, client, namespace=namespace, name=name)


class DataSourceClient:
    """
    DataSourceClient provides a CRUD interface for the Data Source resource.
    """

    def __init__(self, stub):
        self.__stub: DataSourceServiceStub = stub

    def create(self, datasource: DataSource) -> bool:
        request = CreateDataSourceRequest()
        request.item.CopyFrom(DataSource.raw_message)
        try:
            response = self.__stub.CreateDataSource(request)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, datasource: DataSource) -> bool:
        request = UpdateDataSourceRequest()
        request.item = DataSource.raw_message
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
            return DataSource(response.item, self)
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
            return [DataSource(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False
