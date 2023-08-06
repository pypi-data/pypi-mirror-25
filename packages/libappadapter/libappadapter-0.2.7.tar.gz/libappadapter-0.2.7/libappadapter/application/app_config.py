import logging
import re

import os

from libappadapter.exceptions import ApplicationNotFoundException, ApplicationConfigException
from libappadapter.settings import RootConfig

__all__ = ['AppConfig']

logger = logging.getLogger(__name__)

APPLICATION_TEMPLATES = {}  # {app_template: [version]}
regex_version = r'\d+(\.\d+)*'

# load defined application templates
for app_tpl in os.listdir(RootConfig.APPLICATION_MAIN):
    if app_tpl not in APPLICATION_TEMPLATES:
        APPLICATION_TEMPLATES[app_tpl] = []
    # scan application versions
    for _version in os.listdir(os.path.join(RootConfig.APPLICATION_MAIN, app_tpl)):
        m = re.match(regex_version, _version)
        if m is None:
            logger.warning("Invalid version '{0}' for application '{1}'.".format(_version, app_tpl))
        else:
            APPLICATION_TEMPLATES[app_tpl].append(_version)

logger.debug('APPLICATION_MAIN={}'.format(RootConfig.APPLICATION_MAIN))
logger.debug('Total {0} application templates loaded'.format(len(APPLICATION_TEMPLATES)))


class AppConfig(object):
    def __init__(self, name, template, version=None, app_config=None, user_config=None, development_mode=False):
        """
        General configuration of application.

        :param name: user-specified  application name
        :param template: the pre-defined application templates, say INCEPTOR, HDFS etc.
        :param version: the application version
        :param app_config: user-specified application configurations (formatted as `sepc.configs` of instance settings):
               * `instance_versions`: user-specified instance versions of the application.
        :param user_config: user-specified instance configurations (formatted as `metadata.annotations` of instance settings)
        """
        self.name = name
        if template not in APPLICATION_TEMPLATES:
            raise ApplicationNotFoundException(
                "Unsupported application '{0}' in current version.".format(template))
        self.template = template

        # Use latest version when the parameter is not specified.
        # TODO: add ordering based on version schemas
        ordered_versions = self._order_version_schemas(APPLICATION_TEMPLATES[self.template])
        _version = ordered_versions[-1] if version is None or version == '' else version
        if _version not in APPLICATION_TEMPLATES[self.template]:
            raise ApplicationNotFoundException("Version '{0}' of '{1}' unsupported.".format(_version, self.template))
        self.version = _version

        self.app_config = app_config if app_config else dict()
        if 'instance_versions' in self.app_config:
            instance_versions = self.app_config['instance_versions']
            if not isinstance(instance_versions, dict):
                raise ApplicationConfigException(
                    "Invalid instance_versions parameter type: should be dict, given {}".format(type(instance_versions)))
        else:
            self.app_config['instance_versions'] = {}

        self.user_config = user_config if user_config else dict()
        self.development_mode = development_mode

    def to_dict(self):
        return {
            'name': self.name,
            'template': self.template,
            'version': self.version,
            'app_config': self.app_config,
            'user_config': self.user_config,
            'development_mode': self.development_mode,
        }

    def _order_version_schemas(self, versions, reversed_order=False):
        """
        Order version schemas, say 5.0-rc1 < 5.0, 5.0 < 5.1
        :param versions: a list of version strings
        :param reversed_order: if a reversed order is kept
        :return: a list of ordered versions
        """
        if reversed_order:
            return list(reversed(versions))
        else:
            return versions