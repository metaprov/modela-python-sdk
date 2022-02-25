import unittest

from modela.ModelaException import *
from modela.inference.InferenceService import InferenceService
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint
from modela import *

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.training.Model`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000, username="admin", password="admin")

    def tearDown(self):
        self.modela.close()

    def test_connect_predictor(self):
        print(self.modela)
        predictor = self.modela.Predictor("iris-product", "test-predictor")
        #serve = predictor.connect(node_ip="172.21.52.228")
        serve = InferenceService("172.21.52.228", "30661")
        predictions = serve.predict("iris-product", "model-20220219-002120",
                                             "[{\"sepal.length\":4.6, \"sepal.width\":3.2, \"petal.length\":1.0, \"petal.width\":0.3}]",
                                    explain=True)
        assert predictions[0].Label == "Setosa"
