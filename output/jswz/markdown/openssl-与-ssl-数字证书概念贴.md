---
title: "OpenSSL 与 SSL 数字证书概念贴"
source: https://mrxn.net/jswz/openssl-certificate-encryption.html
asset_dir: assets/openssl-与-ssl-数字证书概念贴
---

# OpenSSL 与 SSL 数字证书概念贴

[Mrxn](https://mrxn.net/author/1)- 发表于2015/9/24 22:10
- 9570浏览
- [0评论](#comment)
- 1小时阅读

深入探索

安全研究工具

Nessus

防火墙软件

---

SSL/TLS 介绍见文章 [SSL/TLS原理详解](https://mrxn.net/tls-ssl-understand.html)。  
如果你想快速自建CA然后签发数字证书，请移步 [基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/openssl-self-sign-ca.html)。

首先简单区分一下HTTPS、SSL、OpenSSL三者的关系：

SSL是在客户端和服务器之间建立一条SSL安全通道的安全协议，而OpenSSL是TLS/SSL协议的开源实现，提供开发库和命令行程序。常说的HTTPS是HTTP的加密版，底层使用的加密协议是SSL。

安全工具开发

## 1. PKI、CA与证书

PKI 就是 Public Key Infrastructure 的缩写，翻译过来就是公开密钥基础设施。它是利用公开密钥技术所构建的，解决网络安全问题的，普遍适用的一种基础设施;是一种遵循既定标准的密钥管理平台,它能够为所有网络应用提供加密和数字签名等密码服务及所必需的密钥和证书管理体系。

PKI既不是一个协议，也不是一个[软件](#)，它是一个标准，在这个标准之下发展出的为了实现安全基础服务目的的技术统称为PKI。可以说CA(认证中心)是PKI的核心，而数字证书是PKI的最基本元素，还有如apache等服务器、浏览器等客户端、银行等应用，都是pki的组件。这篇文章可以帮助理解：[PKI/CA 技术的介绍](http://netsecurity.51cto.com/art/200602/21066.htm) 。

### 1.1 CA

为保证用户之间在网上传递信息的安全性、真实性、可靠性、完整性和不可抵赖性

CA 机构，又称为证书认证中心 (Certificate Authority) 中心，是一个负责发放和管理数字证书的第三方权威机构，它负责管理PKI结构下的所有用户(包括各种应用程序)的证书，把用户的公钥和用户的其他信息捆绑在一起，在网上验证用户的身份。CA机构的数字签名使得攻击者不能伪造和篡改证书。

认证中心主要有以下5个功能：

1. 证书的颁发：接收、验证用户(包括下级认证中心和最终用户)的数字证书的申请。可以受理或拒绝
2. 证书的更新：认证中心可以定期更新所有用户的证书，或者根据用户的请求来更新用户的证书
3. 证书的查询：查询当前用户证书申请处理过程；查询用户证书的颁发信息，这类查询由目录服务器ldap来完成
4. 证书的作废：由于用户私钥泄密等原因，需要向认证中心提出证书作废的请求；证书已经过了有效期，认证中心自动将该证书作废。认证中心通过维护证书作废列表 (Certificate Revocation List,CRL) 来完成上述功能。
5. 证书的归档：证书具有一定的有效期，证书过了有效期之后就将作废，但是我们不能将作废的证书简单地丢弃，因为有时我们可能需要验证以前的某个交易过程中产生的数字签名，这时我们就需要查询作废的证书。

### 1.2 Certificate

#### 1.2.1 X.509标准

“SSL证书”这个词是一个相对较大的概念，整个PKI体系中有很多SSL证书格式标准。PKI的标准规定了PKI的设计、实施和运营，规定了PKI各种角色的”游戏规则”，提供数据语法和语义的共同约定。x.509是PKI中最重要的标准，它定义了公钥证书的基本结构，可以说PKI是在X.509标准基础上发展起来的：

- SSL公钥证书
- 证书废除列表CRL(Certificate revocation lists 证书黑名单)

参考 [http://en.wikipedia.org/wiki/X.509](https://en.wikipedia.org/wiki/X.509) 。

另外一个常用的标准是`PKCS#12`，通常采用pfx,p12作为文件扩展名，openssl和java的keytool工具都可以用作生产此类格式的证书。

软件

#### 1.2.2 ssl公钥证书格式

```
1. 证书版本号(Version)
版本号指明X.509证书的格式版本，现在的值可以为:
    1) 0: v1
    2) 1: v2
    3) 2: v3
也为将来的版本进行了预定义
2. 证书序列号(Serial Number)
序列号指定由CA分配给证书的唯一的"数字型标识符"。当证书被取消时，实际上是将此证书的序列号放入由CA签发的CRL中，
这也是序列号唯一的原因。
3. 签名算法标识符(Signature Algorithm)
签名算法标识用来指定由CA签发证书时所使用的"签名算法"。算法标识符用来指定CA签发证书时所使用的:
    1) 公开密钥算法
    2) hash算法
example: sha256WithRSAEncryption
须向国际知名标准组织(如ISO)注册
4. 签发机构名(Issuer)
此域用来标识签发证书的CA的X.500 DN(DN-Distinguished Name)名字。包括:
    1) 国家(C)
    2) 省市(ST)
    3) 地区(L)
    4) 组织机构(O)
    5) 单位部门(OU)
    6) 通用名(CN)
    7) 邮箱地址
5. 有效期(Validity)
指定证书的有效期，包括:
    1) 证书开始生效的日期时间
    2) 证书失效的日期和时间
每次使用证书时，需要检查证书是否在有效期内。
6. 证书用户名(Subject)
指定证书持有者的X.500唯一名字。包括:
    1) 国家(C)
    2) 省市(ST)
    3) 地区(L)
    4) 组织机构(O)
    5) 单位部门(OU)
    6) 通用名(CN)
    7) 邮箱地址
7. 证书持有者公开密钥信息(Subject Public Key Info)
证书持有者公开密钥信息域包含两个重要信息:
    1) 证书持有者的公开密钥的值
    2) 公开密钥使用的算法标识符。此标识符包含公开密钥算法和hash算法。
8. 扩展项(extension)
X.509 V3证书是在v2的基础上一标准形式或普通形式增加了扩展项，以使证书能够附带额外信息。标准扩展是指
由X.509 V3版本定义的对V2版本增加的具有广泛应用前景的扩展项，任何人都可以向一些权威机构，如ISO，来
注册一些其他扩展，如果这些扩展项应用广泛，也许以后会成为标准扩展项。
9. 签发者唯一标识符(Issuer Unique Identifier)
签发者唯一标识符在第2版加入证书定义中。此域用在当同一个X.500名字用于多个认证机构时，用一比特字符串
来唯一标识签发者的X.500名字。可选。
10. 证书持有者唯一标识符(Subject Unique Identifier)
持有证书者唯一标识符在第2版的标准中加入X.509证书定义。此域用在当同一个X.500名字用于多个证书持有者时，
用一比特字符串来唯一标识证书持有者的X.500名字。可选。
11. 签名算法(Signature Algorithm)
证书签发机构对证书上述内容的签名算法
example: sha256WithRSAEncryption
12. 签名值(Issuer's Signature)
证书签发机构对证书上述内容的签名值
```

example:

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 9 (0x9)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CN, ST=GuangDong, L=ShenZhen, O=COMPANY Technologies Co., Ltd, OU=IT_SECTION, CN=registry.example.com.net/emailAddress=zhouxiao@example.com.net
        Validity
            Not Before: Feb 11 06:04:56 2015 GMT
            Not After : Feb  8 06:04:56 2025 GMT
        Subject: C=CN, ST=GuangDong, L=ShenZhen, O=TP-Link Co.,Ltd., OU=Network Management, CN=172.31.1.210
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:a4:b0:dd:eb:c1:cf:5d:47:61:a6:ea:ef:8b:aa:
                    4b:f0:b4:2c:d8:96:c7:7c:ac:fa:c7:35:88:53:d0:
                    ...
                    8a:76:dc:8f:8c:44:c8:0b:3c:36:88:5f:01:f0:44:
                    4e:81:e6:7a:2b:ff:ba:da:33:a5:27:11:c6:f0:08:
                    6e:f3
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints: 
                CA:FALSE
            Netscape Comment: 
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier: 
                07:C6:87:B7:C1:1E:28:E8:96:3F:EB:40:1E:82:41:45:CA:81:B6:3D
            X509v3 Authority Key Identifier: 
                keyid:A4:C2:14:6A:39:D1:95:1E:BD:DF:3B:92:4A:5C:12:42:1B:BC:53:B8
    Signature Algorithm: sha256WithRSAEncryption
         0c:c6:81:70:cd:0a:2d:94:4f:cb:a4:1d:ef:9e:8e:e4:73:ae:
         50:62:a8:9c:64:ef:56:0f:41:fe:6b:b4:d3:07:37:39:2c:ed:
         ...
         6f:62:61:b8:03:d7:97:31:ab:05:44:20:07:65:8b:ad:e2:cc:
         ad:65:73:f6:82:0f:9e:65:d0:ae:b7:1e:fd:9f:c1:d7:41:6c:
         0f:06:95:ee
-----BEGIN CERTIFICATE-----
MIIEMDCCAxigAwIBAgIBCTANBgkqhkiG9w0BAQsFADCBtTELMAkGA1UEBhMCQ04x
EjAQBgNVBAgMCUd1YW5nRG9uZzERMA8GA1UEBwwIU2hlblpoZW4xJjAkBgNVBAoM
...
ujwwRar6pPzusO95WuS93HsNmL2ZFZ63DS4LcW9iYbgD15cxqwVEIAdli63izK1l
c/aCD55l0K63Hv2fwddBbA8Gle4=
-----END CERTIFICATE-----
```

## 2. 附：数据加密的基础知识

### 对称密钥加密

对称密钥加密（一个密钥），也叫做共享密钥加密或机密密钥加密，使用发件人和收件人共同拥有的单个密钥。这种密钥既用于加密，也用于解密，叫做机密密钥。对称密钥加密是加密大量数据的一种行之有效的方法。

对称密钥加密有许多种算法如DES,RC4,IDEA等，但所有这些算法都有一个共同的目的：以可还原的方式将明文 （未加密的数据转换为暗文。暗文使用加密密钥编码，对于没有解密密钥的任何人来说它都是没有意义的。由于对称密钥加密在加密和解密时使用相同的密钥，所以这种加密过程的安全性取决于是否有未经授权的人获得了对称密钥。

安全工具开发

衡量对称算法优劣的主要尺度是其密钥的长度。密钥越长，在找到解密数据所需的正确密钥之前必须测试的密钥数量就越多。需要测试的密钥越多，破解这种算法就越困难。

### 公钥加密

公钥加密使用两个密钥:一个公钥和一个私钥，这两个密钥在数学上是相关的。为了与对称密钥加密相对照，公钥加密有时也叫做不对称密钥加密。在公钥加密中，公钥可在通信双方之间公开传递，或在公用储备库中发布，但相关的私钥是保密的。只有使用私钥才能解密用公钥加密的数据。使用私钥加密的数据只能用公钥解密。下图中，发件人拥有收件人的公钥，并用它加密了一封邮件，但只有收件人掌握解密该邮件的有关私钥。

[[![OpenSSL 与 SSL 数字证书概念贴](images/img-001-66174d251a60.gif "点击查看原图")](https://mrxn.net/content/uploadfile/201509/a2f41443107513.gif)](https://mrxn.net/content/uploadfile/201509/a2f41443107513.gif)

公钥算法的主要局限在于，这种加密形式的速度相对较低。实际上，通常仅在关键时刻才使用公钥算法，如在实体之间交换对称密钥时，或者在签署一封邮件的散列时（散列是通过应用一种单向数学函数获得的一个定长结果，对于数据而言，叫做散列算法）。将公钥加密与其它加密形式（如对称密钥加密）结合使用，可以优化性能，如数字签名和密钥交换。

网络安全

常用公钥算法：

- RSA：适用于数字签名和密钥交换。 是目前应用最广泛的公钥加密算法，特别适用于通过 Internet 传送的数据，RSA算法以它的三位发明者的名字命名。
- DSA：仅适用于数字签名。 数字签名算法 (Digital Signature Algorithm, DSA) 由美国国家安全署 (United States National Security Agency, NSA) 发明，已作为数字签名的标准。DSA 算法的安全性取决于自计算离散算法的困难。这种算法，不适用于数据加密。
- Diffie-Hellman：仅适用于密钥交换。 Diffie-Hellman 是发明的第一个公钥算法，以其发明者 Whitfield Diffie 和 Martin Hellman 的名字命名。Diffie-Hellman 算法的安全性取决于在一个有限字段中计算离散算法的困难。

### 单向散列算法

散列，也称为散列值或消息摘要 ，是一种与基于密钥（对称密钥或公钥）的加密不同的数据转换类型。散列就是通过把一个叫做散列算法的单向数学函数应用于数据，将任意长度的一块数据转换为一个定长的、不可逆转的数字，其长度通常在128～256位之间。所产生的散列值的长度应足够长，因此使找到两块具有相同散列值的数据的机会很少。如发件人生成邮件的散列值并加密它，然后将它与邮件本身一起发送。而收件人同时解密邮件和散列值，并由接收到的邮件产生另外一个散列值，然后将两个散列值进行比较。如果两者相同，邮件极有可能在传输期间没有发生任何改变。

下面是几个常用的散列函数：

- MD5：是RSA数据安全公司开发的一种单向散列算法，MD5被广泛使用，可以用来把不同长度的数据块进行暗码运算成一个128位的数值。
- SHA-1：与 DSA 公钥算法相似，安全散列算法1（SHA-1）也是由 NSA 设计的，并由 NIST 将其收录到 FIPS 中，作为散列数据的标准。它可产生一个 160 位的散列值。SHA-1 是流行的用于创建数字签名的单向散列算法。
- MAC（Message Authentication Code）：消息认证代码，是一种使用密钥的单向函数，可以用它们在系统上或用户之间认证文件或消息，常见的是HMAC（用于消息认证的密钥散列算法）。
- CRC（Cyclic Redundancy Check）：循环冗余校验码，CRC校验由于实现简单，检错能力强，被广泛使用在各种数据校验应用中。占用系统资源少，用软硬件均能实现，是进行数据传输差错检测地一种很好的手段（CRC 并不是严格意义上的散列算法，但它的作用与散列算法大致相同，所以归于此类）。

### 数字签名：结合使用公钥与散列算法

数字签名是邮件、文件或其它数字编码信息的发件人将他们的身份与信息绑定在一起（即为信息提供签名）的方法。对信息进行数字签名的过程，需要将信息与由发件人掌握的秘密信息一起转换（使用私钥）为叫做签名的标记。数字签名用于公钥环境（任何人都可以拥有）中，它通过验证发件人确实是他或她所声明的那个人，并确认收到的邮件与发送的邮件完全相同。

安全工具开发

散列算法处理数据的速度比公钥算法快得多。散列数据还缩短了要签名的数据的长度，因而加快了签名过程。

### 密钥交换：结合使用对称密钥与公钥

对称密钥算法非常适合于快速并安全地加密数据。但其缺点是，发件人和收件人必须在交换数据之前先交换机密密钥。结合使用加密数据的对称密钥算法与交换机密密钥的公钥算法可产生一种既快速又灵活的解决方案。

## 参考

- [openSSL命令、PKI、CA、SSL证书原理](http://www.cnblogs.com/littlehann/p/3738141.html)
- [X.509 wikipeida](https://en.wikipedia.org/wiki/X.509)
- [PKI 基础知识](http://www.wosign.cn/Basic/aboutPKI.htm)
- [数字证书及CA的扫盲介绍](http://kb.cnblogs.com/page/194742/)

原文地址：<http://seanlook.com/2015/01/15/openssl-certificate-encryption/>

- 标签：
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
- [#加密通讯](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86%E9%80%9A%E8%AE%AF)
- [#http](https://mrxn.net/tag/http)
- [#ssl](https://mrxn.net/tag/ssl)
- [#https](https://mrxn.net/tag/https)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

---

文章目录

- [1.
  1. PKI、CA与证书](#toc-1-)
- [1.1.
  1.1 CA](#toc-1-1-)
- [1.2.
  1.2 Certificate](#toc-1-2-)
- [1.2.1.
  1.2.1 X.509标准](#toc-1-2-1-)
- [1.2.2.
  1.2.2 ssl公钥证书格式](#toc-1-2-2-)
- [2.
  2. 附：数据加密的基础知识](#toc-2-)
- [2.1.
  对称密钥加密](#toc-2-1-)
- [2.2.
  公钥加密](#toc-2-2-)
- [2.3.
  单向散列算法](#toc-2-3-)
- [2.4.
  数字签名：结合使用公钥与散列算法](#toc-2-4-)
- [2.5.
  密钥交换：结合使用对称密钥与公钥](#toc-2-5-)
- [3.
  参考](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
