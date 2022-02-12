import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import DataProduct as MDDataProduct
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2_grpc import DataProductServiceStub
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2 import CreateDataProductRequest, \
    UpdateDataProductRequest, \
    DeleteDataProductRequest, GetDataProductRequest, ListDataProductsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union

from modela.data.models import DataProductSpec


class DataProduct(Resource):
    def __init__(self, item: MDDataProduct = MDDataProduct(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)

    @property
    def spec(self) -> DataProductSpec:
        return DataProductSpec().copy_from(self._object.spec).set_parent(self._object.spec)

    def default(self):
        DataProductSpec().apply_config(self._object.spec)



class DataProductClient:
    def __init__(self, stub):
        self.__stub: DataProductServiceStub = stub

    def create(self, dataproduct: DataProduct) -> bool:
        request = CreateDataProductRequest()
        request.item.CopyFrom(dataproduct.raw_message)
        try:
            response = self.__stub.CreateDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataproduct: DataProduct) -> bool:
        request = UpdateDataProductRequest()
        request.item.CopyFrom(dataproduct.raw_message)
        try:
            self.__stub.UpdateDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[DataProduct, bool]:
        request = GetDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataProduct(request)
            return DataProduct(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[DataProduct], bool]:
        request = ListDataProductsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataProducts(request)
            return [DataProduct(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


