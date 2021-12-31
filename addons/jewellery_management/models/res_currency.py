# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ResCurrency(models.Model):
    _description = 'res.currency'
    _inherit = 'res.currency'

    tarifbelipersen = fields.Float("tarif beli persen")
    tarifbeliharga= fields.Float("tarif dalam nominal")
    tarifjualpersen = fields.Float("tarif jual persen")
    tarifjualharga = fields.Float("tarif dalam nominal")


    @api.model
    def create(self, vals):        
        move_line = super(ResCurrency, self).create(vals)
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

