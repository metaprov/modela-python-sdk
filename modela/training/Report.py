import grpc
from github.com.metaprov.modelaapi.pkg.apis.training.v1alpha1.generated_pb2 import Report as MDReport
from github.com.metaprov.modelaapi.services.report.v1.report_pb2_grpc import ReportServiceStub
from github.com.metaprov.modelaapi.services.report.v1.report_pb2 import CreateReportRequest, \
    UpdateReportRequest, \
    DeleteReportRequest, GetReportRequest, ListReportsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Report(Resource):
    def __init__(self, item: MDReport = MDReport(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class ReportClient:
    def __init__(self, stub):
        self.__stub: ReportServiceStub = stub

    def create(self, report: Report) -> bool:
        request = CreateReportRequest()
        request.item.CopyFrom(report.raw_message)
        try:
            response = self.__stub.CreateReport(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, report: Report) -> bool:
        request = UpdateReportRequest()
        request.item.CopyFrom(report.raw_message)
        try:
            self.__stub.UpdateReport(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Report, bool]:
        request = GetReportRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetReport(request)
            return Report(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteReportRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteReport(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Report], bool]:
        request = ListReportsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListReports(request)
            return [Report(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


