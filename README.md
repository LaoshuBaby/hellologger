# HelloLogger

Push your log to everywhere!

-----

PyPi: https://pypi.org/project/hellologger/

## 简介

HelloLogger是一个基于Loguru的同时向多个来源投送日志的日志框架，便于快速配置和接入Aliyun、AWS等SaaS；快速投递到ClickHouse、ElasticSearch、GreptimeDB、MongoDB等时序数据库或文档数据库；快速投递到Syslog或调用WebHook

希望这个日志库能帮助您解决复杂项目中留痕和云观测的难题。

## 数据驱动

### 本地

如果使用loguru，可以设定是否按照时间或者大小分批

### Aliyun

需要使用 https://github.com/aliyun/aliyun-log-python-sdk 项目，并配置本地ALIYUN_ACCESSKEY_ID和ALIYUN_ACCESSKEY_SECRET两个环境变量

需要注意的是，即使开通了SLS服务，并创建了一个项目，创建了一个logstore，也必须手动进行一次导入数据源操作，否则不允许从python-sdk上传日志。

请确保您提供的AccessKey具有SLS的写权限。您可以在RAM中进行权限管理。

### AWS

WIP

### WebHook

WIP

## 愿景和未来架构预期

在未来可能会暴露出一个专门的hellologger.log(level:str,message:str,device:str)并指定logging或者loguru来完成任务，避免有部分平台loguru就是打不上去的也能用本项目打上去。引用hellologger从此一身轻！

（其实目前只允许你用loguru，提供的logger还是loguru的logger而没有重新封装一遍）