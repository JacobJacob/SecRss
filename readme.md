# SecRss
![miao](http://mweb.03sec.com/2018-01-29-timg.jpeg)

## 什么是SecRss？
- 将rss源每天更新的文章保存到本地
- 将rss源每天更新的文章通过平台推送给用户
- ……

## 环境要求：
- python3
- mysql

### 配置运行环境
1. 下载代码

```
git clone https://github.com/anbai-inc/SecRss.git
```

2. 安装依赖环境

```
pip3 install -r requirements.txt
```

3. 更改配置文件

配置文件位于`config`目录下的`news.cfg`文件
#### 配置文件字段解释
- database
数据库配置，具体的就不用说了吧？
- server
静态服务器的url配置，也可以是本地的路径，最后是要展现在网页里面的，确保你网页里面的图片能正常加载出来即可（如果你有网站展示的需要，可以将本项目下的static目录使用软连接的方式进行恭喜一个目录）
- picBlacklist
下载图片黑名单，用`,`号分割

## 平台编写

### 编写一个插件需要按照以下的格式进行编写

```
class Platform(Base):
    def __init__(self, news_list):
        super(Platform, self).__init__(news_list)
        self.info = {
            "name": "xxx", # 平台名字，需要与文件名一致
            "status": True, # 平台是否启用
            "save": True, # 是否存入数据库
            "images": True, # 是否下载图片
        }

    def push_message(self):
        """
        推送消息部分代码
        :return Boolean:
        """
        pass
```
### 注意事项
- 类名字必须为`Platform`,且必须实现`Base`基础类
- `__init__`方法里面的`info`必须按照格式去写，可以添加，不可以**删除**
- `push_message`方法需进行重写，方便对消息平台推送消息，最后返回的类型必须是Boolean类型
- 如果发现基础类里面的某个方法不适用与某个插件，可以对其进行重写

## rss订阅规则源编写
一条完整的rss规则，举个🌰：

```
{
    "name": "evi1cg",
    "s_title": "evi1cg",
    "rss": "https://evi1cg.me/feed",
    "has_content": "",
    "start_str": "<section class=\"post-main-section\">",
    "end_str": "<div class=\"post-tags\">",
    "language": "zh-cn",
    "lazyLoading":true,
    "lazyLabel":"data-original"
}
```
### 各个字段说明

| 字段名 | 描述 |
| --- | --- |
| name | 名字 |
| s_title | 入库时候保存的名字 |
| rss | rss订阅地址 |
| has_content | 采集的内容是否包含xxx，如果为空，则直接进行采集 |
| start_str | 采集文章开始的位置，html标签去表示 |
| end_str | 采集文章结束的位置，html标签去表示 |
| language | 网站语言类型 |
| lazyLoading | 图片是否为懒加载 |
| lazyLabel | 图片懒加载标签里面真实的图片地址 |


## 定是采集设置（适用于linux）
1. 在/var/目录下新建一个`run.sh`，输入以下代码，记住更改代码的绝对路径

```
/usr/bin/python3 /var/sec-news/current/run_news.py >>/var/log.log
```
2. 在linux下输入`crontab -e`，建立以下规则:

```
29 18 * * * /var/run.sh
```
该规则的意思为每天18点29分运行`var`目录下面的`run.sh`(我们上面保存run.sh的路径)

## 内置推送平台一览

> 所有插件都在目录`platform`下，如果你有新的平台插件愿意共享，欢迎向本项目提交push.

| 支持平台 | 模块名字 | 注意事项 | 预览 |
| --- | --- | --- | --- |
| 钉钉 | dingding.py | 需要使用者自己修改dingding.py里面的webhook地址，钉钉webhook申请流程：[点此查看](https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.EiKypY&treeId=257&articleId=105735&docType=1) | ![dingding](http://mweb.03sec.com/2018-01-29-15172071615268.jpg) |

