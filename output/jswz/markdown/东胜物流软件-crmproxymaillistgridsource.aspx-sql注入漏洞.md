---
title: "东胜物流软件 CrmProxyMailListGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListGridSource-sqli.html
asset_dir: assets/东胜物流软件-crmproxymaillistgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 CrmProxyMailListGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/19 08:40
- 210浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

服务器

sql

数据库

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 CrmProxyMailListGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `CrmProxyMailListGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.CrmProxyMailListGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 CrmProxyMailListGridSource.aspx SQL注入漏洞](images/img-001-93b261f6cec9.webp)](https://image.mrxn.net/7ec4db1f8a0b4a0cb2e54ee6b5837025.webp)

当`handle=list`时，参数`TITLE`被直接带入sql语句中，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

JSON处理工具

授权

SQL注入防护

# 漏洞复现

```
GET /PriceCarrier/CrmProxyMailListGridSource.aspx?handle=list&cur_page=1&show_page=10&TITLE=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 CrmProxyMailListGridSource.aspx SQL注入漏洞](images/img-002-bd40a038796a.webp)](https://image.mrxn.net/2432a1cda8794fe0b188e15ecc193588.webp)

成功通过报错注入在响应中回显数据库版本信息。

SQL注入检测工具

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALRElEQVR4Aeyci3LbyBFFefb//1nZ1vWBMY0ZAlJkk1ULVToX99GNERqMzWwq/zwej4/v1Ef7cYayXOz6ip/p+jPs9+oZfbH78jPfnNjz8u9gLeTfvvtf7/IEtoX8u+3HleoHBx7A1qvvLHlHGPsg3Jz9MOowcvMzhGQh6EyzEF3eEeJDUB/CIaje0fud4b5vW8hevK9f9wQOC4FsHUY8OyIkbw5Grt7fFnUR0gdB8xBuboZm9eRi1+UijPewT4T4cvvOENIHI876DguZhW7t7z2BH18I5C3wV+hvE8SHYM/1vP4KIXPgN/Ys/PaAbn/+GQjX9T7gq2fu/Xv+4wvZD7+vv/4E/thC+lsDfL6JHlEfokNQ/wxhnYe1V3Nh9D2LWJlZdb/zWc9XtT+2kK8e5M7nCRwW4tY7Jr7+9yH/8fH5aYC8iXD8ngLxet/qDub05TM0A7mHvGfVYcypm5eLMM/rd3ROx54rflhIiXe97glsC4FsHZ7j2VEh/b4Nq7w+JG8Owle+ORGSB5Q2dMYm/LoAPj/BK/9XbANIfhPaBcx9iA7PcT9uW8hevK9f9wT+8S35Knpk++Qi5K3ofudnef0VOq+wZyBnUIfn3NwKYew3V/eu6ry0r9b9CfEpvgkeFgLztwCiwxz9ffobAWPe3BlC+pzX8xAfjmjW3qsImWV/R+d0XQ5jP4TDc7S/8LCQEu963RP4B7K9fgQYdd+OFULyEOzz7FvpKx/GeebE/byZtvdhnAUjN+sciH/G7Vuh/aI5OeQ+wOP+hDze62dbCGRLHq9vTx2Sg6C6aN+Kq4uQOTBin/N4PGwZ0FyhRl1XQWau9MpUQXJ1XdXzncM8bw6e++ZmuC1kZt7a338C2/cQb11vSBWMW4aRV6bKvhVC+iDYczVjVub05CJkHqxx1asO6XVmRxh9CF/1q6/mwLzfvsL7E9Kf3ov5tpDaThU83yLEhxGrt2r1+5RXpQ/pl4sw6hAOI9asVfVZMPbq9351UR/SL9c/Q0jfWW7vbwvZi/f1657AthDINvtbIIdrPiQHQX81GLlz9b+LkLnAd0d8/je/wIZ9kGeFZPTV5RC/6/odzUH6gPt7yOPNfrZPiOeCbEveEeK73e6fcUg/BM3Dc25OhDGvXujZVgjphaC56p0VzHMQ3Z4+Z8Vh7LO/8LCQEu963RM4LKRvFbJNdRGiQ1C9o7/aSu/+Ge9z9hxyFmec4Wfvx8chBpkDQQMQDkH7IdzcGdpnTl54WIihG1/zBA4Lgefbhvi1zSqPDdE7r0wVxIdgaVU9L7+KkHnAoQXY/uYEHPwzoc5X1XOlVQGf8+u6yhxEl4sw6jDyyh0WUuJdr3sC2z8PqQ3vyyOpQbYp1xfVYZ7TNw/JycWeU4d5Xn+PkKyzRDOdwzwP0e3reDYHxn7zEL1z4P4e8nizn8N/ZEG2B8F+Xhj1vuXOIXkIOq/n5Powz+tfQcgMGLH3em8Yc+pi75ND+uSifSLMc+YLDwsp8a7XPYHDQtzm6kjdh2y9671fX+x+5z0HuU/PzXjvlYu9BzJ75a/yXe/9kLkQNN9z6oWHhZR41+uewOGfGHoUtwjjdiEcgubsg1Ff+TDm7F+hcyB9EFTfY58ByUJQH8LthXB9EaKbEyF6zwHT7yf2mRfVC+9PiE/lTXD7HgLZNgQ9X22tasXVYeyDOa9ZVfatENJf2SoI73mIDr/RTPVVya9i9VRBZtZ11aq/vCr9uq7qHDJPXYTowP095PFmP8s/QzwnZHtnvN6IKnNnWNmqs9x3fBjP7Iy6XxXEr+sqCDcnllcF8SGoL8KoQziMWLOqILr9e7z/DNk/jTe43hZSm9sXjFvce/trfwdIfu/Vtb4IyUGw6/LqrTrjlellj6h/lcN4tt4H8Vdz1UX7YeyDkVd+W4hNN772CSz/llXbqurHg2y165WtUofkIKhemX1BfDVzHSG5lQ50a+PA5/cCBRi5urg6C6Rv5dsPycnFVR8kD9x/y3q82c/9H1nvuhA/TmKdc1YrH/Kx6z2rfM/BvN/cao56oVkRMrO8KvWOkFzX5dW7L/UVmu0+jPeZ5e5PSH9qL+anXww9H2S7MKJ+R7cPyXcOo977zzikH4646oVkPYu5ztVFSB8Eu945JAdBfe8Do65feH9C6im8UR3+2uvZIFt0q+ryFZoTzcnPEHJfCPa882ZotnvqK4Tcyz5zEF2uD6Ouv8Le1/m+7/6E7J/GG1x/eSGQtwOCX/0dfDvsg3GOvgjxIWifCNEBpc8vgcCGGn2mekdIr/nun3H7xLP83v/yQvbN9/XPP4FtIW4T8nasbmVu5XcdMg9GvDqn52Cc0+93hfeZ9kBm68Nzbp95EdIHQXMdze/1bSF78b5+3RNYLmS2vTomjFuHkVdmVs77+Pj4/L8ln2VmGozznWNWXtg1eUfITAjq14yqFVe/ijWrynxdV8F4X/3C5ULKvOvvP4HTb+owbrM2PCtIDkY0668G13zzonMg/ep7vJKpvLm6ruocxntAeM9VbxXEh2Bps4L4zoGRl35/QmZP7oXathDIts7OAtdyfQ6kr96CffVc52Zh7O+5Ge+9kBk9C3N9lYN53vuJMObUn83dFtJDN3/NE9j+u6y+PZhv9yzXfw3IHPsgvOfk5uQrNAeZB2xRvU34dXGmA5/f7ntuxdVFSP+v2x0A4kPQvn3w/oTsn8YbXC8X4vZEyFYh6Nn15aK6COmTm4PoK67e+9T3COMsPXshPgT14Rp3zqpPH57Ps3+Gy4XMwrf255/A9j0EslW3vLq1PiQPwVUe4tu3yumL5iD9MEdzhb23tCpIr75Y3k8UZD4Ez+Y/8+9PyE9s5AdnbH/LciZkyzBi993yCiH9+hAOQefpyzvqX0EYZzvLXrnYdbloToRr82HM9XkQH4LOL7w/IfUU3qi2P0M8k9s8Qzhut2bAXHdeZWYF6YM5znq61u8BmdVzEB2C9kG4eQjXV7+KZ30z//6EXH26fyl3eSGQtwWC/Xww6m4fRv2sT99+UR2ez6scJGMvhENQXYRRrxnfKefZC5kr7776Hi8vZN90X/+5J3BYCGSrEPTWbldUh3lOf4WQvj5PDvFhRP3V3NJXmZVePVUwvxdEtx/Cq2dfMOrmzUB8dQjXLzwspMS7XvcEDt9DPIpblIuQreqL3ZefIYzzen41H9IHa3SWMyBZ9RWafzzGBMz74bkO8Vdz93e5PyH7p/EG19v3ELcnrs7Wfcj2zevDqOuL5uQipE8fRm5Of4ZmIL1yEaJD0Bndl3fseX31jvqQ+8nNyQvvT0g9hTeq7c8QyPbgGq5+B0h/3z7M9T6n93Xe85C5QLc+//df1Q9c+ieBfQCkT71mVa24Oox96iKs/fsT4lN6E9wWUpu/Uqtz29t9dRHydkCw5+FrunML+yx5eVWdQ+4FQX2xeqrkkBwE1TtWT1XX5eVVyfe4LWQv3tevewKHhUC2DyOujlibroLk67rqLH/mQ+aZq5lVcogPR1xl1MWaVyUXS6uSi6XtC3JvfQiHEfXtlYvqhYeFGLrxNU/gxxcC49sB4f56MPJ6K6pWvrpY2X2pF6rX9awg94Zgz/R+GHMw8p6Xd/Q+kP4VL/3HF1JD7/r+E/i/FwLj1j2Kb4kc5rmVbz+kD+ZofyEkU9dVzlghjHkYec34EwW5j+eCcOD+P595vNnP4RPi1jquzm1Ov/Ou64v6ojrkrem6vvoeuwfjDLMw1/XFPk8dxn5zMOrmRXPiTD8sxNCNr3kC20Ig24XneHZMSP8qB/EhaK6/NeoijHn1PcKYOZvZ/c73s+taXyxtX2c6jOezF6ID958hjzf72T4hb3au/+xx/gcAAP//hhKxrgAAAAZJREFUAwCzEj6hRhN1BwAAAABJRU5ErkJggg==)

手机扫码阅读
