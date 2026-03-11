---
title: "sqlmap 最新版系统自带 tamper 解释中文翻译"
source: https://mrxn.net/jswz/sqlmap-tamper.html
---

# sqlmap 最新版系统自带 tamper 解释中文翻译

[Mrxn](https://mrxn.net/author/1)* 发表于2023/10/17 22:16
* 7727浏览
* [3评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

截止目前最新版本为
`1.7.10.1#dev`
版本.系统自带 tamper 共计 69个.相较笔者早期的文章
[SQLMAP tamper WAF 绕过脚本列表注释](https://mrxn.net/netsafe/492.html)
,变化还是较大,因此记录下,下面分别是英文和中文翻译.

# 英文

使用如下命令获取
[sqlmap](//mrxn.net/tag/sqlmap "sqlmap")
自带所有的 tamper 列表

```
python3 sqlmap.py --list-tampers
```

```
* 0eunion.py - Replaces instances of <int> UNION with <int>e0UNION
* apostrophemask.py - Replaces apostrophe character (') with its UTF-8 full width counterpart (e.g. ' -> %EF%BC%87)
* apostrophenullencode.py - Replaces apostrophe character (') with its illegal double unicode counterpart (e.g. ' -> %00%27)
* appendnullbyte.py - Appends (Access) NULL byte character (%00) at the end of payload
* base64encode.py - Base64-encodes all characters in a given payload
* between.py - Replaces greater than operator ('>') with 'NOT BETWEEN 0 AND #' and equals operator ('=') with 'BETWEEN # AND #'
* binary.py - Injects keyword binary where possible
* bluecoat.py - Replaces space character after SQL statement with a valid random blank character. Afterwards replace character '=' with operator LIKE
* chardoubleencode.py - Double URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %2553%2545%254C%2545%2543%2554)
* charencode.py - URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %53%45%4C%45%43%54)
* charunicodeencode.py - Unicode-URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054)
* charunicodeescape.py - Unicode-escapes non-encoded characters in a given payload (not processing already encoded) (e.g. SELECT -> \u0053\u0045\u004C\u0045\u0043\u0054)
* commalesslimit.py - Replaces (MySQL) instances like 'LIMIT M, N' with 'LIMIT N OFFSET M' counterpart
* commalessmid.py - Replaces (MySQL) instances like 'MID(A, B, C)' with 'MID(A FROM B FOR C)' counterpart
* commentbeforeparentheses.py - Prepends (inline) comment before parentheses (e.g. ( -> /**/()
* concat2concatws.py - Replaces (MySQL) instances like 'CONCAT(A, B)' with 'CONCAT_WS(MID(CHAR(0), 0, 0), A, B)' counterpart
* decentities.py - HTML encode in decimal (using code points) all characters (e.g. ' -> &#39;)
* dunion.py - Replaces instances of <int> UNION with <int>DUNION
* equaltolike.py - Replaces all occurrences of operator equal ('=') with 'LIKE' counterpart
* equaltorlike.py - Replaces all occurrences of operator equal ('=') with 'RLIKE' counterpart
* escapequotes.py - Slash escape single and double quotes (e.g. ' -> \')
* greatest.py - Replaces greater than operator ('>') with 'GREATEST' counterpart
* halfversionedmorekeywords.py - Adds (MySQL) versioned comment before each keyword
* hex2char.py - Replaces each (MySQL) 0x<hex> encoded string with equivalent CONCAT(CHAR(),...) counterpart
* hexentities.py - HTML encode in hexadecimal (using code points) all characters (e.g. ' -> &#x31;)
* htmlencode.py - HTML encode (using code points) all non-alphanumeric characters (e.g. ' -> &#39;)
* if2case.py - Replaces instances like 'IF(A, B, C)' with 'CASE WHEN (A) THEN (B) ELSE (C) END' counterpart
* ifnull2casewhenisnull.py - Replaces instances like 'IFNULL(A, B)' with 'CASE WHEN ISNULL(A) THEN (B) ELSE (A) END' counterpart
* ifnull2ifisnull.py - Replaces instances like 'IFNULL(A, B)' with 'IF(ISNULL(A), B, A)' counterpart
* informationschemacomment.py - Add an inline comment (/**/) to the end of all occurrences of (MySQL) "information_schema" identifier
* least.py - Replaces greater than operator ('>') with 'LEAST' counterpart
* lowercase.py - Replaces each keyword character with lower case value (e.g. SELECT -> select)
* luanginx.py - LUA-Nginx WAFs Bypass (e.g. Cloudflare)
* misunion.py - Replaces instances of UNION with -.1UNION
* modsecurityversioned.py - Embraces complete query with (MySQL) versioned comment
* modsecurityzeroversioned.py - Embraces complete query with (MySQL) zero-versioned comment
* multiplespaces.py - Adds multiple spaces (' ') around SQL keywords
* ord2ascii.py - Replaces ORD() occurences with equivalent ASCII() calls
* overlongutf8.py - Converts all (non-alphanum) characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. ' -> %C0%A7)
* overlongutf8more.py - Converts all characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. SELECT -> %C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94)
* percentage.py - Adds a percentage sign ('%') infront of each character (e.g. SELECT -> %S%E%L%E%C%T)
* plus2concat.py - Replaces plus operator ('+') with (MsSQL) function CONCAT() counterpart
* plus2fnconcat.py - Replaces plus operator ('+') with (MsSQL) ODBC function {fn CONCAT()} counterpart
* randomcase.py - Replaces each keyword character with random case value (e.g. SELECT -> SEleCt)
* randomcomments.py - Add random inline comments inside SQL keywords (e.g. SELECT -> S/**/E/**/LECT)
* schemasplit.py - Splits FROM schema identifiers (e.g. 'testdb.users') with whitespace (e.g. 'testdb 9.e.users')
* scientific.py - Abuses MySQL scientific notation
* sleep2getlock.py - Replaces instances like 'SLEEP(5)' with (e.g.) "GET_LOCK('ETgP',5)"
* sp_password.py - Appends (MsSQL) function 'sp_password' to the end of the payload for automatic obfuscation from DBMS logs
* space2comment.py - Replaces space character (' ') with comments '/**/'
* space2dash.py - Replaces space character (' ') with a dash comment ('--') followed by a random string and a new line ('\n')
* space2hash.py - Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
* space2morecomment.py - Replaces (MySQL) instances of space character (' ') with comments '/**_**/'
* space2morehash.py - Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
* space2mssqlblank.py - Replaces (MsSQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
* space2mssqlhash.py - Replaces space character (' ') with a pound character ('#') followed by a new line ('\n')
* space2mysqlblank.py - Replaces (MySQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
* space2mysqldash.py - Replaces space character (' ') with a dash comment ('--') followed by a new line ('\n')
* space2plus.py - Replaces space character (' ') with plus ('+')
* space2randomblank.py - Replaces space character (' ') with a random blank character from a valid set of alternate characters
* substring2leftright.py - Replaces PostgreSQL SUBSTRING with LEFT and RIGHT
* symboliclogical.py - Replaces AND and OR logical operators with their symbolic counterparts (&& and ||)
* unionalltounion.py - Replaces instances of UNION ALL SELECT with UNION SELECT counterpart
* unmagicquotes.py - Replaces quote character (') with a multi-byte combo %BF%27 together with generic comment at the end (to make it work)
* uppercase.py - Replaces each keyword character with upper case value (e.g. select -> SELECT)
* varnish.py - Appends a HTTP header 'X-originating-IP' to bypass Varnish Firewall
* versionedkeywords.py - Encloses each non-function keyword with (MySQL) versioned comment
* versionedmorekeywords.py - Encloses each keyword with (MySQL) versioned comment
* xforwardedfor.py - Append a fake HTTP header 'X-Forwarded-For' (and alike)
```

# 中文

```
0eunion.py - 将 <int> UNION 替换为 <int>e0UNION
apostrophemask.py - 将单引号字符（'）替换为其UTF-8全角对应字符（例如 ' -> %EF%BC%87）
apostrophenullencode.py - 将单引号字符（'）替换为其非法的双Unicode对应字符（例如 ' -> %00%27）
appendnullbyte.py - 在Payload末尾添加（Access）NULL字节字符（%00）
base64encode.py - 对给定Payload中的所有字符进行Base64编码
between.py - 将大于运算符（'>'）替换为 'NOT BETWEEN 0 AND #'，将等于运算符（'='）替换为 'BETWEEN # AND #'。
binary.py - 在可能的情况下注入关键字binary
bluecoat.py - 将SQL语句后的空格字符替换为有效的随机空白字符。然后将字符“=”替换为操作符LIKE。
chardoubleencode.py - 对给定Payload中的所有字符进行双URL编码（不处理已经编码的内容）（例如SELECT -> %2553%2545%254C%2545%2543%2554）
charencode.py - 对给定Payload中的所有字符进行URL编码（不处理已经编码的内容）（例如SELECT -> %53%45%4C%45%43%54）
charunicodeencode.py - 对给定Payload中的所有字符进行Unicode-URL编码（不处理已经编码的内容）（例如SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054）
charunicodeescape.py - 在给定的负载中Unicode转义非编码字符（不处理已经编码的内容）（例如SELECT -> \u0053\u0045\u004C\u0045\u0043\u0054）
commalesslimit.py - 将（MySQL）实例如'LIMIT M，N'替换为'LIMIT N OFFSET M'对应项
commalessmid.py - 将（MySQL）实例如'MID（A，B，C）'替换为'MID（A FROM B FOR C）'对应项
commentbeforeparentheses.py - 在括号（例如（））前添加（内联）注释（例如（-> / ** /（））
concat2concatws.py - 将（MySQL）实例如'CONCAT（A，B）'替换为'CONCAT_WS（MID（CHAR（0），0，0），A，B）'对应项
decentities.py - 使用代码点将所有字符进行HTML十进制编码（例如'-> '）
dunion.py - 将<int> UNION替换为<int>DUNION
equaltolike.py - 将等于运算符（'='）的所有出现替换为LIKE对应项
equaltorlike.py - 将等于运算符（'='）的所有出现替换为RLIKE对应项
escapequotes.py - 反斜杠转义单引号和双引号（例如'->\ '）
greatest.py - 将大于运算符（'>'）替换为GREATEST对应项
halfversionedmorekeywords.py - 在每个关键字之前添加（MySQL）有版本的注释
hex2char.py - 将每个（MySQL）0x <hex>编码的字符串替换为等效的CONCAT（CHAR（），...）对应项
hexentities.py - 使用代码点将所有字符进行HTML十六进制编码（例如'-> 1）
htmlencode.py - 使用代码点将所有非字母数字字符进行HTML编码（例如'-> '）
if2case.py - 将实例如'IF（A，B，C）'替换为'CASE WHEN（A）THEN（B）ELSE（C）END'对应项
ifnull2casewhenisnull.py - 将实例如'IFNULL（A，B）'替换为'CASE WHEN ISNULL（A）THEN（B）ELSE（A）END'对应项
ifnull2ifisnull.py - 将实例如'IFNULL（A，B）'替换为'IF（ISNULL（A），B，A）'对应项
informationschemacomment.py - 在（MySQL）“information_schema”标识符的所有出现之后添加内联注释（/ ** /）
least.py - 将大于运算符（'>'）替换为LEAST对应项
lowercase.py - 将每个关键字字符替换为小写值（例如SELECT-> select）
luanginx.py - LUA-Nginx WAFs绕过（例如Cloudflare）
misunion.py - 将UNION实例替换为-.1UNION
modsecurityversioned.py - 使用（MySQL）有版本的注释括起来完整的查询
modsecurityzeroversioned.py - 使用（MySQL）零版本的注释括起来完整的查询
multiplespaces.py - 在SQL关键字周围添加多个空格（' '）
ord2ascii.py - 将ORD（）出现替换为等效的ASCII（）调用
overlongutf8.py - 将给定负载中的所有（非字母数字）字符转换为过长的UTF8（不处理已经编码的内容）（例如'->%C0%A7）
overlongutf8more.py - 将给定负载中的所有字符转换为过长的UTF8（不处理已经编码的内容）（例如SELECT->%C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94）
percentage.py - 在每个字符（例如SELECT->%S%E%L%E%C%T）前面添加一个百分比符号（'％'）
plus2concat.py - 将加号运算符（'+'）替换为（MsSQL）函数CONCAT（）对应项
plus2fnconcat.py - 将加号运算符（'+'）替换为（MsSQL）ODBC函数{fn CONCAT（）}对应项
randomcase.py - 将每个关键字字符替换为随机情况值（例如SELECT->SEleCt）
randomcomments.py - 在SQL关键字中添加随机内联注释（例如SELECT->S / ** / E / ** / LECT）
schemasplit.py - 将FROM模式标识符（例如'testdb.users'）与空格（例如'testdb 9.e.users'）拆分
scientific.py - 滥用MySQL的科学计数法
sleep2getlock.py - 将实例如'SLEEP（5）'替换为“GET_LOCK（'ETgP'，5）”之类的内容
sp_password.py - 将（MsSQL）函数'sp_password'附加到有效负载的末尾，以自动混淆来自DBMS日志的内容
space2comment.py - 将空格字符（' '）替换为注释'/ ** /'
space2dash.py - 将空格字符（' '）替换为破折号注释（'--'）后跟随一个随机字符串和一个新行（'\n'）
space2hash.py - 将（MySQL）空格字符（' '）的实例替换为井字符（'#'），后跟随一个随机字符串和一个新行（'\n'）
space2morecomment.py - 将（MySQL）空格字符（' '）的实例替换为注释'/ _ /'
space2morehash.py - 将（MySQL）空格字符（' '）的实例替换为井字符（'#'），后跟随一个随机字符串和一个新行（'\n'）
space2mssqlblank.py - 将（MsSQL）空格字符（' '）的实例替换为来自有效备选字符集的随机空白字符
space2mssqlhash.py - 将空格字符（' '）替换为井字符（'#'），后跟随一个新行（'\n'）
space2mysqlblank.py - 将（MySQL）空格字符（' '）的实例替换为来自有效备选字符集的随机空白字符
space2mysqldash.py - 将空格字符（' '）替换为破折号注释（'--'）后跟随一个新行（'\n'）
space2plus.py - 将空格字符（' '）替换为加号（'+'）
space2randomblank.py - 将空格字符（' '）替换为来自有效备选字符集的随机空白字符
substring2leftright.py - 将PostgreSQL SUBSTRING替换为LEFT和RIGHT
symboliclogical.py - 将AND和OR逻辑运算符替换为其符号对应项（&&和||）
unionalltounion.py - 将UNION ALL SELECT实例替换为UNION SELECT对应项
unmagicquotes.py - 将引号字符（'）替换为多字节组合%BF%27，同时在末尾添加通用注释（使其起作用）
uppercase.py - 将每个关键字字符替换为大写值（例如select->SELECT）
varnish.py - 添加HTTP头'X-originating-IP'以绕过Varnish防火墙
versionedkeywords.py - 使用（MySQL）有版本的注释括起来每个非函数关键字
versionedmorekeywords.py - 使用（MySQL）有版本的注释括起来每个关键字
xforwardedfor.py - 添加假HTTP头'X-Forwarded-For'（等等）
```

# 后记

小 Tips : 在对 mssql 数据时,不要使用 randomcomments !
  
有时候合理组合使用这些 tamper 可以大大提高我们发现
[SQL 注入](//mrxn.net/tag/sql注入 "SQL 注入")
的机率.本文为笔记系列.
  
如有不妥之处或不错的 tamper ,欢迎指出交流.

* 标签：
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  sqlmap](https://mrxn.net/tag/sqlmap)

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
[sqlmap 最新版系统自带 tamper 解释中文翻译](https://mrxn.net/jswz/sqlmap-tamper.html)
  
文章链接：
<https://mrxn.net/jswz/sqlmap-tamper.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sqlmap-tamper.html"),
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
text: encodeURI("https://mrxn.net/jswz/sqlmap-tamper.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});