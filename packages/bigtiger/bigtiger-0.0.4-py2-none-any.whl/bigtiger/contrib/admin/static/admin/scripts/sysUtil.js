var win = {
	winopenMax : function(url) {
		var sLeft = 0;
		var sTop = 0;
		var sW = parseInt(screen.availWidth) - 6;
		var sH = parseInt(screen.availHeight) - 50;
		var option = "height="
				+ sH
				+ ",width="
				+ sW
				+ ",left="
				+ sLeft
				+ ",top="
				+ sTop
				+ ",scrollbars=yes,status=yes,toolbar=yes,menubar=no,location=yes,resizable=yes";
		var newWin = window.open(url, "", option);
		newWin.focus();
	},
	winopen80 : function(url) {
		var sW = parseInt(screen.availWidth * 0.8) - 6;
		var sH = parseInt(screen.availHeight * 0.8) - 50;
		var sLeft = (screen.width - sW) / 2;
		var sTop = (screen.height - sH) / 2;
		var option = "height="
				+ sH
				+ ",width="
				+ sW
				+ ",left="
				+ sLeft
				+ ",top="
				+ sTop
				+ ",scrollbars=yes,status=yes,toolbar=no,menubar=no,location=no,resizable=yes";
		var newWin = window.open(url, "", option);
		newWin.focus();
	},
	winopen50 : function(url) {
		var sW = parseInt(screen.availWidth * 0.5) - 6;
		var sH = parseInt(screen.availHeight * 0.5) - 50;
		var sLeft = (screen.width - sW) / 2;
		var sTop = (screen.height - sH) / 2;
		var option = "height="
				+ sH
				+ ",width="
				+ sW
				+ ",left="
				+ sLeft
				+ ",top="
				+ sTop
				+ ",scrollbars=yes,status=yes,toolbar=no,menubar=no,location=no,resizable=yes";
		var newWin = window.open(url, "", option);
		newWin.focus();
	},
	winopenRight : function(url) {
		var sW = parseInt(screen.availWidth * 0.5) - 6;
		var sH = parseInt(screen.availHeight) - 50;
		var sLeft = (screen.width - sW);
		var sTop = 0;
		var option = "height="
				+ sH
				+ ",width="
				+ sW
				+ ",left="
				+ sLeft
				+ ",top="
				+ sTop
				+ ",scrollbars=yes,status=yes,toolbar=no,menubar=no,location=no,resizable=yes";
		var newWin = window.open(url, "", option);
		newWin.focus();
	},
	CloseWindow : function() {
		var ua = navigator.userAgent;
		var ie = navigator.appName == "Microsoft Internet Explorer" ? true
				: false;
		if (ie) {
			var IEversion = parseFloat(ua.substring(ua.indexOf("MSIE ") + 5, ua
					.indexOf(";", ua.indexOf("MSIE "))))
			if (IEversion < 5.5) {
				var str = '<object id=noTipClose classid="clsid:ADB880A6-D8FF-11CF-9377-00AA003B7A11">'
				str += '<param name="Command" value="Close"></object>';
				document.body.insertAdjacentHTML("beforeEnd", str);
				document.all.noTipClose.Click();
			} else {
				window.opener = null;
				window.close();
			}
		} else
			window.close();
	},
	winopenNormal : function(url, winNM, sW, sH) {
		var sLeft = (screen.width - sW) / 2;
		var sTop = (screen.height - sH) / 2;
		if (sW == 0 || sW == "") {
			sLeft = 0;
			sW = parseInt(screen.availWidth) - 6;
		}
		if (sH == 0 || sH == "") {
			sTop = 0;
			sH = parseInt(screen.availHeight) - 50;
		}
		var option = "dialogHeight:" + sH + "px;dialogWidth:" + sW
				+ "px;center:yes;status:off;help:no;scroll:off;resizable=yes";
		var newWin = null;
		var explorer = window.navigator.userAgent;
		if (explorer.indexOf("Chrome") < 0) {
			newWin = window.showModalDialog(url, winNM, option);
		} else {
			option = "height="
					+ sH
					+ ",width="
					+ sW
					+ ",left="
					+ sLeft
					+ ",top="
					+ sTop
					+ ",scrollbars=yes,status=yes,toolbar=no,menubar=no,location=no,resizable=yes";
			newWin = window.open(url, winNM, option);
		}
		if (newWin == null) {
			newWin = window.returnValue;
		}
		return newWin;
	},
	confirmx : function(mess, callback, closed) {
		layer.confirm(mess, {
			icon : 3,
			title : '系统提示'
		}, function(index) {
			// 确认对话框
			if (typeof callback == 'function') {
				callback();
			} else {
				location = href;
			}
			layer.close(index);
		});
		return false;
	},
	promptx : function(title, lable, href, closed) {
		top.$.jBox(
				"<div class='form-search' style='padding:20px;text-align:center;'>"
						+ lable
						+ "：<input type='text' id='txt' name='txt'/></div>", {
					title : title,
					submit : function(v, h, f) {
						if (f.txt == '') {
							top.$.jBox.tip("请输入" + lable + "。", 'error');
							return false;
						}
						if (typeof href == 'function') {
							href();
						} else {
							resetTip(); // loading();
							location = href + encodeURIComponent(f.txt);
						}
					},
					closed : function() {
						if (typeof closed == 'function') {
							closed();
						}
					}
				});
		return false;
	},
	openDialog : function(title, url, width, height, callback, btns, inMsg) {
		btns = btns || ['确定', '关闭'];
		inMsg = inMsg || '';

		layer.open({
			type : 2,
			area : [ width, height ],
			title : title,
			maxmin : true,
			content : url,
			btn : btns,
			yes : function(index, layero) {
				var body = layer.getChildFrame('body', index);
				var iframeWin = layero.find('iframe')[0]; // 得到iframe页的窗口对象，执行iframe页的方法：iframeWin.method();
				iframeWin.contentWindow.msgExchange(function (msg) {
					if (typeof callback === 'function') {
						callback(index, msg);
					}
					// layer.close(index);
				}, inMsg, null);
			},
			cancel : function(index) {
				layer.close(index);
			}
		});
	},

	prompt: function (title, callback, formType) {
		formType = formType || 0;
		var options = {title: title, formType: formType};
		layer.prompt(options, function(text, index){
		    if (typeof callback === 'function') {
		    	callback(text, index);
		    }
		});
	},

	InitLayerContent : function(url, loadFun, param, divId) {
		// fdw 放回20160604 10:13 周六
		if (!url.startWith("http") && !url.startWith(APP_ROOT)
				&& !url.startWith(WEB_ROOT)) {
			url = window.APP_ROOT + url;
		}
		urlUtil.initUrlPars(url);
		// 如果不带，参数传到springmvc后台的时候就没有了，影响通讯录编辑模块
		if (param != '1') {
			if (url.indexOf('?') > 0)
				url = url.substr(0, url.indexOf('?'));
		}
		// $(".layui-layer-content").load(url, function() {
		if (typeof (divId) == "undefined") {
			divId = ".layui-layer-content"
		} else {
			divId = "#" + divId
		}
		$(divId).load(url, function() {
			if (typeof loadFun == 'function') {
				loadFun();
			}
		});
	},
	openDialogHtml : function(title, url, width, height, loadFun, callback, hideBtn) {
		var strDivId = win.getCharacter(6);
		layer.open({
			type : 1,
			area : [ width, height ],
			title : title,
			maxmin : true, // 开启最大化最小化按钮
			content : '<div id="' + strDivId
					+ '" style="width:100%;height:100%;"></div>',
			btn : hideBtn ? [] : [ '确定', '关闭' ],
			yes : function(index, layero) {
				if (typeof callback == 'function') {
					// 传过来的是执行方法
					var resu = callback();
					if (typeof (resu) != 'undefined' && !resu) {
						return;
					}
					// layer.close(index);// 关闭对话框。
				} else {
					// iframeWin.contentWindow.doSubmit();
				}
			},
			cancel : function(index) {
			},
			end : function() {

			},
			full : function() {
				alert('full');
				var height = document.body.offsetHeight - 100;
				$(".layui-layer-content").height(height);
				$("#" + strDivId).height(height);
				// 派发事件
				require([ 'dojo/topic' ], function(topic) {
					topic.publish("/layer/full");
				});
			},
			restore : function() {
				alert('restore');
				var iHei = parseInt(height) - 100;
				$(".layui-layer-content").css('height', iHei + 'px');
				$("#" + strDivId).css('height', iHei + 'px');
				// 派发事件
				require([ 'dojo/topic' ], function(topic) {
					topic.publish("/layer/restore");
				});
			}
		});
		if (url.indexOf('.jsp') < 0) {
			this.InitLayerContent(url, loadFun, '1', strDivId);
		} else
			this.InitLayerContent(url, loadFun, null, strDivId);
		document.onkeydown = function(event) {
			var e = event || window.event
					|| arguments.callee.caller.arguments[0];
			if (e && e.keyCode == 27) { // 按 Esc
				layer.closeAll();
			}
		};
	},
	openDialogNoHtml : function(title, obj, width, height, loadFun, callback) {
		var strDivId = win.getCharacter(6);
		layer.open({
			type : 1,
			area : [ width, height ],
			title : title,
			maxmin : true, // 开启最大化最小化按钮
			content : '<div id="' + strDivId
					+ '" style="width:100%;height:100%;"></div>',
			btn : [ '确定', '关闭' ],
			yes : function(index, layero) {
				if (typeof callback == 'function') {
					// 传过来的是执行方法
					var resu = callback();
					if (typeof (resu) != 'undefined' && !resu) {
						return;
					}
					layer.close(index);// 关闭对话框。
				} else {
					layer.close(index);// 关闭对话框。
				}
			},
			cancel : function(index) {
			},
			end : function() {

			}
		});
		$('#' + strDivId).append(obj);
		$('#' + strDivId).css("overflow", "hidden");
	},
	openDialogHtml_other : function(title, url, width, height, loadFun,
			callback) {
		var strDivId = win.getCharacter(6);
		layer.open({
			type : 1,
			area : [ width, height ],
			title : title,
			maxmin : true, // 开启最大化最小化按钮
			content : '<div id="' + strDivId
					+ '" style="width:100%;height:100%;"></div>',
			btn : [],
			yes : function(index, layer) {
				if (typeof callback == 'function') {
					// 传过来的是执行方法
					var resu = callback();
					if (typeof (resu) != 'undefined' && !resu) {
						return;
					}
					top.layer.close(index);// 关闭对话框。
				} else {
					// iframeWin.contentWindow.doSubmit();
				}
			},
			cancel : function(index) {
			},
			end : function() {

			}
		});
		this.InitLayerContent(url, loadFun, null, strDivId);
	},
	openDialogHtmlMax : function(title, url, width, height, loadFun, callback) {
		var strDivId = win.getCharacter(6);
		var index = top.layer.open({
			type : 1,
			area : [ width, height ],
			title : title,
			maxmin : true, // 开启最大化最小化按钮
			content : '<div id="' + strDivId
					+ '" style="width:100%;height:100%;"></div>',
			yes : function(index, layer) {
				if (typeof callback == 'function') {
					// 传过来的是执行方法
					callback();
					top.layer.close(index);// 关闭对话框。
				} else {
					// iframeWin.contentWindow.doSubmit();
				}
			},
			cancel : function(index) {
			},
			end : function() {

			}
		});
		this.InitLayerContent(url, loadFun, null, strDivId);
		layer.full(index);
	},
	openDialogView : function(title, url, width, height, loadFun,oldExcution) {
		top.layer.open({
			type : 2,
			area : [ width, height ],
			title : title,
			maxmin : true, // 开启最大化最小化按钮
			content : url,
			btn : [ '关闭' ],
			cancel : function(index) {
			},
			success:function(dom, index) {//lanwei 20170103加载完成后回调 替换原有的InitLayerContent函数
				if (typeof loadFun == 'function') {
					if(oldExcution==null){
						loadFun();
					}
				}
			}
		});
		//使用详情页
		if(oldExcution!=null&&oldExcution==true){
			this.InitLayerContent(url, loadFun);
		}
		document.onkeydown = function(event) {
			var e = event || window.event
					|| arguments.callee.caller.arguments[0];
			if (e && e.keyCode == 27) { // 按 Esc
				layer.closeAll();
			}
		};
	},
	openRightFull : function(title, url, width, loadFun) {
		// 用于右侧开小窗top.win.openRightFull('历史同期对比','index.jsp',500);
		var strDivId = win.getCharacter(6);
		if (layer)
			layer.closeAll();
		var height = $(window).height() - 52;
		var strUrl = url;
		if (typeof (loadFun) != "undefined") {
			strUrl = '<div id="' + strDivId
					+ '" style="width:100%;height:100%;"></div>';
		}
		layer.open({
			type : 1 // 此处以iframe举例
			,
			title : title,
			area : [ width + 'px', height + 'px' ],
			shade : 0,
			offset : [ // 为了演示，随机坐标
			52, ($("body").width() - width) ],
			content : strUrl,
			btn : [ '关闭' ] // 只是为了演示
			,
			yes : function() {
				layer.closeAll();
			},
			btn2 : function() {
				layer.closeAll();
			},
			zIndex : layer.zIndex // 重点1
			,
			success : function(layero) {
				layer.setTop(layero); // 重点2
			}
		});
		if (typeof (loadFun) != "undefined") {
			this.InitLayerContent(url, loadFun, null, strDivId);
		}
	},
	getCharacter : function(ilen) {
		var charList = '';
		for (var i = 0; i < ilen; i++) {
			var character = String.fromCharCode(Math.floor(Math.random() * 26)
					+ "a".charCodeAt(0));
			charList += character;
		}
		return charList;
	}
}