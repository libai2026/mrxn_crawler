---
title: "金和OA CallSystemReadOver.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html
asset_dir: assets/金和oa-callsystemreadover.aspx-sql注入漏洞
---

# 金和OA CallSystemReadOver.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/12 14:26
- 709浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

SQL

数据库

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CallSystemReadOver.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 CallSystemReadOver.aspx 的源码，在 bin 目录下查找 JHBase.Web.Menu.dll 将其进行反编译后找到 CallSystemReadOver 的处理逻辑

```
public class CallSystemReadOver : JHSoft.Base.Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    Message.ClearNoSee(this.Request["ID"].ToString());
  }
```

跟进 `ClearNoSee` 方法

```
public static bool ClearNoSee(string MessageID)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  string QueryString = $"update callnosee set DelFlag ='1' where callID='{MessageID}'";
  dbOperator.ExecSQLReInt(QueryString);
  return !dbOperator.IsError;
}
```

深入探索

恶意软件分析工具

技术文章订阅

授权

参数 `MessageID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/JHBase.Web.Menu/CallSystemReadOver.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

MessageID='SQLI_POC
```

[![金和OA CallSystemReadOver.aspx SQL注入漏洞](images/img-001-24b4cf53e178.webp)](https://image.mrxn.net/25c28f57ffe044ccaa3e7849973ccbb8.webp)

成功延时 5 秒

代码安全审计

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALa0lEQVR4AezbgVbkOK8EYL59/3f+L2pNJY7jNAwzDH3ODQdtSaWSbKy46WZ3/3t7e/vfV+1/v75S/ytcwjPNs9yy2QU595njsSy5GZ9pxlz5Y23FZSP3Fb8G8l53f7/KCWwDeZ/u22dt3nzq8MbaVpr0SS4x6x4859OH1qVfkOax/azJBdk14WakNVmvcNYU91kba7eBjOTt/9wJnAZCT58z/sk26X7jU0Nz6UvHoyZ+NHMcvpCuL/8jo7Xpt8KPenwmT6/DGVf1p4GsRDf3707grwyEnv74lOVHCJeY1iLU9nsnWjy4TfDuzLnE76nte8VVku6XfGHxZXSu/Csrfdmcp2sxp74c/5WBfHn1u/B0An9lIPX0lOHxZHP9Lua0g3eiasve3cM3ez/aj4BjXDxnrvjqXUbnOe+PzpU+VjVliTlrkvtb+FcG8rc2c/d5e/uegdwn++UTOA2kruiVfWUVPF7G0nPsEY7WJBd+xOSCY272Z03iEek1Uzvm4tMaGqNdYWpmXGnDzdqKTwMp8rafO4FtIPRTwMc4b5euyeQLOXIc42ea9KdrOP8SXmnCzUj3qTVjs+ZZnBq6T7R0jFAb4vHKwMe4Fb0720De/fv7BU7gv0z/K5j9p5b9aUjuuzFrF16tVbmyq3zxlS8r/0+sevyJ3TfkT07/G2pPA6Gf8qxFx5xx1oxPRnLPMPpZQ68182NMazhjdHQu8Yjz2rSWHaOnubkmcSGtSc0KWWtoHvfnkLcX+/qPns7v7KueiLLUlF9G90JS2zuNypdh4yKiucpfWbTB6BKPmFyQ7j9qOHLRjjjqP/JTFx3H/uELOeZSW3h6yaqCF7X/F9u6B/JiY94GQl+jujZlq30WX0ZraYy2cle20tD1qYmG5hMXcuQ4xqWZjY81c80qnve30lxx9B5wkmB7+ab9bSAn9U38yAlsA8lTQE9qtRs6F22Q5lc14Thr5nqOGjpG2mz/tUhqt8S7Ew6PJy9x8F1y+qa1p8RvEny+T/azwm0gv7n+Lf+mE9j+dDL353ridI7GuXaM+Vgz6q/8PE10PxpX+s9oo0k93Y8d51ziFaYfXf9Mkxxn7X1DcjovgqeBZNJfwdXPlD7J0U8FOyYXnGvCF865xIV0z9KNVrmykaO1xV9Z9MknfobRrpBek8b0oWPcfzp5e7Gv0w15sf19/3ZebIVtIPS1mfdH89hSeLytpDEJOkaoTZcrvCUGJ7ngkDq5ePSMlo45/1vFaNKEXRvuM0jXzVqaZ8dnmnk/s7bibSAV3PbzJ3D511566plqYbZb/mjhnyHdb6WhcxxxpQ1HaxOPyDHHMS5t9s8xR8co2cOutI/kr3/MGhxucuV/SZ9+uL1vSE7pRXAbSE2wbN4XPWk+xqqPpU/iFUZzhWMNvX60ySVeIV3zO9pVn5nj2Lf6c+RSQ/PsOOeqPrYNJKIbf/YEtoGwT5DzO5Zxm5lmuDkOX0j3Lb+MjrleI/04a5OrXlcWTZDuk7iQ5tKjuLLEK6z8aKMmfLjEK+S4Nh3j/mD49mJf2x8XM8nsj55a+MI5N8d0DTtGs0JaN+c485y5uW6Oua6pn6csNbS2uNnoHEdM7Qpp7SqX/qvc9pK1St7cl0/gy4X3QL58dN9TuA2E4xXLtaJ59l/CyQWztcSF4YJ0n8rFkrvC6Ea80o4857WqxzPNmIvPx31mbeIg3QOhnuI2kKeqO/nPTmD700k9QWXPVsbjzwEcMTXsfLjqWZZ4xOLLwpVflphzP3YOkT4Qj/09gvd/cIzfqe271ikLUX4ZXYOkHj2xYenK2LmIaS7xZ7B6xe4b8pkT+4ea7W0vPdlMio7HvSQ346i58lNzlS+eXjPaEelc6crG3OxXviw8x9rKzca1Jn2Cc23Fyc1YuY+MXhv3B8O3F/u6fMnKpFf7pSc651Iz4qyha7Glog+Bx+t14sJZU1wZrUWFB8OpTwSsc1mn8CNt8iOy7jtqnvmXA3lWdOe+7wTugXzf2X6p8zaQuqJl7FfuqmPpyq7yI8+xX9XFomOtSf4ZplfhrCtuNHod9g+5qYkuceGKK57uU/5sVzWzruJoR9wGUoLbfv4Etg+G2UqmlXhE+sngiKPmyqdrxjxHLmvTPGdMPecczUUTpPn0L6Q5GqMdkWOOjqu+bKWlNTSuNCM3+/cNmU/kh+PTB8Psh/OE66kYLdpnOOrLp/uyv44XX0bnyi8b+1b8WRvrRp/uj41OT5zeIicX8VUcvjDaYHGxcEF6TXa8b0hO50Xw9Dsk+1pNlX2SXD/hSJsN8XgC07eQ5mgsrixF5cfC0VrOGM1ck3jEaJ8hvUY0dMw1Rpu12LXholnhfUNWp/KD3PY7ZN4DPdmZrziTpjU0hi+kORqrroyOUeHB8LhFIemYHav3aNEWsuvY/cpdGa27yhef9cofLXzhyI9+5WIjP/rJF943ZDyZF/B/YCAv8FO/8BZOv9TpK1zX58pYa2gepx85vU6JgYgGh5euQfIll+t+WTNIa7Gthcd+ognSPDZtHDxqEn8W7xvy2ZP6R7rfGgg99dUTgj/eMh5PVfqvkNasFlvpR25Vw7HfqJ/91HOsCV94VVO5GMd6Osb9bwzfXuxruyHzZOmpjfuNhs4lDq60I/eRv+oz18yaxIX0vuaaVVz60ehadlzVjdxYH56un2OE2v6HnY0YnG0gA3e7P3gC2wdDPF6/P7OXPBnPtBz7cYyrNn2CtIbG0szGMUfH7H/KYedY+3Pf7GFE1rXRsOfTL7k5Lj5csLjZ7huS03kRvAfyIoPINj78YMj5WtJcmtDxeP2SG7nZj2bG6Oi+7HilrZrkyl9Z8oXsPVn7pSubexVXNvIVj0b3HLnZpzXseN+Q+ZR+ON5+qWcfmfocF09PsvyyWUPn2X/BRrNCdj17Dc2PNbXeaMnRWoR6vDnhHK/qR+7Kx6PntsAvh+bZ9/4r9fStbTQrvG/I6lR+kNsGkqdj3gvnp4CdY/fTo5CdZ+2Xrixr0rriZps1nLU0N2sTr5CuoXGlyV6S46ylORpnLUI9bht7vCXenW0g7/79/QInsA0E2+TY/dUe5ycmGva6aILRJC4MNyN7H45+1ZWlhj1ffFlyweLKEhdWvDL2fhz9qitLXflXRteu8qkPjpptICN5+z93AtvnkEwr+GxLrKef2kKOmuLKaB6nJSpflkT5sXB43OTEI3KdKx2dZ8fi/5XR6z5b774hz07nB3L3QJ4e+r9Pnj4YZgt5qRjxKhd+xNSFo69r+MLkZqxcGV3D9Qev0s2WfuHpPuEL5xytCV9YurLyy8q/ssqvbNQnH45eM3HhfUPqFF7Itl/q9LT4PObnyOQ5186axCuk638nR9dgVfYhl70H8XjTwH4rae7DZu8CrrV0jsas+V62fd83ZDuK13C2gWRan8F56/TERz596BxnjD7axLQ2ceGsKa4sfGHFnzV6DY5YfWJ0bu7Jmi9dasufLbkg5z7bQObiO/6ZEzgNhJ4aZ/ydLdL1eRpSm7iQ1sy5OS5tuCBdyxlnTeLqM9ucY+83567i4tnr2P3KxWg+cXDc02kgEd34MydwD+Rnzv1y1b8ykPHKxc+K9DUNT8eI5BKxvQWl/YjTb8Q5l/gzSPcf+8Wnc5/pk5qVNrnkEtP9cf+npG8v9vVXbgj7hGk/P+f8FIQvnHN0bfgVVt2VRZ/8HIcvpNcqfzSax0bPffC4uZvgNx2u6//KQH5zP7f8yQmcBpKnYYVXfZ5puX4auM7VWnQeFS4Nj6cVpzweuexvFMzcHI/a+HS/xM8w/Uak68NxjIs/DeTZInfu+09gGwg9LT7Gq22x115p6imIRTPHdJ/whTSXmmfIWkvzeFZ+mat9XNlchMftZMfUPtNuA5lFd/wzJ3AP5GfO/XLV/wMAAP//iwzy2gAAAAZJREFUAwBEFJazzEhgAgAAAABJRU5ErkJggg==)

手机扫码阅读
