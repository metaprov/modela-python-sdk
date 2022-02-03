import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataProduct as MDDataProduct
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2_grpc import DataProductServiceStub
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2 import CreateDataProductRequest, UpdateDataProductRequest, \
    DeleteDataProductRequest, GetDataProductRequest, ListDataProductsRequest
from modela.Resource import Resource

class DataProduct(Resource):
    def __init__(self, item: MDDataProduct = None, client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)

class DataProductClient:
    def __init__(self, stub):
        self.__stub: DataProductServiceStub = stub

    def create(self, dataproduct: DataProduct, password: str = "") -> None:
        request = CreateDataProductRequest()
        request.item.CopyFrom(DataProduct.raw_message)
        request.password = password
        try:
            response = self.__stub.CreateDataProduct(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def update(self, dataproduct: DataProduct) -> None:
        request = UpdateDataProductRequest()
        request.item = DataProduct.raw_message
        try:
            self.__stub.UpdateDataProduct(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get(self, namespace: str, name: str) -> DataProduct:
        request = GetDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataProduct(request)
            return DataProduct(response.item, self)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def delete(self, namespace: str, name: str) -> None:
        request = DeleteDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataProduct(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

    def list(self, namespace: str):
        request = ListDataProductsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataProducts(request)
            return response.items.items
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

