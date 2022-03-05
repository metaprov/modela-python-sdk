import time
import unittest

from modela.ModelaException import *
from modela.data.Dataset import Dataset
from modela.server import Modela
from modela import *
from modela.util import convert_size


class Test_Modela_dataset(unittest.TestCase):
    """Tests for `modela.data.DataSet`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create_datasource(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test-create-ds",
                                            infer_file='datasets/iris.csv',
                                            target_column="variety")
        try:
            datasource.delete()
            time.sleep(0.3)
        finally:
            pass
        datasource.submit()
        dataset = self.modela.Dataset(namespace="iris-product", name="test-ds", data_file='datasets/iris.csv',
                                      datasource=datasource, task_type=TaskType.MultiClassification)
        try:
            dataset.delete()
            time.sleep(0.2)
        finally:
            pass

        print(dataset._object)
        dataset.submit()


    def test_1_list(self):
        assert len(self.modela.Datasets.list("iris-product")) >= 1

    def test_1_print(self):
        print(self.modela.Datasets.list("iris-product")[-1])

    def test_1_profile(self):
        ds = self.modela.Datasets.list("iris-product")[1]
        print(ds._print_profile())

    def test_2_update(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test-ds")
        dataset.set_label("test2", "e")
        dataset.update()
        newds = self.modela.Dataset(namespace="iris-product", name="test-ds")
        assert newds.has_label("test2")

    def test_3_get(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test-ds")
        spec = dataset.spec
        assert type(spec) == DatasetSpec

    def test_4_delete(self):
        dataset = self.modela.Dataset(namespace="iris-product", name="test-ds")
        # dataset.delete()
        time.sleep(0.1)
        self.assertRaises(ResourceNotFoundException, self.modela.Datasets.get, "iris-product", "test-ds")




""" These tests should be run by an end-user. """
def test_viz():
    modela = Modela("localhost", 3000)
    datasource = modela.DataSource(namespace="iris-product", name="iris")
    dataset = modela.Dataset(namespace="iris-product", name="test-ds-5", data_file='tests/datasets/iris.csv',
                             datasource=datasource, task_type=TaskType.MultiClassification)


    dataset.submit_and_visualize(replace=True)
    modela.close()

