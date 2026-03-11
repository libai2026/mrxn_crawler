---
title: "金和OA GetSubjectTreeData.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html
asset_dir: assets/金和oa-getsubjecttreedata.aspx-sql注入漏洞
---

# 金和OA GetSubjectTreeData.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/30 13:05
- 223浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

安全研究报告

文本剥离工具

服务器安全服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetSubjectTreeData.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GetSubjectTreeData.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **GetSubjectTreeData** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
```

跟进`loadDeptChild`方法

深入探索

软件

漏洞修复方案

防火墙软件

```
public void loadDeptChild(string deptID)
{
  DataTable table = this.biz.GetList($" ParentID='{deptID}' and  DelFlag=0 ").Tables[0];
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/GetSubjectTreeData.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GetSubjectTreeData.aspx SQL注入漏洞](images/img-001-e0e256d0d20d.webp)](https://image.mrxn.net/420886cd1dcd44a9be8a1ac45de4fa7b.webp)

成功延时 4 秒

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALrUlEQVR4AeycgXIbOQxD/fr//3xnLAdaipLWTurGvqsyYUCCIKWIqyT2dPrrdrv98137p3zkPk5lTr55oeIrk8Zm3So2f4XukdH6zFXfmopZ51zmvuNrIPe6/fkpJ9AGcp/w7VmrmwduQFcPI6f+uVZxtpyrvnXQ94WIYcRVD/cSXmlqzjHEWqq3OWc0/wy6RtgGomDb+09gGAjE9GHE39kujP2g5/w0eR048+aqxryw5uCsByRpBhy3GgJdCxEDTfs7DtCtA2c86zsMZCba3M+dwEsHAuP0ITh/S34ShZVzbJTGBtEHerRWCJGTPzOIPNDS7t+IiQMcT3lNQfBATX07fulAvr2LXdhO4KUD8dOWsa104QDdE+j6XDLjcn7mu+YKXQf9HsS7Tr4MRo34V9pLB/LKjf2tvf7MQP7W03zB9z0MxNd0hl9ZD+J61z65R81B1EBg1la/1ua4amHsB8FBYK1RDJHLvVe+9DNb6cXP9MNAZqLN/dwJtIFAPA3wGL+zPYi+uRZGTnk9PTKIPCB6asDxBwEwzT8itY7MOvk2c0bgWKvGgKmGwKGFx9iK7k4byN3fnx9wAr/8NHwHvX/XOhaag3hCxMkgYkDhYcDxNLnmIMsXCE2huzc0a86x+0L0AJw61oXzjVGgcRZBcKvYvNBrfRf3DdEpfpANA4H+ach7hcjBHGdaPyk5Z7/mIPo6f4UQWhjxqs45r22E6ONYuNIqVw2i3jUQMTxG1wiHgYjc9r4T+AX9BK+2Up+KqoWzl7VVY17onPxsM97cFeYe8iH2M6uByEGg9DKIGJiVHRxw/J45gsUX9VrZouSg/0s35Njw//3LHsiHTbgNpF4v7xPiesKIrrF2hhB11kLEMOKs3pzrV7H5jK6BWCvnvuJDX1/7Ast2wPHjDRg0sz5tIIN6E285gTYQ4JikdwF9bF5YJytOZl6o+JFJlw36NSFioLWyHuj22wTJgdC4JqNl5mos3twKpam20mbeNeYcC9tAnNz43hNob514GxBPlWNNzWYOQrPiIfIwviXhHl9FOHvC2Tf3gdCY8/4geDjROWshco4zVq1zEDUwojUZIXSZkw/BA7d9Q26f9bEciJ8KOKfnrdecY+eF5iDqxcnMC6HPKS+DOa+c6mTyq4mXQV8vrhqEBgKdrz0VQ2jkyyBi1wjFy+TLYNSIl0HkpK+2HEgV7vhnTmAP5GfO+elV2kB0lWSuhPFaKS+DyMmXuUa+bcYpZ16oWAbzftLYpJM5hqhxPEPoNRAxzP8oUA8YNVpXpnw2GLXOSy+DUwPhWzPDNpBZcnM/fwLt3d7V0pqyDWLCNV7VPsvXfo5n9RB7uMrVeljXVK1jIazrtL40NggtBCovc16oWCZfBr1WuX1DdAofZG0gENPS5LJB8HD+3IXgrIOI4UR/jxCc44ywzknn/kIIrXyZ8jL51cTLVrxyEP3ky6CPxa3MfXPenNE5iL5wnp9z1mZsA7Fo43tPoA3EU4JzosB0d9Y6WWPzwquc8jMDjjcO4UTrIDjHGaHPQcQQ6L1kdL05xxkh6s1BH4uHnoOI3VcIwUGg6mQQMbDfOrl92Ed7cxFiSt6fJlrNOei1EHHWQ3CumaH1Nbfis84aiHWAnD58a47g/gV4ePPg1LjeeG9xfNb4IMuXK81Vrv3IKv12+Hsn8O3qPZBvH92fKWwDqdcIzqsLvW8tBO+tQcSAqYbA8eOiEXcHRu5Ot0+vk7ElLxyIvhDo+lkJhOYqB2vNrC5zELVAppd+G8hSsRM/egLtrRNgeIJXO4G51k+i0LXQayFiWL9QqrVw1tSc4xlqH7JnctJVq3Vw7gN631qY887PMK+7b8jshN7ItT9785Syn/eW+exnzcrPevsQT5NrIGIItC6jtZmrvjUQfSDQ/AzhscbrzOqdqzjTVg5ibWC/MLx92MfydwjE1Gb7hXkOgofx98Osj58m52ps/grhXLPqrvpB1NUaCB6oqadi4OnfxbOG+3fI7FTeyO2BvPHwZ0sPA4Hzys0KxF39KFA+W9VC9AeaDDiuOQS2RHJgnnN/YZJ3rnIrs9B5x0JzRnGyGouzXeWsMUJ8T64RDgOxeON7TqANRNPJNtsOxEShx5m2chA1mYfg8rrys8a+eJljiFoYsWpqDGeNesqsyQihMwcRQ6B5IQQHPSpn0zoyxzNsA5klN/fzJ9BeGNalNUlZ5RWLzyZuZRBPTNZXH0IDge4FEcOJrrXGsdCcUZwMol6+zRqIHASaF1btKhYvfTZx1aBfw3kIHtgvDG8f9tF+ZEFMyfuDPhY/myicLwKdF0JfDxHDiOotU51Mvky+TbEMot48RAwofVjNHeT9C9D+mruHDz8h9BZCxLU/nGdQtRA1gFOXe2gDaertvPUE2lsndRd+Ciqv2DkjcExdOZtzxhlvboUQfeF8At0PIpdrr3JZl33XZK76MK4ljWuFimemnM35VSx+3xCf0ofgGwbyId/5h26jDUTXRQb99RRng8hBYP2eIHgY0T1qjeKac5xRuq+a66/qIPZqbUbXZU4+RA2caK1ROpljoWKZ/JW1gawEm//ZE2gDgZi2l4c+Fq/pZoPQmJPGVjkIrfMzhNDAY7yqr2vXONfWHJxrOwfBuc68YyGExjmIWDkbBAdrbANx0cb3nsCXBgL9ZK+2DqG1xk+O4xlWjWOh9fJlNRZnc84I/V7EWwuRg0DzQumeNellEH1cBxEDprr/llA1LXF3vjSQu35//uETaG8ualIyrydf5jijeJk5YHhh6Jx0Mhg14mUQOQgUJ3OPjBAacxAxjGiNUT1tM04580KInuJlEDEESlNNOpl5+TZzRhj77Bvi0/kQ3AP5kEF4G8v3siyAuFaAqePHE4zvL/lqZgQOvYshYsDUgMBRAye6ZxWbFzonXwZRL1/mvBAiJ18GfSzOBpFTD5n5K5ROdqWZ5fYNmZ3KG7n2S73uAeKpqLxiTV4mXwahhRPFy6TLJs4Goc/57FsnhF4rTgbBAwoPA44bdgT3LxAxnHinn/70nlxQY/EQveXLoI/FVZv12TekntKb42Egnpox788cPJ4+hAZ6dI+MXgPW2qrJ9dW31nyNxZuDWLPGgKnjtsEYq0814NC7GCIGTB15OOOWuDvDQO7c/nzjCbSBAG1ycPqzvfmpgNBZY/4KIWrgRNcbXQ+nxpzRWjg15irWGuVnXOaVV3xlsF5b9bJZvXgZRH3WtIFkcvvvO4H2OkQTy3a1JYjJWm8tBA8jWuOajDVXY2nNQd/bvBAiJ39mEHk4caarnNaXQdTVvGLoc9DH0qiHTP7K9g1Zncyb+D2Qy4P/+eTyhaGuVjVvz7zjGVYNxBWGEWs9PNa4/wzdD/o+5jO63hycNZWrWueFzlVUzgbR27G1joX7hugUPsjaL3WI6cHzWL8PT1wI0ccacSuzBvoa81cIUQNcyY7cbP0jcf8yy5m7p5/+BI6XD7MC94PQQGDW7huST+MD/DYQT+8ZfGbftQ+MTwMEB4Hu61rHV2it8EpXc9CvCRHDiOotqz1msXSyWQ6it/LZsrYNJJPbf98JDAOBmCKMuNqmp53z0Nc7ByfvuorWZt6cEc4+0PvWuN4xnLqac5zRdUaIescZIXLQY9a4d+bkmxcOA5Fg2/tOYA/kfWc/XfmlA4Hzuno1XcOVWQNnHWD6+PMR6NC9LHIsrJzjZxD6deD8NwOu1xoyxxnFzyxrINYwBxHDiS8diBfa+P0TeMlAICacnxBvCSIHgeZn6HrnHAvNwbqPdLJntDDvo3rbqk/NW/cswnxt1b9kIGq07TUnMAzE05/haklrISYPNKlzjUgOcPx+sAYitgQiBky1f6jciIkDHH2dcn/HwsrVWJpq0Pet+Uex17jCYSCPmu78nz2BNhCI6cNjXG0pT36lgbO/NRBcjXM/+xDaGkPwgNs0BI4b4xphS37BUZ0MHveD0OT2MHLKQ/DA/p8cbh/20W7Ih+3rr93OvwAAAP//HQ4h7QAAAAZJREFUAwDInIGnm7hzUgAAAABJRU5ErkJggg==)

手机扫码阅读
