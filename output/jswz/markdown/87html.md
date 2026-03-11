---
title: "HTML语言学习教程——HTML语言剖析"
source: https://mrxn.net/jswz/87.html
---

# HTML语言学习教程——HTML语言剖析

[Mrxn](https://mrxn.net/author/1)* 发表于2014/8/21 11:45
* 8073浏览
* [0评论](#comment)
* 63小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| |  |  |  |  | | --- | --- | --- | --- | | |  |  |  | | --- | --- | --- | | |  |  | | --- | --- | | |  | | --- | | HTML语言学习教程——HTML语言剖析（献给不懂HTML的朋友）  目 录  1、HTML语言剖析之Html简介  2、HTML语言剖析之HTML标记一览  3、HTML语言剖析之文件标记  4、HTML语言剖析之排版标记  5、HTML语言剖析之字体标记  6、HTML语言剖析之清单标记  7、HTML语言剖析之表格标记  8、HTML语言剖析之表单标记  9、HTML语言剖析之图形标记  10、HTML语言剖析之链接标记  11、HTML语言剖析之多媒体标记  12、HTML语言剖析之其他标记  13、HTML语言剖析之特殊字符  14、HTML语言剖析之调色原理    1、 HTML语言剖析之Html简介  全写： HyperText Mark-up Language  译名： 超文件注标式语言（译名之一）  简释：一种为普通文件中某些字句加上标示的语言，其目的在于运用标记（tag）使文件达到预期的显示效果。  HTML 是在 SGML 定义下的一个描述性语言，或可说 HTML 是 SGML 的一个应用程式，HTML 不是程式语言，如 C++ 和 Java 之类，它只是标示语言，基本上你只要明白了各种 标记的用法便算学懂了 HTML，HTML 的格式非常简单，只是由文字及标记组合而成，于 编辑方面，任何文字编辑器都可以，只要能将文件另存成 ASCII 纯文字格式即可，当然 以专业的网页编辑软件为佳。  ■ 阅读须知：  这一篇【HTML剖析】偏重于标记的介绍，考虑到易懂及每节的篇幅问题，我并不按 W3C 的 HTML 分类，这可令你更易选择有兴趣的标记，其中只有【文件标记】是必读的，其余可任意选择。这一篇不会提及任何网页编辑软件，只要掌握了 HTML ，任何网页 编辑工具都可以变成一把利器。  ■ 标记写法：  任何标记皆由"<"及">"所围住，如 <P>  标记名与小于号之间不能留有空白字符。  某些标记　要加上参数，某些则不必。如 <font size="+2">Hello</font>  参数只可加于起始标记中。  在起始标记之标记名前加上符号"/"便是其终结标记，如 </font>  标记字母大小写皆可。  ■ 围堵标记与空标记：  标记按型态分为围堵标记与空标记  围堵标记  顾名思义，它以起始标记及终结标记将文字围住，令其达到预期显示效果。  例如 HTML Source ： <b>Creation of Webpage</b> is my favourite.  显示成： Creation of Webpage is my favourite.  其中 <b></b> 便称为围堵标记。  它以起始标记<b>及终结标记</b>标示文字 Creation of webpage ，令它显示成粗体，两者失其一都会发生错误显示。  空标记  是指标记单独出现，只有起始标记没有终结标记。  例如 HTML Source：  I love Creation of Webpage.<br>It's a wonderful place.  显示成：  I love Creation of Webpage.  It's a wonderful place.  其中换行标记<br>便属空标记。  它的作用便是将标记后所有东西显示于下一行，可见终结标记于它是没意义的， 但有些人会为空标记加上终结标记，这是为方便记认而己，对 HTML 没有影响。        2、HTML语言剖析之HTML标记一览  标记 类型 译名或意义 作 用 备注  文件标记  <HTML> ● 文件声明 让浏览器知道这是 HTML 文件  <HEAD> ● 开头 提供文件整体资讯  <TITLE> ● 标题 定义文件标题，将显示于浏览顶端  <BODY> ● 本文 设计文件格式及内文所在  排版标记  <!--注解--> ○ 说明标记 为文件加上说明，但不被显示  <P> ○ 段落标记 为字、画、表格等之间留一空白行  <BR> ○ 换行标记 令字、画、表格等显示于下一行  <HR> ○ 水平线 插入一条水平线  <CENTER> ● 居中 令字、画、表格等显示于中间 反对  <PRE> ● 预设格式 令文件按照原始码的排列方式显示  <DIV> ● 区隔标记 设定字、画、表格等的摆放位置  <NOBR> ● 不折行 令文字不因太长而绕行  <WBR> ● 建议折行 预设折行部位  字体标记  <STRONG> ● 加重语气 产生字体加粗 Bold 的效果  <B> ● 粗体标记 产生字体加粗的效果  <EM> ● 强调标记 字体出现斜体效果  <I> ● 斜体标记 字体出现斜体效果  <TT> ● 打字字体 Courier字体，字母宽度相同  <U> ● 加上底线 加上底线 反对  <H1> ● 一级标题标记 变粗变大加宽，程度与级数反比  <H2> ● 二级标题标记 将字体变粗变大加宽  <H3> ● 三级标题标记 将字体变粗变大加宽  <H4> ● 四级标题标记 将字体变粗变大加宽  <H5> ● 五级标题标记 将字体变粗变大加宽  <H6> ● 六级标题标记 将字体变粗变大加宽  <FONT> ● 字形标记 设定字形、大小、颜色 反对  <BASEFONT> ○ 基准字形标记 设定所有字形、大小、颜色 反对  <BIG> ● 字体加大 令字体稍为加大  <SMALL> ● 字体缩细 令字体稍为缩细  <STRIKE> ● 画线删除 为字体加一删除线 反对  <CODE> ● 程式码 字体稍为加宽如<TT>  <KBD> ● 键盘字 字体稍为加宽，单一空白  <SAMP> ● 范例 字体稍为加宽如<TT>  <VAR> ● 变数 斜体效果  <CITE> ● 传记引述 斜体效果  <BLOCKQUOTE> ● 引述文字区块 缩排字体  <DFN> ● 述语定义 斜体效果  <ADDRESS> ● 地址标记 斜体效果  <SUB> ● 下标字 下标字  <SUP> ● 上标字 指数（平方、立方等）  清单标记  <OL> ● 顺序清单 清单项目将以数字、字母顺序排列  <UL> ● 无序清单 清单项目将以圆点排列  <LI> ○ 清单项目 每一标记标示一项清单项目  <MENU> ● 选单清单 清单项目将以圆点排列，如<UL> 反对  <DIR> ● 目录清单 清单项目将以圆点排列，如<UL> 反对  <DL> ● 定义清单 清单分两层出现  <DT> ○ 定义条目 标示该项定义的标题  <DD> ○ 定义内容 标示定义内容  表格标记  <TABLE> ● 表格标记 设定该表格的各项参数  <CAPTION> ● 表格标题 做成一打通列以填入表格标题  <TR> ● 表格列 设定该表格的列  <TD> ● 表格栏 设定该表格的栏  <TH> ● 表格标头 相等于<TD>，但其内之字体会变粗  表单标记  <FORM> ● 表单标记 决定单一表单的运作模式  <TEXTAREA> ● 文字区块 提供文字方盒以输入较大量文字  <INPUT> ○ 输入标记 决定输入形式  <SELECT> ● 选择标记 建立 pop-up 卷动清单  <OPTION> ○ 选项 每一标记标示一个选项  图形标记  <IMG> ○ 图形标记 用以插入图形及设定图形属性  连结标记  <A> ● 连结标记 加入连结  <BASE> ○ 基准标记 可将相对 URL 转绝对及指定连结目标  框架标记  <FRAMESET> ● 框架设定 设定框架  <FRAME> ○ 框窗设定 设定框窗  <IFRAME> ○ 页内框架 于网页中间插入框架 IE  <NOFRAMES> ● 不支援框架 设定当浏览器不支援框架时的提示  影像地图  <MAP> ● 影像地图名称 设定影像地图名称  <AREA> ○ 连结区域 设定各连结区域  多媒体  <BGSOUND> ○ 背景声音 于背景播放声音或音乐 IE  <EMBED> ○ 多媒体 加入声音、音乐或影像  其他标记  <MARQUEE> ● 走动文字 令文字左右走动 IE  <BLINK> ● 闪烁文字 闪烁文字 NC  <ISINDEX> ○ 页内寻找器 可输入关键字寻找于该一页 反对  <META> ○ 开头定义 让浏览器知道这是 HTML 文件  <LINK> ○ 关系定义 定义该文件与其他 URL 的关系  StyleSheet  <STYLE> ● 样式表 控制网页版面  <span> ● 自订标记 独立使用或与样式表同用  注：  ● 表示该标记属围堵标记，即需要关闭标记如 </标记>。  ○ 表示该标记属空标记，即不需要关闭标记。  IE 表示该标记只适用于 Internet Explorer。  NC 表示该标记只适用于 Netscape Communicator。  反对 表示该标记不为 W3C 所赞同，通常这标记是 IE 或 NC 自订，且己为众所支 持，只是 HTML 标准中有其它同功能或更好的选择。  弃用 表示该标记己为 W3C 所弃用，是过时的标记，但 HTML 具向下兼容的特 性，不用担心新浏览器不支援旧标记。  新 表示该标记是 HTML 4.0 中新增的。        3、HTML语言剖析之文件标记  <HTML> ； <HEAD> ； <TITLE> ； <BODY>  欲明白本篇【HTML剖析】之标记分类请看 【标记一览】。  亦请先明白围堵标记与空标记的分别请看 【HTML概念】。  ■ HTML 基本架构：  以下 HTML Source Code 便是一份 HTML 文件的基本架构：  <HTML>  <HEAD>  <TITLE> 网页的标题 </TITLE>  </HEAD>  <BODY>  网页的内容，很多标记都作用于此  </BODY>  </HTML>  特点解说：  整份文件处于标记<HTML>与</HTML>之间。  <HTML>用以声明这是 HTML 文件，让浏览器认出并正确处理此 HTML 文件。  文件分两部分，由<HEAD>至</HEAD>称为开头，<BODY>至</BODY>称本文。  基本上两者各有适用的标记，如<TITLE>只可出现于开头部分。  开头部分用以存载重要资讯，而只有本文部分会被显示。  所以大部分标记会运用于本文部分。  <TITLE>所标示的是文件的标题。  会出现于浏览器顶部及为别人 Bookmark 时的名称，所以每页有不同而明确的标题 是需要的。  上述标记中只有<BODY>具参数设定。  ■ <BODY> 之参数设定：  例子：  <BODY text="#000000" link="#0000FF" alink="#FF0000" vlink="#0000FF" background="bg1.gif" bgcolor="#FFFFFF" leftmargin=2 topmargin=2 bgproperties="fixed">  text="#000000"  用以设定文字颜色。 #000000 代表黑色，亦可以采用颜色的名称，即 text="black" 。各种颜色的值及名称可参考【调色原理】一节。  link="#0000FF"  设定一般文字连结颜色。  alink="#FF0000"  设定刚按下时文字连结颜色。  vlink="#0000FF"  设定连结后的颜色。（被按过）。  background="bg1.gif"  设定背景墙纸。GIF 或 JPEG 皆可，可以是绝对途径或相对途径。  bgcolor="#FFFFFF"  设定背景颜色。当己设定背景墙纸时会失去作用，除非墙纸有透明部分。  leftmargin=2  设定整份文件显示画面的左方边沿空间，单位为像素。 『只适用于IE』  topmargin=2  设定整份文件显示画面的上方边沿空间。 『只适用于IE』  bgproperties="fixed"  固定背景墙纸，当卷动文字时墙纸不会跟著卷动。 『只适用于IE』  标记及参数之字母大小都可以。      4、HTML语言剖析之排版标记  <!--注解--> ； <P> ； <BR> ； <HR> ； <CENTER> ； <PRE> ； <DIV> ； <NOBR> ； <WBR> ；  ■<!--注解-->： ▲Top  像很多电脑语言一样，HTML 文件亦提供注解功能。浏览器会忽略此标记中的文字（可以 是很多行）而不作显示，一般使用目的：  为文中不同部份加上说明，方便日后修改。  这对较复杂或非私人网页尤其重要，它不单是提醒自已，亦提醒你的同事这部分 做什么、那部分做什么。  例子：  <!--由这处开始是产品订购表格-->  用作版权声明。  假如你不希望别人使用或复制你的网页，可加上警告字眼。  例子：  <!--本文版权为 1998, Creation of Webpage 所拥有，未经许，请勿抄摘-->  ■ <P> ： ▲Top  <P>称为段落标记。作用：为字、画、表格等之间留一空白行。  本来<P>是一围堵标记，标于一段落的头尾，但从 HTML 2.0 开始己不需要</P>作结尾。  <P> 的常用参数： 如：<p align="center">  align="center"  可选值：right, left, center。  内定值： align="left"  例子： 原始码 Here is the text for my paragraph. It does't matter how long it is,  how many space are between the words or when I decide to hit the return key.  It will create a new paragraph only when I begin the tag with another one.  <P>Here's the next paragraph.  显示结果 Here is the text for my paragraph. It does't matter how long it is, how many space are between the words or when I decide to hit the return key. It will create a new paragraph only when I begin the tag with another one.  Here's the next paragraph.  ■ <BR> ： ▲Top  <BR>称为换行标记。作用：令字、画、表格等显示于下一行。  由于浏览器会自动忽略原始码中空白和换行的部分，这令到<BR>成为最常用的标记之 一。因为无论你在原始码中编好了多漂亮的文章，若不适当地加上换行标记或段落标记，浏览器只会将它显示成一大段。  错误示范：（邮局可不会接受一行过的地址） 原始码 566 E Boston Post RD  Mamaroneck NY 10543-9982  United States of America  结果 566 E Boston Post RD Mamaroneck NY 10543-9982 United States of America  正确例子： 原始码 566 E Boston Post RD  <BR>Mamaroneck NY 10543-9982  <BR>United States of America  结果 566 E Boston Post RD  Mamaroneck NY 10543-9982  United States of America  ■ <HR> ： ▲Top  <HR>称为水平线。作用：插入一条水平线。  <HR> 之参数修改：  以： <HR align="LEFT" size="2" width="70%" color="#0000FF" noshade> 为例。  align="LEFT"  设定线条置放位置，可选择：left；right；center 三种设定值。  size="2"  设定线条厚度，以像素作单位，内定为 2。  width="70%"  设定线条长度，可以是绝对值（以像素作单位）或相对值，内定为 100%。  color="#0000FF" 『只适用于IE』  设定线条颜色，内定为黑色。 #0000FF 代表蓝色，亦可以采用颜色的名称，即 text="blue" 。  noshade  设定线条为平面显示，若删去则具阴影或立体，这是内定值。  例子： 原始码 <HR>  <HR align="LEFT" size="4">  <HR align="LEFT" size="2" width="70%" color="#0000FF" noshade>  <HR align="LEFT" size="4" width="70" color="#008000">  显示结果  -------------------------------------------------------------------------------  ■ <CENTER> ： ▲Top  <CENTER>称为居中标记。作用：令字、画、表格等显示于中间。  这标记原先是 Netscape 所定义，后来其它浏览器都支持它，但你会发现很多标记已有 align="CENTER" 的参数，<CENTER>似乎多馀了，事实上它还是常用的标记之一，其简单易用，常用于文字上，对于己加有 align="CENTER" 参数的 <TABLE> 标记亦要不厌其烦 地加上居中标记，因有狻多浏览器不支持<TABLE> 标记中的 align="CENTER" 参数。  例子： 原始码 <CENTER>Chris's First Homepage</CENTER>  <CENTER>What's new</CENTER>  <CENTER>My profile</CENTER>  结果 Chris's First Homepage  What's new  My profile  ■ <PRE> ： ▲Top  <PRE>称为预设格式标记。作用：令文件按照原始码的排列方式显示。  这标记允许保留你于原始码中输入的空白及 Return。细看以下例子你便可体会到此标记的 威力。除了运用一大堆表格标记之外你只有采用这标记才能有此效果。  能以<PRE>标记产生对　效果，或产生多于一行的空白才算上乘！  例子： 原始码         <pre>        Creation of Webpage Log Analysis I  Composer Learning  459 407 480 522 547 586 673  HTML Advanced      200 268 296 358 385 453 506</pre>  显示结果                  Creation of Webpage Log Analysis I  Composer Learning  459 407 480 522 547 586 673  HTML Advanced      200 268 296 358 385 453 506  ■ <DIV> ： ▲Top  <DIV>称为区隔标记。作用：设定字、画、表格等的摆放位置。  <DIV>应用于 Style Sheet（式样表）方面会更显威力，它最终目的是给设计者另一种组织能力，有 Class ; Style ; title ; ID 等属性，将会于【Style Sheet】一节才作详述，这处只介绍 一个属性设定。  以 <DIV align="center"> 为例：  align="center"  可选值：center ; left ; right 。决定字、画、表格等居中、靠左或靠右。  <DIV align="center"> 的作用和居中标记 <CENTER>一样，前者是由 HTML3.0 开始 的标准，后者是通用己久的标示法。  例子： 原始码 <DIV align="center">Chris's First Homepage  <br>What's new  <br>My profile</DIV>  结果 Chris's First Homepage  What's new  My profile  ■ <NOBR> ： ▲Top  <NOBR>称为不折行标记。作用：令某些文字不因太长而绕行，一　显示于同一行或下一 行。它对住址、数学算式、一行数字、程式码等尤为有用。  例子：（其中 Chris's Creation of Webpage 将不被分开而显示于同一行。）码 If you want to know how to create you own homepage quickly, don't miss <NOBR>Chris's Creation of Webpage</NOBR> which will help you a lot.  结果 If you want to know how to create you own homepage quickly, don't miss Chris's Creation of Webpage which will help you a lot.  ■ <WBR> ： ▲Top  <WBR>称为建议折行标记。作用：预设折行部位。  它没有侵犯到 <BR> 的责任，只是作建议而已，若观者的系统解像度够高的话，那么它是不会折行的。  例子：（若不加<WBR>标记，整个网址会显示于下一行。） 原始码 Please visit my other homepage which locate at <http://www.geocities.com/SiliconValley/> <WBR>Sector/8234/index.html There are many softwares for download. I think you will really love that place.  结果 Please visit my other homepage which locate at <http://www.geocities.com/SiliconValley/Sector/8234/index.html> There are many softwares for download. I think you will really love that place.      5、HTML语言剖析之字体标记  <STRONG> <B>  <I> <EM> <VAR> <CITE> <DFN> <ADDRESS>  <TT> <SAMP> <CODE> <KBD> <U> <STRIKE> <BIG> <SMALL> <SUP> <SUB>  <H1> <H2> <H3> <H4> <H5> <H6>  <FONT> <BASEFONT>  ■实体标记与逻辑标记 ： ▲Top  这一节【字体标记】你必须先明白实体标记与逻辑标记的分别，否则你会迷惑于为何不同 的标记却有相同的效果。两者分别有以下两处：  实体标记有固定的显示效果，逻辑标记则依不同浏览器而不同。  例如逻辑标记的 <EM> 由于浏览器的不同它所标示的文字不一定出现斜体效果， 它可能是加底线、粗体或反白等，所以这一节是以它们在 IE 和 NC 中的效果作介 绍。  多个实体标记亦可有效标示同一字句，逻辑标记则通常于旧浏览器不能有效显示多 重的标示。  例如两个逻辑标记 <EM> 及 <STRONG> 同时标示一字句于旧浏览器常失去作用。  实体标记有：  <I> <B> <U>  逻辑标记有：  <STRONG> <EM> <VAR> <CITE> <DFN> <ADDRESS> <CODE> <KBO> <SAMP> <TT>  若要求真确的效果当然以实体标记为佳。  ■<STRONG> <B> ： ▲Top  两者皆能产生字体加粗的效果，但必须注意的是当文件被设为 gb2312 Encoding 时，两者所标示的中文字不会于 Netscape Netvigator 显示粗体效果。  例子： （第一行是没有任何字体标记的，作对照之用） HTML Source Code （原始码）浏览器显示结果  Creation of Webpage  <br><STRONG>Creation of Webpage</STRONG>  <br><B>Creation of Webpage</B>  Creation of Webpage  Creation of Webpage  Creation of Webpage  ■<I> <EM> <VAR> <CITE> <DFN> <ADDRESS>： ▲Top  这些标记于 Internet Explorer 都产生斜体效果，而只有 </DFN> 于 Netscape Netvigator 失去作用。这些标记中只有 <ADDRESS> 较为特别，因它包括换行效果所以不必在它前面加上 <BR> 标记。  例子： HTML Source Code （原始码） 浏览器显示结果  <I>Creation of Webpage</I>  <br><EM>Creation of Webpage</EM>  <br><VAR>Creation of Webpage</VAR>  <br><CITE>Creation of Webpage</CITE>  <br><DFN>Creation of Webpage</DFN>  <ADDRESS>Creation of Webpage</ADDRESS>  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  ■<TT> <SAMP> <CODE> <KBD> <U> <STRIKE> <BIG> <SMALL> <SUP> <SUB> ▲Top  为方便对照及记认，所以把十个标记于在一起介绍。  <TT> <SAMP> <CODE> <KBD> 可令每字母有相等宽度且每字母之间的距离稍为加 宽。但于 NC 不见得如此。  <U> 是加底线的标记，一些特别的浏览器并不支援，因顾虑到与连结混淆。  <STRIKE> 加上删除线的标记。  <BIG> 令字体加大。  <SMALL> 令字体变细。  <SUB> 为下标字， <SUP> 则为上标字，仅剩的数学标记。  例子： （第一行是没有任何字体标记的，作对照之用） HTML Source Code （原始码）浏览器显示结果  Creation of Webpage  <br><TT>Creation of Webpage</TT>  <br><SAMP>Creation of Webpage</SAMP>  <br><CODE>Creation of Webpage</CODE>  <br><KBD>Creation of Webpage</KBD>  <br><U>Creation of Webpage</U>  <br><STRIKE>Creation of Webpage</STRIKE>  <br><BIG>Creation of Webpage</BIG>  <br><SMALL>Creation of Webpage</SMALL>  <br>12345<SUB>7</SUB> 6789<SUP>9</SUP>  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  Creation of Webpage  123457 67899  ■<H1> <H2> <H3> <H4> <H5> <H6>： ▲Top  这些是标题标记，由 <H1> 至 <H6> 变粗变大加宽的程度逐渐减小。每个标题标记所标示 的字句将独占一行且上下留一空白行。  例子： 原始码 <H1>Header Level 1</H1>  <H2>Header Level 2</H2>  <H3>Header Level 3</H3>  <H4>Header Level 4</H4>  <H5>Header Level 5</H5>  <H6>Header Level 6</H6>  显示结果 Header Level 1  Header Level 2  Header Level 3  Header Level 4  Header Level 5  Header Level 6  ■<FONT> <BASEFONT>： ▲Top  这一节只有这两个标记具参数设定，且两者的参数设定是一样的，都是负责设定文字的大 小、字形及颜色，但各有用处，且看以下比较：  <BASEFONT> 可以用于文件的开头部分，即 <HEAD> 与 </HEAD> 之间的位置，将 影响全文字句，是一个空标记，用以改变字体显示的内定值。  <FONT> 是应用于文件的内文部分，即 <BODY> 与 </BODY> 之间的位置，只影响 所标示的字句，是一个围堵标记。  两标记可同时存在，唯没被 <FONT> 所标示的字句才直接受 <BASEFONT> 所影 响，而 <FONT> 本身亦受 <BASEFONT> 的影响。  <FONT>的参数设定：  例子： <font face="Arial" size="+2" color="#008000">Creation of Webpage</font>  face="Arial"  设定文字的字形。Arial 是常用的一种，请不要使用 Window 内建字 形以外的字形。于没有设定为 Gb2312 Encoding 的中文网页，Netscape Netvigator 不会显示此标记 所指明的任何中文字形。  size="+2"  设定文字的大小。其值可以是绝对或相对，  绝对的意思便是标记自己决定文字的大小，不受 <BASEFONT> 的影响，如  size="5" 表示其大小便是 5， 而html内定值为 3，即 size="3"和没有设定是一样的。  相对的意思便是在内定值 3 的基础上增加或减少大小级数，如 size="+2" 便等同绝 对表示法的 size="5"，但若已设定 <BASEFONT size="n"> 则其实际大小便是 n+2 不 再是 3+2 了。<BASEFONT>只有绝对表示法。  color="#008000"  设定文字的颜色。#008000 表示绿色  例子： 原始码 <font size="+1">I love Creation of Webpage</font>  <br><font size="+2" color="#800080">I love Creation of Webpage</font>  <br><font face="Times New Roman" size="5" color="#008000">I love Creation of Webpage</font>  显示结果 I love Creation of Webpage  I love Creation of Webpage  I love Creation of Webpage      6、HTML语言剖析之清单标记  <OL> <LI>  <UL>  <MENU> <DIR>  <DL> <DT> <DD>  ■ <OL> <LI> :  <OL>称为顺序清单标记。<LI>则用以标示清单项目。  所谓顺序清单就是在每一项前面加上 1,2,3... 等数目，又称编号清单。  <OL> 的参数设定（常用）：  例如： <ol type="i" start="4"></ol>  type="i"  设定数目款式，其值有五种，请参考 右表，内定为 type="1"。  start="4"  设定开始数目，不论设定了哪一数 目款式，其值只能是 1,2,3.. 等整 数，内定为 start="1"。  Type Numbering style  1 arabic numbers 1, 2, 3, ...  a lower alpha a, b, c, ...  A upper alpha A, B, C, ...  i lower roman i, ii, iii, ...  I upper roman I, II, III, ...  <LI> 的参数设定（常用）：  例如： <li type="square" value="4">  type="square"  只适用于非顺序清单，设定符号款式，其值有三种，如下，内定为 type="disc"：  符号  是当 type="disc" 时的列项符号。  符号  if" width=10 height=10 border=0> 是当 type="circle" 时的列项符号。  符号  是当 type="square" 时的列项符号。  value="4"  只适用于顺序清单，设定该一项的数目，其後各项将以此作为起始数目而递增， 但前面各项则不受影响，其值只能是 1,2,3.. 等整数，没有内定值。  例子： HTML Source Code （原始码） 浏览器显示结果  My best friends:  <ol>  <li>Michelle Wei  <li>Michael Wan  <li>Gloria Lam  </ol>  My best friends:  Michelle Wei  Michael Wan  Gloria Lam  ■ <UL> ：  <UL>称为无序清单标记。  所谓无序清单就是在每一项前面加上 、、 等符号，故又称符号清单。  <UL> 的参数设定（常用）：  例如： <UL type="square">  type="square"  设定符号款式，其值有三种，如下，内定为 type="disc"：  符号  是当 type="disc" 时的列项符号。  符号  是当 type="circle" 时的列项符号。  符号  是当 type="square" 时的列项符号。  注意：由于 <UL> 及 <LI> 都有 type 这个参数，两者尽可能选用其一。  例子： HTML Source Code （原始码） 浏览器显示结果  My Homepages:  <ul>  <li>Penpals Garden  <li>ICQ Garden  <li>Software City  <li>Creation of Webpage  </ul>  My Homepages:  Penpals Garden  ICQ Garden  Software City  Creation of Webpage  ■ <MENU> <DIR> ：  这两个标记都不为 W3C 所赞同，希望用者能以 <ul> 及 <ol> 代之。  <MENU> 及 <DIR>，基本上它和 <ul> 是一样的，在一些特别的浏览器可能表现出 <ol> 的效果，于旧版的 IE 或 NC 标记 <DIR> 不显示符号或数目。两标记的用法与 <ul> 完全一样。  例子： HTML Source Code （原始码） 浏览器显示结果  My Homepages:  <dir>  <li>Penpals Garden  <li>ICQ Garden  <li>Software City  <li>Creation of Webpage  </dir>  My Homepages:  Penpals Garden  ICQ Garden  Software City  Creation of Webpage  ■ <DL> <DT> <DD> :  <DL>称为定义清单标记。 <DT> 用以标示定义条目，<DD> 则用以标示定义内容。  所谓定义清单就是一种分二层的项目清单，其不故符号及数目。  三个标记都没有常用的参数。而 <DT> <DD> 可以独立使用，只是一些旧的浏览器并不支援，如 IE 3.0。常用的如 <DD> 标记可用以制造段落第一个字前面的空白。  例子： 原始码 <dl>  <dt>How to use Definition List  <dd>First, you should not place paragraph tag right after or before a list structure or between the items of a list. In cerntain contexts, use of extra paragraph tags should always be avoided, when you realize this concept, it is quit easy to write a HTML.  <dt>Other things to know  <dd>We usually put only ONE Definition tag following the Definition Term tag, more than one DD tag is not recommanded. Besides, unlike Definition List is a nonempty tag, both Definition Term and Definition Description are empty tags.  </dl>  显示结果 How to use Definition List  First, you should not place paragraph tag right after or before a list structure or between the items of a list. In cerntain contexts, use of extra paragraph tags should always be avoided, when you realize this concept, it is quit easy to write a HTML.  Other things to know  We usually put only ONE Definition tag following the Definition Term tag, more than one DD tag is not recommanded. Besides, unlike Definition List is a nonempty tag, both Definition Term and Definition Description are empty tags.      7、HTML语言剖析之表格标记  表格标记  <TABLE> <TR> <TD>  <TH>  <CAPTION>  ■ <TABLE> <TR> <TD> ： ▲Top  这三个标记是定义表格的最重要的标记，可以说只学这三个己足够。  <TABLE>是一个容器标记，意思是说它用以声明这是表格而且其他表格标记只能在他的 范围内才适用，属容器标记的还有其他。  <TR>用以标示表格列（row）  <TD>用以标示储存格（cell）  <TABLE> 的参数设定（常用）：  例如： <table width="400" border="1" cellspacing="2" cellpadding="2" align="CENTER" valign="TOP" background="myweb.gif" bgcolor="#0000FF" bordercolor="#FF00FF" bordercolorlight="#00FF00" bordercolordark="#00FFFF" cols="2">  width="400"  表格宽度，接受绝对值（如 80）及相对值（如 80%）。  border="1"  表格边框厚度，不同浏览器有不同的内定值，故请指明。  cellspacing="2"  表格格线厚度，请看例子三，那是加厚到 5 的格线。  cellpadding="2"  文字与格线的距离，请看例子四，那是加至 10 的 padding。  align="CENTER"  表格的摆放位置（水平），可选值为： left, right, center，请看例子五或六，那表格是放于中间的，为怕一些浏览器不支援，故特加上居中标记<CENTER>，只是多 层保证而己，当然只用<CENTER>亦可。  valign="TOP".  表格内字画等的摆放贴　位置（垂直），可选值为： top, middle, bottom。  background="myweb.gif"  表格　纸，与 bgcolor 不要同用。  bgcolor="#0000FF"  表格底色，与 background 不要同用，请看例子六。  bordercolor="#FF00FF"  表格边框颜色，NC 与 IE 有不同的效果，请看例子六。  bordercolorlight="#00FF00"  表格边框向光部分的颜色，请看例子二。『只适用于 IE』  bordercolordark="#00FFFF"  表格边框背光部分的颜色，请看例子二，使用 bordercolorlight 或 bordercolordark 时 bordercolor 将会失效。『只适用于 IE』  cols="2"  表格栏位数目，只是让浏览器在下载表格是先画出整个表格而己。  <TR> 的参数设定（常用）：  例如：<tr align="RIGHT" valign="MIDDLE" bgcolor="#0000FF" bordercolor="#FF00FF" bordercolorlight="#808080" bordercolordark="#FF0000">  align="RIGHT"  该一列内字画等的摆放贴　位置（水平），可选值为： left, center, right。  valign="MIDDLE"  该一列内字画等的摆放贴　位置（垂直），可选值为： top, middle, bottom。  bgcolor="#0000FF"  该一列底色，请看例子五。  bordercolor="#FF00FF"  该一列边框颜色，请看例子三。『只适用于 IE』  bordercolorlight="#808080"  该一列边框向光部分的颜色，请看例子三。『只适用于 IE』  bordercolordark="#FF0000"  该一列边框背光部分的颜色，请看例子三，使用 bordercolorlight 或 bordercolordark 时 bordercolor 将会失效。『只适用于 IE』  <TD> 的参数设定（常用）：  例如：<td width="48%" height="400" colspan="5" rowspan="4" align="RIGHT" valign="BOTTOM" bgcolor="#FF00FF" bordercolor="#808080" bordercolorlight="#FF0000" bordercolordark="#00FF00" background="myweb.gif">  width="48%"  该一储存格宽度，接受绝对值（如 80）及相对值（如 80%）。  height="400"  该一储存格高度。  colspan="5"  该一储存格向右打通的栏数。请看例子六  rowspan="4"  该一储存格向下打通的列数。请看例子六  align="RIGHT"  该一储存格内字画等的摆放贴　位置（水平），可选值为： left, center, right。  valign="BOTTOM"  该一储存格内字画等的摆放贴　位置（垂直），可选值为： top, middle, bottom。  bgcolor="#FF00FF"  该一储存格底色，请看例子四。  bordercolor="#808080"  该一储存格边框颜色，请看例子三。『只适用于 IE』  bordercolorlight="#FF0000"  该一储存格边框向光部分的颜色，请看例子三。『只适用于 IE』  bordercolordark="#00FF00"  该一储存格边框背光部分的颜色，请看例子三，使用 bordercolorlight 或 bordercolordark 时 bordercolor 将会失效。『只适用于 IE』  background="myweb.gif"  该一储存格　纸，与 bgcolor 任用其一。  例子一： 原始码 <table width="60%" border="1">  <tr><td>只有一个储存格（cell）的表格</td></tr>  </table>  显示结果   只有一个储存格（cell）的表格  例子二： 原始码 <table width="60%" border="0" bordercolorlight="#FF00FF" bordercolordark="#FF0000">  <tr><td>第一列第一栏</td><td>第一列第二栏</td></tr>  </table>  显示结果   第一列第一栏 第一列第二栏  例子三： 原始码 <table width="60%" border="0" cellspacing="5">  <tr bordercolor="#0000FF">  <td>第一列第一栏</td>  <td>第一列第二栏</td>  </tr>  <tr bordercolorlight="#FF00FF" bordercolordark="#00FF00">  <td>第二列第一栏</td>  <td>第二列第二栏</td>  </tr>  </table>  显示结果   第一列第一栏 第一列第二栏  第二列第一栏 第二列第二栏  例子四： 原始码 <table width="60%" border="0" cellpadding="10">  <tr>  <td bgcolor="#FFCCE6">第一列第一栏</td>  <td bgcolor="#FFFFC6">第一列第二栏</td>  </tr>  <tr>  <td bgcolor="#FFD9FF">第二列第一栏</td>  <td bgcolor="#DAB4B4">第二列第二栏</td>  </tr>  </table>  显示结果   第一列第一栏 第一列第二栏  第二列第一栏 第二列第二栏  例子五： 原始码 <center>  <table width="60%" cellspacing="0" cellpadding="2" align="CENTER">  <tr>  <td bgcolor="#FFD2E9">第一列第一栏</td>  <td bgcolor="#FFDAB5">第一列第二栏</td>  <td bgcolor="#FFFFB5">第一列第三栏</td>  </tr>  <tr bgcolor="#C0C0C0">  <td>第二列第一栏</td>  <td>第二列第二栏</td>  <td>第二列第三栏</td>  </tr>  </table>  </center>  显示结果  第一列第一栏 第一列第二栏 第一列第三栏  第二列第一栏 第二列第二栏 第二列第三栏  例子六 原始码 <center>  <table width="350" border="1" cellspacing="0" cellpadding="2" align="CENTER" bgcolor="#FFC4E1" bordercolor="#0000FF">  <tr>  <td>第一列第一栏</td>  <td colspan="2">第一列 之 第二栏及第三栏</td>  </tr>  <tr>  <td rowspan="2">第二列及第三列 之 第一栏</td>  <td>第二列第二栏</td>  <td>第二列第三栏</td>  </tr>  <tr>  <td>第三列第二栏</td>  <td>第三列第三栏</td>  </tr>  </table>  </center>  显示结果  第一列第一栏 第一列 之 第二栏及第三栏  第二列及第三列 之 第一栏 第二列第二栏 第二列第三栏  第三列第二栏 第三列第三栏  ■ <TH> ： ▲Top  <TH>与<TD>同样是标示一个储存格，唯一不同的是<TH>所标示的储存格中的文字是以粗 体出现，通常用于表格第一列以标示栏目。它的用法是取代<TD>的位置便可以，其参数 设定请参考<TD>。  当然若为<TD>所标示的储存格中的文字加上粗体标记<B>便等如<TH>的效果。  例子： 原始码 <center>  <table width="350" border="1" cellspacing="0" cellpadding="2" align="CENTER">  <tr align="CENTER">  <th>Month</th><th>% of IE visitor</th><th>% of NC visitor</th>  </tr>  <tr align="CENTER">  <td>August</td><td>61%</td><td>39%</td>  </tr>  <tr align="CENTER">  <td>July</td><td>54%</td><td>46%</td>  </tr>  <tr align="CENTER">  <td>June</td><td>52%</td><td>48%</td>  </tr>  </table>  </center>  显示结果  Month % of IE visitor % of NC visitor  August 61% 39%  July 54% 46%  June 52% 48%  ■ <CAPTION> ： ▲Top  <CAPTION> 的作用是为表格标示一个标题列，有如在表格上方加上一没格线的打通列。 当然亦可置于下方，通常用以存放该表格的标题。  <CAPTION> 的参数设定（常用）：  例如：<caption align="TOP" valign="TOP"></caption>  align="TOP"  该表格标题列相对于表格的摆放贴　位置（水平），可选值为： left, center, right, top, middle, bottom，若 align="bottom" 的话标题列便会出现对表格的下方，不管你的原始码中把 <caption> 放在 <table> 中的头部或尾部。  valign="TOP"  该表格标题列相对于表格的摆放位置（上下），可选值为： top, bottom。和 align="TOP" 或 align="BOTTOM" 是一样的，虽然功能重复了，但如果你要标题列 置于下方及向右或向左贴　，那末两个参数便可一　用了。当只　一个参数时， 请首选 align，因为 valign 是由 HTML 3.0 才开始的参数。  例子： 原始码 <center>  <table width="350" border="1" cellspacing="0" cellpadding="2" align="CENTER">  <caption>网页速成 八月份访客浏览器使用分析</caption>  <tr align="CENTER">  <th>Month</th>  <th>% of IE visitor</th>  <th>% of NC visitor</th>  </tr>  <tr align="CENTER">  <td>August</td>  <td>61%</td>  <td>39%</td>  </tr>  </table>  </center>  显示结果  网页速成 八月份访客浏览器使用分析 Month % of IE visitor % of NC visitor  August 61% 39%      8。1、HTML语言剖析之表单标记 -1  <FORM> <INPUT>  INPUT 的种类： Text, Radio,Checkbox, Password, Submit/Reset, Image, File, Hidden, Button。  <SELECT> <OPTION>  <TEXTAREA>  ■ 引子  表单的用处很多，于网上无处不见，当然是配合 CGI 使用为佳，所以馈下有意使用或学 习 CGI 的话，表单设计见必需的，这一节介绍的标记不多，但其参数变化很多。一份表单的基本架构是：在 <FORM> 标记 的包围下加上一种或以上的表单输入方式及一个或以上的按键。  ■<FORM> <INPUT> ：  <FORM>称为表单标记，用以宣告此为表单模式，属于一个容器标记，表示其它表单标记需要在它的包围中才有效，<INPUT>便是其中的一个，用以设定各种输入资料的方法。它 是一个空标记。  <FORM> 的参数设定（常用）：  例如： <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  action="http://your.isp.com/cgi-local/example.cgi"  表单通常是与 CGI 配合使用的，参数 action 便是用以指明该 CGI 程式的位置，这 样此表单所填的资料才能正确传给 CGI 作处理。若馈下没有 CGI 以进行测试，可 设定此参数为 ACTION="mailto: [[email protected]](/cdn-cgi/l/email-protection) " 那样该表单所填的资料将会寄至 此电邮地址（红色部分）。  method="POST"  传送资料给 CGI 的的方式，可选值为 POST, GET。你只需记住POST容许传送大量资料，但 GET则只接受低于 1K 的资 料，所以你若看过别人的表单原始码的话，你会发现申请表单用的是POST 而搜找器用的是 GET。  <INPUT> 的参数设定（常用）：  由于其第一个参数 type 己有很多的选择，而不同的选择表示出不同的输入方式，且其它 参数亦因此而异，故以下将独立介绍不同输入方式及其它参数设定。  type="Text"  可选值为 Text, Radio,Checkbox, Password, Submit/Reset, Image, File, Hidden, Button。  --------------------------------------------------------------------------------  输入方式一： Text （单行文字盒）  例如<input type="Text" name="age" value="20" align="MIDDLE" size="2" maxlength="255">  type="Text"  输入方式为 Text，能产生一单行文字盒，上限为 255 字元。  name="age"  此一单行文字盒名称，这是最重要的一个，方便 CGI 辨认由表单传来的资料，虽 说可随便命名，但通常 CGI 程式中都有指定名称，若转用其它名称便需要修改该 CGI 程式了，名称可为没空白没特别符号的英文或数字，有大小写的分别，可以写成 Your\_Age，若有访客于此表单此一文字盒填入 40 的话，那末传给 CGI 的字 串便是 Your\_Age=40。  value="20"  此一单行文字盒内定值。若不填写则文字盒是空白的，等待访客亲自键入，若 value="20" 的话， 20 便会出现在文字盒中，当然访客可以修改之。  align="MIDDLE"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle. 没太大有处。  size="2"  此一单行文字盒显示的长度，若馈下是采用 Big5 编码的中文网页便要小心，同 size 的文字盒 NC 会显示得比 IE 狻长。  maxlength="255"  此一单行文字盒可输入字元的上限，为方便编排资料或避免错输入等，宜设定上 限，例如输入电话或 ICQ UIN 的可设为 8，年龄为 2 等。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  请填入电话号码：<input type="Text" name="phone" value="" size="10" maxlength="8">  </form>  显示结果 请填入电话号码：  --------------------------------------------------------------------------------  输入方式二： Radio （单一选择）  例如：<input type="Radio" name="gender" value="female" align="MIDDLE" checked>  type="Radio"  输入方式为 Radio，能产生一单一选择，以供点选。  name="gender"  此一 Radio 名称，参考 Text 部分的说明。  value="female"  内定值。每一个 radio 必须及仅有一个 value，通常有同时采用两个或以上同 name 不同 value 的 Radio 输入方式，可让使用使任选其一。  align="MIDDLE"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle。  checked  设该 Radio 为内定被选。同 name 的各个 Radio 中只能有一个使用，或全不使用这 参数。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  请选性别：  <input type="Radio" name="gender" value="Female">女性  <input type="Radio" name="gender" value="Male" checked>男性  <br>你喜欢吗：  <input type="Radio" name="like" value="Yes">喜欢  <input type="Radio" name="like" value="No">不喜欢  <input type="Radio" name="like" value="NotSure">不肯定  </form>  显示结果 请选性别：  女性  男性  你喜欢吗：  喜欢  不喜欢  不肯定  --------------------------------------------------------------------------------  输入方式三： Checkbox （确认盒）  例如：<input type="Checkbox" name="idol" value="Leon" align="RIGHT" checked>  type="Checkbox"  输入方式为 Checkbox，能产生一确认盒，以供剔选。  name="idol"  此一 Checkbox 名称，参考 Text 部分的说明。  value="Leon"  内定值。每一个 Checkbox 必须及仅有一个 value，当被剔选时这值便会传及 CGI，例如所传字串 idol=Leon 。  align="RIGHT"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle。  checked  设该 Checkbox 为内定被选。每个 Checkbox 都是独立的，所以每一个都可使用这参数，不像 Radio。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  你喜欢以下那些明星：  <br><input type="Checkbox" name="idol01" value="Leon">黎明  <input type="Checkbox" name="idol02" value="Noriko\_Sagai">酒井法子  <input type="Checkbox" name="idol03" value="Leon">郑秀文  <input type="Checkbox" name="idol04" value="BonJovi" checked>BonJovi  </form>  显示结果 你喜欢以下那些明星：  黎明  酒井法子  郑秀文  BonJovi  --------------------------------------------------------------------------------  输入方式四： Password （密码输方盒）  例如：<input type="Password" name="pw" value="999" align="MIDDLE" size="5" maxlength="9">  Password 的其他参数和 Text 是完全相同的，请参考 Text 的介绍。  两者作用不同，Password 所输入的字元全以 \* 号表示。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  请输入姓名：<input type="Text" name="name">  <br>请输入密码：<input type="Password" name="pw" maxlength="9">  </form>  显示结果 请输入姓名：  请输入密码：  --------------------------------------------------------------------------------  输入方式五： Submit （传送键）及 Reset （清除键）  这是表单上重要的两个按键，两者所附带的参数相同，但用处不大。  例如：<input type="Submit" name="other\_funtion" value="确定" align="MIDDLE">  <input type="Reset" value="清除" align="MIDDLE">  type="Submit"  设定输入方式为 Submit 或 Reset。  name="other\_funtion"  Submit 的功能随 name 的不同而不同，须和 CGI 配合。若你只需要普通的传送键，则是其内定，不必用此参数。  value="确定"  这个值不是输给 CGI 的，而是显示在按键上，可以不用，传送键的内定值为 Submit Query，清除键的内定值为 Reset。  align="MIDDLE"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  <input type="Submit"><input type="Reset">  <br><input type="Submit" value="         确定         "><input type="Reset" value="清除">  </form>  显示结果      8。2、HTML语言剖析之表单标记 -2  --------------------------------------------------------------------------------  输入方式六： Image （图片按键）  这通常用以取代 Submit 及 Reset 两个按键，因为由程式产生的按键并不漂亮，这 Image 参 数便容许你采用自已制造的按键。  例如：<input type="Image" name="submit" align="BOTTOM" src="ex\_icon.gif">  type="Image"  输入方式为 Image。  name="submit"  所要代表的按键，可以是 submit, reset, 或其它。  align="BOTTOM"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle。  src="ex\_icon.gif"  按键图片来源，若此图片文件不与该 html 文件在同一目录下，请加上相对或绝对途 径。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  <input type="Image" name="submit" align="BOTTOM" src="ex\_icon.gif">  </form>  显示结果  --------------------------------------------------------------------------------  输入方式七： File  例如：<input type="File" name="upload" align="BOTTOM" size="20" maxlength="100" accept="text/html">  input type="File"  输入方式为 Image。通常用以传输文件。  name="upload"  这文件传输的名称，用以识别之用。  align="BOTTOM"  可选值：top, middle, bottom, left, right, texttop, baseline, absmiddle。  size="20"  所显示文字盒的长度。  maxlength="100"  可输入字元的上限。  accept="text/html"  所接受的文件类别，有二十六种选择，但可不设定。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  <type="File" name="upload" size="30" maxlength="100" accept="text/html">  </form>  显示结果  --------------------------------------------------------------------------------  输入方式八： Hidden  例如：<input type="Hidden" name="ID" value="6618">  type="Hidden"  输入方式为隐藏或内定。它不会显示任何输入介面，而是一个内定值随表单一起 传给 CGI，列如由 CGI 产生的会员号码，或传入可更改的参数以调整 CGI 而避免 修改 CGI 程式码。  name="ID"  这文件传输的名称，用以识别之用。  value="6618"  内定值，会以如 ID=6618 形式传给 CGI。  例子： （"Hidden" 是不被显示的，所以这处多放了一个 "Submit" 键，表示 Hidden 之内定 值会随 submit 键被按而传给 CGI） 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  <input type="Hidden" name="ID" value="6618">  <input type="Submit" value="Submit">  </form>  显示结果  --------------------------------------------------------------------------------  输入方式九： Button  例如：<input type="Button" name="useless" value="Back">  type="Button"  输入方式为一般按键。常配合 Java Script 作为其启动按键。  name="useless"  这文件传输的名称，用处不大。  value="Back"  按键显示名称。  例子： 其中 onclick="history.go( -1 );return true; 属 JAVA 事件。 原始码 <form>  <input type="Button" value="回前一页" onclick="history.go( -1 );return true;">  </form>  显示结果  ■ <SELECT> <OPTION> ：  <SELECT>是卷动选单标记，每一选项皆由 <OPTION> 所标示，把它当作围堵标记或空标记使用都可以。  <SELECT> 的参数设定（常用）：  例如： <select name="where" size="6" multiple>  name="where"  这卷动选单的名称，作识别之用，将会传及 CGI。  size="6"  这卷动选单的列数，即其高度，请自行修改。若使用此参数则不会有 Pop Up 效 果。  multiple  令这卷动选单容许多重选择。  <OPTION> 的参数设定（常用）：  例如： <option value="tw" selected>  value="tw"  这选项的值，将会传及 CGI。请自行修改，但不同选项必须有不同的值。  selected  设该选项为内定被选。一个单选卷动选单只能有一项或零可内定被选。  例子一： （普通 POP UP 卷动选单） 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST"> Where you com from?  <select name="where">  <option value="hk">Hong Kong</option>  <option value="tw" selected>Taiwan</option>  <option value="cn">China</option>  <option value="us">United States</option>  <option value="ca">Canada</option>  </select>  </form>  显示结果 Where you com from?  Hong Kong Taiwan China United States Canada  例子二： （容许多重选择 的卷动选单） 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST"> Where you com from?  <select name="where" multiple>  <option value="hk">Hong Kong</option>  <option value="tw" selected>Taiwan</option>  <option value="cn">China</option>  <option value="us">United States</option>  <option value="ca">Canada</option>  </select>  </form>  显示结果 Where you com from?  Hong Kong Taiwan China United States Canada  例子三：（设定了 Size 的卷动选单） 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST"> Where you com from?  <select name="where" size="5">  <option value="hk">Hong Kong</option>  <option value="tw" selected>Taiwan</option>  <option value="cn">China</option>  <option value="us">United States</option>  <option value="ca">Canada</option>  </select>  </form>  显示结果 Where you com from?  Hong Kong Taiwan China United States Canada  ■ <TEXTAREA> ：  <TEXTAREA>是表单文字区块标记，常用于 bug report, feedback 等需要填写大量资料的用途。  <TEXTAREA> 的参数设定（常用）：  例如： <textarea name="comments" cols="40" rows="4" wrap="VIRTUAL">  name="comments"  这文字区块的名称，作识别之用，将会传及 CGI。  cols="40"  这文字区块的宽度，请自行修改。  rows="4"  这文字区块的列数，即其高度，请自行修改。  wrap="VIRTUAL"  设定其折行问题，可选值为： off, physical, virtual。off 表示不使用此属性，physical 时则会强迫刘览器在送资料到 CGI（Web 伺服器端）必须将实№文字中的换行一并送出，设为 virtual 时则送出连续成串的字（除非使用者按了键盘的 RETURN / ENTER）。  例子： 原始码 <form action="http://your.isp.com/cgi-local/example.cgi" method="POST">  Give comments:  <textarea name="comments" cols="40" rows="4" wrap="VIRTUAL">  这是预设的字句，通常留空的，随你喜欢。</textarea>  </form>  显示结果 Give comments:  这是预设的字句，通常留空的，随你喜欢。      9、HTML语言剖析之图形标记    ■ <IMG> ：  <IMG> 称图形标记，主要用以插入图片于网页中，至于其它用处如配合影片文件等的播 放及影像地图（Image Map 或称一图多连结）则于不会在这节提及，请看【影像地图】及 【其他标记】。  <IMG> 的一般参数设定：  例如 <img src="logo.gif" width=100 height=100 hspace=5 vspace=5 border=2 align="top" alt="Logo of PenPals Garden" lowsrc="pre\_logo.gif">  src="logo.gif"  图片来源，接受 .gif, .jpg 及 .png 格式，前两者通行己久，后者由 96 年开始发展， 于未来取代前两者。若图片文件与该 html 文件同处一目录则只　写上文件案名称，否则必须加上正确的途径，相对及绝对皆可。  width=100 height=100  设定图片大小，此宽度、及高度一般采用 pixels 作单位。通常只设为图片的真实 大小以免失真，若　要改变图片大小最好事先使用图像编辑工具。  hspace=5 vspace=5  设定图片边沿空白，以免文字或其它图片过于贴近。hspace 是设定图片左右的空 间，vspace 则是设定图片上下的空间，高度采用 pixels 作单位。  border=2  图片边框厚度。  align="top"  调整图片旁边文字的位置，你可以控制文字出现在图片的偏上方、中间、底端、 左右等，可选值：top, middle, bottom, left, right，内定为 botom。Netscape 还支持 texttop, baseline, absmiddle, absbottom，  texttop 表示图片和文字依顶线对　，  baseline 表示图片对　到目前文字行底线值，  absmiddle 表示图片对　到目前文字行绝对中央，  absbottom 表示图片对　到目前文字行绝对底部，（绝对底部意指它考虑到比方 y 、g、q 等字的下缘）。  alt="Logo of PenPal Garden"  这是用以描述该图形的文字，若用者使用文字浏览器，由于不支持图片，这些文 字更会代替图片而被显示。若于支持图片显示的浏览器，当鼠标移至图片上该些 文字亦会显示。  lowsrc="pre\_logo.gif"  设定先显示低解像图片，若所加入的是一张很大的图片，下载　时很长，这张低 解像图片会先被显示以免浏览失却兴趣，通当是原图片灰阶版本。  例子一： 原始码 <img src="girl.gif" width=100 height=112 border=0 alt="beautiful girl"> 普通插入  显示结果  普通插入  例子二： 原始码 <img src="girl.gif" width=100 height=112 border=0 alt="beautiful" hspace=10 vspace=20"> 设定上下左右空白位置  显示结果  设定上下左右空白位置  例子三： 原始码 <img src="girl.gif" width=100 height=112 border=4 alt="beautiful" hspace=10 vspace=20"> 设定上下左右空白位置  显示结果  设定字画中间对　，边框厚度为 4。  例子四： 原始码 <img src="girl.gif" width=100 height=112 alt="beautiful lady" align="right" border=0> 设定图片靠右。  显示结果  设定图片靠右。  例子五： 原始码 <img src="girl.gif" width=200 height=220 alt="I'm not beautiful right now" border=0> 放大了的图片  显示结果  放大了的图片      10、HTML语言剖析之链接标记  <A>  <BASE>  ■ <A> ： ▲Top  <A> 称连结标记，由 <A> 与 </A> 所围的文字、图片等等可以成为一个连结。  <A> 的一般参数设定：  例如 <a href="index.html" name="hello" target="\_top">  href="index.html"  这参数不能与另一参数 name 同时使用，使用这参数才能造成可按的连结。  当作为一外部连结时： href 所设定的是该连结所要连到的文件名称，若 该文件与此 html 档不是同在一目录请加上适当的路径，相对绝对皆可。  当作为一内部连结时： href 所设定的是该连结所要连到的同文件内参考 点或指定文件之参考点，且不　要包围任何字画只　加上结束标示 </a>便 可以，例如 <a href="#there"></a> 、 <a href="index.html#there"></a> 及 <a href="http://www.school.net.hk/~chris55/index.html#there"></a> 其中 there 便 是参考点，并　於其前加上符号 # 以作识别，参考点由下一个参数 name 事先於文件中埋下。  name="hello"  这参数是为文件埋下参考点，作为被连结，不会被显示。所以说造成一个内部连 结　要使用两次 <A> 连结标记。一个使用参数 name 事先於文件中埋下一参考 点，另一个使用参数 href 连到这个参考点。  target="\_top"  设定连结被按後之结果所要显示的视窗。可选值为： \_blank, \_parent, \_self, \_top, 框窗名称。  target="框窗名称"  这只运用於框架中，若被设定则连结结果将显示於该“框窗名称”之框窗中，框窗名称是事先由框架标记所命名。  target="\_blank" 或 target="new"  将连结的画面内容，开在新的浏览视窗中。  target="\_parent"  将连结的画面内容，当成文件的上一个画面。  target="\_self"  将连结的画面内容，显示在目前的视窗中。(内定值)  target="\_top"  将框架中连结的画面内容，显示在没有框架的视窗中。（即除去了框架)  例子一：（外部连结） 原始码 <a href="../promote/engines.html">四百五十个寻找引擎</a>  <p><a href="http://www.hkseek.com/icq">  <img src="link\_image.gif" width=99 height=44 border=1 alt="ICQ Garden"></a>  <p><a href="http://www.hkseek.com/icq">  <img src="link\_image.gif" width=99 height=44 border=0 alt="ICQ Garden"></a>  显示结果 四百五十个寻找引擎  例子二（内部连结）：请到 PenPal Garden 的 FAQ Page 刻体验一下何为内部连结。 原始码 <a name="test"></a>  <a href="#test">本页的内部连结</a>  <br><a href="http://www.school.net.hk/~chi/faq.html#14">跳到 PenPal Garden 的 FAQ 部分</a>  显示结果 本页的内部连结  跳到 PenPal Garden 的 FAQ 部分  ■ <BASE> ： ▲Top  <BASE> 是一个连结基准标记，用以改变文件中所有连结标记的参数内定值。它只能应用 於文件的开头部分，即标记 <HEAD> 与 </HEAD> 之间。  <BASE> 的一般参数设定：  例如 <base href="http://www.microsoft.com/" target="\_top">  href="http://www.microsoft.com/"  设定该页网页中所有 HTTP 文件及图形（包括相对路径连结及 <IMG> 图形标记 等）的内定路径，其他如 ftp:// 及 gopher:// 等则不受影响。这参数只可填入一个相 对或绝对的路径，不必填入档案名称。一般相对路径连结及 <IMG> 图形标记等是 内定以该页网页所在的目录作为起点，若依这例子，该文件中所有连结将会以 <http://www.microsoft.com/> 作为起点，若其中有连结如 <a href="index.html">Back to Main Page</a> ，那末它不会连到自已目录下的 index.html，它将会连到 Microsoft 的 首页，这是因为相对路径己给 <BASE> 转成绝对的了。  target="\_top"  设定该页网页中所有连结被按後之结果所要显示的视窗，免得分别为所有连结加 上 target 参数，常应用於框架中。其设定与 <A> 连结标记中 target 参数相同。  例子容後再写，你可亲自尝试或到一些以框架制作的网页去体验一下。      11、HTML语言剖析之多媒体标记  <BGSOUND>  <EMBED>  ■ <BGSOUND>：  <BGSOUND> 是用以插入背景音乐，但只适用於 IE，其参数设定不多。如下  <BGSOUND src="your.mid" autostart=true loop=infinite>  src="your.mid"  设定 midi 档案及路径，可以是相对或绝对。  autostart=true  是否在音乐档传完之後，就自动播放音乐。true 是，false 否 (内定值)。  loop=infinite  是否自动反覆播放。LOOP=2 表示重复两次，Infinite 表示重复多次。  ■ <EMBED>：  <EMBED> 是用以插入各种多媒体，格式可以是 Midi、Wav、AIFF、AU 等等，Netscape 及 新版的 IE 都支援。其参数设定狻多。如下  <EMBED src="your.mid" autostart="true" loop="true" hidden="true">  src="your.mid"  设定 midi 档案及路径，可以是相对或绝对。  autostart=true  是否在音乐档传完之後，就自动播放音乐。true 是，false 否 (内定值)。  loop="true"  是否自动反覆播放。LOOP=2 表示重复两次，true 是， false 否。  HIDDEN="true"  是否完全隐藏控制画面，true 为是，no 为否 (内定)。  STARTTIME="分:秒"  设定歌曲开始播放的时间。如 STARTTIME="00:30" 表示从第30秒处开始播放。  VOLUME="0-100"  设定量的大小，数值是0到100之间。内定则为使用者系统本身之设定。  WIDTH="整数" 和 HIGH="整数"  设定控制画面的宽度和高度。(若 HIDDEN="no")  ALIGN="center"  设定控制画面和旁边文字的对　方式，其值可以是 top、bottom、center、baseline、 left、right、texttop、middle、absmiddle、absbottom。  CONTROLS="smallconsole"  设定控制画面的外貌。预设值是 console。  console 一般正常的面板  smallconsole 较小的面板  playbutton 只显示播放按钮  pausecutton 只显示暂停按钮  stopbutton 只显示停止按钮  volumelever 只显示音量调整钮      12、HTML语言剖析之其他标记  <MARQUEE>  <BLINK>  <ISINDEX>  <META>  <LINK>  ■ <MARQUEE>：  <MARQUEE> 只适用於 IE ，译为「跑马灯」如 Status Bar 的那种，意指走动或卷动的 文字，其参数设定狻多。我先举些例子，然後再列出各参数。  例子一： 原始码 <marquee width=150>I'm a small MARQUEE</marquee>  显示结果 I'm a small MARQUEE  例子二： 原始码 <marquee behavior=slide>This is a slide effect</marquee>  显示结果 This is a slide effect  例子三： 原始码 <marquee behavior=alternate>撞来撞去，啊！我昏啦</marquee>  显示结果 撞来撞去，啊！我昏啦  例子四： 原始码 <marquee scrolldelay=5 scrollamount=50>哗！！太快了，我又昏啦</marquee>  显示结果 哗！！太快了，我又昏啦  <marquee behavior="SCROLL" direction="LEFT" bgcolor="#0000FF" height="30" width="150" hspace="0" vspace="0" loop="INFINITE" scrollamount="30" scrolldelay="500">Hello</marquee>  behavior="SCROLL"  决定文字的卷动方式，可选值为：  SCROLL 一般卷动，是内定值。  SLIDE 如幻灯片，一格格的，效果是文字一接触左边便全部消失。  ALTERNATE 文字向左右两边撞来撞去。  direction="LEFT"  设定文字的卷动方向，LEFT 表示向左，是内定值，RIGHT 表示向右。  bgcolor="#0000FF"  设定文字卷动范围的背景颜色。  height="30" width="150"  >设定文字卷动范围，可采用相对或绝对，如 30% 或 30 等，单位为像素。  hspace="0" vspace="0"  设定文字的水平及垂直空白位置。  loop="INFINITE"  设定文字卷动次数，其值可以是正整数或 INFINITE，INFINITE 是内定值，表示无 限次。  scrollamount="30"  每「格」文字之间的间隔，单位是像素。  scrolldelay="500"  文字卷动的停顿时间，单位是毫秒。  ■ <BLINK> ： ▲Top  <BLINK> 是令文字闪烁，只适用於 NC，用法直接，没有参数。看看例子便知：  例子： 原始码 <blink>我是天上星，闪又闪</blink>  显示结果 我是天上星，闪又闪  ■ <ISINDEX> ： ▲Top  <ISINDEX> 可让某些 Web Server 找寻网页内的关键字，假如你的 Web Server 提供这样的 找寻功能，使用者的浏览器也支援这些找寻功能，那堋，载入网页时就会看到一个简单的 找寻方块。其用法直接，没有参数，本来是要放於 <HEAD> 标记内的，但把它放在 <BODY> 标记内亦不见有问题，请记住，3W 以反对此标记。  例子： 原始码 <isindex>  显示结果  ■ <META> ： ▲Top  <META> 是放於 <HEAD> 与 </HEAD>之间的标记，功用与变化等对，所以我公式化地介 绍。  <meta name="Description" content="This is Chris's Home Page">  该网页的描述，作用於寻找引擎的登录  <meta name="Keywords" content="Chris, Web, Music, photo">  该网页的关键字，作用於寻找引擎的登录  <meta http-equiv="Expires" content="Tue, 09 Dec 1997 00:00:00 GMT">  <meta http-equiv="Pragma" content="no-cache">  以上行功能相同，都是要浏览器重新载入该页，不要使用快取档案，当然可以修 改该 Expire 时间。  <meta http-equiv="Content-Type" content="text/html; charset=big5">  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">  设定这是 HTML 文件及其编码语系，中文网页请使用 big5 那行，或者不设编码亦 可，纯英文网页建议使用 iso-8859-1。  <meta name="GENERATOR" content="Mozilla/4.04 [en] (Win95; I) [Netscape]">  <meta name="GENERATOR" content="Microsoft FrontPage 3.0">  这只表示该网页由甚堋编辑器写成。  <meta http-equiv="refresh" content="10; url=http://www.hkiwc.com">  这一行较为实用，能於预定秒数内自动转到指定的网址。原始码中 10 表示 10秒。  ■ <LINK> ： ▲Top  <LINK> 用来将目前文件与其它 URL 作连结，但不会有连结按钮，用於 <HEAD> 标记间， 格式如下：  <link href="URL" rel="relationship">  <link href="URL" rev="relationship">  其用法我们会於 Style Sheet 一节详细介绍。      13、HTML语言剖析之特殊字符  只要你认识了 HTML 标记，你便会知道特殊字符的用处。 HTML 原始码 显示结果 描述  &lt; < 小於号或显示标记  &gt; > 大於号或显示标记  & & 可用於显示其它特殊字符  " " 引号  ® ? 己注册  © ? 版权  &8482; ? 商标  半方大的空白&8194;  全方大的空白&8195;  不断行的空白  ■ ISO Latin-1 特殊字符 ：  HTML 原始码 显示结果 描述  &AElig; ? Uppercase AE diphthing  Á á Uppercase A, acute accent  Â ? Uppercase A, circumflex accent  À à Uppercase A, grave accent  Å ? Uppercase A, ring  Ã ? Uppercase A, tilde  Ä ? Uppercase A, dieresis or umlaut mark  Ç ? Uppercase C, cedilla  &ETH; D Uppercase Eth, Icelandic  É é Uppercase E, acute accent  Ê ê Uppercase E, circumflex accent  È è Uppercase E, grave accent  Ë ? Uppercase E, dieresis or umlaut mark  Í í Uppercase I, acute accent  Î ? Uppercase I, circumflex accent  Ì ì Uppercase I, grave accent  Ï ? Uppercase I, dieresis or umlaut mark  Ñ ? Uppercase N, tilde  Ó ó Uppercase O, acute accent  Ô ? Uppercase O, circumflex accent  Ò ò Uppercase O, grave accent  Ø ? Uppercase O, slash  Õ ? Uppercase O, tilde  Ö ? Uppercase O, dieresis or umlaut mark  &THORN; T Uppercase THORN, Icelandic  Ú ú Uppercase U, acute accent  Û ? Uppercase U, circumflex accent  Ù ù Uppercase u, grave accent  Ü ü Uppercase U, dieresis or umlaut mark  Ý Y Uppercase Y, acute accent  æ ? Lowercase ae diphthing  á á Lowercase a, acute accent  â a Lowercase a, circumflex accent  à à Lowercase a, grave accent  å ? Lowercase a, ring  ã ? Lowercase a, tilde  ä ? Lowercase a, dieresis or umlaut mark  ç ? Lowercase c, cedilla  ð e Lowercase eth, Icelandic  é é Lowercase e, acute accent  ê ê Lowercase e, circumflex accent  è è Lowercase e, grave accent  ë ? Lowercase e, dieresis or umlaut mark  í í Lowercase i, acute accent  î ? Lowercase i, circumflex accent  ì ì Lowercase i, grave accent  ï ? Lowercase i, dieresis or umlaut mark  ñ ? Lowercase n, tilde  ó ó Lowercase o, acute accent  ô ? Lowercase o, circumflex accent  ò ò Lowercase o, grave accent  ø ? Lowercase o, slash  õ ? Lowercase o, tilde  ö ? Lowercase o, dieresis or umlaut mark  ß ? Lowercase sharp s, German (sz ligature)  þ t Lowercase thorn, Icelandic  ú ú Lowercase u, acute accent  û ? Lowercase u, circumflex accent  ù ù Lowercase u, grave accent  ü ü Lowercase u, dieresis or umlaut mark  ý y Lowercase y, acute accent  ÿ ? Lowercase y, dieresis or umlaut mark      14、HTML语言剖析之调色原理  HTML 的颜色表示可分两种：  以命名方式定义常用的颜色，如 RED。  以 RGB 值表示，如 #FF0000 表示 red。  命名方式涵括的色种不多亦不甚方便，较少采用，以下介绍 RGB 值的原理：  众所皆知颜色是由 "red" "green" "blue" 三原色组合而成的，在 HTML 中对於彩度的定义是 采十六进位的，对於三原色 HTML 分别给予两个十六进位去定义，也就是每个原色可有 256 种彩度，故此三原色可混合成一千六佰多万的颜色。  例如  白色的组成是 red=ff, green=ff, blue=ff, RGB 值即为 ffffff  红色的组成是 red=ff, green=00, blue=00, RGB 值即为 ff0000  绿色的组成是 red=00, green=ff, blue=00, RGB 值即为 00ff00  蓝色的组成是 red=00, green=00, blue=ff, RGB 值即为 0000ff  黑色的组成是 red=00, green=00, blue=00, RGB 值即为 000000  於应用时常在每个 RGB 值之前加上符号 # 以示分别，但不加亦可。  ■ HTML 基本架构：  选按不同颜色按键以测试前景颜色效果 (只适合 Internet Explorer)    选按不同颜色按键以测试背景颜色效果    或输入一个 RGB 颜色码或名称    ■ 16 常用颜色表：  Color Value Name   Color Value Name  #00FFFF aqua     #808080 gray  #000080 navy     #C0C0C0 silver  #000000 black     #008000 green  #808000 olive     #008080 teal  #0000FF blue     #00FF00 lime  #800080 purple     #FFFF00 yellow  #FF00FF fuchsia     #800000 maroon  #FF0000 red     #FFFFFF white  ■ 其它常用颜色表：  Color Value Name   Color Value Name  #F0F8FF aliceblue     #A00000 antiquewith  #7FFFD4 aquamarine     #F0FFFF azure  #F5F5DC beige     #FFE4C4 bisque  #000000 black     #FFEBCD blanchedalmond  #0000FF blue     #8A2BE2 blueviolet  #A52A2A brown     #DEB887 burlywood  #5F9EA0 cadetblue     #7FFF00 chartreuse  #D2691E chocolate     #FF7F50 coral  #C0F000 cornfloewrblue     #FFF8DC cornsilk  #00FFFF cyan     #00008B darkblue  #008B8B darkcyan     #B8860B darkgoldenrod  #A9A9A9 darkgray     #006400 darkgreen  #DA0000 darkhaki     #8B008B darkmagenta  #556B2F darkolivegreen     #DA000E darkorenge  #9932CC darkorchid     #8B0000 darkred  #E9967A darksalmon     #8FBC8F darkseagreen  #483D8B darkslateblue     #2F4F4F darkslategray  #00CED1 darkturquoise     #9400D3 darkviolet  #FF1493 deeppink     #00BFFF deepskyblue  #696969 dimgray     #1E90FF dodgerblue  #B22222 firebrick     #FFFAF0 floralwhite  #228B22 forestgreen     #DCDCDC gainsboro  #00000E gostwhite     #FFD700 gold  #00E00D golenrod     #808080 gray  #008000 green     #ADFF2F greenyellow  #F0FFF0 honeydew     #FF69B4 hotpink  #CD5C5C indianred     #FFFFF0 ivory  #F0E68C khaki     #E6E6FA lavender  #FFF0F5 lavenderblush     #7CFC00 lawngreen  #FFFACD lemonchiffon     #ADD8E6 lightblue  #F08080 lightcoral     #E0FFFF lightcyan  #0000E0 lightgodenrod     #0000E0 lightgodenrodyellow  #0000A0 lightgray     #90EE90 lightgreen  #FFB6C1 lightpink     #FFA07A lightsalmon  #20B2AA lightseagreen     #87CEFA lightskyblue  #0000EB lightslateblue     #778899 lightslategray  #B0C4DE lightsteelblue     #FFFFE0 lightyellow  #32CD32 limegreen     #FAF0E6 linen  #FF00FF magenta     #800000 maroon  #66CDAA mediumaquamarine     #0000CD mediumblue  #BA55D3 mediumorchid     #ED0000 mediumpurpul  #3CB371 mediumseagreen     #7B68EE mediumslateblue  #00FA9A mediumspringgreen     #48D1CC mediumturquoise  #C71585 mediumvioletred     #191970 midnightblue  #F5FFFA mintcream     #FFE4E1 mistyrose  #FFE4B5 moccasin     #FFDEAD navajowhite  #000080 navy     #A0B0E0 navyblue  #FDF5E6 oldlace     #6B8E23 olivedrab  #FFA500 orange     #0E0EED orengered  #DA70D6 orchid     #A00D00 palegodenrod  #98FB98 palegreen     #AFEEEE paleturquoise  #DB7093 palevioletred     #FFEFD5 papayawhip  #FFDAB9 peachpuff     #CD853F peru  #FFC0CB pink     #DDA0DD plum  #B0E0E6 powderblue     #800080 purple  #FF0000 red     #BC8F8F rosybrown  #4169E1 royalblue     #8B4513 saddlebrown  #FA8072 salmon     #F4A460 sandybrown  #2E8B57 seagreen     #FFF5EE seashell  #A0522D sienna     #87CEEB skyblue  #6A5ACD slateblue     #708090 slategray  #FFFAFA snow     #00FF7F springgreen  #4682B4 steelblue     #D2B48C tan  #D8BFD8 thistle     #FF6347 tomato  #40E0D0 turquoise     #EE82EE violet  #00E0ED violetred     #F5DEB3 wheat  #000E00 hite     #F5F5F5 whitesmoke  #FFFF00 yellow     #9ACD32 yellowgreen | | | | |

* 标签：
* [#
  html](https://mrxn.net/tag/html)

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
[HTML语言学习教程——HTML语言剖析](https://mrxn.net/jswz/87.html)
  
文章链接：
<https://mrxn.net/jswz/87.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/87.html"),
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
text: encodeURI("https://mrxn.net/jswz/87.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});