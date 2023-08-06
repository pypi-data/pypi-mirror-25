import _jsonnet
import json

from .exceptions import JsonnetEvalException


def evaluate_jsonnet_file(tpl_path, **config):
    """
    Evaluate configuration from jsonnet template and given params
    :param file_path: absolute or relative (to TEMPLATE_DIR) jsonnet file path
    :param config: params for jsonnet template
    :return: evaluated configuration object
    """
    try:
        json_str = _jsonnet.evaluate_file(tpl_path, tla_codes={"config": json.dumps(config)})
    except RuntimeError as e:
        raise JsonnetEvalException("jsonnet exception: {0}".format(e))
    return json.loads(json_str)
