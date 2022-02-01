from modela_python_sdk.server import ModelaServer
from k8s.io.apimachinery.pkg.apis.meta.v1.generated_pb2 import ObjectMeta
from github.com.metaprov.modelaapi.pkg.apis.infra.v1alpha1.generated_pb2 import Account

def test_account_crud():
    modela_service = ModelaServer("localhost",3000)
    account = Account()
    account.metadata.CopyFrom(ObjectMeta())
    account.metadata.name = "test2"
    account.metadata.namespace = "default-tenant"
    modela_service.accounts.create_account(account,"test2")
    # get the account
    get_account_result = modela_service.accounts.get_account("default-tenant","test2")
    assert get_account_result != None
    # update the account
    get_account_result.spec.email="test@acme.com"
    get_account_result = modela_service.accounts.update_account(get_account_result)





        
