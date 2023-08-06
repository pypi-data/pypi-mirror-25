# libappadapter

该库使用Python语言编写，主要负责接受一系列参数传递给预设的模版，通过jsonnet生成kubernetes能够认识的配置。这个库目前将会被ockle以及otherk8s所使用。

## Install

```bash
pip install -U setuptools
python setup.py install
```

or via pip

```bash
pip install -U libappadapter \
    -i http://172.16.130.43:8081/repository/pypi/simple/ \
    --trusted-host=172.16.130.43
```

## Run tests

如果测试templates，需要编译并安装jsonnet命令行工具：

```bash
git clone https://github.com/google/jsonnet
cd jsonnet && make
export JSONNET_BIN=/path/to/jsonnet
```

运行测试：

```bash
./testing.sh
```

## Usage

该库的功能是，指定一个或多个APP，生成可以被KUBE接受并建立应用的json配置。

### AppConfig参数

对于传入的APP，内部通过`AppConfig`进行描述，例如新建INCEPTOR应用，可以描述为：
```python
from libappadapter import AppConfig, AppType

app1 = AppConfig(name='app1', template=AppType.INCEPTOR, version='0.2')
```
其中`template`参数可以为**大写**的应用名称，即"INCEPTOR"。如果省略版本号，则使用最新版本的应用模板。

### 获取单个APP的Kube配置

在实现逻辑上，给定`AppConfig`，首先通过定义的jsonnet模板得到APP的模板，经校验、转换后，生成Kube配置。

基于以上逻辑，可通过下述步骤获得INCEPTOR的kube配置：
```python
from libappadapter import get_app_template, get_kube_configs_from_template
from libappadapter import get_kube_configs

template = get_app_template(app1)
kube_config = get_kube_configs_from_template(template)

# or in a combined way
kube_config2 = get_kube_configs(app1)

# kube_config == kube_config2
```

### 获取有依赖关系的多个APP的Kube配置

通常多个APP之间是有依赖关系的，如INCEPTOR依赖HDFS。libappadapter提供了两种方式进行依赖关系管理：一是自动化检测APP的组件依赖，二是手动指定组件的依赖关系。后者更利于定制化的依赖关系。

* 自动检测

自动检测方式下，只需要传入多个``AppConfig``实例，其依赖关系由算法进行保证，需设定`auto_relation=True`，例如：
```python
from libappadapter import AppConfig, AppType
from libappadapter import get_constraint_app_templates, get_kube_configs_from_template

db1 = AppConfig('appdb1', AppType.INCEPTOR)
hdfs1 = AppConfig('apphdfs1', AppType.HDFS)

templates = get_constraint_app_templates(apps=[db1, hdfs1], auto_relation=True)

for app_name in templates:
    kube_config = get_kube_configs_from_template(templates[app_name])
```

如果传入的一组应用存在无法满足的依赖关系，则抛出``InvalidDependenceException``。

返回的``templates``是`dict`结构，key为APP名称，value为处理好依赖关系的template。这时各template可以通过`get_kube_configs_from_template`生成独立的kube_config。也可以合并后生成单一的kube_config。后者需要用户根据需要（如APP配置有差异），自行进行template的合并。

* 手动配置

手动配置提供了更加灵活的依赖关系管理，目前支持`depends_on`和`share`关系，前者描述两个APP之间的依赖，后者描述多个APP对子组件的共享关系。

例如建立两个INCEPTOR和HDFS组合，其中INCEPTOR共享metastore子组件，HDFS共享zookeeper子组件：

```python
from libappadapter import AppConfig
from libappadapter import get_constraint_app_templates
from libappadapter.relations import relation

db1 = AppConfig('appdb1', 'INCEPTOR')
db2 = AppConfig('appdb2', 'INCEPTOR')
hdfs1 = AppConfig('apphdfs1', 'HDFS')
hdfs2 = AppConfig('apphdfs2', 'HDFS')

templates = get_constraint_app_templates(
    apps=[db1, db2, hdfs1, hdfs2],
    relations=[
        relation.depends_on(db1, hdfs1),
        relation.depends_on(db2, hdfs2),
        relation.share([hdfs1, hdfs2], 'zookeeper'),
        relation.share([db1, db2], 'metastore')
    ],
)
```

## Development

```text
.
├── libappadapter                       # 模块
│   ├── application                     # 通过jsonnet生成APP模板
│   ├── relations                       # APP/组件依赖关系管理
│   └── templates                       # APP模板
│       ├── applib                      # 模板lib
│       ├── applications                # 模板仓库
│       ├── instance_advanced_configs   # 默认高级参数模板
│       ├── bin
│       └── main                        # 模板生成入口
└── tests
    ├── application
    └── relations
```
