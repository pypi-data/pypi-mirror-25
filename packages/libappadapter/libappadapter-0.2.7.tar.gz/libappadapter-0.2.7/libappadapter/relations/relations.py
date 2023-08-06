# encoding: utf-8
# Copyright 2017 Transwarp Inc. All rights reserved.
import logging

logger = logging.getLogger(__name__)


# ----------------------------
#  Relation interfaces
# ----------------------------

class ApplicationRelation(object):
    """
    Convenient utilities to define app relations
    """

    def __init__(self):
        pass

    def depends_on(self, app1, app2):
        return DependenceRelation(app1, app2)

    def share(self, apps, shared_module):
        return ShareRelation(apps, shared_module)


# ----------------------------
#  Predefined app relations
# ----------------------------

class BaseRelation(object):
    def __init__(self, annotation):
        self.annotation = annotation

    def get_apps(self):
        return []


class DependenceRelation(BaseRelation):
    def __init__(self, app1, app2):
        super(DependenceRelation, self).__init__(self.__class__)
        self.app1 = app1
        self.app2 = app2

    def get_apps(self):
        parent = super(DependenceRelation, self).get_apps()
        parent.extend([self.app1, self.app2])
        return parent

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.app1.name == other.app1.name and self.app2.name == other.app2.name:
            return True
        return False

    def __str__(self):
        return 'DEP: {} -> {}'.format(self.app1.name, self.app2.name)


class ShareRelation(BaseRelation):
    def __init__(self, apps, shared_module):
        super(ShareRelation, self).__init__(self.__class__)
        self.apps = apps
        self.shared_module = shared_module

    def get_apps(self):
        parent = super(ShareRelation, self).get_apps()
        parent.extend(self.apps)
        return parent

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        self_apps = set([i.name for i in self.apps])
        other_apps = set([i.name for i in other.apps])
        if self_apps == other_apps and self.shared_module == other.shared_module:
            return True
        return False

    def __str__(self):
        return 'SHARE: {}: {}'.format(','.join([i.name for i in self.apps]), self.shared_module.name)
