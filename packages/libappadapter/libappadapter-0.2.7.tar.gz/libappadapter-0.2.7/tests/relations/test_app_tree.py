import unittest
import json

from libappadapter.application import AppType
from libappadapter import AppConfig
from libappadapter.exceptions import InvalidDependenceException
from libappadapter.relations import relation
from libappadapter.relations.tree import ApplicationTree
from tests.basecase import BaseTestCase
from libappadapter.relations.relations import DependenceRelation, ShareRelation


class ApplicationTreeCase(BaseTestCase):
    def setUp(self):
        self.db1 = AppConfig('appdb1', 'INCEPTOR', version='5.0')
        self.db2 = AppConfig('appdb2', 'INCEPTOR', version='5.0')
        self.hdfs = AppConfig('apphdfs1', 'HDFS', version='5.0')

    def test_constructor(self):
        tree = ApplicationTree([self.db1, self.db2, self.hdfs])
        self.assertEqual(len(tree.get_trees()), 3)
        self.assertEqual(len(tree.get_apps()), 3)

    def test_add_relation(self):
        dep1 = DependenceRelation(self.db1, self.hdfs)
        dep2 = DependenceRelation(self.db1, self.hdfs)
        dep3 = DependenceRelation(self.db2, self.hdfs)
        tree = ApplicationTree([self.db1, self.db2, self.hdfs],
                               relations=[dep1, dep2, dep3])
        self.assertTrue(len(tree.relations) == 2)

        share1 = ShareRelation([self.db1, self.db2], 'metastore')
        share2 = ShareRelation([self.db2, self.db1], 'metastore')
        share3 = ShareRelation([self.db1, self.db2], 'inceptor')
        tree = ApplicationTree([self.db1, self.db2, self.hdfs],
                               relations=[share1, share2, share3])
        self.assertTrue(len(tree.relations) == 2)

    def test_update_depends_relation(self):
        tree = ApplicationTree([self.db1, self.db2, self.hdfs])
        dep_relation = relation.depends_on(self.db1, self.hdfs)
        tree.update_depends_relation(relations=[dep_relation])

        self.assertEqual(len(tree.get_trees()), 2)
        self.assertEqual(len(tree.get_apps()), 3)

        node_db1 = tree.get_app(self.db1.name)
        template = node_db1.template
        self._assert_dep_equals(template, 'metastore', 'hdfs', 'apphdfs1-hdfs')
        self._assert_dep_equals(template, 'inceptor', 'zookeeper', 'apphdfs1-zookeeper')

    def test_update_share_relation(self):
        tree = ApplicationTree([self.db1, self.db2, self.hdfs])
        share_relation = relation.share([self.db1, self.db2], 'metastore')
        tree.update_share_relation([share_relation])

        self.assertEqual(len(tree.get_trees()), 3)
        self.assertEqual(len(tree.get_apps()), 3)

        template = tree.get_app(self.db2.name).template

        try:
            self._assert_instance_equals(template, 'metastore', 'appdb1-metastore')
        except KeyError:
            pass
        self._assert_dep_equals(template, 'inceptor', 'metastore', 'appdb1-metastore')
        self._assert_dep_equals(template, 'inceptor', 'zookeeper', 'hdfs-zookeeper')

    def test_validate_dependencies(self):
        """ Test mannual configuration of dependencies
        """
        tree = ApplicationTree([self.db1, self.db2, self.hdfs])
        try:
            tree._validate_dependencies()
        except InvalidDependenceException:
            pass

        tree.update_depends_relation(relations=[
            relation.depends_on(self.db1, self.hdfs),
            relation.depends_on(self.db2, self.hdfs),
        ])
        tree._validate_dependencies()

    def test_auto_dependencies(self):
        """ Test auto configuration of dependencies
        """
        tree = ApplicationTree([self.db1, self.db2, self.hdfs], auto_detection=True)
        self.assertEqual(len(tree.get_trees()), 2)

        template = tree.get_app(self.db1.name).template

        self._assert_dep_equals(template, 'metastore', 'hdfs', 'apphdfs1-hdfs')
        self._assert_dep_equals(template, 'inceptor', 'zookeeper', 'apphdfs1-zookeeper')

        template = tree.get_app(self.db2.name).template

        self._assert_dep_equals(template, 'metastore', 'hdfs', 'apphdfs1-hdfs')
        self._assert_dep_equals(template, 'inceptor', 'zookeeper', 'apphdfs1-zookeeper')

    def test_dependency_loop(self):
        kibana = AppConfig('kibana1', AppType.KIBANA, version='5.0', user_config={'use_search': True})
        search = AppConfig('search1', AppType.SEARCH, version='5.0')
        ApplicationTree([kibana, search], auto_detection=True)

if __name__ == '__main__':
    unittest.main()
