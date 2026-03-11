---
title: "MySQL 在 SELECT 的同时 UPDATE 同一张表"
source: https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html
asset_dir: assets/mysql-在-select-的同时-update-同一张表
---

# MySQL 在 SELECT 的同时 UPDATE 同一张表

[Mrxn](https://mrxn.net/author/1)- 发表于2019/4/15 22:54
- 2499浏览
- [1评论](#comment)
- 14分钟阅读

深入探索

恶意软件分析工具

服务器安全服务

Windows安全工具

---

MySQL 不允许 SELECT FROM 后面指向用作 UPDATE 的表，有时候让人纠结。当然，有比创建无休止的临时表更好的办法。本文解释如何 UPDATE 一张表，同时在查询子句中使用 SELECT.

编程

## 问题描述

假设我要 UPDATE 的表跟查询子句是同一张表，这样做有许多种原因，例如用统计数据更新表的字段（此时需要用 group 子句返回统计值），从某一条记录的字段 update 另一条记录，而不必使用非标准的语句，等等。举个例子：

```
create table apples(variety char(10) primary key, price int);

insert into apples values('fuji', 5), ('gala', 6);

update apples
    set price = (select price from apples where variety = 'gala')
    where variety = 'fuji';
```

错误提示是：ERROR 1093 (HY000): You can't specify target table'apples' for update in FROM clause. MySQL 手册 [UPDATE documentation](http://dev.mysql.com/doc/refman/5.0/en/update.html) 这下面有说明 : “Currently, you cannot update a table and select from the same table in a subquery.”  
  
在这个例子中，要解决问题也十分简单，但有时候不得不通过查询子句来 update 目标。好在我们有办法。

## 解决办法

既然 MySQL 是通过临时表来实现 FROM 子句里面的嵌套查询，那么把嵌套查询装进另外一个嵌套查询里，可使 FROM 子句查询和保存都是在临时表里进行，然后间接地在外围查询被引用。下面的语句是正确的：

```
update apples
   set price = (
      select price from (
         select * from apples
      ) as x
      where variety = 'gala')
   where variety = 'fuji';
```

如果你想了解更多其中的机制，请阅读 [MySQL Internals Manual](http://dev.mysql.com/doc/internals/en/select-derived.html) 相关章节。

深入探索

VPN服务

安全研究工具

Web安全课程

## 没有解决的问题

一个常见的问题是，IN() 子句优化废品，被重写成相关的嵌套查询，有时（往往？）造成性能低下。把嵌套查询装进另外一个嵌套查询里并不能阻止它重写成相关嵌套，除非我下狠招。这种情况下，最好用 JOIN 重构查询（[rewrite such a query as a join](http://www.xaprb.com/blog/2006/04/30/how-to-optimize-subqueries-and-joins-in-mysql/)）。  
另一个没解决的问题是临时表被引用多次。“装进嵌套查询” 的技巧无法解决这些问题，因为它们在编译时被创建，而上面讨论的 update 问题是在运行时。（译者注：个人认为跟文章讨论的主题没几毛钱关系）  
原文地址：<http://www.xaprb.com/blog/2006/06/23/how-to-select-from-an-update-target-in-mysql/>

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#SQL](https://mrxn.net/tag/SQL)
- [#MySQL](https://mrxn.net/tag/MySQL)

---

文章目录

- [1.
  问题描述](#toc-1-)
- [2.
  解决办法](#toc-2-)
- [3.
  没有解决的问题](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
