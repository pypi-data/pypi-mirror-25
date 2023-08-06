from libappadapter.k8s.utils import Enum

ApplicationRunningStatus = Enum([
    'DEPLOYING',
    'PENDING',
    'CREATING',
    'TERMINATING',
    'WAITING',
    'UNREADY',
    'RUNNINGERROR',
    'RUNNING',
    'TERMINATED',
])

InstanceRunningStatus = Enum([
    'DEPLOYING',
    'PENDING',
    'CREATING',
    'TERMINATING',
    'WAITING',
    'UNREADY',
    'RUNNINGERROR',
    'RUNNING',
    'TERMINATED',
])

PodRunningStatus = Enum([
    'PENDING',
    'CREATING',
    'TERMINATING',
    'WAITING',
    'UNREADY',
    'RUNNINGERROR',
    'RUNNING',
    'TERMINATED',
])

ContainerRunningStatus = Enum([
    'PENDING',
    'CREATING',
    'TERMINATING',
    'WAITING',
    'UNREADY',
    'RUNNING',
    'TERMINATED',
])