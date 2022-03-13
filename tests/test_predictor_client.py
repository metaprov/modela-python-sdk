import unittest

from modela.ModelaException import *
from modela.inference.Predictor import Predictor
from modela.inference.models import PredictorSpec
from modela.server import Modela
from modela import *


class Test_Modela_predictor(unittest.TestCase):
    """Tests for `modela.inference.Predictor`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="test")
        predictor.submit(replace=True)

    def test_1_list(self):
        assert len(self.modela.Predictors.list("iris-product")) >= 1

    def test_2_update(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="test")
        predictor.set_label("test", "e")
        predictor.update()
        newds = self.modela.Predictor(namespace="iris-product", name="test")
        assert newds.has_label("test")

    def test_3_get(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="test")
        spec = predictor.spec
        assert type(spec) == PredictorSpec

    def test_4_delete(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="test")
        predictor.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.Studies.get, "iris-product", "test")

    def test_5_connect(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="test")
        predictor.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.Studies.get, "iris-product", "test")


    def test_6_get_models(self):
        predictor = self.modela.Studies.list("iris-product")[0]
        assert len(predictor.models) > 0
        print(predictor.best_model.name)
