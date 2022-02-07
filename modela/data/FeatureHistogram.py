import grpc
from github.com.metaprov.modelaapi.pkg.apis.data.v1alpha1.generated_pb2 import FeatureHistogram as MDFeatureHistogram
from github.com.metaprov.modelaapi.services.featurehistogram.v1.featurehistogram_pb2_grpc import FeatureHistogramServiceStub
from github.com.metaprov.modelaapi.services.featurehistogram.v1.featurehistogram_pb2 import CreateFeatureHistogramRequest, \
    UpdateFeatureHistogramRequest, \
    DeleteFeatureHistogramRequest, GetFeatureHistogramRequest, ListFeatureHistogramsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class FeatureHistogram(Resource):
    def __init__(self, item: MDFeatureHistogram = MDFeatureHistogram(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class FeatureHistogramClient:
    def __init__(self, stub):
        self.__stub: FeatureHistogramServiceStub = stub

    def create(self, featurehistogram: FeatureHistogram) -> bool:
        request = CreateFeatureHistogramRequest()
        request.item.CopyFrom(FeatureHistogram.raw_message)
        try:
            response = self.__stub.CreateFeatureHistogram(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, featurehistogram: FeatureHistogram) -> bool:
        request = UpdateFeatureHistogramRequest()
        request.item = FeatureHistogram.raw_message
        try:
            self.__stub.UpdateFeatureHistogram(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[FeatureHistogram, bool]:
        request = GetFeatureHistogramRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetFeatureHistogram(request)
            return FeatureHistogram(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteFeatureHistogramRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteFeatureHistogram(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[FeatureHistogram], bool]:
        request = ListFeatureHistogramsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListFeatureHistograms(request)
            return [FeatureHistogram(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

