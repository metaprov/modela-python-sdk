import time
import unittest

import pandas

from modela.ModelaException import *
from modela.data.DataSource import DataSource
from modela.data.common import DataType
from modela.data.models import DataSourceSpec, Column
from modela.server import Modela
from modela.training.common import Imputation


class Test_Modela_datasource(unittest.TestCase):
    """Tests for `modela.data.DataSource`"""

    @classmethod
    def setUpClass(cls):
        cls.modela = Modela(port_forward=True)

    @classmethod
    def tearDownClass(cls):
        cls.modela.close()

    def test_0_infer_api(self):
        with open('datasets/iris.csv') as f:
            data = f.read()

        loc = self.modela.FileService.upload_file("iris.csv", data, "default-tenant", "iris-product", "v0.0.1",
                                                  "default-minio-bucket", "datasources", "test")
        infer = self.modela.DataSources.infer("iris-product", loc)
        assert infer[0].Name == 'sepal.length'

    def test_0_create(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        assert type(datasource) == DataSource
        datasource.submit(replace=True)

    def test_0_create_infer_file(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test", infer_file='datasets/iris.csv',
                                            target_column="variety")
        assert datasource.spec.Schema.Columns[0].Name == 'sepal.length'
        assert datasource.spec.Schema.Columns[4].Target

    def test_0_create_infer_bytes(self):
        with open('datasets/iris.csv', 'rb') as f:
            data = f.read()

        datasource = self.modela.DataSource(namespace="iris-product", name="test", infer_bytes=data, target_column="variety")
        assert datasource.spec.Schema.Columns[0].Name == 'sepal.length'

    def test_0_create_infer_df(self):
        df = pandas.read_csv('datasets/iris.csv')
        datasource = self.modela.DataSource(namespace="iris-product", name="test", infer_dataframe=df, target_column="variety")
        assert datasource.spec.Schema.Columns[0].Name == 'sepal.length'

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
