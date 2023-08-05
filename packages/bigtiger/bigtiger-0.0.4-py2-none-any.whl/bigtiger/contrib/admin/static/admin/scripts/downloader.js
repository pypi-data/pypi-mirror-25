var downloader = {
	downFileUrl: function (fileUrl) {
		var $downFileFrame = $('#_downFileFrame');
		if ($downFileFrame.length === 0) {
			$downFileFrame = $('<iframe id="_downFileFrame" width="0" height="0" target="_blank"></iframe>');
			$downFileFrame.appendTo($('body'));
		}
		$downFileFrame.attr('src', fileUrl);
	}
}