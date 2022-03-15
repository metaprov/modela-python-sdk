import unittest

from modela.ModelaException import *
from modela.inference.Predictor import Predictor
from modela.inference.models import PredictorSpec
from modela.server import Modela
from modela import *


class Test_Modela_predictor(unittest.TestCase):
    """Tests for `modela.inference.Predictor`"""

    @classmethod
    def setUpClass(cls):
        cls.modela = Modela(port_forward=True)

    @classmethod
    def tearDownClass(cls):
        cls.modela.close()

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

    def test_5_predict(self):
        predictor = self.modela.Predictor(namespace="iris-product", name="testpred", model="model-20220303-194814")
        predictor.submit(replace=True)
        print(predictor.model.dataset.datasource.schema.Columns[-1].Enum)
        predictor.wait_until_ready()
        predictor.predict(predictor.model.test_prediction)
        predictor.delete()

