# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):    
    _description = 'Purchase Order'
    _inherit = 'purchase.order'

    weight = fields.Float("Weight", digits= dp.get_precision('Stock Weight'))
    
    


class PurchaseOrderLine(models.Model):    
    _description = 'Purchase Order Line'
    _inherit = 'purchase.order.line'

    @api.depends('nilairiil','product_qty','tarif')
    def _compute_nilaimurni(self):        
        for record in self:
            record.nilaimurni= (record.nilairiil * record.tarif) * record.product_qty
            

    @api.depends('nilaimurni','currency_id')
    def _compute_nilaikonversi(self):       
        if not self.currency_id:
            self.currency_id = self.order_id._default_currency_id()

        for record in self:
            record.nilaikonversi = record.nilaimurni * record.currency_id.tarifbeliharga
            record.price_unit = record.nilaikonversi
            record.sub_total = record.nilaikonversi

    #weight = fields.Float("Weight", digits= dp.get_precision('Stock Weight'))
    tarif = fields.Float("Tarif", digits= dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits= dp.get_precision('Stock Weight'))
    nilaimurni= fields.Float("Nilai Murni", digits= dp.get_precision('Stock Weight'), compute=_compute_nilaimurni, store=True)
    nilaikonversi=fields.Float("Nilai Konversi", digits= dp.get_precision('Stock Weight'), compute= _compute_nilaikonversi, store=True)
  
    #tarif = field.Fields()
    def _prepare_account_move_line(self, move=False):
        vals = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        vals["nilairiil"]= self.nilairiil
        vals["tarif"] = self.tarif
        vals["nilaimurni"] = self.nilaimurni
        vals["nilaikonversi"] = self.nilaikonversi       
        
        return vals

    def _prepare_stock_moves(self, picking):
        template = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)        
        template[0]['nilairiil']=self.nilairiil
        template[0]["tarif"] = self.tarif
        template[0]["nilaimurni"] = self.nilaimurni
        template[0]["nilaikonversi"] = self.nilaikonversi
       
        return template

   
    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if not self.product_id:
    #         return
    #
    #     # Reset date, price and quantity since _onchange_quantity will provide default values
    #     self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    #     self.price_unit = self.product_qty = 0.0
    #
    #
    #
    #     self._product_id_change()
    #
    #     self._suggest_quantity()
    #     self._onchange_quantity()
        
       

    # @api.depends('product_qty', 'price_unit', 'taxes_id','weight')
    # def _compute_amount(self):
    #     for line in self:
    #         vals = line._prepare_compute_all_values()
    #         vals['price_unit']= line.weight * line.order_id.currency_id.rate
    #         taxes = line.taxes_id.compute_all(
    #             vals['price_unit'],
    #             vals['currency_id'],
    #             vals['product_qty'],
    #             vals['product'],
    #             vals['partner'])
    #         line.update({
    #             'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #             'price_total': taxes['total_included'],
    #             'price_subtotal': taxes['total_excluded'],
    #         })
    #
