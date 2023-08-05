/*!
 * Kline button for Buttons and DataTables.
 * 2016 SpryMedia Ltd - datatables.net/license
 */

(function( factory ){
	if ( typeof define === 'function' && define.amd ) {
		// AMD
		define( ['jquery', 'datatables.net', 'datatables.net-buttons'], function ( $ ) {
			return factory( $, window, document );
		} );
	}
	else if ( typeof exports === 'object' ) {
		// CommonJS
		module.exports = function (root, $) {
			if ( ! root ) {
				root = window;
			}

			if ( ! $ || ! $.fn.dataTable ) {
				$ = require('datatables.net')(root, $).$;
			}

			if ( ! $.fn.dataTable.Buttons ) {
				require('datatables.net-buttons')(root, $);
			}

			return factory( $, root, root.document );
		};
	}
	else {
		// Browser
		factory( jQuery, window, document );
	}
}(function( $, window, document, undefined ) {
'use strict';
var DataTable = $.fn.dataTable;


var _link = document.createElement( 'a' );

/**
 * Clone link and style tags, taking into account the need to change the source
 * path.
 *
 * @param  {node}     el Element to convert
 */
var _styleToAbs = function( el ) {
	var url;
	var clone = $(el).clone()[0];
	var linkHost;

	if ( clone.nodeName.toLowerCase() === 'link' ) {
		clone.href = _relToAbs( clone.href );
	}

	return clone.outerHTML;
};

/**
 * Convert a URL from a relative to an absolute address so it will work
 * correctly in the popup window which has no base URL.
 *
 * @param  {string} href URL
 */
var _relToAbs = function( href ) {
	// Assign to a link on the original page so the browser will do all the
	// hard work of figuring out where the file actually is
	_link.href = href;
	var linkHost = _link.host;

	// IE doesn't have a trailing slash on the host
	// Chrome has it on the pathname
	if ( linkHost.indexOf('/') === -1 && _link.pathname.indexOf('/') !== 0) {
		linkHost += '/';
	}

	return _link.protocol+"//"+linkHost+_link.pathname+_link.search;
};


var options = {'_index_flag': 5158195,
 'backgroundColor': '#fff',
 'color': ['#c23531',
           '#2f4554',
           '#61a0a8',
           '#d48265',
           '#749f83',
           '#ca8622',
           '#bda29a',
           '#6e7074',
           '#546570',
           '#c4ccd3',
           '#f05b72',
           '#ef5b9c',
           '#f47920',
           '#905a3d',
           '#fab27b',
           '#2a5caa',
           '#444693',
           '#726930',
           '#b2d235',
           '#6d8346',
           '#ac6767',
           '#1d953f',
           '#6950a1',
           '#918597',
           '#f6f5ec'],
 'legend': [{'data': ['K'],
             'left': 'center',
             'orient': 'horizontal',
             'selectedMode': 'multiple',
             'show': true,
             'textStyle': {'color': '#333', 'fontSize': 12},
             'top': 'top'}],
 'series': [{'data': [/*open, close, lowest, highest*/],
             'indexflag': 5158195,
             'markLine': {'data': []},
             'markPoint': {'data': []},
             'name': 'K',
             'type': 'candlestick'}],
 'title': [{'left': 'auto',
            'subtext': '',
            'subtextStyle': {'color': '#aaa', 'fontSize': 12},
            'text': 'K',
            'textStyle': {'color': '#000', 'fontSize': 18},
            'top': 'auto'}],
 'toolbox': {'feature': {'dataView': {'show': true},
                         'restore': {'show': true},
                         'saveAsImage': {'show': true,
                                         'title': 'Save as'}},
             'left': '95%',
             'orient': 'vertical',
             'show': true,
             'top': 'center'},
 'tooltip': {'axisPointer': {'type': 'line'},
             'formatter': null,
             'textStyle': {'color': '#fff', 'fontSize': 14},
             'trigger': 'item',
             'triggerOn': 'mousemove|click'},
 'xAxis': [{'axisLabel': {'interval': 'auto', 'margin': 8, 'rotate': 0},
            'axisTick': {'alignWithLabel': false},
            'boundaryGap': false,
            'data': [/*dates*/],
            'inverse': false,
            'max': null,
            'min': null,
            'name': '',
            'nameGap': 25,
            'nameLocation': 'middle',
            'nameTextStyle': {'fontSize': 14},
            'position': null,
            'scale': true,
            'type': 'category'}],
 'yAxis': [{'axisLabel': {'formatter': '{value} ',
                           'interval': 'auto',
                           'margin': 8,
                           'rotate': 0},
            'axisTick': {'alignWithLabel': false},
            'inverse': false,
            'max': null,
            'min': null,
            'name': '',
            'nameGap': 25,
            'nameLocation': 'middle',
            'nameTextStyle': {'fontSize': 14},
            'position': null,
            'scale': true,
            'splitArea': {'show': true},
            'type': 'value'}]}


DataTable.ext.buttons.kline = {
	className: 'buttons-kline',

	text: function ( dt ) {
		return dt.i18n( 'buttons.kline', 'kline' );
	},

	action: function ( e, dt, button, config ) {
		var alldata = dt.buttons.exportData(
			$.extend( {decodeEntities: false}, config.exportOptions ) // XSS protection
		);

		var dateCol = alldata.body.map(function(value, index){return value[0];});
		var prices = alldata.body.map(function(value, index){return [value[1], value[4], value[3], value[2]];});
		options.xAxis[0].data = dateCol;
		options.series[0].data = prices;
		var mychart = echarts.init(document.getElementById('kline'));
		mycart.setOption(options);
	},

	title: '*',

	messageTop: '*',

	messageBottom: '*',

	exportOptions: {},

	header: true,

	footer: false,

	autoPrint: true,

	customize: null
};


return DataTable.Buttons;
}));
