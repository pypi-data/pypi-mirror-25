import logging

from .node import ApplicationNode
from .relations import ApplicationRelation
from .relations import DependenceRelation, ShareRelation
from ..exceptions import ApplicationRelationMismatchException, ApplicationRelationException
from ..exceptions import InvalidApplicationTreeRoot
from ..exceptions import InvalidDependenceException

logger = logging.getLogger(__name__)


class ApplicationTree(object):
    def __init__(self, app_configs, relations=None, auto_detection=False, singleton=False):
        self.relations = list()
        self.auto_detection = auto_detection
        relations = relations if relations else list()

        # Table to map application name to `ApplicationNode`
        self.app_node_mapping = {}  # {app_name: ApplicationNode}
        for app in app_configs:
            self.app_node_mapping[app.name] = ApplicationNode(app)

        # use specified relations
        for relation in relations:
            self.add_relation(relation)

        # Detect dependencies when user does not specify
        if self.auto_detection:
            logger.info("Enable auto detection of application dependencies: {}".format(','.join([i.template for i in app_configs])))
            self._generate_auto_relations()

        # Create trees with dependent relations
        # TODO: validate loop dependencies
        self.update_depends_relation(self.relations)

        # Update share relations
        self.update_share_relation(self.relations)

        # TODO: validate instance singletons

    def _generate_auto_relations(self):
        """
        Generate application relations automatically.
        """
        # Collect all instances to create
        all_instances_to_create = {}  # {instance_type: [(instance_name, app_name)]}
        all_instance_names = list()
        for node in self.app_node_mapping.values():
            for instance_name, instance_type in node.get_instance_list():
                all_instance_names.append(instance_name)
                if instance_type not in all_instances_to_create:
                    all_instances_to_create[instance_type] = []
                all_instances_to_create[instance_type].append((instance_name, node.name))

        def _find_real_dependency(instance_type, app_type):
            """ Search for the existing dependent instance of specific type.
            """
            deps = all_instances_to_create.get(instance_type, [])
            if len(deps) == 0:
                raise RuntimeError('No instance detected for dependency "{}" of application "{}"'
                                   .format(instance_type, app_type))
            # TODO (cxm): use the item at lowest level to avoid loop dependency
            for dep in deps:
                ins_name, app_name = dep
                if node.name != app_name:
                    return dep
                return None

        # Detect and collect auto-detected relations
        relation = ApplicationRelation()
        for node in self.app_node_mapping.values():
            for deps in node.get_instance_list(with_dependencies=True).values():
                for dep_name, dep_type in deps:
                    if dep_name in all_instance_names:
                        # omit dependencies as already in instance_list
                        continue
                    real_dep = _find_real_dependency(dep_type, node.config.template)
                    if real_dep is not None:
                        real_dep_name, real_app_name = real_dep
                        self.add_relation(
                            relation.depends_on(
                                app1=self.app_node_mapping[node.name],
                                app2=self.app_node_mapping[real_app_name]
                            )
                        )

    def add_relation(self, relation):
        """Add new relation by eliminating replications
        """
        if relation not in self.relations:
            # call Relation.__eq__
            self.relations.append(relation)

    def get_trees(self):
        """Return all nodes without parents (tree roots)
        """
        roots = []
        for app in self.app_node_mapping:
            node = self.app_node_mapping[app]
            if node.is_root():
                roots.append(node)
        return roots

    def get_tree(self, root_name):
        root = self.app_node_mapping[root_name]
        if not root.is_root():
            raise InvalidApplicationTreeRoot('Root "{}" not found'.format(root_name))
        return root

    def get_apps(self):
        """ Get a list of ``ApplicationNode``
        """
        return self.app_node_mapping.values()

    def get_app(self, app_name):
        """ Get specific ApplicationNode
        """
        return self.app_node_mapping[app_name]

    def update_depends_relation(self, relations=None):
        """
        Update application trees with dependence relations
        :param relations: list of DependenceRelation
        """
        relations = relations if relations else list()
        for dep_relation in relations:
            if not isinstance(dep_relation, DependenceRelation):
                continue
            try:
                node1 = self.app_node_mapping[dep_relation.app1.name]
                node2 = self.app_node_mapping[dep_relation.app2.name]
            except KeyError:
                raise ApplicationRelationMismatchException(
                    'Mismatch between application list and relation definition'
                )
            try:
                self.app_node_mapping[node1.name].add_child(node2)
            except Exception as e:
                raise ApplicationRelationException(str(e))

    def _get_shared_module(self, share_relation):
        """Validate share relation and obtain shared module.
        NOTE: We use the first app in application list as the shared reference
        :param share_relation: ShareRelation
        :return: (shared_app_name, shared_module)
        """
        relation_apps = share_relation.apps
        shared_module = share_relation.shared_module

        # Validate share relation and obtain shared module
        referred_app_name = None  # string
        shared_module_reference = None  # (instance_name, instance_module)
        for app in relation_apps:
            try:
                node = self.app_node_mapping[app.name]
            except KeyError:
                raise ApplicationRelationMismatchException(
                    'Mismatch between application list and relation definition'
                )

            # Check if the application contains the shared module
            instances = node.get_instance_list(with_dependencies=False)
            modules = [i[1] for i in instances]
            if shared_module not in modules:
                raise ApplicationRelationMismatchException(
                    'Can not find module "{0}" for application "{1}"'.format(shared_module, node.name)
                )

            # NOTE: We use the first app in application list as the shared reference
            if shared_module_reference is None:
                for instance in instances:
                    instance_name, instance_module = instance
                    if instance_module == shared_module:
                        shared_module_reference = instance
                        referred_app_name = node.name

        return referred_app_name, shared_module_reference

    def update_share_relation(self, relations=None):
        """
        Update application trees with share relations. This method should always
        called after :method:``update_depends_relation``
        :param relations: list of ShareRelation
        """
        relations = relations if relations else list()
        for share_relation in relations:
            if not isinstance(share_relation, ShareRelation):
                continue

            referred_app_name, shared_module_reference = self._get_shared_module(share_relation)
            logger.debug('app_name: {0}, shared_module: {1}'.format(referred_app_name, shared_module_reference))

            if shared_module_reference is None:
                raise ApplicationRelationMismatchException(
                    'Invalid shared module {0}'.format(share_relation.shared_module)
                )

            shared_name, shared_module = shared_module_reference

            # Update trees according to the shared module
            removed_instances = []
            for root in self.get_trees():

                # Update trees which relates to the shared module
                found = False
                for app in share_relation.apps:
                    node = self.app_node_mapping[app.name]
                    if root.name == node.name or root.is_ancestor(node):
                        found = True
                        break

                if found:
                    queue = reversed(root.breadth_first_traversal())
                    for node in queue:
                        # Remember all removed instances in case the instance have 1+ steps of dependence
                        removed = node.replace_instance(shared_module, shared_name, removed_instances)
                        removed_instances.extend(removed)

    def _validate_dependencies(self, root=None):
        """
        Validate the completeness of instance dependencies.
        :return: None, otherwise raise ``InvalidDependenceException``
        """
        if root is not None:
            tree = self.get_tree(root.name)
            nodes = tree.breadth_first_traversal()
        else:
            nodes = self.app_node_mapping.values()

        # Collect all instances that will be created
        all_instances = []
        for node in nodes:
            all_instances.extend([iname for iname, itype in node.get_instance_list()])

        # TODO: optimize code efficiency

        # Validate dependencies against created instances
        for node in nodes:
            for deps in node.get_instance_list(with_dependencies=True).values():
                for dep_name, dep_module in deps:
                    if dep_name not in all_instances:
                        raise InvalidDependenceException('Dependency "{0}" of application "{1}" is invalid'
                                                         .format(dep_name, node.name))

    def _validate_circle(self, root=None):
        """Validate if there are any circles in the trees"""
        pass

    def validate(self, root=None):
        self._validate_dependencies(root=root)
        self._validate_circle(root=root)
