/*
******************************************
字符串函数扩展  
函数列表：
1. toFloat
2. format
3. isEmpty
4. startWith
5. endWith
6. contains
7. leftTrim
8. rightTrim
9. trim
10. left
11. right
12. middle
13. isIP
14. isLongDate
15. isShortDate                          
16. isDate
17. isMobilePhone
18. isEmail
19. isZipCode
20. isIDCard
21. isPhone
22. isFloat
23. isNumber
24. htmlEncode
25. toDate

数组函数扩展：
函数列表：
1. foreach
2. all
3. exisit
4. count
5. find
6. findIndex
7. findAll
******************************************
*/

//#region 字符串函数扩展

//#region 转换成浮点数

String.prototype.toFloat = function (place) {
    if (!(this.isNumber() || this.isFloat()))
        return this;
    var orginal = this;
    place = place || 2;
    var pointIndex = orginal.indexOf(".");
    if (-1 == pointIndex) {
        orginal += ".";
        for (var i = 0; i < place; i++)
            orginal += "0";
    }
    else
        orginal = orginal.substring(0, pointIndex + place + 1);
    return orginal;
}

//#endregion

//#region 格式化字符串

String.prototype.format = function () {
    if (0 == arguments.length)
        return this;
    var source = this;

    if (1 == arguments.length && "object" == typeof arguments[0]) {
        return str.replace(/\{([^}]+)\}/g, function ($1, $2, $3) {
            return arguments[0][$2]
        });
    }
    else {
        var args = Array.prototype.slice.call(arguments, 0);
        return source.replace(/\{(\d+)\}/g, function (m, i) {
            return undefined == args[i] ? m : args[i];
        });
    }
}

//#endregion

//#region 是否为空

String.prototype.isEmpty = function () {
    return "" == this.trim();
}

//#endregion

//#region 是否以指定字符串开头

String.prototype.startWith = function (str) {
    return 0 === this.indexOf(str);
}

//#endregion

//#region 是否以指定字符串结尾

String.prototype.endWith = function (str) {
    str = str.toString();
    return this.length - str.length === this.indexOf(str);
}

//#endregion

//#region 是否包含指定字符串

String.prototype.contains = function (str) {
    return -1 !== this.indexOf(str);
}

//#endregion

//#region 去除左边的空格

String.prototype.leftTrim = function () {
    return this.replace(/(^\s*)/g, "");
}

//#endregion

//#region 去除右边的空格

String.prototype.rightTrim = function () {
    return this.replace(/(\s*$)/g, "");
}

//#endregion

//#region 去除前后空格

String.prototype.trim = function () {
    return this.replace(/(^\s*)|(\s*$)/g, "");
}

//#endregion

//#region 从左边截取指定长度的字符串

String.prototype.left = function (len) {
    if (isNaN(parseInt(len)))
        return this;
    else {
        if (parseInt(len) > this.length)
            len = this.length;
    }

    return this.substr(0, len);
}

//#endregion

//#region 从右边截取指定长度的字符串

String.prototype.right = function (len) {
    if (isNaN(parseInt(len)))
        return;
    else {
        if (parseInt(len) > this.length)
            len = this.length;
    }

    return this.substring(this.length - len, this.length);
}

//#endregion

//#region 得到中间的字符串,注意从0开始

String.prototype.middle = function (start, len) {
    if (isNaN(parseInt(start)) || isNaN(parseInt(len)))
        return this;
    return this.substr(start, len);
}

//#endregion

//#region 是否正确的IP地址

String.prototype.isIP = function () {
    var reSpaceCheck = /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
    if (reSpaceCheck.test(this)) {
        this.match(reSpaceCheck);
        if (RegExp.$1 <= 255 && RegExp.$1 >= 0
            && RegExp.$2 <= 255 && RegExp.$2 >= 0
            && RegExp.$3 <= 255 && RegExp.$3 >= 0
            && RegExp.$4 <= 255 && RegExp.$4 >= 0) {
            return true;
        }
        else return false;
    }
    else return false;
}

//#endregion

//#region 是否正确的长日期

String.prototype.isLongDate = function () {
    var r = this.replace(/(^\s*)|(\s*$)/g, "").match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$/);
    if (r == null)
        return false;

    var d = new Date(r[1], r[3] - 1, r[4], r[5], r[6], r[7]);
    return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4] && d.getHours() == r[5] && d.getMinutes() == r[6] && d.getSeconds() == r[7]);
}

//#endregion

//#region 是否是正确的短日期

String.prototype.isShortDate = function () {
    var r = this.replace(/(^\s*)|(\s*$)/g, "").match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})$/);
    if (r == null)
        return false;

    var d = new Date(r[1], r[3] - 1, r[4]);
    return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4]);
}

//#endregion

//#region 是否是正确的日期

String.prototype.isDate = function () {
    return this.isLongDate() || this.isShortDate();
}

//#endregion

//#region 是否是手机号码

String.prototype.isMobilePhone = function () {
    return /^(13[0-9]|15[0|3|6|7|8|9]|18[8|9]|170)\d{8}$/.test(this);
}

//#endregion

//#region 是否是邮件

String.prototype.isEmail = function () {
    return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(this);
}

//#endregion

//#region 是否是邮编(中国)

String.prototype.isZipCode = function () {
    return /^[\d]{6}$/.test(this);
}

//#endregion

//#region 是否是有效的身份证(中国)

String.prototype.isIDCard = function () {
    var iSum = 0;
    var info = "";
    var sId = this;
    var aCity = { 11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙 江", 31: "上海", 32: "江苏", 33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东", 41: "河南", 42: "湖 北", 43: "湖南", 44: "广东", 45: "广西", 46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南", 54: "西 藏", 61: "陕西", 62: "甘肃", 63: "青海", 64: "宁夏", 65: "新疆", 71: "台湾", 81: "香港", 82: "澳门", 91: "国 外" };

    if (!/^\d{17}(\d|x)$/i.test(sId)) {
        return false;
    }
    sId = sId.replace(/x$/i, "a");
    //非法地区
    if (aCity[parseInt(sId.substr(0, 2))] == null)
        return false;

    var sBirthday = sId.substr(6, 4) + "-" + Number(sId.substr(10, 2)) + "-" + Number(sId.substr(12, 2));
    var d = new Date(sBirthday.replace(/-/g, "/"))

    //非法生日
    if (sBirthday != (d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate()))
        return false;
    for (var i = 17; i >= 0; i--)
        iSum += (Math.pow(2, i) % 11) * parseInt(sId.charAt(17 - i), 11);

    if (iSum % 11 != 1)
        return false;

    return true;
}

//#endregion

//#region 是否是有效的电话号码(中国)

String.prototype.isPhone = function () {
    return /(^[0-9]{3,4}\-[0-9]{3,8}$)|(^[0-9]{3,8}$)|(^\([0-9]{3,4}\)[0-9]{3,8}$)|(^0{0,1}13[0-9]{9}$)/.test(this);
}

//#endregion

//#region 是否小数

String.prototype.isFloat = function (place) {
    if (!isNaN(parseInt(place)) && 0 < place)
        return new RegExp("/(^[0-9]\.[0-9]{" + place + "}$)|(^[1-9][0-9]*\.[0-9]{" + place + "}$)/").test(this);
    else
        return /(^[0-9]\.[0-9]*$)|(^[1-9][0-9]*\.[0-9]*$)/.test(this);
}

//#endregion

//#region 是否是数字

String.prototype.isNumber = function () {
    return /(^[1-9]\d*$)|(^0$)/.test(this);
}

//#endregion

//#region 对字符串进行Html编码

String.prototype.htmlEncode = function () {
    var str = this;

    str = str.replace(/&/g, "&amp;");
    str = str.replace(/</g, "&lt;");
    str = str.replace(/>/g, "&gt;");
    str = str.replace(/\'/g, "&apos;");
    str = str.replace(/\"/g, "&quot;");
    str = str.replace(/\n/g, "<br/>");
    str = str.replace(/\ /g, "&nbsp;");
    str = str.replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;");

    return str;
}

//#endregion

//#region 转换成日期

String.prototype.toDate = function () {
    try {
        return new Date(this.replace(/-/g, "\/"));
    }
    catch (e) {
        return null;
    }
}

//#endregion

//#endregion

//#region 数组函数扩展

//#region 遍历数组
//回调参数：数组元素，元素索引

Array.prototype.foreach = function (iterator) {
    for (var i = 0; i < this.length; i++)
        iterator(this[i], i);
}

//#endregion

//#region 数组元素是否全部符合指定条件
//predicate方法参数：数组元素，元素索引

Array.prototype.all = function (predicate) {
    var all = true;
    for (var i = 0; i < this.length; i++)
        all = all && predicate(this[i], i);
    return all;
}

//#endregion

//#region 数组元素是否存在至少一个符合条件
//predicate方法参数：数组元素，元素索引

Array.prototype.exisit = function (item) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == item)
            return true;
    }

    return false;
}

//#endregion

//#region 数组中符合条件的元素个数
//predicate方法参数：数组元素，元素索引

Array.prototype.count = function (predicate) {
    var count = 0;
    for (var i = 0; i < this.length; i++) {
        if (predicate(this[i], i))
            count++;
    }

    return count;
}

//#endregion

//#region 数组中正向查找匹配的第一个元素
//predicate方法参数：数组元素，元素索引

Array.prototype.find = function (predicate) {
    for (var i = 0; i < this.length; i++) {
        if (predicate(this[i], i))
            return this[i]
    }

    return null;
}

//#endregion

//#region 数组中正向查找匹配的第一个元素的位置
//predicate方法参数：数组元素，元素索引

Array.prototype.findIndex = function (predicate) {
    for (var i = 0; i < this.length; i++) {
        if (predicate(this[i], i))
            return i;
    }

    return -1;
}

//#endregion

//#region 数组中查找匹配的所有元素

Array.prototype.findAll = function (predicate) {
    var resultArray = [];
    for (var i = 0; i < this.length; i++) {
        if (predicate(this[i], i))
            resultArray.push(this[i]);
    }

    return resultArray;
}

//#endregion

//#endregion

//#region 日期函数扩展

Date.prototype.compareTo = function (dateTime) {
    return this.valueOf() - dateTime.valueOf();
}

Date.prototype.Format = function (format) {
    var o = {
        "M+": this.getMonth() + 1, //month   
        "d+": this.getDate(),    //day   
        "h+": this.getHours(),   //hour   
        "m+": this.getMinutes(), //minute   
        "s+": this.getSeconds(), //second   
        "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter   
        "S": this.getMilliseconds() //millisecond   
    }

    if (/(y+)/.test(format)) format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(format))
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

Date.prototype.Add = function (interval, number) {
    switch (interval) {
        case "y":
            this.setFullYear(this.getFullYear() + number);
            return this;
        case "q":
            this.setMonth(this.getMonth() + number * 3);
            return this;
        case "m":
            this.setMonth(this.getMonth() + number);
            return this;
        case "w":
            this.setDate(this.getthis() + number * 7);
            return this;
        case "d":
            this.setDate(this.getthis() + number);
            return this;
        case "h":
            this.setHours(this.getHours() + number);
            return this;
        case "mm":
            this.setMinutes(this.getMinutes() + number);
            return this;
        case "s":
            this.setSeconds(this.getSeconds() + number);
            return this;
        default:
            return this;
    }
}

//#endregion

function ChangeDateFormat(jsondate) {
        if (jsondate.length == 0)
            return '';
        jsondate = jsondate.replace("/Date(", "").replace(")/", "");     
        if (jsondate.indexOf("+") > 0) {    
            jsondate = jsondate.substring(0, jsondate.indexOf("+"));     
        }     
        else if (jsondate.indexOf("-") > 0) {    
            jsondate = jsondate.substring(0, jsondate.indexOf("-"));     
        }     
     
        var date = new Date(parseInt(jsondate, 10));   
        var month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;    
        var currentDate = date.getDate() < 10 ? "0" + date.getDate() : date.getDate(); 
        var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours(); 
        var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes(); 
        var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();   
        return date.getFullYear() + "-" + month + "-" + currentDate + " " + hours + ":" + minutes + ":" + seconds;    
}

function OpenModalWin(url, title, width, height, iconCls){
    alert('此方法已过时，请调用OpenModalWin2');
    $("#openwin").attr({'src':url,'width':width, 'height':height})
    $("#openwin").removeAttr('style');
    $('#openwin').window({
        iconCls:'icon-internet',
        title:title,
        width:width + 14,
        height:height,
        modal:true,
        minimizable:false,
        maximizable:false,
        collapsible:false,
        shadow:false,
        inline:false
    });
}

function OpenModalWin2(url, title, width, height, loadCall){
    var iframeId = 'iframe_' + (new Date().getTime());
    $(".viewFramework-product-body").append('<iframe id="{0}" src="" frameborder="0" height="0" style="height: 0px; width: 0px; display: none;"></iframe>'.format(iframeId));
    var iframeObj = $("#"+iframeId);
    iframeObj.attr({'src':url,'width':width, 'height':height})
    iframeObj.removeAttr('style');
    iframeObj.window({iconCls:'icon-internet',title:title,width:width + 14,height:height,
        modal:true,minimizable:false,maximizable:false,collapsible:false,shadow:false,
    });
    if (loadCall != undefined){
        iframeObj.unbind("load");
        iframeObj.load(function(){loadCall(iframeObj);});
    }   
    return iframeObj;
}

/*
********************************************************
pis project global                          
********************************************************
*/
var PIS = PIS || {};
PIS.namespace = function (ns_string) {
    var parts = ns_string.split('.'),
        parent = PIS,
        i = 0;

    if (parts[0] === 'PIS') {
      parts = parts.slice(1);
    }

    for (i = 0; i < parts.length; i++) {
      if (typeof parent[parts[i]] === 'undefined') {
        parent[parts[i]] = {};
      }
      parent = parent[parts[i]];
    }
    return parent;
};

/*
********************************************************
pis project object1                          
********************************************************
*/
PIS.namespace('PIS.object1');
PIS.object1 = function (o) {
    function F() {}
    F.prototype = o;
    return new F();
}

/*
********************************************************
PIS.sl                              
********************************************************
*/
PIS.namespace('PIS.sl');
PIS.sl = (function () {
    var slInstance = null,
        slLoadedExtendFun = function () { //alert('slLoadedExtendFun');
        };

    return {
      silverlightLoad: function (sender, args) {
        try {
          var slControl = sender.getHost();
          if (slControl != null) {
            slInstance = slControl.Content.SL;

            if (typeof slLoadedExtendFun === 'function') {
              slLoadedExtendFun();
            }
          }
        }
        catch (ex) {
          alert("初始化SL组件失败，提示信息：" + ex.Message);
        }
      },
      getSLInstance: function () {
        return slInstance;
      }
    };
}());

/*
********************************************************
PIS.win                              
********************************************************
*/
PIS.namespace('PIS.ui.Win');
PIS.ui.Win = (function() {
    var iframeWarpObj = null;
    var getIframeId = function () {
        return 'iframe_' + (new Date().getTime());
    };
    var frameMsgExchange = function (iframeObj, msg, callbackfunc){
        var contentWin = iframeObj[0].contentWindow;
        if (contentWin.hasOwnProperty('msgExchange')) {
            contentWin.msgExchange(callbackfunc, msg, iframeObj);
        }
    };

    var Const = function (iframeWarp) {
        iframeWarpObj = iframeWarp;
        if (typeof iframeWarp === 'string'){
            iframeWarpObj = $(iframeWarp);
        }

        this.openModal = function(url, title, width, height, msg, callbackfunc){
            var iframeId = getIframeId();
            iframeWarpObj.append('<iframe id="{0}" src="" frameborder="0" height="0" style="height: 0px; width: 0px; display: none;"></iframe>'.format(iframeId));
            var iframeObj = iframeWarpObj.find("#"+iframeId);
            iframeObj.attr({'src':url,'width':width, 'height':height})
            iframeObj.removeAttr('style');
            iframeObj.window({iconCls:'icon-internet',title:title,width:width + 14,height:height,
                modal:true,minimizable:false,maximizable:false,collapsible:false,shadow:false,onClose:function(){iframeObj.remove();}
            });
            if (typeof callbackfunc === 'function'){
                iframeObj.unbind("load");
                iframeObj.load(function(){
                    frameMsgExchange(iframeObj, msg, callbackfunc);
                });
            }

            var closeWin = function () {
               iframeObj.window('close');
            };

            return {
                'close':closeWin
            };
        };
    };
  return Const;
}());

/*
********************************************************
PIS.quickDateSelector                                 
********************************************************
*/
PIS.namespace('PIS.quickDateSelector');
PIS.quickDateSelector = (function () {
    var HTML = '<div class="quickDateSelector" tabindex="0"><div class="dropdown-panle"><div>日期范围</div><div class="form-inline">开始时间：<input class="form-control input-sm from_datetime" id="dateRangeBegin" onclick="WdatePicker({onpicked:PIS.quickDateSelector.datePicked, dateFmt:&quot;yyyy-MM-dd HH&quot;})" type="text" value=""></div><div class="form-inline">结束时间：<input class="form-control input-sm from_datetime" id="dateRangeEnd" onclick="WdatePicker({onpicked:PIS.quickDateSelector.datePicked, dateFmt:&quot;yyyy-MM-dd HH&quot;})" type="text" value=""></div><div>快捷日期</div><ul class="quick-list clearfix"><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(1)">今天</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(2)">昨天</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(3)">最近7天</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(4)">上周</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(5)">最近15天</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(6)">本月</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(7)">最近30天</a></li><li><a href="javascript:void(0)" onclick="PIS.quickDateSelector.chang(8)">上月</a></li></ul><div class="operator"><a class="btn btn-info" href="javascript:void(0)" onclick="PIS.quickDateSelector.hide()">确定</a></div></div></div>';

    var currquickDateEle = null,
        quickDateSelectorEle = null,
        dateRangeBeginEle = null,
        dateRangeEndEle = null;

    var changDate = function(value){
        var beginDate = new Date();
        var endDate = new Date();
        switch(value) {
            case 1:
                var h = beginDate.getHours();
                if (h < 9) {
                    beginDate.setDate(beginDate.getDate() - 1);
                    update(beginDate, endDate);
                }
                else {
                    endDate.setDate(endDate.getDate() + 1);
                    update(beginDate, endDate);
                }
                break;
            case 3:
                beginDate.setDate(beginDate.getDate() - 7);
                update(beginDate, endDate);
                break;
            case 5:
                beginDate.setDate(beginDate.getDate() - 15);
                update(beginDate, endDate);
                break;
            case 7:
                beginDate.setDate(beginDate.getDate() - 30);
                update(beginDate, endDate);
                break;
            case 2:
                var h = beginDate.getHours();
                if (h < 9) {
                    beginDate.setDate(beginDate.getDate() - 2);
                    endDate.setDate(endDate.getDate() - 1);
                    update(beginDate, endDate);
                }
                else {
                    beginDate.setDate(beginDate.getDate() - 1);
                    update(beginDate, endDate);
                }
                break;
            case 4:
                day = beginDate.getDay();
                day = day == 0 ? 7 : day;
                beginDate.setDate(beginDate.getDate() - day - 6);
                endDate.setDate(endDate.getDate() - day);
                update(beginDate, endDate);
                break;
            case 6:
                beginDate.setDate(1);
                update(beginDate, endDate);
                break;
            case 8:
                beginDate.setMonth(beginDate.getMonth() - 1);
                beginDate.setDate(1);
                endDate.setDate(0);
                update(beginDate, endDate);
                break;
        }
    };
    var update = function (beginDate, endDate) {
        var str1 = '{0}-{1}-{2} {3}'.format(beginDate.getFullYear(), beginDate.getMonth() + 1, beginDate.getDate(), '08');
        var str2 = '{0}-{1}-{2} {3}'.format(endDate.getFullYear(), endDate.getMonth() + 1, endDate.getDate(), '08');
      
        dateRangeBeginEle.val(str1);
        dateRangeEndEle.val(str2);

        datePicked();
        hideDateSelector();
    };
    var datePicked = function () {
        currquickDateEle.val('{0}  至  {1}'.format(dateRangeBeginEle.val(), dateRangeEndEle.val()));
        currquickDateEle.attr({beginDate: dateRangeBeginEle.val(), endDate: dateRangeEndEle.val()});
    };
    var showDateSelector = function (e) {
        // var that = $(window.event.srcElement);
        var that = $(e); 
        currquickDateEle = that;
        var offset = that.offset();
        var beginDate = that.attr('beginDate');
        var endDate = that.attr('endDate');
        var dateFmt = that.attr('dateFmt');

        if (quickDateSelectorEle === null) {
            $('body').append(HTML);
            quickDateSelectorEle = $('.quickDateSelector');
            dateRangeBeginEle = $('#dateRangeBegin');
            dateRangeEndEle = $('#dateRangeEnd');
        }

        dateRangeBeginEle.val(beginDate);
        dateRangeEndEle.val(endDate);

        quickDateSelectorEle.css({position : 'absolute', left : offset.left, top : offset.top + that.outerHeight()});
        quickDateSelectorEle.show();
    };
    var hideDateSelector = function () {
        $('.quickDateSelector').hide();
    };
    return {
        show:showDateSelector,
        hide:hideDateSelector,
        datePicked:datePicked,
        chang:changDate
    };
}());