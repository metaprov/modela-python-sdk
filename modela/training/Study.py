import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Study as MDStudy
from github.com.metaprov.modelaapi.services.study.v1.study_pb2_grpc import StudyServiceStub
from github.com.metaprov.modelaapi.services.study.v1.study_pb2 import CreateStudyRequest, \
    UpdateStudyRequest, \
    DeleteStudyRequest, GetStudyRequest, ListStudyRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Study(Resource):
    def __init__(self, item: MDStudy = MDStudy(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class StudyClient:
    def __init__(self, stub):
        self.__stub: StudyServiceStub = stub

    def create(self, study: Study) -> bool:
        request = CreateStudyRequest()
        request.item.CopyFrom(study.raw_message)
        try:
            response = self.__stub.CreateStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, study: Study) -> bool:
        request = UpdateStudyRequest()
        request.item.CopyFrom(study.raw_message)
        try:
            self.__stub.UpdateStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Study, bool]:
        request = GetStudyRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetStudy(request)
            return Study(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteStudyRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Study], bool]:
        request = ListStudyRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListStudys(request)
            return [Study(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


