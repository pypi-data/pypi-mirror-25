# 电渠rabbitMQ Consumer

## 环境

`Python2` 或 `Python3`

- `kombu`
- `gevent`
- `pika`

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
from ctec_consumer.dummy import ctec_consumer

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
    # 创建consumer对象
    # 参数1：队列amqp地址
    # 参数2：队列名称
    # 参数3（可省略）：日志对象，默认值为STDOUT
    # 参数4（可省略）：Consumer最多拉取消息数量，默认值为30条
    # 参数5（可省略）：线程数量，默认值为5
    # 参数6（可省略）：心跳间隔，默认值为30秒
    # 参数7（可省略）：Consumer标签，默认为None
    consumer = ctec_consumer.Consumer('amqp://smallrabbit:123456@172.16.20.46:5673/journal',
                                      'q.journal.loginsync.save',
                                      logger)
    # 注册处理方法
    consumer.register_worker(worker)
    consumer.run()
except Exception as e:
    print(e.message)
except KeyboardInterrupt:
    consumer.stop()
```

### 进程版使用指南

与线程版使用方法相同，只是引入的包由`from ctec_consumer.dummy import ctec_consumer`替换为`from ctec_consumer import ctec_consumer`

**注意**：Python3以下的版本暂时无法使用进程版。

### Gevent版使用指南

与线程版使用方法相同，只是引入的包由`from ctec_consumer.dummy import ctec_consumer`替换为`from ctec_consumer.gevent import ctec_consumer`

### WorkerMessage对象

对象具有以下成员变量：

- `headers`：头部信息，返回dict对象
- `properties`：属性信息，返回dict对象
- `body`消息内容
- `content_encoding`
- `content_type`
- `delivery_info`
- `delivery_tag`
- `payload`：解码后的消息内容

## 批量消费使用指南

**目前批量消费只支持异步客户端**

### 示例代码

```python
import ctec_consumer.consumer_log as ctec_logging
from ctec_consumer.async import ctec_consumer

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
    consumer = ctec_consumer.Consumer('amqp://smallrabbit:123456@172.16.20.46:5673/journal', 'q.journal.loginsync.save', logger)
    # 注册处理方法
    consumer.register_worker(worker)
    consumer.run()
except Exception as e:
    print(e.message)
except KeyboardInterrupt:
    consumer.stop()
```

### WorkerMessage对象属性

- `body`：消息内容
- `basic_deliver`：`pika.Spec.Basic.Deliver`
- `properties`：`pika.Spec.BasicProperties`
- `delivery_tag`

## 停止Consumer

Consumer中已经注册了2和15信号量，线程版可以直接向Consumer进程发送2和15信号量。参考命令：`kill -15 <pid>`

进程版Consumer需要向进程组号发送信号量，参考命令：`kill -- -<pid>`

## FAQ

- cx_Oracle使用过程中不定期进程退出，报错为OCI xxxxxxxxxxxxxx

在初始化Connection或SessionPool的时候，指定`threaded`参数为`True`