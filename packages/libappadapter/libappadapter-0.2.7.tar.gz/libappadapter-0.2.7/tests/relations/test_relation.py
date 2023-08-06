import unittest
import json

from libappadapter import AppConfig, get_constraint_app_templates, AppType
from libappadapter.relations import relation
from tests.basecase import BaseTestCase
from libappadapter.relations.relations import DependenceRelation, ShareRelation


class RelationCase(BaseTestCase):
    def setUp(self):
        self.db1 = AppConfig('appdb1', 'INCEPTOR', version='5.0')
        self.db2 = AppConfig('appdb2', 'INCEPTOR', version='5.0')
        self.hdfs1 = AppConfig('apphdfs1', 'HDFS', version='5.0')
        self.hdfs2 = AppConfig('apphdfs2', 'HDFS', version='5.0')
        self.db3 = AppConfig('appdb3', 'INCEPTOR')

    def test_relation_types(self):
        dep1 = DependenceRelation(self.db1, self.hdfs1)
        dep2 = DependenceRelation(self.db1, self.hdfs1)
        dep3 = DependenceRelation(self.db1, self.hdfs2)

        self.assertTrue(dep1 == dep2)
        self.assertTrue(dep1 != dep3)

        share1 = ShareRelation([self.db1, self.db2], 'metastore')
        share2 = ShareRelation([self.db2, self.db1], 'metastore')
        share3 = ShareRelation([self.db1, self.db3], 'metastore')

        self.assertTrue(share1 == share2)
        self.assertTrue(share1 != share3)

    def test_share(self):
        template = get_constraint_app_templates(
            apps=[self.hdfs1, self.hdfs2],
            relations=[
                relation.share([self.hdfs1, self.hdfs2], 'zookeeper')
            ]
        )

        apphdfs1 = template['apphdfs1']
        apphdfs2 = template['apphdfs2']

        self._assert_instance_equals(apphdfs1, 'zookeeper', 'apphdfs1-zookeeper')
        self._assert_instance_equals(apphdfs1, 'hdfs', 'apphdfs1-hdfs')

        try:
            self._assert_instance_equals(apphdfs2, 'zookeeper', 'apphdfs2-zookeeper')
        except KeyError:
            pass
        self._assert_instance_equals(apphdfs2, 'hdfs', 'apphdfs2-hdfs')
        self._assert_dep_equals(apphdfs2, 'hdfs', 'zookeeper', 'apphdfs1-zookeeper')

    def test_constraint_apps(self):
        templates = get_constraint_app_templates(
            apps=[self.db3, self.db1, self.db2, self.hdfs1, self.hdfs2],
            relations=[
                relation.depends_on(self.db1, self.hdfs1),
                relation.depends_on(self.db2, self.hdfs2),
                relation.share([self.hdfs1, self.hdfs2], 'zookeeper'),
                relation.share([self.db1, self.db2], 'metastore')
            ],
        )

        appdb1 = templates['appdb1']
        appdb2 = templates['appdb2']
        appdb3 = templates['appdb3']
        apphdfs1 = templates['apphdfs1']
        apphdfs2 = templates['apphdfs2']

        # hdfs1
        self._assert_instance_equals(apphdfs1, 'zookeeper', 'apphdfs1-zookeeper')
        self._assert_instance_equals(apphdfs1, 'hdfs', 'apphdfs1-hdfs')
        self._assert_dep_equals(apphdfs1, 'hdfs', 'zookeeper', 'apphdfs1-zookeeper')

        # hdfs2
        try:
            self._assert_instance_equals(apphdfs2, 'zookeeper', 'apphdfs1-zookeeper')
        except KeyError:
            pass
        self._assert_instance_equals(apphdfs2, 'hdfs', 'apphdfs2-hdfs')
        self._assert_dep_equals(apphdfs2, 'hdfs', 'zookeeper', 'apphdfs1-zookeeper')

        # db1
        self._assert_instance_equals(appdb1, 'metastore', 'appdb1-metastore')
        self._assert_dep_equals(appdb1, 'metastore', 'hdfs', 'apphdfs1-hdfs')
        self._assert_instance_equals(appdb1, 'inceptor', 'appdb1-inceptor')
        self._assert_dep_equals(appdb1, 'inceptor', 'metastore', 'appdb1-metastore')
        self._assert_dep_equals(appdb1, 'inceptor', 'zookeeper', 'apphdfs1-zookeeper')

        # db2
        try:
            self._assert_instance_equals(appdb2, 'metastore', 'appdb1-metastore')
        except KeyError:
            pass
        self._assert_instance_equals(appdb2, 'inceptor', 'appdb2-inceptor')
        self._assert_dep_equals(appdb2, 'inceptor', 'metastore', 'appdb1-metastore')
        self._assert_dep_equals(appdb2, 'inceptor', 'zookeeper', 'apphdfs1-zookeeper')

        # db3 (no dependent app)
        self._assert_instance_equals(appdb3, 'metastore', 'appdb3-metastore')
        self._assert_dep_equals(appdb3, 'metastore', 'hdfs', 'hdfs')
        self._assert_instance_equals(appdb3, 'inceptor', 'appdb3-inceptor')
        self._assert_dep_equals(appdb3, 'inceptor', 'metastore', 'appdb3-metastore')
        self._assert_dep_equals(appdb3, 'inceptor', 'zookeeper', 'hdfs-zookeeper')

    def test_app_config_options(self):
        kibana = AppConfig('kibana1', AppType.KIBANA, version='5.0', user_config={'use_search': True})
        search = AppConfig('search1', AppType.SEARCH, version='5.0')
        template = get_constraint_app_templates([search, kibana], auto_relation=True)
        search1 = template['search1']
        kibana1 = template['kibana1']
        self._assert_instance_equals(search1, 'elasticsearch', 'search1-elasticsearch')
        self._assert_dep_equals(kibana1, 'kibana', 'elasticsearch', 'search1-elasticsearch')

    def test_auto_relation(self):
        kibana = AppConfig('kibana1', AppType.KIBANA, version='5.0')
        search = AppConfig('search1', AppType.SEARCH, version='5.0')
        template = get_constraint_app_templates([search, kibana], auto_relation=True)
        search1 = template['search1']
        kibana1 = template['kibana1']
        self._assert_instance_equals(search1, 'elasticsearch', 'search1-elasticsearch')
        self._assert_instance_equals(kibana1, 'kibana', 'kibana1-kibana')

if __name__ == '__main__':
    unittest.main()
