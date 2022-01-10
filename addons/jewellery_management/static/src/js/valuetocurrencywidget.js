odoo.define('jewellery_management.valuetocurrencywidget', function (require) {
"use strict";

	var core = require('web.core');
	var AbstractField = require('web.AbstractField');
	var registry = require('web.field_registry');
	var basic_fields = require('web.basic_fields');

	var _t = core._t;
	var qweb = core.qweb;

	var ValueToCurrency = basic_fields.NumericField.extend({
	    className: 'o_field_number',
        tagName: 'span',
		events: _.extend({}, basic_fields.NumericField.prototype.events, {
	        'keyup': '_onValueToCurrency',
	    }),
		_onValueToCurrency: function (e) {
	        e.preventDefault();
	        e.stopPropagation();
	        var self = this;

	        this._valueToCurrencyConvert(e, e.target.value)
	    },
	    _valueToCurrencyConvert: function(event,amount){

            if(amount == ''){
                amount = '0';
            }
            amount = amount.replace(/[^0-9.]/g, "");

            if (amount.indexOf('.') > -1){
                    amount = amount.toString();

                    var pos = amount.search(/\./g) + 1;
                    amount = amount.substr( 0, pos )
                     + amount.slice( pos ).replace(/\./g, '');

                    var beforeComma = amount.substr(0,amount.indexOf("."));
                    var afterComma = amount.substr(amount.indexOf(".") + 1);

                    beforeComma = parseFloat(beforeComma);
                    beforeComma = beforeComma.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');

                    if(beforeComma.substr(beforeComma.length - 3) == '.00'){
                        beforeComma = beforeComma.substring(0, beforeComma.length - 3);
                    }

                    event.target.value = beforeComma+'.'+afterComma;
                    console.log(amount)
                }else{
                    amount = parseFloat(amount);
                    amount = amount.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');

                    if(amount.substr(amount.length - 3) == '.00'){
                        amount = amount.substring(0, amount.length - 3);
                    }

                    event.target.value = amount;
                    console.log(amount)
                }
            }
	});

	registry
    .add('ValueToCurrency', ValueToCurrency);

    return {
    	ValueToCurrency: ValueToCurrency,
	}

});