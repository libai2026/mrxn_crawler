---
title: "金和OA LoginModeAdvanced.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html
asset_dir: assets/金和oa-loginmodeadvanced.aspx-sql注入漏洞
---

# 金和OA LoginModeAdvanced.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/16 08:28
- 579浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

服务器

软件

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LoginModeAdvanced.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LoginModeAdvanced.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 `LoginModeAdvanced` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.PageInit();

  if (this.Request.QueryString["ID"] != null)
  {
    this.strLoginID = this.Request.QueryString["ID"].ToString();
    this.GetLoginInfoByID(this.strLoginID);
  }
```

深入探索

数据库

漏洞修复方案

编码转换工具

当 `ID` 参数存在且**不等于 null** 时，执行 `this.GetLoginInfoByID();`

```
private void GetLoginInfoByID(string loginID)
{
  DataTable wfLoginById = new WFLogin().GetWFLoginByID(loginID);
```

继续跟进`GetWFLoginByID`方法

```
public DataTable GetWFLoginByID(string loginID)
{
  return this.dbOperator.ExecSQLReDataTable("select * From WFLogin where ID = " + loginID);
}
```

至此，就非常明了了，参数 `ID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/LoginModeAdvanced.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LoginModeAdvanced.aspx SQL注入漏洞](images/img-001-78ae52f28191.webp)](https://image.mrxn.net/b2c9d3cddd6d49fb894bebc4a63e6558.webp)

成功延时 5 秒

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALR0lEQVR4AeyagXbbuq5Es+////N5GSOboiBKcXqSOvddZWU6xGAA0YRUO2n/8/b29s+f4p+LL3t2i3r4LNf1xPEHWQdZB1n/G6THZzjrP9fpmbU/WWcg73X39285gTGQ9wm/PYu+eeAN6PIynq/RDebUgUdfQOnAwMEDmwbb+lD8LnhN+V0a32pQPUxAxebD5uRoz8Ka8BhIghuvP4HDQKCmD0c+2653wlk+Ohz7wbVm33B6BFA1WXdA5eJfofsTQ9VAcbTvBFRfOPLqOoeBrEy39vdO4McG4h0KdWdcvSS9naFqgcP721U/qLrugdJhYz392onNnTEc+5x5n9V/bCDPbuD27U/gWwcC2x0Dtc6d9hmgvPutvf+A9M8/48mA8kBx965i2HtX+7AO9t7oUJp1UHFyP4VvHchPbfJ/qe/PDOR/6QS/+bUeBuLjueKza0M9ynNN90J5Zh1Ks84clA4bd4/xiu1jznhmqN5qeqF0wNT4wVPPioe5LVZetWZ9hIeBPNT7j5edwBgIMO4EuF7/1G6hrnt1B/VrQ9UAPTVi4PHahjAtvBaUxzisLesAyqMOFQNKg4HHNeFzHkXvizGQ9/X9/QtO4D+Z/J+i7x+2u8Geeozhc0+vSa1a5+REz30lfqaHHqjXYBz2Wln/G9xPiCf5S/jTgUDdDXDOqzsCyu/rhH0cHY7alZ6cgKqFI3eP+4PNq0eGyhnPDJWDYvvNHtdQHihWXzEcPZ8OZNXo1n7uBP4DNSVYs3fDivu2YOvRc9Z3fRXrhWM/c6u6rumF6mMc1guVM15x/DOgamDjVV3XoPxdn+P/pidk3vf/2/U9kF822k8HAvWYAWPrwOOHniFcLKC8UDw/+q6hchdtHteD8sH27yNzjf1mLWt1uK6Pd0avM6c+sznZnPHMUPuYNdefDkTjzX/nBMZAnGjneRtQk9VjDva6+bCerAMoL2DqS5wegUVZCzUZ2D1Z+sJQuawDa2aGvQcqnj19nV4BHL3RZ/TaxGMgCW68/gTGQKAmCnueJ+oaymPsy4DSYeOeM36G7T8zbL2ByzZzXdbAeGISB5cNPpJQdR/hkqA8ULw0nYhQNcDbGMjb/fUrTuAwkNw1M+ZdQk3S/Jzr6+7pcfcnhuoP53zVB6pOD1Sc3oF6GCoHxcl3xBeoZx1A1cDG0QO9X+HUicNAvtLo9n7/CdwD+f4z/VcdD/8eAttjCOya+1gB480RGB7zYeDhGcmPRXLiQxr/1edK19sZ6jpAT42+JoDHngClAwPDA7U+29dcDOWdtayhdNg4+hnuJ+TsZF6kHwbS74Z5X1BT7p4ezzVXOah++qFia6BiQMtgPSsGDnc5bL9uWdXYeM6pQfUzlldecyvW33NQ/YH7Y+/bL/sa/x7yzL6cMNREjVe1V7mVf9Zg3z+9zEPljFccf2Au6wCqFjA1OPlgCBcL4PEEzpbUzjA3a7Cvm3OuD39l2ejm15zA+JT1zOWhJuw0oWIovuoB5YGNex/jqz5XOdh6A1fWkQN2dztUDNt7zjC3BWxeU1Ca8RXD0Xs/IVcn9oLc6XuIdyvUFGG7Y6A096vX+FmG6tPre5x+ajJULWwc3wy9asZhqDpzcnICrj3WrNgeqxys+8Z7PyE5he/HH3e8B/LHR/czhYc3dTh/nKByZ48jVB4YuwV2b5rWhofpYwHlheIPeUdQudQHczJxoAblNZ45vmDWsoaqARI+EF8APF4LFEcTUNqj4P0P2Mfv0vhVjjUylBe4fzB8+2Vf400dakpO7WqfUF49sI+jw16zL5QO24eE+AM9WQeweaHW0QPYxyut94tHwL4eKrYmrFeONgOqBtByYGA8VYfkhzD3vN9DPg7lt9CXBjJPcl5/5cWs6mC7i4BlO+tMGq9YT2dg3K29Ti8cPeZkKI9xuPczTk5A1cGezYe/NJAU3PjZExgDWU307NJQEz7LR/9Kv/iDP6mB2guQFjsAjydiJ34EsM957Zk/rI8egOElAw//pekiOQZy4blTf/EE7oH8xcN+5lJjIFCPGhSn+Aw+1j2vHobqk3XQvasYzmugcr0uvcVZDta18UPloDhax1n/7kt85TXXOXViDETh5teewOFXJ05vtS2ouwj2vPKeabDV6jm7pvrM1sDWB/br7pnrz9bWXDHUdewxe6FysOeVRw3Kaxy+n5Ccwi/C+NWJU4eaGhSrh9131oGxDFUD269FYNMArTsGHh8V0zMwCaUDSoPj6zB5pgOP6wBaT2P43DOaLBZ9D4m1AY/rGs98PyHzafyC9eE95GpPmXIA+wlH6+h9ej4x7Pv0mlWcugDOa6FyUGyf1AlY5/SGYe+JFthj5uiBGlQtbJx8oEeOJu4nxJP4JXwYSJ8abBOGWuuRoXQ4sh5fL2weNT2w5WB7H0perxwtgK0m8QrWzKxPDaqP8cx6ZSgvbNxzxqs+alD1xuHDQCLeeN0JvGAgr3ux/w1XHh973SwcHyNzPoZw7uleY9keYTXY90sugNIBrYOB04+OUDnY8yh+X0Dlcp0zvNse31BeKH6IJ3/YC45eOGq9zf2E9BN5cTw+9sJ+ek56ZveqBuc1sM/BPk4v+8jRPgPs+1gbhsplPcOeUHnYPjD0nHHYHlkHZ3F0qN7xzUiuY85nDVUL3P/r5O2XfX3pryzYJgnbXeYdML+2rhnD1mP2Z909xuHkV4DzflA569JHQOWgWF3vFX/FC9UfNu697Rf+0kB6ozv+/hMYn7IynRleCrbJzvmsVx7Y/ICWwakTQ2yLVR7YfarSs2LbmTOG6gHb091zxmEof9YrQOVh6wel9WunfqVFn3E/IfNp/IL1PZBfMIR5C2MgUI/anOxrKA8U97yP5Mx6oGpg454zXrE9zcHWB3gLznLWzqz3GbYu1wisUQ93zXjm1AZqqQuiiTEQTTe/9gROB+LEVtvLVAM9WQfG4VVdtPhE4qDHqT9D/IE1M1sza1mrp06oJT/D/Ir1WfsMWxO2Z69LTpwOxOKb/+4JjF+dOCEv3+Poak44WmBsPqwmx/dVpI+wtsfq4Z7z2urG4fiDrM+QfGA+6xn2XbE+a8Nq+o1nvp+Q+TR+wXoMJBNcYbVHJyyvPGrPePRece/jXlc1PWdsj7B1WQc9XmndY9+wOTn1gXE4cZD1jNSLMZDZcK9fdwKf/upktTWnucqdabkzgjlvn86zx/WZp+uJrcn1AuOZowfxB1kHs6ev4wu6njj6CskJ88Yrvp+Q1am8ULsHcnn4fz85Pvb2S+fx7dCjbiz7SIa71uN4ep8eW7NivSvufj25Zkf3znGv6/HKq0eePa7dg7He8P2EeCq/hMebulP7CvfXkAl36LGvcbhrPY5H2NdYtias1jm5wB4zn3njF3qMrVefWc+subaus/nw/YTkFH4RxkD61K7is/17d8zcvau+eswZz31cm5OtCavJvcY4rCd1gfGKk5+x8qjpM36Gsx8xBvJM4e35+RM4DMRJrfjfbOdP7hxrwv3aq/2p6U1d0ONoejsnJ6zTcxZH19M5OWHOWPZ64cNANN38mhO4B/Kacz+96rcMJI/aGU6vvEj4SNtrtqjJ5oxnNtf7GYdn/7y29hm+qjO36pPrB6vctwxk1fjW/uwEfmwguQOCvq1ooue8q8xfca9dxfZb5XpvPbOu1vv0WN+zfFX/YwN5dnO3b38Ch4E4vRXvS6+jXr9yezfq7fFco0fN2JqZ9cxa1tas2JqZ9aX2M+iV9RuH595n68NAzoy3/ndOYAzEiT7DZ1uba/XMWta5U0T3nMXqM6dXMGuu7S+rz5zaQC3rwDicOMg6sN+Kk/8M1nVfriHGQLrpjl9zAvdAXnPup1f9PwAAAP//nL+0twAAAAZJREFUAwC8tXiwDtTmxQAAAABJRU5ErkJggg==)

手机扫码阅读
