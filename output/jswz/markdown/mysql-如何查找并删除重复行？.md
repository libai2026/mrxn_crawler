---
title: "MySQL 如何查找并删除重复行？"
source: https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html
asset_dir: assets/mysql-如何查找并删除重复行？
---

# MySQL 如何查找并删除重复行？

[Mrxn](https://mrxn.net/author/1)- 发表于2019/4/15 22:50
- 2277浏览
- [0评论](#comment)
- 2小时阅读

深入探索

Web安全书籍

安全认证考试

云安全解决方案

---

## 如何查找重复行

        第一步是定义什么样的行才是重复行。多数情况下很简单：它们某一列具有相同的值。本文采用这一定义，或许你对“重复”的定义比这复杂，你需要对sql做些修改。  
本文要用到的数据样本

编程

```
create table test(id int not null primary key, day date not null);

insert into test(id, day) values(1, '2006-10-08');
insert into test(id, day) values(2, '2006-10-08');
insert into test(id, day) values(3, '2006-10-09');

select * from test;
+----+------------+
| id | day        |
+----+------------+
|  1 | 2006-10-08 |
|  2 | 2006-10-08 |
|  3 | 2006-10-09 |
+----+------------+
```

        前面两行在day字段具有相同的值，因此如何我将他们当做重复行，这里有一查询语句可以查找。查询语句使用GROUP BY子句把具有相同字段值的行归为一组，然后计算组的大小。

```
select day, count(*) from test GROUP BY day;
+------------+----------+
| day        | count(*) |
+------------+----------+
| 2006-10-08 |        2 |
| 2006-10-09 |        1 |
+------------+----------+
```

        重复行的组大小大于1。如何希望只显示重复行，必须使用HAVING子句，比如

```
select day, count(*) from test group by day HAVING count(*) > 1;
+------------+----------+
| day        | count(*) |
+------------+----------+
| 2006-10-08 |        2 |
+------------+----------+
```

深入探索

授权

计算机安全

JSON处理工具

        这是基本的技巧：根据具有相同值的字段分组，然后知显示大小大于1的组。

### 为什么不能使用WHERE子句？

        因为WHERE子句过滤的是分组之前的行，HAVING子句过滤的是分组之后的行。

## 如何删除重复行

        一个相关的问题是如何删除重复行。一个常见的任务是，重复行只保留一行，其他删除，然后你可以创建适当的索引，防止以后再有重复的行写入数据库。  
同样，首先是弄清楚重复行的定义。你要保留的是哪一行呢？第一行，或者某个字段具有最大值的行？本文中，假设要保留的是第一行——id字段具有最小值的行，意味着你要删除其他的行。  
        也许最简单的方法是通过临时表。尤其对于MYSQL，有些限制是不能在一个查询语句中select的同时update一个表。在我的另一篇文章中 [MySQL 在 SELECT 的同时 UPDATE 同一张表](https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html)([How to select from an update target in MySQL](http://www.xaprb.com/blog/2006/06/23/how-to-select-from-an-update-target-in-mysql/)), 讲述了如何绕过这些限制。简单起见，这里只用到了临时表的方法。  
我们的任务是：删除所有重复行，除了分组中id字段具有最小值的行。因此，需要找出大小大于1的分组，以及希望保留的行。你可以使用MIN()函数。这里的语句是创建临时表，以及查找需要用DELETE删除的行。

编程

深入探索

软件

Web安全课程

防火墙软件

```
create temporary table to_delete (day date not null, min_id int not null);

insert into to_delete(day, min_id)
   select day, MIN(id) from test group by day having count(*) > 1;

select * from to_delete;
+------------+--------+
| day        | min_id |
+------------+--------+
| 2006-10-08 |      1 |
+------------+--------+
```

        有了这些数据，你可以开始删除“脏数据”行了。可以有几种方法，各有优劣（详见我的文章many-to-one problems in SQL），但这里不做详细比较，只是说明在支持查询子句的关系数据库中，使用的标准方法。

```
delete from test
   where exists(
      select * from to_delete
      where to_delete.day = test.day and to_delete.min_id <> test.id
   )
```

### 如何查找多列上的重复行

        有人最近问到这样的问题：  
我的一个表上有两个字段b和c，分别关联到其他两个表的b和c字段。我想要找出在b字段或者c字段上具有重复值的行。  
        咋看很难明白，通过对话后我理解了：他想要对b和c分别创建unique索引。如上所述，查找在某一字段上具有重复值的行很简单，只要用group分组，然后计算组的大小。并且查找全部字段重复的行也很简单，只要把所有字段放到group子句。但如果是判断b字段重复或者c字段重复，问题困难得多。这里提问者用到的样本数据

```
create table a_b_c(
   a int not null primary key auto_increment,
   b int,
   c int
);

insert into a_b_c(b,c) values (1, 1);
insert into a_b_c(b,c) values (1, 2);
insert into a_b_c(b,c) values (1, 3);
insert into a_b_c(b,c) values (2, 1);
insert into a_b_c(b,c) values (2, 2);
insert into a_b_c(b,c) values (2, 3);
insert into a_b_c(b,c) values (3, 1);
insert into a_b_c(b,c) values (3, 2);
insert into a_b_c(b,c) values (3, 3);
```

        现在，你可以轻易看到表里面有一些重复的行，但找不到两行具有相同的二元组{b, c}。这就是为什么问题会变得困难了。

### 错误的查询语句

        如果把两列放在一起分组，你会得到不同的结果，具体看如何分组和计算大小。提问者恰恰是困在了这里。有时候查询语句找到一些重复行却漏了其他的。这是他用到了查询

```
select b, c, count(*) from a_b_c
group by b, c
having count(distinct b > 1)
   or count(distinct c > 1);
```

        结果返回所有的行，因为CONT(\*)总是1.为什么？因为 >1 写在COUNT()里面。这个错误很容易被忽略，事实上等效于

```
select b, c, count(*) from a_b_c
group by b, c
having count(1)
   or count(1);
```

为什么？因为 (b> 1) 是一个布尔值，根本不是你想要的结果。你要的是：

```
    select b, c, count(*) from a_b_c
    group by b, c
    having count(distinct b) > 1
       or count(distinct c) > 1;
```

        返回空结果。很显然，因为没有重复的{b,c}。这人试了很多其他的OR和AND的组合，用来分组的是一个字段，计算大小的是另一个字段，像这样

```
select b, count(*) from a_b_c group by b having count(distinct c) > 1;
+------+----------+
| b    | count(*) |
+------+----------+
|    1 |        3 |
|    2 |        3 |
|    3 |        3 |
+------+----------+
```

        没有一个能够找出全部的重复行。而且最令人沮丧的是，对于某些情况，这种语句是有效的，如果错误地以为就是这么写法，然而对于另外的情况，很可能得到错误结果。

        事实上，单纯用GROUP BY 是不可行的。为什么？因为当你对某一字段使用group by时，就会把另一字段的值分散到不同的分组里。对这些字段排序可以看到这些效果，正如分组做的那样。首先，对b字段排序，看看它是如何分组的

| a | b | c |
| --- | --- | --- |
| 7 | 1 | 1 |
| 8 | 1 | 2 |
| 9 | 1 | 3 |
| 10 | 2 | 1 |
| 11 | 2 | 2 |
| 12 | 2 | 3 |
| 13 | 3 | 1 |
| 14 | 3 | 2 |
| 15 | 3 | 3 |

        当你对b字段排序（分组），相同值的c被分到不同的组，因此不能用COUNT(DISTINCT c)来计算大小。COUNT()之类的内部函数只作用于同一个分组，对于不同分组的行就无能为力了。类似，如果排序的是c字段，相同值的b也会分到不同的组，无论如何是不能达到我们的目的的。

### 几种正确的方法

        也许最简单的方法是分别对某个字段查找重复行，然后用UNION拼在一起，像这样：

```
 select b as value, count(*) as cnt, 'b' as what_col
 from a_b_c group by b having count(*) > 1
 union
 select c as value, count(*) as cnt, 'c' as what_col
 from a_b_c group by c having count(*) > 1;
+-------+-----+----------+
| value | cnt | what_col |
+-------+-----+----------+
|     1 |   3 | b        |
|     2 |   3 | b        |
|     3 |   3 | b        |
|     1 |   3 | c        |
|     2 |   3 | c        |
|     3 |   3 | c        |
+-------+-----+----------+
```

        输出what\_col字段为了提示重复的是哪个字段。另一个办法是使用嵌套查询：

```
select a, b, c from a_b_c
    where b in (select b from a_b_c group by b having count(*) > 1)
        or c in (select c from a_b_c group by c having count(*) > 1);
+----+------+------+
| a  | b    | c    |
+----+------+------+
|  7 |    1 |    1 |
|  8 |    1 |    2 |
|  9 |    1 |    3 |
| 10 |    2 |    1 |
| 11 |    2 |    2 |
| 12 |    2 |    3 |
| 13 |    3 |    1 |
| 14 |    3 |    2 |
| 15 |    3 |    3 |
+----+------+------+
```

        这种方法的效率要比使用UNION低许多，并且显示每一重复的行，而不是重复的字段值。还有一种方法，将自己跟group的嵌套查询结果联表查询。写法比较复杂，但对于复杂的数据或者对效率有较高要求的情况，是很有必要的。

```
    select a, a_b_c.b, a_b_c.c
    from a_b_c
       left outer join (
          select b from a_b_c group by b having count(*) > 1
       ) as b on a_b_c.b = b.b
       left outer join (
          select c from a_b_c group by c having count(*) > 1
       ) as c on a_b_c.c = c.c
    where b.b is not null or c.c is not null
```

以上方法可行，我敢肯定还有其他的方法。如果UNION能用，我想会是最简单不过的了。  
  
原文地址：<https://www.xaprb.com/blog/2006/10/09/how-to-find-duplicate-rows-with-sql/>

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#SQL](https://mrxn.net/tag/SQL)
- [#MySQL](https://mrxn.net/tag/MySQL)

---

文章目录

- [1.
  如何查找重复行](#toc-1-)
- [1.1.
  为什么不能使用WHERE子句？](#toc-1-1-)
- [2.
  如何删除重复行](#toc-2-)
- [2.1.
  如何查找多列上的重复行](#toc-2-1-)
- [2.2.
  错误的查询语句](#toc-2-2-)
- [2.3.
  几种正确的方法](#toc-2-3-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALUUlEQVR4Aeyb23bjthJEtfP//3yOW5VNEU1AlC+x/EAvw8W6dBNGU/FYk/nndrv97yvrfycf9jyJbfde5XofuTir617n1qiL6uJK1xd7Tv4VrIF81F2ff+UEtoF8TPv2ynp14/YCbsBWBgx8M/69gPgQ/Fe+1wDSKQL33NR8QYTUQ7B/DxAdRly1tv4M9/XbQPbidf2+EzgMBMbpQ/irW4TP5X16ev/P6r1+xmG+t34vObyWn91rr0H6wIj7jNeHgWhc+J4T+LGBQKbfn67O/TYheRhRv+Oqzz5nZq/V9Uov7yfWT/b/sYH8xDd29bjdvj0Q4P4nG58SmHMP21zn6iI872M9JAcP1BMhXuf9XvqvovWv5l/JfXsgr9zkyrx+AoeBOPWOq5bmYPcUfoQhXP9Dun9C9Dv5+ALhEPyQ7p/WwajfzY8v+jP8sO+fkNpZpjSY+/fijy+V2a8P6f4JqbuTF77se+yvZ6WHgcxCl/Z7J7ANBDJ1eI59a5C8k9eXw3N/lVcX7ScXIf0BpQ2tAe4/5zQg/Mxf5dVFSD+5CNHhOZov3AZS5FrvP4F/fEo+i6ut20e/c3XIU6MPIzd3htYXrrLl1TrzYb6Hqq3V6yH5rlf2q+t6hfTTfDM/DAQydQj2/UF0CL7qw5j3CYLocvtBdHlHiA9HNAvx5B0hPgTdA4T3/Ir3OhjrYeSrPqUfBlLitd53Av9ApgdBp73akn5H85/VrYPcXy7aD+LLZ2iNaEb+KloHuScErdcX1c8Qxj6z/PUKmZ3KG7XTgcA4VQiHYN87PNchPgSt92mD6J3fbrd7FOLfSftijdjs++8iQJcPHLhnNc76wZi37it4OpCvNL1qvn4C20D6U9C5t1jpkKdEH8J7nX5HSF4dRq4uQnx4Ha0V3dsKVznIPXtdz8M8B3O9+m0DKXKt95/AYSAwnx5Eh+DZ1ldPC4z1EG4e5hyiQ/Ds/nu/9957s+uzvP6sdqat8pDvBR54GMis4aX93glsA4FMyWnCyN2SvhzGHITri71OfYWQPtZ9Blc97QHpbU5d3hHGPIRbJ1rXOSSv/wy3gTwLXd7vncDh3d6zW8M47f40dA7JQ/Csv7594HkdxAcsXSLw9PcLiA/B3giiu7eVD8l137pneL1C+qm9mW8DgUwVgu4LRt6nC/Eh2OvMq8thnjcHcx+iQ9B+hdbW9X6pT3EnWrOT7pddh9wbRuy5zu/NPr7AWPchbZ/bQDblunjrCWwDcZod++5gnK55cxD/VW6uY++74pD7AVsL4P6zAkbsPbaCxUXPy0XLVhxyf3OieRGSA77/P8rdro8fPYHD34ecdXeqonm5qC52vXNzIuSpkYvWQXx5IUQzK5ZXa8UhdRCsbC0It06E6JWpBeH6Ynm15K/g9p+sV8JX5r8/geXvIZCp14RruRWILhdh1KumVvdLqwXzfHmzBWO+9wUO/wJsloH0gQd6P/Piq7o5ePSEx7X9INqKl369QuoU/tDaBgKZHgT7Hn0KREgOgiu994Exb505iC8XzcHcN/cVhPTs94DoMOLZPexjrnP1GW4DmZmX9vsnsA1kNUXI0+HWILznIbq57nduDlIHwa6vuPoeIT0g6D3Ffbau1cXSZktfhPTvWf3b7Xa3Or+LJ1+2gZzkLvuXTmD7PcT79anKIU+FfJVX7wip73rv131InblXcNVD3R6Q3hDsfs91Xy5C+kBQXbRf5+qF1yvE0/kjuP0eAvOpwqhDOIy4+n5q6rX067oWpF5dLG+/1CF5OEdrRPvJxZUO4z1ezdlXhLEPhOvP8HqFzE7ljdr2M8SnAOZT1O/o3tXlIqSfPsx5z8tXaL8ZWgO5FwTNQri5V3VIHQSt633URX0RUt85cL3be/tjH4efIU5V7PuFcbrdP+P2hed9IL55sfeH5IBuHd7bAu5/T7Lq1XVI3sbdV+8IY51+r4fk1AuvnyGe1h/BayB/ZBBuY/uhrrDH2XW9rGrNvL0GeTmqQTgE1atXrc5Lq6UOY516ZVxqIsxrug9jrvfrvNfLxVfzs9z1CvEU/whuA3FaMD4t7hOiw4j6on3kYtflkH5y8xBdvvIhOXigNR17D/0zHR69AcsOCNz/0AAjHoJPhG0gTzKX9YsnsP2x13v6tECmLO++uqgvdh3GfjDn1ouQnFzs/dUL9cTSasHYa+VDchDsOblYvfer6/KOkP7wwOsVsj/JP3C9DQQeU4LH/zAA0d0rhENQXYRRXz0Vq7x6Rxj7dv8V7l4gvSDYa82J+nKY15mD+Ks8xDdvrnAbiOaF7z2BbSA1nVp9O6XVUq/rWnKYTxuiw4hVu1/2WeE+W9fmIH1L68tMRxhr9CF65zDq+t4P4stFcx0h+ZUOXG8u3v7Yx+lv6jBOFUbuUwFzXV+83XICkLy6CKMO4RA0ly7Pv0JqIPiZ2llnSB8I9gzMdXPeX1Tf4/afrL14Xb/vBA6/h6y24lQ7mleH+VMC0SG4ynddLq7uB+kLD+xZubjqqb/CXmeu65C9dH2VL/16hdQp/KF1OpA+XcjU/R4gHILmIdycuth1OaTOHITrixDdXKFeXdeSQ7LyzyKkvnrWsr6ua0F8COqLMNf1q4frdCAWXfg7J3D4U5aTgkwVgm6n+3IRxrx1MNf1Rft0DvN6iA7rdxfsBY8soLwhcH+31j10hPgWwMh73py6HFIHQfXC6xVSp/CH1mEgcJzafr8w9yF6fxqsXemQOnMQDiPqv4L9XvKOkHusdO8FyclF6+QdV766uK87DGRvXte/fwLL30Ocngh5SuSiW5bDmNMXIT4EX63r9dapP0PIvcxAeO8Bow4jNw/RIaje+59xSL25wusVUqfwh9Y2EBinBSN3zzDX9UV4nutPVa/T72huhjDe01qzEL/r+iKMOQjX7wjxIWh/CDcPI+854Hq39/bHPrZXiPtyaiI8n6p1onVymNd33zqx+/Jn2GvNrnTI3iBovqP1kJzcnFyE5PRFfRGOucNALL7wPSdwOhCn6fYgU+169+XmIHUQ7L4c4kNQvSPEt38hROtZeWVqwZgrbb/Mn6E15iB91TtCfAhat8+dDsSiC3/nBA4DgUwPgm5jP8W6hvgwYnm1rIP48vJqQXQY0dwZVo9a8KgvXgseGjyuVz3hkYHHe2I9X71rdX3FYexrrnrsFzxyh4FYdOF7TuDwbq/bcIJyETLN7q941+2zQvMdIfe1DkZeOhy10u0Fc78y8zWqkHoI6sJzbm6F7q/weoWsTulN+vZeVk1nv1b7MbPyIU8LjGgdRJd3tC8kJzfXufoezYgw9lLf1+yvIXkYsddB/K7ve9W1vghjHYQD12/qtz/2sf0MgceU4Pz67PuoJ2O/eh5yj5/Sgd7q8I8+3Y9B4P43hBBU7zn1jqscjP1WdXDMXT9D+mm9mW8Dcdpn2PdrvuuQ6cOIPQ/xre/+q3rVmRUhvWFE/arZLxhzeuZfxa/WVf9tIEWu9f4TOAwExqcEwr+71f7UyEXIfSCovrovJAdHtMYeovoKzYmQ3nIRovc+EB1G7Lln/DCQZ+HL++9P4NsDgfnT4NO0+hYgdStfHcacfUVzzxDSo9dAdBix94LRtw9El/e6rstXufK/PZDe/OLfO4EfG0hNd79g/vTAXLd29e1A6mBE6wqtreta8o7l7Ze+GuQe8o7mRUhebh5GXf8Z/thAnt3k8l4/gcNAnG7HVUtzKx/mTwnM9d5vxbu+vz+Mvc3CqO9r6hrimy+tFkSv61oQbk4s75UFY/2+5jCQvXld//4JbAOBTA2e42qLkDp9nxoR4svNiRB/xdVFSB4e+NnekFrrxH6PFe96r9dXh9xPHcLhgdtADF343hO4BvLe8z/c/f8AAAD//8Wrhh8AAAAGSURBVAMAVGHdxWSA3+EAAAAASUVORK5CYII=)

手机扫码阅读
