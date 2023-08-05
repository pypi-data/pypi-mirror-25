/*
******************************************
raintawidget.js
******************************************
*/

var widgets = widgets || {};
widgets.RainTagWidget = (function () {
    var Constr = function (searchform) {
        searchform = searchform || $("#searchform");
        $('.search-tags .tag-list input[type=radio]').on('click', function () {
            searchform.submit();
        });
    };

    return Constr;
}());

$(function () {
    new widgets.RainTagWidget();
});