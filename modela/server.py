import grpc

from typing import List, Optional,Union
from grpc import (  # type: ignore
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor,
)


from github.com.metaprov.modelaapi.services.account.v1 import account_pb2_grpc
from github.com.metaprov.modelaapi.services.dataproduct.v1 import dataproduct_pb2_grpc
from github.com.metaprov.modelaapi.services.datasource.v1 import datasource_pb2_grpc

from modela.Accounts import *
from modela.DataProducts import *
from modela.DataSources import  *

class Modela:
    def __init__(
        self,
        host="localhost",
        port=3000,
        interceptors: Optional[
            List[
                Union[
                    UnaryUnaryClientInterceptor,
                    UnaryStreamClientInterceptor,
                    StreamUnaryClientInterceptor,
                    StreamStreamClientInterceptor,
                ]
            ]
        ] = None,
    ):
        """Initializer.
           Creates a gRPC channel for connecting to the server.
           Adds the channel to the generated client stub.

        Arguments:
            None.

        Returns:
            None.
        """
        self._channel = grpc.insecure_channel('{0}:{1}'.format(host, port))

        if interceptors:
            self._channel = grpc.intercept_channel(  # type: ignore
                self._channel, *interceptors
            )

        self.__accounts_stub = account_pb2_grpc.AccountServiceStub(self._channel)
        self.__account_client = AccountClient(self.__accounts_stub)
        self.__dataproducts_stub = dataproduct_pb2_grpc.DataProductServiceStub(self._channel)
        self.__dataproducts_client = DataProductClient(self.__dataproducts_stub)
        self.__datasources_stub = datasource_pb2_grpc.DataSourceServiceStub(self._channel)
        self.__datasources_client = DataSourceClient(self.__datasources_stub)

    @property
    def Accounts(self):
        return self.__account_client

    def Account(self, namespace="", name="") -> Account:
        return Account(MDAccount(), self.Accounts, namespace=namespace, name=name)

    @property
    def DataProducts(self):
        return self.__dataproducts_client

    def DataProduct(self, namespace="", name="") -> DataProduct:
        return DataProduct(MDDataProduct(), self.DataProducts, namespace, name)

    @property
    def DataSources(self):
        return self.__datasources_client

    def DataSource(self, namespace="", name="") -> DataSource:
        return DataSource(MDDataSource(), self.DataSources, namespace, name)

    def close(self):
        if self._channel:
            self._channel.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
