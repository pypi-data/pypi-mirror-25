/*
******************************************
1、TreeView
******************************************
*/

//#region TreeView

var EasyTree = (function () {
    var defConfig = {
        method: 'get',
        animate: true,
        onlyLeafCheck: false,
        checkbox: true
    };

    var Constr = function (eleId, options) {
        if (typeof eleId !== 'string') {
            throw {
                name: 'Error',
                message: 'treeId只能为字符串类型'
            }
        }
        if (eleId.indexOf('#') < 0)
            eleId = '#' + eleId;

        var $viewstate = $(eleId);
        var treeId = eleId + '_tree';

        var conf = $.extend({}, defConfig, options);
        var $tree = $(treeId).tree(conf);

        this.el = $tree;

        this.getChecked = function () {
            var nodes = $tree.tree('getChecked');
            return nodes;
        };

        this.getLeafChecked = function () {
            var nodes = this.getChecked(),
                item = null,
                leafNodes = [];

            for (var i = nodes.length - 1; i >= 0; i--) {
                item = nodes[i];
                if (!item.hasOwnProperty('children') || item.children === null) {
                    leafNodes.push(item);
                }
            }
            return leafNodes;
        };

        this.clearChecked = function () {
            var nodes = this.getChecked();
            for (var i = nodes.length - 1; i >= 0; i--) {
                $tree.tree('uncheck', nodes[i].target);
            }
        };

        this.check = function (nodeId) {
            var node = $tree.tree('find', nodeId);
            $tree.tree('check', node.target);

        };

        this.saveViewState = function (isLeaf) {
            var nodes = [];
            if (isLeaf) {
                nodes = this.getLeafChecked();
            } else {
                nodes = this.getChecked();
            }

            var ids = _.map(nodes, function (node) {return node.id;});
            var s = ids.join(',');
            $viewstate.val(s);
            return s;
        };

        this.loadViewState = function () {
            var self = this;

            var s = $viewstate.val();
            if (s == 'None' || s == '')
                return;

            var nodes = s.split(',');
            _.each(nodes, function (element, index, list) {
                self.check(element);
            });
        };
    };
    return Constr;
})();

//#endregion

//#region UploadFile

var UploadFile = {};
(function($$){
    $$.del = function(that){
        $(that).parent().hide();
        var file_input = $(that).parent().prev();
        file_input.show();
        $('#' + file_input.attr("id").replace('_file','')).val('');
    };
    $$.change = function(that){
        var newfile = $(that).val();
        var obj = $('#' + $(that).attr("id").replace('_file',''));
        if (newfile != ''){
            var lastIndex = newfile.lastIndexOf('\\');
            newfile = newfile.substr(lastIndex + 1, newfile.length - lastIndex);

            console.log(newfile);
            obj.val('{"flag":"add","filename":"'+newfile+'"}');
        }
        else{
            obj.val('');
        }

        if (typeof $$.change_callback === 'function') {
            $$.change_callback(newfile);
        }
    };
})(UploadFile);

//#endregion

//#region QuickDateSelector
var quickDateSelector = {};
(function () {
    function updateDatePicker (qdateId) {
        var beginId = 'id_' + qdateId + '_begin',
            endId = 'id_' + qdateId + '_end',
            beginReadonlyId = beginId + '_read',
            endReadOnlyId = endId + '_read';
            beginDate = $('#' + beginId).val(),
            endDate = $('#' + endId).val();

        $('#' + beginReadonlyId).val(beginDate);
        $('#' + endReadOnlyId).val(endDate);
    };

    quickDateSelector.quickChangDate = function (self, value) {
        var beginDate = new Date();
        var endDate = new Date();
        switch(value) {
            case 1:
                var h = beginDate.getHours();
                if (h < 9) {
                    beginDate.setDate(beginDate.getDate() - 1);
                }
                else {
                    endDate.setDate(endDate.getDate() + 1);
                }
                break;
            case 3:
                beginDate.setDate(beginDate.getDate() - 7);
                break;
            case 5:
                beginDate.setDate(beginDate.getDate() - 15);
                break;
            case 7:
                beginDate.setDate(beginDate.getDate() - 30);
                break;
            case 2:
                var h = beginDate.getHours();
                if (h < 9) {
                    beginDate.setDate(beginDate.getDate() - 2);
                    endDate.setDate(endDate.getDate() - 1);
                }
                else {
                    beginDate.setDate(beginDate.getDate() - 1);
                }
                break;
            case 4:
                day = beginDate.getDay();
                day = day == 0 ? 7 : day;
                beginDate.setDate(beginDate.getDate() - day - 6);
                endDate.setDate(endDate.getDate() - day);
                break;
            case 6:
                beginDate.setDate(1);
                break;
            case 8:
                beginDate.setMonth(beginDate.getMonth() - 1);
                beginDate.setDate(1);
                endDate.setDate(0);
                break;
        }
        
        var qdateId = $(self).attr('aria-labelledby');
        var str1 = moment(beginDate).format('YYYY-MM-DD HH');
        var str2 = moment(endDate).format('YYYY-MM-DD HH');
        $('#id_' + qdateId + '_begin').val(str1);
        $('#id_' + qdateId + '_end').val(str2);

        updateDatePicker(qdateId);
    };

    quickDateSelector.datePicked = function() {
        var qdateId = $(this).attr('aria-labelledby');
        updateDatePicker(qdateId);
    };
})();

//#endregion