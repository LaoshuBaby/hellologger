# HelloLogger

Push your log to everywhere!

-----

PyPi: https://pypi.org/project/hellologger/

## 简介

HelloLogger是一个基于Loguru的同时向多个来源投送日志的日志框架，便于快速配置和接入Aliyun、AWS等SaaS；快速投递到ClickHouse、ElasticSearch、GreptimeDB、MongoDB等时序数据库或文档数据库；快速投递到Syslog或调用WebHook

希望这个日志库能帮助您解决复杂项目中留痕和云观测的难题。

## 数据驱动

### `file_local` (**`local`**)

可用的日志源：

* loguru

可用的数据驱动：

* loguru.default

可配置项：

* batch_time: 如果使用loguru，可以设定是否按照时间或者大小分批
* batch_size: 如果使用loguru，可以设定是否按照时间或者大小分批

### `file_s3` (**`s3`**)

**WIP**

其实就是本地文件一样的逻辑，只不过考虑不要落盘，全部在内存中进行。需要有好的S3驱动。

### `saas_aliyun_sls` (**`aliyun`**)

可用的日志源：

* loguru

可用的数据驱动：

* aliyun-restful-api (WIP)
* aliyun-log-python-sdk

#### 配置指南（aliyun-restful-api）

暂无，可参考官方文档手搓HTTP请求：https://help.aliyun.com/zh/sls/developer-reference/api-postlogstorelogs

#### 配置指南（aliyun-log-python-sdk）

该数据驱动依赖[aliyun/aliyun-log-python-sdk](https://github.com/aliyun/aliyun-log-python-sdk)项目，您需要提前安装对应package：

```bash
pip install aliyun-log-python-sdk
```

您需要配置2个本地环境变量：

* `ALIYUN_ACCESSKEY_ID`
* `ALIYUN_ACCESSKEY_SECRET`

需要注意的有：

1. 环境变量设置后请重启
2. 请确保您提供的AccessKey具有SLS的写权限。您可以在RAM中进行权限管理。
3. 即使开通了SLS服务，并创建了一个项目，创建了一个logstore，也必须手动在logstor管理界面进行一次“数据接入”操作，才算实质性开通，否则不允许从python-sdk上传日志。

### `saas_aws_cloudwatch` (**`aws`**)

**WIP**

似乎CloudWatch必须有本地客户端才能打日志，没法直接RESTful API调用。

### `db_clickhouse` (**`clickhouse`**)

**WIP**

### `db_elasticsearch` (**`elasticsearch`**)

**WIP**

计划依赖 https://pypi.org/project/elasticsearch-logging-handler/

### `protocal_syslog` (**`syslog`**)

**WIP**

详见 https://docs.render.com/log-streams#sumo-logic

### `protocal_webhook` (**`webhook`**)

**WIP**

计划支持包括但不仅限于如下平台的WebHook模板：
* Discord
* Slack
* Telegram

其中，Discord平台计划提供两个数据驱动，一个依赖loguru-discord，一个仍调用restful api

WebHook需要传入配置文件，以适配不同平台。如果没有指定，就默认Discord的。

## 日志源和未来架构愿景

目前仅有一个日志源loguru

提供的logger是loguru的logger，直接暴露，没有重新封装

在未来可能会封装出一个专门的logger，如：

```python
hellologger.log(level:str,message:str,device:str)
```

并可指定logging或者loguru来完成任务，避免有部分平台loguru就是打不上去的也能用本项目打上去。

引用hellologger从此一身轻！

