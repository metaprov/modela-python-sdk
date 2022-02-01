import grpc

from typing import List, Optional,Union
from grpc import (  # type: ignore
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor,
)


from github.com.metaprov.modelaapi.services.account.v1 import account_pb2_grpc

from modela_python_sdk.account_client import AccountClient
 

class ModelaServer:
    def __init__(
        self,
        host,
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
        self._channel = grpc.insecure_channel('localhost:3000')

        if interceptors:
            self._channel = grpc.intercept_channel(  # type: ignore
                self._channel, *interceptors
            )

        self.__accounts_stub = account_pb2_grpc.AccountServiceStub(self._channel)
        self.__account_client = AccountClient(self.__accounts_stub)

    @property
    def accounts(self):
        return self.__account_client

    def close(self):
        if self._channel:
            self._channel.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
