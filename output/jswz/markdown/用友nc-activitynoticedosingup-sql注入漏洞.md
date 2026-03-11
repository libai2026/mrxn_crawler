---
title: "用友NC ActivityNotice/doSingUp SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html
asset_dir: assets/用友nc-activitynoticedosingup-sql注入漏洞
---

# 用友NC ActivityNotice/doSingUp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/25 08:19
- 873浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

计算机安全

数据库

安全

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 ActivityNotice/doSingUp 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

SQL注入防护

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看`ActivityAction` 类的`doSingUp`方法的实现逻辑吧

```
@Servlet(
    path = "/ActivityNotice"
)
public class ActivityAction extends BaseAction {

@Action
public void doSingUp() {
    HttpServletResponse response = this.getResponse();
    response.setContentType("text/html");
    response.setHeader("Cache-Control", "no-cache");
    response.setCharacterEncoding("UTF-8");
    response.addHeader("Content-type", "text/html;charset=UTF-8");
    HttpServletRequest request = this.request;
    String pk_user = request.getParameter("pk_psndoc");
    String actid = request.getParameter("actid");
    if (pk_user != null && !pk_user.equals("")) {
        IActivitySignupService signup = (IActivitySignupService)NCLocator.getInstance().lookup(IActivitySignupService.class);

        try {
            if (signup.isSingup(pk_user, actid, pk_user)) {
                signup.addUserActivitySignup(pk_user, actid, pk_user, true);
            }
        } catch (BusinessException e3) {
            throw new LfwRuntimeException(e3.getMessage());
        }
```

深入探索

Windows安全工具

传输层安全性协议

安全认证考试

参数`pk_psndoc`、和`actid`被带入`addUserActivitySignup`方法，跟进`addUserActivitySignup`方法看下

代码安全审计

```
public void addUserActivitySignup(String pkUser, String pkActivity, String signupUser, boolean isSchedule) throws BusinessException {
    SignUpVO signup = this.createSignUpFromUser(signupUser);
    signup.setStatus(2);
    signup.setSignupactivity(pkActivity);
    this.saveUserActivitySignup(pkUser, pkActivity, signup, isSchedule);
}
```

继续跟进`saveUserActivitySignup`方法

```
public SignUpVO saveUserActivitySignup(String pkUser, String pkActivity, SignUpVO signup, boolean isSchedule) throws BusinessException {
    AggActivityVO activityVO = this.getAggActivityVOByUserPKandActivity(signup.getPk_person(), pkActivity);
```

继续跟进`getAggActivityVOByUserPKandActivity`方法

```
private AggActivityVO getAggActivityVOByUserPKandActivity(String pk_person, String pkActivity) throws BusinessException {
    AggActivityVO activityVO = this.getActivityQueryService().getAggActivityByPk(pkActivity);
```

继续跟进`getAggActivityByPk`方法

```
public AggActivityVO getAggActivityByPk(String pk_activity) throws LfwBusinessException, BusinessException {
    if (pk_activity != null && pk_activity.length() != 0) {
        AggActivityVO aggvo = (AggActivityVO)this.getOaQueryService().queryBillOfVOByPK(AggActivityVO.class, pk_activity, true);
```

继续跟进`queryBillOfVOByPK`方法

```
public <T> T queryBillOfVOByPK(Class<T> voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    return (T)(new MDBaseDAO()).queryBillOfVOByPK(voClass, billPK, bLazyLoad);
}
public Object queryBillOfVOByPK(Class voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject ncObj = (new VOQueryPersister(voClass.getName())).queryBillImp(billPK, bLazyLoad);
```

继续跟进`queryBillImp`方法

```
protected NCObject queryBillImp(String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject resNCObj = null;

    try {
        Object resVO = this.dao.retrieveByPK(billPK, this.ignoreDrEqual1);
```

跟进`retrieveByPK`方法

```
public Object retrieveByPK(String pkValue, boolean ignoreDrEqual1) throws MetaDataException {
    if (this.metaCollection != null && this.metaCollection.size() != 0) {
        String whereConStr = "";
        whereConStr = (String)this.tableAliasMap.get(this.bean.getTable().getName()) + "." + this.bean.getTable().getPrimaryKeyName() + "='" + pkValue + "'";
        if (ignoreDrEqual1) {
            whereConStr = whereConStr + " and isnull(" + this.bean.getTable().getName() + ".dr,0)=0 ";
        }
```

跟到这里，[漏洞](https://mrxn.net/tag/%E6%B3%A8%E5%85%A5)原因就很明了了，参数**actid**经过一系列的传递，最终在`retrieveByPK`方法这里被拼接进SQL语句中，整个过程没有对参数**actid**进行校验或过滤，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，也是朴实无华的！这个类之前也发过相关SQL注入漏洞：[用友NC ActivityNotice/export SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html)

漏洞扫描服务

# 漏洞复现

> 需注意NC 大多数为Oracle 少数MSSQL

```
POST /portal/pt/ActivityNotice/doSingUp HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&pk_psndoc=1&actid=SQLI_POC
```

[![用友NC ActivityNotice/doSingUp SQL注入漏洞](images/img-001-956e03a54e17.webp)](https://image.mrxn.net/9f4821689772405383336b420b6b73af.webp)

通过报错注入成功在响应回显当前数据库用户！

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALgElEQVR4Aeyc7XbbRgxEdfP+79wGnlyaC+6Kkp1Y+kGfosP5ALgmqMZJT/vrdrv995X6b/F1Nsu2nlPvaG6l6xeaqesquVjavtRXaFa/85Vu7itYC/ndd/31Lk9gW8jvbd8eqdXBgRuwzfhu7iv9kDPYC+EQVPf7hOgQ1Ifwnus+JKfe0f4z3PdtC9mL1/XrnsBhIZCtw4jPHtG3wj65qC7C/H5nef1CZ4mlVck7lle10iFnWvldX3HIHBhxlj8sZBa6tJ97Aj+2EDh/O+rbrje2CsY8hFemqjJVdW0V3xekR80cRIdg9809it/t39/nxxayv+l1vX4C314IjG8ZhEPQt6cjjH4/Ys/LzUH6YY1mOzpL1IfMkp9h7z/LP+J/eyGP3OTKPP4EDgtx6x1XI80N/m+iDvO3Tv93dPoXzPsM2z9DMyKMsyAcguY6zmaXBvf7Hp3Tc8UPCynxqtc9gW0hkK3DfexHheS7vuIw5iG83rwqmPOzecAhUvOqNOq6qnNg+FMGCDcHI1cXYe5DdLiPzincFlLkqtc/gV/1xnylzo4OeSucDeH2QfiZ3/Ny0f5CtY7lVUHu2X05jD6EV28VhJsXy6vqvLRn6/qE+BTfBA8LgbwFEOznhOgQ7L7cNwPmOf2e77p+R8hcOKJZiCfvCPG9Z0fzkJzcHIw6hEPQPIxcfYaHhcxCl/ZzT2BbCDy2Rd+OfkT4Wj+kD0bs8ztfnaNyeiJkdnlV6nVdBaNfWpU5sbR9rXQzMJ8L0SFovnBbSJGrXv8EfkG25LY7QnwY0aP3vBySl4v2iU/oHy3mIfM/xC/+zVm9HcbZEN7zEB2Cfc4qry7u+65PyP5pvMH19vsQzwLjtt3iCnsfjP36IsSHoHqfD/G73vPyQrOQ3tKq1MXSqiA5dRh5Zaq6D8mVd69gnoPocMTrE3Lvib7A234NgWzr7AyQHAR73rdJhOQgaF5fLkJy+hCuL0J0c4UQzYwIc12/I4x5CK977Kv36anLO+qLe//6hPhU3gS3X0PcUj8X5O1QNyeqi5A8BNU7QnwYcTXXfkj+Xk4PkrW3o7muyyH95iAcguqifXJITl3Ul0NywO36hNze6+uwELcH2ZrHhXAIdt0+dbmovkJzkPkQ7PlVDujRAwc+/r2HBoRD0Nn6Itz3zYmQvFyE6BD0fns8LMTmC1/zBA4/ZcG4PY+132Jddx3mfT3Xec2qgvTrd4T4EKyeqn2ueJVaXc9K/wN3f4Nxdu81qg7Jw4j6IsR/pP/6hPiU3gS3n7L6eSBbdcv6EB2C6mcIyTsPwnufvrq8I8z77ZshpAeCzpxlZxqkD4L2i/ZAfAiqd7Rvj9cnpD+lF/PlQtwajFtWFyG+3O8Hosu7ry7qQ/rk+iLEl5srhNGDcAjas8KaUQXJQ7DnK1MFc998ZapWXB0yB7h+H3J7s6/tp6za5L4gW+vnhegQtKfn5JCcXOx9kJw6hJsX9eWQHHz+11sQrWftUYfk1EV9UX2FkDk9D9Htg/u8cst/ZJV51c8/gacX4lsgQrYOI+r3bwnGHISbg/CzfvPmCiG9ehBeXtVKL6+q+5B+COqvEJKrWVXm6rpKfg+fXsi9YZf3/SdwWAiMW67NVnkriA/B8qr0RYjfeWWr1DuWVwXph+Aqt9erb196MM4wA9EhaL6jeRGSl3e83W4fI9Q/yIN/Oyzkwb4r9o+ewHIhkLcAgt7frYsQX25OVBfhft6+jpC+lQ50a/tv5r23aLDzrp/55kXg40+TIagu9nnyPS4X4pALf/YJbAuB+VY9DsSHEbsvd+tySF/XO4d5zjkiJCcvhGgwYnlVEL2u97U6wz5z7xrmcyE6jHhv1raQe6HL+7kn8PBCfIs6ro4KeStW/kp3vr5cXOn6hWZEGM8C4RDsuZpR1XVIHkY0Vz2z0hdh3l/+wwup8FX//gls/z5kttnS+hEg2+1659Vb1XUY+2Hk5iE6BNU7QnygWw9z4OOnIxsgHILq9f1Urbg6jH3q1VvVOSQPXH/ae3uzr+sfWe+2EMjHZXaumVYfuaqZd0+rnqpVprwqmJ8H5nr1WGezu2+fqC/vqC/C/TOZE2HMQ/j+PtcnxKf1Jrj9og7ZFozoOWHUIVx/v+W6hvgwYnlVvQ+S63plq9RFSB6OaKZjzanqOmRG1+UQH4LqNatKDvFhRP0Vwmf++oSsntKL9OW/wvU89QbMqvty0R65CHkbVtw+SA6C5vVnaEY0I4fMUoeRq6/y6j2nLnZf/ghenxCf4pvgthDI2wJBzwfhMOKZD8mbE31L5I+ifZC5cEQzZzMhveYhvPfpq8thnjcHow+PceD6jeHtzb62T4jn8i044+bEnlfvaE5c+ermIG+Zuqi/Rz1IDwTVRXvkkByMaE4033nXuw+Zqz7Dw0JmoUv7uSewLaRvd8Vh3DKEm4fw1bcAcx/munNX876iw/fuBfN+mOv9jPe+p20hvenir3kCh9+pewzItiGo3re74jD2rfrVRUgfBNX7fbpePqQHgmY6VrYKkoMRy9uX/ZCcHoRDUN28HOKrixDdXOH1CfHpvAkeFgLZ2up8EB+C5iAcguodIT4E9evtqFpxGPMwcvvuIcx76r5V93rLq0wVZE5d7wuiV7YKRm62vKrOSzsspMSrXvcEtoW4rRV6RH05jG+BujmID0F10TyMPoTrixC995evJpZW1TlkRnn7WuUgeQiag/D9jNn1M/ltIbNBl/bzT2D7015vDePWYc7dun2dQ/q6bl6EMQfhK199hjD2em8YdXu7D/dz9kFyvV8u9vyKqxden5B6Cm9Uh9+HuF3IW9DP2n15z3W+yqnDc/eDMd/vVxyS8R6lVclh9Fc6PJar2bNy7swrDTIfuP609/ZmX0//IwuyTbcO4X5f6nIY/ZVuX0dIv7r9M+yZFYfMdAaM3D4YdfMdITkYsc+R2w/Jqxc+vRCHXfhvnsDpT1n9trXFqq7L4bj1ykN0c6VVyWH01UWID8HqrdIvhHgQLG1fEL36ZrXP1nXPQPohWJmqnpPDmIOR9xxw/Rpye7Ov7acsz+XWOkK2CyOas/8MIf2rHMSHYM95P4gPn2i2Z7ouF+FzBqyvzYveR95Rf4WQe+3969eQ/hRfzA8LgWwNgp5vv8W6Vod5Dkbd/KNY96ha5cur2vvFq9TqukoO45lg5JWtMl/X+1J/FmG8D4x8P++wkL15Xf/8Ezj8lOURfDPkIqy3a2aPkLzzRDNw3zdnHyQPQf1CiAYjlve1Grs8g6gL4/1g5OZE+0X4zF+fEJ/Sm+D2U5bbElfn0xcfzcHnWwAc2oCP/6wMRjwE/wjef4Z/Itv/OAAy02z31WHMQTgE7YNwCKo7p6M+JA9B9T1en5D903iD6+3XEMjW4DFcnR3S333fGnUYc92Xi/Z1hMwBurV94pwBbBp8Xh8a/wj2/aEbqIub8ecCMvsPPYB9cMxdn5DD43qtsC3ErZ1hP655GLcNI7fPfOcwz8Nc7/01V00srQoyo66rVr46JC8XYa7ri3WPKvkzuC3kmaYr+++ewGEhkLcARnz0CPVmVJmHzJGLlalacUhfZarMiRAfjmimIyRb86r063pWMObNQHT7RYgOI+o/goeFPNJ0Zf7dE/j2QiBvw+rtUT/7FiBzzK36ui4vfLYXxnvCyJ0H0SFY96rSr+t71XMrXvq3F1JDrvp7T+CvLQTGt8c3BqL3I8Nc730wzzkP4gNKpwh8/H7Ee9kgh/jqor78DGE+p/c5t/CvLaTf5OJfewKHhdSWZrUab1Yfnnsr7HMOzPthrtu3R0gWgt6jI8SHoL6z5B0heRix51Yc0jfzDwuZhS7t557AthDI1uA+ro7W3yrIHPMw8jNdv89VFyFz4RP17BW7vuLqHSH36Hqf3305jP0QDp+4LcSmC1/7BK6FvPb5H+7+PwAAAP//+BP+yAAAAAZJREFUAwCkXtfL0IauZgAAAABJRU5ErkJggg==)

手机扫码阅读
