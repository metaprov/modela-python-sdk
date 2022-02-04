import grpc
from github.com.metaprov.modelaapi.pkg.apis.infra.v1alpha1.generated_pb2 import Account as MDAccount
from github.com.metaprov.modelaapi.services.account.v1.account_pb2_grpc import AccountServiceStub
from github.com.metaprov.modelaapi.services.account.v1.account_pb2 import CreateAccountRequest, \
    UpdateAccountRequest, \
    DeleteAccountRequest, GetAccountRequest, ListAccountsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class Account(Resource):
    def __init__(self, item: MDAccount = MDAccount(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class AccountClient:
    """
    AccountClient provides a CRUD interface for the Data Product resource.
    """

    def __init__(self, stub):
        self.__stub: AccountServiceStub = stub

    def create(self, account: Account, password: str = "") -> bool:
        request = CreateAccountRequest()
        request.item.CopyFrom(Account.raw_message)
        request.password = password
        try:
            response = self.__stub.CreateAccount(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, account: Account) -> bool:
        request = UpdateAccountRequest()
        request.item = Account.raw_message
        try:
            self.__stub.UpdateAccount(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[Account, bool]:
        request = GetAccountRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetAccount(request)
            return Account(response.item, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteAccountRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteAccount(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[Account], bool]:
        request = ListAccountsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListAccounts(request)
            return [Account(item, self) for item in response.items.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


