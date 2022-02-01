import grpc
from github.com.metaprov.modelaapi.pkg.apis.infra.v1alpha1.generated_pb2 import Account
from github.com.metaprov.modelaapi.services.account.v1.account_pb2_grpc import AccountServiceStub
from github.com.metaprov.modelaapi.services.account.v1.account_pb2 import CreateAccountRequest,UpdateAccountRequest,DeleteAccountRequest,GetAccountRequest,ListAccountsRequest

import github.com.metaprov.modelaapi as mdapi


class AccountClient:

    def __init__(self,stub):
        self.__stub:AccountServiceStub = stub


    def create_account(self,account:Account,password:str) -> None: 

        request = CreateAccountRequest()
        request.item.CopyFrom(account)
        request.password = password
        try:
            response = self.__stub.CreateAccount(request)   
            print(response)         
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            
        

    def update_account(self,account:Account) ->None:
        request = UpdateAccountRequest()
        request.item.CopyFrom(account)
        try:
            self.__stub.UpdateAccount(account)            
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            
        

    def get_account(self,ns:str,name:str) -> Account:
        request = GetAccountRequest()
        request.namespace = ns
        request.name      = name
        try:
            response = self.__stub.GetAccount(request) 
            return response.item           
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            
    

    def delete_account(self,ns:str,name:str) ->None:
        request = DeleteAccountRequest()
        request.namespace = ns
        request.name      = name
        try:
            response = self.__stub.GetAccount(request)            
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
            return False
    





