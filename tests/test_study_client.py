import time
import unittest

from modela.ModelaException import *
from modela.training.Study import Study
from modela.server import Modela
from modela.training.models import StudySpec, ModelSearch, Ensemble, Training, DataSplit
from modela import *


class Test_Modela_study(unittest.TestCase):
    """Tests for `modela.training.Study`"""

    @classmethod
    def setUpClass(cls):
        cls.modela = Modela(port_forward=True)

    @classmethod
    def tearDownClass(cls):
        cls.modela.close()

    def test_0_create(self):
        study = self.modela.Study(namespace="iris-product", name="test")
        study.spec.Location = DataLocation(BucketName="test")
        assert type(study) == Study
        # study.submit(replace=True)
        Study(client=self.modela.Studies,
              name="test",
              namespace="iris-product",
              dataset="iris",
              task_type=TaskType.MultiClassification,
              objective=Metric.Accuracy,
              bucket="default-minio-bucket",
              search=ModelSearch(MaxTime=200, MaxModels=2, Trainers=2,
                                 SearchSpace=AlgorithmSearchSpace(
                                     Allowlist=[ClassicEstimator.LogisticRegression]))).submit(replace=True)

    def test_1_list(self):
        assert len(self.modela.Studies.list("iris-product")) >= 1

    def test_2_update(self):
        study = self.modela.Study(namespace="iris-product", name="test")
        study.set_label("test", "e")
        study.update()
        newds = self.modela.Study(namespace="iris-product", name="test")
        assert newds.has_label("test")

    def test_3_get(self):
        study = self.modela.Study(namespace="iris-product", name="test")
        spec = study.spec
        assert type(spec) == StudySpec

    def test_4_delete(self):
        study = self.modela.Study(namespace="iris-product", name="test")
        study.delete()
        self.assertRaises(ResourceNotFoundException, self.modela.Studies.get, "iris-product", "test")

    def test_5_get_models(self):
        study = self.modela.Studies.list("iris-product")[0]
        assert len(study.models) > 0


""" These tests should be run by an end-user. """


def test_viz():
    modela = Modela("localhost", 3000)
    study = modela.Study(
        name="test-study-2",
        namespace="iris-product",
        dataset="iris",
        task_type=TaskType.MultiClassification,
        objective=Metric.Accuracy,
        bucket="default-minio-bucket",
        search=ModelSearch(MaxTime=200, MaxModels=8, Trainers=4))

    study.submit_and_visualize(replace=True)
    modela.close()
