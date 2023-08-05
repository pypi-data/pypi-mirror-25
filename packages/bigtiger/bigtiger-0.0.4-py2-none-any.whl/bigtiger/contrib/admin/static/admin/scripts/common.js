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
    $("#main_content").append('<iframe id="{0}" src="" frameborder="0" height="0" style="height: 0px; width: 0px; display: none;"></iframe>'.format(iframeId));

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