import unittest

from modela.ModelaException import *
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.training.Model`"""

    def setUp(self):
        self.modela = Modela(port_forward=True, username="admin", password="admin")

    def tearDown(self):
        self.modela.close()

    def test_0_list(self):
        assert len(self.modela.Models.list("iris-product")) >= 1

    def test_0_print_details(self):
        model = self.modela.Models.list("iris-product")[-1]
        print(model.details)


    def test_1_get(self):
        model = self.modela.Models.list("iris-product")[0]
        spec = model.spec
        print(model)
        assert type(spec) == ModelSpec
