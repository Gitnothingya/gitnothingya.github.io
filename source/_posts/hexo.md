---
title: 博客搭建
top: 100
tags: 
- hexo 
- npm
- git
- node
categories: 
- 学习
- 博客搭建
---
配置博客过程中遇到了许多问题，不少知识点，在该文档中进行总结，便于自己日后查看，重新配置。

**暂时搁置搭建，使用语雀进行学习记录**

# `hexo`

`npm` 命令与 `hexo`自带命令。

<!--more-->

```shell
npm install -g hexo-cli
npm install hexo 
//到指定文件夹运行命令

hexo init
//初始化博客框架

hexo g 
//生成网页

hexo s 
//本地查看网站

hexo d
//部署博客到github上，要两次才换主题，还是有延迟？
```

```shell
hexo new "title"
//生成新文章
```

```markdown
---
title: title
date: 2022-7-14 9:44:13
tags:
---
//front matter 页面属性？
```

```shell
hexo new draft "draft title"
//生成草稿，草稿不会被渲染

hexo new page "ppage title"
//生成纯页面
```

**`numjucks`语言**编写模板

`yaml`语法编写 `front matter`

# 部署博客

## `ssh-key`配置

## `_config.yml`配置

* `url \ root`
* `title \ author`
* `deploy : type \ repo \ branch`

## 主题

直接在 `\themes`文件夹下进行 `clone`然后直接修改克隆下的文件夹，例如对于 `NexT`主题

`git clone git@github.com:theme-next/hexo-theme-next.git `

然后将文件夹名由 `hexo-theme-next` 修改为 `next`

注意在博客框架的 `_config.yml`的主题类型

```
//next
https://github.com/theme-next/hexo-theme-next

//yilia-plus
https://github.com/JoeyBling/hexo-theme-yilia-plus
```

> `Adguard`插件导致主题更新延迟？

# 问题(警告、报错)

> * npm WARN config global `--global`, `--local` are deprecated. Use `--location=global` instead.
>
> **solution:**
>
> ```shell
> # 以管理员身份运行
> npm i -g npm-windows-upgrade  # cmd
> npm-windows-upgrade  
> # 然后选择最新版本
> # 第二个命令出现后如果出现报错，按照提示运行给出命令再次运行第二个即可
> Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force # 管理员运行powershell
> ```

> Connection reset by 20.205.243.166 port 22
> fatal: Could not read from remote repository.
>
> Please make sure you have the correct access rights
> and the repository exists.
> FATAL {
> err: Error: Spawn failed
> at ChildProcess.`<anonymous>` (D:\blog\node_modules\hexo-util\lib\spawn.js:51:21)
> at ChildProcess.emit (node:events:527:28)
> at ChildProcess.cp.emit (D:\blog\node_modules\cross-spawn\lib\enoent.js:34:29)
> at Process.ChildProcess._handle.onexit (node:internal/child_process:291:12) {
> code: 128
> }
> } Something's wrong. Maybe you can find the solution here: %s https://hexo.io/docs/troubleshooting.> html
>
> [Hexo错误：spawn failed的解决方法 | 张洪Heo (zhheo.com)](https://blog.zhheo.com/p/128998ac.html) 可参考进行部分配置确认，如文章开篇所言，可能大部分情况下都是网络的问题，重启或者等待一段时间再进行部署即可
>
> 可使用 `ssh -T git@github.com`进行网络确认

# 文档编写

文档头信息

```markdown
title: 文章标题
date: 2020-09-07 09:25:00  文章创建发布时间，未指明时会有内部记录文档添加进来的时间
author: 文章作者
img: 文章特征图路径，未尝试
top: 文章置顶 true / false
cover: 文章是否加入首页轮播封面？未尝试 true / false
coverImg: 文章在首页轮播封面需要显示的图片路径，如果没有，默认使用文章的特色图片
password: 文章阅读密码，必须是SHA256加密后的密码，使用前需要在主题的config.yml激活verifyPassword选项
toc: 是否开启TOC ， true / false
mathjax: false 是否开启数字公式支持，需要在主题的`_config.yml`文件中一同开启
description: 这是你自定义的文章摘要内容，如果这个属性有值，文章卡片摘要就显示这段文字，否则程序会自动截取文章的部分内容作为摘要
categories: 
- Markdown
- ... 使用多级目录，
tags:
  - Typora
  - Markdown
  使用多个标签
注意同一文章只有一种（多级）目录，可以多个标签
```

# 首页置顶
```shell
# 卸载原有插件安装另一个
npm uninstall hexo-generator-index --save
npm install hexo-generator-index-pin-top --save

# 文章增加top信息

# 添加置顶图标
# 打开 /blog/themes/hexo-theme-next/layout/_macro 目录下的 post.swig 文件，在<div class="post-meta">标签中插入如下代码：
{% if post.top %}
  <i class="fa fa-thumb-tack"></i>
  <font color=7D26CD>置顶</font>
  <span class="post-meta-divider">|</span>
{% endif %}
```


图片展示和下载？
![alt text](../images/client2.jpg)


资源可以直接放吗？
C源文件 server.cpp
{% include_code  lang:cpp server.cpp %}

makefile 
{% codeblock lang:makefile Makefile %}
all:
	g++ client.cpp -o client
	g++ server.cpp -o server
# 根据操作系统和编译器版本可能需要添加 -lpthread 参数
# 本地测试 ubuntu 22.04  g++-11.3.0
{%  endcodeblock %}


