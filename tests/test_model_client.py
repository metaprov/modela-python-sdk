import unittest

from modela.ModelaException import *
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.data.DataSet`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_list(self):
        assert len(self.modela.Models.list("iris-product")) >= 1

    def test_1_get(self):
        list = self.modela.Models.list("iris-product")
        model = self.modela.Model(namespace="iris-product", name="model-20220211-184217")
        spec = model.spec
        prof = model.profile()
        assert type(spec) == ModelSpec
