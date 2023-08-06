import json
import logging
import unittest

from libappadapter import *
from libappadapter import AppConfig
from libappadapter.exceptions import ApplicationNotFoundException
from tests.basecase import BaseTestCase

logger = logging.getLogger(__name__)


def pretty_result(result):
    return json.dumps(result, indent=2, sort_keys=True)


class ApplicationCase(BaseTestCase):
    def setUp(self):
        user_config = {
            'user_config': "{'group': 'admin'}"
        }
        app_config = {
            'Transwarp_Install_ID': "13141234125",
            'Transwarp_Cni_Network': "myPrivateNetwork"
        }
        self.inceptor_config = AppConfig(
            name='db1',
            template='INCEPTOR',
            version='5.0',
            app_config=app_config,
            user_config=user_config
        )
        self.hdfs_config = AppConfig(
            name='hdfs1',
            template='HDFS',
            version='1.0',
            app_config=app_config,
            user_config=user_config,
            development_mode=False,
        )

    def test_app_config(self):
        try:
            get_kube_configs(AppConfig(name='db1', template='APP_NOT_EXISTS', version='1.0'))
        except ApplicationNotFoundException:
            pass
        try:
            get_kube_configs(AppConfig(name='db1', template='INCEPTOR', version='VERSION_NOT_EXISTS'))
        except ApplicationNotFoundException:
            pass

    def test_templates_repo(self):
        from libappadapter.application.app_config import APPLICATION_TEMPLATES

        self.assertTrue(isinstance(APPLICATION_TEMPLATES, dict))
        self.assertTrue(isinstance(APPLICATION_TEMPLATES[AppType.INCEPTOR], list))

        print('Discovered application templates:')
        for i in APPLICATION_TEMPLATES:
            print('\t{0}: {1}'.format(i, ','.join(APPLICATION_TEMPLATES[i])))

    def test_single_app_template(self):
        result = get_app_template(self.inceptor_config)

        self._assert_instance_equals(result, 'metastore', 'db1-metastore')
        self._assert_dep_equals(result, 'metastore', 'hdfs', 'hdfs')

        self._assert_instance_equals(result, 'inceptor', 'db1-inceptor')
        self._assert_dep_equals(result, 'inceptor', 'metastore', 'db1-metastore')
        self._assert_dep_equals(result, 'inceptor', 'zookeeper', 'hdfs-zookeeper')

        self.assertEqual(result['instance_list'][0]['annotations']['user_config'], "{'group': 'admin'}")

    def test_kube_config_from_template(self):
        template = get_app_template(self.inceptor_config)

        instances = template['instance_list']
        for instance in instances:
            self.assertTrue('Transwarp_Cni_Network' in instance['instance_settings'])

        config = get_kube_configs_from_template(template)
        self.assertTrue('application-instance_list.json' in config)

        items = config['application-instance_list.json']['items']
        for item in items:
            metadata = item['metadata']
            self.assertEqual(metadata['annotations']['application_name'], 'db1')
            self.assertEqual(metadata['annotations']['application_type'], 'INCEPTOR')
            self.assertTrue(isinstance(metadata['annotations']['user_config'], unicode))

            ref = item['spec']['applicationRef']['name']
            instance_id = item['metadata']['name']
            if ref == 'metastore':
                self.assertEqual(instance_id, 'db1-metastore')
            elif ref == 'inceptor':
                self.assertEqual(instance_id, 'db1-inceptor')

    def test_kube_configs(self):
        import json
        template = get_app_template(self.inceptor_config)
        config1 = get_kube_configs_from_template(template)
        config2 = get_kube_configs(self.inceptor_config)
        self.assertEqual(json.dumps(config1, sort_keys=True, indent=2),
                         json.dumps(config2, sort_keys=True, indent=2))

    def test_app_tcu(self):
        tcu = calculate_app_tcu(self.hdfs_config)
        self.assertEqual(tcu['hdfs']['c'], 3)
        self.assertEqual(tcu['hdfs']['m'], 6)
        self.assertEqual(tcu['hdfs']['s'], 6)
        self.assertEqual(tcu['zookeeper']['c'], 0.5)
        self.assertEqual(tcu['zookeeper']['m'], 1)
        self.assertEqual(tcu['zookeeper']['s'], 1)


if __name__ == '__main__':
    unittest.main()
