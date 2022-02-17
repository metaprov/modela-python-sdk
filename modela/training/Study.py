import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Study as MDStudy
from github.com.metaprov.modelaapi.services.study.v1.study_pb2_grpc import StudyServiceStub
from github.com.metaprov.modelaapi.services.study.v1.study_pb2 import CreateStudyRequest, \
    UpdateStudyRequest, DeleteStudyRequest, GetStudyRequest, ListStudyRequest, \
    GetStudyProfileRequest, CreateStudyProfileRequest, AbortStudyRequest, PauseStudyRequest, ResumeStudyRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException, ResourceNotFoundException
from typing import List, Union

from modela.data.Dataset import Dataset
from modela.training.Model import Model
from modela.training.common import TaskType
from modela.training.models import *


class Study(Resource):
    def __init__(self, item: MDStudy = MDStudy(), client=None, namespace="", name="", dataset: Union[str, Dataset] = "",
                 lab: ObjectReference = None, task_type: TaskType = TaskType.AutoDetectTask, search: ModelSearch = None,
                 fe_search: FeatureEngineeringSearch = None, baseline: BaselineSettings = None,
                 ensemble: Ensemble = None,
                 training_parameters: Training = None, interpretability: Interpretability = None,
                 schedule: StudySchedule = None,
                 notification: NotificationSetting = None, garbage_collect: bool = True, keep_best_models: bool = True,
                 timeout: int = 600,
                 template: bool = False):
        """

        :param client: The Study client repository, which can be obtained through an instance of Modela.
        :param namespace: The target namespace of the resource.
        :param name: The name of the resource.
        :param dataset: If specified as a string, the SDK will attempt to find a Dataset resource with the given name.
            If specified as a Dataset object, or if one was found with the given name, it will be used in the Study.
        :param lab: The object reference to a lab as a training environment
        :param task_type: The ML task type of the Study
        :param search: The search parameters define how many models to sample
        :param fe_search: The feature engineering search parameters of the Study
        :param baseline: The baseline settings for the Study, which if enabled will train an unoptimized model of each
            algorithm type for benchmarking.
        :param ensemble: The ensemble settings for the Study, which if enabled will combine the top estimators of
            the study after the initial model search.
        :param training_parameters: The training template for each model created by the Study.
        :param interpretability: The interpretability settings for the Study, which when enabled can produce ICE, LIME,
            and Shap value plots
        :param schedule: The schedule for the study to run chronically
        :param notification: The notification settings, which if enabled will forward events about this resource to a notifier.
        :param garbage_collect: If enabled, models which did not move past the testing stage will be garbage collected by
            the system.
        :param keep_best_models: If enabled, the best models from each algorithm will not be garbage collected.
        :param timeout: The timeout of the Study
        :param template: If the Study is a template it will not start a search and can only be used as a template for
            other studies.
        """
        super().__init__(item, client, namespace=namespace, name=name)

    @property
    def spec(self) -> StudySpec:
        return StudySpec().copy_from(self._object.spec)

    @property
    def status(self) -> StudyStatus:
        return StudyStatus().copy_from(self._object.status)

    def default(self):
        StudySpec().apply_config(self._object.spec)

    def abort(self):
        if hasattr(self, "_client"):
            self._client.abort(self.namespace, self.name)
        else:
            raise AttributeError("Object has no client repository")

    def pause(self):
        if hasattr(self, "_client"):
            self._client.pause(self.namespace, self.name)
        else:
            raise AttributeError("Object has no client repository")

    def resume(self):
        if hasattr(self._client, "abort"):
            self._client.resume(self.namespace, self.name)
        else:
            raise AttributeError("Object has no client repository")

    @property
    def models(self) -> List[Model]:
        if hasattr(self, "_client"):
            return self._client.modela.Models.list(self.namespace, {'study': self.name})
        else:
            raise AttributeError("Object has no client repository")

    @property
    def best_model(self) -> Model:
        if hasattr(self, "_client"):
            return self._client.modela.Models.get(self.namespace, self._object.status.bestModel)
        else:
            raise AttributeError("Object has no client repository")



class StudyClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: StudyServiceStub = stub

    def create(self, study: Study) -> bool:
        request = CreateStudyRequest()
        request.study.CopyFrom(study.raw_message)
        try:
            response = self.__stub.CreateStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, study: Study) -> bool:
        request = UpdateStudyRequest()
        request.study.CopyFrom(study.raw_message)
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
            return Study(response.study, self)
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
            response = self.__stub.ListStudies(request)
            return [Study(item, self) for item in response.studies.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def abort(self, namespace: str, name: str) -> bool:
        request = AbortStudyRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.AbortStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def pause(self, namespace: str, name: str) -> bool:
        request = PauseStudyRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.PauseStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def resume(self, namespace: str, name: str) -> bool:
        request = ResumeStudyRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.ResumeStudy(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get_profile(self, namespace: str, name: str, models: int) -> bool:
        request = GetStudyProfileRequest()
        request.namespace = namespace
        request.name = name
        request.models = models
        try:
            response = self.__stub.GetStudyProfile(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def create_profile(self, namespace: str, name: str) -> bool:
        request = CreateStudyProfileRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.CreateStudyProfile(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False
