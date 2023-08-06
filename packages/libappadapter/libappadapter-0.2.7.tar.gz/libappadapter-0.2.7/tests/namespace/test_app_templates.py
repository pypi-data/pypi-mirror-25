import json
import logging
import unittest

from libappadapter import *
from libappadapter.exceptions import NamespaceConfigException
from tests.basecase import BaseTestCase

logger = logging.getLogger(__name__)


def pretty_result(result):
    return json.dumps(result, indent=2, sort_keys=True)


class NamespaceCase(BaseTestCase):
    def setUp(self):
        pass

    def test_namespace_config(self):
        try:
            get_kube_namespace_config("ockletester")
        except NamespaceConfigException, e:
            raise e

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
