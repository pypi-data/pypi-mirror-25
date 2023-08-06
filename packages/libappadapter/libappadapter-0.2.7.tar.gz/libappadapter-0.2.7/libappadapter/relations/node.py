import logging

from ..application import get_app_template

logger = logging.getLogger(__name__)


class ApplicationNode(object):
    def __init__(self, app_config):
        self.name = app_config.name
        self.config = app_config
        self.parents = []
        self.children = []  # [ApplicationNode]
        self.successors = {}  # all successor nodes
        self.template = get_app_template(app_config)

    def __str__(self):
        return 'Application {}: #parent {}, #children {}, #successors {}, #instances {}'.format(
            self.name, len(self.parents), len(self.children), len(self.successors),
            len(self.get_instance_list())
        )

    def __update_successors(self, succ):
        """
        Update node's successors as a fast index of all children and grandchildren
        :param succ: an instance of ApplicationNode
        :return: None
        """
        self.successors[succ.name] = succ
        for parent in self.parents:
            parent.__update_successors(succ)

    def __update_dependent_node(self, child, scope=None):
        """
        Update instance's ``dependencies`` of self with child's ``instance_list``

        When a ``DependenceRelation`` is declared between two apps, it implies that
        the latter's instance are shared by the former application. In this routine,
        we update the former configuration with dependencies's info.

        :param child: the dependent application node
        :param scope: a list of MODULE names that are left out for updating
        :return: None
        """
        assert isinstance(child, ApplicationNode)

        # Extract existing instances from child
        child_modules = {}  # {moduleName: instanceId}
        for instance in child.template.get('instance_list', []):
            instance_id = instance.get('name', None)
            instance_module = instance.get('moduleName', None)
            if None in [instance_id, instance_module]:
                raise RuntimeError('Invalid application dependency of instance: {0}'.format(instance))

            # filter modules that are constrained by scope list
            if scope is not None and instance_module not in scope:
                continue
            child_modules[instance_module] = instance_id

        # Update self's instance dependencies:
        #   1. Replace instance dependencies with child instances
        #   2. Remove instances replaced by those in child
        # TODO: remove instances replaced by those in child
        instances_list = self.template.get('instance_list', [])
        for instance in instances_list:
            instance_id = instance.get('name', None)
            dependencies = instance.get('dependencies', [])
            for dep in dependencies:
                module_name = dep.get('moduleName')
                name = dep.get('name')
                if module_name in child_modules:
                    new_name = child_modules[module_name]
                    dep.update({'name': new_name})
                    logger.info('Update [{0}] dependencies: {1} -> {2}'.format(
                        instance_id, name, new_name))

    def add_child(self, child):
        """Add a new child to self node"""
        self.children.append(child)
        child.parents.append(self)
        self.__update_successors(child)
        self.__update_dependent_node(child)

    def is_leaf(self):
        """If self is a leaf node"""
        return len(self.children) == 0

    def is_root(self):
        """If self is the root of a partial tree"""
        return len(self.parents) == 0

    def is_ancestor(self, successor):
        """Determine if self is an ancestor of given node"""
        return successor.name in self.successors

    def is_successor(self, ancestor):
        return self.name in ancestor.successors

    def breadth_first_traversal(self):
        """
        Walk through the subtree from current node with width-first algorithm
        :return:
        """
        queue = [self]
        for child in self.children:
            queue.extend(child.breadth_first_traversal())
        return queue

    def get_instance_list(self, with_dependencies=False):
        """Get a list of instance belonging to this application.
        """
        instance_list = {}  # {(instance_name, instance_module): [(dep_name, dep_module)]}
        for instance in self.template.get('instance_list', []):
            # instance_id = instance.get('instanceId', None)
            instance_module = instance.get('moduleName', None)
            instance_name = instance.get('name', None)
            key = (instance_name, instance_module)
            instance_list[key] = []

            dependencies = instance.get('dependencies', [])
            for dep in dependencies:
                dep_name = dep.get('name', None)
                dep_module = dep.get('moduleName', None)
                value = (dep_name, dep_module)
                instance_list[key].append(value)

        if with_dependencies:
            return instance_list
        else:
            return instance_list.keys()

    def replace_instance(self, instance_module, instance_name, removed_instance_names=None):
        """
        Update self's instance_list with given module:
          1. Remove the existing module with the same module name
          2. Update instance dependencies according to new module info
        :param instance_module: new module name
        :param instance_name: new instance name of shared module
        :param removed_instance_names: the old instances for the same module
        """
        instance_list = self.template.get('instance_list', [])

        # Recording removed existing instances
        removed_instance_names = removed_instance_names if removed_instance_names else list()
        removed_instances = set(removed_instance_names)
        for i in instance_list:
            old_module = i.get('moduleName', None)
            old_name = i.get('name', None)
            if old_module == instance_module and old_name != instance_name:
                removed_instances.add(old_name)

        # Create new instance list
        new_instance_list = []
        for instance in instance_list:
            if instance.get('name', None) in removed_instances:
                continue

            # Update instance dependencies
            dependencies = instance.get('dependencies', [])
            for dep in dependencies:
                dep_module = dep.get('moduleName', None)
                dep_name = dep.get('name', None)
                if dep_module == instance_module:
                    dep.update({'name': instance_name})
                    removed_instances.add(dep_name)

            new_instance_list.append(instance)

        self.template.update({'instance_list': new_instance_list})

        return list(removed_instances)
