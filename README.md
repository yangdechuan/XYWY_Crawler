# 使用scrapy框架，爬取寻医问药网站所有问答。
##需要提前安装并开启mongodb数据库
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
