/**
 * Created by bhr on 16/4/11.
 */

(function($){
	function geturlqueryobj(url) {
		var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
		var paraObj = {}
		for (i = 0; j = paraString[i]; i++) {
			paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
		}
		delete(paraObj[""])
		return paraObj
	}

	function urlparse(paras) {
		var paraObj = geturlqueryobj(location.href)
		var returnValue = paraObj[paras.toLowerCase()];
		if (typeof(returnValue) == "undefined") {
			return "";
		} else {
			return returnValue;
		}
	}

	function genurlquerystring(obj) {
		var qs = "";
		for (val in obj) {
			qs = qs + val + "=" + obj[val] + "&";
		}
		qs = "?" + qs;
		return qs;
	}
	toggleFieldset = function(el) {
		var fieldset = $(el).parents('fieldset').first();
		$(el).children('i').toggleClass('icon-chevron-right');
		$(el).children('i').toggleClass('icon-chevron-down');
		fieldset.children('table').toggle();
	}
	if (location.href.search($("form.filter select").first().attr("name")) != -1) {
		toggleFieldset($("form.filter legend"));
	}
	// ----- sort -----
	$("th>span[data-skey]").toggleClass("tha");
	$("th>span[data-skey]").click(function(event) {
		var this_span = $(event.target);
		var qobj = geturlqueryobj(location.href);
		qobj["s"] = this_span.data('skey');
		location.href = genurlquerystring(qobj);
	});
	var sort_key = urlparse('s');
	$("th>span[data-skey]").each(function(pos, obj) {
		// 根据排序关键字来添加图标
		if (encodeURI($(obj).data('skey')) == sort_key) {
			$(obj).parent().append("<i class='icon icon-chevron-down'></i>");
		}
	});
	if ($("thead th i").length == 0 && $("table.sortable").length == 1) {
		// 如果没有默认的排序选项,则添加图标到节点编号列
		$("thead th").first().append("<i class='icon icon-chevron-down'></i>");
	}
	// ----- end sort -----
	// ------- pagination --------
	$(".pagination a[data-num]").each(function(i, obj) {
		var page_num = $(obj).data("num");
		var url_obj = geturlqueryobj(location.href);
		url_obj["page"] = page_num;
		$(obj).attr("href", genurlquerystring(url_obj));
	});
	$("a.per-page").click(function() {
		var per_page = $(this).data("number");
		var url_obj = geturlqueryobj(location.href);
		url_obj["pp"] = per_page;
		url_obj["page"] = "0";
		location.href = genurlquerystring(url_obj);
		return false;
	});
	$("form.page").submit(function() {
		var page_num = $("form.page").find('input[name="page"]').val();
		var url_obj = geturlqueryobj(location.href);
		url_obj["page"] = page_num;
		location.href = genurlquerystring(url_obj);
		return false;
	});
	$("form.filter").submit(function() {
		var f = $("form.filter");
		var form_url = $("form.filter").attr("action");
		var f_url_obj = geturlqueryobj(f.serialize());
		var url_obj = geturlqueryobj(location.href);
		var i;
		for (i in f_url_obj) {
			url_obj[i] = f_url_obj[i]
		}
		if (url_obj.hasOwnProperty("page") == true) {
			url_obj["page"] = '';
		}
		if (url_obj.hasOwnProperty("s") == true) {
			url_obj["s"] = '';
		}
		location.href = form_url + genurlquerystring(url_obj);
		return false;
	});
	// ------- END pagination -------
	// --------alarm level ------
	$(".alarm_level a[data-level]").each(function(i, obj) {
		var alarm_level = $(obj).data('level');
		var url_obj = geturlqueryobj(location.href);
		url_obj['level'] = alarm_level;
		$(obj).attr("href", genurlquerystring(url_obj));
	});
})(jQuery);