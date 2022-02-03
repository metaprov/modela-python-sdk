import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataSource as MDDataSource
from github.com.metaprov.modelaapi.services.datasource.v1.datasource_pb2_grpc import DataSourceServiceStub
from github.com.metaprov.modelaapi.services.datasource.v1.datasource_pb2 import CreateDataSourceRequest, UpdateDataSourceRequest, \
    DeleteDataSourceRequest, GetDataSourceRequest, ListDataSourceRequest
from modela.Resource import Resource

class DataSource(Resource):
    def __init__(self, item: MDDataSource = None, client=None, namespace="", name="", infer_file="",
                 infer_dataframe="", target_column="", file_type="csv"):
        super().__init__(item, client, namespace=namespace, name=name)


class DataSourceClient:
    def __init__(self, stub):
        self.__stub: DataSourceServiceStub = stub

    def create(self, datasource: DataSource) -> None:
        request = CreateDataSourceRequest()
        request.item.CopyFrom(DataSource.raw_message)
        try:
            response = self.__stub.CreateDataSource(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def update(self, datasource: DataSource) -> None:
        request = UpdateDataSourceRequest()
        request.item = DataSource.raw_message
        try:
            self.__stub.UpdateDataSource(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get(self, namespace: str, name: str) -> DataSource:
        request = GetDataSourceRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataSource(request)
            return DataSource(response.item, self)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def delete(self, namespace: str, name: str) -> None:
        request = DeleteDataSourceRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataSource(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

    def list(self, namespace: str):
        request = ListDataSourceRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataSources(request)
            return response.items.items
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

