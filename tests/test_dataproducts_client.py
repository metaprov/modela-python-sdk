import time
import unittest

from modela.ModelaException import *
from modela.common import PriorityLevel
from modela.data.DataProduct import DataProduct
from modela.data.common import DataType
from modela.data.models import DataProductSpec
from modela.server import Modela
from modela.training.common import Imputation


class Test_Modela_dataproduct(unittest.TestCase):
    """Tests for `modela.data.DataProduct`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        try:
            dataproduct.delete()
        finally:
            pass
        time.sleep(0.1)
        assert type(dataproduct) == DataProduct
        dataproduct.submit()

    def test_1_list(self):
        assert len(self.modela.DataProducts.list("default-tenant")) > 1

    def test_2_update(self):
        time.sleep(0.3)
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        assert dataproduct.spec.Priority == PriorityLevel.Medium
        dataproduct.spec.Priority = PriorityLevel.High
        dataproduct.update()
        newdp = self.modela.DataProduct(namespace="default-tenant", name="test")
        assert newdp._object.spec.priority == "high"

    def test_3_get(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        assert type(dataproduct.spec) == DataProductSpec

    def test_4_delete(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        dataproduct.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.DataProducts.get, "default-tenant", "test")
