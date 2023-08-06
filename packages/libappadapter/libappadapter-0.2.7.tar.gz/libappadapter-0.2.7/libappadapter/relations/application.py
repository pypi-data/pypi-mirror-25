import logging

from .relations import BaseRelation
from .tree import ApplicationTree

logger = logging.getLogger(__name__)


def get_constraint_app_templates(apps, relations=None, auto_relation=False, singleton=False):
    """
    Create application templates with constraints of pre-defined relations.

    :param apps: a list of application configurations
    :param relations: a list of implementations of :class:`BaseRelation`
    :param auto_relation: if detect application dependencies automatically
    :param singleton: if merge instances with the same type
    :return: a dict of application dependencies
    """
    all_apps = apps

    if relations is None or len(relations) == 0:
        relations = []

    for relation in relations:
        assert isinstance(relation, BaseRelation)
        all_apps.extend(relation.get_apps())

    tree = ApplicationTree(all_apps, relations, auto_relation, singleton)

    result = {}
    for app in tree.get_apps():
        result[app.name] = app.template

    return result
