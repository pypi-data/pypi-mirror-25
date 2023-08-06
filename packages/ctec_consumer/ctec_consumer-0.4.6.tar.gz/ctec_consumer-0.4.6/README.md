# 电渠rabbitMQ Consumer

## 环境

`Python2` 或 `Python3`

- `gevent`
- `pika`
- `kazoo`
- `psutil`

## 使用指南

### 处理方法开发指南

- 方法有且只有一个入参，WorkerMessage对象
- 方法需要明确返回处理响应码，目前支持：
  - CONSUME_SUCCESS，处理成功
  - CONSUME_REDELIVER，处理失败，重新投递
  - CONSUME_REJECT，处理失败，丢弃消息

### 线程版使用指南

```python
import ctec_consumer.consumer_log as ctec_logging
from ctec_consumer.dummy import consumer

# 创建logger对象方法1：
# 参数1：应用名称
# 参数2：日志路径
# 参数3：是否开启DEBUG，默认关闭。
ctec_logging.APP_NAME = 'app_name'
ctec_logging.LOG_PATH = '/opt/logs'
ctec_logging.DEBUG = True

# 定义处理方法，该方法接收一个参数Message对象
# 方法必须要返回固定值，具体取值范围参照上一节文档
# worker_message对象结构参见下文
def worker(worker_message):
    print(worker_message.body)
    # 处理逻辑....
    return ctec_consumer.CONSUME_SUCCESS

try:
    # 创建logger对象方法2：用于写日志。如果不指定，则默认写到STDOUT
    # 参数1：应用名称
    # 参数2：日志路径
    # 参数3：是否开启DEBUG，默认关闭。
    logger = ctec_logging.get_logger('app_name', '/opt/logs', debug=True)

    # 设置采集线程的Zookeeper地址，若关闭采集线程，此处可不进行设置
    data_agent.ZOOKEEPER_HOSTS = '127.0.0.1:2188'

    # 创建consumer对象
    # 参数1：队列amqp地址
    # 参数2：队列名称
    # 以下参数均可以省略
    # 参数3：日志对象，默认值为STDOUT
    # 参数4：Consumer最多拉取消息数量，默认值为30条
    # 参数5：线程数量，默认值为5
    # 参数6：心跳间隔，默认值为30秒
    # 参数7：Consumer标签，默认为None
    # 参数8：is_rpc，标识是否为RPC消费者，默认为False
    # 参数9：agent，是否启动监控线程，默认为True
    # 参数10：app_name，应用名称，监控线程采集使用，默认为None
    # 参数11：app_desc，应用描述，监控线程采集使用，默认为None
    c = consumer.Consumer('amqp://smallrabbit:123456@172.16.20.46:5673/journal',
                                      'q.journal.loginsync.save',
                                      logger)
    # 注册处理方法
    c.register_worker(worker)
    c.run()
except Exception as e:
    print(e.message)
except KeyboardInterrupt:
    c.stop()
```

### 进程版使用指南

与线程版使用方法相同，只是引入的包由`from ctec_consumer.dummy import consumer`替换为`from ctec_consumer import consumer`

**注意**：Python3以下的版本暂时无法使用进程版。

### Gevent版使用指南

与线程版使用方法相同，只是引入的包由`from ctec_consumer.dummy import consumer`替换为`from ctec_consumer.gevent import consumer`

### WorkerMessage对象

对象具有以下成员变量：

- `body`：消息内容
- `basic_deliver`：`pika.Spec.Basic.Deliver`
- `basic_properties`：`pika.Spec.BasicProperties`
- `delivery_tag`
- `properties`
- `is_publish`：是否要转发
- `exchange`：转发的exchange
- `routing_key`：转发的routing key
- `publish_properties`：转发的消息properties
- `publish_body`：转发消息的body，默认为该条消息的body属性

## 批量消费使用指南

**目前批量消费只支持异步客户端**

### 示例代码

```python
import ctec_consumer.consumer_log as ctec_logging
from ctec_consumer.async import consumer

# 创建logger对象方法1：
# 参数1：应用名称
# 参数2：日志路径
# 参数3：是否开启DEBUG，默认关闭。
ctec_logging.APP_NAME = 'app_name'
ctec_logging.LOG_PATH = '/opt/logs'
ctec_logging.DEBUG = True

# 定义处理方法，该方法接收一个参数WorkerMessage对象数组
# 方法必须要返回固定值，具体取值范围参照上一节文档
# WorkerMessage对象结构参见下文
def worker(messages):
    print(messages[0].body)
    # 处理逻辑....
    return ctec_consumer.CONSUME_SUCCESS

try:
    # 创建logger对象方法2：用于写日志。如果不指定，则默认写到STDOUT
    # 参数1：应用名称
    # 参数2：日志路径
    # 参数3：是否开启DEBUG，默认关闭。
    logger = ctec_logging.get_logger('app_name', '/opt/logs', debug=True)

    # 设置采集线程的Zookeeper地址，若关闭采集线程，此处可不进行设置
    data_agent.ZOOKEEPER_HOSTS = '127.0.0.1:2188'

    # 创建consumer对象
    # 参数1：队列amqp地址
    # 参数2：队列名称
    # 参数3（可省略）：日志对象，默认值为STDOUT
    # 参数4（可省略）：Consumer最多拉取消息数量，默认值为30条
    # 参数5（可省略）：线程数量，默认值为5
    # 参数6（可省略）：心跳间隔，默认值为30秒
    # 参数7（可省略）：Consumer标签，默认为None
    # 参数8（可省略）：是否为RPC请求，默认为False
    # 参数9（可省略）：批量消费消息数量，默认为1
    # 参数10（可省略）：agent，是否启动监控线程，默认为True
    # 参数11（可省略）：app_name，应用名称，监控线程采集使用，默认为None
    # 参数12（可省略）：app_desc，应用描述，监控线程采集使用，默认为None
    c = consumer.Consumer('amqp://smallrabbit:123456@172.16.20.46:5673/journal', 'q.journal.loginsync.save', logger)
    # 注册处理方法
    c.register_worker(worker)
    c.run()
except Exception as e:
    print(e.message)
except KeyboardInterrupt:
    c.stop()
```

### WorkerMessage对象属性

- `body`：消息内容
- `basic_deliver`：`pika.Spec.Basic.Deliver`
- `basic_properties`：`pika.Spec.BasicProperties`
- `delivery_tag`
- `properties`
- `is_publish`：是否要转发
- `exchange`：转发的exchange
- `routing_key`：转发的routing key
- `publish_properties`：转发的消息properties
- `publish_body`：转发消息的body，默认为该条消息的body属性

## 消息转发

支持将某一条消息转发到其它的队列中

在处理消息的过程中，设置`is_publish`为True，并且设置相关的消息转发参数即可。

## 应用状态监控

若开启监控线程（默认为开启），会每隔1分钟上传一次consumer的健康及监控信息到zookeeper中，对于部署在docker中的consumer，
建议设置container中的环境变量`HOST_IP`，以便可以正确统计到部署的主机IP。

监控信息目前包括：

- 应用名称
- 应用描述
- 部署路径
- 消费的队列信息
- 每分钟CPU使用率，保存24小时
- 每分钟内存的使用率，保存24小时
- 当前的线程数
- 每分钟的消费消息数量，保存24小时
- 部署的主机IP

准一zookeeper地址：172.16.50.216:2181
准二zookeeper地址：10.128.91.87:2181
生产zookeeper地址：10.128.2.93:2181,10.128.2.94:2181,10.128.2.95:2181

## 停止Consumer

Consumer中已经注册了2和15信号量，线程版可以直接向Consumer进程发送2和15信号量。参考命令：`kill -15 <pid>`

进程版Consumer需要向进程组号发送信号量，参考命令：`kill -- -<pid>`

## FAQ

- cx_Oracle使用过程中不定期进程退出，报错为OCI xxxxxxxxxxxxxx

在初始化Connection或SessionPool的时候，指定`threaded`参数为`True`