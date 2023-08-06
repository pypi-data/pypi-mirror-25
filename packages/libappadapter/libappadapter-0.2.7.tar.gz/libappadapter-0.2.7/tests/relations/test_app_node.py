import unittest

from libappadapter import AppConfig
from libappadapter.relations.tree import ApplicationNode
from tests.basecase import BaseTestCase


class ApplicationNodeCase(BaseTestCase):
    def setUp(self):
        self.app_config = AppConfig('db1', 'INCEPTOR')

    def test_application_node(self):
        app_node = ApplicationNode(self.app_config)
        instances = app_node.get_instance_list(with_dependencies=True)

        for instance in instances:
            instance_name, instance_module = instance

            if instance_module == 'metastore':
                self.assertEqual(instance_name, u'db1-metastore')
            elif instance_module == 'inceptor':
                self.assertEqual(instance_name, u'db1-inceptor')

            deps = instances[instance]
            for dep in deps:
                dep_name, dep_module = dep
                if dep_module == 'zookeeper':
                    self.assertEqual(dep_name, u'hdfs-zookeeper')

    def test_add_child(self):
        app_node = ApplicationNode(self.app_config)
        child = ApplicationNode(AppConfig('hdfs1', 'HDFS'))
        app_node.add_child(child)
        template = app_node.template

        self._assert_dep_equals(template, 'metastore', 'hdfs', 'hdfs1-hdfs')
        self._assert_dep_equals(template, 'inceptor', 'zookeeper', 'hdfs1-zookeeper')
        self.assertTrue(app_node.is_root())
        self.assertTrue(child.is_leaf())
        self.assertTrue(app_node.is_ancestor(child))
        self.assertTrue(child.is_successor(app_node))

    def test_update_shared_module(self):
        app_node = ApplicationNode(self.app_config)
        removed_instances = app_node.replace_instance('zookeeper', 'other-zookeeper')

        self.assertTrue('hdfs-zookeeper' in removed_instances)
        self._assert_dep_equals(app_node.template, 'inceptor', 'zookeeper', 'other-zookeeper')

        app_node = ApplicationNode(self.app_config)
        app_node.replace_instance('metastore', 'other-metastore')
        self._assert_dep_equals(app_node.template, 'inceptor', 'metastore', 'other-metastore')

        app_node = ApplicationNode(self.app_config)
        app_node.replace_instance('metastore', 'db1-metastore')
        self._assert_dep_equals(app_node.template, 'inceptor', 'metastore', 'db1-metastore')
        self._assert_instance_equals(app_node.template, 'metastore', 'db1-metastore')

    def test_breadth_first_traversal(self):
        app_node = ApplicationNode(self.app_config)
        app_node.add_child(ApplicationNode(AppConfig('hdfs1', 'HDFS')))
        app_node.add_child(ApplicationNode(AppConfig('hdfs2', 'HDFS')))
        queue = app_node.breadth_first_traversal()
        self.assertEqual(queue[0].name, 'db1')
        self.assertEqual(queue[1].name, 'hdfs1')
        self.assertEqual(queue[2].name, 'hdfs2')


if __name__ == '__main__':
    unittest.main()
