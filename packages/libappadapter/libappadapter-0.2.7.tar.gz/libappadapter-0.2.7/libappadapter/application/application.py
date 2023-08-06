# Copyright 2017 Transwarp Inc. All rights reserved.
import json
import logging
import os

from .app_config import AppConfig
from ..helpers import evaluate_jsonnet_file
from ..settings import RootConfig

logger = logging.getLogger(__name__)
INSTANCE_ADVANCED_CONFIGS_DIR = 'instances/instance_advanced_configs'

__all__ = [
    "get_app_template",
    "get_kube_configs",
    "get_kube_configs_from_template",
    "get_app_advanced_configs",
    "get_all_apps_advanced_configs",
    "calculate_app_tcu",
]


def _sanitize_app_name(name):
    # TODO: validate application name
    return name


def get_app_template(app_config):
    """
    Get the dependency template of application.

    :param app_config: user-defined ``AppConfig``
    :return: application dependency object with ``instance_list``
    """
    tpl_name = app_config.template
    tpl_version = app_config.version
    tpl_path = os.path.join(RootConfig.APPLICATION_MAIN, tpl_name, tpl_version, 'dependency.jsonnet')

    # Configuration fields for `dependency.jsonnet`
    tpl_config = {
        'application_type': tpl_name,
        'application_name': _sanitize_app_name(app_config.name),
        'application_version': tpl_version,
        'user_config': app_config.user_config,
        'app_config': app_config.app_config,
        'development_mode': app_config.development_mode
    }

    result = evaluate_jsonnet_file(tpl_path, **tpl_config)

    # add extra app settings
    result.update(app_config.app_config)
    return result


def get_app_advanced_configs(app_config):
    """
    Get default advanced configs of a specific application
    :param app_config: ``AppConfig`` instance
    :return: dict object showing advanced configs of an application
    """
    app_version = app_config.version
    app_type = app_config.template
    app_template = get_app_template(app_config)

    app_configs = []
    for instance in app_template.get('instance_list', []):
        instance_type = instance.get('moduleName', '')
        instance_version = instance.get('version', '')
        if instance_type != '' and instance_version != '':
            instance_advanced_configs_path = os.path.join(RootConfig.TEMPLATES_FOLDER, INSTANCE_ADVANCED_CONFIGS_DIR,
                                                          instance_type, instance_version, 'advanced_configs.json')

            if os.path.exists(instance_advanced_configs_path):
                with open(instance_advanced_configs_path) as f:
                    instance_advanced_configs = json.load(f)
                app_configs.extend(instance_advanced_configs.get('configs', []))
            else:
                logger.warning('Default advanced configs NOT found for instance %s [%s]'
                               % (instance_type, instance_version))

    app_advanced_configs = {
        'configs': app_configs,
        'component_type': app_type,
        'component_version': app_version
    }

    return app_advanced_configs


def get_all_apps_advanced_configs():
    """
    Get default advanced configs of all the applications in templates/applications
    :return: a list of dict objects showing advanced configs of each application
    """
    apps_advanced_configs = []
    for app in os.listdir(RootConfig.APPLICATION_MAIN):
        # scan application versions
        for _version in os.listdir(os.path.join(RootConfig.APPLICATION_MAIN, app)):
            app_config = AppConfig(app, app, _version)
            app_advanced_configs = get_app_advanced_configs(app_config)
            apps_advanced_configs.append(app_advanced_configs)

    return apps_advanced_configs


def get_kube_configs_from_template(template=None, main_portal='main', version='1.0'):
    """
    Generate application template for kubernetes regarding to dependency configuration.

    :param template: the dependency returned by :method:``get_app_dependency``
    :param main_portal: the main folder of application template (relative to ``APPLICATION_MAIN``)
    :param version: the version of main template
    :return: application template for kubernetes
    """
    if template is None:
        template = {
            'instance_list': [],
            'instance_settings': [],
            'version': '',
        }
    tpl_path = os.path.join(RootConfig.TEMPLATES_FOLDER, main_portal, version, 'application-main.jsonnet')
    result = evaluate_jsonnet_file(tpl_path, **template)
    return result


def get_kube_configs(app_config, **kwargs):
    """
    Generate application template for kubernetes.

    :param app_config: user-defined ``AppConfig``
    :param kwargs: more parameters for :method:``get_kube_configs_from_template``
    :return: application template for kubernetes
    """
    template = get_app_template(app_config)
    result = get_kube_configs_from_template(template=template, **kwargs)
    return result


def get_components_dependencies():
    """
    Generate components_dependencies template for ockle.

    :return: components_dependencies object for ockle
    """
    tpl_path = os.path.join(RootConfig.TEMPLATES_FOLDER, 'components_dependencies.json')
    result = evaluate_jsonnet_file(tpl_path=tpl_path)
    return result


def calculate_app_tcu(app_config):
    """
    Calculate the TCU number of application
    :param app_config: user-defined ``AppConfig``
    :return: a dict in form like:
        {
            "hdfs": {
                "c": 3,
                "m": 6,
                "s": 6
            },
            "zookeeper": {
                "c": 3,
                "m": 6,
                "s": 6
            },
        }
    """
    template = get_app_template(app_config)
    return template.get('TCU', dict())
