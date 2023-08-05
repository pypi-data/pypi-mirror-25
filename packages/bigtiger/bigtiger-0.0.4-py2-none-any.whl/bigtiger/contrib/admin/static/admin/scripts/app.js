var app = app || {};

app.refreshData = (function () {
    var ele = null;

    var Constr = function () {
        ele = $('#app-notice-num');
        this.rei_prjdbinf_count = function () {
            /*$.get('/rei/rei_prjdbinf/json/count/', function(data){
                ele.text(data.Count);
                if (data.Count > 0) {
                    ele.show();
                } else {
                    ele.hide();
                }
            });*/
        };
    };
    return Constr;
}());

app.weatherData = (function () {
    var ele = null,
        template = null;

    var Constr = function () {
        ele = $('#weather');
        template =  _.template($('#weather-template').html());

        this.refresh = function () {
            $.get('/base/weather/', function(data){
                // alert(data.results[0].weather_data[0].date);
                if (data === null)
                    return;

                ele.html(template({'day': data.results[0].weather_data[0], 'day1': data.results[0].weather_data[1], 'day2': data.results[0].weather_data[2]}));
            });
        };
    };
    return Constr;
}());

// 内容区域高度管理
app.mainWindow = (function () {
    var _gridResizeFun = null,
        _mainResizeFun = null;

    var onMainWinResize = function () {
        var winHeight = $(window).height();

        if (typeof _gridResizeFun === 'function') {
            var h = winHeight - app.ui.header_height - app.ui.main_content_padding[0] - app.ui.main_content_padding[2] - app.ui.box_title;
            _gridResizeFun(h)
        }

        if (typeof _mainResizeFun === 'function') {
            var h = winHeight - app.ui.header_height - app.ui.main_content_padding[0] - app.ui.main_content_padding[2];
            _mainResizeFun(h);
        }
    };

    var Constr = function () {
        $(window).resize(onMainWinResize);

        this.gridResize = function (func) {
             _gridResizeFun = func;
            onMainWinResize();

        };

        this.mainResize = function (func) {
             _mainResizeFun = func;
            onMainWinResize();
        };

        this.clear = function () {
            _gridResizeFun = null;
            _mainResizeFun = null;
        };
    };

    return new Constr();
})();

app.menus = (function () {
    var find = function (menuId, menuItems) {
            var menuItem,
                max = menuItems.length,
                i = 0;

            for (i; i < max; i++) {
                menuItem = menuItems[i];
                if (menuId === menuItem.Id) {
                    return menuItem;
                } else if (menuItem.childs !== undefined) {
                    var item = findMenu(menuId, menuItem.childs);
                    if (item !== null) {
                        return item;
                    }
                } 
            };
            return null;
        },
        treeFind = function (childs, menuId, depth) {
            var item = null;

            for (var i = childs.length - 1; i >= 0; i--) {
                item = childs[i];
                if (item.id === menuId) {
                    return item;
                }

                if (item.depth !== depth && item.childs !== undefined) {
                    var result = treeFind(item.childs, menuId, depth);
                    if (result !== undefined)
                        return result;
                }
            }
        },
        children = function (menuId, menuItems) {
            var menuItem,
                max = menuItems.length,
                i = 0;

            for (i; i < max; i++) {
                menuItem = menuItems[i];
                if (menuId === menuItem.Id) {
                    return menuItem;
                }
            };
            return null;
        };

    var Constr = function () {
        this.getMenu = function (menuId, depth) {
            depth = depth || 1;

            if (depth === 0)
                return app.rootMenu;

            var childs = app.rootMenu.childs;
            var menuItem = treeFind(childs, menuId, depth);
            return menuItem;
        };
    };

    return new Constr;
}());

var TopbarView = Backbone.View.extend({
    el: '.topbar-nav-list',

    events: {
        'click li':         'link'
    },

    initialize: function () {
    },

    render: function () {
    },

    link: function (e) {
        e.preventDefault();

        var domObj,
            menuId, 
            mainMenuId,
            url,
            menuItem;

        domObj = $(e.currentTarget);
        menuId = domObj.attr('data-menu');
        mainMenuId = domObj.attr('data-mainMenu');
        url = domObj.children('a').attr('href');

        menuItem = app.menus.getMenu(mainMenuId);
        app.views.menuView.setSelected(mainMenuId);
        app.views.sidebarView.show(menuItem.childs);
        app.views.sidebarView.setSelected(menuId);
        app.views.productView.link(url);
    }
});

var MenuView = Backbone.View.extend({
    el: '.header_nav',

    events: {
        'click li':              'selected'
    },

    initialize: function () {
        this.$ifrInner = $('#ifrInner');
        this.$lis = this.$('ul li');
        this.render();
    },

    render: function () {
        var menuId = this.getSelected();
        this.link(menuId);
        return this;
    },

    selected: function (e) {
        e.preventDefault();
        var that = $(e.currentTarget);
        var menuId = that.attr('data-menu');

        this.setSelected(menuId);
        this.link(menuId);
    },

    link: function (menuId) {
        var menuItem = app.menus.getMenu(menuId, 1);

        if (menuItem === null) {
            return;
        }

        app.mainWindow.clear();

        if (menuItem.childs === undefined) {
            app.views.sidebarView.hide();
            app.views.productView.link(menuItem.menu_url);
        } else {
            app.views.sidebarView.show(menuItem.childs);
            app.views.productView.show(menuItem); 
        }
    },

    getSelected: function () {
        var menuId,
            domObj;

         this.$lis.each(function (i, domEle) {
            domObj = $(domEle);
            if (domObj.hasClass('selected')) {
                menuId = domObj.attr('data-menu');
            }
        });
        return menuId;
    },

    setSelected: function (menuId) {
        this.$lis.each(function(i, domEle) {
            if ($(domEle).attr('data-menu') !== menuId) {
                $(domEle).removeClass("selected");
            } else {
                $(domEle).addClass("selected");
            }
        });
    }
});

var SidebarView = Backbone.View.extend({
    el: '.sidebar',

    events: {
        'click .sidebar-fold':          'flod',
        'click .sidebar-title':         'navFlod',
        'click .nav-item':              'selected'
    },

    initialize: function () {
        this.$fold = this.$('.sidebar-fold');
        this.$inner = this.$('.sidebar-inner');
        this.$main = $('.viewFramework-body');

        this.template =  _.template($('#sidebar-template').html());
    },

    render: function () {
        return this;
    },

    flod: function (e) {
        if (this.$main.hasClass('viewFramework-sidebar-full')) {
            this.$main.removeClass('viewFramework-sidebar-full');
            this.$main.addClass('viewFramework-sidebar-mini');
        } else {
            this.$main.removeClass('viewFramework-sidebar-mini');
            this.$main.addClass('viewFramework-sidebar-full');
        }

        if (window.hasOwnProperty('onMainWinResize')) {
            onMainWinResize();
        }
    },

    navFlod: function (e) {
        var obj = $(e.currentTarget),
            parentObj = obj.parent('.sidebar-nav');

        if (parentObj.hasClass('sidebar-nav-fold')) {
            parentObj.removeClass('sidebar-nav-fold');
        } else {
            parentObj.addClass('sidebar-nav-fold');
        }
    },

    selected: function (e) {
        e.preventDefault();
        var that = $(e.currentTarget);
        var menuId = that.attr('data-menu');
        this.setSelected(menuId);
        var url = that.children('a').attr('href');
        this.linkUrl(url);
    },

    linkUrl: function (url) {
        app.views.productView.link(url);
    },

    link: function (menuId) {
        this.setSelected(menuId);
        alert('未实现此方法');
    },

    show: function (menus) {
        this.$inner.html(this.template({e: menus}));
        if (this.$main.hasClass('viewFramework-sidebar-none')) {
            this.$main.removeClass('viewFramework-sidebar-none');
            this.$main.addClass('viewFramework-sidebar-full');
        }
    },

    hide: function () {
        this.$main.removeClass('viewFramework-sidebar-full');
        this.$main.removeClass('viewFramework-sidebar-mini');
        this.$main.addClass('viewFramework-sidebar-none');
        this.$inner.empty();
    },

    setSelected: function (menuId) {
         this.$('.nav-item').each(function(i, domEle) {
            if ($(domEle).attr('data-menu') !== menuId) {
                $(domEle).removeClass("selected");
            } else {
                $(domEle).addClass("selected");
            }
        });
    }
});

var ProductView = Backbone.View.extend({
    el: '.viewFramework-product',

    events: {
        'click .product-item':           'productSelect',
        'load #ifrInner':                'ifrInnerLoaded'

    },

    initialize: function () {
        this.template =  _.template($('#product-template').html());
        // this.full_template = _.template($('#product-full-template').html());
        this.$product = this.$('.product');
        this.$ifrInner = this.$('#ifrInner');
        this.iframe = document.getElementById("ifrInner");
    },

    render: function () {

    },

    ifrInnerLoaded: function () {
    },

    productSelect: function (e) {
        e.preventDefault();
        var that = $(e.currentTarget);
        var url = that.children('a').attr('href');
        var menuId = that.attr('data-menu');
        app.views.sidebarView.setSelected(menuId);

        var menuItem = app.menus.getMenu(menuId, 3);
        if (menuItem.childs === undefined) {
            this.link(url);
        }
        else {
            var url = menuItem.childs[0].menu_url;
            $('.product1').html(url);
            this.link(url);
        }
    },

    link: function (url) {
        var $product = this.$product;
        
        $.get(url, function (data) {
            $product.empty();
            $product.html(data);
        });
    },

    show: function (menuItem) {
        var menuItems = [],
            childs1 = menuItem.childs,
            childs2 = null;

        for(var m = 0, m_max = childs1.length; m < m_max; m++) {
            if (childs1[m].childs === undefined) {
                menuItems.push(childs1[m]);
            } else {
                childs2 = childs1[m].childs;
                for (var n = 0, n_max = childs2.length; n < n_max; n++) {
                   menuItems.push(childs2[n]);
                }
            }
        }
        var feature = JSON.parse(menuItem.remark);
        if (menuItems.length < 13) {
            this.$product.html(this.template({e: menuItem, lst: menuItems, feature: feature}));
        } else {
            var menuItems = _.filter(menuItems, function(item){ return item.is_important == 1; });
            this.$product.html(this.template({e: menuItem, lst: menuItems, feature: feature}));

            // this.$product.html(this.template({e: menuItem, lst: menuItems, childs1: childs1}));
        }
        this.$ifrInner.hide();
    },

    hide: function () {

    },

    full: function () {

    },

    large: function () {

    },

    small: function () {

    }
});

var AppView = Backbone.View.extend({
    el: 'body', 

    events: {
    },

    initialize: function () {

    },

    render: function () {
        return this;
    }
});


var DropdownView = Backbone.View.extend({
    el: '[data-toggle="dropdown"]',
    events: {
        'blur':        'show',
        'click':       'hide'
    },

    initialize: function () {
    },

    render: function () {
        return this;
    },

    show: function (e) {
        e.preventDefault();
        var p = $(e.currentTarget).parent('.dropdown');
        setTimeout(function() {p.removeClass('open');}, 500);
    },

    hide: function (e) {
        e.preventDefault();
        $(e.currentTarget).parent('.dropdown').addClass('open');
    }
});