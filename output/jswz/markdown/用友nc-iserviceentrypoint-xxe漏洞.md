---
title: "用友NC IServiceEntryPoint XXE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html
asset_dir: assets/用友nc-iserviceentrypoint-xxe漏洞
---

# 用友NC IServiceEntryPoint XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/10 08:30
- 1230浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

VPN服务

物流软件安全

企业安全咨询

---

# 漏洞简介

⽤友NC IServiceEntryPoint 接⼝处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感⽂件，进 ⼀步利⽤可导致服务器失陷。

漏洞预警服务

# 影响版本

NC65

# fofa语法

> `app="⽤友-UFIDA-NC"`

# 漏洞分析

看下 `IServiceEntryPoint` 的业务逻辑

```
package nc.uap.oba.word.webservice;

import nc.bs.framework.common.UserExit;
import nc.uap.oba.Serializer;
import nc.uap.oba.word.webservice.entity.BusinessResult;
import nc.uap.oba.word.webservice.entity.RequestInfo;
import nc.uap.oba.word.webservice.entity.ResponseService;
import nc.uap.oba.word.webservice.handler.CustomServiceHandler;
import nc.uap.oba.word.webservice.handler.ReqServiceHandler;

public class ServiceEntryPointImpl implements IServiceEntryPoint {
    public ServiceEntryPointImpl() {
    }

    public String getResult(String data) {
        BusinessResult result = new BusinessResult();
        result.setSuccessful(false);
        String message = null;

        try {
            RequestInfo reqInfo = (RequestInfo)Serializer.deserialize(data, RequestInfo.class);
            UserExit.getInstance().setUserDataSource(reqInfo.getDsName());
            message = reqInfo.getName();
```

深入探索

数据库

文本剥离工具

传输层安全性协议

`getResult` 方法直接将 `data` 带入 `Serializer.deserialize` 方法中，看下其实现逻辑

网络安全

```
package nc.uap.oba;

import java.io.StringReader;
import java.io.StringWriter;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.transform.stream.StreamSource;

public class Serializer {
    public Serializer() {
    }

    public static String serialize(Object value) throws Exception {
        StringWriter writer = new StringWriter();
        JAXBContext jaxbContext = JAXBContext.newInstance(new Class[]{value.getClass()});
        Marshaller marshaller = jaxbContext.createMarshaller();
        marshaller.marshal(value, writer);
        return writer.getBuffer().toString();
    }

    public static <T> T deserialize(String xml, Class<?> type) throws Exception {
        JAXBContext jaxbContext = JAXBContext.newInstance(new Class[]{type});
        StreamSource streamSouce = new StreamSource(new StringReader(xml));
        Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
        return (T)unmarshaller.unmarshal(streamSouce);
    }
}
```

`deserialize` 方法里直接使用 `javax.xml.bind.Unmarshaller` 对 xml 内容进行操作，而JAXB的`Unmarshaller`默认启用外部实体解析功能，未对XML输入中的实体引用进行限制，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)测试

```
POST /uapws/service/nc.uap.oba.word.webservice.IServiceEntryPoint HTTP/1.1
Host: nc.mrxn.net
Content-Type: text/xml;charset=UTF-8

<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:iser="http://webservice.word.oba.uap.nc/IServiceEntryPoint">  
  <soapenv:Header/>  
  <soapenv:Body> 
    <iser:getResult> 
      <!--type: string-->  
      <iser:string>XXE POC</iser:string> 
    </iser:getResult> 
  </soapenv:Body> 
</soapenv:Envelope>
```

DNSLOG 平台成功收到HTTP请求

计算机服务器

[![用友NC IServiceEntryPoint XXE漏洞](images/img-001-625a4ddb57c1.webp)](https://image.mrxn.net/1996db71b511443ca42b5b9b92f32c1f.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
