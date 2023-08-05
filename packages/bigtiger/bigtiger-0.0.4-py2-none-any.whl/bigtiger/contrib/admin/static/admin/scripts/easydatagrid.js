var EasyDataGrid = (function () {
	var defConfig = {
		rownumbers: true,
		singleSelect: true,
		selectOnCheck: false,
		checkOnSelect: false,
		method: 'get',
		pagination: true,
		showPageList: false,
		showRefresh: false,
		border: false,
		pageSize: 20,
		pagePosition: 'bottom',
		fit: true,
		fitColumns: false,
		striped: true,
		nowrap: true,
		pageList: [5, 10, 20, 50, 100, 200, 500, 1000, 5000],
		emptyMsg: '没有结果数据',
		showHeader: true,
		showFooter: false,
		loadFilter: function (data) {
			if (data.data === null) {
				data.rows = [];
			} else {
				data.rows = data.data;
			}
			return data;
		},
		loadError: function(tableName){
		}
	};

	var Constr = function (dataGridId, options) {
		if (typeof dataGridId !== 'string') {
			throw {
				name: 'Error',
				message: 'dataGridId只能为字符串类型'
			}
		}

		var conf = $.extend({}, defConfig, options);

		if (dataGridId.indexOf('#') < 0)
			dataGridId = '#' + dataGridId;

		var $dataGrid = $(dataGridId).datagrid(conf);

		this.el = $dataGrid;


		this.getSelections = function () {
			return $dataGrid.datagrid('getSelections');
		};

		this.getChecked = function () {
			return $dataGrid.datagrid('getChecked');
		};

		this.load = function (queryParams) {
			$dataGrid.datagrid('load', queryParams);
		};

		this.reload = function () {
			$dataGrid.datagrid("reload");
		};

		this.getRows = function () {
			return $dataGrid.datagrid("getRows");
		};

		this.getRow = function (rowIndex) {
			var rows = this.getRows();
			return rows[rowIndex];
		};

		this.loadData = function (data) {
			return $dataGrid.datagrid("loadData", data);
		};
	};
	return Constr;
})();