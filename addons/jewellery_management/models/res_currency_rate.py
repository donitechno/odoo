# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ResCurrencyRate(models.Model):
    _description = 'res.currency.rate'
    _inherit = 'res.currency.rate'

    tarifbelipersen = fields.Float("tarif beli persen")
    tarifbelinominal = fields.Float("tarif beli dalam nominal")
    tarifjualpersen = fields.Float("tarif jual persen")
    tarifjualnominal = fields.Float("tarif beli dalam nominal")

    currency_rate_lines = fields.One2many('res.currency.rate.line', inverse_name='currency_rate_id', string='currency rate',
                                          required=True,
                                          ondelete='cascade')

    @api.model
    def default_get(self, fields_list):
        res = super(ResCurrencyRate, self).default_get(fields_list)
        vals = []
        for currency in self.env['res.currency'].search([]):
            vals.append((0, 0, {'name': currency.name, 'symbol': currency.symbol, 'tarifbelinominal': 1.0,
                                'tarifbelipersen': 1.0, 'tarifjualnominal': 1.0, 'tarifjualpersen': 1.0, }))
            # res.update(val)
        # vals = (0, 0, {'name': 'IDR', 'tarifbelinominal':1.0 }),
        # (0, 0, {'name': 'USD', 'tarifbelinominal': 1.0})]
        res['currency_rate_lines'] = vals
        return res

    @api.model
    def create(self, vals):        
        move_line = super(ResCurrencyRate, self).create(vals)
        #import pdb
        #pdb.set_trace()
        return move_line

    # def _prepare_move_line_vals(self, quantity=None,reserved_quant=None):
    #     self.ensure_one()
    #
    #     vals = super(StockMove, self)._prepare_move_line_vals(quantity=self.product_uom_qty)
    #     vals= dict(vals,weight=self.weight)
    #     #import pdb
    #     #pdb.set_trace()
    #     return vals


# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ResCurrencyRateLine(models.Model):
    _description = 'res.currency.rate.line'
    #_inherit = 'res.currency.rate.line'
    _name = 'res.currency.rate.line'

    name = fields.Char('Currency', required=True, index=True, copy=False)
    symbol = fields.Char('Symbol', copy=False,)
    rate = fields.Float("rate tengah")

    tarifbelipersen = fields.Float("tarif beli persen")
    tarifbelinominal= fields.Float("tarif beli dalam nominal")
    tarifjualpersen = fields.Float("tarif jual persen")
    tarifjualnominal = fields.Float("tarif beli dalam nominal")
    currency_rate_id = fields.Many2one('res.currency.rate',  string="currency rate detail",
                                    copy=False)

    @api.model
    def create(self, vals):
        move_line = super(ResCurrencyRateLine, self).create(vals)
        #import pdb
        #pdb.set_trace()
        return move_line

    # def _prepare_move_line_vals(self, quantity=None,reserved_quant=None):
    #     self.ensure_one()
    #
    #     vals = super(StockMove, self)._prepare_move_line_vals(quantity=self.product_uom_qty)
    #     vals= dict(vals,weight=self.weight)
    #     #import pdb
    #     #pdb.set_trace()
    #     return vals


