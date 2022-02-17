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
from modela.infra.models import NotificationSetting, Workload
from modela.training.common import TaskType


class DataProduct(Resource):
    def __init__(self, item: MDDataProduct = MDDataProduct(), client=None, namespace="", name="", servingsite: str = None,
                 lab: str = None, task_type: TaskType = TaskType.BinaryClassification, default_workload: Workload = None,
                 default_bucket: str = None, notification_setting: NotificationSetting = None):
        """
        :param client: The Data Product client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        :param servingsite: The default Serving Site of the Data Product
        :param lab: The default Lab of the Data Product
        :param task_type: The default task type of the Data Product
        :param default_workload: The default workload of the Data Product
        :param default_bucket: The default bucket used for all Data Product resources.
        :param notification_setting: The default notification settings used for all Data Product resources.
        """
        super().__init__(item, client, namespace=namespace, name=name)

    @property
    def spec(self) -> DataProductSpec:
        return DataProductSpec().copy_from(self._object.spec).set_parent(self._object.spec)

    def default(self):
        DataProductSpec().apply_config(self._object.spec)



class DataProductClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: DataProductServiceStub = stub

    def create(self, dataproduct: DataProduct) -> bool:
        request = CreateDataProductRequest()
        request.dataproduct.CopyFrom(dataproduct.raw_message)
        try:
            response = self.__stub.CreateDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataproduct: DataProduct) -> bool:
        request = UpdateDataProductRequest()
        request.dataproduct.CopyFrom(dataproduct.raw_message)
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
            return [DataProduct(item, self) for item in response.dataproducts.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


