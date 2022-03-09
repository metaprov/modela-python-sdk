from modela import Modela
from modela.inference.InferenceService import InferenceService

Prediction = "[{\"sepal.length\":4.6, \"sepal.width\":3.2, \"petal.length\":1.0, \"petal.width\":0.3}]"

client = Modela("modela-api-gateway.vcap.me", secure=True, tls_cert='tests/api_server.crt',
                username="admin", password="admin")
predictor = client.Predictors.list(namespace="iris-product")[0]
predictor_service = predictor.connect(tls_cert='tests/inference_server.crt')
predictions = predictor_service.predict(Prediction)
print(predictions)