---
title: "MySQL 在 SELECT 的同时 UPDATE 同一张表"
source: https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html
asset_dir: embedded-base64
---

MySQL 不允许 SELECT FROM 后面指向用作 UPDATE 的表，有时候让人纠结。当然，有比创建无休止的临时表更好的办法。本文解释如何 UPDATE 一张表，同时在查询子句中使用 SELECT.

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

搜索

网络设备

客户关系管理

## 没有解决的问题

一个常见的问题是，IN() 子句优化废品，被重写成相关的嵌套查询，有时（往往？）造成性能低下。把嵌套查询装进另外一个嵌套查询里并不能阻止它重写成相关嵌套，除非我下狠招。这种情况下，最好用 JOIN 重构查询（[rewrite such a query as a join](http://www.xaprb.com/blog/2006/04/30/how-to-optimize-subqueries-and-joins-in-mysql/)）。  
另一个没解决的问题是临时表被引用多次。“装进嵌套查询” 的技巧无法解决这些问题，因为它们在编译时被创建，而上面讨论的 update 问题是在运行时。（译者注：个人认为跟文章讨论的主题没几毛钱关系）  
原文地址：<http://www.xaprb.com/blog/2006/06/23/how-to-select-from-an-update-target-in-mysql/>
