import unittest

from modela.ModelaException import *
from modela.training.Study import Study
from modela.server import Modela
from modela.training.models import StudySpec, ModelSearch, Ensemble, Training, DataSplit


class Test_Modela_study(unittest.TestCase):
    """Tests for `modela.training.Study`"""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        self.modela.close()

    def test_0_create(self):
        study = self.modela.Study(namespace="iris-product", name="test")
        try:
            study.delete()
        finally:
            pass
        assert type(study) == Study
        study.submit()
        Study(client=self.modela.Studies,
              search=ModelSearch(MaxTime=200, MaxModels=10), Ensemble=Ensemble(Enabled=True, Top=3),
              training_parameters=Training(Split=DataSplit()), )

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
        print(study.best_model.name)