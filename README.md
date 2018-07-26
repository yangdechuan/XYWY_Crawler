# 使用scrapy框架，爬取寻医问药网站所有问答。
## 需要提前安装并开启mongodb数据库
以ubuntu为例，安装配置方式如下：
1. 安装mongodb
```
sudo apt-get install mongodb
```
2. 启动mongodb
```
service mongodb start
```
## 程序执行方式如下：
```
scrapy crawl xywy_spider
```
## 在数据库中查看爬取的数据
mongo命令进入数据库交互窗口
```
show dbs; # 查看有哪些数据库
use xywy; # 进入数据库
show collections; # 查看当前数据库中的表
db.xywy_qa.find(); # 查看该表中的数据
db.xywy_qa.find().count(); 数据量
```
