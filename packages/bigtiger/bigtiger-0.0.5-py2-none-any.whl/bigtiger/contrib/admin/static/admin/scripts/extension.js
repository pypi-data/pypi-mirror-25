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

Array.prototype.exisit = function (predicate) {
    for (var i = 0; i < this.length; i++) {
        if (predicate(this[i], i))
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