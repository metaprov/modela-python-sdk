import unittest

from modela.ModelaException import *
from modela.data.DataProductVersion import DataProductVersion
from modela.data.common import DataType
from modela.data.models import DataProductVersionSpec, Column
from modela.server import Modela
from modela.training.common import Imputation


class Test_Modela_dataproductversion(unittest.TestCase):
    """Tests for `modela.data.DataProductVersion`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        dataproductversion = self.modela.DataProductVersion(namespace="iris-product", name="test")
        try:
            dataproductversion.delete()
        finally:
            pass
        assert type(dataproductversion) == DataProductVersion
        dataproductversion.submit()

    def test_1_list(self):
        assert len(self.modela.DataProductVersions.list("iris-product")) > 1

    def test_2_update(self):
        dataproductversion = self.modela.DataProductVersion(namespace="iris-product", name="test")
        dataproductversion.spec.Baseline = True
        dataproductversion.update()
        newdpv = self.modela.DataProductVersion(namespace="iris-product", name="test")
        assert newdpv._object.spec.baseline == True

    def test_3_get(self):
        dataproductversion = self.modela.DataProductVersion(namespace="iris-product", name="test")
        spec = dataproductversion.spec
        assert type(spec) == DataProductVersionSpec

    def test_4_delete(self):
        dataproductversion = self.modela.DataProductVersion(namespace="iris-product", name="test")
        dataproductversion.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.DataProductVersions.get, "iris-product", "test")
