# alidiary
> 使用python，在新浪云上开发微信公众号后台

## 用户手册

1. 看段子，输入指令，如:'段子'，看搞笑段子。
2. 天气查询，输入城市+天气，如:'上海天气'，查询上海天气。
3. 英汉互译，输入fy+要翻译的内容，如：'fy+hello'，翻译'hello'。
4. 调戏小阿狸，输入'ali'即可进入聊天模式，输入'bye'退出聊天模式。
5. 反馈功能，输入fk+要反馈的内容，如：'fk+小阿狸真可爱！'。
6. 更多功能，敬请期待……


![ali.png](http://upload-images.jianshu.io/upload_images/688387-f42a74208981b2d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![functions.png](http://upload-images.jianshu.io/upload_images/688387-ea2e484adec15cfe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 功能演示
### 1、段子
使用python抓取糗事百科上的最火的搞笑段子，抓取后解析展示给用户。

### 2、天气查询
获取城市名称之后，调用了阿里云市场的天气预报查询API，获取字符串数据，转化为json格式，简单处理之后展示给用户。

### 3、英汉互译
调用有道云翻译的API，简单处理之后展示给用户。

### 4、调戏小阿狸
调用图灵机器人的API，简单处理之后展示给用户。

### 5、反馈功能
存储用户反馈信息

### 6、其他
后续更新，敬请期待……