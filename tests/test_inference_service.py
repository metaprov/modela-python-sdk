import unittest

from modela.ModelaException import *
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.training.Model`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_infer(self):
        self.modela.InferenceService.predict("iris-product", "model-20220219-002120",
                                             "{\"sepal_length\":4.6, \"sepal_width\":3.2, \"petal_length\":1.0, \"petal_width\":0.3}")
