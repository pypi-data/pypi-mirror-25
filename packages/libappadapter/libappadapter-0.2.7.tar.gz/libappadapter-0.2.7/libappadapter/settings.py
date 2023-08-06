# Copyright 2017 Transwarp Inc. All rights reserved.
import os
import logging

__all__ = ['RootConfig', 'is_debugging', 'logger']


is_debugging = os.getenv("LIBAPP_DEBUG", 'true')
if is_debugging == 'true':
    is_debugging = True
else:
    is_debugging = False

logging.basicConfig()
logger = logging.getLogger('libappadapter')
if is_debugging:
    logger.setLevel('DEBUG')
else:
    logger.setLevel('INFO')


class RootConfig(object):

    LIBRARY_ROOT = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.join(LIBRARY_ROOT, '..'))

    TEMPLATES_FOLDER = os.getenv("LIBAPP_TEMPLATES_FOLDER", os.path.join(LIBRARY_ROOT, 'templates'))
    NAMESPACE_FOLDER = os.getenv("LIBAPP_NAMESPACE_FOLDER", os.path.join(LIBRARY_ROOT, 'templates/namespace'))
    APPLICATION_MAIN = os.path.join(TEMPLATES_FOLDER, 'applications')


if __name__ == '__main__':
    logger.info(RootConfig.TEMPLATES_FOLDER)