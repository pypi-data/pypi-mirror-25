from unittest import TestCase


class BaseTestCase(TestCase):

    def _assert_dep_equals(self, app, instance, dependency, target_name):
        instance_list = app['instance_list']
        target_instance = [i for i in instance_list if i['moduleName'] == instance]
        assert len(target_instance) > 0
        module_list = target_instance[0]['dependencies']
        target_module = [i for i in module_list if i['moduleName'] == dependency]
        assert len(target_module) > 0
        self.assertEqual(target_module[0]['name'], target_name)

    def _assert_instance_equals(self, app, instance, target_name):
        instance_list = app['instance_list']
        target_instance = [i for i in instance_list if i['moduleName'] == instance]
        if len(target_instance) == 0:
            raise KeyError('instance {0} not found'.format(instance))
        self.assertEqual(target_instance[0]['name'], target_name)
