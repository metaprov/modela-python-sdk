import unittest

from modela.ModelaException import *
from modela.training.Model import Model
from modela.server import Modela
from modela.training.models import ModelSpec
import pprint

class Test_Modela_model(unittest.TestCase):
    """Tests for `modela.training.Model`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_upload(self):
        self.modela.FileService.upload_file("test", "test123", "default-tenant", "iris-product", "v0.0.1",
                                            "default-minio-bucket", "dataset", "test")
