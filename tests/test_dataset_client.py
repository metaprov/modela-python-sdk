import unittest

from modela.ModelaException import *
from modela.data.Dataset import Dataset
from modela.server import Modela
from modela import *

class Test_Modela_dataset(unittest.TestCase):
    """Tests for `modela.data.DataSet`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test")
        try:
            dataset.delete()
        finally:
            pass
        assert type(dataset) == Dataset
        dataset.submit()

    def test_1_list(self):
        assert len(self.modela.Datasets.list("iris-product")) >= 1

    def test_2_update(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test")
        dataset.set_label("test", "e")
        dataset.update()
        newds = self.modela.Dataset(namespace="iris-product", name="test")
        assert newds.has_label("test")

    def test_3_get(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test")
        spec = dataset.spec
        assert type(spec) == DatasetSpec

    def test_4_delete(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test")
        dataset.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.Datasets.get, "iris-product", "test")
