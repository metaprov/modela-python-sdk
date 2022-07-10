from typing import List, Union

import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Model as MDModel
from github.com.metaprov.modelaapi.services.model.v1.model_pb2 import \
    DeleteModelRequest, GetModelRequest, ListModelsRequest, \
    AbortModelRequest, CompileModelRequest, DeployModelRequest, DownloadModelRequest, \
    PauseModelRequest, GetModelProfileRequest, PublishModelRequest, ResumeModelRequest, TestModelRequest
from github.com.metaprov.modelaapi.services.model.v1.model_pb2_grpc import ModelServiceStub
from tabulate import tabulate

from modela.ModelaException import ModelaException
from modela.Resource import Resource
from modela.common import Metric
from modela.data.Dataset import Dataset
from modela.training.Report import Report
from modela.training.common import ModelPhase, TaskType
from modela.training.models import ModelSpec, ModelStatus, ModelProfile


class Model(Resource):
    def __init__(self, item: MDModel = MDModel(), client=None, namespace="", name=""):
        """
        The Model resource is a machine learning model generated by the Modela data plane. Models are immutable and
        cannot be changed once created.

        :param client: The Model client repository, which can be obtained through an instance of Modela.
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

    def profile(self) -> ModelProfile:
        self.ensure_client_repository()
        profile = self._client.profile(self.namespace, self.name)
        return ModelProfile().copy_from(profile)

    def abort(self):
        self.ensure_client_repository()
        self._client.abort(self.namespace, self.name)

    def pause(self):
        self.ensure_client_repository()
        self._client.pause(self.namespace, self.name)

    def resume(self):
        self.ensure_client_repository()
        self._client.resume(self.namespace, self.name)

    def compile(self, target, compiler):
        self.ensure_client_repository()
        self._client.compile(self.namespace, self.name, target, compiler)

    def publish(self):
        self.ensure_client_repository()
        self._client.publish(self.namespace, self.name)

    def test(self):
        self.ensure_client_repository()
        self._client.test(self.namespace, self.name)

    def download(self) -> bytes:
        self.ensure_client_repository()
        return self._client.download(self.namespace, self.name)

    def deploy(self, predictor: str, replicas: int = 0, traffic: int = 0, role: str = ""):
        if hasattr(self, "_client"):
            self._client.deploy(self.namespace, self.name, predictor, replicas, traffic, role)
        else:
            raise AttributeError("Object has no client repository")

    @property
    def test_prediction(self) -> str:
        """ Generate a default prediction payload for the model. """
        return self.dataset.test_prediction

    @property
    def report(self) -> Report:
        """ Return the report associated with the model, if it exists. """
        if hasattr(self, "_client"):
            if self._object.status.reportName != "":
                return self._client.modela.Report(namespace=self.namespace, name=self._object.status.reportName)
            else:
                print("Model {0} has no report. Call Model.test() to create one.")
        else:
            raise AttributeError("Object has no client repository")


    @property
    def dataset(self) -> Dataset:
        """ Return the dataset associated with the model """
        if hasattr(self, "_client"):
            return self._client.modela.Dataset(namespace=self.namespace, name=self.spec.DatasetName)
        else:
            raise AttributeError("Object has no client repository")


    @property
    def phase(self) -> ModelPhase:
        return self.status.Phase

    @property
    def details(self) -> str:
        """
        Generate a table about the details of the model.

        :return: A table of the model's metrics and hyperparameters
        """

        return "Estimator: {0} | Trial #: {1}\n".format(self.spec.Estimator.AlgorithmName, self.spec.TrialID) + \
                self.metrics + "\n" + self.hyperparameters

    @property
    def hyperparameters(self) -> str:
        """
        Generate a table with the hyperparameters of the model.
        """
        hyper_table = []
        for parameters in self.spec.Estimator.Parameters:
            hyper_table.append([parameters.Name, parameters.Value])

        return tabulate(hyper_table, tablefmt='psql', headers=['Hyperparameter', 'Value'])

    @property
    def metrics(self) -> str:
        """
        Generate a table with the metrics of the model.
        """
        test_table, headers, headers_as_metric, status = [], ['Metric'], [], self.status
        if self.spec.Task == TaskType.BinaryClassification:
            metrics = ['Accuracy', 'Auc', 'F1', 'Log Loss', 'Precision', 'Recall']
            headers_as_metric = [Metric.Accuracy, Metric.RocAuc, Metric.F1Binary, Metric.LogLoss, Metric.PrecisionBinary, Metric.RecallBinary]
            test_table = [[metric] for metric in metrics]
        elif self.spec.Task == TaskType.MultiClassification:
            metrics = ['Accuracy', 'F1 Micro', 'F1 Macro', 'F1 Weighted', 'Precision Macro', 'Precision Micro', 'Precision Weighted',
                       'Recall Macro', 'Recall Micro', 'Recall Weighted']
            headers_as_metric = [Metric.Accuracy, Metric.F1Micro, Metric.F1Macro, Metric.F1Weighted, Metric.PrecisionMacro, Metric.PrecisionMicro,
                                 Metric.PrecisionWeighted, Metric.RecallMacro, Metric.RecallMicro, Metric.RecallWeighted]
            test_table = [[metric] for metric in metrics]
        elif self.spec.Task == TaskType.Regression:
            headers = []

        if len(self.status.Cv) > 0:
            headers.append("Validation")
            for idx, metric in enumerate(headers_as_metric):
                test_table[idx].append([x for x in status.Cv if x.Metric == metric][0].Value)

        if len(self.status.Train) > 0:
            headers.append("Train")
            for idx, metric in enumerate(headers_as_metric):
                test_table[idx].append([x for x in status.Train if x.Metric == metric][0].Value)

        if len(self.status.Test) > 0:
            headers.append("Test")
            for idx, metric in enumerate(headers_as_metric):
                test_table[idx].append([x for x in self.status.Test if x.Metric == metric][0].Value)

        return tabulate(test_table, tablefmt='psql', headers=headers)

    def get_cv_metric(self, metric: Metric) -> float:
        out_metric = [x for x in self.status.Cv if x.Metric == metric]
        if len(out_metric) == 0:
            raise TypeError("{0} model does not have the {1} metric.".format(self.spec.Task.name, metric.name))

        return out_metric[0].Value

    def get_train_metric(self, metric: Metric) -> float:
        out_metric = [x for x in self.status.Train if x.Metric == metric]
        if len(out_metric) == 0:
            raise TypeError("{0} model does not have the {1} metric..".format(self.spec.Task.name, metric.name))

        return out_metric[0].Value

    def get_test_metric(self, metric: Metric) -> float:
        out_metric = [x for x in self.status.Test if x.Metric == metric]
        if len(out_metric) == 0:
            raise TypeError("{0} model does not have the {1} metric.".format(self.spec.Task.name, metric.name))

        return out_metric[0].Value

    def __repr__(self):
        return "<{0} model at {1}/{2}>".format(self.spec.Estimator.AlgorithmName, self.namespace, self.name)



class ModelClient:
    def __init__(self, stub, modela):
        self.__stub: ModelServiceStub = stub
        self.modela = modela

    def create(self, model: Model) -> bool:
        raise TypeError("Modela does not support the creation of custom models in this release.")
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

    def list(self, namespace: str, labels: dict = None) -> Union[List[Model], bool]:
        request = ListModelsRequest()
        request.namespace = namespace
        if labels is not None:
            request.labels.update(labels)

        try:
            response = self.__stub.ListModels(request)
            return [Model(item, self) for item in response.models.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def abort(self, namespace: str, name: str) -> bool:
        request = AbortModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.AbortModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def compile(self, namespace: str, name: str, target: str, compiler: str) -> bool:
        request = CompileModelRequest()
        request.namespace = namespace
        request.name = name
        request.target = target
        request.compiler = compiler
        try:
            response = self.__stub.CompileModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def deploy(self, namespace: str, name: str, predictor: str, replicas: int = 0,
               traffic: int = 0, role: str = "") -> bool:
        request = DeployModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeployModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def download(self, namespace: str, name: str) -> bytes:
        request = DownloadModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DownloadModel(request)
            return response.raw
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def pause(self, namespace: str, name: str) -> bool:
        request = PauseModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.PauseModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def resume(self, namespace: str, name: str) -> bool:
        request = ResumeModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.ResumeModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def test(self, namespace: str, name: str) -> bool:
        request = TestModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.TestModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def profile(self, namespace: str, name: str) -> bool:
        request = GetModelProfileRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetModelProfile(request)
            return response.profile
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def publish(self, namespace: str, name: str) -> bool:
        request = PublishModelRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.PublishModel(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


