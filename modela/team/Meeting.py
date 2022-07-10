from typing import List, Union

import grpc
from github.com.metaprov.modelaapi.pkg.apis.team.v1alpha1.generated_pb2 import Meeting as MDMeeting
from github.com.metaprov.modelaapi.services.meeting.v1.meeting_pb2 import CreateMeetingRequest, \
    UpdateMeetingRequest, \
    DeleteMeetingRequest, GetMeetingRequest, ListMeetingsRequest
from github.com.metaprov.modelaapi.services.meeting.v1.meeting_pb2_grpc import MeetingServiceStub

from modela.ModelaException import ModelaException
from modela.Resource import Resource


class Meeting(Resource):
    def __init__(self, item: MDMeeting = MDMeeting(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class MeetingClient:
    def __init__(self, stub, modela):
        self.modela = modela
        self.__stub: MeetingServiceStub = stub

    def create(self, meeting: Meeting) -> bool:
        request = CreateMeetingRequest()
        request.meeting.CopyFrom(meeting.raw_message)
        try:
            response = self.__stub.CreateMeeting(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, meeting: Meeting) -> bool:
        request = UpdateMeetingRequest()
        request.meeting.CopyFrom(meeting.raw_message)
        try:
            self.__stub.UpdateMeeting(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Meeting, bool]:
        request = GetMeetingRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetMeeting(request)
            return Meeting(response.meeting, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteMeetingRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteMeeting(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Meeting], bool]:
        request = ListMeetingsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListMeetings(request)
            return [Meeting(item, self) for item in response.meetings.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


