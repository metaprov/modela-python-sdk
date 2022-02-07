import unittest
from modela.server import Modela

class Test_Modela_datasource(unittest.TestCase):
    """Tests for `modela` package."""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.modela.close()

    def test_datasource_create(self):
        #datasource = self.modela.DataSource(namespace="default-tenant", name="test")
        #assert datasource != None
        #datasource.submit(password="test")
        pass

    def test_datasource_update(self):
        pass

    def test_datasource_get(self):
        datasource = self.modela.DataSource(namespace="iris-product", name="test")
        datasource.spec.csvfile.nullValues = "test"
        print(type(datasource.spec.schema.columns))


    def test_datasource_delete(self):
        #datasource = self.modela.DataSource(namespace="default-tenant", name="test")
        #datasource.delete()
        pass

    def test_datasource_list(self):
        #print(len(self.modela.DataSource.list("default-tenant")))
        pass




