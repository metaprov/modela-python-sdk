import unittest

from modela.ModelaException import *
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.training.Model`"""

    @classmethod
    def setUpClass(cls):
        cls.modela = Modela(port_forward=True)

    @classmethod
    def tearDownClass(cls):
        cls.modela.close()

    def test_0_list(self):
        resource = self.modela.ModelAutobuilder(namespace="iris-product", name="test-mab",
                                                data_file="datasets/heart.csv",
                                                target_column="target")
        resource.submit()