import grpc
from github.com.metaprov.modelaapi.pkg.apis.infra.v1alpha1.generated_pb2 import Account as MDAccount
from github.com.metaprov.modelaapi.services.account.v1.account_pb2_grpc import AccountServiceStub
from github.com.metaprov.modelaapi.services.account.v1.account_pb2 import CreateAccountRequest, UpdateAccountRequest, \
    DeleteAccountRequest, GetAccountRequest, ListAccountsRequest
from typing import List
from modela.Resource import Resource


class Account(Resource):
    def __init__(self, item: MDAccount = None, client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class AccountClient:
    def __init__(self, stub):
        self.__stub: AccountServiceStub = stub

    def create(self, account: Account, password: str = "") -> None:
        request = CreateAccountRequest()
        request.item.CopyFrom(account.raw_message)
        request.password = password
        try:
            response = self.__stub.CreateAccount(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def update(self, account: Account) -> None:
        request = UpdateAccountRequest()
        request.item = account.raw_message
        try:
            self.__stub.UpdateAccount(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get(self, namespace: str, name: str) -> Account:
        request = GetAccountRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetAccount(request)
            return Account(response.item, self)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def delete(self, namespace: str, name: str) -> None:
        request = DeleteAccountRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteAccount(request)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

    def list(self, namespace: str):
        request = ListAccountsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListAccounts(request)
            return response.items.items
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False

