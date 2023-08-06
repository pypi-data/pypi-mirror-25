import json
import logging
import unittest

from libappadapter.k8s.utils import amount_to_float, format_amount
from tests.basecase import BaseTestCase

logger = logging.getLogger(__name__)


def pretty_result(result):
    return json.dumps(result, indent=2, sort_keys=True)


class UtilsCase(BaseTestCase):
    def setUp(self):
        self.unitstr_1 = "12288Mi"
        self.unitstr_2 = "2457.56Ki"
        self.unitstr_3 = "0.00087891Ki"
        self.unitstr_4 = "1048576G"
        self.unitstr_5 = "12288MB"
        self.unitstr_6 = "12288mb"
        self.unitstr_cpu_1 = "1000m"
        self.unitstr_cpu_2 = "0.192"
        self.unitstr_cpu_3 = "10"
        self.unitstr_int = 0
        self.unitstr_invalid = "100Invalid"

    def test_amount_to_float(self):
        self.assertEqual(amount_to_float(self.unitstr_1), float(12884901888))
        self.assertEqual(amount_to_float(self.unitstr_2), 2516541.44)
        self.assertEqual(amount_to_float(self.unitstr_5), float(12884901888))
        self.assertEqual(amount_to_float(self.unitstr_6), float(12884901888))
        self.assertEqual(amount_to_float(self.unitstr_cpu_1), 1)
        self.assertEqual(amount_to_float(self.unitstr_cpu_2), 0.192)
        self.assertEqual(amount_to_float(self.unitstr_int), 0)

    def test_convert_unit(self):
        self.assertEqual(format_amount(self.unitstr_1), "12GB")
        self.assertEqual(format_amount(self.unitstr_2), "2.4MB")
        self.assertEqual(format_amount(self.unitstr_3), "0.9B")
        self.assertEqual(format_amount(self.unitstr_4), "1024TB")
        self.assertEqual(format_amount(self.unitstr_cpu_1), "1")
        self.assertEqual(format_amount(self.unitstr_cpu_2), "0.19")
        self.assertEqual(format_amount(self.unitstr_cpu_3), "10")
        self.assertEqual(format_amount(self.unitstr_int), "0")
        self.assertEqual(format_amount(self.unitstr_invalid), "100Invalid")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
