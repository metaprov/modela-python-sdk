import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Model as MDModel
from github.com.metaprov.modelaapi.services.model.v1.model_pb2_grpc import ModelServiceStub
from github.com.metaprov.modelaapi.services.model.v1.model_pb2 import CreateModelRequest, \
    UpdateModelRequest, \
    DeleteModelRequest, GetModelRequest, ListModelsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union

from modela.training.models import ModelSpec, ModelStatus


class Model(Resource):
    def __init__(self, item: MDModel = MDModel(), client=None, namespace="", name=""):
        """
        The Model resource is a machine learning model generated by the Modela data plane. Models are immutable and
        cannot be changed once created.

        :param client: The Dataset client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        """
        super().__init__(item, client, namespace=namespace, name=name)

    @property
    def spec(self) -> ModelSpec:
        return ModelSpec().copy_from(self._object.spec)

    @property
    def status(self) -> ModelStatus:
        return ModelStatus().copy_from(self._object.status)

    def default(self):
        raise TypeError("Model {0} was not found; model resources cannot be created.".format(self.name))

    def submit(self):
        raise TypeError("Model resources cannot be created.")

    def update(self):
        raise TypeError("Model resources cannot be updated.")


class ModelClient:
    def __init__(self, stub):
        self.__stub: ModelServiceStub = stub

    def create(self, model: Model) -> bool:
        raise TypeError("Modela currently does not support the creation of custom models.")
        # request = CreateModelRequest()
        # request.model.CopyFrom(model.raw_message)
        # try:
        #    response = self.__stub.CreateModel(request)
        #    return True
        # except grpc.RpcError as err:
        #    error = err

        # ModelaException.process_error(error)

    def update(self, model: Model) -> bool:
        raise TypeError("Model resources cannot be changed after creation.")
        # request = UpdateModelRequest()
        # request.model.CopyFrom(model.raw_message)
        # try:
        #    self.__stub.UpdateModel(request)
        #    return True
        # except grpc.RpcError as err:
        #    error = err

        # ModelaException.process_error(error)
        # return False

    def get(self, namespace: str, name: str) -> Union[Model, bool]:
        request = GetModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetModel(request)
            return Model(response.model, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Model], bool]:
        request = ListModelsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListModels(request)
            return [Model(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False
