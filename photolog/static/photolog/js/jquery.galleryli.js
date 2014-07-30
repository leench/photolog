(function($) {
	$.fn.galleryli = function(options) {
		var options = $.extend({}, $.fn.galleryli.defaults, options);
		$(this, 'img').click(function(){
			alert(1);
		});
	};
	$.fn.galleryli.defaults = {
	};
})(jQuery);
