import hashlib
from typing import List

import grpc
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1 import grpcinferenceservice_pb2_grpc
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1.grpcinferenceservice_pb2 import PredictRequest
from github.com.metaprov.modelaapi.services.grpcinferenceservice.v1.grpcinferenceservice_pb2_grpc import \
    GRPCInferenceServiceStub

from modela.ModelaException import ModelaException




class InferenceService:
    def __init__(self, host, port=3000):
        self._channel = grpc.insecure_channel(f'{host}:{port}')
        self._stub = grpcinferenceservice_pb2_grpc.GRPCInferenceServiceStub(self._channel)

    def close(self):
        """Closes Dapr runtime gRPC channel."""
        if self._channel:
            self._channel.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def predict(self,
                namespace: str,
                name: str,
                payload: str,
                validate: bool = True,
                explain: bool = False,
                format: str = "json",
                labeled: bool = False,
                metrics: List[str] = []
                ):
        request = PredictRequest(namespace=namespace, name=name, validate=validate, explain=explain, format=format,
                                 payload=payload, labeled=labeled)
        request.metrics.extend(metrics)
        try:
            response = self._stub.Predict(request)
            print(response)
            return response
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
