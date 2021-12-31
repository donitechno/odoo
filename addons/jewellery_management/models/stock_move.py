# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):    
    _description = 'Stock Move'
    _inherit = 'stock.move'

    tarif = fields.Float("Tarif", digits=dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits=dp.get_precision('Stock Weight'))
    nilaimurni = fields.Float("Nilai Murni", digits=dp.get_precision('Stock Weight'), store=True)
    nilaikonversi = fields.Float("Nilai Konversi", digits=dp.get_precision('Stock Weight'), store=True)

    @api.model
    def create(self, vals):        
        move_line = super(StockMove, self).create(vals)
        #import pdb
        #pdb.set_trace()
        return move_line

    def _prepare_move_line_vals(self, quantity=None,reserved_quant=None):
        self.ensure_one()
        
        vals = super(StockMove, self)._prepare_move_line_vals(quantity=self.product_uom_qty)
        vals['nilairiil']= self.nilairiil
        vals['nilaimurni']= self.nilaimurni
        vals['nilaikonversi']= self.nilaikonversi
        #vals= dict(vals,weight=self.weight)
        #import pdb
        #pdb.set_trace()
        return vals


class StockMoveLine(models.Model):
    _inherit ='stock.move.line'

    tarif = fields.Float("Tarif", digits=dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits=dp.get_precision('Stock Weight'))
    nilaimurni = fields.Float("Nilai Murni", digits=dp.get_precision('Stock Weight'), store=True)
    nilaikonversi = fields.Float("Nilai Konversi", digits=dp.get_precision('Stock Weight'), store=True)

    @api.model
    def create(self, vals):        
        move_line = super(StockMoveLine, self).create(vals)
        
        return move_line

  
    