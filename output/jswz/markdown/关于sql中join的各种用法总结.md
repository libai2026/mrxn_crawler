---
title: "关于SQL中join的各种用法总结"
source: https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html
asset_dir: assets/关于sql中join的各种用法总结
---

# 关于SQL中join的各种用法总结

[Mrxn](https://mrxn.net/author/1)- 发表于2019/4/17 20:58
- 3061浏览
- [0评论](#comment)
- 55分钟阅读

深入探索

数据库

MySQL

SQL

---

首先声明：文章来源于国外的 **codeproject** 我这里只是由于复习**[SQL](https://mrxn.net/tag/SQL)**的时候需要就**Google**搜索[可以用我个人搭建的[**Googl**e搜索](https://g.mrxn.net/)供大家搜索文章学习使用]了一下，找到这篇文章,再次做个简单的记录同时也方便以后的有缘人，如有侵权的地方还请来信注明，感谢原文的作者的勤劳付出，留下如此详细全面的关于**[SQL](https://mrxn.net/tag/MySQL)**的join的用法。  
  
**codeproject**是国外一个免费的可以公开自己写的代码与程序的优秀网站有点类似于**[GitHub](https://mrxn.net/tag/github)**只不过是社区版，在这个网站所有用户都可以发布自己写过的代码，程序，或者是详细的文档说明。比国内的cnblog、csdn都要好，如果要说缺点的话，就是全英文的，当然大部分还是比较容易理解的。但是**codeproject**也有中文区: <https://www.codeproject.com/Forums/1580230/General-Chinese-Topics.aspx> ,感兴趣的可以去注册玩。  
  
我们先用一张图来看一下 LEFT JOIN、RIGHT JOIN、INNER JOIN、OUTER JOIN 等七种 join 相关的用法：  
  
 [[![关于SQL中join的各种用法总结](images/img-001-1c4a15475938.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201904/69891555507304.jpg)](https://mrxn.net/content/uploadfile/201904/69891555507304.jpg)下面分开说明这七种用法，先说第一种：  
  
**`1.INNER JOIN（内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-002-91bc50373ad2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/73071555507921.png)](https://mrxn.net/content/uploadfile/201904/73071555507921.png)这是最简单，最容易理解的Join，也是最常见的。此查询将返回左表（表A）中右表（表B）中都具有匹配记录的所有记录(共同拥有的相同的部分)。此Join用法的代码大致如下：

```
SELECT <select_list> 
FROM Table_A A
INNER JOIN Table_B B
ON A.Key = B.Key
```

**`2.LEFT JOIN（左连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-003-929394749987.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/bfdb1555508227.png)](https://mrxn.net/content/uploadfile/201904/bfdb1555508227.png)LEFT JOIN 关键字会从左表 (table\_name1) 那里返回所有的行，即使在右表 (table\_name2) 中没有匹配的行。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
LEFT JOIN Table_B B
ON A.Key = B.Key
```

**`3.RIGHT JOIN（右连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-004-860575589443.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/28821555508227.png)](https://mrxn.net/content/uploadfile/201904/28821555508227.png)   
  
RIGHT JOIN 关键字从右表（table2）返回所有的行，即使左表（table1）中没有匹配。如果左表中没有匹配，则结果为 NULL。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
RIGHT JOIN Table_B B
ON A.Key = B.Key
```

**`4.OUTER JOIN（外连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-005-1c19511192a3.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/de141555508227.png)](https://mrxn.net/content/uploadfile/201904/de141555508227.png)   
  
FULL OUTER JOIN 关键字只要左表（table1）和右表（table2）其中一个表中存在匹配，则返回行. FULL OUTER JOIN 关键字结合了 LEFT JOIN 和 RIGHT JOIN 的结果。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.Key = B.Key
```

**`5.LEFT JOIN EXCLUDING INNER JOIN（左连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-006-3848e9fa3f39.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/41161555508227.png)](https://mrxn.net/content/uploadfile/201904/41161555508227.png)   
  
此查询将返回左表（表A）中与右表（表B）中的任何记录都不匹配的所有记录。此Join的编写如下：

编程

```
SELECT <select_list> 
FROM Table_A A
LEFT JOIN Table_B B
ON A.Key = B.Key
WHERE B.Key IS NULL
```

**`6.RIGHT JOIN EXCLUDING INNER JOIN（右连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-007-b884fadb4576.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/bf0b1555508227.png)](https://mrxn.net/content/uploadfile/201904/bf0b1555508227.png)   
  
此查询将返回右表（表B）中与左表（表A）中的任何记录都不匹配的所有记录。此Join的编写如下：

搜索引擎

```
SELECT <select_list>
FROM Table_A A
RIGHT JOIN Table_B B
ON A.Key = B.Key
WHERE A.Key IS NULL
```

**`7.OUTER JOIN EXCLUDING INNER JOIN（外连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-008-1173d2785ce7.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/01931555508227.png)](https://mrxn.net/content/uploadfile/201904/01931555508227.png)   
  
  
  
此查询将返回左表（表A）中的所有记录以及右表（表B）中都不匹配的所有记录。我还没有需要使用这种类型的Join，但是其他的类型，我经常使用。此Join的编写如下：

```
SELECT <select_list>
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.Key = B.Key
WHERE A.Key IS NULL OR B.Key IS NULL
```

下面举一些例子：

假设我们有两个表，Table\_A和Table\_B。这些表中的数据如下所示：  

```
TABLE_A
  PK Value
---- ----------
   1 FOX
   2 COP
   3 TAXI
   6 WASHINGTON
   7 DELL
   5 ARIZONA
   4 LINCOLN
  10 LUCENT

TABLE_B
  PK Value
---- ----------
   1 TROT
   2 CAR
   3 CAB
   6 MONUMENT
   7 PC
   8 MICROSOFT
   9 APPLE
  11 SCOTCH
```

这七种连接方式的结果如下所示：  

```
-- INNER JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
       B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
INNER JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7

(5 row(s) affected)
```

```
-- LEFT JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
LEFT JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   4 LINCOLN    NULL       NULL
   5 ARIZONA    NULL       NULL
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
  10 LUCENT     NULL       NULL

(8 row(s) affected)
```

```
-- RIGHT JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
RIGHT JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11

(8 row(s) affected)
```

```
-- OUTER JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11
   5 ARIZONA    NULL       NULL
   4 LINCOLN    NULL       NULL
  10 LUCENT     NULL       NULL

(11 row(s) affected)
```

```
-- LEFT EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
LEFT JOIN Table_B B
ON A.PK = B.PK
WHERE B.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   4 LINCOLN    NULL       NULL
   5 ARIZONA    NULL       NULL
  10 LUCENT     NULL       NULL
(3 row(s) affected)
```

```
-- RIGHT EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
RIGHT JOIN Table_B B
ON A.PK = B.PK
WHERE A.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11

(3 row(s) affected)
```

```
-- OUTER EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.PK = B.PK
WHERE A.PK IS NULL
OR B.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11
   5 ARIZONA    NULL       NULL
   4 LINCOLN    NULL       NULL
  10 LUCENT     NULL       NULL

(6 row(s) affected)
```

注：原文连接：https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins

- 标签：
- [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#SQL](https://mrxn.net/tag/SQL)
- [#MySQL](https://mrxn.net/tag/MySQL)
- [#数据库](https://mrxn.net/tag/%E6%95%B0%E6%8D%AE%E5%BA%93)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
