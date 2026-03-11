---
title: "配合chrome浏览器console解密一段JSFuck代码[\"\x66\x69\x6c\x74\x65\x72\"]"
source: https://mrxn.net/jswz/decode-jsfuck.html
asset_dir: assets/配合chrome浏览器console解密一段jsfuck代码[x66x69x6cx74x65x72]
---

# 配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]

[Mrxn](https://mrxn.net/author/1)- 发表于2019/11/16 11:05
- 5734浏览
- [1评论](#comment)
- 23分钟阅读

深入探索

脚本

网页浏览器

软件

---

在测试某个项目的时候，发现一段[JavaScript](https://mrxn.net/tag/JavaScript)代码，省略不重要的部分如下：  
  
// 原内容如下，只知道有个正则  
  
['mmh']["\x66\x69\x6c\x74\x65\x72"]["\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72"](((['mmh'] + [])[  
  
    "\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72"]['\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65'][  
  
    '\x61\x70\x70\x6c\x79'](null,  
  
    "33s102Y117y110O99L116H105n111u110Z40g41U123u102m117c110M99m116T105y111d110" ['\x73\x70\x6c\x69\x74'](/[a-zA-Z]{1,}/))))('mmh');  
  
// 在JavaScript中对于\x66这种开头的，\x代表这是一个16进制，直接在console里面打印出来就ok  
  
// console.log('\x66\x69\x6c\x74\x65\x72') => filter  
  
// 然后依次打印所有的类似字节即可得到如下转码后的[JavaScript](https://mrxn.net/tag/JavaScript)代码  
  
// 如果你到这里不知道如何下手的话，怎么办？搜索啊！Google搜索以下 XXXX是什么 就有结果了  
  
// 或者把全部\x66这种解密后得到的相关字符串去搜索就有结果了  
  
[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-001-7ecf5319e36e.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/61fc1573873681.png)](https://mrxn.net/content/uploadfile/201911/61fc1573873681.png)  
  
// 下面看一下jsfuck对照表，然后解密  
  
// false       =>  ![]  
  
// true        =>  !![]  
  
// undefined   =>  [][[]]  
  
// NaN         =>  +[![]]  
  
// 0           =>  +[]  
  
// 1           =>  +!+[]  
  
// 2           =>  !+[]+!+[]  
  
// 10          =>  [+!+[]]+[+[]]  
  
// Array       =>  []  
  
// Number      =>  +[]  
  
// String      =>  []+[]  
  
// Boolean     =>  ![]  
  
// Function    =>  []["filter"]  
  
// eval        =>  []["filter"]["constructor"](CODE)()  
  
// window      =>  []["filter"]["constructor"]("return this")()  
  
// 解码后的代码如下，为了节省字符，使用mrxn123代替代码中的超长字符串  
  
['mmh']["filter"]["constructor"](((['mmh'] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/))))('mmh');  
  
// 根据jsfuck对照表，我们去掉mmh，这样就是熟悉的原滋原味的jsfuck格式的代码了  
  
[]["filter"]["constructor"]((([] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/))))();  
  
// 根据eval对照[]["filter"]["constructor"](CODE)()，我们只需要把code部分代码直接console.log()出来就好  
  
console.log(((([] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/)))));  
  
// 输出：{  
  
[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-002-4ed42df0c86a.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/fcf41573873681.png)](https://mrxn.net/content/uploadfile/201911/fcf41573873681.png)  
  
// 同样的姿势将开始用mrxn123替换掉的字符串替换回去，回车，OK！JavaScript源码就出现在控制台了

[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-003-54a82761d9bd.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/8fcd1573873681.png)](https://mrxn.net/content/uploadfile/201911/8fcd1573873681.png)   
注意：上面的步骤中，替换需要去掉原内容中的空格，不然会报错。

- 标签：
- [#JavaScript](https://mrxn.net/tag/JavaScript)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
