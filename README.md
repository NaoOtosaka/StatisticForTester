# KM&GameAcademy 数据统计服务

## 1.目录结构

- app: API存放目录
  - v1: API版本
  - manager.py: API版本控制器
- backup: 备份文件夹，当前备份迁移mysql前sqlite文件
- common: 通用基类
- database: 静态数据库文件，迁移mysql已废弃
- doc: 项目文档
- files: 项目接收文件
- libs: API依赖通用方法
- log: 日志存放路径
- sql: 项目初始化SQL备份
- tools: 公用常用方法
- ttf: 字体文件
- app.py: 服务启动主入口
- config: 项目配置文件

## 2.Install

依赖环境：

- python 3.6+
- DBUtils 2.0
- pandas 1.2.0
- PyMySQL 1.0.2
- gevent 20.9.0
- Flask 1.1.2
- Flask_Cors 3.0.9
- wordcloud 1.8.1

## 3.项目说明

### 3.1.设计思想

- 参考RESTful API接口设计标准及规范，主要基于Python Flask搭建API服务，二次封装子蓝图以实现API版本管理
- 基于数据库线程池，使用PDBC对Mysql进行操作

### 3.2.配置说明

#### 3.2.1.Config基类

```python
# 项目基础路径
workPath = sys.path[1]

# 数据库选择(mysql/sqlite)（已废弃）
DB_TYPE = 'mysql'

# =============SQLITE===============
# SQLITE数据库路径配置
DB_PATH = workPath + '/database/data.db'

# 是否启动外键约束
USE_FOREIGN = True

# 数据库缓存分页大小
CACHE_SIZE = 8000

# =============MYSQL===============
# MYSQL主机名配置
BD_HOST = ''
# MYSQL主机端口配置
DB_PORT = 3306
# MYSQL用户名
DB_USER = ''
# MYSQL密码
DB_PASSWORD = ''
# MYSQL数据库名
DB_NAME = ''

# API版本选择
API_VERSION = 'v1'
```

```python
class BaseData(object):
    """
    基础数据类
    作为看板导出CSV文件解析脚本依赖类
    作为Config基类的嵌套类声明
    """
    # 测试阶段名称与id对应关系
    # 如需新增阶段类型时，需在此配置中同步追加
    plan = {
        "冒烟测试": 1,
        "冒烟复核": 2
        ...
    }
    
    # BUG类型名称与id对应关系
    # 如需新增类型时，需在此配置中同步追加
    bug_type = {
        "前端BUG": 1,
        "服务端BUG": 2
        ...
    }
    
    # BUG分类名称与id对应关系
    # 如需新增分类时，需在此配置中同步追加
    bug_category = {
        "未选定": 1
        ...
    }
    
    # 测试平台
    # 如需新增平台时，需在此配置中同步追加
    develop_project = [
        '游戏学院-开发',
        'KM-平台开发'
    ]
    
    # 线上缺陷对应平台
    # 如需新增平台时，需在此配置中同步追加
    prod_project = [
        '游戏学院-缺陷',
        'KM-缺陷跟踪'
    ]

```

#### 3.2.2.DevelopmentConfig类

```python
"""
测试环境配置类
继承配置基类
"""
# API调试模式
DEBUG = True

# 日志路径配置
LOG_PATH = Config.workPath + '\\log\\'

# 日志输出等级
LOG_LEVEL = 'DEBUG'

DB_TYPE = 'mysql'

# =============MYSQL===============
BD_HOST = ''
# MYSQL主机端口配置
DB_PORT = 3306
# MYSQL用户名
DB_USER = ''
# MYSQL密码
DB_PASSWORD = ''
# MYSQL数据库名
DB_NAME = 'DataStatistic'

# 主机配置
API_HOST = '0.0.0.0'
API_PORT = 9222

# 文件解析编码配置
ENCODING = 'gbk'

# 文件路径配置
FILES_PATH = Config.workPath + '\\files\\'

# 词云字体文件路径配置
TTF_PATH = Config.workPath + '\\ttf\\'
```

#### 3.2.3.ProjectionConfig类

```python
"""
生产环境配置类
继承配置基类
"""
# API调试模式
DEBUG = False

# 工作区配置
workPath = '/Users/pijingwen/PycharmProjects/qa-dbstatistics'

# 日志输出等级
LOG_LEVEL = 'WARNING'

# 日志路径配置
LOG_PATH = workPath + '/log/'

# 数据库路径配置
DB_HOST = workPath + '/database/data.db'

# =============MYSQL===============
# MYSQL主机名配置
BD_HOST = ''
# MYSQL用户名
DB_USER = ''
# MYSQL密码
DB_PASSWORD = ''
# MYSQL数据库名
DB_NAME = ''

# 主机配置
API_HOST = '0.0.0.0'
API_PORT = 9222

# 文件解析编码配置
ENCODING = 'gbk'

# 文件路径配置
FILES_PATH = workPath + '/files/'

# 词云字体文件路径配置
TTF_PATH = workPath + '/ttf/'
```

### 3.3.基类说明

#### 3.3.1.DBPool - 数据库线程池类

```python
class DBPool:
    """
    数据库线程池类
    """
    def __init__(self):
        # 实例化日志对象
        self.logger = setLogger('databases')
        # 线程池初始化
        self.pool = PooledDB(
            # 指定数据库类
            creator=pymysql,
            maxconnections=None,
            # 池最小链接数
            mincached=3,
            # 池最大链接数
            maxcached=10,
            maxshared=0,
            blocking=True,
            maxusage=None,
            setsession=None,
            ping=0,
            host=CONF.BD_HOST,
            port=CONF.DB_PORT,
            user=CONF.DB_USER,
            password=CONF.DB_PASSWORD,
            database=CONF.DB_NAME,
            charset='utf8mb4'
        )
```

```
主要用于优化数据库查询速度，保证接口稳定性
```

#### 3.3.2.NestableBlueprint - 嵌套蓝图类

```python
class NestableBlueprint(Blueprint):
    """
    嵌套蓝图
    """
    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']
            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)
```

```
蓝图基类二次封装，用于实现接口版本管理
```

#### 3.3.3.StatisticMysql - Mysql操作类

```python
class StatisticMysql:
    """
    Mysql操作
    """
    def __init__(self):
        # 实例化日志对象
        self.logger = setLogger('databases')
        # 线程池初始化
        self.pool = PooledDB(
            ...
        )

    def connect(self):
        try:
            # 线程池中链接线程
            conn = self.pool.connection()
            cursor = conn.cursor()
            return conn, cursor
        except pymysql.DatabaseError:
            self.logger.error(pymysql.DatabaseError)
            return 0

    def query(self, sql):
        """
        查询操作类
        :return:
        """
        # 获取链接对象，游标
        conn, cursor = self.connect()

        # sql解析
        sql = sql.strip()

        # 查询处理
        if sql.lstrip().upper().startswith("SELECT"):
            result = self.select(cursor, sql)
        elif sql.lstrip().upper().startswith("INSERT"):
            result = self.insert(conn, cursor, sql)
        elif sql.lstrip().upper().startswith("UPDATE"):
            result = self.update(conn, cursor, sql)
        elif sql.lstrip().upper().startswith("DELETE"):
            result = self.delete(conn, cursor, sql)
        else:
            result = 0

        # 释放游标
        cursor.close()
        # 释放链接
        conn.close()

        return result

    @staticmethod
    def select(cursor, sql):
        """
        SELECT语句
        """
        ...

    @staticmethod
    def insert(conn, cursor, sql):
        """
        INSERT语句
        """
        ...

    @staticmethod
    def update(conn, cursor, sql):
        """
        UPDATE语句
        """
		...

    @staticmethod
    def delete(conn, cursor, sql):
        """
        DELETE语句
        """
        ...
```

### 3.4.API版本管理

**app.manager.py**

```python
# 作为对一级蓝图的拓展，用于将API方法封装为一个版本，便于后续API迭代or重构时版本管理
def resign_blueprint(flask_server):
    """
    注册子功能蓝图
    :param flask_server:
    :return:
    """
    flask_server.register_blueprint(Project.project_api)
    flask_server.register_blueprint(Tester.tester_api)
    flask_server.register_blueprint(Developer.developer_api)
    flask_server.register_blueprint(Bug.bug_api)
    flask_server.register_blueprint(Files.files_api)
    flask_server.register_blueprint(Planner.planner_api)
    flask_server.register_blueprint(Tools.tools_api)


# 实例化API二级蓝图
api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api/v1')

resign_blueprint(api_v1)
```

**app.py**

```python
# 主入口启动方法中将二级蓝图在一级蓝图中注册
# 如需添加版本，追加注册即可

# 引入v1版本管理器
from app.manager import api_v1

def setup(flask_server, debug):
    """
    设置启动
    :param debug:
    :param flask_server:
    :return:
    """
    ...

    # 注册API蓝图(二级蓝图)
    flask_server.register_blueprint(api_v1)

    ...
```

### 3.5.日志

**tools.log.py**

```python
def setLogger(log_name):
    """
    实例化日志对象
    :param log_name:
    :return:
    """
    # 初始化log实例
    logger = logging.getLogger(log_name)

    # 设定输出等级
    logger.setLevel(config.CONF.LOG_LEVEL)

    # 设置输出日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s %(filename)s %(message)s",
        datefmt="%Y/%m/%d %X"
    )

    # 设定输出文件名
    timestamp = get_today_timestamp()
    log_file_name = str(timestamp) + '.log'

    # 创建handler
    fh = logging.FileHandler(config.CONF.LOG_PATH + log_file_name, encoding="utf-8")
    ch = logging.StreamHandler()

    # 为handler指定输出格式
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 添加handler处理器
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
```

```
日志未封装基类，而是以函数方式接收日志名从而实例化并返回日志对象。后续迭代优化时建议将该模块重构为基类使用
```

### 3.6.拓展（模块拓展示例 - 以词云模块为例）

#### 3.6.1.封装拓展模块方法

```
拓展模块存放于tools文件夹下，以拓展功能名命名
```

**wordCloud.py**

```python
from wordcloud import WordCloud
import base64
import io

from config import CONF
from libs.bug import get_model_data_with_project


def count_model(str_list):
    str_set = set(str_list)

    count_data = {}

    for item in str_set:
        count_data[item] = str_list.count(item)
    temp = sorted(count_data.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(temp)


def get_wordcloud_with_project(project_id=None):
    """
    获取词云
    :return:
    """
    # 字体文件路径
    font = CONF.TTF_PATH + 'msyh.ttc'

    # 源数据处理(模块名称)
    str_list = get_model_data_with_project(project_id)

    # 分词
    text = ""
    for item in str_list:
        text += item + " "

    # 生成词云
    pil_img = WordCloud(
        font_path=font,
        width=800,
        height=300,
        background_color="white",
        prefer_horizontal=0.6,
        collocations=False).generate(text=text).to_image()

    # base64输出
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64
```

#### 3.6.2.拓展模块接口实现

```
拓展模块对应接口实现于app目录下Tools.py文件中
接口及方法命名于模块名一致
```

**app.v1.Tools.py**

```python
from flask import Blueprint
from flask import request
import json

from tools.log import setLogger
from tools.wordCloud import get_wordcloud_with_project

# 实例化日志对象
logger = setLogger('tools_api')

# 实例化蓝图
tools_api = Blueprint('tools', __name__, url_prefix='/tools')


@tools_api.route('/wordcloud', methods=['GET'])
def wordcloud():
    project_id = int(request.values.get('projectId'))

    return get_wordcloud_with_project(project_id)
```

#### 3.6.3.额外配置项

##### 3.6.3.1.拓展模块蓝图实例化

**app.v1.Tools.py**

```python
# 实例化蓝图
tools_api = Blueprint('tools', __name__, url_prefix='/tools')
```



##### 3.6.3.2.拓展模块蓝图注册至二级蓝图

**app.manager.py**

```python
def resign_blueprint(flask_server):
    """
    注册子功能蓝图
    :param flask_server:
    :return:
    """
    ...
    flask_server.register_blueprint(Tools.tools_api)
    ...
```

