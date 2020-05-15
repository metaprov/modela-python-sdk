import grpc

from proto import prediction_server_pb2, prediction_server_pb2_grpc

SERVER_ADDRESS = '0.0.0.0'
PORT = 8080


class PredictionServerClient(object):
    def __init__(self,host,port=3000):
        """Initializer.
           Creates a gRPC channel for connecting to the server.
           Adds the channel to the generated client stub.
        Arguments:
            None.

        Returns:
            None.
        """
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = prediction_server_pb2_grpc.PredictionServerStub(self.channel)


    def predict(self,name:str,columns:str,features:str,full:bool) -> str:
        request = prediction_server_pb2.PredictionRequest(
            name=name,columns=columns,features=features,full=full
        )

        try:
            response = self.stub.Predict(request)
            return response
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member


    def batch_predict(self,url:str) -> str:
        """Make a batch prediction.
                Arguments:
                    url: The resource name of a user.

                Returns:
                    a url for the result.
                """
        request = prediction_server_pb2.BatchPredictRequest(
            url=url
        )

        try:
            response = self.stub.BatchPredict(request)
            return response
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member



    def get_product_metadata(self) -> str:
        """Gets the product metadata.
                Arguments:
                    name: The resource name of a user.

                Returns:
                    a json string describing the product
                """

        request = prediction_server_pb2.GetProductRequest()
        try:
            response = self.stub.GetProduct(request)
            return response.content
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get_schema_metadata(self) -> str:
        """Gets the schema metadata
                Arguments:
                    None

                Returns:
                    a json string describing the schema for this predictor
           """
        request = prediction_server_pb2.GetSchemaRequest()
        try:
            response = self.stub.GetSchema(request)
            return response.content
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get_dataset_metadata(self) -> str:
        """Gets the dataset metadata.
                Arguments:
                    None

                Returns:
                    a json string describing the dataset for this predictor
                """
        request = prediction_server_pb2.GetSchemaRequest()
        try:
            response = self.stub.GetSchema(request)
            return response.content
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def get_model(self) -> str:
        """Gets the model metadata
                Arguments:
                    None

                Returns:
                    a json string describing the model for this predictor
                """
        request = prediction_server_pb2.GetSchemaRequest()
        try:
            response = self.stub.GetSchema(request)
            return response.content
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member


    def get_stat(self) -> str:
        """Gets a user.
                Arguments:
                    None
                Returns:
                    a json statistics string
                """
        request = prediction_server_pb2.GetStatRequest()
        try:
            response = self.stub.GetStat(request)
            return response.content
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member


