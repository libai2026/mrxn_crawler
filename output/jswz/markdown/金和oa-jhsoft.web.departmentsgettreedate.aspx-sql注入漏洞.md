---
title: "金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html
asset_dir: assets/金和oa-jhsoft.web.departmentsgettreedate.aspx-sql注入漏洞
---

# 金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/8 13:31
- 204浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

恶意软件分析工具

传输层安全性协议

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetTreeDate.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GetTreeDate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Departments.dll` 将其进行反编译后找到 **GetTreeDate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Session["UserCode"] != null)
    this.strUser = this.Session["UserCode"].ToString();
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
  else
    this.loadDate();
}
```

跟进`loadDeptChild`方法

```
public void loadDeptChild(string deptID)
{
  DataTable firstSubDeptByDeptId = new Role().GetFirstSubDeptByDeptID(deptID);
```

继续跟进`GetFirstSubDeptByDeptID`方法

```
public DataTable GetFirstSubDeptByDeptID(string deptID)
{
  DataTable firstSubDeptByDeptId = (DataTable) null;
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select  a.DeptID, a.DeptName,case when exists(select * from dbo.department where deptparentid=a.deptid and deptdelflag=0) then 1 else 0 end as haschild ");
  stringBuilder.Append("   from dbo.Department  a left outer join dbo.Sort b on a.DeptID =b.SortObjectID  ");
  stringBuilder.Append($" where  a.deptparentid={deptID} and b.SortType = 'Dept' and a.DeptDelFlag = 0");
  stringBuilder.Append(" order by sortid ");
  try
  {
    firstSubDeptByDeptId = this.ObjDAL.ExecSQLReDataTable(stringBuilder.ToString());
```

参数`id`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.Departments/GetTreeDate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞](images/img-001-4265fe0aa136.webp)](https://image.mrxn.net/f05b183a8b4d4dbb9340d398fd5b586b.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALf0lEQVR4Aeyc7XbcyA1E5+77v7NiTJ1LsUH2kJIdjX60z8LF+gDYJjiRpWTz3+Px+PhOfUx+9VmT2Cab34R20X35GdqqN+Nd73l9UV9UF7su/w7WQv70rX9+yxPYFvJn2487dXVwZ5gDHoD0eQ2ffDPaBfDMOg9Gbly/EJLR+ypC+mFE59Q9quDcNydW9k6ZL9wWUmTV+5/AYSEwbh/Cv3pU34y7fZD7QNB+CO9z9Lt+xs3COEu998x0SP/M73PkkD4YUX+Ph4XszXX980/gny0Esn3/CBDu2wSvuX09P9Mh8/QL7a3rfcExWz5E730QvTJ3qvff6Zll/tlCZjdY+teewF8vBPI2+ZbAa+7xrvKznLoIuR98ot4MIdl+BvPq8hnezc36z/S/XsjZ0KV9/wkcFuLWO85uYU7/yT8+nt9DANv3Nvoi5C3t3H71GZo7Q3sg9zjLlAbxzXeszFnB6767c3qu+GEhJa563xPYFgLZOrzGflRIXh3CfbMgfOar9/yMmxch8wGlDfsMDeD5CdZXl0N8dRi5ugjnPkSH1+icwm0hRVa9/wn851vxVexHh7wFXZfD6EO49zV3xc2J5gvVRDi/h75YvVVwni+vCuLbJ5ZX1XlpX631CfEp/hI8LATyFkCwnxOiQ1DfN0EO8dVFfTkkpy5CdAiqixAdjmhGhGTkInxN98wijP0QDsGr++jv8bCQvbmuf/4J/AfjNt2+CPEhqO5R5TD66ubEmQ7pNyeah/hy0dwZXmVmvjrknjCi9zInn2HPQead5dcn5OypvFHbFgLZGozYzwbx3Tqc81kfJA9BczfmPaOQPgjad4bPht1vkJ6d9LyE6M6A8Kf55zd1EeLDiPp/Wp7/wOg/xT+/9dwfaftnW8imrIu3PoFtIX1rM951Tw95G/QhXF99hpC8PoxcvSMkB3irDYHnd+QK9sohftf1Z7r+FfZ+yP1gjttCroYv/2eewGEhbhWyRY8B4RBUn6Fz9CF9EOy6eYjfOUSHEc0V9pnyjpWt6rq8vCrIvdTF8qrkM4T0V7Zqltvrh4XszXX9809gWwhkm1dHqE1XQfJ1vS+I3ueY6fqMQ+bY13HWV7rZuq7qHMbZEF7Zs4LRh3DnivZ2Dsnrv8JtIa9Cy/u5J3D4ae/s1m4dsu3O7VOXQ/IQVL9C58DrPogPR+wzIJmudw7J9TNCdPMzH8ac+Tu4PiH9qb6ZbwuBbNXzuE05xFeHcz7Lq/d+dci8Kw7JOWeP9t7FZ+/Hxxaf8a5DzgAj9pyDIbkrDjy2hTzWr1/xBLaFuF0Yt9lPCfHNz3x1SL7zWb858W6u8mZFGO9dmSqIDsHS7pRzRXtmHM7nz/Klbwtx+ML3PoHtvw+BbLO2VDU7VnlVkDwES9uX/XutrtXvIozz7YPo8j1CvLrfnbIXxj71jjDmILznvHfXO4f0A+tryOOX/Tr8RxZkW56zbxniq4vmZwjp6/6s/64OmQtso+0Fhp/2GoBzXV+E5CCo7vzOITkY0RxEn/HSDwspcdX7nsDhO3W3D+M21UWID0H/CBDec3JzIoz5rs+4+h4hsyCoByP3LBAdgl23X4Tk5DN0jn7n6me4PiFnT+WN2uFvWTC+BXDOv7L1/Z9v1gfjfe7m9rO9trejvnjlz3IwnrXnHo/HU3L+k9z8bX1Cbj6on4ptC3GbogeQQ94K+cxXh+RnXP1qnv4ddCbcuzckB0H7vZccXvs9B2Nev8+V73FbiE0L3/sEtr9lQbYKQY8F5xyiQ3C/5bq2f4aQPghWT1XPQ3x1CIcjmulYc6sgPfqlVclFSK68femLkBwE1UWIDiPqn+H6hJw9lTdqh4Xs34i69mx1fVb6V2ivObkIeYu+6zun0BmQmRAsrwrCzZVWJe8IycOI1VNlvq7PSl+EzOkcWD/LevyyX9v3IW726nwwbrfnIX6fB9Gv8jDmYOSzfqBb278B7FmA58+25IeGJkDyyt/tm/VD5ju38PAfWTYvfM8TWAt5z3Of3nX7a+9Z4kyrj1VV92D8+OlXtkoOycnLq5KLcC9XvZa9Iowz1EWIDyPO5tknQvrk4qwfxvxZbn1CfIq/BLcv6p4Hxi12HeJDUP+7CJkDQd8acTYXkocjznpmM9VF+zuH3OvKh+QgaP4Ork/Inaf0g5nDQnwrINuVeyZ5R31IHwTVzctFdRHGPnMdze/1rskhMyFoj768IyTfc533vu7LO0LmwyceFtKHL/6zT+CwEMi23GY/DsSHoH7PyyE5CJqHc26fORGSn/mVg/OMPSIkB8HqPSvzenJ43Qfx7+bNFR4W4s0XvucJ3F5IbW9fHhfyNkDQDIzcvL4IYw7CIWifCNEh6JzCWabrla3qOmQmjGhOrN6qzkurUu8I49zKVsGnfnshffji/58n8OXv1CHb9Di14X1BfDVzn3h+BenTtb+j/nfQWbPeK98+yFnhHM11dL4I6d/n1idk/zR+wfW2EDhua38+iO92RTMQv3MYdf0rhNd93h+Sg/n/4Wa/F6THGfoQXd4RXvuzeeow9qvvcVtIv/ni73kCh59leQw43yaMuvkZun19GPu7b04d7uWrD5K1VyyvCka/tDsF6TPr3I7dl8PYr36G6xNy9lTeqG1/y3Lb/SwwbtccnOv6fc5MN6cvdh3G+3XfvkIYsxBeXpW9Hct7VT0PmXulO9McjH0QDqz/kcPjl/06fA1xm2I/L2Sb+hAOwZ7v3D51GPsgHEY03xE+c3r9Hp2bg/TqQzgEZzn13td1fXWx6/LC9TXEp/RLcPsa4nkgbwcE1cXaYpVcLK0K0lfXVfoixIdgZapg5OY7QnLq1VtVpSZCshDsevVUqYulVUH66rpKH6JDsLyq7ndemSpIHwTNFa5PSD2FX1TbQuC4rTpnbbSqrqsgOQiWV1XeviD+XttfV0/VXqtrSF95Z1WZKkgOjlh+lf11XQXJ1vWrguTsh/BZD5z7EP3unJq/LaTIqvc/gcNC3KboEWHcdvfNdR3Sd+XbJ5qHsV/9DL/aC5kNwbOZpTkXkpOXVyWH+KXtC6Kb6wjxgfV9yOOX/Tp8Qq7OB9mmOXjNfRsgOQjary+H+BBU72jfHmHs0bO3867PfHMdZ/muyyHngxH1C7+8kH6oxf/tEzgsBMbtebva3r7URUifma7L9SF5GNFcR0iu63veZ+vNdH3IbAjO8ur2dbzyzZsT1QsPCylx1fuewOFnWR7lbHvlQd6iut5Xz8vFfbaur3T9jtVbBTkHHLH8Khi90r5SHx8fz3/pxx44nwejDuG9T/4K1yfk1dN5g7f9LGv2JvYzmeu6HMa3Q90+iA9BddE8xIegumj+DM1cob3m5JB7QlBf7Lmu64v6IoxzIRxY34c8ftmv7WsIfG4Jrq/7nwPSow7hMKK+bw+MPoSbE+G1Dhidovfsga7LReD5L4te9enDeV7/1dz1NcSn9EtwW4hbu8J+7p7Xn+n6HXte3nOdmyvsXufw+s2F+DBin3PF6yxVV7kzf1vImbm0n38Ch4XA+HZA+NXR4F7OOZB8vUlVED7z1UVIHo5opubuS12E9Mr32bqe6TD2mYPoMKL+HTws5E7Tyvz/nsBfLwTyNnjEerOqYNS7L4fkqqdKva6rZlx9j5Wv2mt1DeM9KlNVXhXEh2Bp+4LoEKzeKhj5vqeuK1NV11V1XVXX+yrN+uuF7Aev679/Av9sIW7YI8nh/C3SFyE5+2Hk6ubl30HI7D5LDq/9fk9IXr3PUb+D/2whd262MtdP4LAQt9txNsqcPuRtgaA+hEOw53tOX4T0QdD8Hs2qdQ5jL4Sbg/Dery/CmLvKdx/GfucWHhZS4qr3PYFtIZCtwWucHRXSN3sb7NOHMQ8jn+XUnQfpgyP2zIw7U4Rx1qyv6/ard4TMVYdw+MRtIYYWvvcJrIW89/kf7v4/AAAA//+vtHcUAAAABklEQVQDAHwW/tH0y4X5AAAAAElFTkSuQmCC)

手机扫码阅读
