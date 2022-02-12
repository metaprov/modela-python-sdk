import unittest

from modela.ModelaException import *
from modela.data.DataSource import DataSource
from modela.data.common import DataType
from modela.data.models import DataSourceSpec, Column
from modela.server import Modela
from modela.training.common import Imputation


class Test_Modela_datasource(unittest.TestCase):
    """Tests for `modela.data.DataSource`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        try:
            datasource.delete()
        finally:
            pass
        assert type(datasource) == DataSource
        datasource.submit()

    def test_1_list(self):
        assert len(self.modela.DataSources.list("iris-product")) >= 1

    def test_2_update(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        datasource.spec.Schema.Columns.append(
            Column("col", DataType.Text, Imputation=Imputation.ReplaceWithMean, SkewThreshold=4, Enum=["1", "2"]))
        datasource.update()
        newds = self.modela.DataSource(namespace="iris-product", name="test")
        assert len(newds._object.spec.schema.columns) == 1

    def test_3_get(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        spec = datasource.spec
        assert type(spec) == DataSourceSpec

    def test_4_delete(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        datasource.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.DataSources.get, "iris-product", "test")
