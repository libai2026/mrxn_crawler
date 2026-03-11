---
title: "「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%"
source: https://mrxn.net/jswz/updaet_modify_freebuf_pic.html
asset_dir: assets/「更新」油猴脚本-freebuf文章图片去除!small并自动缩放图片大小到100%
---

# 「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%

[Mrxn](https://mrxn.net/author/1)- 发表于2019/5/1 16:38
- 3288浏览
- [6评论](#comment)
- 5分钟阅读

深入探索

SQL

安全研究报告

漏洞扫描服务

---

我之前写过一篇文章是关于freebuf文章图片去除!small得，地址在这里:<https://mrxn.net/jswz/modify_freebuf_pic.html>，但是后来我发现有一个BUG，很严重得那种：因为我当时在写插件的时候是在文章全部浏览完后直接写得，这也就导致了我当时忽略了 freebuf 的图片是懒加载的，这样的话如果还是像我之前那样直接去除图片 src 末尾的 !small ，会导致没有在第一屏内的图片不会被渲染出来！so ，趁着这次五一国际劳动节放假当天，我就来更新来了！本次更新重新设计了一下，就是取消掉了那个小标签添加，在文章页面禁用了lazyload加载，当你读文章慢慢往下滚动的时候就可以自动去除图片末尾的 !small 了，而且回自动修改图片的宽度属性到 100% (受父节点限制，不会撑爆的)，尽可能的显示图片大小从而方便阅读。[![「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%](images/img-001-2f1e8a64c823.gif "脚本演示")](https://raw.githubusercontent.com/Mr-xn/modify_freebuf_pic/master/%E5%8E%BB%E9%99%A4!small.gif)

### [Greasy Fork 在线下载安装](https://greasyfork.org/zh-CN/scripts/381845-freebuf%E6%96%87%E7%AB%A0%E5%9B%BE%E7%89%87%E5%8E%BB%E9%99%A4-small)

Github地址：<https://github.com/Mr-xn/modify_freebuf_pic>

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#JavaScript](https://mrxn.net/tag/JavaScript)

---

文章目录

- [1.
  Greasy Fork 在线下载安装](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
