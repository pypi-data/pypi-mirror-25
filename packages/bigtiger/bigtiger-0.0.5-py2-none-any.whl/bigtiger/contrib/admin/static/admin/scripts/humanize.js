var humanize = humanize || {};

humanize.formatDate = function (val, row) {
	if (val == null) return '';
	return moment(val).format('YYYY-MM-DD'); 
};

humanize.formatDateTime = function (val, row) {
	if (val == null) return '';
	return moment(val).format('YYYY-MM-DD HH:mm:ss');
}

humanize.formatYesNo = function (val, row) {
	if (val == 0) {
		return '否';
	}
	return '是';
}

humanize.formatSex = function (val, row) {
	if (val == 1) {
		return '男';
	} else if (val == 0) {
		return '女';
	} else {
		return '未知';
	}
}

humanize.formatDataStatus = function (val, row) {
	if (val == 0) {
		return '新增';
	}
	return '锁定';
}

humanize.formatDetailInfo = function (val, row) {
	return '<span class="glyphicon glyphicon-info-sign" style="cursor:pointer" title="详情"></span>'
}