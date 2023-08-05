var messager = {
	toast: function (content) {
		layer.msg(content, {time: 1000}, function(){});
	},
	alert: function (content, options, yes) {
		// alert(content);
		layer.alert(content, options, yes);
	},
	confirm: function (content, options, yes, cancel) {
		layer.confirm(content, options, yes, cancel);
	},
	deleteConfirm: function (yes) {
		if (typeof yes !== 'function') {
			throw {
				'name': 'Error',
				'message': 'yes typeof not function!'
			}
		}
		this.confirm('你确定要删除该条数据吗？', {icon: 3, title:'删除提示', btn: ['确定','取消']}, function (index) {
			layer.close(index);
			yes();
		});
	}
};