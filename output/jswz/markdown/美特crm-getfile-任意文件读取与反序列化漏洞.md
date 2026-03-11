---
title: "美特CRM getFile 任意文件读取与反序列化漏洞"
source: https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html
asset_dir: assets/美特crm-getfile-任意文件读取与反序列化漏洞
---

# 美特CRM getFile 任意文件读取与反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/9 08:32
- 1255浏览
- [0评论](#comment)
- 1小时阅读

深入探索

脚本语言

客户关系管理

encrypt

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM getFile 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)和fastjson[反序列化漏洞](https://mrxn.net/tag/rce)。

# 影响版本

CRM6.5

# fofa语法

> `body="/common/scripts/basic.js" && body="www.metacrm.com.cn"`

# 漏洞分析

深入探索

Nessus

在线安全工具

防火墙软件

先看 web.xml 里对于 getFile 接口的定义

客户关系管理

```
<!-- 流的方式展示文件 -->
    <servlet>
        <servlet-name>getFile</servlet-name>
        <servlet-class>com.metasoft.framework.controller.getFile</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>getFile</servlet-name>
        <url-pattern>/getFile</url-pattern>
    </servlet-mapping>
```

进入 `com.metasoft.framework.controller.getFile` 看下其实现逻辑

漏洞预警服务

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-001-3c6829ebc9ee.webp)](https://image.mrxn.net/17cd8d4bb8b84abe8171ac39996c8c54.webp)

以及系统的fastjson版本 fastjson-1.2.4.jar,是存在漏洞的版本

物流软件安全

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-002-9fc49f9e3085.webp)](https://image.mrxn.net/66fd2a7d00644896b6b04010da7c0f8f.webp)

看下AES加解密的部分

```
public class AesEcbCipher {
    private static final String SECRET_KEY = "metacrmloginpass";
    private byte[] key = "metacrmloginpass".getBytes();

    public AesEcbCipher(String secretKey) {
        this.key = secretKey.getBytes();
    }

    public AesEcbCipher() {
    }

    public String Encrypt(String sSrc) {
        try {
            SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, skeySpec);
            byte[] encrypted = cipher.doFinal(sSrc.getBytes("UTF-8"));
            return (new BASE64Encoder()).encode(encrypted);
        } catch (Exception ex) {
            Debug.error("", ex);
            return null;
        }
    }

    public String Decrypt(String sSrc) {
        if (sSrc != null && sSrc.length() != 0) {
            try {
                SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(2, skeySpec);
                byte[] encrypted1 = (new BASE64Decoder()).decodeBuffer(sSrc);
                byte[] original = cipher.doFinal(encrypted1);
                return new String(original, "UTF-8");
            } catch (Exception ex) {
                Debug.error("", ex);
                return sSrc;
            }
        } else {
            return sSrc;
        }
    }

    public String encrypt(String sSrc) {
        try {
            SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, skeySpec);
            byte[] encrypted = cipher.doFinal(sSrc.getBytes("UTF-8"));
            return Hex.encodeHexStr(encrypted);
        } catch (Exception ex) {
            Debug.error("", ex);
            return null;
        }
    }

    public String decrypt(String sSrc) {
        if (sSrc != null && sSrc.length() != 0) {
            try {
                SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(2, skeySpec);
                byte[] encrypted1 = Hex.decodeHex(sSrc.toCharArray());
                byte[] original = cipher.doFinal(encrypted1);
                return new String(original, "UTF-8");
            } catch (Exception ex) {
                Debug.error("", ex);
                return sSrc;
            }
        } else {
            return sSrc;
        }
    }
}
```

硬编码密钥 `metacrmloginpass` ，加解密都是基于hex格式进行，即传入的数据为hex格式。

## 反序列化

再看下涉及反序列化的处理逻辑

```
import com.alibaba.fastjson.JSONObject;
......
String a = request.getServletPath();
String c = request.getRequestURI();
c = StringUtil.replaceStr(c, a + "/", "");
String[] ps = StringUtil.string2array(c, "/");
String url = ps[0];
AesEcbCipher aec = new AesEcbCipher();
String dec = aec.decrypt(url);
JSONObject json = JSONObject.parseObject(dec);
```

`dec` 最终来自AES解密后 `url` 后的结果，而 `url`又来自 `request.getRequestURI()` 替换掉 ServletPath+/ 后的值，如请求 `/mrxn/xxxxxxx` 得到的最终 `url` 值就是去掉 `mrxn/` 后的 `xxxxxxx` ；经过上述处理后，直接调用 fastjson 的 `parseObject` 方法处理，导致fastjson 反序列化漏洞。

漏洞预警服务

## 文件读取

```
String fileName = json.getString("fileName");
String folder = json.getString("folder");
String sCorpName = json.getString("sCorpName");
String securityCode = json.getString("securityCode");
UserState us = UserManager.getUserBySessionId(request.getSession().getId());
if (us == null && !FileSecurityCode.checkSecurityCode(securityCode)) {
    request.setAttribute("error", (new ResourceService()).getDispMessage("error.common.upanddown.login"));

    try {
        request.getRequestDispatcher("/common/images/default/limit.png").forward(request, response);
    } catch (ServletException e) {
        Debug.error("", e);
    }

} else {
    FileSecurityCode.visits(securityCode);
    response.setContentType(Path.getContentType(fileName));
    String path;
    if ("attach".equals(folder)) {
        path = Path.getAttachAbsoluteDirectory(sCorpName);
    } else if ("template".equals(folder)) {
        path = Path.getTemplateAbsoluteDirectory(sCorpName);
    } else if ("userlogo".equals(folder)) {
        path = Path.getLogoAbsoluteDirectory(sCorpName);
    } else if ("messageserv".equals(folder)) {
        path = Path.getMessageServerAbsoluteDirectory(sCorpName);
    } else if ("picture".equals(folder)) {
        path = Path.getPictureAbsoluteDirectory(sCorpName);
    } else if ("skinbackground".equals(folder)) {
        path = Path.getBackgroundAbsoluteDirectory(sCorpName);
    } else if ("icon".equals(folder)) {
        path = Path.getIconAbsoluteDirectory(sCorpName);
    } else {
        path = Path.getTempAbsoluteDirectory(sCorpName);
    }

    path = path + fileName;
    this.log.debug("path={}", path);
    FileInputStream fio = new FileInputStream(new File(path));
    IOUtils.copyLarge(fio, response.getOutputStream());
    IOUtils.closeQuietly(fio);
```

AES解密后的内容经fastjson处理后，取出其中需要的 fileName 、folder、sCorpName、securityCode等，主要是`path = path + fileName;` 其中 path 与 fileName 都是用户可控，且对路径无任何校验或过滤，拼接后直接调用 `new File(path)` 进行文件操作，造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

整体执行流程如下图所示

漏洞预警服务

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-003-45d7ac5b4abf.webp)](https://image.mrxn.net/91a1f5068aab4ef580b25c59b0af52ce.webp)

# 漏洞复现

## 反序列化

```
GET /getFile/AES加密后的payload HTTP/1.1
Host: metasoft.mrxn.net
Cookie: JSESSIONID=D74D969B9489FFBE41D5F5ACE5CAC014
```

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-004-ed6e8367b5f4.webp)](https://image.mrxn.net/e384f1c4633d4822803e7d85d3cc0e17.webp)

DNSLOG平台成功收到请求

## 文件读取

> [漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)需要合法的cookie或者securityCode
>
> 漏洞预警服务
>
> 而系统自带 druid ，因此可以访问 `/druid/websession.html` 拿到系统以及存在的 `SESSIONID` 后进行批量枚举尝试

```
GET /getFile/AES加密后的payload HTTP/1.1
Host: metasoft.mrxn.net
Cookie: JSESSIONID=2A6482AE7774FBC13DD7854E15CE90F4
```

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-005-e7446d765335.webp)](https://image.mrxn.net/f8ea7ec43dbc4568bd42aaaa15a43b51.webp)  
[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-006-ade69cb525fe.webp)](https://image.mrxn.net/6ff0bddd7fdb498793e60cb057177031.webp)

成功读取到 `web.xml` 文件内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
- [#目录遍历](https://mrxn.net/tag/%E7%9B%AE%E5%BD%95%E9%81%8D%E5%8E%86)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.反序列化](#toc-4-1-)
- [4.2.文件读取](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.反序列化](#toc-5-1-)
- [5.2.文件读取](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
