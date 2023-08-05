var ListPageView = (function () {
	var Constr = function (pageConfig) {
		pageConfig = pageConfig || {};

		if (!pageConfig.hasOwnProperty('windowBtns')) {
			pageConfig['windowBtns'] = ['确定', '关闭'];
		}

		var self = this;

		for (var i in pageConfig) {
			this[i] = pageConfig[i];
		}

		if (!this.hasOwnProperty('getDataGridLoadUrl')) {
			this.getDataGridLoadUrl = function () {
				var t = _.template('<%= pageUrl %>json/');
		   		return t({'pageUrl': this.pageUrl});
			};
		}

		if (!this.hasOwnProperty('getInsertUrl')) {
			this.getInsertUrl = function () {
				var t = _.template('<%= pageUrl %>add/?ref=<%= pageUrl %>');
		    	return t({'pageUrl': this.pageUrl});
			};
		}

		if (!this.hasOwnProperty('getUpdateUrl')) {
			this.getUpdateUrl = function (row) {
				var t = _.template('<%= pageUrl %><%= Id %>/?ref=<%= pageUrl %>');
		    	return t({'pageUrl': this.pageUrl, 'Id': this.getRowKey(row)});
			};
		}

		if (!this.hasOwnProperty('getDeleteUrl')) {
			this.getDeleteUrl = function (rows) {
				var self = this;
				var ids = _.map(rows, function(item) { return self.getRowKey(item); }).join(',');
				var t = _.template('<%= pageUrl %><%= pk %>/delete/');
				return t({'pageUrl': this.pageUrl, 'pk': ids});
			};
		}

		if (!this.hasOwnProperty('getDetailUrl')) {
			this.getDetailUrl = function (row) {
				var t = _.template('<%= pageUrl %><%= pk %>/detail/');
		    	return t({'pageUrl': this.pageUrl, 'pk': this.getRowKey(row)});
			};
		}

		if (!this.hasOwnProperty('getExportUrl')) {
			this.getExportUrl = function () {
				var t = _.template('<%= pageUrl %>xls/');
		    	return t({'pageUrl': this.pageUrl});
			};
		}

		if (!this.hasOwnProperty('getImportUrl')) {
			this.getImportUrl = function () {
				var t = _.template('<%= pageUrl %>import/');
		    	return t({'pageUrl': this.pageUrl});
			};
		}

		var opts = {
			queryParams: this.getQueryParams(),
			url: this.getDataGridLoadUrl(),
			toolbar: this.toolbarId
		};

		if (this.detailColumn !== undefined) {
			opts.onClickCell = function (index, field, value) {
				if (field === self.detailColumn) {
					self.detail(index, field, value);
				}
			};
		}

		var pageOpts = this.gridOptions || {};
		opts= $.extend({}, opts, pageOpts);
		this.dataGrid = new EasyDataGrid(this.dataGridId, opts);

		for (var i = this.btns.length - 1; i >= 0; i--) {
			var btnId = this.btns[i];
			var btnObj = $('#btn_' + btnId);
			btnObj.show();

			var func = (function () {
				var _func;
				if (btnId in self) {
					_func = self[btnId];
				} else {
					throw {
						'name': 'Error',
						'message': '未找到事件处理函数:' + btnId
					}
				}
				var __func = function () {
					_func.apply(self, []);
				};
				return __func;
			})();

			btnObj.click(func);
		};
	};

	Constr.prototype.search = function () {
		var q = this.getQueryParams();
		this.dataGrid.load(q);
	};

	Constr.prototype.insert = function () {
		var self = this,
    		url = this.getInsertUrl(),
    		width = this.windowWidth,
    		height = this.windowHeight,
    		title = this.pageTitle + '新增';

    	win.openDialog(title, url, width, height, function (layerId) {
    			self.dataGrid.reload();
				layer.close(layerId);
			}
		);
	};

	Constr.prototype.update = function () {
    	var rows = this.dataGrid.getChecked();
    	if (rows.length === 0) {
			messager.toast('请选择一个修改项目');
    		return false;
    	}

    	if (rows.length > 1) {
    		messager.toast('只能选择一个修改项目');
    		return false;
    	}

    	if (this.hasOwnProperty('updataValid')) {
    		try {
	    		this.updataValid(rows[0]);
	    	}
	    	catch (e) {
	    		messager.toast(e.message);
	    		return;
	    	}
    	}

    	var self = this,
    		url = this.getUpdateUrl(rows[0]),
    		width = this.windowWidth,
    		height = this.windowHeight,
    		title = this.pageTitle + '编辑';

		win.openDialog(title, url, width, height, function (layerId) {
				self.dataGrid.reload();
				layer.close(layerId);
			}
		);
	};

	Constr.prototype.delete = function () {
		var self = this,
			rows = this.dataGrid.getChecked();

    	if (rows.length === 0) {
    		messager.toast('请选择删除项目');
    		return false;
    	}

    	if (this.hasOwnProperty('deleteValid')) {
    		try {
    			this.deleteValid(rows[0]);
	    	}
	    	catch (e) {
	    		messager.toast(e.message);
	    		return;
	    	}
    	}

    	messager.deleteConfirm(function (index) {
    		var url = self.getDeleteUrl(rows),
    			csrf = $("input[name='csrfmiddlewaretoken']").val();

	    	$.post(url, {'csrfmiddlewaretoken': csrf}, function (data) {
	    		messager.toast(data.message);
	    		if (data.success) {
	    			self.dataGrid.reload();
	    		}
	    	});
    	});
	};

	Constr.prototype.import = function () {
		var self = this,
    		url = this.getImportUrl(),
    		width = this.windowWidth,
    		height = this.windowHeight,
    		title = this.pageTitle + '导入';

    	win.openDialog(title, url, width, height, function (layerId) {
			self.dataGrid.reload();
			layer.close(layerId);
		});
	};

	Constr.prototype.export = function () {
		var self = this,
    		baseUrl = this.getExportUrl(),
    		queryParams = this.getQueryParams();

    	var url = this.getUrl(baseUrl, queryParams);
    	downloader.downFileUrl(url);
	};

	Constr.prototype.detail = function (index, field, value) {
		var row = this.dataGrid.getRow(index);
		var url = this.getDetailUrl(row),
    		width = this.windowWidth,
    		height = this.windowHeight,
    		title = this.pageTitle + '详细';

    	win.openDialog(title, url, width, height, function (layerId) {
			layer.close(layerId);
		}, []);

	};

	Constr.prototype.getUrl = function (baseUrl, queryParams) {
		var urlTemp = _.template('<%= baseUrl %>?<%= queryString %>');
		return urlTemp({'baseUrl': baseUrl, 'queryString': $.param(queryParams)});
	};

	return Constr;
})();