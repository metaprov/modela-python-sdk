#!/usr/bin/env python

"""Tests for `modeld_python_sdk` package."""


import unittest
from modeld_python_sdk.client import ModeldGrpcClient


class TestModeld_python_client(unittest.TestCase):
    """Tests for `modeld_python_sdk` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_predict(self):
        client = ModeldGrpcClient("localhost",3000)
        payload = "[{\"sepal_length\":4.6, \"sepal_width\":3.2, \"petal_length\":1.0, \"petal_width\":0.3},{\"sepal_length\":1.6, \"sepal_width\":2.2, \"petal_length\":1.0, \"petal_width\":1.3}]"
        res = client.predict(payload)
        print(res)




