# Copyright 2017 Transwarp Inc. All rights reserved.
import json
import logging

import os

from ..exceptions import NamespaceConfigException
from ..helpers import evaluate_jsonnet_file
from ..settings import RootConfig

__all__ = ['get_kube_namespace_config']

logger = logging.getLogger(__name__)


def _format_jsonnet_namespace_params(tenant_name, params):
    jsonnet_configs = {}

    if params is not None:
        user_config = {
            'admin': params.get("admin", ""),
            'admin_group': params.get("admin_group", ""),
            'normal_group': params.get("normal_group", ""),
        }
        application_params = params.get('application_params', [])
        annotations = {
            'status': 'Creating',
            'user_config': json.dumps(user_config),
            'application_params': json.dumps(application_params),
        }
        jsonnet_configs.update(annotations=annotations)

    jsonnet_configs.update(name=tenant_name)
    return jsonnet_configs


def get_kube_namespace_config(namespace, **kwargs):
    jsonnet_file = os.path.join(RootConfig.NAMESPACE_FOLDER, '1.0/template-json/namespace-main.jsonnet')
    try:
        user_dict = _format_jsonnet_namespace_params(namespace, kwargs)
        return evaluate_jsonnet_file(jsonnet_file, **user_dict)
    except Exception, e:
        raise NamespaceConfigException(e)
