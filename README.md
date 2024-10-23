# pandas 外置手册(U-tools专用)

本手册依赖[uTools效率工具](http://www.u.tools/)及其插件[程序员手册](https://yuanliao.info/d/356-1-1-4-bug-tmux)开发。

## 手册制作

1. 使用Python脚本`pandas_doc_spider.py`爬取[pandas](https://pandas.pydata.org/docs/reference/index.html)的API文档，并生成适用于[程序员手册](https://yuanliao.info/d/356-1-1-4-bug-tmux)的目录文件；
2. 自定义CSS。

## 手册优点：

1. 借助Utools可实现API速查
2. 离线文档，搜索速度比官方快很多
3. 精简全部JS引入，提高加载速度
4. 精简部分CSS样式，提高阅读体验
5. 精简无关标签，提高阅读体验

## 使用方法：

1. 下载并安装[uTools效率工具](http://www.u.tools/)；
2. 下载[pandas 外置手册](https://github.com/Nothing1024/Pytorch-handbook-Utools/releases)并解压；
3. 在[uTools效率工具](http://www.u.tools/)的插件市场中安装`程序员手册插件；
4. 在手册插件的`手册设置`中添加手册，根据需要配置名称，关键字，说明，路径（解压后手册的绝对路径）；
5. 点击`保存`，打开手册开关。

## 结果展示

![image](https://user-images.githubusercontent.com/71422761/156357160-ac86d5e7-0041-438f-88a2-26136860282e.png)

![image](https://user-images.githubusercontent.com/71422761/156357208-88ba4f2d-a1e8-4276-91ed-7ec9ad88ca57.png)

