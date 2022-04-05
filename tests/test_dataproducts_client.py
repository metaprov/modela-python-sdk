import time
import unittest

from modela import *
from modela.ModelaException import *
from modela.common import PriorityLevel
from modela.data.DataProduct import DataProduct
from modela.data.common import DataType
from modela.data.models import DataProductSpec
from modela.server import Modela
from modela.training.common import Imputation, TaskType


class Test_Modela_dataproduct(unittest.TestCase):
    """Tests for `modela.data.DataProduct`"""

    @classmethod
    def setUpClass(cls):
        cls.modela = Modela(port_forward=True)

    @classmethod
    def tearDownClass(cls):
        cls.modela.close()

    def test_0_create(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test",
                                              serving_site="default-serving-site",
                                              public=True,
                                              task_type=TaskType.Regression,
                                              default_training_workload=Workload("general-small"),
                                              default_resource_workload=Workload("general-small"),
                                              default_bucket="test",

        )
        assert type(dataproduct) == DataProduct
        dataproduct.submit(replace=True)

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
